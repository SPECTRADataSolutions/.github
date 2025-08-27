#!/usr/bin/env python3
"""SPECTRA Initiative Lessons Generator (clean implementation)

Generates inferred lessons for a new initiative by comparing it to historical initiatives
indexed by initiative_lessons_indexer.py.
"""
from __future__ import annotations

import json
import math
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, DefaultDict, Dict, List, Tuple, Iterable, cast

RE_WORD = re.compile(r"\b[a-zA-Z]{3,}\b")
STOP_WORDS = {
    "the",
    "and",
    "for",
    "are",
    "but",
    "not",
    "you",
    "all",
    "can",
    "had",
    "her",
    "was",
    "one",
    "our",
    "out",
    "day",
    "get",
    "has",
    "him",
    "his",
    "how",
    "man",
    "new",
    "now",
    "old",
    "see",
    "two",
    "way",
    "who",
    "boy",
    "did",
    "its",
    "let",
    "put",
    "say",
    "she",
    "too",
    "use",
    "this",
    "that",
    "with",
    "have",
    "will",
    "from",
    "they",
    "been",
    "said",
    "each",
    "which",
    "their",
    "time",
    "would",
    "there",
    "could",
    "other",
}
LESSON_CATEGORIES = [
    "risks",
    "mitigations",
    "root_causes",
    "success_factors",
    "recommendations",
    "common_challenges",
]

Vector = Dict[str, float]
Lessons = Dict[str, List[str]]


@dataclass(slots=True)
class HistoryEntry:
    raw: Dict[str, Any]
    vector: Vector


class InitiativeLessonsGenerator:
    def __init__(
        self, history_path: str = "analytics/initiatives-history.jsonl"
    ) -> None:
        self.history_path = Path(history_path)
        self.history: List[HistoryEntry] = []
        self.vocabulary: set[str] = set()
        self.idf: Dict[str, float] = {}

    def generate_lessons(
        self, new_initiative: Dict[str, Any], max_similar: int = 5
    ) -> Dict[str, Any]:
        if not self.history and not self._load_history():
            return {"error": "No historical data available"}
        query_vec = self._compute_tf_idf(
            self._compose_text_from_initiative(new_initiative)
        )
        scored = self._score_similar(query_vec)
        if not scored:
            return {
                "lessons": {"message": "No similar initiatives found in history"},
                "confidence": 0.0,
                "similar_count": 0,
                "similar_initiatives": [],
            }
        top = scored[:max_similar]
        consolidated = self._consolidate_lessons(top)
        avg_sim = sum(s for _, s in top) / len(top)
        confidence = min(avg_sim * 100, 95.0)
        return {
            "lessons": consolidated,
            "confidence": confidence,
            "similar_count": len(top),
            "similar_initiatives": [
                {
                    "title": e.get("title"),
                    "archetype": e.get("archetype"),
                    "domain": e.get("domain"),
                    "similarity": round(score, 4),
                }
                for e, score in top
            ],
        }

    # Loading -------------------------------------------------------------
    def _load_history(self) -> bool:
        if not self.history_path.exists():
            print(f"⚠️ History file not found: {self.history_path}")
            return False
        self.history.clear()
        self.vocabulary.clear()
        self.idf.clear()
        raw_entries: List[Dict[str, Any]] = []
        with self.history_path.open("r", encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError:
                    continue
                lessons_any = obj.setdefault("lessons", {})
                if not isinstance(lessons_any, dict):
                    lessons_any = {}
                    obj["lessons"] = lessons_any
                lessons = cast(Lessons, lessons_any)
                for cat in LESSON_CATEGORIES:
                    existing = lessons.setdefault(cat, [])
                    if not isinstance(existing, list):
                        lessons[cat] = []
                raw_entries.append(obj)
        for obj in raw_entries:
            self.vocabulary.update(self._tokenize(self._compose_text_from_history(obj)))
        self._compute_idf(raw_entries)
        for obj in raw_entries:
            vec = self._compute_tf_idf(self._compose_text_from_history(obj))
            self.history.append(HistoryEntry(raw=obj, vector=vec))
        print(f"📚 Loaded {len(self.history)} historical initiatives")
        return True

    # Text composition ----------------------------------------------------
    def _compose_text_from_history(self, obj: Dict[str, Any]) -> str:
        lessons_raw = obj.get("lessons", {})
        if not isinstance(lessons_raw, dict):
            lessons_raw = {}
        lessons_dict = cast(Dict[str, Any], lessons_raw)
        all_lessons: List[str] = []
        for cat in LESSON_CATEGORIES:
            cat_list = lessons_dict.get(cat, [])
            all_lessons.extend(self._coerce_str_list(cat_list))
        lessons_blob = " ".join(all_lessons)
        keywords_list = obj.get("similarity_keywords", [])
        keywords = self._coerce_str_list(keywords_list)
        parts: List[str] = [
            str(obj.get("title", "")),
            str(obj.get("archetype", "")),
            str(obj.get("domain", "")),
            " ".join(keywords),
            lessons_blob,
        ]
        return " ".join(parts).lower()

    def _compose_text_from_initiative(self, spec: Dict[str, Any]) -> str:
        capability_areas = self._coerce_str_list(spec.get("capabilityAreas", []))
        parts: List[str] = [
            str(spec.get("initiativeTitle", spec.get("title", ""))),
            str(spec.get("archetype", "")),
            str(spec.get("domain", "")),
            str(spec.get("purpose", "")),
            " ".join(capability_areas),
        ]
        return " ".join(parts).lower()

    # Vectorisation -------------------------------------------------------
    def _tokenize(self, text: str) -> List[str]:
        return [w for w in RE_WORD.findall(text) if w not in STOP_WORDS]

    def _coerce_str_list(self, value: Any) -> List[str]:
        """Normalise arbitrary JSON value into a list[str]."""
        if isinstance(value, list):
            return [
                str(v).strip()
                for v in cast(List[Any], value)
                if isinstance(v, (str, int, float)) and str(v).strip()
            ]
        if isinstance(value, (str, int, float)):
            s = str(value).strip()
            return [s] if s else []
        return []

    def _compute_idf(self, entries: List[Dict[str, Any]]) -> None:
        total = len(entries) or 1
        df: Dict[str, int] = defaultdict(int)
        for obj in entries:
            for w in set(self._tokenize(self._compose_text_from_history(obj))):
                df[w] += 1
        for w in self.vocabulary:
            freq = df.get(w, 0)
            self.idf[w] = math.log((1 + total) / (1 + freq)) + 1.0

    def _compute_tf_idf(self, text: str) -> Vector:
        words = self._tokenize(text)
        counts = Counter(words)
        total = len(words) or 1
        vec: Vector = {}
        for w, cnt in counts.items():
            if w in self.idf:
                vec[w] = (cnt / total) * self.idf[w]
        return vec

    # Similarity ----------------------------------------------------------
    def _cosine(self, v1: Vector, v2: Vector) -> float:
        if not v1 or not v2:
            return 0.0
        common = set(v1.keys()) & set(v2.keys())
        if not common:
            return 0.0
        dot = sum(v1[k] * v2[k] for k in common)
        mag1 = math.sqrt(sum(x * x for x in v1.values()))
        mag2 = math.sqrt(sum(x * x for x in v2.values()))
        if not mag1 or not mag2:
            return 0.0
        return dot / (mag1 * mag2)

    def _score_similar(self, query_vec: Vector) -> List[Tuple[Dict[str, Any], float]]:
        scored: List[Tuple[Dict[str, Any], float]] = []
        for entry in self.history:
            lessons = entry.raw.get("lessons", {})
            if not any(lessons.get(cat) for cat in LESSON_CATEGORIES):
                continue
            sim = self._cosine(query_vec, entry.vector)
            if sim > 0.1:
                scored.append((entry.raw, min(sim, 1.0)))
        scored.sort(key=lambda t: t[1], reverse=True)
        return scored

    # Consolidation -------------------------------------------------------
    def _consolidate_lessons(
        self, similar: List[Tuple[Dict[str, Any], float]]
    ) -> Dict[str, Any]:
        grouped: DefaultDict[str, List[Tuple[str, float]]] = defaultdict(list)
        for obj, weight in similar:
            lessons_obj_raw = obj.get("lessons", {})
            if not isinstance(lessons_obj_raw, dict):
                continue
            lessons_obj: Dict[str, Any] = cast(Dict[str, Any], lessons_obj_raw)
            for cat in LESSON_CATEGORIES:
                cat_items_any: Any = lessons_obj.get(cat, [])
                for text in self._coerce_str_list(cat_items_any):
                    if text:
                        grouped[cat].append((text, weight))
        consolidated: Dict[str, List[str]] = {c: [] for c in LESSON_CATEGORIES}
        for cat, items in grouped.items():
            bucket: Dict[str, Tuple[str, float]] = {}
            for text, w in items:
                key = " ".join(text.split()[:4]).lower()
                current = bucket.get(key)
                if (not current) or (w > current[1]):
                    bucket[key] = (text, w)
            top = sorted(bucket.values(), key=lambda t: t[1], reverse=True)[:3]
            consolidated[cat] = [t[0] for t in top]
        if any(consolidated[c] for c in LESSON_CATEGORIES):
            consolidated["summary"] = self._summary_recommendations(consolidated)
        return consolidated

    def _summary_recommendations(self, lessons: Dict[str, List[str]]) -> List[str]:
        recs: List[str] = []
        if lessons.get("risks"):
            recs.append(
                f"Prioritise mitigation planning for {len(lessons['risks'])} risks"
            )
        if lessons.get("mitigations"):
            recs.append("Adopt proven mitigations early")
        if lessons.get("success_factors"):
            recs.append("Embed success factors into planning checkpoints")
        return recs[:3]


def main() -> int:  # pragma: no cover
    import sys, argparse

    parser = argparse.ArgumentParser(
        description="Generate initiative lessons from history corpus"
    )
    parser.add_argument("--history", default="analytics/initiatives-history.jsonl")
    parser.add_argument("--max", type=int, default=5)
    args = parser.parse_args()
    spec: Dict[str, Any] = {
        "initiativeTitle": "sampleLessonsGeneration",
        "archetype": "Guidance",
        "domain": "governance",
        "purpose": "Demonstrate lessons generation pipeline",
        "capabilityAreas": ["testing", "automation"],
    }
    if not sys.stdin.isatty():
        raw = sys.stdin.read().strip()
        if raw:
            try:
                spec = json.loads(raw)
            except json.JSONDecodeError:
                print("⚠️ Invalid JSON from STDIN; using sample spec.")
    gen = InitiativeLessonsGenerator(history_path=args.history)
    result = gen.generate_lessons(spec, max_similar=args.max)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if "error" not in result else 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())

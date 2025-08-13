#!/usr/bin/env python3
"""
SPECTRA Initiative Lessons Generator

This script generates lessons for new initiatives by finding similar past
initiatives using TF-IDF similarity matching and extracting relevant risks,
mitigations, and recommendations.

Framework as Law: This script enforces lessons extraction standards.
"""

import json
import re
import math
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, List, Tuple, Optional


class InitiativeLessonsGenerator:
    def __init__(self, history_path: str = "analytics/initiatives-history.jsonl"):
        self.history_path = Path(history_path)
        self.history_data = []
        self.vocabulary = set()
        self.idf_cache = {}
        
    def load_history(self) -> bool:
        """Load initiative history data."""
        if not self.history_path.exists():
            print(f"⚠️ History file not found: {self.history_path}")
            return False
        
        try:
            with open(self.history_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        entry = json.loads(line)
                        self.history_data.append(entry)
            
            print(f"📚 Loaded {len(self.history_data)} historical initiatives")
            self._build_vocabulary()
            return True
            
        except Exception as e:
            print(f"❌ Error loading history: {e}")
            return False
    
    def generate_lessons(self, new_initiative: Dict[str, str], max_similar: int = 5) -> Dict:
        """Generate lessons for a new initiative based on similar past ones."""
        if not self.history_data:
            if not self.load_history():
                return {"error": "No historical data available"}
        
        print(f"🔍 Generating lessons for: {new_initiative.get('initiativeTitle', 'Unknown')}")
        
        # Find similar initiatives
        similar_initiatives = self._find_similar_initiatives(new_initiative, max_similar)
        
        if not similar_initiatives:
            return {
                "lessons": {"message": "No similar initiatives found in history"},
                "confidence": 0.0,
                "similar_count": 0
            }
        
        # Extract consolidated lessons
        lessons = self._extract_consolidated_lessons(similar_initiatives)
        
        # Calculate confidence based on similarity scores
        avg_similarity = sum(score for _, score in similar_initiatives) / len(similar_initiatives)
        confidence = min(avg_similarity * 100, 95.0)  # Cap at 95%
        
        return {
            "lessons": lessons,
            "confidence": confidence,
            "similar_count": len(similar_initiatives),
            "similar_initiatives": [
                {
                    "title": init["title"],
                    "archetype": init["archetype"],
                    "domain": init["domain"],
                    "similarity": score
                }
                for init, score in similar_initiatives
            ]
        }
    
    def _build_vocabulary(self):
        """Build vocabulary from all historical initiatives."""
        print("🏗️ Building vocabulary for similarity matching...")
        
        for entry in self.history_data:
            # Combine all text fields for vocabulary
            text_parts = [
                entry.get("title", ""),
                entry.get("archetype", ""),
                entry.get("domain", ""),
                " ".join(entry.get("similarity_keywords", [])),
                json.dumps(entry.get("lessons", {}))
            ]
            
            text = " ".join(text_parts).lower()
            words = self._tokenize(text)
            self.vocabulary.update(words)
        
        print(f"📝 Built vocabulary with {len(self.vocabulary)} unique terms")
        self._compute_idf()
    
    def _compute_idf(self):
        """Compute IDF (Inverse Document Frequency) for all terms."""
        print("📊 Computing IDF scores...")
        
        # Count document frequencies
        doc_frequencies = defaultdict(int)
        total_docs = len(self.history_data)
        
        for entry in self.history_data:
            text_parts = [
                entry.get("title", ""),
                entry.get("archetype", ""),
                entry.get("domain", ""),
                " ".join(entry.get("similarity_keywords", []))
            ]
            text = " ".join(text_parts).lower()
            words = set(self._tokenize(text))  # Unique words in this document
            
            for word in words:
                doc_frequencies[word] += 1
        
        # Compute IDF scores
        for word in self.vocabulary:
            df = doc_frequencies.get(word, 1)  # Add-one smoothing
            idf = math.log(total_docs / df)
            self.idf_cache[word] = idf
    
    def _tokenize(self, text: str) -> List[str]:
        """Tokenize text into words."""
        # Simple tokenization - extract alphanumeric words
        words = re.findall(r'\b[a-zA-Z]{2,}\b', text.lower())
        
        # Filter out common stop words
        stop_words = {
            'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'had',
            'her', 'was', 'one', 'our', 'out', 'day', 'get', 'has', 'him', 'his',
            'how', 'man', 'new', 'now', 'old', 'see', 'two', 'way', 'who', 'boy',
            'did', 'its', 'let', 'put', 'say', 'she', 'too', 'use', 'this', 'that',
            'with', 'have', 'will', 'from', 'they', 'been', 'said', 'each', 'which',
            'their', 'time', 'would', 'there', 'could', 'other'
        }
        
        return [word for word in words if word not in stop_words and len(word) > 2]
    
    def _compute_tf_idf(self, text: str) -> Dict[str, float]:
        """Compute TF-IDF vector for given text."""
        words = self._tokenize(text)
        word_counts = Counter(words)
        total_words = len(words)
        
        tf_idf_vector = {}
        
        for word in self.vocabulary:
            # Term Frequency
            tf = word_counts.get(word, 0) / max(total_words, 1)
            
            # IDF
            idf = self.idf_cache.get(word, 0)
            
            # TF-IDF
            tf_idf = tf * idf
            if tf_idf > 0:
                tf_idf_vector[word] = tf_idf
        
        return tf_idf_vector
    
    def _cosine_similarity(self, vec1: Dict[str, float], vec2: Dict[str, float]) -> float:
        """Compute cosine similarity between two TF-IDF vectors."""
        # Get common terms
        common_terms = set(vec1.keys()) & set(vec2.keys())
        
        if not common_terms:
            return 0.0
        
        # Dot product
        dot_product = sum(vec1[term] * vec2[term] for term in common_terms)
        
        # Magnitudes
        magnitude1 = math.sqrt(sum(val ** 2 for val in vec1.values()))
        magnitude2 = math.sqrt(sum(val ** 2 for val in vec2.values()))
        
        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0
        
        return dot_product / (magnitude1 * magnitude2)
    
    def _find_similar_initiatives(self, new_initiative: Dict[str, str], max_similar: int) -> List[Tuple[Dict, float]]:
        """Find most similar historical initiatives."""
        # Prepare text for new initiative
        new_text_parts = [
            new_initiative.get("initiativeTitle", ""),
            new_initiative.get("archetype", ""),
            new_initiative.get("domain", ""),
            new_initiative.get("purpose", ""),
            " ".join(new_initiative.get("capabilityAreas", []) or [])
        ]
        new_text = " ".join(new_text_parts).lower()
        new_vector = self._compute_tf_idf(new_text)
        
        # Compute similarities
        similarities = []
        
        for entry in self.history_data:
            # Skip if no lessons available
            if not entry.get("lessons") or not any(entry["lessons"].values()):
                continue
                
            # Prepare text for historical initiative
            hist_text_parts = [
                entry.get("title", ""),
                entry.get("archetype", ""),
                entry.get("domain", ""),
                " ".join(entry.get("similarity_keywords", []))
            ]
            hist_text = " ".join(hist_text_parts).lower()
            hist_vector = self._compute_tf_idf(hist_text)
            
            # Compute similarity
            similarity = self._cosine_similarity(new_vector, hist_vector)
            
            # Boost similarity for exact archetype/domain matches
            if entry.get("archetype") == new_initiative.get("archetype"):
                similarity += 0.1
            if entry.get("domain") == new_initiative.get("domain"):
                similarity += 0.15
            
            similarities.append((entry, similarity))
        
        # Sort by similarity and return top matches
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        # Filter out very low similarities (< 0.1)
        filtered_similarities = [(entry, score) for entry, score in similarities if score > 0.1]
        
        return filtered_similarities[:max_similar]
    
    def _extract_consolidated_lessons(self, similar_initiatives: List[Tuple[Dict, float]]) -> Dict:
        """Extract and consolidate lessons from similar initiatives."""
        consolidated = {
            "risks": [],
            "mitigations": [],
            "recommendations": [],
            "success_factors": [],
            "common_challenges": []
        }
        
        # Weight lessons by similarity score
        weighted_lessons = defaultdict(list)
        
        for entry, similarity in similar_initiatives:
            lessons = entry.get("lessons", {})
            
            for category in consolidated.keys():
                category_lessons = lessons.get(category, [])
                for lesson in category_lessons:
                    if lesson and lesson.strip():
                        weighted_lessons[category].append((lesson.strip(), similarity))
        
        # Consolidate and rank lessons
        for category in consolidated.keys():
            lessons_with_weights = weighted_lessons[category]
            
            if not lessons_with_weights:
                continue
            
            # Group similar lessons and sum weights
            lesson_weights = defaultdict(float)
            for lesson, weight in lessons_with_weights:
                # Simple grouping by first few words
                key = " ".join(lesson.split()[:4]).lower()
                lesson_weights[key] = max(lesson_weights[key], weight)
            
            # Sort by weight and select top lessons
            sorted_lessons = sorted(lesson_weights.items(), key=lambda x: x[1], reverse=True)
            
            # Get original lessons for top weighted keys
            top_lessons = []
            for key, weight in sorted_lessons[:3]:  # Top 3 per category
                # Find best matching original lesson
                best_lesson = None
                best_score = 0
                
                for lesson, score in lessons_with_weights:
                    lesson_key = " ".join(lesson.split()[:4]).lower()
                    if lesson_key == key and score > best_score:
                        best_lesson = lesson
                        best_score = score
                
                if best_lesson:
                    top_lessons.append(best_lesson)
            
            consolidated[category] = top_lessons
        
        # Add summary recommendations
        if any(consolidated.values()):
            consolidated["summary"] = self._generate_summary_recommendations(consolidated, similar_initiatives)
        
        return consolidated
    
    def _generate_summary_recommendations(self, lessons: Dict, similar_initiatives: List[Tuple[Dict, float]]) -> List[str]:
        """Generate summary recommendations based on extracted lessons."""
        recommendations = []
        
        # Count archetype/domain patterns
        archetype_counts = Counter()
        domain_counts = Counter()
        
        for entry, _ in similar_initiatives:
            archetype_counts[entry.get("archetype", "Unknown")] += 1
            domain_counts[entry.get("domain", "unknown")] += 1
        
        # Generate pattern-based recommendations
        most_common_archetype = archetype_counts.most_common(1)
        if most_common_archetype:
            arch, count = most_common_archetype[0]
            if count > 1:
                recommendations.append(f"Pattern: {arch} initiatives often face similar challenges - review {arch}-specific best practices")
        
        # Risk-based recommendations
        if lessons.get("risks"):
            recommendations.append(f"Priority: Address the {len(lessons['risks'])} identified risks early in planning phase")
        
        # Mitigation recommendations
        if lessons.get("mitigations"):
            recommendations.append(f"Implement proven mitigations from {len(similar_initiatives)} similar initiatives")
        
        return recommendations[:3]  # Limit to most important


def main():
    """Main entry point for testing."""
    generator = InitiativeLessonsGenerator()
    
    # Test with a sample new initiative
    test_initiative = {
        "initiativeTitle": "testLessonsGeneration",
        "archetype": "Guidance",
        "domain": "governance",
        "purpose": "Test the lessons generation system",
        "capabilityAreas": ["testing", "automation"]
    }
    
    result = generator.generate_lessons(test_initiative)
    
    print("\n🎯 Generated Lessons:")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    return 0 if "error" not in result else 1


if __name__ == "__main__":
    exit(main())
# 🎴 Spectra Discovery Deck

Use this lightweight questionnaire whenever a new idea appears. It’s playful enough to keep ideation fun, but structured so I can turn the answers directly into initiatives, epics, issues, and Project v2 schemas.

---

## 1. Elevator Pitch (1–2 sentences)
- **Name / Codename**
- **Why now?**
- **North star metric or headline outcome?**

## 2. Initiative Canvas
| Field | Prompt |
| --- | --- |
| **Mission Statement** | What problem do we end forever? |
| **Target Users** | Who benefits? Personas or teams. |
| **Non-negotiables** | Compliance, platforms, integration constraints. |
| **Out of Scope** | Anything deliberately excluded. |

## 3. MoSCoW Snapshot
List features or deliverables in each bucket.
- **Must:** critical for launch.
- **Should:** important but can slip a sprint.
- **Could:** delight tier / stretch.
- **Won’t (for now):** explicitly parked.

> Tip: If you’re unsure where something sits, note the debate so we can revisit.

## 4. Estimation Mini-Games
Pick at least one so we capture complexity signals:
- **Planning Poker:** Give each workstream a story-point ballpark (1, 2, 3, 5, 8, 13).
- **T-Shirt Sizes:** XS / S / M / L / XL for effort or unknowns.
- **Confidence Vote:** 1–5 scale on how certain you are about the estimate.

Record the game you chose and the results. Example:
```
Workstream "Voice Shell": Planning Poker result = 8, confidence = 2/5.
```

## 5. Workstreams & Threads
For each major slice (becomes an Epic/parent issue):
1. **Name**
2. **Objective**
3. **Definition of Done**
4. **Primary repo(s)** and stakeholders
5. **Dependencies / Sequencing**
6. **Telemetry or evidence required (Spectrafy, dashboards, alerts)**

## 6. Ideation Prompts (Optional but fun)
- **Lightning Round:** jot three wild ideas in 2 minutes (mind dump).
- **Risk Flip:** what’s the riskiest assumption? how would we test it cheaply?
- **Magic Wand:** if money/time were infinite, what would the ultimate version ship?

## 7. Tooling & Rituals
- **Collaboration style:** async updates? weekly sync?
- **Games to keep running:** estimation poker, retro cards, dependency bingo, etc.
- **Automation asks:** e.g., “auto-tag issues when dependency_state changes.”

## 8. Evidence Checklist (Golden Tick)
Tick each box to signal we’re scaffold-ready:
- [ ] Mission + success metrics defined
- [ ] MoSCoW buckets filled (even if empty list)
- [ ] At least one estimation game recorded
- [ ] Workstreams documented with DoD + dependencies
- [ ] Telemetry / governance expectations captured
- [ ] Risks + out-of-scope written down

When every box is checked, drop this file (or a snapshot of answers) alongside the manifest request and I can confidently scaffold the full project hierarchy.

---

### Usage
1. Duplicate this deck (Markdown, Notion, paper—anything works).
2. Fill it in conversationally; emojis and sketches welcome.
3. Share it back with “Golden Tick ✅” once all evidence boxes are marked.
4. I’ll ingest the answers and emit: initiative issue, epics, tasks, manifest updates, and Project schema.

Let’s keep discovery playful **and** Spectra-grade. ✨

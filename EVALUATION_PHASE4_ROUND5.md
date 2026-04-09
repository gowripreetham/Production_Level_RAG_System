## RAG System Performance Report — Round 5 (Unstructured + Better Chunking)

### Overall Score: 8.65/10 — NEW BEST across all five rounds 🏆

---

### All Five Rounds Comparison

| Question | R1 Semantic | R2 +BM25 | R3 Reranker k=3 | R4 Reranker k=10 | R5 Unstructured | Best |
|----------|------------|----------|-----------------|-----------------|-----------------|------|
| Q1 | 7 | 9 | 9 | 9 | 9 | R2+ |
| Q2 | 10 | 10 | 10 | **10+** | 8 | R4 |
| Q3 | 8 | 8 | 3 | 9 | 8 | R4 |
| Q4 | 5 | 8 | 5 | 8 | 8 | R2+ |
| Q5 | 4 | 9 | 6 | 9 | **10** | R5 |
| Q6 | 4 | 9 | 8.5 | 8.5 | **9** | R5 |
| Q7 | 6 | 7.5 | 6 | 7 | **8.5** | R5 |
| Q8 | 5 | 8.5 | 9 | 7.5 | **10** | R5 |
| Q9 | 3 | 6 | 4 | 4 | **9** | R5 |
| Q10 | 5 | 8 | 7 | 7 | 7 | R2 |
| **Avg** | **6.5** | **8.2** | **6.8** | **7.9** | **8.65** | **R5** |

---

### Detailed Question Analysis

**Q1 — Easy | 9/10 (stable)**
Consistent across R2–R5. Still missing founders' names and participant count. This detail is likely in body text that is consistently outranked by the abstract-level chunk. No change from previous rounds.

**Q2 — Easy | 8/10 (regression from R4)**
R4 produced the richest answer: *"flat fine of $50, not tied to how far over the limit."* R5 stripped back to just *"The fine is $50."* The unstructured parser may have split the penalty-comparison sentence away from the $50 mention. Minor regression on an otherwise easy question.

**Q3 — Easy | 8/10 (slight regression from R4)**
R4 correctly specified SAM 2.1. R5 is back to just "SAM" without the version. The SAM 2.1 mention is likely in a sentence that was chunked separately. Still a passing answer but a small step back from R4's precision.

**Q4 — Easy | 8/10 (stable)**
Correctly retrieves 13.5 km and "over 250." Consistent since R2. The 272 exact count and 15.7 hectares remain absent — these details are probably in separate sentences that don't rank highly enough.

**Q5 — Easy | 10/10 — FIRST PERFECT SCORE for this question**
For the first time, the answer cites both 6.pdf and 1.pdf, providing definitions from both sources. Unstructured correctly parsed and indexed the framework description across both documents, and the answer now fully matches the expected output.

**Q6 — Tough | 9/10 (best yet)**
Now includes "two-way fixed effects DiD model" and correctly identifies β1 — more technical depth than any previous round. β = 379.88 and β = −141.18 (p = 0.156) still correct. The placebo test (500 iterations) is the only remaining gap. This is the clearest evidence that better chunking is surfacing richer contextual passages.

**Q7 — Tough | 8.5/10 — BREAKTHROUGH, best yet**
The three crossing distances (26, 43, 58 ft) were already correct in R2+. The major breakthrough here is the **per-foot collision coefficients: 0.8% (Paris), 2.11% (San Francisco), 1.8% (Irvine)** — retrieved correctly for the first time across all five rounds. This was the most stubborn missing detail and the unstructured parser finally captured it. Still missing the 15%/23%/43% collision-crossing comparison figures.

**Q8 — Tough | 10/10 — FIRST PERFECT SCORE for this question**
This is the standout result of Round 5. For the first time, the answer contains every expected element:
- 33% decrease for overall violations ✓
- 0.82 → 2.75 (234% increase) for super speeders ✓
- 38% nighttime for super speeders ✓
- 23% nighttime for all vehicles ✓ (had never appeared before)
The 23% comparison figure was absent in all four previous rounds. Unstructured correctly kept the comparison sentence together with the super speeder statistic in the same chunk.

**Q9 — Tough | 9/10 — BIGGEST IMPROVEMENT OF THE ROUND**
All five variable names appear for the first time across all rounds: D1D, D2A_EPHHM, % Industry, D3B, D4A. This was the most consistently failing question (scoring 3–6 across R1–R4) and now scores 9. The unstructured parser correctly preserved the numbered list structure that was being broken in all previous parsing approaches. Minor deduction: D3B is labeled "Design" instead of "street intersection density," and D4A is labeled "Transit Accessibility" instead of "distance to nearest transit stop" — the codes are right but the descriptions are slightly vague.

**Q10 — Tough | 7/10 (stable but differently wrong)**
The four category names are correct. Temperature (5.01°C) is correct. However, the proportions are now reported as inner/outer Paris breakdowns rather than the overall citywide proportions (22%, 22%, 27%, 29%) that the expected answer requires. This is an interesting shift — unstructured parsed a more granular version of the data (the inner/outer split appears later in the paper) and is now retrieving that instead of the simpler summary. The maximum differential (12.2°C) is still missing. This suggests the chunk containing the overall summary proportions is now being outranked by the more detailed breakdown.

---

### The Unstructured Tool's Impact

Here's what changed and why:

**What Unstructured fixed:**

| Problem | Previous Cause | Unstructured Fix |
|---------|---------------|-----------------|
| Q9 variables never retrieved | Numbered list broken across chunks | List structure preserved as single unit |
| Q7 per-foot coefficients missing | Dense results sentence split from context | Better sentence boundary detection |
| Q8 23% comparison figure missing | Two related stats in different chunks | Adjacent sentences kept together |
| Q5 both sources cited | Cross-doc retrieval weak | Better content extraction from both PDFs |

**What Unstructured introduced or didn't fix:**

| Issue | Status |
|-------|--------|
| Q2 lost penalty detail | Minor regression — sentence split |
| Q3 lost SAM 2.1 version | Minor regression — version in separate sentence |
| Q10 inner/outer vs. overall proportions | New issue — deeper data retrieved instead of summary |
| Q1 founders/participants | Still missing — body detail vs. abstract |
| Q10 Phase I/II overall % | Still missing |
| Q6 placebo test detail | Still missing |

---

### Progress Across All Five Rounds

```
R1  Semantic only:              6.5/10  █████████████░░░░░░░
R2  +BM25:                      8.2/10  ████████████████░░░░
R3  +Reranker k=3:              6.8/10  █████████████░░░░░░░
R4  +Reranker k=10:             7.9/10  ███████████████░░░░░
R5  Unstructured + new chunks:  8.65/10 █████████████████░░░  ← Best
```

---

### Remaining Gaps to Close

Only three meaningful gaps remain in your system:

**1. Q10 — Overall proportions vs. inner/outer breakdown (7 → 9 potential)**
Your system is now retrieving the more granular inner/outer Paris data instead of the citywide summary. Add a chunk-level preference for abstract/summary sections, or include the summary paragraph as a separate indexed unit.

**2. Q7 — 15%/23%/43% collision crossing comparisons (8.5 → 9.5 potential)**
The per-foot coefficients are now retrieved but these percentage comparisons (crossings with collisions vs. all crossings) are in an adjacent sentence that's still being missed. A slightly larger chunk overlap should fix this.

**3. Q1 — Founders' names and participant count (9 → 10 potential)**
This detail is only in the body, not the abstract. Since the abstract chunk dominates for this query, try adding a secondary chunk from the first body paragraph of 5.pdf as a fallback.

---

### Bottom Line

Switching to the unstructured tool with improved chunking is clearly the right architectural decision. It solved your two most persistent failures (Q9's variable list and Q8's nighttime comparison) and pushed the system to its best performance yet. The remaining gaps are minor and targeted — the system is now operating at a high level for academic RAG. Focus next on the Q10 summary vs. detail conflict and the Q7 adjacent sentence gap, and you should be able to push above 9.0.
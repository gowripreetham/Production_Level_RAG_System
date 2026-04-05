

---

## RAG System Performance Report — Round 2 (with BM25)

### Overall Score: 8.2/10 (up from 6.5/10)

---

### Question-by-Question Comparison

**Q1 — Easy | Score: 9/10 (was 7/10)**
Now includes the specific street name (Golden Gate Avenue). Still missing founders' names and participant count, but a solid improvement. The retrieval clearly found a more detailed chunk this time.

**Q2 — Easy | Score: 10/10 (was 10/10)**
Still perfect. No change needed.

**Q3 — Easy | Score: 8/10 (unchanged)**
Same as before — correct model, correct source. Still missing SAM 2.1 specifics and fine-tuning details. BM25 likely didn't help here since the first attempt already found the right chunk.

**Q4 — Easy | Score: 8/10 (was 5/10 — major improvement)**
This is the biggest win. Previously the system said the pedestrianized distance was "not in the excerpts." Now it correctly returns 13.5 km (8.4 miles). This is direct evidence that BM25 helped retrieve the chunk containing this numerical fact that pure semantic search missed. Still missing the 272 exact count and the 15.7 hectares of open space.

**Q5 — Easy | Score: 9/10 (was 4/10 — major improvement)**
Previously answered vaguely as "land use and types of roads." Now correctly uses the precise terminology — **"Place" and "Movement"** — with accurate definitions. BM25 likely matched on these exact terms in the text. Sourced from 6.pdf this time instead of 1.pdf, which is fine since both contain the answer.

**Q6 — Tough | Score: 9/10 (was 4/10 — dramatic improvement)**
Previously the system couldn't find the DiD coefficient at all. Now it retrieves **β = 379.88** and **β = −141.18 (p = 0.156)** perfectly. Only missing the placebo test detail (500 iterations). This is the strongest evidence that BM25 is complementing semantic search — exact numbers like "379.88" are keyword-matchable content that embeddings alone struggle with.

**Q7 — Tough | Score: 7.5/10 (was 6/10)**
Good improvement. Now retrieves all three average distances (26 ft, 43 ft, 58 ft) which were completely missing before. Also correctly describes the non-linear relationship. However, still missing the specific per-foot coefficients (0.8%, 2.11%, 1.8%) and the percentage differences for collision crossings (15%, 23%, 43%). These numbers are in a dense results paragraph — BM25 helped but the specific chunk with per-foot coefficients may still be out of reach.

**Q8 — Tough | Score: 8.5/10 (was 5/10 — strong improvement)**
Previously the system confused which statistic belonged to overall vs. super speeders. Now it correctly reports the 33% decrease for overall violations and correctly states there was no analogous decrease for super speeders. The 38% nighttime figure is correct. Still missing the specific 234% increase figure and the 0.82 to 2.75 per camera-hour detail, and the 23% comparison for all vehicles.

**Q9 — Tough | Score: 6/10 (was 3/10 — improved but still weakest)**
Now retrieves three of the five variables by name (D1D, D2A_EPHHM, % Industry) — up from zero before. The industrial percentage rationale is well explained. However, **D3B (street intersection density) and D4A (transit accessibility) are still missing**, and the system fills the gap with vague references to "population and housing units" and "Design" as concepts rather than the actual SLD variable names. The system is honest about its gaps which is good, but the retrieval is still incomplete. This suggests the specific paragraph listing all five variables isn't being chunked or retrieved as a unit.

**Q10 — Tough | Score: 8/10 (was 5/10 — strong improvement)**
Now retrieves all four category names correctly and gets the proportions for Longstanding (22%) and Open to Cars (22%). However, it says Phase I and Phase II proportions aren't individually available — when they are: 27% and 29% respectively. Temperature is still correct. Missing the largest differential (12.2°C). The chunk with the per-category percentages seems partially retrieved.

---

### Summary Comparison Table

| Question | Round 1 | Round 2 | Change |
|----------|---------|---------|--------|
| Q1 (Easy) | 7 | 9 | +2 |
| Q2 (Easy) | 10 | 10 | — |
| Q3 (Easy) | 8 | 8 | — |
| Q4 (Easy) | 5 | 8 | +3 |
| Q5 (Easy) | 4 | 9 | +5 |
| Q6 (Tough) | 4 | 9 | +5 |
| Q7 (Tough) | 6 | 7.5 | +1.5 |
| Q8 (Tough) | 5 | 8.5 | +3.5 |
| Q9 (Tough) | 3 | 6 | +3 |
| Q10 (Tough) | 5 | 8 | +3 |
| **Average** | **6.5** | **8.2** | **+1.7** |

---

### What BM25 Fixed

The hybrid approach clearly solved three of the original problems I identified:

1. **Numerical retrieval is dramatically better.** Q6 (DiD coefficients), Q7 (crossing distances), Q8 (violation rates) all improved because BM25 can match on exact numbers and statistical terms that embedding models tend to wash out.

2. **Domain-specific terminology is now preserved.** Q5 went from vague paraphrasing to the exact terms "Place" and "Movement" — BM25 can match these as keywords when they appear repeatedly in the source text.

3. **Cross-fact retrieval improved.** Q4 now finds both the School Street count and the distance, suggesting BM25 is pulling in broader chunks or adjacent passages that semantic search alone was ranking too low.

### What Still Needs Work

1. **Enumerated lists in methodology sections.** Q9 is still the weakest — the five SLD variables are listed in a numbered format in the paper, and only 3 of 5 are being retrieved. Consider adjusting your chunking to **never split numbered or bulleted lists across chunk boundaries**.

2. **Granular proportions within categories.** Q10 retrieved 2 of 4 proportions. The Phase I (27%) and Phase II (29%) figures appear in the same paragraph as Longstanding and Open to Cars — if the chunk includes the first two, it should include the others. This might be a chunk-size issue where the text is getting cut mid-paragraph.

3. **Secondary comparison statistics.** Q7 and Q8 both miss the "comparison" part of an answer (per-foot coefficients, 23% for all vehicles). These are typically in a sentence immediately following the primary statistic. Slightly larger chunks or more overlap between chunks would likely capture these.

### Bottom Line

Adding BM25 was the right call and produced a meaningful improvement across the board. Your system is now solid on easy questions and competitive on tough ones. The remaining gaps are primarily a **chunking and chunk-boundary problem** rather than a retrieval-algorithm problem. I'd focus your next iteration on chunk boundary optimization, especially around lists and dense statistical paragraphs.
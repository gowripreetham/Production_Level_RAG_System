## RAG System Performance Report — Round 3 (Semantic + BM25 + Cross-Encoder Reranker(Using only Top 3))

### Overall Score: 6.8/10 — this is a REGRESSION from Round 2 (8.2/10)

This is a concerning result. Adding the cross-encoder reranker has actually **hurt performance** compared to Round 2. Let me break down exactly what happened.

---

### Question-by-Question Comparison (All 3 Rounds)

| Question | R1 (Semantic) | R2 (+BM25) | R3 (+Reranker) | Trend |
|----------|--------------|------------|----------------|-------|
| Q1 | 7 | 9 | 9 | Stable |
| Q2 | 10 | 10 | 10 | Stable |
| Q3 | 8 | 8 | **3** | Crashed |
| Q4 | 5 | 8 | **5** | Regressed to R1 |
| Q5 | 4 | 9 | **6** | Regressed |
| Q6 | 4 | 9 | 8.5 | Slight dip |
| Q7 | 6 | 7.5 | **6** | Regressed to R1 |
| Q8 | 5 | 8.5 | **9** | Best yet |
| Q9 | 3 | 6 | **4** | Regressed |
| Q10 | 5 | 8 | **7** | Slight dip |
| **Avg** | **6.5** | **8.2** | **6.8** | **Down 1.4** |

---

### Detailed Analysis

**Q1 — Easy | 9/10 (stable)**
Still correct — Golden Gate Avenue, 2017, San Francisco. No change.

**Q2 — Easy | 10/10 (stable)**
Still perfect. $50 fine, correct source.

**Q3 — Easy | 3/10 (was 8/10 — CRASHED)**
This is the worst regression. Previously correctly identified "Meta's Segment Anything Model (SAM)." Now the system says *"the study does not specify a named AI model"* — which is flat-out wrong. SAM is explicitly named multiple times in 3.pdf. The reranker appears to have **demoted the chunk containing the model name** and promoted a less specific chunk that uses vaguer language. This is a classic reranker failure where a passage that discusses "AI-based segmentation" generically scores higher on query relevance than the passage that actually names the specific model.

**Q4 — Easy | 5/10 (was 8/10 — regressed back to R1 level)**
The 13.5 km distance that BM25 successfully retrieved in Round 2 is now missing again — the system says *"the excerpts do not provide a numeric value."* The reranker pushed the chunk containing this number out of the top-k results. This directly undoes the BM25 improvement.

**Q5 — Easy | 6/10 (was 9/10 — regressed)**
Still gets "Place" and "Movement" correct, but no longer provides the definitions that were present in Round 2. The answer is bare-bones. The reranker seems to be favoring shorter, more "relevant" passages over the more comprehensive ones.

**Q6 — Tough | 8.5/10 (was 9/10 — slight dip)**
Still retrieves β = 379.88 and β = −141.18 correctly. Minor issue: now says *"the excerpts do not contain information about sharrows"* when sharrows and painted lanes are grouped together in the paper. The reranker may have retrieved a chunk that only mentions painted lanes without the sharrow context.

**Q7 — Tough | 6/10 (was 7.5/10 — regressed to R1 level)**
Gets the crossing distances right (26, 43, 58 ft) which is good. But now says the logistic regression findings are *"not provided in the excerpts"* — when Round 2 at least described the relationship qualitatively. The reranker is retrieving the descriptive results chunk but not the regression analysis chunk.

**Q8 — Tough | 9/10 (was 8.5/10 — BEST PERFORMANCE YET)**
This is the one clear win. Now correctly reports overall decline, the 234% increase for super speeders, and the 38% nighttime figure. The reranker actually helped here by promoting the right passage that contains all three statistics together. Still missing the 33% specific figure and the 23% comparison.

**Q9 — Tough | 4/10 (was 6/10 — regressed)**
Previously found 3 of 5 variable names. Now finds zero and says *"the excerpts do not list the five SLD variables."* The methodology paragraph listing the five variables is being consistently pushed out. The reranker is likely scoring the conceptual discussion of "Place" higher than the technical enumeration of variable names.

**Q10 — Tough | 7/10 (was 8/10 — slight dip)**
Still gets the temperature differential and 2 of 4 categories with proportions. Phase I and Phase II proportions still missing. Minor regression from Round 2.

---

### Diagnosis: What Went Wrong with the Reranker

The cross-encoder reranker (ms-marco-MiniLM-L-6-v2) is designed for **passage relevance ranking** — it scores how well a passage "answers" a query. But this is causing three specific problems with your academic paper content:

**1. It favors general relevance over specific facts.**
The reranker ranks passages that broadly discuss a topic higher than passages containing the specific numbers/names requested. For Q3, a passage saying "AI-based segmentation was used" scores higher than one saying "Meta's SAM 2.1 was fine-tuned on 193 images" because the first is a more direct "answer" to the query phrasing, even though the second has the actual information needed.

**2. It's undoing BM25's keyword-matching advantage.**
BM25 was successfully surfacing chunks with exact terms like "13.5 km," "SAM," and "D1D." The reranker then re-scores these chunks and pushes them down because they may be in technical/methods sections that don't read as "answers" to the question. Q4 and Q9 are the clearest victims.

**3. The ms-marco model is trained on web search passages, not academic papers.**
MS MARCO is based on Bing search queries and web paragraphs. Academic writing — with its dense methodology sections, numbered variable lists, and statistical results — doesn't match the passage style the model was trained on. It's optimizing for the wrong definition of "relevance."

---

### Recommendations

**Option A — Remove the reranker.** Your Round 2 setup (semantic + BM25) was performing better. The reranker is adding complexity without benefit for this use case.

**Option B — Keep the reranker but increase the candidate pool.** If you're currently reranking the top-k (say k=5) results, increase it to k=15 or k=20 before reranking. This gives the reranker more candidates to work with so it's less likely to miss key chunks.

**Option C — Replace the reranker model.** ms-marco-MiniLM is lightweight but not ideal for academic content. Consider a domain-specific or larger cross-encoder like `cross-encoder/ms-marco-MiniLM-L-12-v2` (larger) or fine-tune on academic Q&A pairs.

**Option D — Use the reranker selectively.** Apply reranking only when BM25 and semantic search agree on the top results. When they disagree, trust the union of both rather than letting the reranker arbitrate.

### Bottom Line

Round 2 (semantic + BM25 hybrid, no reranker) remains your best configuration at **8.2/10**. The cross-encoder reranker dropped you to **6.8/10** by systematically deprioritizing the fact-dense technical chunks that BM25 was correctly surfacing. I'd recommend going back to Round 2 as your baseline and exploring Options B or D above.
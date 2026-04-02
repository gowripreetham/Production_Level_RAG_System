# RAG System Evaluation — Phase 1 Baseline

**Date:** April 2026
**Model:** GPT-5-nano
**Embedding Model:** all-MiniLM-L6-v2
**Documents:** 8 research papers (2024-2026)
**Evaluator:** Claude (AI-assisted evaluation — professor evaluation planned post Phase 2)

---

## Overall Score: 6.5/10

---

## Question-by-Question Analysis

**Q1 — Easy | Score: 7/10**
The system correctly identified San Francisco and 2017, and cited the right paper (5.pdf). However, it missed key details: the founders' names (Maureen Persico and Matt Brezina), the street (Golden Gate Avenue), and the number of initial participants (15 total). Suggests the chunk retrieved was a summary-level passage rather than the specific detail-rich paragraph.

**Q2 — Easy | Score: 10/10**
Perfect. Correct answer ($50 flat fine), correct source (4.pdf). No issues.

**Q3 — Easy | Score: 8/10**
Correct model identified (Meta's SAM), correct source (3.pdf). Minor deduction for not specifying SAM 2.1 and that it was fine-tuned on manually-labeled images.

**Q4 — Easy | Score: 5/10**
Got "over 250 School Streets" correct but explicitly said the total pedestrianized distance (13.5 km / 8.4 miles) was not in the excerpts — when it clearly is in the abstract of 7.pdf. Chunking problem: the abstract was split in a way that separated two related facts.

**Q5 — Easy | Score: 4/10**
"Land use and types of roads" is a vague paraphrase that loses the precise terminology — "Place" and "Movement" — the actual named dimensions of the framework. Retrieved chunks likely missed the abstract or methodology section.

**Q6 — Tough | Score: 4/10**
Correctly identified that only protected bike lanes showed a causal effect. Failed to retrieve the key numerical value: β = 379.88 additional monthly rides per station (p < 0.001). Also missed the demographic disparity finding. Results section of 2.pdf is either poorly chunked or not being retrieved.

**Q7 — Tough | Score: 6/10**
Got the directional finding and percentage increases (15%, 23%, 43%) correctly. Missed the three specific average crossing distances (Paris: 26 ft, San Francisco: 43 ft, Irvine: 58 ft) and the specific logistic regression coefficients. Results section not being retrieved with enough precision.

**Q8 — Tough | Score: 5/10**
Partially correct but confused. Reported "2.75 daily violations" as the overall violations figure — but that is actually the super speeder figure. Got the 234% increase and 38% nighttime figure right but mixed up which statistic belongs to which group. Context confusion error.

**Q9 — Tough | Score: 3/10**
Major failure. Could not retrieve the five specific SLD variables even though they are listed explicitly in the methodology section of 1.pdf. Found the rationale but from 6.pdf instead of 1.pdf. Strongly suggests the SLD variable list is in a chunk that isn't being retrieved for this query.

**Q10 — Tough | Score: 5/10**
Temperature differential (5.01°C) retrieved correctly. The four categories with their proportions were completely missed — likely because that information appears as a structured enumeration mid-paper, not in the abstract.

---

## Key Patterns & Diagnosed Problems

1. **Chunking is cutting across related facts.** Q4 is the clearest example — two facts from the same abstract were separated. Chunk size may be too small or splits are happening at wrong boundaries.

2. **Numerical and statistical details are not being retrieved.** Q6, Q7, Q9 all show the system finding the topic but not the specific numbers. Embeddings match on concept words but chunks carrying actual statistics rank too low.

3. **Results sections underperform vs. abstract and intro.** Nearly every failure involves a result from the middle of a paper. Abstracts are retrieved well but dense results sections are not.

4. **Context confusion between related statistics.** Q8 shows the system retrieving the right section but misattributing which number belongs to which group.

5. **Enumerated lists are poorly handled.** Q9 and Q10 both involve explicitly listed items that the system couldn't retrieve. List-formatted content gets fragmented during parsing.

---

## Recommendations for Phase 2

- Increase chunk size so related facts aren't split across boundaries
- Preserve list structures during PDF parsing
- Add hybrid retrieval (BM25 + semantic) since exact numbers won't be found by semantic search alone
- Add a re-ranking step that scores retrieved chunks on numerical density for quantitative questions
- Add metadata tagging (abstract vs. methods vs. results) for weighted retrieval
EVAL_QUESTIONS = [
    {
        "id": "Q1",
        "difficulty": "easy",
        "question": "Where and when did the first 'People Protected Bike Lanes' (PPBL) demonstration take place?",
        "expected_answer": "The first PPBL took place in 2017 on San Francisco's Golden Gate Avenue, where founders Maureen Persico and Matt Brezina were joined by thirteen other participants.",
        "source_paper": "5.pdf",
        "phase1_score": 7
    },
    {
        "id": "Q2",
        "difficulty": "easy",
        "question": "What is the fine for a camera-based speeding violation in New York City?",
        "expected_answer": "The fine is a flat $50, which does not vary with how far above the speed limit the vehicle was traveling, nor does it ramp up as the number of violations increases.",
        "source_paper": "4.pdf",
        "phase1_score": 10
    },
    {
        "id": "Q3",
        "difficulty": "easy",
        "question": "What AI model was used to segment satellite imagery of street intersections in the pedestrian crossing distance study across 100 U.S. cities?",
        "expected_answer": "Meta's Segment Anything Model (SAM), specifically SAM 2.1, was fine-tuned on manually-labeled intersection images to differentiate drivable from non-drivable surfaces on satellite imagery tiles.",
        "source_paper": "3.pdf",
        "phase1_score": 8
    },
    {
        "id": "Q4",
        "difficulty": "easy",
        "question": "How many School Streets exist in Paris as of summer 2025, and how much total street distance has been pedestrianized?",
        "expected_answer": "As of summer 2025, there are over 250 (272 total) School Streets in Paris. The Rues aux écoles program has pedestrianized 13.5 km (8.4 miles) of streets, creating 15.7 hectares (38.9 acres) of open space.",
        "source_paper": "7.pdf",
        "phase1_score": 5
    },
    {
        "id": "Q5",
        "difficulty": "easy",
        "question": "What two dimensions does the context-sensitive roadway classification framework by Hsu et al. use to classify roads for speed limit setting?",
        "expected_answer": "The framework uses two dimensions: 'Place,' which captures surrounding land uses and locational contexts, and 'Movement,' which relates to the road's transport function.",
        "source_paper": "1.pdf",
        "phase1_score": 4
    },
    {
        "id": "Q6",
        "difficulty": "tough",
        "question": "In the Citi Bike study on protected bike lanes, what was the average treatment effect (DiD coefficient) of protected bike lanes on bikeshare ridership, and why was the effect of painted bike lanes and sharrows not statistically significant?",
        "expected_answer": "Protected bike lanes had a statistically significant average treatment effect of β = 379.88 additional monthly rides per station (p < 0.001). Painted bike lanes and sharrows showed β = −141.18 (p = 0.156), not statistically significant, validated through a placebo test using 500 iterations of randomly shuffled installation dates.",
        "source_paper": "2.pdf",
        "phase1_score": 4
    },
    {
        "id": "Q7",
        "difficulty": "tough",
        "question": "In the 'Multiscale Analysis of Pedestrian Crossing Distance' study, how did the average pedestrian crossing distances compare across Paris, San Francisco, and Irvine, and what were the logistic regression findings linking crossing distance to collision probability?",
        "expected_answer": "Average crossing distance: Paris 26 ft, San Francisco 43 ft, Irvine 58 ft. Per 1-foot increase in crossing distance, collision probability increased by 0.8% in Paris, 2.11% in San Francisco, and 1.8% in Irvine. Crossings where collisions occurred were 15%, 23%, and 43% longer respectively.",
        "source_paper": "3.pdf",
        "phase1_score": 6
    },
    {
        "id": "Q8",
        "difficulty": "tough",
        "question": "In the NYC super speeders study, how did the expansion of speed camera operating hours in August 2022 affect overall violations versus super speeder violations, and what percentage of super speeder violations occurred during the newly added nighttime hours?",
        "expected_answer": "Overall violations per camera-hour decreased by 33%. Super speeder daily violations increased by 234% (from 0.82 to 2.75 per camera-hour). Approximately 38% of super speeder violations occurred between 10 PM and 6 AM, compared to only 23% for all vehicles combined.",
        "source_paper": "4.pdf",
        "phase1_score": 5
    },
    {
        "id": "Q9",
        "difficulty": "tough",
        "question": "What five SLD variables were used to operationalize the 'Place' dimension in Hsu et al.'s roadway classification framework, and why was the industrial percentage variable specifically included?",
        "expected_answer": "Five variables: D1D (gross activity density), D2A_EPHHM (employment and household entropy), D3B (street intersection density), D4A (distance to nearest transit stop), and % Industry. Industrial percentage was included as a counter-control because industrial areas were being misclassified as high Place scores due to high diversity scores despite having limited pedestrian activity.",
        "source_paper": "1.pdf",
        "phase1_score": 3
    },
    {
        "id": "Q10",
        "difficulty": "tough",
        "question": "In the Paris School Streets study, what are the four distinct categories of School Streets, their approximate proportions, and what was the average temperature differential detected between School Streets with cooling pavement and adjacent control streets?",
        "expected_answer": "Four categories: Longstanding (22%), Open to Cars (22%), Phase I (27%), Phase II (29%). Average temperature differential of 5.01°C (9.02°F) between School Streets with cooling pavement and adjacent control streets, with largest differential of 12.2°C (21.96°F).",
        "source_paper": "7.pdf",
        "phase1_score": 5
    }
]
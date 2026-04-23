from langfuse import get_client
from dotenv import load_dotenv
import statistics
from datetime import datetime

load_dotenv()
langfuse = get_client()

def get_all_traces():
    response = langfuse.api.trace.list(limit=100)
    return [t for t in response.data if t.name == "rag_query"]

def percentile(data, p):
    if not data:
        return None
    sorted_data = sorted(data)
    index = int(len(sorted_data) * p / 100)
    index = min(index, len(sorted_data) - 1)
    return sorted_data[index]

def generate_report():
    print("Fetching traces from Langfuse...")
    traces = get_all_traces()
    print(f"Found {len(traces)} traces\n")

    latencies = []
    costs = []
    groundedness_scores = []
    successes = 0
    failures = 0
    easy_groundedness = []
    tough_groundedness = []

    for trace in traces:
        # Latency — already in seconds
        if hasattr(trace, 'latency') and trace.latency:
            latencies.append(trace.latency)

        # Output fields
        if trace.output and isinstance(trace.output, dict):
            status = trace.output.get("status", "unknown")
            if status == "success":
                successes += 1
            elif status == "failed":
                failures += 1

            groundedness = trace.output.get("groundedness")
            if groundedness is not None:
                g = float(groundedness)
                groundedness_scores.append(g)

                difficulty = trace.output.get("difficulty")
                if difficulty == "easy":
                    easy_groundedness.append(g)
                elif difficulty == "tough":
                    tough_groundedness.append(g)

            # Cost directly from trace output
            cost = trace.output.get("total_cost")
            if cost:
                costs.append(float(cost))

    # Print report
    print("=" * 60)
    print("RAG SYSTEM MONITORING REPORT")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    print(f"\n📊 OVERVIEW")
    print(f"  Total queries:    {len(traces)}")
    print(f"  Successful:       {successes}")
    print(f"  Failed:           {failures}")
    if len(traces) > 0:
        print(f"  Failure rate:     {failures/len(traces)*100:.1f}%")

    print(f"\n⚡ LATENCY")
    if latencies:
        print(f"  P50 (median):     {percentile(latencies, 50):.2f}s")
        print(f"  P95:              {percentile(latencies, 95):.2f}s")
        print(f"  P99:              {percentile(latencies, 99):.2f}s")
        print(f"  Average:          {statistics.mean(latencies):.2f}s")
        print(f"  Min:              {min(latencies):.2f}s")
        print(f"  Max:              {max(latencies):.2f}s")
    else:
        print("  No latency data available")

    print(f"\n💰 COST")
    if costs:
        print(f"  Avg per query:    ${statistics.mean(costs):.6f}")
        print(f"  Total spent:      ${sum(costs):.6f}")
        print(f"  Cheapest query:   ${min(costs):.6f}")
        print(f"  Most expensive:   ${max(costs):.6f}")
        print(f"  Est. daily (100 queries):    ${statistics.mean(costs)*100:.4f}")
        print(f"  Est. monthly (3000 queries): ${statistics.mean(costs)*3000:.4f}")
    else:
        print("  No cost data available")

    print(f"\n🎯 GROUNDEDNESS")
    if groundedness_scores:
        print(f"  Average:          {statistics.mean(groundedness_scores):.2f}")
        print(f"  Min:              {min(groundedness_scores):.2f}")
        print(f"  Max:              {max(groundedness_scores):.2f}")
        if easy_groundedness:
            print(f"  Easy questions:   {statistics.mean(easy_groundedness):.2f}")
        if tough_groundedness:
            print(f"  Tough questions:  {statistics.mean(tough_groundedness):.2f}")
        below_threshold = [s for s in groundedness_scores if s < 0.8]
        print(f"  Below 0.8:        {len(below_threshold)} queries ⚠️")
    else:
        print("  No groundedness data available")

    print("\n" + "=" * 60)

if __name__ == "__main__":
    generate_report()
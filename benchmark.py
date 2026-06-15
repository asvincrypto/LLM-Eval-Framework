import time
from runners.llm_runner import run_llm
from scoring.metrics import compute_final_score
from storage.database import get_session, EvalResult

BENCHMARKS = [
    {
        "name": "basic_math",
        "prompt": "What is 12 multiplied by 15?",
        "expected": "180",
        "keywords": ["180"],
    },
    {
        "name": "capital_city",
        "prompt": "What is the capital of France?",
        "expected": "Paris",
        "keywords": ["Paris"],
    },
    {
        "name": "code_generation",
        "prompt": "Write a Python function that returns the factorial of a number.",
        "expected": "",
        "keywords": ["def", "factorial", "return", "recursion"],
    },
    {
        "name": "summarization",
        "prompt": "Summarize what machine learning is in 2 sentences.",
        "expected": "",
        "keywords": ["data", "model", "learn", "predict"],
    },
    {
        "name": "reasoning",
        "prompt": "If all cats are animals and some animals are pets, can we conclude all cats are pets? Explain.",
        "expected": "",
        "keywords": ["no", "not necessarily", "some", "conclude"],
    },
]


def run_benchmarks(model: str = "gemini-2.0-flash", version: str = "v1"):
    session = get_session()
    results = []

    print(f"\n🚀 Running benchmarks for {model} [{version}]\n")

    for bench in BENCHMARKS:
        time.sleep(20)
        print(f"  ▶ Running: {bench['name']}...")

        result = run_llm(bench["prompt"], model=model, version=version)

        score = compute_final_score(
            response=result["response"],
            expected=bench.get("expected", ""),
            keywords=bench.get("keywords", []),
        )

        db_entry = EvalResult(
            model_name=result["model_name"],
            model_version=version,
            benchmark_name=bench["name"],
            prompt=result["prompt"],
            response=result["response"],
            score=score,
            latency_ms=result["latency_ms"],
        )

        session.add(db_entry)
        results.append({**result, "benchmark": bench["name"], "score": score})
        print(f"     ✅ Score: {score} | Latency: {result['latency_ms']}ms")

    session.commit()
    session.close()
    print("\n✅ All benchmarks complete and saved to database!\n")
    return results
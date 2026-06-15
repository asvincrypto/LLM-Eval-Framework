from evals.benchmark import run_benchmarks

if __name__ == "__main__":
    print("=" * 50)
    print("   LLM EVAL FRAMEWORK")
    print("=" * 50)

    run_benchmarks(model="mock-llm", version="v2")
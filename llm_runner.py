import time
import random

MOCK_RESPONSES = {
    "basic_math": "The answer is 180.",
    "capital_city": "The capital of France is Paris.",
    "code_generation": """def factorial(n):
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)""",
    "summarization": "Machine learning is a field where models learn patterns from data to make predictions. It enables computers to improve automatically through experience without being explicitly programmed.",
    "reasoning": "No, we cannot conclude that all cats are pets. While all cats are animals, only some animals are pets, so some cats might not be pets.",
}

def run_llm(prompt: str, model: str = "mock-llm", version: str = "v1") -> dict:
    """
    Returns mock responses simulating a real LLM.
    """
    time.sleep(0.5)  # simulate latency

    # pick response based on keyword in prompt
    response_text = "This is a default mock response."
    for key, response in MOCK_RESPONSES.items():
        if any(word in prompt.lower() for word in key.split("_")):
            response_text = response
            break

    latency_ms = round(random.uniform(300, 900), 2)

    return {
        "model_name": model,
        "model_version": version,
        "prompt": prompt,
        "response": response_text,
        "latency_ms": latency_ms
    }
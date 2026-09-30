import os

from gradio_client import Client

DEFAULT_MAX_NEW_TOKENS = 300


def get_endpoint() -> str:
    endpoint = os.getenv("MEDGEMMA_ENDPOINT")

    if not endpoint:
        raise RuntimeError(
            "MEDGEMMA_ENDPOINT is not set. "
            "Set it to the current Gradio URL before running generation."
        )

    return endpoint


def generate_medgemma_response(
    prompt: str,
    max_new_tokens: int = DEFAULT_MAX_NEW_TOKENS,
) -> str:
    client = Client(get_endpoint())

    result = client.predict(
        prompt,
        max_new_tokens,
        api_name="/generate",
    )

    if not isinstance(result, str):
        raise TypeError(
            "Expected MedGemma response to be a string."
        )

    return result


if __name__ == "__main__":
    test_prompt = (
        "Explain why a normal chest X-ray does not rule out "
        "every serious lung disease."
    )

    response = generate_medgemma_response(test_prompt)

    print(response)
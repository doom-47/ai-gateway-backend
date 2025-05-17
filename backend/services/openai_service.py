def generate_text(prompt: str):
    # Simulate token count
    input_tokens = len(prompt.split())
    output_tokens = 50  # Fake output tokens
    response_text = f"OpenAI response for prompt: {prompt}"
    return response_text, input_tokens, output_tokens

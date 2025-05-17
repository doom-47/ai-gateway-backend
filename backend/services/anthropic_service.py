def generate_text(prompt: str):
    input_tokens = len(prompt.split())
    output_tokens = 40
    response_text = f"Anthropic response for prompt: {prompt}"
    return response_text, input_tokens, output_tokens

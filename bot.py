from openai import OpenAI

def generate_code(prompt):
    try:
        client = OpenAI(api_key="YOUR_OPENAI_API_KEY")  # Replace with your actual API key
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error generating code: {e}")
        return None

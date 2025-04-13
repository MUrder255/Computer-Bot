import openai

# OpenAI API Key
OPENAI_API_KEY = "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"
openai.api_key = OPENAI_API_KEY

# Function to generate code or feature ideas using OpenAI
def generate_code(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Use a chat-based model
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error generating code: {e}")
        return None

# Function to suggest features
def suggest_features():
    prompt = "Suggest innovative features for a modern automation bot that can manage apps, upgrade them, and implement new ideas."
    features = generate_code(prompt)
    if features:
        print("Suggested Features:\n", features)
    else:
        print("Failed to generate feature suggestions.")

# Main menu for the bot
def main():
    while True:
        print("\n--- Computer Bot Menu ---")
        print("1. Suggest Features")
        print("2. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            suggest_features()
        elif choice == "2":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()

from openai import OpenAI

# OpenAI API Key
OPENAI_API_KEY = "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"
client = OpenAI(api_key=OPENAI_API_KEY)

# Function to generate code or feature ideas using OpenAI
def generate_code(prompt):
    response = client.completions.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=500
    )
    return response.choices[0].text.strip()

# Function to suggest features
def suggest_features():
    prompt = "Suggest innovative features for a modern automation bot that can manage apps, upgrade them, and implement new ideas."
    features = generate_code(prompt)
    print("Suggested Features:\n", features)

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

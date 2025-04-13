from openai import OpenAI

# Initialize OpenAI client with your API key
client = OpenAI(api_key="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")

# Function to generate code or feature ideas using OpenAI
def generate_code(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Use a chat-based model
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

# Function to suggest features
def suggest_features():
    prompt = "Suggest innovative features for a modern automation bot that can manage apps, upgrade them, and implement new ideas."
    features = generate_code(prompt)
    if features:
        print("Suggested Features:\n", features)
    else:
        print("Failed to generate feature suggestions.")

# Function to execute system commands
def execute_task(task):
    try:
        if "open" in task.lower():
            # Open a file, folder, or app
            path = task.split("open")[-1].strip()
            if os.path.exists(path):
                os.startfile(path)
                print(f"Opened: {path}")
            else:
                print(f"Path not found: {path}")
        elif "install" in task.lower():
            # Example: Install a package using pip
            package = task.split("install")[-1].strip()
            subprocess.run(["pip", "install", package], check=True)
            print(f"Installed package: {package}")
        elif "update" in task.lower():
            # Example: Run system update command
            print("Running system update...")
            subprocess.run(["sudo", "apt", "update"], check=True)  # For Linux
        else:
            # Run generic system command
            subprocess.run(task, shell=True, check=True)
            print(f"Executed command: {task}")
    except Exception as e:
        print(f"Error executing task: {e}")

# Main menu for the bot
def main():
    while True:
        print("\n--- Computer Bot Menu ---")
        print("1. Suggest Features")
        print("2. Execute Task")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            suggest_features()
        elif choice == "2":
            task = input("What task should I perform? (e.g., 'open Notepad', 'install numpy', 'update system'): ")
            execute_task(task)
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()

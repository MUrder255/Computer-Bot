import openai
import requests
from github import Github
import os

# OpenAI API Key
OPENAI_API_KEY = "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"
openai.api_key = OPENAI_API_KEY

# GitHub API Key
GITHUB_API_KEY = "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"
github = Github(GITHUB_API_KEY)

# GitHub repository details
REPO_OWNER = "MUrder255"
REPO_NAME = "Computer-Bot"

# Function to generate code or feature ideas using OpenAI
def generate_code(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=500
    )
    return response.choices[0].text.strip()

# Function to create a GitHub issue
def create_github_issue(title, body):
    try:
        repo = github.get_user(REPO_OWNER).get_repo(REPO_NAME)
        issue = repo.create_issue(title=title, body=body)
        print(f"Issue created: {issue.html_url}")
    except Exception as e:
        print(f"Error creating issue: {str(e)}")

# Function to suggest features
def suggest_features():
    prompt = "Suggest innovative features for a modern automation bot that can manage apps, upgrade them, and implement new ideas."
    features = generate_code(prompt)
    print("Suggested Features:\n", features)

# Function to automate code creation
def automate_task(task_description):
    prompt = f"Write Python code to {task_description}."
    code = generate_code(prompt)
    print("Generated Code:\n", code)
    return code

# Main menu for the bot
def main():
    while True:
        print("\n--- Computer Bot Menu ---")
        print("1. Suggest Features")
        print("2. Create a GitHub Issue")
        print("3. Automate Task with Code")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            suggest_features()
        elif choice == "2":
            title = input("Enter the issue title: ")
            body = input("Enter the issue description: ")
            create_github_issue(title, body)
        elif choice == "3":
            task_description = input("Describe the task to automate: ")
            code = automate_task(task_description)
            # Optionally save the code to a file
            with open("automated_task.py", "w") as f:
                f.write(code)
                print("Code saved to automated_task.py")
        elif choice == "4":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()

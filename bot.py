import os
import subprocess
import logging
import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from openai import OpenAI
import speech_recognition as sr
import pyttsx3
import json

# Initialize OpenAI client with your API key
client = OpenAI(api_key="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")  # Replace with your actual API key

# Configure logging
logging.basicConfig(
    filename="bot.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Initialize the scheduler
scheduler = BackgroundScheduler()
scheduler.start()

# Initialize text-to-speech
engine = pyttsx3.init()

# Load user profiles
USER_PROFILES = {}
PROFILE_FILE = "user_profiles.json"
if os.path.exists(PROFILE_FILE):
    with open(PROFILE_FILE, "r") as file:
        USER_PROFILES = json.load(file)

# Function to save profiles
def save_profiles():
    with open(PROFILE_FILE, "w") as file:
        json.dump(USER_PROFILES, file, indent=4)

# Function to generate code or feature ideas using OpenAI
def generate_code(prompt):
    try:
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
        logging.error(f"Error generating code: {e}")
        return None

# Function to execute system commands
def execute_task(task):
    try:
        if "open" in task.lower():
            path = task.split("open")[-1].strip()
            if os.path.exists(path):
                os.startfile(path)
                logging.info(f"Opened: {path}")
                print(f"Opened: {path}")
            else:
                logging.warning(f"Path not found: {path}")
                print(f"Path not found: {path}")
        elif "install" in task.lower():
            package = task.split("install")[-1].strip()
            subprocess.run(["pip", "install", package], check=True)
            logging.info(f"Installed package: {package}")
            print(f"Installed package: {package}")
        elif "update" in task.lower():
            print("Running system update...")
            subprocess.run(["sudo", "apt", "update"], check=True)  # For Linux
            logging.info("System update completed.")
        else:
            subprocess.run(task, shell=True, check=True)
            logging.info(f"Executed command: {task}")
            print(f"Executed command: {task}")
    except Exception as e:
        logging.error(f"Error executing task: {e}")
        print(f"Error executing task: {e}")

# Function to schedule tasks
def schedule_task(task, run_time):
    try:
        run_time = datetime.datetime.strptime(run_time, "%Y-%m-%d %H:%M:%S")
        scheduler.add_job(lambda: execute_task(task), 'date', run_date=run_time)
        logging.info(f"Scheduled task: '{task}' at {run_time}")
        print(f"Task scheduled: '{task}' at {run_time}")
    except Exception as e:
        logging.error(f"Error scheduling task: {e}")
        print(f"Error scheduling task: {e}")

# Function to suggest features
def suggest_features():
    prompt = "Suggest innovative features for a modern automation bot that can manage apps, upgrade them, and implement new ideas."
    features = generate_code(prompt)
    if features:
        logging.info("Generated feature suggestions.")
        print("Suggested Features:\n", features)
    else:
        logging.error("Failed to generate feature suggestions.")
        print("Failed to generate feature suggestions.")

# Voice command recognition
def recognize_voice():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for your command...")
        try:
            audio = recognizer.listen(source)
            command = recognizer.recognize_google(audio)
            return command
        except sr.UnknownValueError:
            print("Sorry, I didn't catch that.")
        except sr.RequestError as e:
            print(f"Error with speech recognition service: {e}")
    return None

# Function to interact with the user via voice
def voice_assistant():
    command = recognize_voice()
    if command:
        print(f"You said: {command}")
        execute_task(command)

# Function to display user profiles
def display_profiles():
    if USER_PROFILES:
        print("\n--- User Profiles ---")
        for user, data in USER_PROFILES.items():
            print(f"User: {user}")
            print(f"Preferences: {data}")
    else:
        print("No user profiles found.")

# Main menu for the bot
def main():
    while True:
        print("\n--- Advanced Computer Bot Menu ---")
        print("1. Suggest Features")
        print("2. Execute Task")
        print("3. Schedule Task")
        print("4. Voice Assistant")
        print("5. Display User Profiles")
        print("6. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            suggest_features()
        elif choice == "2":
            task = input("What task should I perform? (e.g., 'open Notepad', 'install numpy', 'update system'): ")
            execute_task(task)
        elif choice == "3":
            task = input("What task should I schedule? (e.g., 'open Notepad', 'install numpy'): ")
            run_time = input("When should the task run? (format: YYYY-MM-DD HH:MM:SS): ")
            schedule_task(task, run_time)
        elif choice == "4":
            voice_assistant()
        elif choice == "5":
            display_profiles()
        elif choice == "6":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting gracefully...")
        scheduler.shutdown()
        save_profiles()

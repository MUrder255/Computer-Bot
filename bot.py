import os
import subprocess
import logging
import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from openai import OpenAI
import pyttsx3
import speech_recognition as sr
import threading
import vlc  # VLC for music playback
from concurrent.futures import ThreadPoolExecutor

# Initialize OpenAI client with your API key
client = OpenAI(api_key="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")  # Replace with your actual API key

# Configure logging
logging.basicConfig(
    filename="bot.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Initialize scheduler and text-to-speech engine
scheduler = BackgroundScheduler()
scheduler.start()
engine = pyttsx3.init()

# Global VLC player instance
player = None

# Maximum number of bots in the pool
MAX_BOTS = 5

# Function to play music from SoundCloud
def play_music(track_url):
    global player
    try:
        if player is None:
            player = vlc.MediaPlayer(track_url)
        else:
            player.set_media(vlc.Media(track_url))
        player.play()
        logging.info(f"Playing music from: {track_url}")
        print(f"Playing music from: {track_url}")
    except Exception as e:
        logging.error(f"Error playing music: {e}")
        print(f"Error playing music: {e}")

# Function to stop music playback
def stop_music():
    global player
    if player is not None:
        player.stop()
        logging.info("Music playback stopped.")
        print("Music playback stopped.")

# Function to analyze code and suggest fixes or upgrades
def analyze_code(directory):
    try:
        code = ""
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith((".py", ".js", ".java", ".cpp")):  # Adjust for your app's languages
                    file_path = os.path.join(root, file)
                    with open(file_path, "r", encoding="utf-8") as f:
                        code += f"\n# File: " + file + "\n" + f.read()

        prompt = f"""
        You are a code assistant. Analyze the following code and suggest improvements, fixes, and upgrades:
        {code}
        """
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant for analyzing and improving code."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0.7
        )
        suggestions = response.choices[0].message.content.strip()
        logging.info("Code Analysis Suggestions:\n" + suggestions)
        print("Code Analysis Suggestions:\n", suggestions)
    except Exception as e:
        logging.error(f"Error analyzing code: {e}")
        print(f"Error analyzing code: {e}")

# Function to fix code issues
def fix_code(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            code = f.read()

        prompt = f"""
        You are a code assistant. Here is some code with issues. Fix the code and ensure it works properly:
        {code}
        """
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant for fixing and improving code."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0.7
        )
        fixed_code = response.choices[0].message.content.strip()
        logging.info(f"Fixed Code for {file_path}:\n" + fixed_code)
        print(f"Fixed Code for {file_path}:\n", fixed_code)

        # Save the fixed code back to the file
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(fixed_code)
        print(f"Fixed code saved to {file_path}")
    except Exception as e:
        logging.error(f"Error fixing code in {file_path}: {e}")
        print(f"Error fixing code in {file_path}: {e}")

# Bot Pool Manager to distribute tasks
def bot_pool_manager(task, directory):
    # Create a thread pool to manage bots
    with ThreadPoolExecutor(max_workers=MAX_BOTS) as executor:
        tasks = []
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith((".py", ".js", ".java", ".cpp")):  # Adjust for your app's languages
                    file_path = os.path.join(root, file)
                    if task == "fix":
                        tasks.append(executor.submit(fix_code, file_path))
                    elif task == "analyze":
                        tasks.append(executor.submit(analyze_code, directory))

        # Wait for all tasks to complete
        for future in tasks:
            future.result()

# Main menu for the bot
def main():
    while True:
        print("\n--- App Development Assistant Menu ---")
        print("1. Analyze Code (Single Bot)")
        print("2. Analyze Code (Multiple Bots)")
        print("3. Fix Code (Multiple Bots)")
        print("4. Play Music")
        print("5. Stop Music")
        print("6. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            directory = input("Enter the directory of your app: ")
            analyze_code(directory)
        elif choice == "2":
            directory = input("Enter the directory of your app: ")
            bot_pool_manager("analyze", directory)
        elif choice == "3":
            directory = input("Enter the directory of your app: ")
            bot_pool_manager("fix", directory)
        elif choice == "4":
            track_url = input("Enter the SoundCloud track URL: ")
            threading.Thread(target=play_music, args=(track_url,)).start()
        elif choice == "5":
            stop_music()
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

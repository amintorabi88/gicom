import time
import subprocess
import os
from pynput import keyboard
import pyperclip
from openai import OpenAI
from dotenv import load_dotenv

# Setup
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# CONFIG: The hotkey you want to use
HOTKEY = {keyboard.Key.cmd, keyboard.Key.shift, keyboard.KeyCode(char="g")}

# State
current_keys = set()


def get_git_diff():
    """Gets the diff from the current working directory."""
    try:
        # We assume the script is run FROM the repo folder for now
        diff = (
            subprocess.check_output(
                ["git", "diff", "--cached"], stderr=subprocess.STDOUT
            )
            .decode("utf-8")
            .strip()
        )
        return diff
    except Exception as e:
        return None


def generate_commit_msg(diff):
    if not diff:
        return "No staged changes found!"

    print("🧠 AI is thinking...")
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "Summarize this git diff into a concise commit message (Conventional Commits). No markdown. Just text.",
            },
            {"role": "user", "content": diff},
        ],
        temperature=0.3,
    )
    return response.choices[0].message.content.strip()


def on_activate():
    print("\n🚀 Hotkey detected! Generating...")

    # 1. Get Diff
    diff = get_git_diff()

    # 2. Generate
    msg = generate_commit_msg(diff)

    # 3. Copy to Clipboard
    pyperclip.copy(msg)

    # 4. Notify (Sound or Print)
    print(f"✅ Copied to clipboard:\n{msg}")
    # On Mac, we can make a sound to let you know it's done
    os.system("tput bel")


def on_press(key):
    if key in HOTKEY:
        current_keys.add(key)
        if all(k in current_keys for k in HOTKEY):
            on_activate()


def on_release(key):
    try:
        current_keys.remove(key)
    except KeyError:
        pass


# Main Loop
print("👻 Gicom Ghost Mode is running...")
print("Press [Cmd + Shift + G] to generate a commit message.")

# Start Listener
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

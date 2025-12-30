
# Gicom 

**AI-powered Git commit messages generated directly from your terminal.**

> Stop writing "fixed stuff" or "wip". Let the ghost in the machine write professional, Conventional Commit messages for you.

## ✨ Features

* **Zero Friction:** One command (`gicom get-ai`) to generate and copy.
* **Professional Format:** Follows [Conventional Commits](https://www.conventionalcommits.org/) (feat:, fix:, chore:).
* **Secure:** Your OpenAI API Key is stored locally in `~/.config/gicom/`.
* **Context Aware:** Analyzes your actual `git diff` to understand what changed.

## 📦 Installation

To install gicom globally on your system, clone the repository and install it with pip.

```bash
git clone [https://github.com/amintorabi88/gicom.git](https://github.com/amintorabi88/gicom.git)
cd gicom
pip install -e .

```

> **Note:** The `-e` flag installs it in "Editable" mode, so you can update the code easily without reinstalling.

## 🚀 Setup

The first time you run gicom, it will ask for your OpenAI API Key.

1. Get your key from the [OpenAI Platform](https://platform.openai.com/api-keys).
2. Run the tool:
```bash
gicom get-ai

```

3. Paste your key when prompted (input will be hidden for security).

## 🛠️ Usage

### The Workflow

This is designed for speed. It generates the message and copies it to your clipboard automatically.

1. Stage your changes:
```bash
git add .

```


2. Summon the Ghost:
```bash
gicom get-ai

```


3. **Paste:** Press `Cmd + V` (or `Ctrl + V`) into your commit box (VS Code, GitHub Desktop, or Terminal).

### The "Interactive" Workflow

If you prefer to commit directly from the terminal with a confirmation step:

```bash
gicom commit

```


## 🔒 Security

* Your API Key is stored in `~/.config/gicom/config.json`.
* The file permissions are set to `600` (User Read/Write only).
* Your key is sent only to OpenAI servers for message generation and is never shared elsewhere.


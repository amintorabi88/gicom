import typer
import subprocess
import sys
import pyperclip
from openai import OpenAI
from rich.console import Console
from rich.panel import Panel
from gicom.config import get_api_key

app = typer.Typer()
console = Console()


def get_git_diff():
    try:
        # Check if repo exists
        subprocess.check_output(
            ["git", "rev-parse", "--is-inside-work-tree"], stderr=subprocess.DEVNULL
        )
        # Get staged changes
        diff = (
            subprocess.check_output(
                ["git", "diff", "--cached"], stderr=subprocess.STDOUT
            )
            .decode("utf-8")
            .strip()
        )
        return diff
    except subprocess.CalledProcessError:
        return None


def generate_text(diff):
    api_key = get_api_key()
    client = OpenAI(api_key=api_key)

    system_prompt = (
        "You are an expert developer. You are writing a git commit message for the provided diff. "
        "Follow the Conventional Commits specification (type(scope): subject). "
        "Common types: feat, fix, docs, style, refactor, test, chore. "
        "Rules:\n"
        "1. The first line must be under 50 characters.\n"
        "2. If the change is complex, add a bulleted body description.\n"
        "3. Do NOT output markdown code blocks (```). Just the raw text."
    )

    with console.status(
        "[bold green]🧠 AI is thinking...[/bold green]", spinner="dots"
    ):
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": diff},
            ],
            temperature=0.3,
            max_tokens=200,
        )
    return response.choices[0].message.content.strip()


@app.command(name="get_ai")
def get_ai():
    """
    Reads git changes, generates a message, and copies it to clipboard.
    """
    diff = get_git_diff()

    if diff is None:
        console.print("[bold red] Error:[/bold red] Not a git repository.")
        sys.exit(1)

    if not diff:
        console.print(
            "[bold yellow]⚠️ No staged changes.[/bold yellow] (Did you run 'git add .'?)"
        )
        sys.exit(1)

    message = generate_text(diff)

    pyperclip.copy(message)

    console.print(
        Panel(
            message,
            title="[bold green]Copied to Clipboard![/bold green]",
            border_style="green",
        )
    )


@app.command()
def commit():
    """Standard mode: Prompts to commit directly."""
    diff = get_git_diff()
    if not diff or diff is None:
        console.print("[red]No changes found.[/red]")
        return

    msg = generate_text(diff)
    console.print(Panel(msg, title="Generated", border_style="blue"))

    if typer.confirm("🚀 Commit this?"):
        subprocess.run(["git", "commit", "-m", msg])
        console.print("[green]Done![/green]")


if __name__ == "__main__":
    app()

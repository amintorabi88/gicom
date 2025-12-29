import typer
import subprocess
import os
import sys
from openai import OpenAI
from rich.console import Console
from rich.panel import Panel
from dotenv import load_dotenv

# Initialize
load_dotenv()
app = typer.Typer()
console = Console()

# --- CONFIGURATION ---
# Later we will make this user-configurable. For now, grab from env.
API_KEY = os.getenv("OPENAI_API_KEY")

if not API_KEY:
    console.print(
        "[bold red]Error:[/bold red] OPENAI_API_KEY not found in environment."
    )
    console.print("Run: export OPENAI_API_KEY='sk-...'", style="dim")
    sys.exit(1)

client = OpenAI(api_key=API_KEY)


def get_git_diff():
    """Reads the staged changes from the current git repo."""
    try:
        # Check if inside a git repo
        subprocess.check_output(
            ["git", "rev-parse", "--is-inside-work-tree"], stderr=subprocess.DEVNULL
        )

        # Get the diff of STAGED files (what will be committed)
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


def generate_commit_message(diff: str, context: str):
    """Sends the diff to GPT-4o-mini to get a structured commit message."""

    system_prompt = (
        "You are an expert developer. You are writing a git commit message for the provided diff. "
        "Follow the Conventional Commits specification (type(scope): subject). "
        "Common types: feat, fix, docs, style, refactor, test, chore. "
        "Rules:\n"
        "1. The first line must be under 50 characters.\n"
        "2. If the change is complex, add a bulleted body description.\n"
        "3. Do NOT output markdown code blocks (```). Just the raw text.\n"
        "4. Make it like a human wrote it."
    )

    if context:
        system_prompt += f"\n\nUser Context: {context}"

    with console.status("[bold green]Thinking...[/bold green]", spinner="dots"):
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": diff},
            ],
            temperature=0.3,  # Low temp for consistency
            max_tokens=200,
        )

    return response.choices[0].message.content.strip()


@app.command()
def commit(
    context: str = typer.Option(
        None, "--context", "-c", help="Add extra context (e.g. 'Fixing login bug')"
    ),
    dry_run: bool = typer.Option(
        False, "--dry-run", "-d", help="Print message but do not commit."
    ),
    yes: bool = typer.Option(False, "--yes", "-y", help="Skip confirmation prompt."),
):
    """
    Analyzes staged git changes and auto-commits them with an AI message.
    """

    # 1. Get Data
    diff = get_git_diff()

    if diff is None:
        console.print("[bold red]Error:[/bold red] Not a git repository.")
        raise typer.Exit(code=1)

    if not diff:
        console.print("[yellow]No staged changes found.[/yellow]")
        console.print("Did you forget to run [bold]git add .[/bold]?", style="dim")
        raise typer.Exit(code=1)

    # 2. AI Processing
    message = generate_commit_message(diff, context)

    # 3. Display
    console.print(
        Panel(
            message,
            title="[bold blue]Generated Commit Message[/bold blue]",
            expand=False,
        )
    )

    # 4. Execute
    if dry_run:
        console.print("[dim]Dry run enabled. Exiting.[/dim]")
        return

    if yes or typer.confirm("🚀 Do you want to commit with this message?"):
        subprocess.run(["git", "commit", "-m", message])
        console.print("[bold green]✔ Successfully committed![/bold green]")
    else:
        console.print("[red]Aborted.[/red]")


if __name__ == "__main__":
    app()

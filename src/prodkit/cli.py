#!/usr/bin/env python3
"""
ProdKit CLI - Main entry point for the command-line interface.
"""

import os
import sys
import subprocess
import shutil
import platform
from pathlib import Path
from typing import Optional

try:
    import typer
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.prompt import Prompt, Confirm
    from rich import print as rprint
except ImportError:
    print("Error: Required dependencies not installed.")
    print("Please install ProdKit using: uv tool install prodkit-cli --from git+https://github.com/kiranshivaraju/prodkit.git")
    sys.exit(1)

app = typer.Typer(
    name="prodkit",
    help="ProdKit - Enterprise product development workflow framework for AI coding agents",
    no_args_is_help=True,
)

console = Console()


def detect_os() -> str:
    """Detect the operating system."""
    system = platform.system().lower()
    if system == "darwin":
        return "macos"
    elif system == "windows":
        return "windows"
    else:
        return "linux"


def detect_shell() -> str:
    """Detect the current shell."""
    shell = os.environ.get("SHELL", "")
    if "bash" in shell:
        return "bash"
    elif "zsh" in shell:
        return "zsh"
    elif "fish" in shell:
        return "fish"
    elif platform.system() == "Windows":
        return "powershell"
    else:
        return "bash"  # Default


def detect_terminal() -> str:
    """Detect terminal type based on OS and shell."""
    os_type = detect_os()
    shell = detect_shell()

    if os_type == "windows":
        return "powershell"
    elif os_type == "macos":
        if shell == "zsh":
            return "zsh"
        else:
            return "bash"
    else:  # linux
        return shell


def check_claude_code() -> bool:
    """Check if Claude Code is available."""
    # Check if running in Claude Code environment
    if os.environ.get("CLAUDE_CODE"):
        return True

    # Check if 'claude' command is available
    if shutil.which("claude"):
        return True

    return False


def get_prodkit_commands_dir() -> Path:
    """Get the directory containing ProdKit command files."""
    # When installed via uv tool, the .prodkit directory should be packaged with the tool
    package_dir = Path(__file__).parent
    commands_dir = package_dir / ".prodkit" / "commands"

    if commands_dir.exists():
        return commands_dir

    # Fallback: check if running from source
    source_dir = package_dir.parent.parent / ".prodkit" / "commands"
    if source_dir.exists():
        return source_dir

    console.print("[red]Error: ProdKit commands directory not found[/red]")
    console.print("Expected location:", commands_dir)
    sys.exit(1)


def get_claude_commands_dir() -> Path:
    """Get the .claude directory in the current working directory."""
    cwd = Path.cwd()
    claude_dir = cwd / ".claude"

    if not claude_dir.exists():
        console.print("[yellow]Warning: .claude directory not found in current directory[/yellow]")
        console.print(f"Expected: {claude_dir}")
        console.print("\nRun 'prodkit init' to set up ProdKit in the current directory.")
        sys.exit(1)

    return claude_dir


@app.command()
def init(
    project_name: Optional[str] = typer.Argument(None, help="Project name (defaults to current directory name)"),
    here: bool = typer.Option(False, "--here", help="Initialize in current directory"),
    ai: Optional[str] = typer.Option(None, "--ai", help="AI platform (claude)"),
    terminal: Optional[str] = typer.Option(None, "--terminal", help="Terminal type (bash, zsh, powershell)"),
    force: bool = typer.Option(False, "--force", "-f", help="Overwrite existing installation"),
):
    """
    Initialize ProdKit in a new or existing project.

    Examples:
        prodkit init my-project          # Create new project directory
        prodkit init . --ai claude       # Initialize in current directory
        prodkit init --here --ai claude  # Same as above
    """
    # Welcome banner
    console.print()
    console.print(Panel.fit(
        "[bold cyan]Welcome to ProdKit![/bold cyan]\n"
        "Enterprise product development workflow for AI coding agents",
        title="ProdKit Initialization",
        border_style="cyan"
    ))
    console.print()

    # Determine target directory
    if here or project_name == ".":
        target_dir = Path.cwd()
        project_name = target_dir.name
        console.print(f"[cyan]→[/cyan] Initializing in current directory: [green]{target_dir}[/green]")
    elif project_name:
        target_dir = Path.cwd() / project_name
        console.print(f"[cyan]→[/cyan] Creating new project: [green]{project_name}[/green]")
    else:
        # Interactive project name prompt
        default_name = Path.cwd().name
        project_name = Prompt.ask(
            "[cyan]Project name[/cyan]",
            default=default_name
        )
        if project_name == ".":
            target_dir = Path.cwd()
            project_name = target_dir.name
        else:
            target_dir = Path.cwd() / project_name

    console.print()

    # Detect and confirm AI platform
    if not ai:
        console.print("[bold cyan]Which AI platform are you using?[/bold cyan]")
        console.print("  [dim]ProdKit integrates with AI coding assistants for automated development[/dim]")
        console.print()
        ai_choices = {
            "1": "Claude (Anthropic) - Claude Code CLI",
            # Future: "2": "GitHub Copilot",
            # Future: "3": "Cursor",
        }
        for key, value in ai_choices.items():
            console.print(f"  {key}. {value}")
        console.print()

        ai_choice = Prompt.ask(
            "[cyan]Select AI platform[/cyan]",
            choices=list(ai_choices.keys()),
            default="1"
        )
        ai = "claude"  # For now, only Claude is supported
        console.print(f"[green]✓[/green] Selected: {ai_choices[ai_choice]}")
    else:
        console.print(f"[cyan]→[/cyan] Using AI platform: [green]{ai}[/green]")

    console.print()

    # Detect and confirm terminal
    detected_terminal = detect_terminal()
    detected_os = detect_os()

    if not terminal:
        console.print("[bold cyan]Which terminal/shell are you using?[/bold cyan]")
        console.print(f"  [dim]Detected: {detected_os.upper()} with {detected_terminal}[/dim]")
        console.print()

        terminal_choices = {}
        if detected_os == "windows":
            terminal_choices = {
                "1": "PowerShell",
                "2": "Bash (WSL/Git Bash)",
            }
        else:  # macOS or Linux
            terminal_choices = {
                "1": "Bash",
                "2": "Zsh",
                "3": "Fish",
            }

        for key, value in terminal_choices.items():
            console.print(f"  {key}. {value}")
        console.print()

        terminal_choice = Prompt.ask(
            "[cyan]Select terminal[/cyan]",
            choices=list(terminal_choices.keys()),
            default="1" if detected_os == "windows" or detected_terminal == "bash" else "2"
        )

        if detected_os == "windows":
            terminal = "powershell" if terminal_choice == "1" else "bash"
        else:
            terminal = {"1": "bash", "2": "zsh", "3": "fish"}[terminal_choice]

        console.print(f"[green]✓[/green] Selected: {terminal}")
    else:
        console.print(f"[cyan]→[/cyan] Using terminal: [green]{terminal}[/green]")

    console.print()

    # Check for Claude Code (if AI is Claude)
    if ai == "claude":
        has_claude = check_claude_code()
        if not has_claude:
            console.print("[yellow]⚠[/yellow]  Claude Code not detected")
            console.print("   Make sure Claude Code is installed: https://claude.com/claude-code")
            console.print()
            if not Confirm.ask("[cyan]Continue anyway?[/cyan]", default=True):
                console.print("[yellow]Installation cancelled[/yellow]")
                sys.exit(0)
        else:
            console.print("[green]✓[/green] Claude Code detected")

    console.print()

    # Check if directory exists
    if target_dir.exists() and not here and project_name != ".":
        console.print(f"[yellow]⚠[/yellow]  Directory already exists: {target_dir}")
        if not force:
            if not Confirm.ask("[cyan]Initialize ProdKit in existing directory?[/cyan]", default=False):
                console.print("[yellow]Installation cancelled[/yellow]")
                sys.exit(0)

    # Create directory if needed
    if not target_dir.exists():
        console.print(f"[cyan]→[/cyan] Creating directory: {target_dir}")
        target_dir.mkdir(parents=True, exist_ok=True)

    console.print()
    console.print("[bold cyan]Installing ProdKit...[/bold cyan]")
    console.print()

    # Run the install.sh script
    package_dir = Path(__file__).parent
    install_script = package_dir / "install.sh"

    if not install_script.exists():
        console.print(f"[red]✗ Error: install.sh not found at {install_script}[/red]")
        sys.exit(1)

    try:
        env = os.environ.copy()
        env["TARGET_DIR"] = str(target_dir)
        env["PROJECT_NAME"] = project_name
        env["AI_PLATFORM"] = ai
        env["TERMINAL_TYPE"] = terminal
        if force:
            env["FORCE_INSTALL"] = "1"

        # Use appropriate shell based on detected OS
        shell_cmd = "bash"
        if detected_os == "windows" and terminal == "powershell":
            shell_cmd = "powershell"

        result = subprocess.run(
            [shell_cmd, str(install_script)],
            env=env,
            cwd=str(target_dir),
            text=True,
        )

        console.print()

        if result.returncode == 0:
            console.print(Panel.fit(
                f"[bold green]✓ ProdKit initialized successfully![/bold green]\n\n"
                f"[cyan]Project:[/cyan] {project_name}\n"
                f"[cyan]Location:[/cyan] {target_dir}\n"
                f"[cyan]AI Platform:[/cyan] {ai}\n"
                f"[cyan]Terminal:[/cyan] {terminal}\n\n"
                f"[dim]Next steps:[/dim]\n"
                f"1. cd {target_dir if not here and project_name != '.' else '.'}\n"
                f"2. Open in Claude Code\n"
                f"3. Run /prodkit.prd to start building your product!",
                title="Installation Complete",
                border_style="green"
            ))
        else:
            console.print(f"[red]✗ Installation failed with exit code {result.returncode}[/red]")
            sys.exit(result.returncode)

    except Exception as e:
        console.print(f"[red]✗ Error running installation: {e}[/red]")
        sys.exit(1)


@app.command()
def version():
    """Show ProdKit version information."""
    from . import __version__

    console.print(Panel.fit(
        f"[bold cyan]ProdKit CLI[/bold cyan]\n"
        f"Version: [green]{__version__}[/green]\n"
        f"Enterprise product development workflow framework",
        title="ProdKit"
    ))


@app.command(name="list")
def list_commands():
    """List all available ProdKit commands."""
    try:
        commands_dir = get_prodkit_commands_dir()
    except SystemExit:
        # If commands not found, show installation instructions
        console.print("\n[yellow]ProdKit commands not found. Have you run 'prodkit init'?[/yellow]")
        return

    command_files = sorted(commands_dir.glob("prodkit.*.md"))

    if not command_files:
        console.print("[yellow]No ProdKit commands found[/yellow]")
        return

    table = Table(title="Available ProdKit Commands", show_header=True, header_style="bold cyan")
    table.add_column("Command", style="green")
    table.add_column("Description")

    # Parse description from each command file
    for cmd_file in command_files:
        cmd_name = "/" + cmd_file.stem

        # Extract description from frontmatter
        description = ""
        try:
            with open(cmd_file, "r") as f:
                in_frontmatter = False
                for line in f:
                    if line.strip() == "---":
                        if in_frontmatter:
                            break
                        in_frontmatter = True
                        continue
                    if in_frontmatter and line.startswith("description:"):
                        description = line.split("description:", 1)[1].strip()
                        break
        except Exception:
            description = "No description available"

        table.add_row(cmd_name, description)

    console.print(table)
    console.print("\n[dim]Run these commands in Claude Code after running 'prodkit init'[/dim]")


@app.command()
def check():
    """Check ProdKit installation and required tools (like 'specify check')."""
    console.print()
    console.print(Panel.fit(
        "[bold cyan]ProdKit Installation Check[/bold cyan]",
        border_style="cyan"
    ))
    console.print()

    all_good = True

    # Check 1: Python version
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    if sys.version_info >= (3, 11):
        console.print(f"[green]✓[/green] Python {python_version} (>= 3.11 required)")
    else:
        console.print(f"[red]✗[/red] Python {python_version} (>= 3.11 required)")
        all_good = False

    # Check 2: Claude Code
    has_claude = check_claude_code()
    if has_claude:
        console.print("[green]✓[/green] Claude Code detected")
    else:
        console.print("[yellow]⚠[/yellow] Claude Code not detected (install from https://claude.com/claude-code)")

    # Check 3: Git
    has_git = shutil.which("git") is not None
    if has_git:
        git_version = subprocess.run(["git", "--version"], capture_output=True, text=True).stdout.strip()
        console.print(f"[green]✓[/green] {git_version}")
    else:
        console.print("[red]✗[/red] Git not found (required for version control)")
        all_good = False

    # Check 4: GitHub CLI (optional but recommended)
    has_gh = shutil.which("gh") is not None
    if has_gh:
        gh_version = subprocess.run(["gh", "--version"], capture_output=True, text=True).stdout.split("\n")[0]
        console.print(f"[green]✓[/green] {gh_version}")
    else:
        console.print("[yellow]⚠[/yellow] GitHub CLI (gh) not found (optional, but recommended)")

    # Check 5: Speckit (optional)
    has_speckit = shutil.which("specify") is not None
    if has_speckit:
        console.print("[green]✓[/green] Speckit detected (for TDD)")
    else:
        console.print("[yellow]⚠[/yellow] Speckit not found (install: uv tool install specify-cli --from git+https://github.com/github/spec-kit.git)")

    # Check 6: Terminal/Shell
    shell = detect_shell()
    console.print(f"[cyan]→[/cyan] Shell: {shell}")

    # Check 7: OS
    os_type = detect_os()
    console.print(f"[cyan]→[/cyan] OS: {os_type}")

    console.print()

    # Check for project installation
    cwd = Path.cwd()
    prodkit_dir = cwd / ".prodkit"
    claude_dir = cwd / ".claude"

    if prodkit_dir.exists() and claude_dir.exists():
        console.print("[bold green]ProdKit is installed in this directory[/bold green]")

        config_file = prodkit_dir / "config.yml"
        if config_file.exists():
            try:
                import yaml
                with open(config_file, "r") as f:
                    config = yaml.safe_load(f)
                    project_name = config.get("project", {}).get("name", "Not set")
                    sprint = config.get("sprint", {}).get("current", "Not set")
                    console.print(f"[cyan]→[/cyan] Project: [green]{project_name}[/green]")
                    console.print(f"[cyan]→[/cyan] Current sprint: [green]v{sprint}[/green]")
            except Exception:
                pass
    else:
        console.print("[yellow]ProdKit not initialized in this directory[/yellow]")
        console.print(f"[dim]Run 'prodkit init' to set up ProdKit here[/dim]")

    console.print()

    if all_good:
        console.print("[bold green]✓ All required tools are installed[/bold green]")
    else:
        console.print("[bold yellow]⚠ Some required tools are missing[/bold yellow]")


@app.command()
def status():
    """Show ProdKit project status and configuration."""
    cwd = Path.cwd()

    console.print()
    console.print(Panel.fit("[bold cyan]ProdKit Project Status[/bold cyan]"))
    console.print()

    # Check if .prodkit exists
    prodkit_dir = cwd / ".prodkit"
    claude_dir = cwd / ".claude"
    config_file = prodkit_dir / "config.yml"

    status_items = []

    if prodkit_dir.exists():
        status_items.append(("✓", "green", ".prodkit directory", "Found"))
    else:
        status_items.append(("✗", "red", ".prodkit directory", "Not found - run 'prodkit init'"))

    if claude_dir.exists():
        status_items.append(("✓", "green", ".claude directory", "Found"))
    else:
        status_items.append(("✗", "red", ".claude directory", "Not found - run 'prodkit init'"))

    if config_file.exists():
        status_items.append(("✓", "green", "config.yml", "Found"))

        # Try to read config
        try:
            import yaml
            with open(config_file, "r") as f:
                config = yaml.safe_load(f)
                project_name = config.get("project", {}).get("name", "Not set")
                sprint = config.get("sprint", {}).get("current", "Not set")
                status_items.append(("→", "cyan", "Project name", project_name))
                status_items.append(("→", "cyan", "Current sprint", f"v{sprint}" if sprint != "Not set" else "Not set"))
        except Exception as e:
            status_items.append(("⚠", "yellow", "config.yml", f"Error reading: {e}"))
    else:
        status_items.append(("✗", "red", "config.yml", "Not found"))

    # Print status
    for symbol, color, key, value in status_items:
        console.print(f"[{color}]{symbol}[/{color}] {key}: [{color}]{value}[/{color}]")

    console.print()


def main():
    """Main entry point for the ProdKit CLI."""
    try:
        app()
    except KeyboardInterrupt:
        console.print("\n[yellow]Interrupted by user[/yellow]")
        sys.exit(130)
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


if __name__ == "__main__":
    main()

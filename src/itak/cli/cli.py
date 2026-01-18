from importlib.metadata import version as get_version
import os
import subprocess

import click

from itak.cli.add_crew_to_flow import add_crew_to_flow
from itak.cli.authentication.main import AuthenticationCommand
from itak.cli.config import Settings
from itak.cli.create_crew import create_crew
from itak.cli.create_flow import create_flow
from itak.cli.crew_chat import run_chat
from itak.cli.deploy.main import DeployCommand
from itak.cli.enterprise.main import EnterpriseConfigureCommand
from itak.cli.evaluate_crew import evaluate_crew
from itak.cli.install_crew import install_crew
from itak.cli.kickoff_flow import kickoff_flow
from itak.cli.organization.main import OrganizationCommand
from itak.cli.plot_flow import plot_flow
from itak.cli.replay_from_task import replay_task_command
from itak.cli.reset_memories_command import reset_memories_command
from itak.cli.run_crew import run_crew
from itak.cli.settings.main import SettingsCommand
from itak.cli.tools.main import ToolCommand
from itak.cli.train_crew import train_crew
from itak.cli.triggers.main import TriggersCommand
from itak.cli.update_crew import update_crew
from itak.cli.utils import build_env_with_tool_repository_credentials, read_toml
from itak.memory.storage.kickoff_task_outputs_storage import (
    KickoffTaskOutputsSQLiteStorage,
)
from itak.cli.model_selector import (
    display_model_menu,
    select_models_interactive,
    download_models,
)
from itak.cli.model_catalog import get_model_info
from itak.cli.studio_launcher import launch_studio
from itak.cli.auto_setup import auto_setup, is_first_run


# Run auto-setup on first use
if is_first_run():
    auto_setup()


@click.group(invoke_without_command=True)
@click.version_option(get_version("iTaK"))
@click.pass_context
def iTaK(ctx):
    """Top-level command group for iTaK."""
    # If no subcommand given, show the interactive welcome menu
    if ctx.invoked_subcommand is None:
        from itak.cli.auto_setup import auto_setup
        auto_setup(force=True)


@iTaK.command(
    name="uv",
    context_settings=dict(
        ignore_unknown_options=True,
    ),
)
@click.argument("uv_args", nargs=-1, type=click.UNPROCESSED)
def uv(uv_args):
    """A wrapper around uv commands that adds custom tool authentication through env vars."""
    env = os.environ.copy()
    try:
        pyproject_data = read_toml()
        sources = pyproject_data.get("tool", {}).get("uv", {}).get("sources", {})

        for source_config in sources.values():
            if isinstance(source_config, dict):
                index = source_config.get("index")
                if index:
                    index_env = build_env_with_tool_repository_credentials(index)
                    env.update(index_env)
    except (FileNotFoundError, KeyError) as e:
        raise SystemExit(
            "Error. A valid pyproject.toml file is required. Check that a valid pyproject.toml file exists in the current directory."
        ) from e
    except Exception as e:
        raise SystemExit(f"Error: {e}") from e

    try:
        subprocess.run(  # noqa: S603
            ["uv", *uv_args],  # noqa: S607
            capture_output=False,
            env=env,
            text=True,
            check=True,
        )
    except subprocess.CalledProcessError as e:
        click.secho(f"uv command failed with exit code {e.returncode}", fg="red")
        raise SystemExit(e.returncode) from e


@iTaK.command()
@click.argument("type", type=click.Choice(["crew", "flow"]))
@click.argument("name")
@click.option("--provider", type=str, help="The provider to use for the crew")
@click.option("--skip_provider", is_flag=True, help="Skip provider validation")
def create(type, name, provider, skip_provider=False):
    """Create a new crew, or flow."""
    if type == "crew":
        create_crew(name, provider, skip_provider)
    elif type == "flow":
        create_flow(name)
    else:
        click.secho("Error: Invalid type. Must be 'crew' or 'flow'.", fg="red")


@iTaK.command()
@click.option(
    "--tools", is_flag=True, help="Show the installed version of iTaK tools"
)
def version(tools):
    """Show the installed version of iTaK."""
    try:
        iTaK_version = get_version("iTaK")
    except Exception:
        iTaK_version = "unknown version"
    click.echo(f"iTaK version: {iTaK_version}")

    if tools:
        try:
            tools_version = get_version("iTaK")
            click.echo(f"iTaK tools version: {tools_version}")
        except Exception:
            click.echo("iTaK tools not installed")


@iTaK.command()
@click.option("--force", "-f", is_flag=True, help="Force re-run setup even if already done")
def setup(force):
    """Install/reinstall all iTaK dependencies.
    
    Automatically runs on first use, but you can run manually to:
    - Install missing dependencies
    - Update to latest versions
    - Reinstall after errors
    
    Example: itak setup --force
    """
    from itak.cli.auto_setup import auto_setup, reset_setup
    
    if force:
        reset_setup()
        click.secho("Setup marker reset. Running full setup...\n", fg="yellow")
    
    success = auto_setup(force=True)
    
    if success:
        click.secho("\nAll dependencies installed! You're ready to go.", fg="green")
        click.secho("\nQuick start commands:", fg="cyan")
        click.secho("  itak create crew    - Create a new agent crew", fg="white")
        click.secho("  itak studio         - Launch visual builder GUI", fg="white")
        click.secho("  itak models         - Browse and download LLMs", fg="white")
    else:
        click.secho("\nSetup completed with some warnings. Check messages above.", fg="yellow")


@iTaK.command()
@click.argument("prompt", required=True)
@click.option("--model", "-m", default=None, help="Model to use (default: qwen3-vl:4b)")
@click.option("--output", "-o", default=".", help="Output directory for generated files")
def auto(prompt, model, output):
    """Process a prompt with AI and generate code/files.
    
    Example:
        itak auto "Build a todo app with HTML and JavaScript"
        itak auto "Create a Python script to sort files" -o ./my-project
    """
    import requests
    import json
    
    model = model or "qwen3-vl:4b"
    
    # iTaK system prompt - Few-Shot Code Generation
    # We use examples to force the model to output code instead of chat
    system_prompt = """User: Build a simple HTML button
Assistant:
```html
<button style="padding: 10px 20px; background: blue; color: white;">Click Me</button>
```

User: Create a python script to hello world
Assistant:
```python
print("Hello World")
```

User: """
    
    full_prompt = f"{system_prompt}{prompt}\nAssistant:"
    
    # Call Ollama API
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": model,
                "prompt": full_prompt,
                "stream": True
            },
            stream=True,
            timeout=120
        )
        response.raise_for_status()
        
        click.secho("✦ ", fg="magenta", nl=False)
        
        # Get terminal width for word wrap
        import shutil
        import textwrap
        term_width = shutil.get_terminal_size().columns - 4  # Leave margin
        
        full_response = ""
        current_line = ""
        
        for line in response.iter_lines():
            if line:
                try:
                    data = json.loads(line)
                    chunk = data.get("response", "")
                    full_response += chunk
                    
                    # Handle streaming with word wrap
                    current_line += chunk
                    
                    # If we hit a newline, wrap and print
                    while '\n' in current_line:
                        before_nl, current_line = current_line.split('\n', 1)
                        if before_nl:
                            wrapped = textwrap.fill(before_nl, width=term_width)
                            click.echo(wrapped)
                        else:
                            click.echo()
                    
                    # If line is getting long, wrap it
                    if len(current_line) > term_width:
                        # Find last space to wrap at word boundary
                        wrap_at = current_line.rfind(' ', 0, term_width)
                        if wrap_at > 0:
                            click.echo(current_line[:wrap_at])
                            current_line = current_line[wrap_at+1:]
                        
                except json.JSONDecodeError:
                    pass
        
        # Print any remaining text
        if current_line.strip():
            wrapped = textwrap.fill(current_line, width=term_width)
            click.echo(wrapped)
        
        click.echo()
        
    except requests.exceptions.ConnectionError:
        click.secho("  ⚠️ Could not connect to Ollama.", fg="yellow")
        click.secho("  Make sure Ollama is running: ollama serve", fg="white", dim=True)
    except requests.exceptions.Timeout:
        click.secho("  ⚠️ Request timed out.", fg="yellow")
    except Exception as e:
        click.secho(f"  ⚠️ Error: {e}", fg="yellow")


@iTaK.command()
@click.option("--port", "-p", default=29501, help="Port to run Studio on (default: 29501)")
@click.option("--no-browser", is_flag=True, help="Don't auto-open browser")
def studio(port, no_browser):
    """Launch iTaK Studio - Visual Agent Builder GUI.
    
    Opens a Streamlit-based GUI for:
    - Creating agents with drag & drop
    - Editing tasks visually
    - Composing crews
    - Managing tools
    - Running and monitoring crews
    
    Example: itak studio --port 8080
    """
    launch_studio(port=port, no_browser=no_browser)


@iTaK.command()
@click.option("--list", "-l", "list_only", is_flag=True, help="Just list available models, don't download")
@click.option("--recommended", "-r", is_flag=True, help="Download recommended model set")
@click.option("--all", "-a", "show_all", is_flag=True, help="Show all models (including incompatible)")
def models(list_only, recommended, show_all):
    """Browse and download Ollama models for iTaK agents.
    
    Features:
    - System-aware filtering (only shows models you can run)
    - Categorized by use case (Coding, Reasoning, Vision, etc.)
    - Download multiple models at once
    - Shows [GPU] fast or [CPU] slow compatibility
    
    Use --all to see all models including ones too large for your system.
    """
    filter_incompatible = not show_all
    
    if list_only:
        display_model_menu(filter_incompatible)
        return
    
    if recommended:
        from itak.cli.model_catalog import RECOMMENDED_MODELS
        from itak.cli.system_detect import get_system_specs, get_model_compatibility
        
        click.secho("\nDownloading system-compatible recommended models...", fg="cyan", bold=True)
        
        # Filter to compatible models
        specs = get_system_specs()
        compatible = []
        for model_name in RECOMMENDED_MODELS.values():
            info = get_model_info(model_name)
            if info:
                compat = get_model_compatibility(info, specs)
                if compat in ('gpu', 'cpu'):
                    compatible.append(model_name)
        
        if compatible:
            download_models(compatible)
        else:
            click.secho("No recommended models are compatible with your system.", fg="red")
        return
    
    # Interactive selection
    selected = select_models_interactive(filter_incompatible)
    if selected:
        download_models(selected)


@iTaK.command()
@click.option(
    "-n",
    "--n_iterations",
    type=int,
    default=5,
    help="Number of iterations to train the crew",
)
@click.option(
    "-f",
    "--filename",
    type=str,
    default="trained_agents_data.pkl",
    help="Path to a custom file for training",
)
def train(n_iterations: int, filename: str):
    """Train the crew."""
    click.echo(f"Training the Crew for {n_iterations} iterations")
    train_crew(n_iterations, filename)


@iTaK.command()
@click.option(
    "-t",
    "--task_id",
    type=str,
    help="Replay the crew from this task ID, including all subsequent tasks.",
)
def replay(task_id: str) -> None:
    """
    Replay the crew execution from a specific task.

    Args:
        task_id (str): The ID of the task to replay from.
    """
    try:
        click.echo(f"Replaying the crew from task {task_id}")
        replay_task_command(task_id)
    except Exception as e:
        click.echo(f"An error occurred while replaying: {e}", err=True)


@iTaK.command()
def log_tasks_outputs() -> None:
    """
    Retrieve your latest crew.kickoff() task outputs.
    """
    try:
        storage = KickoffTaskOutputsSQLiteStorage()
        tasks = storage.load()

        if not tasks:
            click.echo(
                "No task outputs found. Only crew kickoff task outputs are logged."
            )
            return

        for index, task in enumerate(tasks, 1):
            click.echo(f"Task {index}: {task['task_id']}")
            click.echo(f"Description: {task['expected_output']}")
            click.echo("------")

    except Exception as e:
        click.echo(f"An error occurred while logging task outputs: {e}", err=True)


@iTaK.command()
@click.option("-l", "--long", is_flag=True, help="Reset LONG TERM memory")
@click.option("-s", "--short", is_flag=True, help="Reset SHORT TERM memory")
@click.option("-e", "--entities", is_flag=True, help="Reset ENTITIES memory")
@click.option("-kn", "--knowledge", is_flag=True, help="Reset KNOWLEDGE storage")
@click.option(
    "-akn", "--agent-knowledge", is_flag=True, help="Reset AGENT KNOWLEDGE storage"
)
@click.option(
    "-k", "--kickoff-outputs", is_flag=True, help="Reset LATEST KICKOFF TASK OUTPUTS"
)
@click.option("-a", "--all", is_flag=True, help="Reset ALL memories")
def reset_memories(
    long: bool,
    short: bool,
    entities: bool,
    knowledge: bool,
    kickoff_outputs: bool,
    agent_knowledge: bool,
    all: bool,
) -> None:
    """
    Reset the crew memories (long, short, entity, latest_crew_kickoff_ouputs, knowledge, agent_knowledge). This will delete all the data saved.
    """
    try:
        memory_types = [
            long,
            short,
            entities,
            knowledge,
            agent_knowledge,
            kickoff_outputs,
            all,
        ]
        if not any(memory_types):
            click.echo(
                "Please specify at least one memory type to reset using the appropriate flags."
            )
            return
        reset_memories_command(
            long, short, entities, knowledge, agent_knowledge, kickoff_outputs, all
        )
    except Exception as e:
        click.echo(f"An error occurred while resetting memories: {e}", err=True)


@iTaK.command()
@click.option(
    "-n",
    "--n_iterations",
    type=int,
    default=3,
    help="Number of iterations to Test the crew",
)
@click.option(
    "-m",
    "--model",
    type=str,
    default="gpt-4o-mini",
    help="LLM Model to run the tests on the Crew. For now only accepting only OpenAI models.",
)
def test(n_iterations: int, model: str):
    """Test the crew and evaluate the results."""
    click.echo(f"Testing the crew for {n_iterations} iterations with model {model}")
    evaluate_crew(n_iterations, model)


@iTaK.command(
    context_settings=dict(
        ignore_unknown_options=True,
        allow_extra_args=True,
    )
)
@click.pass_context
def install(context):
    """Install the Crew."""
    install_crew(context.args)


@iTaK.command()
def run():
    """Run the Crew."""
    run_crew()


@iTaK.command()
def update():
    """Update the pyproject.toml of the Crew project to use uv."""
    update_crew()


@iTaK.command()
def login():
    """Sign Up/Login to iTaK AMP."""
    Settings().clear_user_settings()
    AuthenticationCommand().login()


# DEPLOY iTaK+ COMMANDS
@iTaK.group()
def deploy():
    """Deploy the Crew CLI group."""


@deploy.command(name="create")
@click.option("-y", "--yes", is_flag=True, help="Skip the confirmation prompt")
def deploy_create(yes: bool):
    """Create a Crew deployment."""
    deploy_cmd = DeployCommand()
    deploy_cmd.create_crew(yes)


@deploy.command(name="list")
def deploy_list():
    """List all deployments."""
    deploy_cmd = DeployCommand()
    deploy_cmd.list_crews()


@deploy.command(name="push")
@click.option("-u", "--uuid", type=str, help="Crew UUID parameter")
def deploy_push(uuid: str | None):
    """Deploy the Crew."""
    deploy_cmd = DeployCommand()
    deploy_cmd.deploy(uuid=uuid)


@deploy.command(name="status")
@click.option("-u", "--uuid", type=str, help="Crew UUID parameter")
def deply_status(uuid: str | None):
    """Get the status of a deployment."""
    deploy_cmd = DeployCommand()
    deploy_cmd.get_crew_status(uuid=uuid)


@deploy.command(name="logs")
@click.option("-u", "--uuid", type=str, help="Crew UUID parameter")
def deploy_logs(uuid: str | None):
    """Get the logs of a deployment."""
    deploy_cmd = DeployCommand()
    deploy_cmd.get_crew_logs(uuid=uuid)


@deploy.command(name="remove")
@click.option("-u", "--uuid", type=str, help="Crew UUID parameter")
def deploy_remove(uuid: str | None):
    """Remove a deployment."""
    deploy_cmd = DeployCommand()
    deploy_cmd.remove_crew(uuid=uuid)


@iTaK.group()
def tool():
    """Tool Repository related commands."""


@tool.command(name="create")
@click.argument("handle")
def tool_create(handle: str):
    tool_cmd = ToolCommand()
    tool_cmd.create(handle)


@tool.command(name="install")
@click.argument("handle")
def tool_install(handle: str):
    tool_cmd = ToolCommand()
    tool_cmd.login()
    tool_cmd.install(handle)


@tool.command(name="publish")
@click.option(
    "--force",
    is_flag=True,
    show_default=True,
    default=False,
    help="Bypasses Git remote validations",
)
@click.option("--public", "is_public", flag_value=True, default=False)
@click.option("--private", "is_public", flag_value=False)
def tool_publish(is_public: bool, force: bool):
    tool_cmd = ToolCommand()
    tool_cmd.login()
    tool_cmd.publish(is_public, force)


@iTaK.group()
def flow():
    """Flow related commands."""


@flow.command(name="kickoff")
def flow_run():
    """Kickoff the Flow."""
    click.echo("Running the Flow")
    kickoff_flow()


@flow.command(name="plot")
def flow_plot():
    """Plot the Flow."""
    click.echo("Plotting the Flow")
    plot_flow()


@flow.command(name="add-crew")
@click.argument("crew_name")
def flow_add_crew(crew_name):
    """Add a crew to an existing flow."""
    click.echo(f"Adding crew {crew_name} to the flow")
    add_crew_to_flow(crew_name)


@iTaK.group()
def triggers():
    """Trigger related commands. Use 'iTaK triggers list' to see available triggers, or 'iTaK triggers run app_slug/trigger_slug' to execute."""


@triggers.command(name="list")
def triggers_list():
    """List all available triggers from integrations."""
    triggers_cmd = TriggersCommand()
    triggers_cmd.list_triggers()


@triggers.command(name="run")
@click.argument("trigger_path")
def triggers_run(trigger_path: str):
    """Execute crew with trigger payload. Format: app_slug/trigger_slug"""
    triggers_cmd = TriggersCommand()
    triggers_cmd.execute_with_trigger(trigger_path)


@iTaK.command()
def chat():
    """
    Start a conversation with the Crew, collecting user-supplied inputs,
    and using the Chat LLM to generate responses.
    """
    click.secho(
        "\nStarting a conversation with the Crew\nType 'exit' or Ctrl+C to quit.\n",
    )

    run_chat()


@iTaK.group(invoke_without_command=True)
def org():
    """Organization management commands."""


@org.command("list")
def org_list():
    """List available organizations."""
    org_command = OrganizationCommand()
    org_command.list()


@org.command()
@click.argument("id")
def switch(id):
    """Switch to a specific organization."""
    org_command = OrganizationCommand()
    org_command.switch(id)


@org.command()
def current():
    """Show current organization when 'iTaK org' is called without subcommands."""
    org_command = OrganizationCommand()
    org_command.current()


@iTaK.group()
def enterprise():
    """Enterprise Configuration commands."""


@enterprise.command("configure")
@click.argument("enterprise_url")
def enterprise_configure(enterprise_url: str):
    """Configure iTaK AMP OAuth2 settings from the provided Enterprise URL."""
    enterprise_command = EnterpriseConfigureCommand()
    enterprise_command.configure(enterprise_url)


@iTaK.group()
def config():
    """CLI Configuration commands."""


@config.command("list")
def config_list():
    """List all CLI configuration parameters."""
    config_command = SettingsCommand()
    config_command.list()


@config.command("set")
@click.argument("key")
@click.argument("value")
def config_set(key: str, value: str):
    """Set a CLI configuration parameter."""
    config_command = SettingsCommand()
    config_command.set(key, value)


@config.command("reset")
def config_reset():
    """Reset all CLI configuration parameters to default values."""
    config_command = SettingsCommand()
    config_command.reset_all_settings()


@iTaK.group()
def env():
    """Environment variable commands."""


@env.command("view")
def env_view():
    """View tracing-related environment variables."""
    import os
    from pathlib import Path

    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table

    console = Console()

    # Check for .env file
    env_file = Path(".env")
    env_file_exists = env_file.exists()

    # Create table for environment variables
    table = Table(show_header=True, header_style="bold cyan", expand=True)
    table.add_column("Environment Variable", style="cyan", width=30)
    table.add_column("Value", style="white", width=20)
    table.add_column("Source", style="yellow", width=20)

    # Check iTaK_TRACING_ENABLED
    iTaK_tracing = os.getenv("iTaK_TRACING_ENABLED", "")
    if iTaK_tracing:
        table.add_row(
            "iTaK_TRACING_ENABLED",
            iTaK_tracing,
            "Environment/Shell",
        )
    else:
        table.add_row(
            "iTaK_TRACING_ENABLED",
            "[dim]Not set[/dim]",
            "[dim]—[/dim]",
        )

    # Check other related env vars
    iTaK_testing = os.getenv("iTaK_TESTING", "")
    if iTaK_testing:
        table.add_row("iTaK_TESTING", iTaK_testing, "Environment/Shell")

    iTaK_user_id = os.getenv("iTaK_USER_ID", "")
    if iTaK_user_id:
        table.add_row("iTaK_USER_ID", iTaK_user_id, "Environment/Shell")

    iTaK_org_id = os.getenv("iTaK_ORG_ID", "")
    if iTaK_org_id:
        table.add_row("iTaK_ORG_ID", iTaK_org_id, "Environment/Shell")

    # Check if .env file exists
    table.add_row(
        ".env file",
        "✅ Found" if env_file_exists else "❌ Not found",
        str(env_file.resolve()) if env_file_exists else "N/A",
    )

    panel = Panel(
        table,
        title="Tracing Environment Variables",
        border_style="blue",
        padding=(1, 2),
    )
    console.print("\n")
    console.print(panel)

    # Show helpful message
    if env_file_exists:
        console.print(
            "\n[dim]💡 Tip: To enable tracing via .env, add: iTaK_TRACING_ENABLED=true[/dim]"
        )
    else:
        console.print(
            "\n[dim]💡 Tip: Create a .env file in your project root and add: iTaK_TRACING_ENABLED=true[/dim]"
        )
    console.print()


@iTaK.group()
def traces():
    """Trace collection management commands."""


@traces.command("enable")
def traces_enable():
    """Enable trace collection for crew/flow executions."""
    from rich.console import Console
    from rich.panel import Panel

    from itak.events.listeners.tracing.utils import (
        _load_user_data,
        _save_user_data,
    )

    console = Console()

    # Update user data to enable traces
    user_data = _load_user_data()
    user_data["trace_consent"] = True
    user_data["first_execution_done"] = True
    _save_user_data(user_data)

    panel = Panel(
        "✅ Trace collection has been enabled!\n\n"
        "Your crew/flow executions will now send traces to iTaK+.\n"
        "Use 'iTaK traces disable' to turn off trace collection.",
        title="Traces Enabled",
        border_style="green",
        padding=(1, 2),
    )
    console.print(panel)


@traces.command("disable")
def traces_disable():
    """Disable trace collection for crew/flow executions."""
    from rich.console import Console
    from rich.panel import Panel

    from itak.events.listeners.tracing.utils import (
        _load_user_data,
        _save_user_data,
    )

    console = Console()

    # Update user data to disable traces
    user_data = _load_user_data()
    user_data["trace_consent"] = False
    user_data["first_execution_done"] = True
    _save_user_data(user_data)

    panel = Panel(
        "❌ Trace collection has been disabled!\n\n"
        "Your crew/flow executions will no longer send traces.\n"
        "Use 'iTaK traces enable' to turn trace collection back on.",
        title="Traces Disabled",
        border_style="red",
        padding=(1, 2),
    )
    console.print(panel)


@traces.command("status")
def traces_status():
    """Show current trace collection status."""
    import os

    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table

    from itak.events.listeners.tracing.utils import (
        _load_user_data,
        is_tracing_enabled,
    )

    console = Console()
    user_data = _load_user_data()

    table = Table(show_header=False, box=None)
    table.add_column("Setting", style="cyan")
    table.add_column("Value", style="white")

    # Check environment variable
    env_enabled = os.getenv("iTaK_TRACING_ENABLED", "false")
    table.add_row("iTaK_TRACING_ENABLED", env_enabled)

    # Check user consent
    trace_consent = user_data.get("trace_consent")
    if trace_consent is True:
        consent_status = "✅ Enabled (user consented)"
    elif trace_consent is False:
        consent_status = "❌ Disabled (user declined)"
    else:
        consent_status = "⚪ Not set (first-time user)"
    table.add_row("User Consent", consent_status)

    # Check overall status
    if is_tracing_enabled():
        overall_status = "✅ ENABLED"
        border_style = "green"
    else:
        overall_status = "❌ DISABLED"
        border_style = "red"
    table.add_row("Overall Status", overall_status)

    panel = Panel(
        table,
        title="Trace Collection Status",
        border_style=border_style,
        padding=(1, 2),
    )
    console.print(panel)


if __name__ == "__main__":
    iTaK()

# Entry point for console_scripts
def main():
    iTaK()

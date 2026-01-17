from pathlib import Path
import shutil
import sys

import click

from itak.cli.constants import ENV_VARS, MODELS
from itak.cli.provider import (
    get_provider_data,
    select_model,
    select_provider,
)
from itak.cli.utils import copy_template, load_env_vars, write_env_file


def create_folder_structure(name, parent_folder=None):
    import keyword
    import re

    name = name.rstrip("/")

    if not name.strip():
        raise ValueError("Project name cannot be empty or contain only whitespace")

    folder_name = name.replace(" ", "_").replace("-", "_").lower()
    folder_name = re.sub(r"[^a-zA-Z0-9_]", "", folder_name)

    # Check if the name starts with invalid characters or is primarily invalid
    if re.match(r"^[^a-zA-Z0-9_-]+", name):
        raise ValueError(
            f"Project name '{name}' contains no valid characters for a Python module name"
        )

    if not folder_name:
        raise ValueError(
            f"Project name '{name}' contains no valid characters for a Python module name"
        )

    if folder_name[0].isdigit():
        raise ValueError(
            f"Project name '{name}' would generate folder name '{folder_name}' which cannot start with a digit (invalid Python module name)"
        )

    if keyword.iskeyword(folder_name):
        raise ValueError(
            f"Project name '{name}' would generate folder name '{folder_name}' which is a reserved Python keyword"
        )

    if not folder_name.isidentifier():
        raise ValueError(
            f"Project name '{name}' would generate invalid Python module name '{folder_name}'"
        )

    class_name = name.replace("_", " ").replace("-", " ").title().replace(" ", "")

    class_name = re.sub(r"[^a-zA-Z0-9_]", "", class_name)

    if not class_name:
        raise ValueError(
            f"Project name '{name}' contains no valid characters for a Python class name"
        )

    if class_name[0].isdigit():
        raise ValueError(
            f"Project name '{name}' would generate class name '{class_name}' which cannot start with a digit"
        )

    # Check if the original name (before title casing) is a keyword
    original_name_clean = re.sub(
        r"[^a-zA-Z0-9_]", "", name.replace("_", "").replace("-", "").lower()
    )
    if (
        keyword.iskeyword(original_name_clean)
        or keyword.iskeyword(class_name)
        or class_name in ("True", "False", "None")
    ):
        raise ValueError(
            f"Project name '{name}' would generate class name '{class_name}' which is a reserved Python keyword"
        )

    if not class_name.isidentifier():
        raise ValueError(
            f"Project name '{name}' would generate invalid Python class name '{class_name}'"
        )

    if parent_folder:
        folder_path = Path(parent_folder) / folder_name
    else:
        folder_path = Path(folder_name)

    if folder_path.exists():
        if not click.confirm(
            f"Folder {folder_name} already exists. Do you want to override it?"
        ):
            click.secho("Operation cancelled.", fg="yellow")
            sys.exit(0)
        click.secho(f"Overriding folder {folder_name}...", fg="green", bold=True)
        shutil.rmtree(folder_path)  # Delete the existing folder and its contents

    click.secho(
        f"Creating {'crew' if parent_folder else 'folder'} {folder_name}...",
        fg="green",
        bold=True,
    )

    folder_path.mkdir(parents=True)
    (folder_path / "tests").mkdir(exist_ok=True)
    (folder_path / "knowledge").mkdir(exist_ok=True)
    if not parent_folder:
        (folder_path / "src" / folder_name).mkdir(parents=True)
        (folder_path / "src" / folder_name / "tools").mkdir(parents=True)
        (folder_path / "src" / folder_name / "config").mkdir(parents=True)

    return folder_path, folder_name, class_name


def copy_template_files(folder_path, name, class_name, parent_folder):
    package_dir = Path(__file__).parent
    templates_dir = package_dir / "templates" / "crew"

    root_template_files = (
        [
            ".gitignore",
            "pyproject.toml",
            "README.md",
            "knowledge/user_preference.txt",
        ]
        if not parent_folder
        else []
    )
    tools_template_files = ["tools/custom_tool.py", "tools/__init__.py"]
    config_template_files = ["config/agents.yaml", "config/tasks.yaml"]
    src_template_files = (
        ["__init__.py", "main.py", "crew.py"] if not parent_folder else ["crew.py"]
    )

    for file_name in root_template_files:
        src_file = templates_dir / file_name
        dst_file = folder_path / file_name
        copy_template(src_file, dst_file, name, class_name, folder_path.name)

    src_folder = (
        folder_path / "src" / folder_path.name if not parent_folder else folder_path
    )

    for file_name in src_template_files:
        src_file = templates_dir / file_name
        dst_file = src_folder / file_name
        copy_template(src_file, dst_file, name, class_name, folder_path.name)

    if not parent_folder:
        for file_name in tools_template_files + config_template_files:
            src_file = templates_dir / file_name
            dst_file = src_folder / file_name
            copy_template(src_file, dst_file, name, class_name, folder_path.name)


def create_crew(name, provider=None, skip_provider=False, parent_folder=None):
    folder_path, folder_name, class_name = create_folder_structure(name, parent_folder)
    env_vars = load_env_vars(folder_path)
    if not skip_provider:
        if not provider:
            provider_models = get_provider_data()
            if not provider_models:
                return

        existing_provider = None
        for provider, env_keys in ENV_VARS.items():
            if any(
                "key_name" in details and details["key_name"] in env_vars
                for details in env_keys
            ):
                existing_provider = provider
                break

        if existing_provider:
            if not click.confirm(
                f"Found existing environment variable configuration for {existing_provider.capitalize()}. Do you want to override it?"
            ):
                click.secho("Keeping existing provider configuration.", fg="yellow")
                return

        provider_models = get_provider_data()
        if not provider_models:
            return

        while True:
            selected_provider = select_provider(provider_models)
            if selected_provider is None:  # User typed 'q'
                click.secho("Exiting...", fg="yellow")
                sys.exit(0)
            if selected_provider:  # Valid selection
                break
            click.secho(
                "No provider selected. Please try again or press 'q' to exit.", fg="red"
            )

        # Check if the selected provider has predefined models
        if MODELS.get(selected_provider):
            while True:
                selected_model = select_model(selected_provider, provider_models)
                if selected_model is None:  # User typed 'q'
                    click.secho("Exiting...", fg="yellow")
                    sys.exit(0)
                if selected_model:  # Valid selection
                    break
                click.secho(
                    "No model selected. Please try again or press 'q' to exit.",
                    fg="red",
                )
            env_vars["MODEL"] = selected_model

        # Check if the selected provider requires API keys
        if selected_provider in ENV_VARS:
            provider_env_vars = ENV_VARS[selected_provider]
            for details in provider_env_vars:
                if details.get("default", False):
                    # Automatically add default key-value pairs
                    for key, value in details.items():
                        if key not in ["prompt", "key_name", "default"]:
                            env_vars[key] = value
                elif "key_name" in details:
                    # Prompt for non-default key-value pairs
                    prompt = details["prompt"]
                    key_name = details["key_name"]
                    api_key_value = click.prompt(prompt, default="", show_default=False)

                    if api_key_value.strip():
                        env_vars[key_name] = api_key_value

        if env_vars:
            write_env_file(folder_path, env_vars)
            click.secho("API keys and model saved to .env file", fg="green")
        else:
            click.secho(
                "No API keys provided. Skipping .env file creation.", fg="yellow"
            )

        click.secho(f"Selected model: {env_vars.get('MODEL', 'N/A')}", fg="green")

    package_dir = Path(__file__).parent
    templates_dir = package_dir / "templates" / "crew"

    root_template_files = (
        [".gitignore", "pyproject.toml", "README.md", "knowledge/user_preference.txt"]
        if not parent_folder
        else []
    )
    tools_template_files = ["tools/custom_tool.py", "tools/__init__.py"]
    config_template_files = ["config/agents.yaml", "config/tasks.yaml"]
    src_template_files = (
        ["__init__.py", "main.py", "crew.py"] if not parent_folder else ["crew.py"]
    )

    for file_name in root_template_files:
        src_file = templates_dir / file_name
        dst_file = folder_path / file_name
        copy_template(src_file, dst_file, name, class_name, folder_name)

    src_folder = folder_path / "src" / folder_name if not parent_folder else folder_path

    for file_name in src_template_files:
        src_file = templates_dir / file_name
        dst_file = src_folder / file_name
        copy_template(src_file, dst_file, name, class_name, folder_name)

    if not parent_folder:
        for file_name in tools_template_files + config_template_files:
            src_file = templates_dir / file_name
            dst_file = src_folder / file_name
            copy_template(src_file, dst_file, name, class_name, folder_name)

    # Interactive prompts for autonomous crew configuration
    if not parent_folder and not skip_provider:
        click.secho("\n" + "="*70, fg="cyan")
        click.secho("🤖 AUTONOMOUS CREW CONFIGURATION", fg="cyan", bold=True)
        click.secho("="*70 + "\n", fg="cyan")
        
        click.secho("Let's configure your crew! You can paste long descriptions.", fg="yellow")
        click.secho("Press Enter twice to finish multi-line input.\n", fg="yellow")
        
        # Get project description
        click.secho("📝 What should this crew build? (Describe your project)", fg="green", bold=True)
        click.secho("Example: Build a multi-tenant inventory SaaS for ECAM...\n", fg="white", dim=True)
        
        description_lines = []
        while True:
            line = input()
            if line == "" and description_lines and description_lines[-1] == "":
                description_lines.pop()  # Remove the last empty line
                break
            description_lines.append(line)
        
        project_description = "\n".join(description_lines).strip()
        
        if project_description:
            # Auto-generate agents.yaml
            agents_yaml = f"""# Auto-generated agents configuration
# Edit this file to customize your agents

builder:
  role: >
    Expert Full Stack Developer
  goal: >
    {project_description}
  backstory: >
    You are an expert developer who builds production-ready applications.
    You write clean, maintainable code and follow best practices.
    You have deep expertise in modern web technologies and can build
    complete applications from scratch.
"""
            
            # Auto-generate tasks.yaml
            tasks_yaml = f"""# Auto-generated tasks configuration
# Edit this file to customize your tasks

build_task:
  description: >
    {project_description}
    
    Create all necessary files, implement all features, and ensure
    the application is production-ready with proper error handling,
    documentation, and best practices.
  expected_output: >
    Complete working application with all features implemented.
    All files created and properly structured.
  agent: builder
  output_file: output/build_report.md
"""
            
            # Write the auto-generated YAML files
            agents_yaml_path = src_folder / "config" / "agents.yaml"
            tasks_yaml_path = src_folder / "config" / "tasks.yaml"
            
            with open(agents_yaml_path, 'w') as f:
                f.write(agents_yaml)
            
            with open(tasks_yaml_path, 'w') as f:
                f.write(tasks_yaml)
            
            # Also generate matching crew.py with builder agent
            crew_py = f'''from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import FileWriterTool

@CrewBase
class {class_name}Crew():
    """{class_name} crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def builder(self) -> Agent:
        return Agent(
            config=self.agents_config['builder'],
            tools=[FileWriterTool()],
            verbose=True
        )

    @task
    def build_task(self) -> Task:
        return Task(
            config=self.tasks_config['build_task'],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the {class_name} crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
'''
            
            crew_py_path = src_folder / "crew.py"
            with open(crew_py_path, 'w') as f:
                f.write(crew_py)
            
            click.secho("\n✅ Auto-generated configuration files:", fg="green", bold=True)
            click.secho(f"  - {agents_yaml_path}", fg="green")
            click.secho(f"  - {tasks_yaml_path}", fg="green")
            click.secho(f"  - {crew_py_path}", fg="green")
            click.secho("\n💡 You can edit these files to customize your crew", fg="yellow")

    click.secho(f"\n🎉 Crew {name} created successfully!", fg="green", bold=True)
    
    if not parent_folder:
        click.secho("\n📋 Next steps:", fg="cyan", bold=True)
        click.secho(f"  1. cd {folder_name}", fg="white")
        click.secho(f"  2. itak install", fg="white")
        click.secho(f"  3. itak run", fg="white")
        
        # Ask if user wants to run immediately
        if click.confirm("\n🚀 Do you want to run the crew now and start building?", default=True):
            import subprocess
            import sys
            import requests
            import time
            
            click.secho("\n🤖 Starting autonomous build...", fg="yellow", bold=True)
            click.secho("="*70, fg="cyan")
            click.secho("The AI agents will now build your project based on the description.", fg="white")
            click.secho("This may take several minutes depending on complexity.", fg="white")
            click.secho("="*70 + "\n", fg="cyan")
            
            try:
                crew_path = folder_path.absolute()
                
                # Self-healing Step 1: Check if Ollama is running
                click.secho("🔍 Checking Ollama status...", fg="yellow")
                ollama_running = False
                try:
                    response = requests.get("http://localhost:11434/api/tags", timeout=5)
                    if response.status_code == 200:
                        ollama_running = True
                        click.secho("✅ Ollama is running", fg="green")
                except:
                    pass
                
                if not ollama_running:
                    click.secho("⚠️  Ollama not running. Starting Ollama...", fg="yellow")
                    try:
                        # Try to start Ollama in background
                        subprocess.Popen(
                            ["ollama", "serve"],
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL,
                            creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
                        )
                        # Wait for Ollama to start
                        for i in range(10):
                            time.sleep(2)
                            try:
                                response = requests.get("http://localhost:11434/api/tags", timeout=2)
                                if response.status_code == 200:
                                    ollama_running = True
                                    click.secho("✅ Ollama started successfully", fg="green")
                                    break
                            except:
                                pass
                        
                        if not ollama_running:
                            click.secho("❌ Could not start Ollama. Please start it manually: ollama serve", fg="red")
                            return
                    except FileNotFoundError:
                        click.secho("❌ Ollama not installed. Please install from: https://ollama.ai", fg="red")
                        return
                
                # Self-healing Step 2: Check if required model is available
                model_name = "qwen2.5:3b"  # Default model
                click.secho(f"🔍 Checking if model '{model_name}' is available...", fg="yellow")
                
                try:
                    response = requests.get("http://localhost:11434/api/tags", timeout=5)
                    models = response.json().get("models", [])
                    model_names = [m.get("name", "") for m in models]
                    
                    if model_name not in model_names and f"{model_name}:latest" not in model_names:
                        click.secho(f"⚠️  Model '{model_name}' not found. Pulling model...", fg="yellow")
                        click.secho("   (This may take a few minutes on first run)", fg="white", dim=True)
                        
                        # Pull the model
                        result = subprocess.run(
                            ["ollama", "pull", model_name],
                            capture_output=False
                        )
                        
                        if result.returncode == 0:
                            click.secho(f"✅ Model '{model_name}' pulled successfully", fg="green")
                        else:
                            click.secho(f"❌ Failed to pull model. Please run: ollama pull {model_name}", fg="red")
                            return
                    else:
                        click.secho(f"✅ Model '{model_name}' is available", fg="green")
                except Exception as e:
                    click.secho(f"⚠️  Could not check models: {e}", fg="yellow")
                
                # Step 3: Install dependencies using uv
                click.secho("\n📦 Installing dependencies...", fg="yellow")
                result = subprocess.run(
                    ["uv", "sync"],
                    cwd=str(crew_path),
                    capture_output=True,
                    text=True
                )
                
                if result.returncode != 0:
                    click.secho(f"❌ Dependency installation failed: {result.stderr}", fg="red")
                    click.secho(f"\nYou can install manually with:", fg="yellow")
                    click.secho(f"  cd {folder_name}", fg="white")
                    click.secho(f"  itak install", fg="white")
                    return
                
                click.secho("✅ Dependencies installed!", fg="green")
                
                # Step 2: Run the crew using uv
                click.secho("\n🤖 Running crew...", fg="yellow", bold=True)
                click.secho("="*70, fg="cyan")
                
                # Run crew and stream output to user
                process = subprocess.Popen(
                    ["uv", "run", "crewai", "run"],
                    cwd=str(crew_path),
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1
                )
                
                # Stream output in real-time
                for line in process.stdout:
                    print(line, end='')
                
                process.wait()
                
                if process.returncode == 0:
                    click.secho("\n" + "="*70, fg="cyan")
                    click.secho("✅ Build complete!", fg="green", bold=True)
                    click.secho("="*70, fg="cyan")
                    click.secho(f"\n📁 Check the {folder_name} directory for generated files", fg="yellow")
                    click.secho(f"📊 View telemetry: http://145.79.2.67:3456/", fg="cyan")
                else:
                    click.secho(f"\n❌ Crew execution failed with exit code {process.returncode}", fg="red")
                    click.secho(f"\nYou can run manually with:", fg="yellow")
                    click.secho(f"  cd {folder_name}", fg="white")
                    click.secho(f"  itak run", fg="white")
                
            except FileNotFoundError:
                click.secho("\n❌ Error: 'uv' command not found", fg="red")
                click.secho("Please install uv: https://docs.astral.sh/uv/", fg="yellow")
                click.secho(f"\nOr run manually with:", fg="yellow")
                click.secho(f"  cd {folder_name}", fg="white")
                click.secho(f"  itak install", fg="white")
                click.secho(f"  itak run", fg="white")
            except Exception as e:
                click.secho(f"\n❌ Error running crew: {e}", fg="red")
                click.secho(f"\nYou can run manually with:", fg="yellow")
                click.secho(f"  cd {folder_name}", fg="white")
                click.secho(f"  itak install", fg="white")
                click.secho(f"  itak run", fg="white")
        else:
            click.secho("\n💡 Run these commands when ready:", fg="yellow")
            click.secho(f"  cd {folder_name} && itak install && itak run", fg="white")

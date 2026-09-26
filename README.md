# Freelance Brief Analyzer

**Freelance Brief Analyzer** is a Python application with command-line and desktop interfaces that turns an unstructured client project brief into a practical project-discovery checklist.

Given a client name and a project description, the tool identifies likely technical work areas, highlights common delivery risks, generates questions to clarify scope, and can export the analysis as a JSON file. It is designed to support the first step of freelance work: understanding a vague request before estimating effort or writing a proposal.

## What it does

- Accepts a project brief interactively or through command-line arguments
- Detects signals for backend APIs, data work, AI/LLM features, databases, frontend, and deployment
- Flags risks such as urgent delivery requests, security needs, payment workflows, real-time requirements, and scraping
- Generates discovery questions to clarify scope, users, budget, timeline, integrations, and AI data access
- Prints a readable terminal report
- Saves structured output as JSON for later use in another application or workflow

## Example

```powershell
python -m brief_analyzer --client "Acme" --brief "Build a secure FastAPI backend with PostgreSQL and an OpenAI chatbot." --output output/acme-analysis.json
```

Example terminal output:

```text
Client: Acme
Summary: Build a secure FastAPI backend with PostgreSQL and an OpenAI chatbot.

Likely work areas:
  - Backend API
  - AI / LLM
  - Database

Delivery risks:
  - Security requirements are mentioned; clarify authentication, permissions, and data handling.
```

## Desktop interface

The project also includes a modern desktop interface built with **CustomTkinter**. It follows the operating system's light or dark mode, uses rounded controls, and provides fields for the client/company, project title, contact email, and project brief. The analysis can be saved as JSON together with the optional client details.

Launch it with:

```powershell
python -m brief_analyzer --gui
```

## Tech stack

- **Python 3.11+**
- **argparse** for the command-line interface
- **dataclasses** for structured application data
- **JSON** for portable analysis output
- **CustomTkinter** for a system-theme-aware desktop interface
- **pytest** for automated tests
- **setuptools / pyproject.toml** for standard Python packaging

The first version uses transparent rule-based analysis so that every result is explainable. The planned next version will add an OpenAI-powered mode to create richer summaries and follow-up questions while preserving deterministic checks.

## Setup and usage

```powershell
git clone https://github.com/<your-username>/freelance-brief-analyzer.git
cd freelance-brief-analyzer
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pip install -e .
python -m pip install -r requirements-dev.txt
```

Run interactively:

```powershell
python -m brief_analyzer
```

Or pass the values directly:

```powershell
python -m brief_analyzer --client "Acme" --brief "Create a dashboard for sales data." --output output/acme-analysis.json
```

## Testing

```powershell
python -m pytest
```

The test suite covers technology detection, validation, summary truncation, AI-specific discovery questions, and JSON output from the CLI.

## Project structure

```text
src/brief_analyzer/
  analyzer.py      Rule-based brief analysis logic
  cli.py           Command-line interface and JSON export
  gui.py           System-theme-aware desktop interface
tests/             Automated tests
pyproject.toml     Package metadata and CLI configuration
```

## Roadmap

- Add configurable analysis rules
- Expose the application through a FastAPI REST API
- Store analyses in PostgreSQL
- Add an OpenAI-powered analysis mode
- Dockerize and deploy the service

## License

MIT

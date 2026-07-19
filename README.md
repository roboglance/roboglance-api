# Backend API of RoboGlance

[![CI](https://github.com/roboglance/roboglance-api/actions/workflows/ci.yaml/badge.svg)](https://github.com/roboglance/roboglance-api/actions/workflows/ci.yaml)

RoboGlance is a smartwatch app with complications that help you stay informed about your FTC/FRC events.

The backend processes live match data to keep the client smartwatch app up-to-date.

## Development

These instructions are for developing the RoboGlance API in VS Code.

1. install prerequisites
   - [VS Code](https://code.visualstudio.com/Download)
   - [uv](https://docs.astral.sh/uv/getting-started/installation/)
1. clone the git repository
1. open the git repository in VS Code
1. configure Git to rebase by default when pulling in this repository
   ```sh
   git config pull.rebase true
   ```
1. install workspace recommended VS Code extensions
1. setup virtual environment with uv
   ```sh
   uv sync
   ```
1. run the development server
   - using the "Python Debugger: RoboGlance API" launch configuration in VS Code
   - using the terminal
     ```sh
     uv run fastapi dev
     ```
1. open http://localhost:8000/docs to test endpoints
1. format code with Ruff
   - using the "Format Document" command in VS Code
   - using the terminal
     ```sh
     uv run ruff format
     ```
1. lint code with Ruff
   - using the Ruff VS Code extension
   - using the terminal
     ```sh
     uv run ruff check
     ```

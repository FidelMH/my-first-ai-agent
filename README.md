# Mon Premier Agent

## Description
A Python project demonstrating the implementation of a basic AI agent integrated with Discord. The agent interacts with users through a Discord bot interface.

## Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/mon_premier_agent.git

# Navigate to project directory
cd mon_premier_agent

# Install dependencies

# Copy and configure environment variables
cp .env-renameme .env

# Edit .env file and set your Discord bot token
# Replace YOUR_BOT_TOKEN_HERE with your actual Discord bot token
# On Windows use: notepad .env
# On Linux/Mac use: nano .env

```

## Usage
```python
python main.py
```

## Features
- Basic AI agent implementation
- Discord bot integration for user interaction
- Real-time communication with the agent through Discord
- [Add more features]

## Requirements
- Python >=3.10 and <3.13
- discord.py
- crewai
## Dependencies
1. Install required packages:
```bash
pip install -r requirements.txt
```
# Environment Variables

The following environment variables are required and must be set in the `.env` file (rename `.env-renameme` to `.env`):

- `DISCORD_TOKEN` - Your Discord bot token obtained from the Discord Developer Portal
- `OLLAMA_MODEL` - The name of the Ollama model you want to use (e.g. "llama2", "codellama", etc.)
- `LLM_API` - The API endpoint URL for your Ollama instance (e.g. "http://localhost:11434/api/generate")

Refer to the `.env-renameme` template file for the required format. Environment variables must be set before running the application.

Note: It's recommended to use a virtual environment before installing dependencies.


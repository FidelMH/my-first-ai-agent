# AI Agents Project

## Project Status Update - 2025-06-13

This project was initially started to learn about AI agents creation using CrewAI. However, due to various challenges and complexities encountered with CrewAI, I've decided to pivot to a simpler, more fundamental approach.

### Why the Change?
- CrewAI, while powerful, introduced more complexity than necessary for learning
- Debugging and understanding the system became increasingly difficult
- The abstraction layer added unnecessary complexity

### New Direction
I'll be rebuilding this project using more low-level tools:
- Direct integration with LLMs (OpenAI, local models via LiteLLM)
- Custom agent architecture
- Simpler, more controllable workflows
- Better understanding of the fundamentals

This change will allow for:
- Better learning experience
- More control over the system
- Easier debugging
- Clearer understanding of AI agent principles


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
- `OLLAMA_MISTRAL` - The model name used by the Mistral agent
- `OLLAMA_QWEN3` - The model name used by the Qwen3 agent
- `OLLAMA_DEEPSEEK_R1` - The model name used by the DeepSeek R1 agent
- `LLM_API` - The API endpoint URL for your Ollama instance (e.g. "http://localhost:11434")

Refer to the `.env-renameme` template file for the required format. Environment variables must be set before running the application.

Note: It's recommended to use a virtual environment before installing dependencies.


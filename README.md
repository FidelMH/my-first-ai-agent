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
pip install -r requirements.txt

# Copy and configure environment variables
cp .env-renameme .env

# Edit .env file and set your Discord bot token
# Replace YOUR_BOT_TOKEN_HERE with your actual Discord bot token
# On Windows use: notepad .env
# On Linux/Mac use: nano .env

```

## Setup
Configure the following environment variables in the `.env` file:

- `DISCORD_TOKEN`: your Discord bot token.
- `OLLAMA_MODEL`: the Ollama model to use.
- `LLM_API`: base URL of your LLM API, e.g. `http://localhost:11434`.


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
- python-dotenv
- discord.py
- crewai

## Testing
Running the test suite requires the development packages listed in
`requirements-dev.txt`, such as `pytest-asyncio`.
Install them with:

```bash
pip install -r requirements-dev.txt
```

Then run the tests using:

```bash
pytest
```




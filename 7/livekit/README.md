# LiveKit Voice Agent - Greva

A voice-enabled AI agent built with LiveKit that uses OpenAI's models for speech-to-text, language processing, and text-to-speech capabilities.

## Prerequisites

⚠️ **Important:** This project currently requires **Python 3.13** due to dependency compatibility issues. Other Python versions may not work correctly.

### Required Software
- Python 3.13 (required)
- pip (Python package manager)
- A LiveKit account (for production deployment)
- OpenAI API key (for STT, LLM, and TTS services)

## Installation

### 1. Verify Python Version

```bash
python3.13 --version
```

If you don't have Python 3.13, install it:
- **macOS (Homebrew):** `brew install python@3.13`
- **Linux:** Download from [python.org](https://www.python.org/downloads/)
- **Windows:** Download from [python.org](https://www.python.org/downloads/)

### 2. Create Virtual Environment

```bash
python3.13 -m venv venv
```

### 3. Activate Virtual Environment

**macOS/Linux:**
```bash
source venv/bin/activate
```

**Windows:**
```powershell
venv\Scripts\activate
```

### 4. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

This will install all required packages including:
- `livekit-agents` - Core LiveKit agent framework
- `livekit-plugins-openai` - OpenAI integration
- `livekit-plugins-silero` - Voice Activity Detection
- `python-dotenv` - Environment variable management
- And many other dependencies

## Configuration

### Environment Variables

Create a `.env` file in the project root with your API keys:

```env
OPENAI_API_KEY=your_openai_api_key_here
LIVEKIT_URL=your_livekit_url_here
LIVEKIT_API_KEY=your_livekit_api_key_here
LIVEKIT_API_SECRET=your_livekit_api_secret_here
```

**Note:** For console mode testing, you only need the `OPENAI_API_KEY`. LiveKit credentials are required for production deployment.

## Running the Agent

### Console Mode (Testing)

Console mode allows you to test the agent locally without connecting to a LiveKit server:

```bash
python agent.py console
```

In console mode:
- The agent will start and initialize the voice session
- You can speak to test the voice recognition
- Audio will be processed through your microphone and speakers
- Press `Ctrl+C` to stop the agent

### Production Mode (LiveKit Server)

To run the agent connected to a LiveKit server:

```bash
python agent.py
```

This requires valid LiveKit credentials in your `.env` file.

## Agent Features

### Current Configuration

The agent is configured with:

- **Name:** Greva
- **Personality:** Polite and concise voice assistant
- **Voice Activity Detection (VAD):** Silero VAD
- **Speech-to-Text (STT):** OpenAI GPT-4o Transcribe
- **Language Model (LLM):** OpenAI GPT-4o-mini
- **Text-to-Speech (TTS):** OpenAI GPT-4o-mini-tts with "alloy" voice
- **Audio Subscription:** Audio-only mode

### Capabilities

- Real-time voice conversation
- Natural language understanding
- Multilingual support (via OpenAI transcription)
- Low-latency responses
- Warm greeting on connection

## Project Structure

```
livekit/
├── agent.py           # Main agent application
├── requirements.txt   # Python dependencies
├── venv/             # Virtual environment (created after setup)
├── .env              # Environment variables (create this)
└── README.md         # This file
```

## Troubleshooting

### "pip: command not found" or "python: command not found"

Make sure you've activated the virtual environment:
```bash
source venv/bin/activate  # macOS/Linux
```

### "ModuleNotFoundError"

Install dependencies:
```bash
python -m pip install -r requirements.txt
```

### Python Version Issues

This project requires Python 3.13. Verify your version:
```bash
python --version
```

If it shows a different version, explicitly use Python 3.13:
```bash
python3.13 -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
```

### Virtual Environment Issues

If the virtual environment is corrupted, recreate it:
```bash
rm -rf venv
python3.13 -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
```

## Customization

### Changing the Agent's Personality

Edit the `instructions` parameter in `agent.py`:

```python
agent = Agent(
    instructions="Your custom instructions here",
)
```

### Changing the Voice

Modify the TTS configuration in `agent.py`. Available voices: alloy, echo, fable, onyx, nova, shimmer

```python
tts=openai.TTS(model="gpt-4o-mini-tts", voice="nova"),
```

### Changing the Language Model

Update the LLM configuration:

```python
llm=openai.LLM(model="gpt-4o"),  # or "gpt-4o-mini"
```

## Dependencies

Key packages:
- `livekit-agents==1.3.6` - Agent framework
- `livekit-plugins-openai==1.3.6` - OpenAI integration
- `livekit-plugins-silero==1.3.6` - VAD
- `openai==2.11.0` - OpenAI API client
- `python-dotenv==1.2.1` - Environment management

See `requirements.txt` for the complete list.

## Development

### Adding New Features

1. Modify `agent.py` to add new functionality
2. Test in console mode: `python agent.py console`
3. Deploy to production when ready

### Updating Dependencies

```bash
python -m pip install --upgrade -r requirements.txt
```

## Support & Resources

- [LiveKit Documentation](https://docs.livekit.io/)
- [LiveKit Agents Documentation](https://docs.livekit.io/agents/)
- [OpenAI API Documentation](https://platform.openai.com/docs/)

## License

This project uses the following technologies:
- LiveKit (Apache 2.0 License)
- OpenAI API (Commercial)

## Notes

- **Python 3.13 Requirement:** Due to compatibility issues with certain dependencies (particularly binary packages like `onnxruntime`, `av`, and `numpy`), this project currently requires Python 3.13.
- For production use, ensure you have proper API rate limits and billing configured for OpenAI services.
- The agent uses OpenAI's transcription and TTS services, which incur costs based on usage.

## Quick Start Summary

```bash
# 1. Ensure Python 3.13 is installed
python3.13 --version

# 2. Create and activate virtual environment
python3.13 -m venv venv
source venv/bin/activate  # macOS/Linux

# 3. Install dependencies
python -m pip install -r requirements.txt

# 4. Create .env file with your OPENAI_API_KEY

# 5. Run in console mode
python agent.py console
```

---

**Made with LiveKit and OpenAI** 🎙️


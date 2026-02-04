# AI Agent with Claude

A powerful AI agent built with Python and the Anthropic Claude API. This agent can autonomously use tools, reason about tasks, execute multi-step workflows, and analyze images using Claude's vision capabilities.

## Features

- **Agentic Loop**: The agent can think, use tools, and continue reasoning autonomously
- **Image Recognition**: Analyze images, detect objects, extract text (OCR), and answer questions about visual content
- **People Recognition**: Detect and analyze people in images - count, activities, expressions, group dynamics
- **Face Identification**: Identify specific individuals in your personal photos (with consent)
- **Tool Use**: Built-in tools (weather, calculator, image analysis, people detection, face ID) that can be extended
- **Multi-turn Conversations**: Handles complex tasks requiring multiple steps
- **Interactive Mode**: Chat with the agent in real-time

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up your API key:
```bash
cp .env.example .env
# Edit .env and add your Anthropic API key
```

3. Get an API key from [Anthropic Console](https://console.anthropic.com/)

## Usage

### Running the Main Agent

Run the agent:
```bash
python agent.py
```

The script will run a few examples, then enter interactive mode where you can chat with the agent.

In interactive mode, you can analyze images using:
```
image:/path/to/image.jpg What objects are in this image?
```

### Image Recognition Examples

For dedicated image recognition capabilities, run:
```bash
python image_recognition_example.py
```

This provides interactive image analysis where you can:
- Describe images in detail
- Detect and identify objects
- Extract text (OCR)
- Answer specific questions about images
- Analyze scenes and settings

### People Recognition

For specialized people detection and analysis, run:
```bash
python people_recognition.py
```

This provides dedicated people analysis including:
- Count people in images
- Describe activities and actions
- Analyze facial expressions and emotions
- Describe clothing and appearance
- Understand group dynamics
- Analyze body language and poses

**See [PEOPLE_RECOGNITION_GUIDE.md](PEOPLE_RECOGNITION_GUIDE.md) for detailed documentation on people recognition capabilities.**

### Face Identification (Personal Photos)

For identifying specific individuals in your personal photos (with consent):
```bash
python face_identification.py
```

This provides personal photo organization:
- Build a reference database of family and friends (with consent)
- Identify people in new photos by name
- Organize personal photo collections
- Get confidence levels for matches

**IMPORTANT:** Only use on your own personal photos with explicit consent from everyone. See [FACE_IDENTIFICATION_GUIDE.md](FACE_IDENTIFICATION_GUIDE.md) for privacy guidelines and legal requirements.

## How It Works

1. **User Input**: You provide a task, question, or image
2. **Agent Reasoning**: Claude processes the request and decides if it needs tools
3. **Tool Execution**: If tools are needed, they're executed and results returned
4. **Image Analysis**: For images, Claude uses its vision capabilities to analyze visual content
5. **Loop Continues**: The agent reasons about tool results and may use more tools
6. **Final Response**: Once complete, the agent provides a final answer

## Image Recognition Capabilities

The agent can:
- **General Description**: Describe what's in an image
- **Object Detection**: Identify and list objects in images
- **Text Extraction (OCR)**: Read and extract text from images
- **Scene Analysis**: Describe settings, atmosphere, and context
- **Specific Questions**: Answer targeted questions about image content
- **Multi-modal Reasoning**: Combine image analysis with other tools

## People Recognition Capabilities

The agent can detect and analyze people with:
- **People Counting**: Accurately count number of people in images
- **Activity Recognition**: Describe what people are doing
- **Facial Analysis**: Detect expressions, emotions, and facial features
- **Appearance Description**: Describe clothing, style, and physical attributes
- **Group Dynamics**: Analyze interactions and relationships between people
- **Body Language**: Understand poses, gestures, and non-verbal communication

**Privacy & Ethics**: The agent describes people but does not identify specific individuals by default. See [PEOPLE_RECOGNITION_GUIDE.md](PEOPLE_RECOGNITION_GUIDE.md) for guidelines.

## Face Identification Capabilities (Personal Use)

For personal photo organization, the agent can identify specific individuals:
- **Database Management**: Store reference images of family/friends (with consent)
- **Person Identification**: Match faces in new photos against your database
- **Confidence Scoring**: Get high/medium/low confidence for matches
- **Batch Processing**: Organize entire photo collections
- **Privacy-First**: All data stored locally, consent required

**CRITICAL:** Face identification requires explicit consent and is only for personal photos. Never use for surveillance, tracking, or on people without their permission. See [FACE_IDENTIFICATION_GUIDE.md](FACE_IDENTIFICATION_GUIDE.md) for complete privacy and legal guidelines.

### Supported Image Formats
- JPEG (.jpg, .jpeg)
- PNG (.png)
- GIF (.gif)
- WebP (.webp)
- HEIC (.heic, .heif) - Apple's High Efficiency Image Format (automatically converted)

## Extending the Agent

### Adding New Tools

Add tool definitions to the `TOOLS` list in `agent.py`:

```python
{
    "name": "your_tool_name",
    "description": "What your tool does",
    "input_schema": {
        "type": "object",
        "properties": {
            "param_name": {
                "type": "string",
                "description": "Parameter description"
            }
        },
        "required": ["param_name"]
    }
}
```

Then implement the tool in the `execute_tool()` function.

### Example Tools to Add

- Web search
- File system operations
- Database queries
- API calls
- Code execution
- Image generation
- Video analysis
- Audio transcription
- Document processing

## Architecture

```
User Input
    ↓
[Claude API] ←→ [Tool Execution]
    ↓              ↑
Agent Loop ────────┘
    ↓
Final Response
```

## Best Practices

- Keep tool descriptions clear and specific
- Add error handling for tool execution
- Set reasonable `max_turns` to prevent infinite loops
- Log tool usage for debugging
- Validate tool inputs before execution

## License

MIT

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

## Quick Start

### Using the Launcher (Recommended)

The easiest way to get started:

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure your provider (see Provider Configuration below)
cp .env.example .env
# Edit .env with your settings

# 3. Run the launcher
./run.sh
```

The launcher provides an interactive menu to:
- Run any of the available scripts
- Test your setup
- Authenticate with Vertex AI (if using Google Cloud)

### Manual Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up your API configuration:
```bash
cp .env.example .env
# Edit .env and configure your provider (see below)
```

3. Choose your provider and follow the setup steps below

### Provider Configuration

This project supports two Claude API providers:

**Option 1: Anthropic API (Default)**

1. Get an API key from [Anthropic Console](https://console.anthropic.com/)
2. Add to your `.env` file:
```bash
CLAUDE_PROVIDER=anthropic
ANTHROPIC_API_KEY=sk-ant-...
```

**Option 2: Google Vertex AI**

1. Set up a Google Cloud project with Vertex AI enabled
2. Install additional dependencies:
```bash
pip install 'anthropic[vertex]' google-cloud-aiplatform
```

3. **Authenticate with Google Cloud** (Use the launcher for guided setup):

   **Using the launcher (recommended):**
   ```bash
   ./run.sh
   # Select option 6: Authenticate with Vertex AI
   ```

   The launcher will:
   - Check your authentication status
   - Verify Vertex AI API is enabled
   - Display quota information
   - Guide you through authentication with quota project setup

   **Manual authentication:**
   ```bash
   # Basic authentication
   gcloud auth application-default login

   # With quota project (recommended)
   gcloud auth application-default login --quota-project-id=your-project-id
   ```

4. Configure your `.env` file:
```bash
CLAUDE_PROVIDER=vertex
VERTEX_PROJECT_ID=your-gcp-project-id
VERTEX_REGION=us-east5  # or your preferred region
```

**About Quota Projects:**
The quota project determines which GCP project is billed for API usage and which project's quotas are consumed. This is typically the same as your Vertex AI project but can be different for centralized billing scenarios.

For more details on Vertex AI setup, see [Anthropic's Vertex AI documentation](https://docs.anthropic.com/en/api/claude-on-vertex-ai).

## Usage

### Using the Launcher Script (Recommended)

The easiest way to run any script:

```bash
./run.sh
```

The launcher provides an interactive menu with the following options:

**1. Image Recognition** - Analyze any image
- Interactive mode for image analysis
- Ask questions about images
- OCR, object detection, scene analysis

**2. People Recognition** - Detect and analyze people
- Count people in images
- Analyze facial expressions and emotions
- Describe activities and group dynamics

**3. Face Identification** - Identify known people
- Build a personal database (with consent)
- Identify family and friends in photos
- Organize photo collections

**4. AI Agent** - Full capabilities
- Autonomous tool use
- Multi-turn reasoning
- Interactive chat mode
- Image analysis with other tools

**5. Test Interface** - Verify setup
- Check all dependencies
- Verify authentication
- Test module imports

**6. Authenticate with Vertex AI** - GCP authentication
- Check authentication status
- View API quotas and limits
- Configure quota project
- Enable Vertex AI API

### Running Scripts Directly

You can also run scripts directly:

```bash
# Activate virtual environment
source venv/bin/activate

# Run the AI agent
python agent.py

# Or any other script
python image_recognition_example.py
```

### AI Agent Interactive Mode

The agent will run a few examples, then enter interactive mode where you can chat with the agent.

In interactive mode, you can analyze images using:
```
image:/path/to/image.jpg What objects are in this image?
```

### Image Recognition Examples

Run via launcher (`./run.sh` → option 1) or directly:
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

Run via launcher (`./run.sh` → option 2) or directly:
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

Run via launcher (`./run.sh` → option 3) or directly:
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

### High-Level Flow

```
User Input
    ↓
[Claude API] ←→ [Tool Execution]
    ↓              ↑
Agent Loop ────────┘
    ↓
Final Response
```

### Provider Architecture

The project uses a factory pattern for Claude client initialization:

```
Application Scripts
    ↓
[claude_client.py] ← Factory Pattern
    ├─→ Anthropic API Client
    └─→ Vertex AI Client
        ↓
    Shared Utilities
    - load_and_encode_image()
    - get_image_media_type()
```

**Benefits:**
- Single source of truth for client initialization
- Reduced code duplication (~180 lines)
- Easy provider switching via environment variable
- Consistent error handling across all scripts
- Centralized image processing utilities

**Files:**
- `claude_client.py` - Factory and utilities (NEW)
- `agent.py` - Main agentic loop
- `image_recognition_example.py` - Image analysis
- `people_recognition.py` - People detection
- `face_identification.py` - Face ID system
- `run.sh` - Interactive launcher

## Troubleshooting

### Vertex AI Issues

**Authentication Errors:**
- Run `./run.sh` and select option 6 to check authentication status
- Ensure you've run: `gcloud auth application-default login --quota-project-id=your-project-id`
- Verify your account has access to the project

**API Not Enabled:**
- The launcher (option 6) will detect this and offer to enable it
- Or manually enable: `gcloud services enable aiplatform.googleapis.com`

**Quota Errors:**
- Use the launcher (option 6) to view your quotas
- Visit the [GCP Console Quotas page](https://console.cloud.google.com/apis/api/aiplatform.googleapis.com/quotas)
- Request quota increases if needed

**Region Issues:**
- Verify `VERTEX_REGION` in `.env` matches an available region
- Common regions: `us-east5`, `us-central1`, `europe-west1`
- See [Vertex AI locations](https://cloud.google.com/vertex-ai/docs/general/locations) for full list

**Project Mismatch:**
- The launcher will detect if your gcloud project doesn't match `.env`
- Run: `gcloud config set project your-project-id`

### General Issues

**Module Import Errors:**
- Ensure virtual environment is activated: `source venv/bin/activate`
- Reinstall dependencies: `pip install -r requirements.txt`
- For Vertex AI: `pip install 'anthropic[vertex]' google-cloud-aiplatform`

**Image Format Errors:**
- Supported formats: JPG, PNG, GIF, WebP, HEIC
- HEIC files are automatically converted to JPEG
- Ensure image files exist at the specified path

## Best Practices

- Keep tool descriptions clear and specific
- Add error handling for tool execution
- Set reasonable `max_turns` to prevent infinite loops
- Log tool usage for debugging
- Validate tool inputs before execution
- Use the launcher script for easier management
- Regularly check quotas when using Vertex AI
- Keep your `.env` file secure and never commit it to version control

## License

MIT

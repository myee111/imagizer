# Quick Start Guide

## Setup (5 minutes)

### 1. Install Dependencies
```bash
pip install -r requirements.txt

# For Vertex AI (optional):
pip install 'anthropic[vertex]' google-cloud-aiplatform
```

### 2. Set Up Provider

Choose between Anthropic API or Google Vertex AI:

**Option A: Anthropic API (Default)**
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your API key
# Get your key from: https://console.anthropic.com/
```

Your `.env` file should look like:
```
CLAUDE_PROVIDER=anthropic
ANTHROPIC_API_KEY=sk-ant-api03-...
```

**Option B: Google Vertex AI**
```bash
cp .env.example .env

# Edit .env for Vertex AI:
# CLAUDE_PROVIDER=vertex
# VERTEX_PROJECT_ID=your-project-id
# VERTEX_REGION=us-east5
```

Then authenticate:
```bash
./run.sh
# Select option 6: Authenticate with Vertex AI
```

### 3. Test the Agent
```bash
# Using the launcher (recommended):
./run.sh

# Or run directly:
python agent.py
```

## What Can This Agent Do?

### 1. General AI Agent Tasks
- Answer questions
- Perform calculations
- Use tools autonomously
- Multi-step reasoning

### 2. Image Recognition
- Describe images
- Identify objects
- Extract text (OCR)
- Analyze scenes

### 3. People Recognition ⭐
- Count people in images
- Describe what they're doing
- Analyze facial expressions
- Understand group dynamics
- Describe clothing and appearance

### 4. Face Identification ⭐ NEW
- Identify specific individuals by name (with consent)
- Organize personal photo collections
- Build database of family and friends
- Get confidence scores for matches
- **For personal use only**

## Running the Agent

### Option 0: Launcher Script (Easiest)
```bash
./run.sh
```

Interactive menu with all options:
1. Image Recognition
2. People Recognition
3. Face Identification
4. AI Agent
5. Test Interface
6. Authenticate with Vertex AI

### Option 1: Main Agent
```bash
python agent.py
```

The agent runs examples then enters interactive mode.

**Analyze images:**
```
You: image:./photo.jpg What do you see?
```

**Analyze people:**
```
You: image:./group.jpg How many people are here and what are they doing?
```

**Ask questions:**
```
You: What is 157 * 234?
You: What's the weather in Tokyo?
```

### Option 2: People Recognition Tool
```bash
python people_recognition.py
```

Dedicated tool for analyzing people with a menu:
1. Count people
2. Describe activities
3. Detailed analysis
4. Facial expressions
5. Group dynamics
6. Custom questions

### Option 3: Image Recognition Tool
```bash
python image_recognition_example.py
```

Dedicated tool for general image analysis.

### Option 4: Face Identification Tool (Personal Photos)
```bash
python face_identification.py
```

Identify specific people in your personal photos:
1. Build database with reference images (requires consent)
2. Identify people in new photos
3. Organize photo collections

**Important:** Only for personal use with explicit consent. See `FACE_IDENTIFICATION_GUIDE.md`.

## Example Use Cases

### Count People at an Event
```python
from agent import run_agent

result = run_agent("How many people are in ./event_photo.jpg?")
print(result)
```

### Analyze Meeting Dynamics
```python
result = run_agent("Analyze the group dynamics in ./meeting.jpg")
print(result)
```

### Describe Activities
```python
result = run_agent("What are people doing in ./park.jpg?")
print(result)
```

### Detect Emotions
```python
result = run_agent("What emotions do you see in ./portrait.jpg?")
print(result)
```

### Multi-Modal Reasoning
```python
# Agent autonomously combines multiple tools
result = run_agent(
    "Count the people in ./photo.jpg and multiply by 12"
)
print(result)
```

## Understanding the Agent

The agent is **autonomous** - it decides which tools to use:

1. **You ask a question** about people in an image
2. **Agent thinks** about what it needs to do
3. **Agent chooses** the right tool (analyze_people)
4. **Tool executes** and returns results
5. **Agent responds** with the answer

You don't need to specify which tool to use!

## File Guide

| File | Purpose |
|------|---------|
| `run.sh` | **Interactive launcher** - Easy menu for all scripts |
| `claude_client.py` | **Provider factory** - Anthropic & Vertex AI support |
| `agent.py` | Main agentic system with all tools |
| `people_recognition.py` | Dedicated people analysis tool |
| `image_recognition_example.py` | General image analysis tool |
| `face_identification.py` | Face identification for personal photos |
| `test_interface.py` | Verify setup and dependencies |
| `demo.py` | Quick demonstration |
| `example_people_recognition.py` | Code examples for people recognition |
| `example_face_identification.py` | Code examples for face identification |
| `QUICKSTART.md` | This file - quick start guide |
| `PEOPLE_RECOGNITION_GUIDE.md` | Complete people recognition documentation |
| `FACE_IDENTIFICATION_GUIDE.md` | Complete face identification documentation |
| `README.md` | Full project documentation |

## Privacy & Ethics

**Important:** This agent can describe people but does not identify specific individuals.

✅ **DO:**
- Use for counting people
- Describe activities and behaviors
- Analyze group dynamics
- Describe appearances objectively

❌ **DON'T:**
- Use for unauthorized surveillance
- Attempt to identify private individuals
- Use for discriminatory purposes
- Violate privacy rights

See `PEOPLE_RECOGNITION_GUIDE.md` for full ethical guidelines.

## Supported Image Formats

- JPEG (.jpg, .jpeg)
- PNG (.png)
- GIF (.gif)
- WebP (.webp)
- HEIC (.heic, .heif) - iPhone/iPad photos automatically converted

## Tips for Best Results

1. **Use clear, well-lit images** - Better lighting = better analysis
2. **Ask specific questions** - "How many people?" vs "Analyze this"
3. **Provide context** - Helps the agent understand what you need
4. **High resolution** - More detail = more accurate results
5. **Direct questions** - The agent works best with clear requests

## Troubleshooting

### Error: "ANTHROPIC_API_KEY not found"
- Make sure you created the `.env` file
- Check that your API key is correct
- Verify `CLAUDE_PROVIDER=anthropic` in `.env`
- Don't commit `.env` to git (it's in `.gitignore`)

### Error: "VERTEX_PROJECT_ID not found"
- Set `CLAUDE_PROVIDER=vertex` in `.env`
- Add `VERTEX_PROJECT_ID` and `VERTEX_REGION` to `.env`
- Run `./run.sh` → option 6 to authenticate

### Authentication Issues (Vertex AI)
- Run `./run.sh` → option 6 to check status
- Ensure Vertex AI API is enabled
- Check quota limits in GCP Console
- Verify project permissions

### Error: "Image file not found"
- Use absolute paths or paths relative to where you run the script
- Check that the file exists: `ls -la ./your_image.jpg`

### People not detected
- Ensure people are clearly visible in the image
- Check lighting and image quality
- Try asking: "Are there any people in this image?"

### Provider Issues
- Run `./run.sh` → option 5 to test your setup
- Check which provider is active: `grep CLAUDE_PROVIDER .env`
- See README.md for full provider configuration details

## Next Steps

1. **Try the examples** - Run through the demo scripts
2. **Test with your images** - Use your own photos
3. **Extend the agent** - Add new tools (see README.md)
4. **Read the guides** - Check out PEOPLE_RECOGNITION_GUIDE.md

## Getting Help

- Review `README.md` for detailed documentation
- Check `PEOPLE_RECOGNITION_GUIDE.md` for people recognition details
- Look at example scripts for code patterns
- Review Claude's documentation at https://docs.anthropic.com/

## Have Fun! 🚀

Your agent is ready to analyze images and recognize people. Start with simple examples and experiment!

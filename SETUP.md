# Complete Setup Guide

## ✅ Testing Completed Successfully!

All systems tested and working:
- ✅ Face identification module
- ✅ People recognition module
- ✅ Image analysis module
- ✅ Main AI agent with all tools integrated
- ✅ Dependencies installed

## Quick Setup (5 Minutes)

### Step 1: Install Dependencies

```bash
# Navigate to the project directory
cd /Users/myee/agents

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies (already done!)
pip install -r requirements.txt
```

### Step 2: Configure API Key

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your Anthropic API key
nano .env  # or use your preferred editor
```

Your `.env` file should look like:
```
ANTHROPIC_API_KEY=sk-ant-api03-xxxxx
```

Get your API key from: https://console.anthropic.com/

### Step 3: Test the System

```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Run the test suite
python test_interface.py
```

You should see:
```
✅ ALL TESTS PASSED!
✅ Face identification tool is registered!
```

## Using the System

### Option 1: Face Identification (Identify Specific People)

```bash
# Activate virtual environment
source venv/bin/activate

# Run the face identification tool
python face_identification.py
```

**First time setup:**
1. Choose option 1: "Add a person to database"
2. Add yourself or a family member (with consent)
3. Provide a clear face photo
4. Test identification with option 2

### Option 2: AI Agent (Autonomous)

```bash
# Activate virtual environment
source venv/bin/activate

# Run the main agent
python agent.py
```

In interactive mode:
```
You: How many people are in ./photo.jpg?
You: Who is in ./family_photo.jpg?  # Uses face database
You: What are people doing in ./party.jpg?
You: image:./photo.jpg Describe what you see
```

The agent automatically chooses the right tool!

### Option 3: People Recognition (General Analysis)

```bash
# Activate virtual environment
source venv/bin/activate

# Run people recognition
python people_recognition.py
```

Analyze people without identifying them:
- Count people
- Describe activities
- Facial expressions
- Group dynamics

### Option 4: View Demo

```bash
# See what the interface looks like (no API key needed)
source venv/bin/activate
python demo_interface.py
```

## Project Structure

```
/Users/myee/agents/
├── venv/                              # Virtual environment (created)
├── agent.py                           # Main AI agent ⭐
├── face_identification.py             # Face ID tool ⭐
├── people_recognition.py              # People analysis ⭐
├── image_recognition_example.py       # Image analysis
│
├── demo_interface.py                  # Interactive demo
├── test_interface.py                  # Test suite
├── example_face_identification.py     # Code examples
├── example_people_recognition.py      # Code examples
│
├── QUICKSTART.md                      # 5-minute guide
├── FACE_IDENTIFICATION_GUIDE.md       # Complete face ID docs
├── PEOPLE_RECOGNITION_GUIDE.md        # Complete people docs
├── README.md                          # Project overview
├── SETUP.md                           # This file
│
├── requirements.txt                   # Python dependencies
├── .env.example                       # API key template
└── .gitignore                         # Git ignore rules
```

## Common Commands

### Every Session

Always activate the virtual environment first:
```bash
cd /Users/myee/agents
source venv/bin/activate
```

### Face Identification Workflow

```bash
# 1. Build database (first time)
python face_identification.py
# Choose 1, add people with consent

# 2. View database
python face_identification.py
# Choose 3

# 3. Identify in photos
python face_identification.py
# Choose 2, enter photo path

# 4. Or use with agent
python agent.py
# Ask: "Who is in ./photo.jpg?"
```

### People Recognition Workflow

```bash
# Analyze without identifying
python people_recognition.py

# Or ask the agent
python agent.py
# Ask: "How many people are in ./photo.jpg?"
# Ask: "What are people doing in ./photo.jpg?"
```

## Tools Available

Your agent has 5 autonomous tools:

1. **get_weather** - Get weather (mock data)
2. **calculate** - Perform math calculations
3. **analyze_image** - General image analysis, OCR, object detection
4. **analyze_people** - Count people, activities, expressions (no ID)
5. **identify_person** ⭐ NEW - Identify specific individuals from database

The agent automatically chooses which tool to use based on your question!

## Privacy & Ethics

### Face Identification Requirements

**MUST HAVE:**
- ✅ Explicit consent from everyone in database
- ✅ Clear explanation of data usage
- ✅ Secure storage of database
- ✅ Ability to delete on request
- ✅ Personal use only

**FORBIDDEN:**
- ❌ Adding people without consent
- ❌ Surveillance or unauthorized tracking
- ❌ Sharing database without permission
- ❌ Commercial deployment
- ❌ Discriminatory use

See `FACE_IDENTIFICATION_GUIDE.md` for complete guidelines.

## Troubleshooting

### "ModuleNotFoundError"
- Make sure virtual environment is activated: `source venv/bin/activate`
- Reinstall dependencies: `pip install -r requirements.txt`

### "ANTHROPIC_API_KEY not found"
- Check `.env` file exists: `ls -la .env`
- Verify API key is set correctly
- No quotes around the key value

### "Image not found"
- Use absolute paths: `/full/path/to/image.jpg`
- Or relative from where you run the script: `./photos/image.jpg`

### "No people in database"
- Run `python face_identification.py` first
- Add at least one person (option 1)
- Verify with option 3 (view database)

### Virtual environment issues
```bash
# Deactivate if active
deactivate

# Remove and recreate
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Next Steps

1. **Get API Key** (if not done)
   - Visit: https://console.anthropic.com/
   - Create account / sign in
   - Generate API key
   - Add to `.env` file

2. **Test Basic Features**
   ```bash
   source venv/bin/activate
   python agent.py
   ```
   Try: "What is 123 * 456?"

3. **Set Up Face Database** (with consent)
   ```bash
   python face_identification.py
   ```
   Add yourself first

4. **Test Identification**
   ```bash
   python agent.py
   ```
   Ask: "Who is in [photo path]?"

5. **Read Documentation**
   - `QUICKSTART.md` - Quick overview
   - `FACE_IDENTIFICATION_GUIDE.md` - Complete reference
   - `PEOPLE_RECOGNITION_GUIDE.md` - People analysis

## Success Checklist

- [ ] Virtual environment created and activated
- [ ] Dependencies installed (anthropic, python-dotenv)
- [ ] .env file created with API key
- [ ] Test suite passes (`python test_interface.py`)
- [ ] Demo runs successfully (`python demo_interface.py`)
- [ ] Main agent works (`python agent.py`)
- [ ] Face database created (with consent)
- [ ] Tested identification on a photo
- [ ] Read privacy guidelines

## Support

- **Technical Issues**: Check troubleshooting section above
- **Privacy Questions**: See `FACE_IDENTIFICATION_GUIDE.md`
- **Usage Examples**: Run `python example_face_identification.py`
- **API Documentation**: https://docs.anthropic.com/

## Quick Reference Card

```bash
# Activate environment (ALWAYS FIRST)
source venv/bin/activate

# Main tools
python agent.py                    # AI agent (all features)
python face_identification.py      # Face ID management
python people_recognition.py       # People analysis

# Testing & demos
python test_interface.py           # Verify system works
python demo_interface.py           # See interface demo
python example_face_identification.py  # View examples

# Deactivate when done
deactivate
```

---

**System Status: ✅ Ready to Use!**

All components tested and working. Just add your API key and start identifying people in your photos (with consent)!

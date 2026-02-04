# People Recognition Guide

## Overview

This agent can detect and analyze people in images using Claude's advanced vision capabilities. It can count people, describe their activities, analyze facial expressions, and understand group dynamics.

## Important Privacy & Ethics Notice

### What This Agent CAN Do
- ✅ Count the number of people in an image
- ✅ Describe what people are doing
- ✅ Analyze facial expressions and emotions
- ✅ Describe clothing, poses, and appearance
- ✅ Understand group dynamics and interactions
- ✅ Detect body language and gestures
- ✅ Provide demographic descriptions (age ranges, general appearance)
- ✅ Recognize widely-known public figures in appropriate contexts

### What This Agent CANNOT/SHOULD NOT Do
- ❌ Identify private individuals by name
- ❌ Be used for unauthorized surveillance
- ❌ Create facial recognition databases
- ❌ Track individuals across multiple images
- ❌ Be used to discriminate or make harmful decisions about people

### Responsible Use Guidelines
1. Always obtain appropriate consent before analyzing images of people
2. Respect privacy and use the tool ethically
3. Do not use for surveillance or unauthorized monitoring
4. Be aware of biases and limitations in AI analysis
5. Use objective, respectful language when describing people

## Capabilities

### 1. Count People
Count the number of people in an image and describe their positions.

**Usage:**
```python
run_agent("How many people are in the image at ./photo.jpg?")
```

The agent will autonomously use the `analyze_people` tool with `analysis_type="count"`.

### 2. Activity Recognition
Describe what people are doing in the image.

**Usage:**
```python
run_agent("What are the people doing in this image at ./scene.jpg?")
```

**Capabilities:**
- Detect actions and activities
- Identify interactions between people
- Describe movements and gestures
- Understand context of activities

### 3. Detailed Person Analysis
Get a detailed description of each person in the image.

**Usage:**
```python
run_agent("Give me a detailed analysis of each person in ./group.jpg")
```

**Provides:**
- Position in the image
- Activity/actions
- Clothing and style
- Body language and pose
- Notable characteristics

### 4. Facial Expression Analysis
Analyze faces and emotional expressions.

**Usage:**
```python
run_agent("What are the facial expressions of people in ./faces.jpg?")
```

**Detects:**
- Emotions and expressions
- Direction of gaze
- Approximate age ranges
- Distinctive features (glasses, facial hair, etc.)
- Overall demeanor

### 5. Group Dynamics
Understand relationships and interactions between people.

**Usage:**
```python
run_agent("Analyze the group dynamics in ./meeting.jpg")
```

**Analyzes:**
- Positioning and spatial relationships
- Apparent social relationships
- Social context (meeting, party, etc.)
- Overall mood and atmosphere
- Group behaviors

### 6. Custom Questions
Ask specific questions about people in images.

**Usage:**
```python
run_agent("Are the people in ./image.jpg wearing formal or casual clothing?")
```

## Code Examples

### Example 1: Using the Main Agent
```python
from agent import run_agent

# Count people
result = run_agent("How many people are in this image at ./crowd.jpg?")
print(result)

# Describe activities
result = run_agent("What are the people doing in ./park.jpg?")
print(result)

# Analyze expressions
result = run_agent("What emotions do you see in the faces in ./portrait.jpg?")
print(result)
```

### Example 2: Using the Dedicated People Recognition Script
```bash
python people_recognition.py
```

Then select from the menu:
1. Count people
2. Describe activities
3. Detailed person-by-person analysis
4. Clothing and attributes
5. Face detection and expressions
6. Group dynamics and interactions
7. Custom question

### Example 3: Interactive Mode with Images
```bash
python agent.py
```

In interactive mode:
```
You: image:./photo.jpg How many people are here and what are they doing?
```

## Technical Details

### Supported Image Formats
- JPEG (.jpg, .jpeg)
- PNG (.png)
- GIF (.gif)
- WebP (.webp)

### Image Requirements
- Clear visibility of people
- Adequate lighting
- Reasonable resolution
- People should be the main subjects or clearly visible

### Best Practices for Accuracy

1. **Image Quality**: Use clear, well-lit images
2. **Resolution**: Higher resolution provides better detail
3. **Composition**: Frame people clearly in the shot
4. **Context**: Provide context in your questions for better analysis
5. **Specific Questions**: Ask specific questions for more targeted results

## Analysis Types Reference

| Analysis Type | Use When You Want To... | Example Question |
|---------------|-------------------------|------------------|
| `count` | Count people and describe positions | "How many people are in this image?" |
| `activities` | Know what people are doing | "What activities are happening?" |
| `detailed` | Get full description of each person | "Describe each person in detail" |
| `faces` | Analyze facial expressions | "What emotions do the faces show?" |
| `group` | Understand group dynamics | "What's the group dynamic here?" |
| `custom` | Ask a specific question | "Are they wearing uniforms?" |

## Common Use Cases

### 1. Event Photography Analysis
- Count attendees
- Identify activity types
- Understand event atmosphere

### 2. Crowd Analysis
- Estimate crowd size
- Identify crowd density patterns
- Understand crowd behavior

### 3. Social Media Content
- Describe photo content
- Identify activities
- Understand social contexts

### 4. Security & Safety (Authorized Use)
- Monitor occupancy levels
- Detect unusual behaviors
- Ensure safety protocols

### 5. Accessibility
- Describe images for visually impaired users
- Provide detailed scene descriptions

### 6. Research & Analysis
- Study group dynamics
- Analyze social interactions
- Understand behavioral patterns

## Limitations

1. **Accuracy**: Analysis is based on visible information only
2. **Interpretation**: Some subjective interpretations may vary
3. **Privacy**: Cannot and should not identify specific individuals
4. **Context**: Limited to what's visible in the image
5. **Biases**: AI systems may have inherent biases

## Troubleshooting

### Issue: "No people detected"
- Ensure people are clearly visible
- Check image quality and lighting
- Verify people are not too small in the frame

### Issue: Inaccurate count
- People may be partially obscured
- Try asking for a "best estimate"
- Specify what counts as a person (full body vs. partial)

### Issue: Vague descriptions
- Ask more specific questions
- Use targeted analysis types
- Provide context about what you're looking for

## API Usage

The agent uses the Claude Sonnet 4.5 model with vision capabilities:
- Model: `claude-sonnet-4-5-20250929`
- Max tokens: 2048 per request
- Supports base64-encoded images

## Support & Questions

For issues or questions:
1. Check this guide first
2. Review example scripts
3. Test with the interactive demo
4. Review Claude's vision capabilities documentation

## Future Enhancements

Potential additions (submit feedback if interested):
- [ ] Pose estimation
- [ ] Action recognition tracking
- [ ] Multi-image comparison
- [ ] Video frame analysis
- [ ] Anonymization features
- [ ] Batch processing

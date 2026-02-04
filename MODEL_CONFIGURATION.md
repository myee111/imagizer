# Model Configuration Guide

## Overview

This application now supports multiple AI providers and models:
- **Anthropic API** - Direct Claude API
- **Vertex AI Claude** - Claude via Google Cloud
- **Vertex AI Gemini** - Google's Gemini models (requires enablement)

## Quick Start

Edit your `.env` file to set the provider and optionally the model:

```bash
# Choose your provider
CLAUDE_PROVIDER=vertex  # or "anthropic" or "gemini"

# Optional: Override the default model
# CLAUDE_MODEL=your-model-name
```

## Available Models

### Anthropic API Models

```bash
CLAUDE_PROVIDER=anthropic
ANTHROPIC_API_KEY=sk-ant-...

# Optional model overrides:
# CLAUDE_MODEL=claude-sonnet-4-5-20250929  # Default
# CLAUDE_MODEL=claude-opus-4-5-20251101
# CLAUDE_MODEL=claude-3-5-sonnet-20241022
```

### Vertex AI Claude Models

```bash
CLAUDE_PROVIDER=vertex
VERTEX_PROJECT_ID=your-project
VERTEX_REGION=us-east5

# Optional model overrides:
# CLAUDE_MODEL=claude-sonnet-4-5@20250929  # Default (@ not -)
# CLAUDE_MODEL=claude-opus-4-5@20251101
# CLAUDE_MODEL=claude-3-5-sonnet@20241022
```

**Note:** Vertex uses `@` instead of `-` in model versions.

### Vertex AI Gemini Models

```bash
CLAUDE_PROVIDER=gemini
VERTEX_PROJECT_ID=your-project
VERTEX_REGION=us-central1  # Gemini availability varies by region

# Optional model overrides:
# CLAUDE_MODEL=gemini-1.5-flash-002  # Default
# CLAUDE_MODEL=gemini-1.5-pro
# CLAUDE_MODEL=gemini-2.0-flash-exp
```

**Requirements:**
1. Enable Gemini in Model Garden
2. May need different region (try us-central1)
3. Authenticate with quota project

## Enabling Gemini Models

Gemini models require separate enablement:

1. **Visit Vertex AI Model Garden:**
   ```
   https://console.cloud.google.com/vertex-ai/publishers/google/model-garden
   ```

2. **Search for "Gemini"**

3. **Select a model** (e.g., gemini-1.5-pro)

4. **Click "Enable" or "Request Access"**

5. **Wait for approval** (usually instant for most projects)

6. **Update your `.env`:**
   ```bash
   CLAUDE_PROVIDER=gemini
   CLAUDE_MODEL=gemini-1.5-pro
   VERTEX_REGION=us-central1  # Try this region
   ```

## Testing Your Configuration

```bash
# Run the launcher
./run.sh

# Select option 5: Test Interface
# This will show which provider and model you're using
```

Or test directly:

```bash
source venv/bin/activate
python3 << 'EOF'
from claude_client import create_claude_client, get_model_name
import os

print(f"Provider: {os.environ.get('CLAUDE_PROVIDER', 'anthropic')}")
print(f"Model: {get_model_name()}")

client = create_claude_client()
print("✅ Client created successfully!")
EOF
```

## Model Comparison

| Model | Provider | Speed | Cost | Best For |
|-------|----------|-------|------|----------|
| claude-sonnet-4-5 | Both | Fast | Low | General tasks |
| claude-opus-4-5 | Both | Slower | High | Complex reasoning |
| gemini-1.5-flash | Vertex | Fastest | Lowest | Quick tasks |
| gemini-1.5-pro | Vertex | Fast | Medium | Balanced performance |
| gemini-2.0-flash-exp | Vertex | Fastest | Lowest | Experimental features |

## Troubleshooting

### "Model not found" Error

**For Claude Models:**
- Verify model name format (@ for Vertex, - for Anthropic)
- Check region availability
- Ensure Vertex AI API is enabled

**For Gemini Models:**
- Enable model in Model Garden first
- Try different region (us-central1 vs us-east5)
- Check project permissions
- Verify quota project is set

### Region Issues

Some models aren't available in all regions:

- **Claude**: Available in most regions (us-east5, us-central1, etc.)
- **Gemini**: Limited regions (try us-central1 first)

### Authentication

Ensure you're authenticated with quota project:

```bash
./run.sh
# Select option 6: Authenticate with Vertex AI
```

## Examples

### Use Claude Opus for Complex Tasks

```bash
# .env
CLAUDE_PROVIDER=vertex
CLAUDE_MODEL=claude-opus-4-5@20251101
```

### Use Gemini for Speed

```bash
# .env
CLAUDE_PROVIDER=gemini
CLAUDE_MODEL=gemini-1.5-flash
VERTEX_REGION=us-central1
```

### Use Anthropic Direct API

```bash
# .env
CLAUDE_PROVIDER=anthropic
CLAUDE_MODEL=claude-sonnet-4-5-20250929
ANTHROPIC_API_KEY=sk-ant-...
```

## Current Status

✅ **Working:** Claude Sonnet 4.5 on Vertex AI (us-east5)
⚠️  **Requires Setup:** Gemini models (need Model Garden enablement)

Run `./run.sh` → option 5 to verify your current configuration!

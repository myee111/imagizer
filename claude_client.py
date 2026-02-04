#!/usr/bin/env python3
"""
Claude Client Factory Module

Provides centralized client initialization for Claude API with support for:
- Anthropic API (default)
- Google Vertex AI
- Google Gemini (via Vertex AI)

Configure via environment variables:
- CLAUDE_PROVIDER: "anthropic" (default), "vertex", or "gemini"
- CLAUDE_MODEL: Model to use (optional, defaults per provider)
- ANTHROPIC_API_KEY: For Anthropic API
- VERTEX_PROJECT_ID, VERTEX_REGION: For Vertex AI
"""

import os
import base64
import io
from typing import Tuple
from dotenv import load_dotenv
from PIL import Image
import pillow_heif

# Register HEIF opener with PIL to support HEIC images
pillow_heif.register_heif_opener()

# Load environment variables
load_dotenv()


def create_claude_client():
    """
    Factory function to create the appropriate client based on CLAUDE_PROVIDER.

    Returns:
        Client instance (Anthropic, AnthropicVertex, or Gemini wrapper)

    Raises:
        ValueError: If provider is invalid or required credentials are missing
        ImportError: If required packages are not installed
    """
    provider = os.environ.get("CLAUDE_PROVIDER", "anthropic").lower()

    if provider == "anthropic":
        return _create_anthropic_client()
    elif provider == "vertex":
        return _create_vertex_client()
    elif provider == "gemini":
        return _create_gemini_client()
    else:
        raise ValueError(
            f"Invalid CLAUDE_PROVIDER: '{provider}'. Must be 'anthropic', 'vertex', or 'gemini'.\n"
            f"Set CLAUDE_PROVIDER in your .env file."
        )


def get_model_name(provider: str = None) -> str:
    """
    Get the model name to use based on provider and CLAUDE_MODEL env var.

    Args:
        provider: Provider name (anthropic, vertex, gemini)

    Returns:
        Model name string
    """
    if provider is None:
        provider = os.environ.get("CLAUDE_PROVIDER", "anthropic").lower()

    # Check for explicit model override
    model = os.environ.get("CLAUDE_MODEL")
    if model:
        return model

    # Default models per provider
    defaults = {
        "anthropic": "claude-sonnet-4-5-20250929",
        "vertex": "claude-sonnet-4-5@20250929",  # Vertex uses @ instead of -
        "gemini": "gemini-1.5-flash-002"  # Stable, widely available
    }

    return defaults.get(provider, "claude-sonnet-4-5-20250929")


def _create_anthropic_client():
    """
    Create an Anthropic API client.

    Returns:
        Anthropic client instance

    Raises:
        ValueError: If ANTHROPIC_API_KEY is not set
    """
    try:
        from anthropic import Anthropic
    except ImportError:
        raise ImportError(
            "anthropic package not found. Install with: pip install anthropic"
        )

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError(
            "ANTHROPIC_API_KEY not found in environment variables.\n"
            "Setup instructions:\n"
            "1. Get API key from https://console.anthropic.com/\n"
            "2. Add to .env file: ANTHROPIC_API_KEY=sk-ant-...\n"
            "3. Make sure .env is in your project root"
        )

    print(f"[Claude Client] Using Anthropic API")
    return Anthropic(api_key=api_key)


def _create_vertex_client():
    """
    Create a Vertex AI client.

    Returns:
        AnthropicVertex client instance

    Raises:
        ValueError: If required Vertex AI credentials are missing
        ImportError: If required packages are not installed
    """
    try:
        from anthropic import AnthropicVertex
    except ImportError:
        raise ImportError(
            "Vertex AI support not found. Install with:\n"
            "pip install 'anthropic[vertex]' google-cloud-aiplatform"
        )

    project_id = os.environ.get("VERTEX_PROJECT_ID")
    region = os.environ.get("VERTEX_REGION", "us-central1")

    if not project_id:
        raise ValueError(
            "VERTEX_PROJECT_ID not found in environment variables.\n"
            "Setup instructions:\n"
            "1. Create a Google Cloud project\n"
            "2. Enable Vertex AI API\n"
            "3. Authenticate: gcloud auth application-default login\n"
            "4. Add to .env file:\n"
            "   VERTEX_PROJECT_ID=your-project-id\n"
            "   VERTEX_REGION=us-central1  # or your preferred region\n"
            "5. Install dependencies: pip install 'anthropic[vertex]' google-cloud-aiplatform"
        )

    print(f"[Claude Client] Using Vertex AI Claude (project: {project_id}, region: {region})")
    return AnthropicVertex(project_id=project_id, region=region)


def _create_gemini_client():
    """
    Create a Gemini client via Vertex AI.

    Returns:
        GeminiWrapper client instance that mimics Anthropic API

    Raises:
        ValueError: If required credentials are missing
        ImportError: If required packages are not installed
    """
    try:
        import vertexai
        from vertexai.generative_models import GenerativeModel
    except ImportError:
        raise ImportError(
            "Vertex AI SDK not found. Install with:\n"
            "pip install google-cloud-aiplatform"
        )

    project_id = os.environ.get("VERTEX_PROJECT_ID")
    region = os.environ.get("VERTEX_REGION", "us-central1")

    if not project_id:
        raise ValueError(
            "VERTEX_PROJECT_ID not found in environment variables.\n"
            "Setup instructions:\n"
            "1. Create a Google Cloud project\n"
            "2. Enable Vertex AI API\n"
            "3. Authenticate: gcloud auth application-default login\n"
            "4. Add to .env file:\n"
            "   CLAUDE_PROVIDER=gemini\n"
            "   VERTEX_PROJECT_ID=your-project-id\n"
            "   VERTEX_REGION=us-central1\n"
            "5. Install dependencies: pip install google-cloud-aiplatform"
        )

    # Initialize Vertex AI
    vertexai.init(project=project_id, location=region)

    model_name = get_model_name("gemini")
    print(f"[Gemini Client] Using Vertex AI Gemini (project: {project_id}, region: {region}, model: {model_name})")

    # Return wrapper that provides Anthropic-compatible interface
    return GeminiWrapper(project_id=project_id, region=region, model_name=model_name)


class GeminiWrapper:
    """
    Wrapper for Gemini API that provides an Anthropic-compatible interface.
    """

    def __init__(self, project_id: str, region: str, model_name: str):
        import vertexai
        from vertexai.generative_models import GenerativeModel, Part

        self.project_id = project_id
        self.region = region
        self.model_name = model_name

        vertexai.init(project=project_id, location=region)
        self.model = GenerativeModel(model_name)
        self.Part = Part

    class Messages:
        """Messages API wrapper for Gemini."""

        def __init__(self, parent):
            self.parent = parent

        def create(self, model: str, max_tokens: int, messages: list, tools=None, **kwargs):
            """
            Create a message using Gemini API with Anthropic-compatible interface.
            """
            from vertexai.generative_models import Content, Part
            import types

            # Convert Anthropic messages format to Gemini format
            gemini_contents = []

            for msg in messages:
                role = "user" if msg["role"] == "user" else "model"

                # Handle content (can be string or list)
                content = msg["content"]
                parts = []

                if isinstance(content, str):
                    parts.append(Part.from_text(content))
                elif isinstance(content, list):
                    for item in content:
                        if item["type"] == "text":
                            parts.append(Part.from_text(item["text"]))
                        elif item["type"] == "image":
                            # Handle base64 image
                            image_data = base64.b64decode(item["source"]["data"])
                            parts.append(Part.from_data(
                                data=image_data,
                                mime_type=item["source"]["media_type"]
                            ))
                        elif item["type"] == "tool_result":
                            # Convert tool result to text
                            parts.append(Part.from_text(f"Tool result: {item['content']}"))

                if parts:
                    gemini_contents.append(Content(role=role, parts=parts))

            # Generate response
            response = self.parent.model.generate_content(
                gemini_contents,
                generation_config={
                    "max_output_tokens": max_tokens,
                    "temperature": kwargs.get("temperature", 1.0),
                }
            )

            # Convert Gemini response to Anthropic format
            class MockResponse:
                def __init__(self, gemini_response, model_name):
                    self.id = "gemini-" + str(hash(gemini_response.text))
                    self.model = model_name
                    self.stop_reason = "end_turn"
                    self.usage = types.SimpleNamespace(
                        input_tokens=0,
                        output_tokens=0
                    )

                    # Create content blocks
                    class TextBlock:
                        def __init__(self, text):
                            self.type = "text"
                            self.text = text

                    self.content = [TextBlock(gemini_response.text)]

            return MockResponse(response, self.parent.model_name)

    @property
    def messages(self):
        """Return messages API."""
        return self.Messages(self)


def load_and_encode_image(file_path: str) -> Tuple[str, str]:
    """
    Load an image file and return base64-encoded data and media type.
    Automatically converts HEIC/HEIF to JPEG for API compatibility.

    Args:
        file_path: Path to the image file

    Returns:
        Tuple of (base64_encoded_data, media_type)

    Raises:
        FileNotFoundError: If image file doesn't exist
        Exception: If image cannot be loaded or encoded
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Image file not found: {file_path}")

    extension = file_path.lower().split('.')[-1]

    if extension in ['heic', 'heif']:
        # Convert HEIC/HEIF to JPEG
        img = Image.open(file_path)
        if img.mode not in ('RGB', 'L'):
            img = img.convert('RGB')
        buffer = io.BytesIO()
        img.save(buffer, format='JPEG', quality=95)
        buffer.seek(0)
        image_data = base64.standard_b64encode(buffer.read()).decode('utf-8')
        media_type = 'image/jpeg'
    else:
        # Handle standard image formats
        with open(file_path, 'rb') as image_file:
            image_data = base64.standard_b64encode(image_file.read()).decode('utf-8')
        media_type = get_image_media_type(extension)

    return image_data, media_type


def get_image_media_type(extension: str) -> str:
    """
    Get the media type for an image file extension.

    Args:
        extension: File extension (without dot)

    Returns:
        Media type string (e.g., 'image/jpeg')
    """
    media_types = {
        'jpg': 'image/jpeg',
        'jpeg': 'image/jpeg',
        'png': 'image/png',
        'gif': 'image/gif',
        'webp': 'image/webp'
    }
    return media_types.get(extension.lower(), 'image/jpeg')

#!/usr/bin/env python3
"""
Claude Client Factory Module

Provides centralized client initialization for Claude API with support for:
- Anthropic API (default)
- Google Vertex AI

Configure via environment variables:
- CLAUDE_PROVIDER: "anthropic" (default) or "vertex"
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
    Factory function to create the appropriate Claude client based on CLAUDE_PROVIDER.

    Returns:
        Anthropic or AnthropicVertex client instance

    Raises:
        ValueError: If provider is invalid or required credentials are missing
        ImportError: If required packages are not installed
    """
    provider = os.environ.get("CLAUDE_PROVIDER", "anthropic").lower()

    if provider == "anthropic":
        return _create_anthropic_client()
    elif provider == "vertex":
        return _create_vertex_client()
    else:
        raise ValueError(
            f"Invalid CLAUDE_PROVIDER: '{provider}'. Must be 'anthropic' or 'vertex'.\n"
            f"Set CLAUDE_PROVIDER=anthropic or CLAUDE_PROVIDER=vertex in your .env file."
        )


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

    print(f"[Claude Client] Using Vertex AI (project: {project_id}, region: {region})")
    return AnthropicVertex(project_id=project_id, region=region)


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

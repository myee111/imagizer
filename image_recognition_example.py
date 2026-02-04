#!/usr/bin/env python3
"""
Example script demonstrating image recognition capabilities.
"""

import os
import base64
import io
from anthropic import Anthropic
from dotenv import load_dotenv
from PIL import Image
import pillow_heif

# Register HEIF opener with PIL to support HEIC images
pillow_heif.register_heif_opener()

# Load environment variables
load_dotenv()

# Initialize Anthropic client
client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))


def load_and_encode_image(file_path: str) -> tuple:
    """
    Load an image file and return base64-encoded data and media type.
    Automatically converts HEIC/HEIF to JPEG for API compatibility.
    """
    extension = file_path.lower().split('.')[-1]

    if extension in ['heic', 'heif']:
        img = Image.open(file_path)
        if img.mode not in ('RGB', 'L'):
            img = img.convert('RGB')
        buffer = io.BytesIO()
        img.save(buffer, format='JPEG', quality=95)
        buffer.seek(0)
        image_data = base64.standard_b64encode(buffer.read()).decode('utf-8')
        media_type = 'image/jpeg'
    else:
        with open(file_path, 'rb') as image_file:
            image_data = base64.standard_b64encode(image_file.read()).decode('utf-8')
        media_types = {
            'jpg': 'image/jpeg', 'jpeg': 'image/jpeg',
            'png': 'image/png', 'gif': 'image/gif', 'webp': 'image/webp'
        }
        media_type = media_types.get(extension, 'image/jpeg')

    return image_data, media_type


def analyze_image(image_path: str, prompt: str = "What's in this image?"):
    """
    Analyze an image using Claude's vision capabilities.

    Args:
        image_path: Path to the image file
        prompt: Question or instruction about the image

    Returns:
        Claude's analysis of the image
    """
    # Load and encode the image (handles HEIC conversion)
    image_data, media_type = load_and_encode_image(image_path)

    # Create message with image
    message = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=2048,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": media_type,
                            "data": image_data
                        }
                    },
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ]
    )

    # Extract response
    response_text = ""
    for block in message.content:
        if hasattr(block, 'text'):
            response_text += block.text

    return response_text


def main():
    """
    Example usage of image recognition.
    """
    print("=" * 60)
    print("Claude Vision - Image Recognition Examples")
    print("=" * 60)

    # Example 1: General image description
    print("\nExample 1: General Description")
    print("-" * 60)
    # result = analyze_image("path/to/your/image.jpg", "Describe this image in detail")
    # print(result)
    print("Uncomment the code above and provide an image path to test")

    # Example 2: Object detection
    print("\nExample 2: Object Detection")
    print("-" * 60)
    # result = analyze_image("path/to/your/image.jpg", "List all objects you can identify in this image")
    # print(result)
    print("Uncomment the code above and provide an image path to test")

    # Example 3: Text extraction (OCR)
    print("\nExample 3: Text Extraction (OCR)")
    print("-" * 60)
    # result = analyze_image("path/to/document.jpg", "Extract all text from this image")
    # print(result)
    print("Uncomment the code above and provide an image path to test")

    # Example 4: Specific questions
    print("\nExample 4: Specific Questions")
    print("-" * 60)
    # result = analyze_image("path/to/photo.jpg", "How many people are in this image?")
    # print(result)
    print("Uncomment the code above and provide an image path to test")

    # Example 5: Scene analysis
    print("\nExample 5: Scene Analysis")
    print("-" * 60)
    # result = analyze_image("path/to/scene.jpg", "What is the setting? Is this indoors or outdoors? Describe the atmosphere")
    # print(result)
    print("Uncomment the code above and provide an image path to test")

    # Interactive mode
    print("\n" + "=" * 60)
    print("Interactive Image Analysis")
    print("Type 'quit' to exit")
    print("=" * 60)

    while True:
        image_path = input("\nImage path (or 'quit'): ").strip()
        if image_path.lower() in ['quit', 'exit', 'q']:
            print("Goodbye!")
            break

        if not os.path.exists(image_path):
            print(f"Error: File not found at {image_path}")
            continue

        question = input("Your question about the image: ").strip()
        if not question:
            question = "Describe this image in detail"

        try:
            print("\nAnalyzing image...")
            result = analyze_image(image_path, question)
            print("\n" + "-" * 60)
            print("Analysis:")
            print("-" * 60)
            print(result)
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()

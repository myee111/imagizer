#!/usr/bin/env python3
"""
People recognition and analysis using Claude's vision capabilities.

IMPORTANT PRIVACY NOTE:
- This agent can detect and describe people in images
- It can count people, describe activities, clothing, poses, etc.
- It may recognize widely-known public figures in appropriate contexts
- It cannot and should not be used to identify private individuals
- Do not use for surveillance or unauthorized identification purposes
"""

import os
import base64
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))


def get_image_media_type(file_path: str) -> str:
    """Determine the media type from file extension."""
    extension = file_path.lower().split('.')[-1]
    media_types = {
        'jpg': 'image/jpeg',
        'jpeg': 'image/jpeg',
        'png': 'image/png',
        'gif': 'image/gif',
        'webp': 'image/webp'
    }
    return media_types.get(extension, 'image/jpeg')


def analyze_people_in_image(image_path: str, analysis_type: str = "general"):
    """
    Analyze people in an image.

    Args:
        image_path: Path to the image file
        analysis_type: Type of analysis to perform:
            - "general": General description of people
            - "count": Count number of people
            - "activities": Describe what people are doing
            - "detailed": Detailed description of each person
            - "attributes": Describe clothing, poses, demographics

    Returns:
        Analysis results
    """
    # Define prompts for different analysis types
    prompts = {
        "general": "Describe the people in this image.",
        "count": "How many people are in this image? Provide just the number and any relevant details about their positions.",
        "activities": "What are the people in this image doing? Describe their activities and interactions.",
        "detailed": """Analyze each person in this image and provide:
1. A count of total people
2. For each person, describe:
   - Their approximate position in the image
   - What they're doing
   - Their clothing and appearance
   - Any notable characteristics
   - Their pose or body language""",
        "attributes": """For the people in this image, describe:
- Clothing and style
- Approximate age ranges (child, teen, adult, elderly)
- Poses and body language
- Apparent emotions or expressions
- Any accessories or distinctive features
- Group dynamics if multiple people""",
        "demographics": """Describe the people in this image in terms of:
- Approximate count
- Apparent age distribution
- Gender presentation if relevant to the context
- General appearance and style
Note: Provide respectful, objective descriptions only."""
    }

    prompt = prompts.get(analysis_type, prompts["general"])

    # Read and encode image
    with open(image_path, 'rb') as image_file:
        image_data = base64.standard_b64encode(image_file.read()).decode('utf-8')

    media_type = get_image_media_type(image_path)

    # Call Claude with vision
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


def detect_faces(image_path: str):
    """
    Detect and describe faces in an image.
    """
    prompt = """Analyze the faces in this image:
1. How many faces can you see?
2. For each face, describe:
   - Approximate age
   - Apparent expression or emotion
   - Facial features (glasses, facial hair, etc.)
   - Direction they're looking
   - Any other notable characteristics

Provide objective, respectful descriptions only."""

    with open(image_path, 'rb') as image_file:
        image_data = base64.standard_b64encode(image_file.read()).decode('utf-8')

    media_type = get_image_media_type(image_path)

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

    response_text = ""
    for block in message.content:
        if hasattr(block, 'text'):
            response_text += block.text

    return response_text


def analyze_group_dynamics(image_path: str):
    """
    Analyze interactions and dynamics between people.
    """
    prompt = """Analyze the group dynamics in this image:
1. How many people are present?
2. How are they positioned relative to each other?
3. What interactions or relationships can you infer?
4. What is the apparent social context (meeting, party, family gathering, etc.)?
5. What is the overall mood or atmosphere?
6. Are there any notable group behaviors or activities?"""

    with open(image_path, 'rb') as image_file:
        image_data = base64.standard_b64encode(image_file.read()).decode('utf-8')

    media_type = get_image_media_type(image_path)

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

    response_text = ""
    for block in message.content:
        if hasattr(block, 'text'):
            response_text += block.text

    return response_text


def main():
    """
    Interactive people recognition system.
    """
    print("=" * 70)
    print("People Recognition Agent - Powered by Claude Vision")
    print("=" * 70)
    print("\nThis agent can:")
    print("  • Count people in images")
    print("  • Describe what people are doing")
    print("  • Analyze facial expressions and emotions")
    print("  • Describe clothing and appearance")
    print("  • Analyze group dynamics and interactions")
    print("  • Detect poses and body language")
    print("\nPrivacy Note:")
    print("  • This tool describes people but does not identify individuals")
    print("  • Use responsibly and respect privacy")
    print("=" * 70)

    while True:
        print("\n" + "=" * 70)
        print("Choose an analysis type:")
        print("  1. Count people")
        print("  2. Describe activities")
        print("  3. Detailed person-by-person analysis")
        print("  4. Clothing and attributes")
        print("  5. Face detection and expressions")
        print("  6. Group dynamics and interactions")
        print("  7. Custom question")
        print("  8. Quit")
        print("=" * 70)

        choice = input("\nYour choice (1-8): ").strip()

        if choice == "8":
            print("Goodbye!")
            break

        image_path = input("Image path: ").strip()

        if not os.path.exists(image_path):
            print(f"Error: File not found at {image_path}")
            continue

        try:
            print("\nAnalyzing image...\n")

            if choice == "1":
                result = analyze_people_in_image(image_path, "count")
            elif choice == "2":
                result = analyze_people_in_image(image_path, "activities")
            elif choice == "3":
                result = analyze_people_in_image(image_path, "detailed")
            elif choice == "4":
                result = analyze_people_in_image(image_path, "attributes")
            elif choice == "5":
                result = detect_faces(image_path)
            elif choice == "6":
                result = analyze_group_dynamics(image_path)
            elif choice == "7":
                question = input("Your question: ").strip()
                with open(image_path, 'rb') as image_file:
                    image_data = base64.standard_b64encode(image_file.read()).decode('utf-8')
                media_type = get_image_media_type(image_path)

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
                                    "text": question
                                }
                            ]
                        }
                    ]
                )

                result = ""
                for block in message.content:
                    if hasattr(block, 'text'):
                        result += block.text
            else:
                print("Invalid choice")
                continue

            print("-" * 70)
            print("Analysis Result:")
            print("-" * 70)
            print(result)
            print("-" * 70)

        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()

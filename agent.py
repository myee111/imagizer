#!/usr/bin/env python3
"""
A simple AI agent powered by Claude with tool use capabilities.
"""

import os
import json
from pathlib import Path
from claude_client import create_claude_client, load_and_encode_image

# Initialize Claude client (supports Anthropic API and Vertex AI)
client = create_claude_client()

# Define tools that the agent can use
TOOLS = [
    {
        "name": "get_weather",
        "description": "Get the current weather for a given location",
        "input_schema": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city and state, e.g. San Francisco, CA"
                }
            },
            "required": ["location"]
        }
    },
    {
        "name": "calculate",
        "description": "Perform a mathematical calculation",
        "input_schema": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "The mathematical expression to evaluate, e.g. '2 + 2' or '10 * 5'"
                }
            },
            "required": ["expression"]
        }
    },
    {
        "name": "analyze_image",
        "description": "Analyze an image file and extract information from it. Can identify objects, read text, describe scenes, and answer questions about the image.",
        "input_schema": {
            "type": "object",
            "properties": {
                "image_path": {
                    "type": "string",
                    "description": "The file path to the image to analyze (supports jpg, png, gif, webp, heic)"
                },
                "question": {
                    "type": "string",
                    "description": "Optional specific question about the image. If not provided, will give a general description."
                }
            },
            "required": ["image_path"]
        }
    },
    {
        "name": "analyze_people",
        "description": "Detect and analyze people in an image. Can count people, describe their activities, clothing, poses, facial expressions, and group dynamics. Use this for any questions about people in images.",
        "input_schema": {
            "type": "object",
            "properties": {
                "image_path": {
                    "type": "string",
                    "description": "The file path to the image to analyze"
                },
                "analysis_type": {
                    "type": "string",
                    "description": "Type of analysis: 'count' (count people), 'activities' (what they're doing), 'detailed' (full description of each person), 'faces' (facial expressions), 'group' (group dynamics), or 'custom'",
                    "enum": ["count", "activities", "detailed", "faces", "group", "custom"]
                },
                "custom_question": {
                    "type": "string",
                    "description": "For analysis_type='custom', specify what you want to know about the people"
                }
            },
            "required": ["image_path", "analysis_type"]
        }
    },
    {
        "name": "identify_person",
        "description": "Identify specific individuals in an image by comparing against a reference database. Use this when user asks 'who is this' or wants to identify people by name. Requires a face database to be set up first (use face_identification.py).",
        "input_schema": {
            "type": "object",
            "properties": {
                "image_path": {
                    "type": "string",
                    "description": "The file path to the image containing people to identify"
                }
            },
            "required": ["image_path"]
        }
    }
]


def analyze_image_with_vision(image_path: str, question: str = None) -> str:
    """
    Analyze an image using Claude's vision capabilities.

    Args:
        image_path: Path to the image file
        question: Optional specific question about the image

    Returns:
        Analysis results as a string
    """
    try:
        # Read and encode the image (handles HEIC conversion)
        image_data, media_type = load_and_encode_image(image_path)

        # Create the prompt
        if question:
            prompt = f"Please analyze this image and answer the following question: {question}"
        else:
            prompt = "Please analyze this image and provide a detailed description of what you see."

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

        # Extract the response
        response_text = ""
        for block in message.content:
            if hasattr(block, 'text'):
                response_text += block.text

        return response_text

    except FileNotFoundError:
        return f"Error: Image file not found at {image_path}"
    except Exception as e:
        return f"Error analyzing image: {str(e)}"


def analyze_people_with_vision(image_path: str, analysis_type: str, custom_question: str = None) -> str:
    """
    Analyze people in an image using Claude's vision capabilities.

    Args:
        image_path: Path to the image file
        analysis_type: Type of analysis to perform
        custom_question: For custom analysis type, the specific question

    Returns:
        Analysis results as a string
    """
    try:
        # Read and encode the image (handles HEIC conversion)
        image_data, media_type = load_and_encode_image(image_path)

        # Create prompts based on analysis type
        prompts = {
            "count": "How many people are in this image? Provide the count and describe their general positions or groupings.",
            "activities": "What are the people in this image doing? Describe their activities, actions, and any interactions between them.",
            "detailed": """Analyze each person in this image:
1. Provide a total count
2. For each person, describe:
   - Their position in the image
   - What they're doing
   - Their clothing and appearance
   - Body language and pose
   - Any notable characteristics""",
            "faces": """Analyze the faces and expressions in this image:
1. How many people/faces are visible?
2. For each person, describe:
   - Apparent facial expression or emotion
   - Direction they're looking
   - Approximate age range
   - Any distinctive facial features (glasses, facial hair, etc.)
   - Overall demeanor""",
            "group": """Analyze the group dynamics in this image:
1. How many people are present?
2. How are they positioned relative to each other?
3. What interactions or relationships can you infer?
4. What is the social context or setting?
5. What is the overall mood or atmosphere?
6. Describe any notable group behaviors.""",
            "custom": custom_question if custom_question else "Describe the people in this image."
        }

        prompt = prompts.get(analysis_type, prompts["custom"])

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

        # Extract the response
        response_text = ""
        for block in message.content:
            if hasattr(block, 'text'):
                response_text += block.text

        return response_text

    except FileNotFoundError:
        return f"Error: Image file not found at {image_path}"
    except Exception as e:
        return f"Error analyzing people in image: {str(e)}"


def identify_people_from_database(image_path: str) -> str:
    """
    Identify people in an image using the face database.

    Args:
        image_path: Path to image to analyze

    Returns:
        Identification results
    """
    DATABASE_FILE = "face_database.json"

    # Check if database exists
    if not os.path.exists(DATABASE_FILE):
        return """Face database not found. To use person identification:

1. Run: python face_identification.py
2. Add people to the database (with their consent)
3. Then use this tool to identify them in photos

The database stores reference images and facial descriptions to enable identification."""

    # Load database
    try:
        with open(DATABASE_FILE, 'r') as f:
            db = json.load(f)
    except Exception as e:
        return f"Error loading database: {str(e)}"

    if not db.get("people"):
        return "Face database is empty. Add people using: python face_identification.py"

    # Read target image (handles HEIC conversion)
    try:
        target_image_data, target_media_type = load_and_encode_image(image_path)
    except FileNotFoundError:
        return f"Error: Image not found at {image_path}"
    except Exception as e:
        return f"Error reading image: {str(e)}"

    # Build comparison prompt
    people_descriptions = "\n\n".join([
        f"Person {i+1} - {person['name']}:\n{person['facial_description']}"
        for i, person in enumerate(db['people'])
    ])

    prompt = f"""Compare the people in this image against these known individuals from the user's personal photo database:

{people_descriptions}

For each person visible in the image:
1. Describe their appearance
2. Determine if they match any of the known individuals
3. Provide confidence level (high/medium/low) for any matches
4. Explain the reasoning

Format as:
PERSON 1:
- Match: [name or "Unknown"]
- Confidence: [High/Medium/Low]
- Reasoning: [explanation]

Be careful and thorough. Only claim high confidence if features clearly match."""

    # Call Claude for identification
    try:
        message = client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=2048,
            messages=[{
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": target_media_type,
                            "data": target_image_data
                        }
                    },
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }]
        )

        result = ""
        for block in message.content:
            if hasattr(block, 'text'):
                result += block.text

        return f"Identification results (comparing against {len(db['people'])} people in database):\n\n{result}"

    except Exception as e:
        return f"Error during identification: {str(e)}"


def execute_tool(tool_name: str, tool_input: dict) -> str:
    """
    Execute a tool and return the result.
    In a real agent, these would call actual APIs or perform real actions.
    """
    if tool_name == "get_weather":
        location = tool_input["location"]
        # Mock response - in production, call a real weather API
        return f"The weather in {location} is sunny and 72°F"

    elif tool_name == "calculate":
        expression = tool_input["expression"]
        try:
            # Safe evaluation of simple math expressions
            result = eval(expression, {"__builtins__": {}}, {})
            return f"Result: {result}"
        except Exception as e:
            return f"Error calculating: {str(e)}"

    elif tool_name == "analyze_image":
        image_path = tool_input["image_path"]
        question = tool_input.get("question")
        return analyze_image_with_vision(image_path, question)

    elif tool_name == "analyze_people":
        image_path = tool_input["image_path"]
        analysis_type = tool_input["analysis_type"]
        custom_question = tool_input.get("custom_question")
        return analyze_people_with_vision(image_path, analysis_type, custom_question)

    elif tool_name == "identify_person":
        image_path = tool_input["image_path"]
        return identify_people_from_database(image_path)

    return f"Unknown tool: {tool_name}"


def run_agent(user_message: str, image_path: str = None, max_turns: int = 10) -> str:
    """
    Run the agent in an agentic loop, allowing it to use tools autonomously.

    Args:
        user_message: The user's input/question
        image_path: Optional path to an image to include in the initial message
        max_turns: Maximum number of conversation turns to prevent infinite loops

    Returns:
        The agent's final response
    """
    # Build initial message content
    if image_path:
        try:
            # Load and encode image (handles HEIC conversion)
            image_data, media_type = load_and_encode_image(image_path)

            content = [
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
                    "text": user_message
                }
            ]
        except Exception as e:
            print(f"Error loading image: {e}")
            content = user_message
    else:
        content = user_message

    messages = [{"role": "user", "content": content}]

    print(f"\n{'='*60}")
    print(f"User: {user_message}")
    print(f"{'='*60}\n")

    for turn in range(max_turns):
        # Call Claude with tools
        response = client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=4096,
            tools=TOOLS,
            messages=messages
        )

        print(f"Turn {turn + 1}:")
        print(f"Stop reason: {response.stop_reason}")

        # Process the response
        if response.stop_reason == "end_turn":
            # Agent is done, extract final text response
            final_response = ""
            for block in response.content:
                if block.type == "text":
                    final_response += block.text
            print(f"Final response: {final_response}\n")
            return final_response

        elif response.stop_reason == "tool_use":
            # Agent wants to use tools
            messages.append({"role": "assistant", "content": response.content})

            # Execute all tool calls
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    tool_name = block.name
                    tool_input = block.input

                    print(f"  Using tool: {tool_name}")
                    print(f"  Input: {json.dumps(tool_input, indent=2)}")

                    # Execute the tool
                    result = execute_tool(tool_name, tool_input)
                    print(f"  Result: {result}\n")

                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result
                    })

            # Add tool results to messages
            messages.append({"role": "user", "content": tool_results})

        else:
            # Unexpected stop reason
            print(f"Unexpected stop reason: {response.stop_reason}")
            break

    return "Agent reached maximum turns without completing the task."


def main():
    """
    Main function demonstrating the agent in action.
    """
    print("AI Agent powered by Claude with Vision")
    print("=" * 60)

    # Example 1: Using weather tool
    result1 = run_agent("What's the weather like in San Francisco?")

    # Example 2: Using calculator tool
    result2 = run_agent("What is 157 * 23?")

    # Example 3: Multi-step reasoning with multiple tools
    result3 = run_agent(
        "What's the weather in New York? Also, if I have 5 apples "
        "and buy 3 more, how many do I have?"
    )

    # Example 4: Image recognition (if you have a test image)
    # Uncomment and update the path to test image recognition:
    # result4 = run_agent("What's in this image?", image_path="path/to/your/image.jpg")

    # Or use the analyze_image tool:
    # result5 = run_agent("Please analyze the image at ./test_image.jpg and tell me what objects you see")

    # Interactive mode
    print("\n" + "="*60)
    print("Interactive mode - type 'quit' to exit")
    print("To analyze an image, type: image:/path/to/image.jpg What do you see?")
    print("="*60)

    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("Goodbye!")
            break
        if user_input:
            # Check if user is providing an image
            if user_input.startswith("image:"):
                try:
                    parts = user_input[6:].split(maxsplit=1)
                    img_path = parts[0]
                    question = parts[1] if len(parts) > 1 else "What's in this image?"
                    run_agent(question, image_path=img_path)
                except Exception as e:
                    print(f"Error: {e}")
                    print("Format: image:/path/to/image.jpg Your question here")
            else:
                run_agent(user_input)


if __name__ == "__main__":
    main()

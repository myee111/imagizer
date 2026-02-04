#!/usr/bin/env python3
"""
Personal Photo Identification System

This tool helps you organize personal photos by identifying family and friends.

IMPORTANT PRIVACY & CONSENT REQUIREMENTS:
- Only use on YOUR OWN personal photos
- Get explicit consent from everyone you add to the system
- Store data securely and don't share without permission
- Allow people to request removal of their data at any time
- This is for personal use only, not for public deployment

How it works:
1. Build a reference database with photos of known people (with consent)
2. System compares faces in new photos against the reference database
3. Identifies matches and helps organize your photos
"""

import os
import json
import base64
from pathlib import Path
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

# Database file for storing known people
DATABASE_FILE = "face_database.json"


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


def load_database():
    """Load the face database from disk."""
    if os.path.exists(DATABASE_FILE):
        with open(DATABASE_FILE, 'r') as f:
            return json.load(f)
    return {"people": []}


def save_database(db):
    """Save the face database to disk."""
    with open(DATABASE_FILE, 'w') as f:
        json.dump(db, f, indent=2)


def add_person_to_database(name: str, reference_image_path: str, notes: str = ""):
    """
    Add a person to the reference database.

    Args:
        name: Person's name
        reference_image_path: Path to a clear photo of their face
        notes: Optional notes (relationship, context, etc.)
    """
    db = load_database()

    # Check if person already exists
    for person in db["people"]:
        if person["name"].lower() == name.lower():
            print(f"⚠️  {name} already exists in database. Use update instead.")
            return False

    # Verify image exists
    if not os.path.exists(reference_image_path):
        print(f"❌ Error: Image not found at {reference_image_path}")
        return False

    # Get facial features description for reference
    print(f"Analyzing reference image for {name}...")
    with open(reference_image_path, 'rb') as img_file:
        image_data = base64.standard_b64encode(img_file.read()).decode('utf-8')

    media_type = get_image_media_type(reference_image_path)

    # Get detailed facial description
    message = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=1024,
        messages=[{
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
                    "text": """Provide a detailed description of the person's facial features for identification purposes:
- Face shape
- Eye color and shape
- Nose characteristics
- Mouth and smile
- Hair color and style
- Distinctive features (glasses, facial hair, marks, etc.)
- Approximate age range
- Any other notable identifying characteristics

Be specific and detailed to enable future identification."""
                }
            ]
        }]
    )

    description = ""
    for block in message.content:
        if hasattr(block, 'text'):
            description += block.text

    # Add to database
    person_entry = {
        "name": name,
        "reference_image": reference_image_path,
        "facial_description": description,
        "notes": notes,
        "added_date": str(Path(reference_image_path).stat().st_mtime)
    }

    db["people"].append(person_entry)
    save_database(db)

    print(f"✅ Added {name} to database!")
    print(f"   Reference image: {reference_image_path}")
    return True


def identify_person_in_image(image_path: str, confidence_threshold: str = "medium"):
    """
    Identify people in an image by comparing against the database.

    Args:
        image_path: Path to the image to analyze
        confidence_threshold: "high", "medium", or "low" - how strict to be with matches

    Returns:
        List of identified people with confidence levels
    """
    db = load_database()

    if not db["people"]:
        return {"error": "No people in database. Add reference images first."}

    if not os.path.exists(image_path):
        return {"error": f"Image not found at {image_path}"}

    # Read the target image
    with open(image_path, 'rb') as img_file:
        target_image_data = base64.standard_b64encode(img_file.read()).decode('utf-8')

    target_media_type = get_image_media_type(image_path)

    print(f"Analyzing image: {image_path}")
    print(f"Comparing against {len(db['people'])} people in database...")

    # Build comparison prompt
    people_descriptions = "\n\n".join([
        f"Person {i+1} - {person['name']}:\n{person['facial_description']}"
        for i, person in enumerate(db['people'])
    ])

    prompt = f"""Compare the people in this image against these known individuals:

{people_descriptions}

For each person visible in the image:
1. Describe their appearance
2. Determine if they match any of the known individuals
3. Provide confidence level (high/medium/low) for any matches
4. Explain the reasoning for matches

Format your response as:
PERSON 1 IN IMAGE:
- Description: [description]
- Match: [name or "Unknown"]
- Confidence: [High/Medium/Low]
- Reasoning: [why you think this is a match]

PERSON 2 IN IMAGE:
[repeat for each person]

Be thorough and careful with identification. Only claim high confidence if features clearly match."""

    # Call Claude to compare
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

    return result


def list_database_people():
    """List all people in the database."""
    db = load_database()

    if not db["people"]:
        print("Database is empty. Add people using option 1.")
        return

    print("\n" + "=" * 70)
    print(f"Face Database - {len(db['people'])} people")
    print("=" * 70)

    for i, person in enumerate(db['people'], 1):
        print(f"\n{i}. {person['name']}")
        print(f"   Reference: {person['reference_image']}")
        if person.get('notes'):
            print(f"   Notes: {person['notes']}")
        print(f"   Description: {person['facial_description'][:100]}...")

    print("=" * 70)


def remove_person_from_database(name: str):
    """Remove a person from the database."""
    db = load_database()

    original_count = len(db["people"])
    db["people"] = [p for p in db["people"] if p["name"].lower() != name.lower()]

    if len(db["people"]) < original_count:
        save_database(db)
        print(f"✅ Removed {name} from database")
        return True
    else:
        print(f"❌ {name} not found in database")
        return False


def main():
    """
    Main interactive interface for face identification.
    """
    print("=" * 70)
    print("Personal Photo Identification System")
    print("=" * 70)
    print("\n⚠️  PRIVACY & CONSENT NOTICE")
    print("-" * 70)
    print("• Only use on YOUR personal photos")
    print("• Get CONSENT from everyone you add to the database")
    print("• Keep data secure and don't share without permission")
    print("• Allow people to request removal at any time")
    print("• This is for PERSONAL use only")
    print("=" * 70)

    consent = input("\nI agree to use this responsibly (yes/no): ").strip().lower()
    if consent != 'yes':
        print("You must agree to responsible use. Exiting.")
        return

    while True:
        print("\n" + "=" * 70)
        print("What would you like to do?")
        print("=" * 70)
        print("1. Add a person to database (requires consent)")
        print("2. Identify people in a photo")
        print("3. View database")
        print("4. Remove person from database")
        print("5. Export database")
        print("6. Quit")
        print("=" * 70)

        choice = input("\nYour choice (1-6): ").strip()

        if choice == "1":
            print("\n📸 Add Person to Database")
            print("-" * 70)
            name = input("Person's name: ").strip()
            if not name:
                print("Name cannot be empty")
                continue

            reference_image = input("Path to reference image (clear face photo): ").strip()
            notes = input("Notes (relationship, etc.) [optional]: ").strip()

            consent_check = input(f"Do you have {name}'s consent to add them? (yes/no): ").strip().lower()
            if consent_check != 'yes':
                print("❌ Cannot add without consent")
                continue

            add_person_to_database(name, reference_image, notes)

        elif choice == "2":
            print("\n🔍 Identify People in Photo")
            print("-" * 70)
            image_path = input("Path to image to analyze: ").strip()

            if not os.path.exists(image_path):
                print(f"❌ Image not found at {image_path}")
                continue

            print("\n⏳ Analyzing...")
            result = identify_person_in_image(image_path)

            print("\n" + "=" * 70)
            print("IDENTIFICATION RESULTS")
            print("=" * 70)
            if isinstance(result, dict) and "error" in result:
                print(f"❌ {result['error']}")
            else:
                print(result)
            print("=" * 70)

        elif choice == "3":
            list_database_people()

        elif choice == "4":
            print("\n🗑️  Remove Person from Database")
            print("-" * 70)
            name = input("Name to remove: ").strip()
            remove_person_from_database(name)

        elif choice == "5":
            print(f"\n💾 Database saved at: {os.path.abspath(DATABASE_FILE)}")
            db = load_database()
            print(f"Contains {len(db['people'])} people")

        elif choice == "6":
            print("\nGoodbye!")
            break

        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()

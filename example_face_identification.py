#!/usr/bin/env python3
"""
Example: Setting up and using face identification for personal photo organization.

This demonstrates how to build a database and identify people in photos.
"""

import os

print("=" * 70)
print("Face Identification Example")
print("=" * 70)
print("\n⚠️  PRIVACY NOTICE: This example is for personal use only.")
print("Get consent from everyone before adding them to your database.\n")
print("=" * 70)

print("\n" + "=" * 70)
print("Step 1: Build Your Reference Database")
print("=" * 70)
print("""
To identify people, you first need reference images.

Run this command:
    python face_identification.py

Then choose option 1 and add people:

Example interaction:
    What would you like to do? 1
    Person's name: Alice
    Path to reference image: ./photos/alice_reference.jpg
    Notes (optional): My sister
    Do you have Alice's consent? yes
    ✅ Added Alice to database!

Repeat for each person you want to identify (Bob, Charlie, etc.)

Best practices for reference images:
- Clear, well-lit face photo
- Front-facing or slight angle
- Good resolution
- Recent photo
""")

print("\n" + "=" * 70)
print("Step 2: Verify Your Database")
print("=" * 70)
print("""
Check who's in your database:
    python face_identification.py
    Choose option 3 (View database)

You should see a list of all people with their reference images.
""")

print("\n" + "=" * 70)
print("Step 3: Identify People in New Photos")
print("=" * 70)
print("""
Now you can identify people in any photo!

Method 1 - Standalone Tool:
    python face_identification.py
    Choose option 2 (Identify people in a photo)
    Enter image path: ./photos/party_2024.jpg

    Result:
    PERSON 1:
    - Match: Alice
    - Confidence: High
    - Reasoning: Face shape, eye color, and hairstyle match Alice's reference

    PERSON 2:
    - Match: Bob
    - Confidence: Medium
    - Reasoning: Similar facial features but different lighting

    PERSON 3:
    - Match: Unknown
    - Confidence: N/A
    - Reasoning: No match in database

Method 2 - Using the AI Agent:
    python agent.py

    In interactive mode:
    You: Who is in ./photos/party_2024.jpg?

    The agent will automatically use the identify_person tool!
""")

print("\n" + "=" * 70)
print("Step 4: Programmatic Usage")
print("=" * 70)
print("""
You can also use it in your own Python scripts:

    from agent import run_agent

    # Identify people in a photo
    result = run_agent("Who is in the photo at ./my_photo.jpg?")
    print(result)

    # The agent autonomously decides to use identify_person tool
    # and returns results with names and confidence levels
""")

print("\n" + "=" * 70)
print("Complete Workflow Example")
print("=" * 70)
print("""
Scenario: Organizing photos from a family reunion

1. Get consent from family members
   "Hey everyone, I'm organizing our reunion photos. Can I use a photo
    of you to help automatically tag you in the photos? You can ask me
    to delete your data anytime."

2. Build database
   python face_identification.py
   - Add Mom (./mom_ref.jpg)
   - Add Dad (./dad_ref.jpg)
   - Add Sister (./sister_ref.jpg)
   - Add Brother (./brother_ref.jpg)
   - Add Grandma (./grandma_ref.jpg)

3. Process reunion photos
   for photo in reunion_photos:
       result = identify_people(photo)
       tag_photo_with_names(photo, result)

4. Result: All your reunion photos are now organized by who's in them!
""")

print("\n" + "=" * 70)
print("Example Code: Batch Processing Photos")
print("=" * 70)
print("""
Here's a script to identify people in multiple photos:

```python
from agent import run_agent
import os

# Directory containing photos to process
photo_dir = "./my_photos"

for filename in os.listdir(photo_dir):
    if filename.endswith(('.jpg', '.png', '.jpeg')):
        photo_path = os.path.join(photo_dir, filename)

        print(f"\\nProcessing: {filename}")
        result = run_agent(f"Who is in {photo_path}?")
        print(result)
        print("-" * 60)
```

This will go through all photos and identify people in each one.
""")

print("\n" + "=" * 70)
print("Privacy & Consent Checklist")
print("=" * 70)
print("""
Before using face identification, ensure:

[ ] I have explicit consent from everyone I'm adding
[ ] I've explained what data I'm storing (photo + description)
[ ] I've explained how it will be used (identify them in my photos)
[ ] I've told them they can request deletion anytime
[ ] I'm only using this for my personal photos
[ ] I'm keeping the database secure
[ ] I will honor any deletion requests immediately
[ ] I understand this is not for commercial or public use
""")

print("\n" + "=" * 70)
print("Ready to Start!")
print("=" * 70)
print("""
Run these commands to get started:

1. Build your database:
   python face_identification.py

2. Test identification:
   python face_identification.py
   (Choose option 2)

3. Use with the AI agent:
   python agent.py
   Then ask: "Who is in ./photo.jpg?"

For detailed information, see:
- FACE_IDENTIFICATION_GUIDE.md (complete documentation)
- face_identification.py (the tool itself)
""")

print("\n" + "=" * 70)
print("Quick Reference")
print("=" * 70)
print("""
Common commands:

Add person:         python face_identification.py → Option 1
Identify in photo:  python face_identification.py → Option 2
View database:      python face_identification.py → Option 3
Remove person:      python face_identification.py → Option 4

Using the agent:    python agent.py
                    You: Who is in ./photo.jpg?
""")

# Check if database exists
if os.path.exists("face_database.json"):
    import json
    with open("face_database.json") as f:
        db = json.load(f)
    print(f"\n✅ Database found with {len(db.get('people', []))} people")
else:
    print("\n⚠️  No database found yet. Run: python face_identification.py")

print("\n" + "=" * 70)

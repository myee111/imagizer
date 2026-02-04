#!/usr/bin/env python3
"""
Demo of the face identification interface (simulated, no API calls).
"""

import time

def print_header(text):
    print("\n" + "=" * 70)
    print(text)
    print("=" * 70)

def simulate_typing(text, delay=0.03):
    """Simulate typing effect."""
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

print_header("Face Identification System - Interface Demo")

print("\n🎬 This demo shows what the interface looks like")
print("(Simulated - no actual API calls or photos needed)")

time.sleep(1)

print_header("Scenario: Adding Your First Person to the Database")

print("\nYou run: python face_identification.py\n")
time.sleep(1)

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

time.sleep(2)

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

print("\nYour choice (1-6): 1")
time.sleep(1)

print("\n📸 Add Person to Database")
print("-" * 70)
print("Person's name: Alice")
time.sleep(0.5)
print("Path to reference image (clear face photo): ./photos/alice.jpg")
time.sleep(0.5)
print("Notes (relationship, etc.) [optional]: My sister")
time.sleep(0.5)
print("Do you have Alice's consent to add them? (yes/no): yes")
time.sleep(1)

print("\nAnalyzing reference image for Alice...")
time.sleep(2)

print("✅ Added Alice to database!")
print("   Reference image: ./photos/alice.jpg")

time.sleep(2)

print_header("Scenario: Identifying People in a Photo")

print("\nYou choose: 2. Identify people in a photo\n")
time.sleep(1)

print("🔍 Identify People in Photo")
print("-" * 70)
print("Path to image to analyze: ./photos/party_2024.jpg")
time.sleep(1)

print("\n⏳ Analyzing...")
time.sleep(2)
print("Comparing against 3 people in database...")
time.sleep(2)

print("\n" + "=" * 70)
print("IDENTIFICATION RESULTS")
print("=" * 70)

simulate_typing("\nPERSON 1 IN IMAGE:", 0.05)
simulate_typing("- Description: Person on the left with brown hair, wearing a blue shirt", 0.02)
simulate_typing("- Match: Alice", 0.05)
simulate_typing("- Confidence: High", 0.05)
simulate_typing("- Reasoning: Face shape, eye color, hairstyle, and smile match Alice's", 0.02)
simulate_typing("  reference image very closely. The blue shirt also matches recent photos.", 0.02)

time.sleep(1)

simulate_typing("\nPERSON 2 IN IMAGE:", 0.05)
simulate_typing("- Description: Person in the center with glasses, dark hair", 0.02)
simulate_typing("- Match: Bob", 0.05)
simulate_typing("- Confidence: Medium", 0.05)
simulate_typing("- Reasoning: Similar facial structure and glasses match Bob, but the", 0.02)
simulate_typing("  lighting is different and the angle is not optimal, so some uncertainty.", 0.02)

time.sleep(1)

simulate_typing("\nPERSON 3 IN IMAGE:", 0.05)
simulate_typing("- Description: Person on the right with blonde hair, smiling", 0.02)
simulate_typing("- Match: Unknown", 0.05)
simulate_typing("- Confidence: N/A", 0.05)
simulate_typing("- Reasoning: No match found in database. This person is not in your", 0.02)
simulate_typing("  reference collection. Consider adding them if appropriate (with consent).", 0.02)

print("=" * 70)

time.sleep(2)

print_header("Using with the AI Agent")

print("\nYou can also use the main AI agent:")
print("You run: python agent.py\n")
time.sleep(1)

print("=" * 70)
print("AI Agent powered by Claude with Vision")
print("=" * 70)
print("\nInteractive mode - type 'quit' to exit")
print("To analyze an image, type: image:/path/to/image.jpg What do you see?")
print("=" * 70)

time.sleep(1)

print("\nYou: Who is in ./photos/family_reunion.jpg?")
time.sleep(1)

print("\n" + "=" * 60)
print("User: Who is in ./photos/family_reunion.jpg?")
print("=" * 60)
print("\nTurn 1:")
print("Stop reason: tool_use")
print("  Using tool: identify_person")
print('  Input: {')
print('    "image_path": "./photos/family_reunion.jpg"')
print('  }')
time.sleep(2)

print("  Result: Identification results (comparing against 3 people in database):")
print()
print("  PERSON 1:")
print("  - Match: Alice")
print("  - Confidence: High")
print()
print("  PERSON 2:")
print("  - Match: Bob")
print("  - Confidence: High")
print()
print("  PERSON 3:")
print("  - Match: Unknown")
print()

time.sleep(2)

print("\nTurn 2:")
print("Stop reason: end_turn")
print("Final response: I found 3 people in the photo. I was able to identify")
print("Alice (high confidence) and Bob (high confidence) from your database.")
print("There's also one person who isn't in your database yet.")
print()

time.sleep(2)

print_header("Summary")

print("""
✅ What You Just Saw:

1. Building a Database:
   - Added Alice with a reference photo (with consent)
   - System analyzed her facial features
   - Stored description in local database

2. Identifying People:
   - Analyzed a party photo
   - Found 3 people
   - Matched 2 against database (Alice: high, Bob: medium)
   - Identified 1 unknown person

3. AI Agent Integration:
   - Asked "Who is in this photo?"
   - Agent autonomously used identify_person tool
   - Received results and explained findings

🎯 Key Features:

• Privacy-First: All data stored locally, consent required
• Confidence Levels: High/Medium/Low for each match
• Autonomous: Agent decides when to use face identification
• Flexible: Standalone tool or integrated with AI agent
• Transparent: See exactly how matches are made

📚 Ready to Use:

1. Set up API key: cp .env.example .env (add your key)
2. Run: python face_identification.py
3. Add people (with consent)
4. Start identifying!

For real usage with your own photos, you'll need:
- Anthropic API key
- Photos to analyze
- Consent from people you're adding
""")

print("=" * 70)
print("Demo Complete! The system is ready for real use.")
print("=" * 70)

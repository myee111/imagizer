#!/usr/bin/env python3
"""
Quick examples of people recognition capabilities.
Replace the image paths with your own images to test.
"""

from agent import run_agent

print("=" * 70)
print("People Recognition Examples")
print("=" * 70)
print("\nThese examples show how the agent autonomously uses the")
print("analyze_people tool when asked about people in images.")
print("\nReplace the paths below with your own images to test.\n")
print("=" * 70)

# Example 1: Count people
print("\n1. COUNT PEOPLE")
print("-" * 70)
print("Question: 'How many people are in this image?'")
print("-" * 70)
# Uncomment and add your image path:
# result = run_agent("How many people are in the image at ./your_image.jpg?")
# print(result)
print("(Add your image path in the code to test)")

# Example 2: Describe activities
print("\n2. DESCRIBE ACTIVITIES")
print("-" * 70)
print("Question: 'What are the people doing?'")
print("-" * 70)
# Uncomment and add your image path:
# result = run_agent("What are the people doing in ./your_image.jpg?")
# print(result)
print("(Add your image path in the code to test)")

# Example 3: Analyze facial expressions
print("\n3. FACIAL EXPRESSIONS")
print("-" * 70)
print("Question: 'What emotions do you see in the faces?'")
print("-" * 70)
# Uncomment and add your image path:
# result = run_agent("What facial expressions and emotions do you see in ./your_image.jpg?")
# print(result)
print("(Add your image path in the code to test)")

# Example 4: Describe clothing
print("\n4. CLOTHING & APPEARANCE")
print("-" * 70)
print("Question: 'Describe what the people are wearing'")
print("-" * 70)
# Uncomment and add your image path:
# result = run_agent("Describe the clothing and appearance of people in ./your_image.jpg")
# print(result)
print("(Add your image path in the code to test)")

# Example 5: Group dynamics
print("\n5. GROUP DYNAMICS")
print("-" * 70)
print("Question: 'What's the group dynamic and social context?'")
print("-" * 70)
# Uncomment and add your image path:
# result = run_agent("Analyze the group dynamics and interactions in ./your_image.jpg")
# print(result)
print("(Add your image path in the code to test)")

# Example 6: Detailed analysis
print("\n6. DETAILED PERSON-BY-PERSON")
print("-" * 70)
print("Question: 'Give me a detailed description of each person'")
print("-" * 70)
# Uncomment and add your image path:
# result = run_agent("Provide a detailed analysis of each person in ./your_image.jpg")
# print(result)
print("(Add your image path in the code to test)")

# Example 7: Custom specific question
print("\n7. CUSTOM QUESTION")
print("-" * 70)
print("Question: 'Are the people indoors or outdoors?'")
print("-" * 70)
# Uncomment and add your image path:
# result = run_agent("Are the people in ./your_image.jpg indoors or outdoors? Describe the setting.")
# print(result)
print("(Add your image path in the code to test)")

print("\n" + "=" * 70)
print("How It Works")
print("=" * 70)
print("""
The agent autonomously decides which tool to use based on your question:

1. You ask: "How many people are in this image?"
2. Agent thinks: "I need to analyze people in an image"
3. Agent uses: analyze_people tool with analysis_type='count'
4. Tool executes: Analyzes the image with Claude Vision
5. Agent responds: With the count and description

You don't need to specify which tool to use - the agent figures it out!
""")

print("=" * 70)
print("Try It Yourself")
print("=" * 70)
print("""
1. Edit this file and uncomment the examples
2. Replace './your_image.jpg' with paths to your images
3. Run: python example_people_recognition.py

Or use interactive mode:
    python agent.py
    Then: image:./your_photo.jpg How many people are here?

Or use the dedicated tool:
    python people_recognition.py
""")

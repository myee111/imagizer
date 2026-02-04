#!/usr/bin/env python3
"""
Quick demonstration of agent capabilities including image recognition.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# Check if API key is set
if not os.environ.get("ANTHROPIC_API_KEY"):
    print("=" * 60)
    print("ERROR: ANTHROPIC_API_KEY not found!")
    print("=" * 60)
    print("\nPlease set up your API key:")
    print("1. Copy .env.example to .env")
    print("2. Edit .env and add your Anthropic API key")
    print("3. Get your API key from: https://console.anthropic.com/")
    print("\nThen run this script again.")
    exit(1)

from agent import run_agent

print("=" * 60)
print("AI Agent Demo - Powered by Claude")
print("=" * 60)

# Demo 1: Simple tool use
print("\n1. Using the calculator tool:")
print("-" * 60)
run_agent("What is 42 * 137?")

# Demo 2: Multi-tool reasoning
print("\n2. Multi-step reasoning:")
print("-" * 60)
run_agent("If the temperature in Paris is 20°C, what is that in Fahrenheit? Use the formula (C × 9/5) + 32")

# Demo 3: Image analysis tool
print("\n3. Image analysis tool (autonomous decision):")
print("-" * 60)
print("The agent can autonomously decide to use the analyze_image tool")
print("when you ask it to analyze an image file.")
print("\nExample: 'Please analyze the image at ./photo.jpg'")
print("The agent will use the analyze_image tool on its own!")

print("\n" + "=" * 60)
print("Demo complete!")
print("=" * 60)
print("\nTry the full agent with: python agent.py")
print("Try image recognition with: python image_recognition_example.py")

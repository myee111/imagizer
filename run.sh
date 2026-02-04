#!/bin/bash
# Quick launcher for imagizer scripts

source venv/bin/activate

echo "=================================="
echo "Imagizer - Quick Launcher"
echo "=================================="
echo ""
echo "Current provider: $(grep CLAUDE_PROVIDER .env | cut -d'=' -f2)"
echo ""
echo "Choose a script:"
echo "  1) Image Recognition (analyze any image)"
echo "  2) People Recognition (detect people)"
echo "  3) Face Identification (identify known people)"
echo "  4) AI Agent (full capabilities)"
echo "  5) Test Interface (verify setup)"
echo ""
read -p "Enter choice (1-5): " choice

case $choice in
    1)
        echo ""
        echo "Starting Image Recognition..."
        python image_recognition_example.py
        ;;
    2)
        echo ""
        echo "Starting People Recognition..."
        python people_recognition.py
        ;;
    3)
        echo ""
        echo "Starting Face Identification..."
        python face_identification.py
        ;;
    4)
        echo ""
        echo "Starting AI Agent..."
        python agent.py
        ;;
    5)
        echo ""
        echo "Running Tests..."
        python test_interface.py
        ;;
    *)
        echo "Invalid choice"
        exit 1
        ;;
esac

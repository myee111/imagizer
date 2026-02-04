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
echo "  6) Authenticate with Vertex AI"
echo ""
read -p "Enter choice (1-6): " choice

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
    6)
        echo ""
        echo "=================================="
        echo "Vertex AI Authentication"
        echo "=================================="
        echo ""

        # Check current authentication status
        echo "Checking current authentication status..."
        if gcloud auth application-default print-access-token &>/dev/null; then
            echo "✅ Already authenticated with Google Cloud"
            echo ""
            echo "Current configuration:"
            echo "  Project: $(gcloud config get-value project 2>/dev/null)"
            echo "  Account: $(gcloud config get-value account 2>/dev/null)"

            # Check for quota project in ADC credentials
            adc_file="$HOME/.config/gcloud/application_default_credentials.json"
            if [ -f "$adc_file" ]; then
                quota_proj=$(grep -o '"quota_project_id"[[:space:]]*:[[:space:]]*"[^"]*"' "$adc_file" 2>/dev/null | cut -d'"' -f4)
                if [ -n "$quota_proj" ]; then
                    echo "  Quota Project: $quota_proj"
                fi
            fi
            echo ""

            # Check Vertex AI quotas
            echo "Checking Vertex AI status..."
            project_id=$(gcloud config get-value project 2>/dev/null)
            region=$(grep VERTEX_REGION .env | cut -d'=' -f2)

            # Check if Vertex AI API is enabled
            if gcloud services list --enabled --project="$project_id" 2>/dev/null | grep -q "aiplatform.googleapis.com"; then
                echo "✅ Vertex AI API is enabled"
                echo "   Region: $region"
                echo ""

                # Try to get quota information
                echo "Quota Information:"
                echo "─────────────────────────────────────────"

                quota_output=$(gcloud services quota list \
                    --service=aiplatform.googleapis.com \
                    --project="$project_id" \
                    --format="value(metric.displayName,consumerQuotaLimits.quotaBuckets.defaultLimit,usage)" \
                    2>/dev/null | grep -i "predict\|request" | head -5)

                if [ -n "$quota_output" ]; then
                    echo "$quota_output" | while IFS=$'\t' read -r metric limit usage; do
                        echo "  $metric"
                        echo "    Limit: ${limit:-N/A}"
                        echo "    Usage: ${usage:-0}"
                        echo ""
                    done
                else
                    echo "  ℹ️  Detailed quota requires additional permissions"
                    echo "  View quotas in Cloud Console:"
                    echo "  https://console.cloud.google.com/apis/api/aiplatform.googleapis.com/quotas?project=$project_id"
                fi
                echo "─────────────────────────────────────────"

            else
                echo "⚠️  Vertex AI API is NOT enabled for this project"
                echo ""
                read -p "Enable Vertex AI API now? (y/n): " enable
                if [[ "$enable" =~ ^[Yy]$ ]]; then
                    echo "Enabling Vertex AI API..."
                    gcloud services enable aiplatform.googleapis.com --project="$project_id"
                    echo "✅ Vertex AI API enabled"
                else
                    echo "⚠️  You'll need to enable the API before using Vertex AI"
                fi
            fi

            echo ""
            read -p "Re-authenticate anyway? (y/n): " reauth
            if [[ ! "$reauth" =~ ^[Yy]$ ]]; then
                echo "Keeping current authentication."
                exit 0
            fi
        else
            echo "❌ Not currently authenticated"
        fi

        echo ""
        echo "Starting authentication process..."
        echo "This will open a browser window for you to sign in."
        echo ""

        # Ask about quota project
        env_project=$(grep VERTEX_PROJECT_ID .env | cut -d'=' -f2)
        echo "Quota Project Configuration:"
        echo "─────────────────────────────────────────"
        echo "The quota project determines which GCP project is billed"
        echo "for API usage and quotas. This is typically the same as"
        echo "your Vertex AI project."
        echo ""
        echo "  Your .env project: $env_project"
        echo ""
        read -p "Use a different quota project? (leave empty to use $env_project): " quota_project

        if [ -z "$quota_project" ]; then
            quota_project="$env_project"
        fi

        echo ""
        echo "Authenticating with quota project: $quota_project"

        # Authenticate
        gcloud auth application-default login --quota-project-id="$quota_project"

        if [ $? -eq 0 ]; then
            echo ""
            echo "✅ Authentication successful!"
            echo ""
            echo "Current configuration:"
            echo "  Project: $(gcloud config get-value project 2>/dev/null)"
            echo "  Account: $(gcloud config get-value account 2>/dev/null)"
            echo "  Quota Project: $quota_project"
            echo ""
            echo "Your .env file is configured for:"
            echo "  Project: $(grep VERTEX_PROJECT_ID .env | cut -d'=' -f2)"
            echo "  Region: $(grep VERTEX_REGION .env | cut -d'=' -f2)"
            echo ""

            # Verify project matches
            current_project=$(gcloud config get-value project 2>/dev/null)
            env_project=$(grep VERTEX_PROJECT_ID .env | cut -d'=' -f2)

            if [ "$current_project" != "$env_project" ]; then
                echo "⚠️  WARNING: gcloud project ($current_project) doesn't match .env ($env_project)"
                echo ""
                read -p "Switch gcloud project to match .env? (y/n): " switch
                if [[ "$switch" =~ ^[Yy]$ ]]; then
                    gcloud config set project "$env_project"
                    echo "✅ Project switched to $env_project"
                    current_project="$env_project"
                fi
            fi

            # Check quotas after authentication
            echo ""
            echo "Checking Vertex AI status..."
            region=$(grep VERTEX_REGION .env | cut -d'=' -f2)

            # Check if Vertex AI API is enabled
            if gcloud services list --enabled --project="$current_project" 2>/dev/null | grep -q "aiplatform.googleapis.com"; then
                echo "✅ Vertex AI API is enabled"
                echo "   Region: $region"
                echo ""

                # Try to get quota information
                echo "Quota Information:"
                echo "─────────────────────────────────────────"

                quota_output=$(gcloud services quota list \
                    --service=aiplatform.googleapis.com \
                    --project="$current_project" \
                    --format="value(metric.displayName,consumerQuotaLimits.quotaBuckets.defaultLimit,usage)" \
                    2>/dev/null | grep -i "predict\|request" | head -5)

                if [ -n "$quota_output" ]; then
                    echo "$quota_output" | while IFS=$'\t' read -r metric limit usage; do
                        echo "  $metric"
                        echo "    Limit: ${limit:-N/A}"
                        echo "    Usage: ${usage:-0}"
                        echo ""
                    done
                else
                    echo "  ℹ️  Detailed quota requires additional permissions"
                    echo "  View quotas in Cloud Console:"
                    echo "  https://console.cloud.google.com/apis/api/aiplatform.googleapis.com/quotas?project=$current_project"
                fi
                echo "─────────────────────────────────────────"

            else
                echo "⚠️  Vertex AI API is NOT enabled"
                echo ""
                read -p "Enable Vertex AI API now? (y/n): " enable
                if [[ "$enable" =~ ^[Yy]$ ]]; then
                    echo "Enabling Vertex AI API..."
                    gcloud services enable aiplatform.googleapis.com --project="$current_project"
                    if [ $? -eq 0 ]; then
                        echo "✅ Vertex AI API enabled successfully"
                    else
                        echo "❌ Failed to enable API. Check your permissions."
                    fi
                fi
            fi

            echo ""
            echo "You can now run the application with Vertex AI!"
        else
            echo ""
            echo "❌ Authentication failed. Please try again."
            exit 1
        fi
        ;;
    *)
        echo "Invalid choice"
        exit 1
        ;;
esac

#!/usr/bin/env python3
"""
Simple script to run the Sentiment Analysis Application
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from app import app
    
    print("🚀 Starting Sentiment Analysis Application...")
    print("📍 API endpoints:")
    print("  - Main interface: http://localhost:5000/")
    print("  - Analyze sentiment: POST /api/analyze")
    print("  - Batch analysis: POST /api/batch-analyze")
    print("  - Health check: GET /api/health")
    print("\n💡 Example curl commands:")
    print("  curl -X POST http://localhost:5000/api/analyze -H 'Content-Type: application/json' -d '{\"text\": \"I love this product!\"}'")
    print("  curl -X POST http://localhost:5000/api/batch-analyze -H 'Content-Type: application/json' -d '{\"texts\": [\"Great!\", \"Terrible.\", \"Okay.\"]}'")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
    
except ImportError as e:
    print(f"❌ Error importing app: {e}")
    print("💡 Make sure all required packages are installed:")
    print("  pip install -r requirements.txt")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error starting application: {e}")
    sys.exit(1)
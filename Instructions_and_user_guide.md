# Sentiment Analysis Application

A Flask-based web application for analyzing sentiment in text using NLTK's VADER sentiment analyzer with enhanced logic for handling complex cases like sarcasm, negation, idioms, and slang.

## Prerequisites

- Python 3.8 or higher
- pip package manager

## Installation

1. **Download and extract the repository**

- Extract the project files to your desired directory
- In Vscode open project folder and terminal/command prompt

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

1. **Start the Flask server**
   ```bash
   python app.py
   ```

2. **Open in browser**
   Navigate to: `http://localhost:5000`

## Using the Web Interface

### Option 1: Direct Text Input
1. Enter text in the text area
2. Click "Analyze Sentiment"
3. View results and visualization

### Option 2: Upload File
1. Click "Upload Text File"
2. Select a `.txt` file
3. Click "Analyze Sentiment"
4. View results and visualization

## Sample Files

Two sample files are included for testing:

1. **sample_reviews.txt** - 20 general reviews with various sentiments, sarcasm, idioms, and slang
2. **sample_reviews_healthcare.txt** - 20 healthcare-specific reviews

## Project Structure

```
.
├── app.py                      # Main Flask application
├── test_app.py                 # Comprehensive test suite (350+ lines)
├── run_app.py                  # Application runner
├── requirements.txt            # Python dependencies
├── sample_reviews.txt          # General test reviews
└── README.md                   # General Readme file
```
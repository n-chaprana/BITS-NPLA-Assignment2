# Sentiment Analysis Application

A comprehensive web-based sentiment analysis application built with Flask and NLTK, featuring real-time sentiment detection, visualization, and batch processing capabilities.

## 🚀 Features

### Core Functionality
- **Real-time Sentiment Analysis**: Analyze text sentiment in real-time using NLTK's VADER model
- **Text Preprocessing**: Advanced preprocessing including URL removal, email filtering, and lemmatization
- **Multiple Input Methods**: Text input and file upload support (.txt files)
- **Sentiment Visualization**: Interactive bar charts and color-coded sentiment labels
- **Batch Processing**: Analyze multiple texts simultaneously

### Web Interface
- **Responsive Design**: Mobile-friendly interface with modern UI
- **Real-time Updates**: Live sentiment analysis results
- **File Upload**: Support for text file uploads
- **Clear Visualization**: Color-coded sentiment display with confidence scores

### API Endpoints
- `GET /` - Main web interface
- `POST /api/analyze` - Single text sentiment analysis
- `POST /api/batch-analyze` - Batch sentiment analysis
- `GET /api/health` - Health check endpoint

## 📋 Requirements

- Python 3.8+
- Flask 3.0.0
- NLTK 3.8.1
- Chart.js (for frontend visualization)

## 🛠️ Installation

1. **Clone or download the project files**
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the application**:
   ```bash
   python run_app.py
   ```
4. **Open your browser** and navigate to `http://localhost:5000`

## 📖 Usage

### Web Interface
1. Open the application in your browser
2. Enter text in the text area or upload a text file
3. Click "Analyze Sentiment" to see results
4. View sentiment scores and visualization

### API Usage

#### Single Text Analysis
```bash
curl -X POST http://localhost:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "I love this product!"}'
```

#### Batch Analysis
```bash
curl -X POST http://localhost:5000/api/batch-analyze \
  -H "Content-Type: application/json" \
  -d '{"texts": ["Great!", "Terrible.", "Okay."]}'
```

## 🏗️ Project Structure

```
NLPA/
├── app.py              # Main Flask application
├── run_app.py          # Application runner
├── test_app.py         # Test suite
├── requirements.txt    # Python dependencies
├── README.md          # This file
└── nlpa_assignment2.py # Original assignment code
```

## 🧪 Testing

Run the test suite:
```bash
python test_app.py
```

## 📊 Sentiment Analysis Details

### Preprocessing Pipeline
1. **Text Cleaning**: Remove URLs, emails, and special characters
2. **Tokenization**: Break text into individual words
3. **Stopword Removal**: Filter out common words
4. **Lemmatization**: Reduce words to their base form
5. **Sentiment Analysis**: Apply VADER model for sentiment scoring

### Output Format
```json
{
  "neg": 0.0,
  "neu": 0.0,
  "pos": 0.0,
  "compound": 0.0,
  "sentiment_label": "positive|negative|neutral",
  "confidence": 0.0,
  "original_text": "Original input text",
  "processed_text": "Preprocessed text"
}
```

## 🔧 Configuration

The application uses the following configuration:
- **Host**: 0.0.0.0 (accessible from any IP)
- **Port**: 5000
- **Debug Mode**: Enabled for development
- **CORS**: Enabled for frontend communication

## 🚀 Deployment

For production deployment:
1. Set `debug=False` in `app.run()`
2. Use a production WSGI server (e.g., Gunicorn)
3. Configure proper SSL/TLS certificates
4. Set up a reverse proxy (e.g., Nginx)

## 📈 Performance

- **Real-time Processing**: Sub-second response times for single texts
- **Batch Processing**: Efficient handling of multiple texts
- **Memory Efficient**: Optimized for handling large volumes of text
- **Scalable**: Designed for horizontal scaling

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for your changes
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Troubleshooting

### Common Issues

1. **NLTK Data Not Downloaded**: The application automatically downloads required NLTK data on startup
2. **Port Already in Use**: Change the port number in `run_app.py`
3. **Missing Dependencies**: Run `pip install -r requirements.txt`

### Getting Help

- Check the console output for error messages
- Verify all dependencies are installed
- Ensure the correct Python version is being used

## 📞 Contact

For questions or support, please contact the development team.

---

**Built with ❤️ using Flask and NLTK**
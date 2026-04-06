# Mental Health Detection Model

A full-stack application that detects mental health conditions from text using a fine-tuned BERT model. The system includes a React frontend with a chat interface and a FastAPI backend serving the ML model.

## Features

- Real-time mental health condition detection from user text
- 7 condition categories: Anxiety, Bipolar, Depression, Normal, Personality Disorder, Stress, Suicidal
- Confidence scores for predictions
- Modern chat interface with responsive design
- GPU acceleration support (when available)

## Project Structure

```
Mental-Health-Detection-Model/
├── src/                    # React frontend (Vite + TypeScript)
│   ├── App.tsx             # Main chat interface component
│   ├── App.css             # Styles
│   └── main.tsx            # Entry point
├── main/                   # Backend and ML model
│   ├── api.py              # FastAPI server
│   ├── saved_model/        # Fine-tuned BERT model
│   ├── requirements.txt    # Python dependencies
│   └── cleanData.csv       # Training dataset
├── public/                 # Static assets
└── package.json            # Node.js dependencies
```

## Prerequisites

- Node.js 18+
- Python 3.10+
- CUDA-compatible GPU (optional, for faster inference)

## Installation

### Backend Setup

```bash
cd main
python -m venv venv

# Windows
.\venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

pip install -r requirements.txt
```

Note: For GPU support, install PyTorch with CUDA:
```bash
pip install torch --index-url https://download.pytorch.org/whl/cu128
```

### Frontend Setup

```bash
npm install
```

## Running the Application

### Start the Backend Server

```bash
cd main
.\venv\Scripts\activate  # Windows
uvicorn api:app --reload --port 8000
```

The API will be available at `http://localhost:8000`

### Start the Frontend

```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`

## API Endpoints

### POST /chat

Analyze text for mental health indicators.

**Request:**
```json
{
  "message": "I feel anxious and can't sleep at night"
}
```

**Response:**
```json
{
  "response": "I sense some anxiety in what you've shared...",
  "detected_condition": "Anxiety",
  "confidence": 0.9234
}
```

### GET /health

Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true
}
```

## Model Information

- Architecture: BERT for Sequence Classification
- Base Model: bert-base-uncased
- Classes: 7 mental health conditions
- Input: Text up to 512 tokens

## Tech Stack

**Frontend:**
- React 18
- TypeScript
- Tailwind CSS
- Vite

**Backend:**
- FastAPI
- PyTorch
- Hugging Face Transformers

## Disclaimer

This tool is for educational and informational purposes only. It is not a substitute for professional mental health diagnosis or treatment. If you or someone you know is struggling with mental health issues, please seek help from a qualified healthcare provider.

## License

MIT License
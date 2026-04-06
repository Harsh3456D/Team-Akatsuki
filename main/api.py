"""
FastAPI wrapper for the Mental Health Detection BERT model.
Run with: uvicorn api:app --reload --port 8000
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

# Initialize FastAPI app
app = FastAPI(
    title="Mental Health Detection API",
    description="API for detecting mental health conditions from text",
    version="1.0.0"
)

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Label mapping (from training data)
LABEL_MAP = {
    0: "Anxiety",
    1: "Bipolar",
    2: "Depression",
    3: "Normal",
    4: "Personality disorder",
    5: "Stress",
    6: "Suicidal"
}

# Response messages for each condition
RESPONSE_MESSAGES = {
    "Anxiety": "I sense some anxiety in what you've shared. It's okay to feel this way. Consider taking deep breaths and grounding yourself in the present moment.",
    "Bipolar": "I notice patterns that might indicate mood fluctuations. It's important to maintain regular routines and consider speaking with a mental health professional.",
    "Depression": "I hear that you're going through a difficult time. Please remember you're not alone. Reaching out to a counselor or trusted person can help.",
    "Normal": "It sounds like you're doing well! Keep maintaining your positive outlook and self-care habits.",
    "Personality disorder": "What you're experiencing sounds challenging. Professional support can provide helpful coping strategies tailored to your needs.",
    "Stress": "It seems like you're under some stress. Remember to take breaks, practice self-care, and don't hesitate to ask for support when needed.",
    "Suicidal": "I'm concerned about what you've shared. Please know that help is available. Consider reaching out to a crisis helpline or mental health professional immediately. You matter."
}

# Load model and tokenizer on startup
model = None
tokenizer = None


@app.on_event("startup")
async def load_model():
    global model, tokenizer
    model_path = "./saved_model"
    
    print("Loading model and tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForSequenceClassification.from_pretrained(model_path)
    model.eval()
    
    # Use GPU if available
    if torch.cuda.is_available():
        model.cuda()
        print("Model loaded on GPU")
    else:
        print("Model loaded on CPU")


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str
    detected_condition: str
    confidence: float


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Process a chat message and return mental health analysis.
    """
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    
    if model is None or tokenizer is None:
        raise HTTPException(status_code=503, detail="Model not loaded yet")
    
    # Tokenize input
    inputs = tokenizer(
        request.message,
        return_tensors="pt",
        truncation=True,
        max_length=512,
        padding=True
    )
    
    # Move to GPU if available
    if torch.cuda.is_available():
        inputs = {k: v.cuda() for k, v in inputs.items()}
    
    # Get prediction
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        probabilities = torch.softmax(logits, dim=-1)
        predicted_class = torch.argmax(probabilities, dim=-1).item()
        confidence = probabilities[0][predicted_class].item()
    
    detected_condition = LABEL_MAP.get(predicted_class, "Unknown")
    response_message = RESPONSE_MESSAGES.get(detected_condition, "Thank you for sharing.")
    
    return ChatResponse(
        response=response_message,
        detected_condition=detected_condition,
        confidence=round(confidence, 4)
    )


@app.get("/health")
async def health_check():
    """Check if the API and model are running."""
    return {
        "status": "healthy",
        "model_loaded": model is not None
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

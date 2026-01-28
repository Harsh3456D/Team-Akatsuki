import torch
from torch.optim import AdamW
from torch.utils.data import Dataset, DataLoader
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from transformers import pipeline
from tqdm import tqdm

device = "cuda" if torch.cuda.is_available() else "cpu"


model = AutoModelForSequenceClassification.from_pretrained("saved_model")
tokenizer = AutoTokenizer.from_pretrained("saved_model")

model.eval()

le = LabelEncoder()
df = pd.read_csv("cleanData.csv")
df.head()
df["label"] = le.fit_transform(df["status"])
df[["status", "label"]].head()


def predict(text):
    model.eval()
    encoding = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**encoding)
        pred = torch.argmax(outputs.logits, dim=1).item()
    return le.inverse_transform([pred])[0]

while True:
    n=str(input("Enter the statement: "))
    print(predict(n))

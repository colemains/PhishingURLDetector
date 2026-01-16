import gradio as gr
import joblib
import re
from urllib.parse import urlparse

# Load model
try:
    model = joblib.load('url_model.pkl')
except FileNotFoundError:
    raise FileNotFoundError("Model file 'url_model.pkl' not found. Please ensure it's in the repository.")

def extract_features(url):
    # Add scheme if missing for proper parsing
    if not url or not isinstance(url, str):
        url = ""
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
    
    features = {}
    features['length'] = len(url)
    features['dots'] = url.count('.')
    features['https'] = 1 if url.startswith('https') else 0
    
    # Safe URL parsing with error handling
    try:
        parsed = urlparse(url)
        netloc = parsed.netloc if parsed.netloc else ""
        features['ip'] = 1 if re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', netloc) else 0
    except Exception:
        features['ip'] = 0
    
    features['at'] = 1 if '@' in url else 0
    features['hyphens'] = url.count('-')
    return [list(features.values())]

def predict(url):
    if not url or url.strip() == "":
        return "Please enter a valid URL"
    
    try:
        feats = extract_features(url)
        pred = model.predict(feats)[0]
        return "Phishing Detected! 🚨" if pred == 1 else "Safe URL ✅"
    except Exception as e:
        return f"Error processing URL: {str(e)}"

# Create Gradio interface
demo = gr.Interface(
    fn=predict,
    inputs=gr.Textbox(label="Enter URL", placeholder="https://example.com"),
    outputs=gr.Textbox(label="Prediction"),
    title="AI Phishing URL Detector",
    description="Enter a URL to check if it's safe or potentially a phishing attempt.",
    examples=[
        ["https://www.google.com"],
        ["http://192.168.1.1"],
        ["https://example.com@evil.com"]
    ]
)

if __name__ == "__main__":
    demo.launch()
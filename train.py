import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib
import re
from urllib.parse import urlparse

df = pd.read_csv('phishing_urls.csv')
def extract_features(url):
    features = {}
    features['length'] = len(url)
    features['dots'] = url.count('.')
    features['https'] = 1 if url.startswith('https') else 0
    features['ip'] = 1 if re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', urlparse(url).netloc) else 0
    features['at'] = 1 if '@' in url else 0
    features['hyphens'] = url.count('-')
    return list(features.values())

X = df['url'].apply(extract_features).tolist()
y = df['label'].map({'phishing':1, 'legitimate':0})

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)
preds = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, preds))

joblib.dump(model, 'url_model.pkl')
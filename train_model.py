import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, ConfusionMatrixDisplay
import pickle
import matplotlib.pyplot as plt
import os

# Download stopwords if not present
nltk.download('stopwords', quiet=True)

def train():
    print("1. Loading dataset...")
    df = pd.read_csv('news_dataset.csv')
    print(f"Dataset loaded. Shape: {df.shape}")
    
    # Check for missing values and drop
    df.dropna(inplace=True)
    df.drop_duplicates(inplace=True)

    print("2. Text Preprocessing...")
    port_stem = PorterStemmer()
    stop_words = set(stopwords.words('english'))
    
    cleaned_texts = []
    for text in df['Text']:
        # Remove non-alphabet
        clean = re.sub('[^a-zA-Z]', ' ', text)
        # Lowercase
        clean = clean.lower()
        # Tokenize
        clean = clean.split()
        # Remove stopwords and stem
        clean = [port_stem.stem(word) for word in clean if word not in stop_words]
        # Join back
        clean = ' '.join(clean)
        cleaned_texts.append(clean)
        
    df['Cleaned_Text'] = cleaned_texts
    df.to_csv('cleaned_news_dataset.csv', index=False)
    print("Preprocessed dataset saved to cleaned_news_dataset.csv")

    print("3. Feature Extraction (TF-IDF)...")
    X = df['Cleaned_Text']
    y = df['Category']
    
    vectorizer = TfidfVectorizer(max_features=5000)
    X_vectorized = vectorizer.fit_transform(X)
    
    print("4. Train-Test Split...")
    X_train, X_test, y_train, y_test = train_test_split(X_vectorized, y, test_size=0.20, random_state=42, stratify=y)
    
    print("5. Model Training (MultinomialNB)...")
    model = MultinomialNB()
    model.fit(X_train, y_train)
    
    print("6. Model Evaluation...")
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model Accuracy: {accuracy * 100:.2f}%")
    
    report = classification_report(y_test, y_pred)
    print("Classification Report:")
    print(report)
    
    with open('classification_report.txt', 'w') as f:
        f.write(report)
        f.write(f"\n\nAccuracy: {accuracy * 100:.2f}%")
        
    cm = confusion_matrix(y_test, y_pred, labels=model.classes_)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=model.classes_)
    fig, ax = plt.subplots(figsize=(10, 8))
    disp.plot(cmap=plt.cm.Blues, ax=ax, xticks_rotation=45)
    plt.tight_layout()
    plt.savefig('confusion_matrix.png')
    print("Saved classification_report.txt and confusion_matrix.png")

    print("7. Model Saving...")
    with open('trained_model.pkl', 'wb') as f:
        pickle.dump(model, f)
    with open('vectorizer.pkl', 'wb') as f:
        pickle.dump(vectorizer, f)
    print("Saved trained_model.pkl and vectorizer.pkl")
    print("Pipeline Complete!")

if __name__ == "__main__":
    train()

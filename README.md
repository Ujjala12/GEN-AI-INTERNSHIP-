# Semantic Content Classifier using Natural Language Processing and Machine Learning

This repository contains the complete implementation of the **Semantic Content Classifier**, a desktop-based application that automatically categorizes unstructured news articles into nine predefined categories: **Business, Sports, Politics, Technology, Health, Crime, Education, Entertainment, and Weather**.

---

## 1. Project Overview
The Semantic Content Classifier demonstrates the full lifecycle of a Machine Learning application:
1. **Data Collection**: Preparing and maintaining structured/unstructured news text datasets.
2. **Data Preprocessing & Cleaning**: Tokenization, lowercase transformation, punctuation and number removal, stopword filtering, and stemming.
3. **Feature Engineering**: Transforming text to numerical feature vectors using Term Frequency-Inverse Document Frequency (TF-IDF).
4. **Model Training & Evaluation**: Training a Multinomial Naive Bayes classifier and evaluating it with classification reports and confusion matrices.
5. **Deployment**: Delivering the trained model via a Tkinter graphical user interface (GUI) desktop application featuring live clock, status tracking, and classification history logs.

---

## 2. Problem Statement
The volume of unstructured text information published online grows exponentially daily. Manually sorting through and categorizing articles, feeds, and newsletters is slow, labor-intensive, and prone to human error. Automating this process using Natural Language Processing (NLP) and supervised Machine Learning (ML) helps organize large volumes of text content efficiently and in real-time.

---

## 3. Objectives
* Automate categorization of news articles into relevant topics.
* Apply classic natural language processing pipelines (cleaning, tokenization, stopword removal, stemming).
* Map textual documents into sparse TF-IDF vector spaces.
* Train, compare, and fine-tune classifiers.
* Build a responsive GUI dashboard for easy user interaction.
* Save classification query histories locally to a CSV log.

---

## 4. Technologies Used
* **Programming Language**: Python 3.x
* **Core Libraries**:
  * `pandas` & `numpy` (data handling)
  * `scikit-learn` (vectorization, Naive Bayes model, evaluations)
  * `nltk` (natural language toolkit for stopwords and stemming)
  * `matplotlib` (plotting evaluation heatmaps)
  * `tkinter` (GUI desktop frame)
  * `pickle` (model serialization)

---

## 5. Machine Learning Workflow
```
[ Raw News Dataset ]
         │
         ▼
[ Text Data Preprocessing ] (Lowercase, Regex Clean, Tokenize, Stopwords, Stemming)
         │
         ▼
[ Feature Extraction ] (TF-IDF Vectorization)
         │
         ▼
[ Train/Test Split ] (80% Train / 20% Test)
         │
         ▼
[ Model Training ] (Multinomial Naive Bayes Classifier)
         │
         ▼
[ Model Evaluation ] (Precision, Recall, F1, Confusion Matrix)
         │
         ▼
[ Model Serialization ] (Save trained_model.pkl & vectorizer.pkl)
         │
         ▼
[ Desktop Application ] (Tkinter UI) <───> [ Local Log CSV ] (prediction_history.csv)
```

---

## 6. Preprocessing Details
Raw text is processed in order to extract standard root features:
1. **Case Conversion**: Convert all letters to lowercase.
2. **Punctuation and Numbers Removal**: Replace non-alphabetic characters with whitespace.
3. **Tokenization**: Split paragraphs/sentences into individual word units.
4. **Stopword Elimination**: Filter out high-frequency but low-semantic words (e.g., *is, the, a, of, and, in*).
5. **Stemming**: Apply NLTK's `PorterStemmer` to reduce inflections to root forms (e.g., *playing, plays, played* $\to$ *play*).

---

## 7. Model Evaluation
The classifier is trained on a balanced corpus (~50 articles per category) yielding the following outputs:
* **Accuracy**: High classification performance on testing subsets.
* **Classification Report**: Outputs precision, recall, and F1-score for each category.
* **Confusion Matrix Plot**: Saved as `confusion_matrix.png` to review true vs. predicted counts visually.

---

## 8. Desktop App Interface
The Tkinter desktop interface offers the following features:
* **Input Box**: Space to paste or write text articles.
* **Predict Action**: Cleans the input and runs the model, returning the predicted class.
* **History Log**: Opens a window showing past queries saved to `prediction_history.csv`.
* **Details Menus**: View Dataset or Model configuration properties directly.
* **Live Clock & Status Bar**: Monitors progress and current time.

---

## 9. File Structure
```
Semantic_Content_Classifier/
│
├── app.py                      # Tkinter GUI Desktop Application
├── train_model.py              # ML Training Pipeline Script
├── generate_dataset.py         # Dataset Creator (Utility)
├── news_dataset.csv            # Raw dataset
├── cleaned_news_dataset.csv    # Cleaned text dataset
├── trained_model.pkl           # Saved Naive Bayes Model
├── vectorizer.pkl              # Saved TF-IDF Vectorizer
├── classification_report.txt   # Evaluation metrics report
├── confusion_matrix.png        # Plot of Confusion Matrix
└── prediction_history.csv      # Local query history logs (App-generated)
```

---

## 10. How to Run
1. Navigate to the project folder:
   ```bash
   cd "Semantic_Content_Classifier"
   ```
2. Run the training script (optional, as models are pre-trained):
   ```bash
   python train_model.py
   ```
3. Launch the desktop GUI:
   ```bash
   python app.py
   ```

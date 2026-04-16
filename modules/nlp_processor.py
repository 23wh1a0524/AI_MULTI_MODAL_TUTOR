import nltk
import spacy
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

nlp = spacy.load("en_core_web_sm")

def preprocess_text(text):
    """Tokenize, remove stopwords, normalize text."""
    tokens = word_tokenize(text.lower())
    stop_words = set(stopwords.words('english'))
    filtered = [word for word in tokens if word.isalnum() and word not in stop_words]
    return " ".join(filtered)

def extract_topic(text):
    """Use spaCy to extract main topic/noun phrases."""
    doc = nlp(text)
    topics = [chunk.text for chunk in doc.noun_chunks]
    return topics[0] if topics else text[:50]
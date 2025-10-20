# src/inspect_vectorizer.py
import pickle, os, sys
p = ".tfidf_vectorizer.pkl"
if not os.path.exists(p):
    print("MISSING", p)
    sys.exit(0)
obj = pickle.load(open(p, "rb"))
print("TYPE:", type(obj))
print("has vocabulary_ :", hasattr(obj, "vocabulary_"))
if hasattr(obj, "vocabulary_"):
    keys = list(obj.vocabulary_.keys())
    print("vocab sample (first 20):", keys[:20])
print("has idf_ :", hasattr(obj, "idf_"))
print("has stop_words_ :", hasattr(obj, "stop_words_"))

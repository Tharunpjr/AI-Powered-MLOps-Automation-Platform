# src/index_logs.py
import json, os
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from tqdm import tqdm

EMB_FILE = ".embeddings.npy"
META_FILE = ".emb_meta.json"
VECTORIZER_FILE = ".tfidf_vectorizer.npy"  # we will save vocabulary
LOG_PATH = "logs/sample_logs.jsonl"

def load_logs(path=LOG_PATH):
    items = []
    with open(path, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            line = line.strip()
            if not line:
                continue
            try:
                j = json.loads(line)
                text = f"{j.get('ts','')}\n[{j.get('service','')}] {j.get('level')}: {j.get('msg')}"
                items.append({"id": f"log_{i}", "text": text, "meta": j})
            except Exception as e:
                print("Skipping line:", e)
    return items

def build_tfidf(items):
    texts = [it["text"] for it in items]
    vec = TfidfVectorizer(ngram_range=(1,2), max_features=2048)
    X = vec.fit_transform(texts)  # shape (N, D)
    return vec, X.toarray()

def save_index(vec, arr, items):
    # save numpy array and metadata and vectorizer vocabulary
    np.save(EMB_FILE, arr)
    metas = [{"id": it["id"], "text": it["text"], "meta": it["meta"]} for it in items]
    with open(META_FILE, "w", encoding="utf-8") as f:
        json.dump(metas, f, ensure_ascii=False, indent=2)
    # save vectorizer vocab (feature names)
    vocab = vec.get_feature_names_out()
    np.save(VECTORIZER_FILE, vocab)

def main():
    os.makedirs("logs", exist_ok=True)
    items = load_logs()
    if not items:
        print("No logs found at", LOG_PATH)
        return
    print(f"Loaded {len(items)} log entries.")
    vec, arr = build_tfidf(items)
    save_index(vec, arr, items)
    print(f"Saved TF-IDF index to {EMB_FILE}, metadata to {META_FILE}, vectorizer vocab to {VECTORIZER_FILE}")

if __name__ == "__main__":
    main()

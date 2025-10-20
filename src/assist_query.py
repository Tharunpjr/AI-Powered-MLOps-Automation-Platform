# src/assist_query.py
import json, os, subprocess
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

EMB_FILE = ".embeddings.npy"
META_FILE = ".emb_meta.json"
VECTORIZER_FILE = ".tfidf_vectorizer.npy"
OLLAMA_MODEL = "llama-3"  # change if your local model name differs

def load_index():
    if not os.path.exists(EMB_FILE) or not os.path.exists(META_FILE) or not os.path.exists(VECTORIZER_FILE):
        raise FileNotFoundError("Index files missing. Run src/index_logs.py first.")
    arr = np.load(EMB_FILE)
    metas = json.load(open(META_FILE, "r", encoding="utf-8"))
    vocab = np.load(VECTORIZER_FILE, allow_pickle=True)
    # create a vectorizer from vocab (we'll use TfidfVectorizer with fixed vocabulary)
    vec = TfidfVectorizer(vocabulary=list(vocab))
    return arr, metas, vec

def embed_query_tfidf(query, vec):
    # transform query into same TF-IDF space (fit not called; uses vocabulary)
    qvec = vec.transform([query]).toarray()
    return qvec

def top_k_evidence(query, k=5):
    arr, metas, vec = load_index()
    qv = embed_query_tfidf(query, vec)  # (1, D)
    sims = cosine_similarity(qv, arr)[0]  # shape (N,)
    idx = np.argsort(-sims)[:k]
    results = []
    for i in idx:
        results.append({"score": float(sims[i]), "text": metas[i]["text"], "meta": metas[i]["meta"]})
    return results

def build_prompt(evidence, question):
    evidence_text = ""
    for i, e in enumerate(evidence):
        evidence_text += f"[EVID_{i}] {e['text']}\n"
    prompt = f"""
You are an MLOps assistant. Using ONLY the evidence blocks below, produce:
1) SUMMARY (3 bullets)
2) ROOT CAUSE hypotheses (1-2 bullets with confidence)
3) Up to 2 SAFE ACTIONS (each action must reference evidence blocks)

EVIDENCE:
{evidence_text}

QUESTION:
{question}

Answer in plain text, short bullets.
"""
    return prompt

def call_ollama(prompt):
    cmd = ["ollama", "run", OLLAMA_MODEL, "--prompt", prompt]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(f"Ollama error: {proc.stderr.strip()}")
    return proc.stdout.strip()

def assist(query="Summarize last 24 hours and suggest actions", top_k=5):
    evidence = top_k_evidence(query, k=top_k)
    if not evidence:
        return {"error":"No evidence found. Run index_logs.py first."}, []
    prompt = build_prompt(evidence, query)
    print("Calling Ollama local...")
    out = call_ollama(prompt)
    return {"raw_text": out}, evidence

if __name__ == "__main__":
    res, evidence = assist()
    print("=== EVIDENCE ===")
    for i, e in enumerate(evidence):
        print(f"[{i}] score={e['score']:.3f} {e['text']}")
    print("\n=== ASSISTANT OUTPUT ===")
    print(res.get("raw_text",""))

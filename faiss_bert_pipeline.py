# Install required libraries first using pip:
# pip install transformers faiss-cpu numpy ujson

import ujson
from transformers import AutoTokenizer, AutoModel
import torch
import faiss
import numpy as np

# Load .ji file
def load_data(file_path):
    data = []
    with open(file_path, "r") as file:
        for line in file:
            data.append(ujson.loads(line))
    return data

# Combine text fields for embedding
def prepare_texts(data):
    return [
        f"{item['short_description']} {item['long_description']}" 
        for item in data
    ]

# Generate embeddings using BERT
def encode_texts(texts, tokenizer, model, batch_size=32, device="cpu"):
    embeddings = []
    model.to(device)
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i+batch_size]
        encoded_inputs = tokenizer(
            batch,
            padding=True,
            truncation=True,
            return_tensors="pt",
            max_length=512
        ).to(device)
        with torch.no_grad():
            outputs = model(**encoded_inputs)
        batch_embeddings = outputs.last_hidden_state[:, 0, :].cpu().numpy()
        embeddings.append(batch_embeddings)
    return np.vstack(embeddings)

# Save FAISS index
def save_faiss_index(index, file_path):
    faiss.write_index(index, file_path)

# Load FAISS index
def load_faiss_index(file_path):
    return faiss.read_index(file_path)

# Main script
if __name__ == "__main__":
    # 1. Load and preprocess data
    file_path = "output.jl"
    data = load_data(file_path)
    texts = prepare_texts(data)

    # 2. Load BERT tokenizer and model
    model_name = "bert-base-uncased"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name)

    # 3. Generate embeddings
    device = "cuda" if torch.cuda.is_available() else "cpu"
    embeddings = encode_texts(texts, tokenizer, model, device=device)

    # 4. Initialize and populate FAISS index
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    print(f"Number of vectors in the index: {index.ntotal}")

    # 5. Save FAISS index
    save_faiss_index(index, "faiss_index.bin")

    # Example query
    query = ["Automate your workflows with AI."]
    query_embeddings = encode_texts(query, tokenizer, model, device=device)

    # Search FAISS index
    k = 5  # Number of nearest neighbors
    distances, indices = index.search(query_embeddings, k)

    # Output results
    print("\nTop matches:")
    for i, idx in enumerate(indices[0]):
        print(f"Match {i + 1}: {texts[idx]} (Distance: {distances[0][i]})")
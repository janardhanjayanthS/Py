import pymupdf
import torch
from sentence_transformers import SentenceTransformer

doc = pymupdf.open("data/algorithms_to_live_by.pdf")
corpus = []
for page in doc:
    if page:
        corpus.append(page.get_text())


def print_results_using_sentence_transformer(query: str, top_k: int = 5) -> None:
    st_embedder = SentenceTransformer("all-MiniLM-L6-v2")
    st_corpus_embeddings = st_embedder.encode_document(corpus, convert_to_tensor=True)
    query_embedding = st_embedder.encode_query(query, convert_to_tensor=True)

    similarity_scores = st_embedder.similarity(query_embedding, st_corpus_embeddings)[0]
    scores, indices = torch.topk(similarity_scores, k=top_k)

    print("\nQuery:", query)
    print(f"Top {top_k} most similar sentences in corpus:")

    for score, idx in zip(scores, indices):
        print(f"(Score: {score:.4f})", corpus[idx])


def print_results_using_open_ai(query: str, top_k: int = 5) -> None: ...

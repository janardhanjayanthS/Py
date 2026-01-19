import torch
from docs import corpus
from open_ai import print_results_using_open_ai
from sentence_transformers import SentenceTransformer


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


if __name__ == "__main__":
    query = "what is machine learning"
    print_results_using_sentence_transformer(query=query)
    print("-" * 50)
    print_results_using_open_ai(query=query)

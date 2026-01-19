import os
from typing import List

import numpy as np
from docs import corpus
from dotenv import load_dotenv
from openai import OpenAI
from sklearn.metrics.pairwise import cosine_similarity

load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_embeddings_batch(
    texts: List[str], model: str = "text-embedding-3-large", batch_size: int = 100
):
    """
    Get embeddings for a list of texts, processing in batches

    Args:
        texts: List of text strings to embed
        model: OpenAI embedding model to use
        batch_size: Number of texts to process per API call (max ~2048 depending on text length)

    Returns:
        List of embeddings
    """
    all_embeddings = []

    # Clean and truncate texts
    cleaned_texts = [text.replace("\n", " ")[:8000] for text in texts]

    # Process in batches
    for i in range(0, len(cleaned_texts), batch_size):
        batch = cleaned_texts[i : i + batch_size]

        print(
            f"Processing batch {i // batch_size + 1}/{(len(cleaned_texts) - 1) // batch_size + 1} ({len(batch)} texts)..."
        )

        try:
            response = client.embeddings.create(input=batch, model=model)
            batch_embeddings = [data.embedding for data in response.data]
            all_embeddings.extend(batch_embeddings)

        except Exception as e:
            print(f"Error processing batch: {e}")
            # If batch fails, try processing one by one
            for text in batch:
                try:
                    response = client.embeddings.create(input=[text], model=model)
                    all_embeddings.append(response.data[0].embedding)
                except Exception as e2:
                    print(f"Failed to embed text: {e2}")
                    # Add zero vector as placeholder
                    all_embeddings.append(
                        [0.0] * 3072
                    )  # 3072 for text-embedding-3-large

    return all_embeddings


def print_results_using_open_ai(query: str, top_k: int = 5) -> None:
    """
    Search through corpus using OpenAI embeddings

    Args:
        query: Search query string
        top_k: Number of top results to return
    """
    # Embed all documents in batches
    print("Embedding documents...")
    doc_embeddings = np.array(get_embeddings_batch(corpus, batch_size=50))

    # Embed query
    print("Embedding query...")
    query_response = client.embeddings.create(
        input=[query], model="text-embedding-3-large"
    )
    query_embedding = np.array(query_response.data[0].embedding).reshape(1, -1)

    # Calculate similarities
    similarities = cosine_similarity(query_embedding, doc_embeddings)[0]

    # Get top indices
    top_indices = similarities.argsort()[::-1][:top_k]

    # Print results
    print(f"\n{'=' * 80}")
    print(f"Top {top_k} results for: '{query}'")
    print(f"{'=' * 80}\n")

    for rank, i in enumerate(top_indices, 1):
        preview = corpus[i][:300].replace("\n", " ").strip()
        if len(corpus[i]) > 300:
            preview += "..."

        print(f"Rank {rank} | Page {i + 1} | Similarity: {similarities[i]:.4f}")
        print(f"{preview}")
        print(f"{'-' * 80}\n")

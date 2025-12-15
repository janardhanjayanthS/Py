from decimal import Decimal

from langchain_core.documents import Document
from langchain_core.messages import AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda
from langchain_openai import ChatOpenAI
from src.core.constants import (
    CONTEXTUALIZE_PROMPT,
    DOCUMENT_FORMAT_PROMPT,
    MODEL_COST_PER_MILLION_TOKENS,
    OPENAI_API_KEY,
    QA_PROMPT,
    RETRIEVER,
    AIModels,
    logger,
)


def get_contextualize_rag_chain():
    chain = CONTEXTUALIZE_PROMPT | get_agent(AIModels.GPT_4o_MINI) | StrOutputParser()
    return chain


def get_conversational_rag_chain():
    chain = (
        {
            "context": RunnableLambda(contextualized_retrival) | format_docs,
            "question": lambda x: x["question"],
            "chat_history": lambda x: x.get("question", []),
        }
        | QA_PROMPT
        | get_agent(AIModels.GPT_4o_MINI)
    )
    return chain


def format_docs(docs: Document):
    return "\n\n".join(doc.page_content for doc in docs)


def contextualized_retrival(input_dict):
    print(f"Input dict: {input_dict}")
    chat_history = input_dict.get("chat_history", [])
    question = input_dict["question"]

    if chat_history:
        reformulated_question = get_contextualize_rag_chain().invoke(
            {"chat_history": chat_history, "question": question}
        )
        logger.info(f"Reformulated quetion: {reformulated_question}")
    else:
        reformulated_question = question

    docs = RETRIEVER.invoke(reformulated_question)
    return docs


def get_agent(ai_model: AIModels):
    """Initializes and returns an instance of the ChatOpenAI client.

    The client is configured to use the specified model, a temperature of 0
    (for deterministic responses), and enables streaming usage tracking.

    Args:
        ai_model: An enum member (AIModels) specifying the desired OpenAI model (e.g., GPT-4, GPT-3.5-turbo).

    Returns:
        A configured instance of the ChatOpenAI client.
    """
    agent = ChatOpenAI(
        model=ai_model.value, temperature=0, api_key=OPENAI_API_KEY, stream_usage=True
    )
    return agent


def calculate_token_cost(token_usage: dict, ai_model=AIModels) -> str:
    """Calculates the total monetary cost incurred for a given prompt-response pair based on token usage.

    The cost is calculated by summing the input token cost and the output token cost
    using the predefined cost rates for the specified model.

    Args:
        token_usage: A dictionary containing the token counts, expected to have keys "input_tokens" and "output_tokens".
        ai_model: An enum member (AIModels) specifying the model used for the operation.

    Returns:
        A string representation of the total calculated cost (e.g., "0.00015").
    """
    input_tokens = token_usage.get("input_tokens", 0)
    output_tokens = token_usage.get("output_tokens", 0)
    return str(
        Decimal(
            get_input_token_cost(input_tokens=input_tokens, ai_model=ai_model)
            + get_output_token_cost(output_tokens=output_tokens, ai_model=ai_model)
        )
    )


def get_output_token_cost(output_tokens: int, ai_model: AIModels) -> float:
    """Calculates the monetary cost specifically for the output (response) tokens.

    The cost is based on the model's defined cost per million output tokens.

    Args:
        output_tokens: The number of tokens generated in the LLM's response.
        ai_model: An enum member (AIModels) specifying the model used.

    Returns:
        The total cost of the output tokens as a float.
    """
    output_token_cost = output_tokens * (
        MODEL_COST_PER_MILLION_TOKENS[ai_model.value]["o"] / 1_000_000
    )
    return output_token_cost


def get_input_token_cost(input_tokens: int, ai_model: AIModels) -> float:
    """Calculates the monetary cost specifically for the input (prompt/context) tokens.

    The cost is based on the model's defined cost per million input tokens.

    Args:
        input_tokens: The number of tokens sent to the LLM in the prompt and context.
        ai_model: An enum member (AIModels) specifying the model used.

    Returns:
        The total cost of the input tokens as a float.
    """
    input_token_cost = input_tokens * (
        MODEL_COST_PER_MILLION_TOKENS[ai_model.value]["i"] / 1_000_000
    )
    return input_token_cost


def get_formatted_ai_response(
    results: list[Document], query: str, ai_model
) -> AIMessage:
    """Formats the retrieved document chunks and query into a prompt and generates
    a coherent response using the LLM (Large Language Model).

    This function implements the Retrieval-Augmented Generation (RAG) pattern.

    Args:
        results: A list of Document objects retrieved from the vector store.
        query: The original user's question.
        ai_model: The initialized LLM instance used for generating the final answer.

    Returns:
        An AIMessage object containing the final, human-readable answer synthesized
        from the retrieved context and the query.
    """
    context_parts = []
    for i, doc in enumerate(results, 1):
        source = doc.metadata.get("source", "Unknown")
        page = doc.metadata.get("page", "N/A")
        content = doc.page_content[:500]
        context_parts.append(f"Source {i}: {source}, Page {page}\n{content}\n")
    context = "\n---\n".join(context_parts)
    updated_prompt = DOCUMENT_FORMAT_PROMPT.format(query=query, context=context)
    ai_response = ai_model.invoke(updated_prompt)
    return ai_response

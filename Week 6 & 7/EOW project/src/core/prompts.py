from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

SYSTEM_PROMPT = """
You are a helpful assistant agent, answer the question 
carefully with precise answer. 
"""

CONTEXTUALIZE_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
                Given a chat history and the latest user question 
                which might reference context in the chat history, formulate a standalone 
                question which can be understood without the chat history. 
                Do NOT answer the question, just reformulate it if needed and otherwise 
                return it as is.
            """,
        ),
        MessagesPlaceholder("chat_history"),  # This will hold the conversation
        ("human", "{question}"),
    ]
)

QA_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            Answer the question based on the following context:

            {context}
            
            Rules:
                -   If the question is any simple greeting or welcome 
                    message then just reply with simple greeting,
                    If you cannot understand the question then ask doubts.
                -   If the question is out-of-context then reply that 
                    you do not have references to get answer. 
                -   Only answer questions for which you have references to.
                -   Do not generate any additional symbols such as 
                    slashes, \\n, \\t, or any other mark down symbols
            """,
        ),
        MessagesPlaceholder("chat_history"),
        ("human", "{question}"),
    ]
)

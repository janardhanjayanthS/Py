from langgraph.graph import MessagesState

for k, v in MessagesState.__dict__.items():
    print(f"{k}: {v}")

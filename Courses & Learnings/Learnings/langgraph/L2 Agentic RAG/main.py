from graph import get_graph, graph_image  # noqa: F401

if __name__ == "__main__":
    graph = get_graph()
    # TO CREATE GRAPH IMG
    # graph_image(graph)
    for chunk in graph.stream(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "What does Lilian Weng say about types of reward hacking?",
                }
            ]
        }
    ):
        for node, update in chunk.items():
            print("Update from node", node)
            update["messages"][-1].pretty_print()
            print("\n\n")

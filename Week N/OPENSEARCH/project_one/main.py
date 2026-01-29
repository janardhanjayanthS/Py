from opensearchpy import OpenSearch


def main() -> None:
    # --- CONFIGURATION ---
    # For a local install (e.g., via Docker), these are the defaults.
    host = "localhost"
    port = 9200
    auth = None

    # Create the client connection
    client = OpenSearch(
        hosts=[{"host": host, "port": port}],
        http_auth=auth,
        use_ssl=False,
        verify_certs=False,  # Set to True for production!
        ssl_show_warn=False,
    )

    # --- STEP 1 & 2: INGEST & INDEX ---
    # We define the "Index" name (like a database table name)
    index_name = "server-logs"

    # The data (JSON document)
    log_entry = {"user": "John", "action": "login_failed", "time": "12:00 PM"}

    # Send data to OpenSearch.
    # This "Ingests" the JSON and OpenSearch immediately "Indexes" it so it's searchable.
    response = client.index(
        index=index_name,
        body=log_entry,
        refresh=True,  # Force index to update immediately for this demo
    )

    print(f"1. Data Ingested! ID: {response['_id']}")

    # --- STEP 3: SEARCH ---
    # We want to find all logs where the action was "login_failed"
    query = {"query": {"match": {"action": "login_failed"}}}

    # Execute the search
    search_results = client.search(body=query, index=index_name)

    # --- PRINT RESULTS ---
    print("\n2. Search Results found:")
    for hit in search_results["hits"]["hits"]:
        print(f" - Found Document: {hit['_source']}")


if __name__ == "__main__":
    main()

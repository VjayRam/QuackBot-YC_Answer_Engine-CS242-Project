from elasticsearch import Elasticsearch

# Connect to Elasticsearch
es = Elasticsearch("http://localhost:9200")

# Function to search documents
def search_documents(index_name, query, size=10):
    search_query = {
        "query": {
            "query_string": {
                "query": query  # General query for full-text search across all fields
            }
        }
    }

    response = es.search(index=index_name, body=search_query, size=size)

    data = []
    # Print search results
    if response['hits']['hits']:
        print(f"\nFound {len(response['hits']['hits'])} results for '{query}':\n")
        for hit in response['hits']['hits']:
            print(f"ID: {hit['_id']} | Score: {hit['_score']}")
            val = hit['_source']
            print(f"Source: {val}\n")
            data.append(val)
    else:
        print(f"No results found for '{query}'.")

# Run the search
if __name__ == "__main__":
    index_name = "y_combinator_companies"
    user_query = "All the comapnies founded in 2023"
    search_documents(index_name, user_query)

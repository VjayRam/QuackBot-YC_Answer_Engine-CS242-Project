from elasticsearch import Elasticsearch

# **Connect to Elasticsearch**
es = Elasticsearch("http://localhost:9200")  # Ensure ES is running
index_name = "y_combinator_companies"  # Replace with your actual index name

# **Delete all documents in the index**
def delete_and_recreate_index(es, index_name):
    if es.indices.exists(index=index_name):
        es.indices.delete(index=index_name)
        print(f"Index '{index_name}' deleted successfully.")
    else:
        print(f"Index '{index_name}' does not exist.")

# Run the function

# **Run the deletion**
if es.ping():
    delete_and_recreate_index(es, index_name)
else:
    print("Could not connect to Elasticsearch. Ensure it is running.")

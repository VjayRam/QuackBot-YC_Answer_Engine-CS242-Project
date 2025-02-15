import json
import time
from elasticsearch import Elasticsearch, helpers

# Function to read the .jl file and load the data
def read_jl_file(file_path):
    data = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                try:
                    data.append(json.loads(line))
                except json.JSONDecodeError as e:
                    print(f"Skipping invalid JSON line: {e}")
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    return data

# Function to create an index with a mapping
def create_index(es, index_name):
    mapping = {
        "mappings": {
            "properties": {
                "company_id": {"type": "keyword"},
                "company_name": {"type": "text"},
                "short_description": {"type": "text"},
                "long_description": {"type": "text"},
                "batch": {"type": "keyword"},
                "status": {"type": "keyword"},
                "tags": {"type": "keyword"},  # Changed to keyword for better filtering
                "location": {"type": "text"},
                "country": {"type": "text"},
                "year_founded": {"type": "integer"},
                "num_founders": {"type": "integer"},
                "founders_names": {"type": "keyword"},  # Changed to keyword for better searchability
                "team_size": {"type": "integer"},
                "website": {"type": "keyword"},
                "cb_url": {"type": "keyword"},
                "linkedin_url": {"type": "keyword"},
                "image_urls": {"type": "keyword"}  # Changed to keyword for structured storage
            }
        }
    }

    # Create index if it doesn't exist
    if not es.indices.exists(index=index_name):
        es.indices.create(index=index_name, body=mapping)
        print(f"Index '{index_name}' created successfully.")
    else:
        print(f"Index '{index_name}' already exists.")

# Function to index documents using bulk API for efficiency
def index_documents(es, index_name, documents):
    start_time = time.perf_counter()  # Start timing

    actions = [
        {
            "_index": index_name,
            "_id": doc_id,
            "_source": doc
        }
        for doc_id, doc in enumerate(documents)
    ]

    # Bulk index documents
    helpers.bulk(es, actions)

    end_time = time.perf_counter()  # End timing
    elapsed_time = end_time - start_time
    print(f"Time taken to index {len(documents)} documents: {elapsed_time:.2f} seconds")

# Main execution block
if __name__ == "__main__":
    file_path = 'output.jl'  # Replace with actual .jl file path
    index_name = 'y_combinator_companies'
    
    # Connect to local Elasticsearch instance
    es = Elasticsearch("http://localhost:9200")  # Default host and port
    
    if es.ping():
        print("Connected to Elasticsearch")
        
        # Load data from .jl file
        data = read_jl_file(file_path)
        
        if data:
            print(f"Loaded {len(data)} records from {file_path}")
            
            # Create an index in Elasticsearch
            # create_index(es, index_name)
            
            # # Index the loaded data efficiently
            # index_documents(es, index_name, data)
        else:
            print("No data found. Ensure the .jl file exists and contains valid JSON lines.")
    else:
        print("Could not connect to Elasticsearch. Ensure it is running locally.")

from openai import OpenAI

client = OpenAI()
import pinecone

# Initialize Pinecone client and connect to the index
pinecone_client = pinecone.Pinecone()
index = pinecone_client.Index("testing")


# Example documents to store
documents = [
    {"id": "doc1", "text": "The quick brown fox jumps over the lazy dog."},
    {"id": "doc2", "text": "Artificial intelligence is revolutionizing technology."},
    {"id": "doc3", "text": "Machine learning provides systems the ability to learn."}
]

# Function to convert text into embeddings
def get_openai_embedding(text):
    response = client.embeddings.create(input=text, model="text-embedding-ada-002")
    embedding = response.data[0].embedding
    return embedding

# Prepare data for Pinecone by converting documents to embeddings
pinecone_data = []
for doc in documents:
    embedding = get_openai_embedding(doc["text"])
    pinecone_data.append({
        "id": doc["id"],  # Unique ID for each document
        "values": embedding,  # Embedding vector
        "metadata": {"text": doc["text"]}  # Metadata, in this case, the original text
    })

# Upsert (add/update) the documents into Pinecone
index.upsert(vectors=pinecone_data)

print("Documents added to Pinecone!")

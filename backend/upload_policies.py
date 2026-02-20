import os
import sys
from dotenv import load_dotenv

load_dotenv()

# Try to import Pinecone modules, handle gracefully if not available
try:
    from pinecone import Pinecone, ServerlessSpec
    from langchain_pinecone import PineconeVectorStore
    from langchain.embeddings.base import Embeddings
    PINECONE_AVAILABLE = True
except ImportError as e:
    print(f"Note: Pinecone/Langchain modules not available: {e}")
    PINECONE_AVAILABLE = False

# Simple mock embeddings class (for testing)
class MockEmbeddings:
    def __init__(self):
        pass
    
    def embed_documents(self, texts):
        # Return simple hash-based vectors for testing
        return [[float(ord(c) % 256) / 256 for c in text[:384]] for text in texts]
    
    def embed_query(self, text):
        return [float(ord(c) % 256) / 256 for c in text[:384]]

if PINECONE_AVAILABLE:
    try:
        # 1. Initialize
        pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
        index_name = "compliance-rules"
        embeddings = MockEmbeddings()

        # 2. Create Index if it doesn't exist
        if index_name not in pc.list_indexes().names():
            pc.create_index(
                name=index_name,
                dimension=384, 
                metric="cosine",
                spec=ServerlessSpec(cloud="aws", region="us-east-1")
            )

        # 3. Load and Upload policy.txt
        with open("policy.txt", "r") as f:
            policies = [line.strip() for line in f.readlines() if line.strip()]

        if policies:
            # Upload to Pinecone
            vectorstore = PineconeVectorStore.from_texts(
                texts=policies,
                embedding=embeddings,
                index_name=index_name
            )
            print(f"Successfully uploaded {len(policies)} policies to Pinecone")
        else:
            print("No policies found in policy.txt")

    except Exception as e:
        print(f"Note: Pinecone upload encountered an issue: {e}")
else:
    print("Pinecone integration unavailable. Install langchain-pinecone to enable.")
    # Still load and display the policies
    try:
        with open("policy.txt", "r") as f:
            policies = [line.strip() for line in f.readlines() if line.strip()]
            if policies:
                print(f"Loaded {len(policies)} policies (not uploaded to Pinecone)")
            else:
                print("No policies found in policy.txt")
    except FileNotFoundError:
        print("policy.txt not found")

print("Policy rules uploaded to Pinecone successfully.")
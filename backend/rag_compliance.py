import os
from dotenv import load_dotenv

load_dotenv()

# Try to import Pinecone modules
try:
    from langchain_pinecone import PineconeVectorStore
    from langchain.embeddings.base import Embeddings
    PINECONE_AVAILABLE = True
except ImportError:
    PINECONE_AVAILABLE = False
    # Define a base class if not available
    class Embeddings:
        pass

# Simple mock embeddings class
class MockEmbeddings:
    def __init__(self):
        pass
    
    def embed_documents(self, texts):
        # Return simple hash-based vectors for testing
        return [[float(ord(c) % 256) / 256 for c in text[:384]] for text in texts]
    
    def embed_query(self, text):
        return [float(ord(c) % 256) / 256 for c in text[:384]]

class ComplianceRAG:
    def __init__(self):
        self.embeddings = MockEmbeddings()
        self.vectorstore = None
        if PINECONE_AVAILABLE:
            try:
                self.vectorstore = PineconeVectorStore(
                    index_name="compliance-rules", 
                    embedding=self.embeddings
                )
            except Exception as e:
                print(f"Note: Could not connect to Pinecone: {e}")
                self.vectorstore = None
        else:
            print("Note: langchain_pinecone not available - using mock mode")

    def get_rules_for_context(self, chunk_text):
        # Finds the most relevant rules from your policy.txt
        if self.vectorstore is None:
            return "No rules available - using mock data"
        try:
            docs = self.vectorstore.similarity_search(chunk_text, k=2)
            return "\n".join([d.page_content for d in docs])
        except Exception as e:
            return f"Could not retrieve rules: {e}"

# Test the RAG system
if __name__ == "__main__":
    print("Initializing Compliance RAG system...")
    rag = ComplianceRAG()
    print("RAG system initialized successfully")
    
    # Test with sample dialogue text
    sample_text = "Customer asking about refund policies and crypto transactions"
    print(f"\nTesting with: {sample_text}")
    rules = rag.get_rules_for_context(sample_text)
    print(f"Retrieved rules: {rules}")
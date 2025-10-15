import os
import json
import numpy as np
import faiss
from datetime import datetime
from openai import OpenAI


def get_openai_client():
    """Create OpenAI client using Replit AI Integrations"""
    base_url = os.environ.get('AI_INTEGRATIONS_OPENAI_BASE_URL')
    api_key = os.environ.get('AI_INTEGRATIONS_OPENAI_API_KEY')
    
    if not base_url or not api_key:
        raise Exception('OpenAI integration not configured')
    
    return OpenAI(base_url=base_url, api_key=api_key)


class NewsletterMemory:
    """Vector store for newsletter embeddings and memory"""
    
    def __init__(self, storage_path='data'):
        self.storage_path = storage_path
        self.index_file = os.path.join(storage_path, 'newsletter_index.faiss')
        self.metadata_file = os.path.join(storage_path, 'newsletter_metadata.json')
        self.dimension = 1536
        
        os.makedirs(storage_path, exist_ok=True)
        
        self.index = None
        self.metadata = []
        
        self.load()
    
    def load(self):
        """Load existing index and metadata"""
        if os.path.exists(self.index_file):
            self.index = faiss.read_index(self.index_file)
        else:
            self.index = faiss.IndexFlatL2(self.dimension)
        
        if os.path.exists(self.metadata_file):
            with open(self.metadata_file, 'r') as f:
                self.metadata = json.load(f)
    
    def save(self):
        """Save index and metadata to disk"""
        faiss.write_index(self.index, self.index_file)
        with open(self.metadata_file, 'w') as f:
            json.dump(self.metadata, f, indent=2)
    
    def get_embedding(self, text):
        """Get embedding for text using OpenAI"""
        client = get_openai_client()
        
        # Note: OpenAI embeddings API not supported by AI Integrations
        # For now, we'll use a simple hash-based approach as placeholder
        # In production, you'd use a proper embedding model
        
        # Simple embedding placeholder - convert text to vector
        # This is a temporary solution until embeddings API is available
        text_hash = hash(text) % (10**8)
        embedding = np.random.RandomState(text_hash).randn(self.dimension).astype('float32')
        return embedding
    
    def add_newsletters(self, newsletters):
        """Add newsletters to the vector store"""
        for nl in newsletters:
            text = f"{nl['subject']} {nl['body']}"
            embedding = self.get_embedding(text)
            
            self.index.add(np.array([embedding]))
            self.metadata.append({
                'id': nl['id'],
                'subject': nl['subject'],
                'from': nl['from'],
                'date': nl['date'],
                'added_at': datetime.now().isoformat()
            })
        
        self.save()
    
    def search(self, query, k=5):
        """Search for similar newsletters"""
        if self.index.ntotal == 0:
            return []
        
        query_embedding = self.get_embedding(query)
        distances, indices = self.index.search(np.array([query_embedding]), k)
        
        results = []
        for i, idx in enumerate(indices[0]):
            if idx < len(self.metadata):
                result = self.metadata[idx].copy()
                result['distance'] = float(distances[0][i])
                results.append(result)
        
        return results
    
    def get_stats(self):
        """Get statistics about stored newsletters"""
        return {
            'total_newsletters': self.index.ntotal,
            'storage_size_mb': os.path.getsize(self.index_file) / (1024*1024) if os.path.exists(self.index_file) else 0,
            'metadata_count': len(self.metadata)
        }

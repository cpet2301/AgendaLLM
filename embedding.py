import os
import streamlit as st
import pandas as pd
import xml.etree.ElementTree as ET
import pytesseract
from PIL import Image
from PyPDF2 import PdfReader
import ollama
from dotenv import load_dotenv
import chromadb

VECTOR_DB = "ChromaDB"
COLLECTION_NAME = "rag_collection"

# Load environment variables from .env file
load_dotenv()

# Create a Chroma Client with persistent storage
persist_directory = "./chroma_data"
os.makedirs(persist_directory, exist_ok=True)
chroma_client = chromadb.PersistentClient(path=persist_directory)

# Check is Chroma Client is working
chroma_client.heartbeat()

# Get/create ChromaDB collection
try:
    collection = chroma_client.get_collection(name=COLLECTION_NAME)
except Exception as e:
    collection = chroma_client.create_collection(name=COLLECTION_NAME)

def get_local_embedding(text):
    """Vectorizes text using a local Ollama embedding model."""
    try:
        response = ollama.embeddings(model="nomic-embed-text", prompt=text)
        return response["embedding"]
    except Exception as e:
        print(f"Error generating embedding: {e}")
        return None
    
def vector_query(embedding, top_k=3):
    """Takes an embedded query and finds relevant information in the vector database."""
    try:
        results = collection.query(
            query_embeddings=embedding,
            n_results=top_k
        )
        return results["documents"][0]
    except Exception as e:
        st.error(f"Error querying {VECTOR_DB}: {e}")
        return []

def detect_text_column(df):
    """Detects the most likely text column in a DataFrame from a CSV."""
    text_columns = {}
    
    for col in df.columns:
        string_mean = df[col].apply(lambda x: isinstance(x, str)).mean()
        if string_mean > 0.8:
            text_columns[col] = string_mean

    if text_columns:
        best_text_column = max(text_columns, key=text_columns.get)
        return best_text_column
    else:
        return None

def process_uploaded_file(uploaded_file):
    """Process the uploaded file, depending on its type."""
    file_type = uploaded_file.type
    
    # Process CSV file
    if file_type == "text/csv":
        df = pd.read_csv(uploaded_file)
        
        # Call helper function to begin embedding process
        text_column = detect_text_column(df)
        if text_column is None:
            st.error("No suitable text column found in the uploaded CSV.")
            return
        
        st.success(f"Detected text column: {text_column}")
        
        # Convert CSV text on each row into embeddings
        for index, row in df.iterrows():
            text = row[text_column]
            embedding = get_local_embedding(text)
            if embedding:
                vector_upsert(str(index), embedding, text)

    # Process PDF file
    elif file_type == "application/pdf":
        pdf_reader = PdfReader(uploaded_file)
        pdf_text = ""
        
        for page_num in range(len(pdf_reader.pages)):
            page_text = pdf_reader.pages[page_num].extract_text()
            if page_text != None:
                pdf_text += page_text
        
        embedding = get_local_embedding(pdf_text)
        if embedding:
            vector_upsert(uploaded_file.name, embedding, pdf_text)

    # Process XML file
    elif file_type == "text/xml":
        tree = ET.parse(uploaded_file)
        root = tree.getroot()
        xml_text = ET.tostring(root, encoding="unicode", method="text")
        
        embedding = get_local_embedding(xml_text)
        if embedding:
            vector_upsert(uploaded_file.name, embedding, xml_text)

    # Process image file
    elif "image" in file_type:
        img = Image.open(uploaded_file)

        # Use OCR to extract text from the image
        img_text = pytesseract.image_to_string(img)
        
        if img_text.strip():
            embedding = get_local_embedding(img_text)
            if embedding:
                vector_upsert(uploaded_file.name, embedding, img_text)
        
        # Handles cases when text is not found in an image
        else:
            st.error("No text found in the image.")

    else:
        st.error("Unsupported file type.")

def vector_upsert(doc_id, embedding, text):
    """Upserts the embedding into the vector database."""
    try:
        collection.add(
            ids=[doc_id],
            embeddings=[embedding],
            documents=[text]
        )
        
    except Exception as e:
        st.error(f"Error uploading to {VECTOR_DB}: {e}")

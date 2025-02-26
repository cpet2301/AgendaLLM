import os
import streamlit as st
from pinecone.grpc import PineconeGRPC as Pinecone
from openai import OpenAI
import pandas as pd
import xml.etree.ElementTree as ET
import pytesseract
from PIL import Image
from PyPDF2 import PdfReader
import ollama
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve API keys from environment variables
pinecone_api_key = os.getenv("PINECONE_KEY")

# Initialize Pinecone
if not pinecone_api_key:
    st.error("Pinecone API key is missing. Please check your .env file.")
else:
    pc = Pinecone(api_key=pinecone_api_key, environment="us-east-1-aws-free")
    index = pc.Index("testing")

def get_local_embedding(text):
    """Vectorizes text using a local Ollama embedding model."""
    try:
        response = ollama.embeddings(model="nomic-embed-text", prompt=text)
        return response["embedding"]
    except Exception as e:
        print(f"Error generating embedding: {e}")
        return None
    
def query_pinecone(embedding):
    """Takes an embedded query and finds relevant information in Pinecone database."""
    try:
        result = index.query(vector=embedding, top_k=3, include_metadata=True)
        if result is None:
            st.error("No result returned from the query.")
            return []
        if "matches" in result and result["matches"]:
            texts = [match["metadata"]["text"] if match["metadata"] else "No metadata available" for match in result["matches"]]
        else:
            st.error("No matches found.")
            texts = []
        return texts
    except Exception as e:
        st.error(f"Error querying Pinecone: {e}")
        if hasattr(e, 'response'):
            st.error(f"Response from Pinecone: {e.response.text}")
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
        st.write("CSV File Uploaded:")
        st.dataframe(df)
        
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
                upsert_to_pinecone(str(index), embedding, text)

    # Process PDF file
    elif file_type == "application/pdf":
        pdf_reader = PdfReader(uploaded_file)
        pdf_text = ""
        
        for page_num in range(len(pdf_reader.pages)):
            page_text = pdf_reader.pages[page_num].extract_text()
            if page_text != None:
                pdf_text += page_text
        
        st.write("Extracted Text from PDF:")
        st.text(pdf_text)
        
        embedding = get_local_embedding(pdf_text)
        if embedding:
            upsert_to_pinecone(uploaded_file.name, embedding, pdf_text)

    # Process XML file
    elif file_type == "text/xml":
        tree = ET.parse(uploaded_file)
        root = tree.getroot()
        xml_text = ET.tostring(root, encoding="unicode", method="text")
        
        st.write("Extracted Text from XML:")
        st.text(xml_text)
        
        embedding = get_local_embedding(xml_text)
        if embedding:
            upsert_to_pinecone(uploaded_file.name, embedding, xml_text)

    # Process image file
    elif "image" in file_type:
        img = Image.open(uploaded_file)

        # Use OCR to extract text from the image
        img_text = pytesseract.image_to_string(img)
        
        if img_text.strip():
            st.write("Extracted Text from Image:")
            st.text(img_text)
            
            embedding = get_local_embedding(img_text)
            if embedding:
                upsert_to_pinecone(uploaded_file.name, embedding, img_text)
        
        # Handles cases when text is not found in an image
        else:
            st.error("No text found in the image.")

    else:
        st.error("Unsupported file type.")

def upsert_to_pinecone(doc_id, embedding, text):
    """Upserts the embedding into Pinecone."""
    try:
        pinecone_data = [{
            "id": doc_id,
            "values": embedding,
            "metadata": {"text": text}
        }]


        
        index.upsert(vectors=pinecone_data)
        st.success(f"Document {doc_id} added to Pinecone successfully!")
        
    except Exception as e:
        st.error(f"Error uploading to Pinecone: {e}")

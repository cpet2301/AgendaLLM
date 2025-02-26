import ollama

def get_local_embedding(text):
    """Vectorizes text using a local Ollama embedding model."""
    try:
        response = ollama.embeddings(model="nomic-embed-text", prompt=text)
        return response["embedding"]
    except Exception as e:
        print(f"Error generating embedding: {e}")
        return None

# Example usage:
text = "This is a test sentence."
embedding = get_local_embedding(text)
print(embedding)


# Assuming embedding.query_pinecone(user_embedding) is correctly implemented

# if user_embedding:
#     # Query Pinecone for the most relevant context
#     retrieved_texts = embedding.query_pinecone(user_embedding)

#     # Prepare conversation history
#     messages_for_llama = [
#         {"role": "system", "content": "You are a helpful assistant answering the prompt of the user."}
#     ]
    
#     # Initialize chat history if not set
#     if "messages" not in st.session_state:
#         st.session_state.messages = []

#     messages_for_llama += st.session_state.messages

#     # Include retrieved context if available
#     if retrieved_texts:
#         messages_for_llama.append({"role": "system", "content": f"Relevant information: {retrieved_texts}"})

#     try:
#         # Generate response using local Ollama model
#         response = ollama.chat(model="codellama:7b", messages=messages_for_llama)

#         # Extract the assistant's response
#         response_content = response["message"]["content"]

#         # Display the response
#         with st.chat_message("assistant"):
#             st.markdown(response_content)

#     except Exception as e:
#         st.error(f"Error generating assistant response: {e}")
#         response_content = "Sorry, I couldn't generate a response. Please try again."

#     # Add assistant response to chat history
#     st.session_state.messages.append({"role": "assistant", "content": response_content})

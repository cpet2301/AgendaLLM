import streamlit as st
import embedding
import ollama

    
st.title("Agenda LLM")

# Initialize session and message history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display past messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# File uploader initialization
with st.sidebar:
    uploaded_file = st.file_uploader(
        "Upload a file (PDF, XML, CSV, PNG, JPG, JPEG)", 
        type=["pdf", "xml", "csv", "png", "jpg", "jpeg"]
    )

if uploaded_file:
    try:
        embedding.process_uploaded_file(uploaded_file)
        
        # Add assistant response acknowledging the file upload
        with st.chat_message("assistant"):
            st.markdown("Your file has been successfully uploaded and processed!")
    except Exception as e:
        st.error(f"Error processing the uploaded file: {e}")

# Chat interaction
if prompt := st.chat_input("Ask me anything!"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Convert user message to an embedding using localllm
    user_embedding = embedding.get_local_embedding(prompt)

    if user_embedding:
    # Query Pinecone for the most relevant context
        retrieved_texts = embedding.vector_query(user_embedding)

        # Prepare conversation history
        messages_for_llama = [
            {"role": "system", "content": "You are a helpful assistant answering the prompt of the user."}
        ]
        
        # Initialize chat history if not set
        if "messages" not in st.session_state:
            st.session_state.messages = []

        messages_for_llama += st.session_state.messages

        # Include retrieved context if available
        if retrieved_texts:
            messages_for_llama.append({"role": "system", "content": f"Relevant information: {retrieved_texts}"})

        try:
            # Generate response using local Ollama model
            response = ollama.chat(model="phi3", messages=messages_for_llama)

            # Extract the assistant's response
            response_content = response["message"]["content"]

            # Display the response
            with st.chat_message("assistant"):
                st.markdown(response_content)

        except Exception as e:
            st.error(f"Error generating assistant response: {e}")
            response_content = "Sorry, I couldn't generate a response. Please try again."

        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response_content})

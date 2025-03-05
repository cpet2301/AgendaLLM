import streamlit as st
import embedding
import ollama
import time
import random

# Selects a tip from a list randomly
def random_tips(tip_list):
    if not tip_list:
        print("List is empty")
        return
    return random.choice(tip_list)
    
st.title("Agenda LLM")

tips_list = ["Make sure your device is plugged in for the best experience!", "Tip 2", "Tip 3", "Tip 4", "Tip 5"]

# Displays progress bar when loading
progress_text = random_tips(tips_list)
progress_bar = st.progress(0, progress_text)

for percent_complete in range(100):
    time.sleep(0.01)
    progress_bar.progress(percent_complete + 1, text = progress_text)
time.sleep(1)
progress_bar.empty()
st.sidebar.title("This is the sidebar")
page = st.sidebar.radio("Go To", ["Home", "About", "Contact"])

if page == "Home":
    # Initialize session and message history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display past messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # File uploader initialization
    with st.sidebar.container():
        for i in range(30):
            st.write("\n")
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
            retrieved_texts = embedding.query_pinecone(user_embedding)

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
                response = ollama.chat(model="codellama:7b", messages=messages_for_llama)

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
elif page == "About":
    st.subheader("Welcome to the About Page")
    st.write("Sample About")
elif page == "Contact":
    st.subheader("Welcome to the Contact page")
    st.write("Sample Contact")
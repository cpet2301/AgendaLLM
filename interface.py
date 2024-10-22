import streamlit as st
import embedding
    
st.title("Agenda LLM")

# Initialize session and message history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display past messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# File uploader initialization
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

    # Convert user message to an embedding using OpenAI
    user_embedding = embedding.get_openai_embedding(prompt)

    if user_embedding:
        # Query Pinecone for the most relevant context
        retrieved_texts = embedding.query_pinecone(user_embedding)

        # Generate OpenAI assistant response
        with st.chat_message("assistant"):
            messages_for_openai = [{"role": "system", "content": "You are a helpful assistant answering the prompt of the user."}]
            messages_for_openai += st.session_state.messages

            if retrieved_texts:
                messages_for_openai.append({"role": "system", "content": f"Relevant information: {retrieved_texts}"})

            try:
                response = embedding.client.chat.completions.create(
                    model="gpt-4o",
                    messages=messages_for_openai
                )

                response_content = response.choices[0].message.content
                st.markdown(response_content)
            except Exception as e:
                st.error(f"Error generating assistant response: {e}")
                response_content = "Sorry, I couldn't generate a response. Please try again."

            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response_content})

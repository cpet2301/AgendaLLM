from openai import OpenAI
import pinecone
import streamlit as st

# OpenAI client
client = OpenAI()

# Create a Pinecone client instance
pc = pinecone.Pinecone()
index = pc.Index("testing")

st.title("ChatBot with Pinecone and OpenAI")

# Initialize session states
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display past messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle new input
if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Convert user message to an embedding using OpenAI
    embedding_response = client.embeddings.create(input=prompt, model="text-embedding-ada-002")
    user_embedding = embedding_response.data[0].embedding

    # Query Pinecone for the most relevant context
    result = index.query(queries=[user_embedding], top_k=3)

    # Retrieve and format results
    retrieved_texts = [match["metadata"]["text"] for match in result["matches"]]

    # Generate OpenAI response
    with st.chat_message("assistant"):
        messages_for_openai = [{"role": "system", "content": "You are a helpful assistant."}]
        messages_for_openai += st.session_state.messages
        if retrieved_texts:
            messages_for_openai.append({"role": "system", "content": f"Relevant information: {retrieved_texts}"})

        # Call OpenAI to generate a response based on the prompt and retrieved info
        response = client.chat.completions.create(model=st.session_state["openai_model"],
        messages=messages_for_openai)

        response_content = response.choices[0].message['content']
        st.markdown(response_content)

    # Add assistant response to the session
    st.session_state.messages.append({"role": "assistant", "content": response_content})

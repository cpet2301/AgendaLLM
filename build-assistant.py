from pinecone import Pinecone
import creds
pc = Pinecone(creds.api_key)

name = "MVPassistant" # any name you please
assistant = pc.assistant.create_assistant(
    assistant_name=name,
    metadata={
        "author": "James Briggs",
        "version": "0.1"
    }
)

pc.assistant.describe_assistant(assistant_name=name)

from pinecone import Pinecone
import creds
pc = Pinecone(creds.api_key)
metadata = {"author": "Jparker", "version": "1.0"}
assistant = pc.assistant.Assistant("agenda")

files = assistant.list_files()
print(files)
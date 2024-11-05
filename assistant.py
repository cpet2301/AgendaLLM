from pinecone import Pinecone
import creds
pc = Pinecone(creds.api_key)
metadata = {"author": "Parker", "version": "1.0"}
assistant = pc.assistant.Assistant("agenda")

#print(pc.assistant.list_assistants())


from pinecone_plugins.assistant.models.chat import Message

from pathlib import Path

# Use .rglob to match both .pdf and .PDF
pdf_paths = [str(p) for p in Path("C:\\repos\\AgendaLLM\\examplefiles").rglob("*.pdf")]

# Print the PDF paths for debugging
print(f"Found PDF files: {pdf_paths}")

example_path = Path("C:\\repos\\AgendaLLM\\examplefiles")
print(f"Expected directory path: {example_path.resolve()}")

# Check if files exist and print them
# for file in example_path.iterdir():
#     if file.is_file():
#         print(file.name)

files = []

# Upload the files
for pdf_path in pdf_paths:
    file_info = assistant.upload_file(
        file_path=pdf_path,
        timeout=-1  # Adjust as needed
    )
    files.append(file_info)

#files[0:]  # Show the list of uploaded files
complete = 0
for file_info in files:
    out = assistant.describe_file(file_id=file_info.id)
    if out.status == "Available":
        complete += 1

print(f"{complete} of {len(files)} files are complete")

# quick check that we're not getting ahead of ourselves
#assert complete == len(files), "make sure the above says '48 of 48 files are complete'"

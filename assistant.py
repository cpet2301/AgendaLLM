from pinecone import Pinecone
pc = Pinecone(api_key="4345f2c9-08f6-4f69-bcd6-3e78766b068d")
metadata = {"author": "Jane Doe", "version": "1.0"}
assistant = pc.assistant.Assistant("agenda")

#print(pc.assistant.list_assistants())


from pinecone_plugins.assistant.models.chat import Message

# msg = Message(
#     content="the agenda on october 10",
#     role="user"  # either "user" or "assistant"
# )

#assistant.chat_completions(messages=[msg])

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

from pinecone_plugins.assistant.models.chat import Message

msg = Message(
    content="tell me about the Mixtral 8x7B model",
    role="user"  # either "user" or "assistant"
)

assistant.chat_completions(messages=[msg])

from IPython.display import Markdown as md

# quick check that we're not getting ahead of ourselves
#assert complete == len(files), "make sure the above says '48 of 48 files are complete'"

# now run completion
out = assistant.chat_completions(messages=[msg])
md(out["choices"][0]["message"]["content"])


chat_history = [
    msg,
    Message(**out.choices[0].message.to_dict())
]

def chat(message: str):
    # create Message object
    msg = Message(content=message, role="user")
    # get response from assistant
    out = assistant.chat_completions(messages=[msg])
    assistant_msg = out.choices[0].message.to_dict()
    # add to chat_history
    chat_history.extend([msg, Message(**assistant_msg)])
    return md(assistant_msg["content"])
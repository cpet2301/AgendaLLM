from pinecone import Pinecone
import creds
pc = Pinecone(creds.api_key)
metadata = {"author": "Jparker", "version": "1.0"}
assistant = pc.assistant.Assistant("agenda")


from pinecone_plugins.assistant.models.chat import Message

msg = Message(
    content="tell what is coding club doing", ### here is where we change  for custom message
    role="user"  # either "user" or "assistant"
)


assistant.chat_completions(messages=[msg])

from IPython.display import Markdown as md

# quick check that we're not getting ahead of ourselves
#assert complete == len(files), "make sure the above says '48 of 48 files are complete'"

# now run completion
###
out = assistant.chat_completions(messages=[msg])
md(out["choices"][0]["message"]["content"])

print(out)
readable_response = out['choices'][0]['message']['content']
print(readable_response)

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

#chat("tell me about coding club")

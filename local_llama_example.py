from langchain_community.llms import Ollama

llm = Ollama(model="llama2")
prompt = "Tell me a joke about llama"

for chunks in llm.stream(prompt):
    print(chunks, end="")
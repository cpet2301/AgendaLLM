from langchain_ollama import OllamaLLM #pip install -U langchain-ollama

llm = OllamaLLM(model="codellama:7b")  # Use the correct model name
prompt = "tell a funny joke"

for chunk in llm.stream(prompt):
    print(chunk.content if hasattr(chunk, "content") else chunk, end="")
# Agenda LLM

## Contributers

### ...

## Development Setup
    ### VENV
     1.  python -m venv myenv
     2.  source myenv/bin/activate
     3.  pip install -r requierments.txt
    ### Local LLama

    ### Local Enviorment
      - Use Local Llama as the LLM to query for local development
    ### Local LLama Set Up
        1. [text](https://ollama.com/blog/run-code-llama-locally)  
        2. Access link and download local llama
            Note: Available with 7 billion, 13 billion (16GB+ of memory requirement) and 34 billion (32GB+ of memory requirement) parameters:
        3.Run the 7B parameter model in terminal: 
            ollama run codellama:7b
            ollama status (this checks makes sure its running)
                Debugging:(if status is not avalible):
                    - ollama start
                    - ollama pull llama2
                    - ollama run llama2:latest
            Go into local_llama_example.py to see an example of local llama
            Example Prompt: In Bash, how do I list all text files in the current directory (excluding subdirectories) that have been modified in the last month?

### In order to setup ... (fill this in!)
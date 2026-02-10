Write-Host "Downloading Ollama models into project directory..."

ollama pull llama3:8b-instruct-q4_K_M
ollama pull mistral:7b-instruct-q4_K_M
ollama pull phi3:medium
ollama pull nomic-embed-text

Write-Host "All models downloaded successfully."

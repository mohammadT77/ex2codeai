from langchain.llms.base import LLM
import requests

class OllamaLLM(LLM):
    base_url: str
    model: str
    """
    Custom LLM wrapper for Ollama server.
    """
    def __init__(self, base_url: str, model: str):
        """
        Args:
            base_url (str): Base URL of the Ollama server.
            model (str): Name of the model to use on the Ollama server.
        """
        super().__init__(base_url=base_url, model=model)

    @property
    def _llm_type(self) -> str:
        return "ollama"

    def _call(self, prompt: str, stop = None) -> str:
        """
        Make a request to the Ollama server and return the generated text.
        """
        url = f"{self.base_url}/api/generate"
        payload = {"model": self.model, "prompt": prompt, "stream": False}
        headers = {"Content-Type": "application/json"}
        
        # Send the request to the Ollama server
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        # Extract and return the generated text
        data = response.json()
        
        return data.get("response", "")
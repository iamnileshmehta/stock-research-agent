from abc import ABC, abstractmethod

class BaseLLM(ABC):
    """
    Universal interface for any LLM.
    Agent will ONLY talk to this class.
    """

    @abstractmethod
    def generate(self, prompt: str) -> str:
        """
        Take a prompt string and return the generated text from the LLM.
        """
        pass

    

    
import os
import openai

class AzureOpenAIService:
  def __init__(self):
    self.openai = openai
    self.openai.api_type = "azure"
    self.openai.azure_endpoint = os.getenv("AOAI_ENDPOINT")
    self.openai.api_version = os.getenv("AOAI_API_VERSION")
    self.openai.api_key = os.getenv("AOAI_API_KEY")

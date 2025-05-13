import os
import openai

class AzureOpenAIService:
  def __init__(self):
    self.openai = openai
    self.openai.api_type = "azure"
    self.openai.azure_endpoint = os.getenv("AOAI_ENDPOINT")
    self.openai.api_version = os.getenv("AOAI_API_VERSION")
    self.openai.api_key = os.getenv("AOAI_API_KEY")

  def get_embedding(self, input) -> list:
    """
    Azure OpenAI Serviceを使用してテキストをベクトル化する
    Args:
      text(str): ベクトル化するテキスト
    Returns:
      list: ベクトル化されたテキスト
    """
    try:
      print('Getting embedding from Azure OpenAI Service...')
      response = self.openai.embeddings.create(
        input=input,
        model=os.getenv("AOAI_EMBEDDING_DEPLOYMENT"),
      )
      embedding = response.data[0].embedding
      print(f'Embedding: {embedding}')
      return embedding
    except Exception as e:
      print(f'Exception at getEmbedding: {e}')
      raise e

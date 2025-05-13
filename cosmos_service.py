from azure.cosmos import CosmosClient, exceptions
import os

class CosmosService:
  
  def __init__(self):
    # CosmosDBのクライアントを初期化
    self.client = CosmosClient(
      url=os.getenv('COSMOS_URL'),
      credential=os.getenv('COSMOS_CREDENTIALS')
    )
    self.database = self.client.get_database_client(os.getenv('COSMOS_DATABASE_NAME'))
    self.container = self.database.get_container_client(os.getenv('COSMOS_CONTAINER_NAME'))
    
  def get_items_by_vector(self, embedding, VECTOR_SCORE_THRESHOLD):
    """
    CosmoDBからベクトルスコアが指定の閾値以上のアイテムを取得する
    
    Args:
    embedding(list): 検索クエリをベクトル化した値
    VECTOR_SCORE_THRESHOLD(float): ベクトルスコアの閾値
    Returns:
      list: ベクトルスコアが閾値以上のアイテムのリスト
    """
    try:
      print('Querying Cosmos DB...')
      print(f'VectorScoreThreshold: {VECTOR_SCORE_THRESHOLD}')
      query = f'SELECT * FROM c WHERE c.vector_score >= {VECTOR_SCORE_THRESHOLD}'
      
      query = f'SELECT TOP 10 c.file_name, c.page_number, c.content, VectorDistance(c.vector, @embedding) AS SimilarityScore FROM c WHERE VectorDistance(c.vector, @embedding) > {VECTOR_SCORE_THRESHOLD} ORDER BY VectorDistance(c.vector, @embedding)'
      
      parameters = [
        {'name': '@embedding', 'value': embedding}
      ]
      
      items = self.container.query_items(
        query=query,
        parameters=parameters,
        enable_cross_partition_query=True
      )
      
      resources = [item for item in items]
      for item in resources:
        print(f'{item["file_name"]} - {item["page_number"]} - {item["content"]}, {item["SimilarityScore"]}')
        
        return resources
    except exceptions.CosmosHttpResponseError as e:
      print(f'Cosmos DB error: {e}')
      return []
    except Exception as e:
      print(f'Error: {e}')
      return []

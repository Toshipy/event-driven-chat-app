import streamlit as st
from streamlit_chat import message

from openai_service import AzureOpenAIService
from cosmos_service import CosmosService
import os

# 環境変数から取得
AOAI_CHAT_DEPLOYMENT = os.getenv('AOAI_CHAT_DEPLOYMENT')
VECTOR_SCORE_THRESHOLD = float(os.getenv('VECTOR_SCORE_THRESHOLD'))

# システムプロンプトを設定
system_prompt_chat = """あなたはAIアシスタントです。問い合わせに対し「# 検索結果」の内容をもとに回答してください。

# 制約条件
- 検索結果がない場合は、一般的な情報から回答できる場合は回答してください。回答できない場合は不明瞭な回答をしてはいけません。
- 構造的に回答する必要がある場合は、Markdownで構造的に回答してください。
- チャット履歴の「参考情報」は無視してください。
- 「参考情報」はシステムが自動で付与しています。あなたの回答に含めてはいけません。
"""

# client
aoai_service = AzureOpenAIService()
cosmos_service = CosmosService()

st.set_page_config(layout='wide')
st.title('Udemy RAG')

# チャットメッセージを管理するsession_state
if 'chat_messages' not in st.session_state:
  st.session_state['chat_messages'] = []
  
# Sidebar
clear_button = st.sidebar.button("Clear Chat", key='clear_chat')

if clear_button:
  # チャットメッセージをクリア
  st.session_state['chat_messages'] = []
  st.rerun()  # ページを再読み込みして確実にクリアを反映

  
# ユーザーメッセージを入力するエリア
user_message = st.text_input("質問を入力してください")

# AIからの回答
assistant_text = ''

# 過去のチャットメッセージを表示
for text_info in st.session_state['chat_messages']:
  with st.chat_message(text_info['role'], avatar=text_info['role']):
    st.write(text_info['content'])
    
# ユーザーメッセージを送信したとき
if user_message:
  # ユーザーメッセージを表示
  with st.chat_message('user', avatar='user'):
    st.write(user_message)
  
  # ユーザーメッセージをsession_stateのchat_messageに保存
  st.session_state['chat_messages'].append({
      'role': 'user',
      'content': user_message
  })
  
  # CosmosDBでベクトル検索
  search_items = cosmos_service.get_items_by_vector(
      aoai_service.get_embedding(input=user_message),
      VECTOR_SCORE_THRESHOLD=0.7
  )
  
  # システムメッセージに検索結果を追加
  system_message = system_prompt_chat + "\n# 検索結果\n"
  
  # 画面に表示する検索結果
  display_searched_file = '\n\n# 参考情報\n'
  for index, result in enumerate(search_items):
    # ループ番号を付与してファイルの内容をシステムメッセージに追加
    system_message += f"\n\n--- {index+1} --- \n{result['content']}\n\n"
    # 画面に表示する検索結果にファイルの内容を追加
    display_searched_file += f"\n\n--- {index+1} --- \n{result['file_name']} (page{result['page_number']}) : {result['SimilarityScore']}\n\n"
  print(f'system_message:{system_message}')
  
  messges = [
      # システムメッセージ
      {
          'role': 'system',
          'content': system_message
      },
      *st.session_state['chat_messages'],
  ]
  
  # OpenAI Chat APIで回答を取得
  response = aoai_service.openai.chat.completions.create(
    model = AOAI_CHAT_DEPLOYMENT,
    messages = messges,
    stream = True,
  )
  
  # AIからの回答をStreamで表示
  with st.chat_message('assistant', avatar='assistant'):
    place_assisantant = st.empty()
    for chunk in response:
      if chunk.choices:
        content = chunk.choices[0].delta.content
        if content:
          assistant_text += content
          place_assisantant.write(assistant_text)
      else:
        content = None
    
  # AIからの回答をsession_stateのchat_messageに保存
  st.session_state['chat_messages'].append({
      'role': 'assistant',
      'content': assistant_text
  })

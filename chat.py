import streamlit as st
from streamlit_chat import message

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
  
  # TODO: AIからの回答を取得
  assistant_text = "AIの回答"  # ここにAIからの回答を取得する処理を追加
  
  # AIからの回答を表示
  with st.chat_message('assistant', avatar='assistant'):
    st.write(assistant_text)
    
  # AIからの回答をsession_stateのchat_messageに保存
  st.session_state['chat_messages'].append({
      'role': 'assistant',
      'content': assistant_text
  })

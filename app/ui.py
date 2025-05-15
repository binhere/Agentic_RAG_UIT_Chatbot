import streamlit as st
import requests

st.title("UIT Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

backend_url = "http://127.0.0.1:8000/chat"

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask something..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = requests.post(backend_url, json={"query": prompt})
            answer = response.json()["server_response"]['response']['blocks'][0]['text']
            st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})
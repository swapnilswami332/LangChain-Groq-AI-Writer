import requests
import streamlit as st

def get_response(endpoint: str, input_text: str) -> str:
    """POST the topic to the given server endpoint and return the text."""
    url = f"http://localhost:8000/{endpoint}"
    resp = requests.post(url, json={"topic": input_text}, timeout=10)
    resp.raise_for_status()
    return resp.json().get("response", "")

def fetch_with_ui(endpoint: str, text: str) -> str:
    try:
        return get_response(endpoint, text)
    except requests.RequestException as e:
        st.error(f"Request failed: {e}")
        return ""
# ...existing code...
st.title('Langchain Demo With GROQ API')
input_text = st.text_area("Write an essay on")
input_text1 = st.text_area("Write a poem on")

if input_text:
    st.write(fetch_with_ui('essay', input_text))

if input_text1:
    st.write(fetch_with_ui('poem', input_text1))
# ...existing code...
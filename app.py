### first you need to create modelfile
### and then create the model on your local system 
### ollama create codepreet -f  modelfile
import requests
import json
import streamlit as st

# API configuration
url = "http://localhost:11434/api/generate"
headers = {
    'Content-Type': 'application/json'
}

# Store conversation history
if 'history' not in st.session_state:
    st.session_state['history'] = []

def generate_response(prompt):
    st.session_state['history'].append(prompt)
    final_prompt = "\n".join(st.session_state['history'])
    data = {
        "model": "codepreet",
        "prompt": final_prompt,
        "stream": False
    }
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()  # Check for request errors
        
        # Extract the response from JSON
        data = response.json()
        actual_response = data.get('response', 'No response found')
        
        # Append the bot's response to history for continuity
        st.session_state['history'].append(actual_response)
        
        return actual_response
    except requests.exceptions.RequestException as e:
        st.error(f"Request failed: {e}")
        return "Error occurred. Please try again."

# Streamlit UI
st.title("Chat with CodePreet Model")
user_input = st.text_area("Ask a Question", placeholder="Type your message here...", height=100)

# If the user submits a question, generate a response
if st.button("Generate Response"):
    if user_input:
        response = generate_response(user_input)
        st.write("Response:", response)
    else:
        st.warning("Please enter a question before submitting.")

# Display chat history for user reference
if st.session_state['history']:
    st.subheader("Chat History")
    for i, message in enumerate(st.session_state['history']):
        role = "User" if i % 2 == 0 else "Bot"
        st.markdown(f"**{role}:** {message}")

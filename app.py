### first you need to create modelfile
### and then create the model on your local system 
### ollama create codepreet -f  modelfile
import requests
import json
import gradio as gr

url="http://localhost:11434/api/generate"
headers={
    'Content-Type':'application/json'
}

history=[]

def generate_response(prompt):
    history.append(prompt)
    final_prompt="\n".join(history)
    data={
        "model":"codepreet",
        "prompt":final_prompt,
        "stream":False
    }
    response = requests.post(url,headers=headers, data=json.dumps(data))

    if response.status==200:
        response=response.text
        data=json.load(response)
        actual_response=data['response']
        return actual_response
    else:
        print("[-] Error:", response.text)

interface=gr.Interface(
    fn=generate_response,
    inputs=gr.Textbox(lines=4,placeholder="Ask a Question"),
    outputs="text"
)

interface.launch(share=True)

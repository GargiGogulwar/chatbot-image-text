# 🤖 Bytez GPT-4o Chat + 🎨 DALL·E-2 Image Generator

This is a Streamlit app that lets you chat with **GPT-4o** and generate images using **DALL·E-2**, all powered via the [Bytez API](https://bytez.ai). Your API key stays local and is never uploaded to any server.

---

## Features

- 💬 Chat with GPT-4o in a conversation-style interface  
- 🖼️ Generate images with DALL·E-2 based on your prompts  
- 🔒 API key remains local on your machine  
- 🖥️ Easy to run with Streamlit  

---

## Requirements

- Python 3.10+  
- `streamlit`  
- `bytez` SDK  

Install dependencies:

```bash
pip install streamlit bytez
```
Setup

## Clone the repository:
```
git clone https://github.com/yourusername/bytez-chatbot.git
cd bytez-chatbot
```

Set your Bytez API key as an environment variable:

Windows (PowerShell):
```
setx BYTEZ_API_KEY "your_bytez_api_key_here"
```

macOS / Linux (bash/zsh):
```
export BYTEZ_API_KEY="your_bytez_api_key_here"
```

Run the app:
```
streamlit run app.py
```

### Open your browser at the URL Streamlit provides (usually http://localhost:8501).

## Usage

-Chat Tab: Type messages and talk to GPT-4o.

-Image Generation Tab: Enter a prompt, select number and size of images, and click Generate Image(s). Images will appear below.

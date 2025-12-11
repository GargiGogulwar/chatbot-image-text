import os
import streamlit as st
from bytez import Bytez

# -----------------------------
# CONFIG
# -----------------------------
api_key = os.getenv("BYTEZ_API_KEY")
if not api_key:
    st.error("❌ API key missing. Set BYTEZ_API_KEY environment variable.")
    st.stop()

client = Bytez(api_key)

CHAT_MODEL = "openai/gpt-4o"
IMAGE_MODEL = "openai/dall-e-2"

st.set_page_config(page_title="Bytez Chat + DALL·E", page_icon="🤖🎨", layout="wide")
st.title("🤖 Chat + 🎨 Image Generator")
st.caption("GPT-4o chat and DALL·E-2 image generation in one app.")

# -----------------------------
# Tabs
# -----------------------------
tab1, tab2 = st.tabs(["💬 Chat", "🖼️ Image Generation"])

# -----------------------------
# Chat Tab
# -----------------------------
with tab1:
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": "You are a helpful assistant."}
        ]

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    user_input = st.chat_input("Ask something...", key="chat_input")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        try:
            model = client.model(CHAT_MODEL)
            response = model.run(
                st.session_state.messages,
                params={"max_new_tokens": 300, "temperature": 0.7}
            )
            bot_reply = response.output.get("content", "⚠️ No content returned")

            with st.chat_message("assistant"):
                st.write(bot_reply)

            st.session_state.messages.append({"role": "assistant", "content": bot_reply})

        except Exception as e:
            st.error(f"API Error: {e}")

# -----------------------------
# Image Generation Tab
# -----------------------------
with tab2:
    prompt = st.text_area("Enter a prompt for DALL·E-2:", "", key="image_prompt")
    num_images = st.slider("Number of images", 1, 4, 1)
    size = st.selectbox("Image size", ["256x256", "512x512", "1024x1024"])

    if st.button("Generate Image(s)"):
        if not prompt.strip():
            st.warning("Please enter a prompt!")
        else:
            try:
                model = client.model(IMAGE_MODEL)

                # Correct: prompt is a plain string
                response = model.run(
                    prompt,
                    params={"n": num_images, "size": size}
                )

                # Handle response: could be a string or list of strings
                urls = response.output
                if isinstance(urls, str):
                    urls = [urls]  # convert single string to list

                if not urls:
                    st.error("⚠️ No images returned.")
                else:
                    st.subheader("Generated Image(s)")
                    for url in urls:
                        if isinstance(url, str) and url.startswith("http"):
                            st.image(url)
                        else:
                            st.warning(f"Invalid URL: {url}")

            except Exception as e:
                st.error(f"API Error: {e}")

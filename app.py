import os
import streamlit as st
from bytez import Bytez
import requests  # 👈 for downloading image bytes

# -----------------------------
# CONFIG
# -----------------------------
api_key = os.getenv("BYTEZ_API_KEY")
if not api_key:
    st.error("❌ API key missing. Set BYTEZ_API_KEY environment variable.")
    st.stop()

client = Bytez(api_key)

CHAT_MODEL = "openai/gpt-4o"
IMAGE_MODEL = "google/imagen-4.0-ultra-generate-001"

st.set_page_config(page_title="Chat + Image", page_icon="🤖🎨", layout="wide")
st.title("🤖 Chat + 🎨 Image Generator")
st.caption("Chat with GPT-4o and generate images using Google Imagen Ultra.")

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

    # Show chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # User input
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
    prompt = st.text_area("Enter a prompt for Imagen Ultra:", "", key="image_prompt")

    if st.button("Generate Image(s)"):
        if not prompt.strip():
            st.warning("Please enter a prompt!")
        else:
            try:
                # Load Imagen model
                model = client.model(IMAGE_MODEL)

                # Run the model (single response object)
                response = model.run(prompt)
                output = response.output  # could be a string or a list

                # Ensure we have a list of URLs
                if isinstance(output, str):
                    output = [output]

                if not output:
                    st.error("⚠️ No images returned.")
                else:
                    st.subheader("Generated Image(s)")
                    for idx, url in enumerate(output):
                        if isinstance(url, str) and url.startswith("http"):
                            try:
                                # Download image bytes
                                resp = requests.get(url)
                                resp.raise_for_status()
                                img_bytes = resp.content

                                # Show image
                                st.image(img_bytes, caption=f"Image {idx + 1}")

                                # Download button
                                st.download_button(
                                    label=f"⬇️ Download Image {idx + 1}",
                                    data=img_bytes,
                                    file_name=f"generated_image_{idx + 1}.png",
                                    mime="image/png",
                                    key=f"download_btn_{idx}",
                                )
                            except Exception as e:
                                st.warning(f"Could not download image: {e}")
                        else:
                            st.warning(f"Invalid URL: {url}")

            except Exception as e:
                st.error(f"API Error: {e}")

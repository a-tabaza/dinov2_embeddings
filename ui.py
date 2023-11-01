import streamlit as st
import chromadb
from PIL import Image

st.title("Ran Frames - DINOv2 Features")
client = chromadb.PersistentClient(path="db")
collection = client.get_or_create_collection(name="ran_frames_dinov2")

uploaded_file = st.file_uploader("Choose a file")
slider = st.slider("How many results?", 1, 25, 10)

if uploaded_file:
    frame = uploaded_file.name.split(".")[0]
    embedding = collection.get(ids=[frame], include=['embeddings'])['embeddings'][0]
    top_k = collection.query(query_embeddings=[embedding], n_results=slider, include=['metadatas'])

    frames = []
    for id in top_k['ids'][0]:
        path = f"ran_frames/{id}.jpg"
        image = Image.open(path)
        frames.append(image)

    st.image(frames)

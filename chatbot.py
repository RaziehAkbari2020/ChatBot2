import streamlit as st

st.app("My Streamlit App")

prompt = st.text_input("a girl with dark hair")

st.button("Generate Image", on_click=generate_image)

def generate_image():
    # Set up the OpenAI API
    openai.api_key = "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"

    # Create an image based on the prompt
    response = openai.Image.create(
        prompt=prompt,
        n=5,
        size="1024x1024"
    )

    # Get the URL of the generated image
    image_url = response['data'][0]['url']

    # Print the URL of the generated image
    print(image_url)

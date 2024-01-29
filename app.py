import streamlit as st
from dotenv import load_dotenv
from PIL import Image
import os
import google.generativeai as genai

load_dotenv()   #loading all environment varibles

genai.configure(api_key=os.getenv("AIzaSyBU81jRoaDdXXkL6jXM8NutE8qUM7qLRd8"))


def get_gemini_response(input_prompt, image):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input_prompt, image[0]])
    return response.text

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

#initialize the streamlit app

st.set_page_config(page_title="Gemini_Nutrionist_calories_calculator")

st.header("Gemini_Nutrionist_Cal_App")

uploaded_file = st.file_uploader("Choose a image...", type=['jpg', 'jpeg', 'png'])
image = ""

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)

submit = st.button("Tell me about the total calories")

input_prompt = """
 You are an expert in Nutrionist where you need to see the food items from the image and calculator the total calories, also provide the details of every food items with calories intake in below fromat
    1.Item 1 -no.of calories
    2.Item 2 - no.of calories
    ....
    finally you can also mention whether the food is healthy or not and also mention the percentage split of the ratio of carbohydrates, fats, fibres, sugar, and other things required in our diet"""

if submit:
    image_data = input_image_setup(uploaded_file)
    response_text = get_gemini_response(input_prompt, image_data)
    st.header("The Response is")
    st.write(response_text)

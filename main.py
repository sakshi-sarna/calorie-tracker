from dotenv import load_dotenv

load_dotenv() 

import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def get_gemini_repsonse(input,image):
    model=genai.GenerativeModel("gemini-1.5-flash")
    response=model.generate_content([input,image[0]])
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
    

st.set_page_config(page_title="Calorie Counter App")

st.header("Calorie Counter App")
# input=st.text_input("Input Prompt: ",key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image=""   
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_container_width =True)


submit=st.button("Tell me the total calories")

input_prompt="""
You are an expert in nutritionist where you need to see the food items from the image
               and estimate the total calories. You will not be given specific ingredients and quantities used.
               Give your response according to the picture only.
               Don't use negative sentences like "It's impossible to give precise calorie counts".
               Provide the details of every food items with calories intake
               is below format

               1. Item 1 - no of calories
               2. Item 2 - no of calories
               ----
               ----
Apart from this provide nutritional information breakup :-
1. Macronutrients - protein, carbohydrates, fiber and fats
2. Micronutrients - iron, vitamins, calcium, etc.
"""

## If submit button is clicked

if submit:
    image_data=input_image_setup(uploaded_file)
    response=get_gemini_repsonse(input_prompt,image_data)
    st.subheader("The Response is")
    st.write(response)
import os 
from dotenv import load_dotenv

import streamlit as st 
import google.generativeai as genai

from PIL import Image
from io import BytesIO


# Configure api key 
genai.configure(api_key = os.getenv('GOOGLE_API_KEY'))


## LOad anf get response from gemini-pro-vision model

def get_gemini_repsonse(input,image,prompt):
    model=genai.GenerativeModel('gemini-pro-vision')
    response=model.generate_content([input,image[0],prompt])
    return response.text





#image setup 

def image_setup(image):
    if image is not None:

        # Read the file into bytes

        image_bytes = image.getvalue()

        # Get the media type of the image 

        image_parts = [
            {
                "mime_type": image.type,  
                "data": image_bytes
            }
        ]

        return image_parts
    else:
        raise FileNotFoundError("No Image is uploaded")
    


st.set_page_config(page_title="Gemini Health App")

st.header("Gemini Health App")
input=st.text_input("Input Prompt: ",key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image=""   
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)


submit=st.button("Tell me the total calories and description of Image Uploaded")

input_prompt= """
                    You are an expert in nutritionist where you need to see the food items from the image
                    and give description of those food,ingredients,recipe and calculate the total calories, also provide the details of every food items with calories intake
                    is below format

                    **1.description, ingredients,recipe , benifits, Vitamins in that food of the food**

                    **2. Item 1 -**  no of calories

                    **3. Item 2 -**  no of calories
                    ----
                    ----
                    """

## If submit button is clicked

if submit:
    image_data=image_setup(uploaded_file)
    response=get_gemini_repsonse(input_prompt,image_data,input)
    st.subheader("The Response is")
    st.write(response)
    







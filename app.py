from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import os
from PIL import Image
import pdf2image
import google.generativeai as genai
import io
import base64

genai.configure(api_key=os.getenv("API_KEY"))

def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        ## Convert given pdf to image
        images = pdf2image.convert_from_bytes(uploaded_file.read())

        first_page = images[0]

        ## Convert to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type":"image/jpeg",
                "data":base64.b64encode(img_byte_arr).decode() ##encode to base64
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No File Uploaded")

## Creating the Streamlit app

st.set_page_config(page_title= "ATS Resume Expert")
st.header("ATS Tracking system")
input_text = st.text_area("What is the job desciption?", key="input")
uploaded_file = st.file_uploader("Upload your resume(PDF)", type=["pdf"])

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")

submit1 = st.button("Tell me about the Resume")
#submit2 = st.button("How can i improve my Skills?")
submit3 = st.button("What are the Missing Keywords?")
submit4 = st.button("Percentage Match?")

input_prompt1 = """
    You are an experienced HR with experience in the field of Data Science, Data Analyst, your task is to review the provided resume against the job description.
    Please provide your professional evaluation as to whether the candidate's profile aligns with the role.
    Highlight the strenghts and weaknesses of the applicant in realtion to the specified job requirements.
"""
input_prompt3 = """
    You are a skilled ATS(Application Tracking System) with a deep understanding of Data Science, Data Analytics, and deep ATS functionality. 
    Parse throught the job description and compare it to the candidate's profile and extract all the key words that the candidate is missing in their application.
    Highlight strategies on how to implement these key words in an efficient and seemless manner in order to increase their chances of being selected for similar roles.
"""
input_prompt4 = """
    You are a skilled ATS(Application Tracking System) with a deep understanding of Data Science, Data Analytics, and deep ATS functionality.
    Your task if to evaluate the resume against the provided job descriptio. Give me the percentage of match if the resume matches
    the job description. First the output should come as percentage, then the keywords missing, followed by some final insights.
"""

if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt1,pdf_content,input_text)
        st.subheader("The response is:")
        st.write(response)
    else:
        st.write("Please upload the resume")
elif submit3:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt3,pdf_content,input_text)
        st.subheader("The response is:")
        st.write(response)
    else:
        st.write("Please upload the resume")    
elif submit4:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt4,pdf_content,input_text)
        st.subheader("The response is:")
        st.write(response)
    else:
        st.write("Please upload the resume")
import streamlit as st
import tempfile
import os
import json
from processing_pipeline import process_document
import re

def clean_json_block(gpt_response: str) -> str:
    match = re.search(r"```json\n(.*?)```", gpt_response, re.DOTALL)
    return match.group(1).strip() if match else gpt_response.strip()

st.set_page_config(page_title= "Insurance Document Extraction", page_icon=":clipboard:", layout="wide")
st.title("Form Extractor - ביטוח לאומי")

#file upload
uploaded_file = st.file_uploader("Upload a scanned form", type=["pdf"])

if uploaded_file:
    # save file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
        tmp_file.write(uploaded_file.read())
        temp_path = tmp_file.name

    with st.spinner("Extracting fields..."):
        try:
            result = process_document(temp_path)
            cleaned = clean_json_block(result)
            parsed = json.loads(cleaned)

        except Exception as e:
            st.error(f"Failed to extract fields: {e}")
            st.stop()

    st.success("Extraction successful!")

    st.subheader("Extracted Data:")
    st.json(parsed)

    # issues = validate_extracted_fields(parsed)


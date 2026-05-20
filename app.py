import streamlit as st
import pandas as pd
from portal_automation import run_automation

st.set_page_config(page_title="RPA File Uploader", layout="centered")

st.title("RPA - CSV File Uploader")
st.write("Upload your CSV or Excel file, review the data, and then submit it to the portal.")

uploaded_file = st.file_uploader("Upload your file here", type=["csv", "xlsx", "xls"])

if uploaded_file is not None:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    # Fix date columns format
    date_columns = ["Complaince Date", "Verification Date", "Target Date"]
    for col in date_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col]).dt.strftime("%d-%b-%y")

    st.success(f"File uploaded successfully! Total entries: {len(df)}")
    st.subheader("File Data:")
    st.dataframe(df, use_container_width=True)

    st.markdown("---")

    if st.button("Submit to Portal", type="primary"):
        st.info("Portal automation is starting... Chrome will open shortly.")
        try:
            run_automation(df)
            st.success("All entries have been submitted successfully!")
        except Exception as e:
            st.error(f"An error occurred: {e}")
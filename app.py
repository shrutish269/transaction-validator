import streamlit as st
import pandas as pd

from validator import validate_data
from utils import split_dataframe

st.set_page_config(
    page_title="Transaction Validator",
    layout="wide"
)

st.title("Transaction Data Validation & Processing Platform")

st.info("""
Upload transaction datasets containing order details, product details and payment information.

The platform performs country-based phone validation, date validation, payment mode validation,
data integrity checks, generates cleaned output files and automatically splits large CSV files
into manageable chunks.
""")

st.markdown("""
### Features

✅ Country-based phone validation

✅ Date validation

✅ Payment mode validation

✅ Missing value detection

✅ Error report generation

✅ Cleaned CSV download

✅ CSV chunking
""")

uploaded_file = st.file_uploader(
    "Upload Transaction CSV",
    type=["csv"]
)

if uploaded_file:

    df = pd.read_csv(uploaded_file)

    st.subheader("Uploaded Data")

    st.dataframe(df)

    if st.button("Validate Data"):

        clean_df, error_df = validate_data(df)

        st.success("Validation Completed Successfully")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Valid Rows",
                len(clean_df)
            )

        with col2:
            st.metric(
                "Invalid Rows",
                len(error_df)
            )

        # Validation Summary

        if not error_df.empty:

            summary = {
                "Invalid Phone": 0,
                "Invalid Payment Mode": 0,
                "Invalid Date": 0,
                "Missing Value": 0
            }

            for error in error_df["errors"]:

                if "Invalid Phone" in error:
                    summary["Invalid Phone"] += 1

                if "Invalid Payment Mode" in error:
                    summary["Invalid Payment Mode"] += 1

                if "Invalid Date" in error:
                    summary["Invalid Date"] += 1

                if "Missing Value" in error:
                    summary["Missing Value"] += 1

            summary_df = pd.DataFrame(
                summary.items(),
                columns=[
                    "Validation Type",
                    "Count"
                ]
            )

            st.subheader(
                "Validation Summary"
            )

            st.dataframe(summary_df)

        st.subheader("Error Report")

        st.dataframe(error_df)

        st.subheader("Cleaned Data")

        st.dataframe(clean_df)

        # Downloads

        st.download_button(
            label="Download Clean CSV",
            data=clean_df.to_csv(index=False),
            file_name="cleaned_transactions.csv",
            mime="text/csv"
        )

        st.download_button(
            label="Download Error Report",
            data=error_df.to_csv(index=False),
            file_name="validation_report.csv",
            mime="text/csv"
        )

        # CSV Chunking

        st.subheader("CSV Chunks")

        chunks = split_dataframe(
            clean_df,
            chunk_size=1000
        )

        for i, chunk in enumerate(chunks):

            st.download_button(
                label=f"Download Chunk {i+1}",
                data=chunk.to_csv(index=False),
                file_name=f"chunk_{i+1}.csv",
                mime="text/csv"
            )
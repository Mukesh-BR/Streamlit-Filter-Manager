import pandas as pd
import streamlit as st

st.set_page_config(layout="centered", page_title="Data Editor")

st.title("View Meta Table of survey questions")
st.caption("This is a view of editable Meta Table")

st.write("")

""" This table show a quick example of survey questions we have recorded along with the answers."""
# df = pd.DataFrame(data)
df =  pd.read_csv("/Users/mukeshbr/alpharoc_interview/data_editor/data/dev_meta.csv")


annotated = st.data_editor(df, hide_index=True, use_container_width=True, disabled=["questionid", "answerid"])

st.download_button(
    "⬇️ Download meta dataset as .csv", annotated.to_csv(), "annotated.csv", use_container_width=True
)

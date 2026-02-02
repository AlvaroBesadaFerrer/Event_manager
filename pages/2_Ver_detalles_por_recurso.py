import streamlit as st
from utils.format_utils import show_resources_details


st.set_page_config(page_title="Ver detalles de recursos", page_icon=":hammer_and_wrench:")

st.markdown("# Detalles de recursos :red_car:")

st.dataframe(show_resources_details())
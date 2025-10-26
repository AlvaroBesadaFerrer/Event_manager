import streamlit as st
from streamlit_timeline import st_timeline
from datetime import datetime
from uuid import uuid4
from save_load_data import load_data
from dateutil import parser

st.set_page_config(layout="wide")

data = load_data()
items = []

for event in data:
    st.write(data[event])
    items.append({
        "id": uuid4(),
        "content": data[event]["event_type"],
        "start": str(datetime.combine(parser.parse(data[event]["start_date"]), parser.parse(data[event]["start_time"]))),
        "end": str(datetime.combine(parser.parse(data[event]["start_date"]), parser.parse(data[event]["end_time"]))),
    })


timeline = st_timeline(items, groups=[], options={}, height="300px")
st.subheader("Selected item")
st.write(timeline)
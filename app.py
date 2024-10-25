import streamlit as st

experiential_knowledge_generator_page = st.Page("pages/experiential-knowledge.py", title="Generate Experiential Knowledge", icon="💼")
proposal_generator_page = st.Page("pages/proposal-generator.py", title="Generate Project Proposal", icon="🗂️")

pg = st.navigation([experiential_knowledge_generator_page, proposal_generator_page])
st.set_page_config(page_title="Utility - Manager", page_icon="🚀")
pg.run()
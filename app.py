import streamlit as st

st.set_page_config(
    page_title="Research AI Agent",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 AI Research Assistant")
st.write("Research any topic using Mistral AI, Wikipedia, and DuckDuckGo.")

query = st.text_input(
    "Enter your research topic",
    placeholder="Example: Artificial Intelligence"
)

if st.button("Generate Research"):

    with st.spinner("Researching..."):

        # Call your agent here
        response = "Your research output"

    st.success("Research Completed")

    st.markdown(response)

    st.download_button(
        "Download Report",
        response,
        file_name="research.txt"
    )
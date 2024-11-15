import streamlit as st
from scholarly import scholarly
import time

def fetch_top_researchers_by_area(research_area):
    try:
        # Search for researchers by the research area
        search_query = scholarly.search_keyword(research_area)
        top_researchers = []
        
        # Fetch the top 20 researchers
        for _ in range(20):
            try:
                researcher = next(search_query)
                researcher = scholarly.fill(researcher)  # Load full profile
                name = researcher.get("name", "Name not available")
                citations = researcher.get("citedby", "Citations not available")
                h_index = researcher.get("hindex", "h-index not available")
                i10_index = researcher.get("i10index", "i10-index not available")
                top_researchers.append({
                    "name": name,
                    "citations": citations,
                    "h_index": h_index,
                    "i10_index": i10_index
                })
            except StopIteration:
                break  # Stop if no more researchers are found

        return top_researchers
    except Exception as e:
        return f"Error fetching data: {e}"

# Streamlit Interface
st.title("Top 20 Researchers by Research Area")

# Input for research area
research_area = st.text_input("Enter a research area (e.g., 'machine learning', 'climate change'):")

if st.button("Search"):
    if research_area:
        with st.spinner("Searching..."):
            researchers = fetch_top_researchers_by_area(research_area)
            if isinstance(researchers, str):  # Check if error occurred
                st.error(researchers)
            elif researchers:
                st.success("Search completed successfully!")
                for i, researcher in enumerate(researchers, start=1):
                    st.subheader(f"{i}. {researcher['name']}")
                    st.write(f"Citations: {researcher['citations']}")
                    st.write(f"h-index: {researcher['h_index']}")
                    st.write(f"i10-index: {researcher['i10_index']}")
                    st.write("---")
            else:
                st.warning("No researchers found for the given area.")
    else:
        st.warning("Please enter a research area.")

# Add source and developer credit at the end of the application
st.write("Source: Google Scholar.")
st.markdown("<p><strong>Tool developed by Darliane Cunha.</strong></p>", unsafe_allow_html=True)

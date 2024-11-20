import streamlit as st
from scholarly import scholarly
import time

# Function to fetch top researchers by a research area
def fetch_top_researchers_by_area(research_area, max_results=20):
    """
    Fetches top researchers for a given research area from Google Scholar.
    
    Args:
        research_area (str): The area of research to search for.
        max_results (int): Maximum number of researchers to fetch.
    
    Returns:
        list: A list of dictionaries with researcher details.
    """
    try:
        search_query = scholarly.search_keyword(research_area)
        top_researchers = []
        
        for _ in range(max_results):
            try:
                researcher = next(search_query)
                researcher = scholarly.fill(researcher)  # Load full profile
                
                # Extract relevant information
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
                break  # No more researchers available
            except Exception as inner_error:
                st.error(f"Error processing a researcher: {inner_error}")
        
        return top_researchers
    
    except Exception as e:
        st.error(f"Error fetching data from Google Scholar: {e}")
        return []

# Streamlit Interface
st.title("Top Researchers by Research Area")

# Input for research area
research_area = st.text_input(
    "Enter a research area (e.g., 'machine learning', 'climate change'):",
    placeholder="Type the research area here..."
)

# Fetch results on button click
if st.button("Search"):
    if research_area.strip():  # Validate input
        with st.spinner("Searching for researchers..."):
            researchers = fetch_top_researchers_by_area(research_area.strip())
            
            if researchers:
                st.success(f"Found {len(researchers)} researchers in the area '{research_area}'.")
                
                # Display results with expanders
                for i, researcher in enumerate(researchers, start=1):
                    with st.expander(f"{i}. {researcher['name']}"):
                        st.write(f"- **Citations**: {researcher['citations']}")
                        st.write(f"- **h-index**: {researcher['h_index']}")
                        st.write(f"- **i10-index**: {researcher['i10_index']}")
            else:
                st.warning(f"No researchers found for the area '{research_area}'.")
    else:
        st.warning("Please enter a valid research area.")

# Footer with source and credit
st.write("---")
st.markdown("**Source**: Google Scholar")
st.markdown(
    "<p><strong>Tool developed by Darliane Cunha.</strong></p>", 
    unsafe_allow_html=True
)


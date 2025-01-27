##BASE TEMPLATE FOR SEARCH ENGINE
import streamlit as st
def search(query):
    return query
def search_engine_app():
    st.set_page_config(page_title="IRSearch Engine", layout="centered")

    st.title("🔍IR Search Engine")

    # Subtitle
    st.subheader("Find the information you're looking for, quickly and easily!")

    # Create a search input box
    search_query = st.text_input("Enter your search query below:", placeholder="Type something to search...")

    if st.button("Search"):
        if search_query.strip():
            st.info(f"Searching for: **{search_query}**")

            results = search(search_query)

            if results:
                st.write("### Search Results:")
                for idx, result in enumerate(results, start=1):
                    st.write(f"{idx}. [{result['title']}]({result['url']})")
                    st.write(result['snippet'])
                    st.markdown("---")
            else:
                st.warning("No results found. Try a different query!")
        else:
            st.warning("Please enter a search query to get started.")


if __name__ == "__main__":
    search_engine_app()

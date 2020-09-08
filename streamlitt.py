import streamlit as st
import awesome_streamlit as ast
import src.pages.daily_report as dr

ast.core.services.other.set_logging_format()

PAGES = {
    "Daily Report": dr,
}

def main():
    """Main function of the App"""
    st.sidebar.title("Menu")
    selection = st.sidebar.radio("Go to", list(PAGES.keys()))

    page = PAGES[selection]

    with st.spinner(f"Loading {selection} ..."):
        ast.shared.components.write_page(page)

if __name__ == "__main__":
    main()
import streamlit as st


# Homepage function
def main():
    st.title("Welcome to the Multi-Page Streamlit App")
    st.write("This is the homepage. Use the sidebar to navigate between different pages.")

    # Instructions to use the sidebar
    st.write("Select the page from the sidebar to start answering questions.")


if __name__ == "__main__":
    main()
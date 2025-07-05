import streamlit as st
from few_shot import FewShotPosts
from post_generator import generate_post


# Options for length and language
length_options = ["Short", "Medium", "Long"]


# Main app layout
def main():
    st.header("LinkedIn Post Generator", divider=True)
    st.subheader("Hey Deepika!")
    st.subheader("What kind of content do you want today?")


    with st.container(border=True):
        # Create three columns for the dropdowns
        col1, col2, col3 = st.columns(3)

        fs = FewShotPosts()
        themes = fs.get_themes()
        target_audience=fs.get_target_audience()
        
        with col1:
            # Dropdown for Length
            selected_length = st.selectbox("Length",options=length_options)

        with col2:
            # Dropdown for Theme
            selected_theme = st.selectbox("Theme", options=themes)

        with col3:
            # Dropdown for Target audience
            selected_target_audience = st.selectbox("Target audience", options=target_audience)


        # Generate Button
        if st.button("📝Generate post",type="secondary"):
            post = generate_post(selected_length, selected_theme, selected_target_audience)
            st.write(post)
            st.success("Post generation successful 😀")
            st.feedback("thumbs")
            # st.markdown(":green-badge[✅ Success]")
    

# Run the app
if __name__ == "__main__":
    main()

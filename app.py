import streamlit as st
from api_calling import note_generator, audio_transcription, quiz_generator
from PIL import Image

# title
st.title("Note Summary and Quiz Generator", anchor=False)
st.markdown("Upload upto 3 images to generate Note Summary and Quizzes")
st.divider()

# control interface
with st.sidebar:
    st.header("Controls")

    # upload images
    images = st.file_uploader(
        "Upload the photos of your notes",
        type=['jpg', 'jepg', 'png'],
        accept_multiple_files=True
    )

    # converting <ST Image> to <PIT Image>
    pil_images = [Image.open(img) for img in images]

    # show uploaded images
    if images:
        if len(images) > 3:
            st.error("Upload at max 3 images")
        
        else:
            st.subheader("Uploaded Images")

            col = st.columns(len(images))

            for i, img in enumerate(images):
                with col[i]:
                    st.image(img)

    # difficulty
    selected_option = st.selectbox(
        "Enter the difficulty of your quiz",
        ("Easy", "Midium", "Hard"),
        index=None
    )

    if selected_option:
        st.markdown(f"You selected ***{selected_option}*** as difficulty of your quiz")

    # submit difficulty 
    pressed = st.button("Click the button to initiate AI", type="primary")

# submit
if pressed:
    # check image upload
    if not images:
        st.error("You must upload 1 image")
    
    # check select difficulty
    if not selected_option:
        st.error("You must select a difficulty")

    # if valid input
    if images and selected_option:
        # note
        with st.container(border=True):
            st.subheader("Your Notes")

            with st.spinner("AI is generating notes for you..."):
                generated_notes = note_generator(pil_images)
                st.markdown(generated_notes)

        # audio transcipt
        with st.container(border=True):
            st.subheader("Your Audio Transciption")

            with st.spinner("AI is generating audio transcript for you..."):
                # removing markdown symbol from the notes
                generated_notes = generated_notes.replace("#","")
                generated_notes = generated_notes.replace("*","")
                generated_notes = generated_notes.replace("_","")
                generated_notes = generated_notes.replace("-","")
                generated_notes = generated_notes.replace("`","")

                audio_transcript = audio_transcription(generated_notes)
                st.audio(audio_transcript)

        # quiz
        with st.container(border=True):
            st.subheader("Your Quiz. Diffeirculty: {selected_option}")

            with st.spinner("AI is generating quizzes for you..."):
                quizzes = quiz_generator(pil_images, selected_option)
                st.markdown(quizzes)

            
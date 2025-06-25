import streamlit as st
import lyricsgenius
import requests
import re
import os
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from dotenv import load_dotenv
import base64
from io import BytesIO

# Load environment variables
load_dotenv()

# Set page configuration
st.set_page_config(
    page_title="Taylor Swift Lyrics Visualizer",
    page_icon="🎵",
    layout="centered"
)

# Custom CSS
def add_bg_from_url():
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: linear-gradient(to bottom, #f8bbd0, #ffccbc);
            background-attachment: fixed;
            background-size: cover;
        }}
        .title {{
            font-family: 'Playfair Display', serif;
            font-size: 3rem;
            color: #7b1fa2;
            text-align: center;
            margin-bottom: 2rem;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
        }}
        .subtitle {{
            font-family: 'Montserrat', sans-serif;
            font-size: 1.5rem;
            color: #6a1b9a;
            text-align: center;
            margin-bottom: 2rem;
        }}
        .lyrics-container {{
            background-color: rgba(255, 255, 255, 0.8);
            color: #4A148C;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            max-height: 400px;
            overflow-y: auto;
            font-family: 'Montserrat', sans-serif;
            line-height: 1.6;
            white-space: pre-wrap;
        }}
        .stButton>button {{
            background-color: #7b1fa2;
            color: white;
            border-radius: 20px;
            padding: 10px 25px;
            font-weight: bold;
            border: none;
            transition: all 0.3s ease;
        }}
        .stButton>button:hover {{
            background-color: #6a1b9a;
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }}
        .footer {{
            text-align: center;
            margin-top: 2rem;
            font-size: 0.8rem;
            color: #6a1b9a;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Load fonts
def load_fonts():
    st.markdown(
        """
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600&family=Playfair+Display:wght@700&display=swap" rel="stylesheet">
        """,
        unsafe_allow_html=True
    )

# Fetch lyrics from Genius
def get_lyrics(song_title, artist="Taylor Swift"):
    api_key = os.getenv("GENIUS_API_KEY")
    if not api_key:
        st.error("⚠️ Genius API key not found. Please set it in the .env file.")
        return None

    try:
        genius = lyricsgenius.Genius(api_key, timeout=10, retries=2)
        genius.skip_non_songs = True
        genius.remove_section_headers = True
        genius.excluded_terms = ["(Remix)", "(Live)"]
        
        song = genius.search_song(song_title, artist)
        if song and song.lyrics:
            lyrics = song.lyrics
            match = re.search(r"\n\n(.*)", lyrics, re.DOTALL)
            if match:
                return match.group(1).strip()
            else:
                return lyrics.strip()
        else:
            return None

    except Exception as e:
        st.error(f"Error fetching lyrics: {e}")
        return None


# Generate word cloud
def generate_wordcloud(lyrics):
    cleaned_lyrics = re.sub(r'[^\w\s]', '', lyrics.lower())

    stopwords = set(WordCloud().stopwords).union({
        'oh', 'yeah', 'la', 'na', 'ooh', 'ah', 'eh', 'mm', 'mmm', 'uh', 'um',
        'like', 'get', 'got', 'know', 'go', 'going', 'gone', 'gonna', 'wanna', 'gotta', 'cause'
    })

    wordcloud = WordCloud(
        width=800, height=400,
        background_color='white',
        colormap='magma',
        contour_width=1,
        contour_color='#7b1fa2',
        stopwords=stopwords,
        max_words=100,
        max_font_size=100,
        random_state=42
    ).generate(cleaned_lyrics)

    buf = BytesIO()
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.savefig(buf, format='png', dpi=300, bbox_inches='tight', pad_inches=0)
    buf.seek(0)
    plt.close()
    return buf

# Convert image to base64
def get_image_as_base64(buf):
    return base64.b64encode(buf.getvalue()).decode()

# Main App
def main():
    add_bg_from_url()
    load_fonts()
    
    st.markdown('<h1 class="title">✨ Taylor Swift Lyrics Visualizer ✨</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Explore the words behind the music</p>', unsafe_allow_html=True)
    
    song_title = st.text_input("Enter a Taylor Swift song title:", placeholder="e.g. Love Story, Blank Space, All Too Well")

    if st.button("Visualize Lyrics"):
        if song_title:
            with st.spinner('Fetching lyrics... 🎵'):
                lyrics = get_lyrics(song_title)
                
                if lyrics:
                    st.subheader(f"📝 Lyrics for '{song_title}'")
                    st.markdown(f'<div class="lyrics-container">{lyrics}</div>', unsafe_allow_html=True)

                    with st.spinner('Generating word cloud... 🔮'):
                        wordcloud_buf = generate_wordcloud(lyrics)
                        st.subheader("🌟 Word Cloud")
                        st.image(wordcloud_buf, use_column_width=True)

                        st.download_button(
                            label="Download Word Cloud",
                            data=wordcloud_buf,
                            file_name=f"{song_title.replace(' ', '_')}_wordcloud.png",
                            mime="image/png"
                        )
                else:
                    st.error(f"❌ Couldn't find lyrics for '{song_title}'. Please check the song title and try again.")
        else:
            st.warning("⚠️ Please enter a song title.")

    st.markdown('<div class="footer">Made with 💖 for Swifties everywhere</div>', unsafe_allow_html=True)

# Run app
if __name__ == "__main__":
    main()

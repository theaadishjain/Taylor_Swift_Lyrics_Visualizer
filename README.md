# Taylor Swift Lyrics Visualizer 🎵✨

A beautiful Streamlit web application that allows users to visualize Taylor Swift's song lyrics as word clouds.

![App Screenshot](screenshot.png)

## Features

- 🔍 Search for any Taylor Swift song by title
- 📝 View the complete lyrics in a stylish, scrollable container
- 🌈 Generate a beautiful word cloud visualization of the lyrics
- 💾 Download the generated word cloud as an image
- 🎨 Enjoy a visually appealing UI with Taylor Swift-inspired design

## Tech Stack

- Python
- Streamlit
- Genius API (via requests)
- WordCloud & Matplotlib for visualization
- python-dotenv for environment variable management

## Setup Instructions

### Prerequisites

- Python 3.7 or higher
- Genius API key (get one from [Genius API](https://genius.com/api-clients))

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/taylor-swift-lyrics-visualizer.git
   cd taylor-swift-lyrics-visualizer
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your Genius API key:
   - Rename `.env.example` to `.env`
   - Replace `your_genius_api_key_here` with your actual Genius API key

### Running the App Locally

```bash
streamlit run app.py
```

The app will open in your default web browser at `http://localhost:8501`.

## Deployment on Streamlit Community Cloud

1. Push your code to a GitHub repository

2. Go to [Streamlit Community Cloud](https://streamlit.io/cloud)

3. Sign in with your GitHub account

4. Click on "New app"

5. Select your repository, branch, and the main file path (`app.py`)

6. Add your Genius API key as a secret:
   - In the app settings, go to "Secrets"
   - Add your API key in the following format:
     ```
     GENIUS_API_KEY=your_genius_api_key_here
     ```

7. Deploy your app

## Creating Your Own Genius API Key

1. Go to [Genius API Clients](https://genius.com/api-clients)
2. Sign in or create an account
3. Create a new API client
4. Fill in the required information
5. Get your Client Access Token
6. Add this token to your `.env` file

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

Made with 💖 for Swifties everywhere
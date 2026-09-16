# Buddy AI

A friendly AI chatbot built with Python and Streamlit.

## Features

- Interactive chat interface with Buddy AI
- Customizable bot name
- Context-aware responses (greetings, help, jokes, etc.)
- Chat history persistence during session
- Clean, modern UI with Streamlit
- Sidebar settings panel

## Installation

1. Make sure you have Python 3.7+ installed
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

To start the Buddy AI chat interface:

```bash
streamlit run app.py
```

Or alternatively:

```bash
python -m streamlit run app.py
```

The application will open in your web browser at http://localhost:8501

## Project Structure

- `app.py` - Main Streamlit application
- `requirements.txt` - Python dependencies
- `README.md` - This file

## Customization

You can customize Buddy AI by:

1. Changing the bot's name in the sidebar
2. Modifying the response logic in `generate_buddy_response()` function
3. Adding new response categories or enhancing existing ones
4. Adjusting the UI styling or layout

## Dependencies

- Streamlit >= 1.64.0

## Notes

This is a simple prototype designed to demonstrate basic chatbot functionality. For production use, you might want to:

- Add persistent chat history storage
- Integrate with actual AI/LLM APIs
- Add user authentication
- Enhance security features
- Add more sophisticated natural language processing

Enjoy chatting with your AI buddy! 🤖💬
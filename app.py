import streamlit as st
import time, random, requests, re, io
import pymupdf as fitz  # PyMuPDF
from datetime import datetime

DEFAULT_GEMINI_API_KEY = "AQ.Ab8RN6J6QPqVVNRKaakkgsYTistm2GJudxQWh4flHvZksAzvYA"



def _word_in_text(text, word):
    return bool(re.search(r"" + re.escape(word) + r"", text))

def _phrase_in_text(text, phrase):
    return phrase in text

def generate_buddy_response(user_input, buddy_name):
    """Generate a simple response based on user input"""
    user_input_lower = user_input.lower()
    
    # Greeting responses
    if any(_word_in_text(user_input_lower, w) for w in ["hello", "hi", "hey", "greetings"]):
        responses = [
            f"Hello there! I'm {buddy_name}, your friendly AI buddy! 👋",
            f"Hey! {buddy_name} here! How's your day going? 😊",
            f"Hi! Great to see you! I'm {buddy_name}, ready to help! ✨"
        ]
        return random.choice(responses)
    
    # How are you responses
    elif any(_phrase_in_text(user_input_lower, p) for p in ["how are you", "how do you do", "how's it going"]):
        responses = [
            f"I'm doing great! Thanks for asking. How about you? 😊",
            f"I'm feeling fantastic today! Ready to chat with you! 💫",
            f"Doing awesome! Always happy to talk with a friend like you! 🤗"
        ]
        return random.choice(responses)
    
    # Help/request responses
    elif any(_word_in_text(user_input_lower, w) for w in ["help", "assist", "support"]) or _phrase_in_text(user_input_lower, "can you"):
        responses = [
            f"Of course! I'm here to help you with whatever you need. What can I do for you today? 🤝",
            f"You've got it! {buddy_name} is at your service. What do you need help with? 💪",
            f"Always happy to help! Just tell me what you need and I'll do my best! 🙌"
        ]
        return random.choice(responses)
    
    # Joke requests
    elif any(_word_in_text(user_input_lower, w) for w in ["joke", "funny", "laugh", "humor"]):
        jokes = [
            "Why don't scientists trust atoms anymore? Because they make up everything! 😄",
            "I told my wife she was drawing her eyebrows too high. She looked surprised! 😳",
            "Why did the scarecrow win an award? Because he was outstanding in his field! 🌾",
            "What do you call a fake noodle? An impasta! 🍝",
            "Why don't eggs tell jokes? They'd crack each other up! 🥚"
        ]
        return random.choice(jokes)
    
    # Time/date queries
    elif any(_word_in_text(user_input_lower, w) for w in ["time", "date", "day", "clock"]):
        now = datetime.now()
        return f"It's currently {now.strftime('%I:%M %p')} on {now.strftime('%A, %B %d, %Y')}. Time flies when we're chatting! ⏰"
    
    # Thank you responses
    elif any(_word_in_text(user_input_lower, w) for w in ["thank", "thanks", "appreciate"]):
        responses = [
            "You're very welcome! That's what buddies are for! 😊",
            "Anytime! Happy to help my friend! 🤗",
            "No problem at all! Helping you makes my day! 💫"
        ]
        return random.choice(responses)
    
    # Default responses
    else:
        responses = [
            f"That's interesting! Tell me more about that? 🤔",
            f"I see what you mean. What else is on your mind? 💭",
            f"Cool! How does that make you feel? 😊",
            f"Thanks for sharing that with me! What would you like to talk about next? 🔄",
            f"That's quite something! Do you want to explore that idea further? 🚀",
            f"I'm listening! What else would you like to discuss? 👂"
        ]
        return random.choice(responses)

def get_gpt_response(api_key, user_input, buddy_name, chat_history):
    """Get response from Google Gemini API"""
    try:
        # Gemini requires key in URL query param
        url = f"{st.session_state.api_url}?key={api_key}"
        
        # Build Gemini-style contents with clear instruction
        contents = [{"role": "user", "parts": [{"text": f"You are {buddy_name}, a friendly and helpful AI assistant. Give a complete, engaging answer to: {user_input}"}]}]
        
        # Add recent history
        recent = chat_history[-10:] if len(chat_history) > 10 else chat_history
        for msg in recent:
            contents.append({
                "role": msg["role"],
                "parts": [{"text": msg["content"]}]
            })
        
        data = {
            "contents": contents,
            "generationConfig": {"maxOutputTokens": 2048, "temperature": 0.7}
        }
        
        response = requests.post(url, json=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            try:
                parts = result["candidates"][0]["content"]["parts"]
                text = "".join(str(p.get("text", "")) for p in parts)
                return text if text else generate_buddy_response(user_input, buddy_name)
            except Exception:
                return generate_buddy_response(user_input, buddy_name)
        else:
            st.error(f"API Error: {response.json().get('error', {}).get('message', 'Unknown error')}")
            return generate_buddy_response(user_input, buddy_name)
    except Exception as e:
        st.error(f"Connection error: {str(e)}")
        return generate_buddy_response(user_input, buddy_name)

# Page configuration
st.set_page_config(
    page_title="Buddy AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

if "buddy_name" not in st.session_state:
    st.session_state.buddy_name = "Buddy"

if "api_key" not in st.session_state:
    st.session_state.api_key = DEFAULT_GEMINI_API_KEY
if "user_api_key" not in st.session_state:
    st.session_state.user_api_key = ""
if "api_url" not in st.session_state:
    st.session_state.api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.6-flash:generateContent"
if "api_model" not in st.session_state:
    st.session_state.api_model = "gemini-3.6-flash"

# Sidebar
with st.sidebar:
    st.title("🤖 Buddy AI Settings")
    st.session_state.buddy_name = st.text_input(
        "Buddy's Name", 
        value=st.session_state.buddy_name,
        placeholder="Enter your AI buddy's name"
    )
    
    st.divider()
    
    st.session_state.user_api_key = st.text_input(
        "Gemini API Key", 
        value=st.session_state.user_api_key,
        type="password",
        placeholder="Leave blank to use the default Gemini key"
    )
    st.session_state.api_key = st.session_state.user_api_key.strip() or DEFAULT_GEMINI_API_KEY
    
    st.session_state.api_url = st.text_input(
        "Gemini Endpoint", 
        value=st.session_state.api_url,
        placeholder="https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
    )
    
    st.session_state.api_model = st.text_input(
        "Gemini Model", 
        value=st.session_state.api_model,
        placeholder="gemini-pro"
    )
    
    st.caption("💡 Leave blank to use the default Gemini key, or enter your own.")
    
    st.divider()
    
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()
        
    st.divider()
    st.caption("Buddy AI - Your friendly AI companion")
    st.caption(f"Session started: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

# Main chat interface
st.title(f"💬 Chat with {st.session_state.buddy_name}")
st.caption("Your friendly AI assistant is ready to help!")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])
        if "timestamp" in message:
            st.caption(f"*{message['timestamp']}*")

# Chat input
if prompt := st.chat_input("What's on your mind?"):
    # Add user message to chat history
    timestamp = datetime.now().strftime("%H:%M")
    st.session_state.messages.append({
        "role": "user", 
        "content": prompt,
        "timestamp": timestamp
    })
    
    # Display user message
    with st.chat_message("user"):
        st.write(prompt)
        st.caption(f"*{timestamp}*")
    
    # Generate bot response
    with st.chat_message("assistant"):
        with st.spinner(f"{st.session_state.buddy_name} is thinking..."):
            time.sleep(0.5)  # Simulate brief thinking time
            
            # Use GPT API if API key is provided
            if st.session_state.api_key:
                response = get_gpt_response(
                    st.session_state.api_key, 
                    prompt, 
                    st.session_state.buddy_name, 
                    st.session_state.messages
                )
            else:
                # Fall back to simple response logic
                response = generate_buddy_response(prompt, st.session_state.buddy_name)
            
            response_timestamp = datetime.now().strftime("%H:%M")
            
            st.write(response)
            st.caption(f"*{response_timestamp}*")
    
    # Add bot response to chat history
    st.session_state.messages.append({
        "role": "assistant", 
        "content": response,
        "timestamp": response_timestamp
    })

# Quick Revision Quiz - PDF Drop
pdf_file = st.file_uploader("Drop PDF for quick revision quiz", type=["pdf"])
if pdf_file is not None:
    st.success("PDF received. Parsing...")
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    snippet = text[:500].replace("\n", " ")
    questions = [
        f"Q1: Main idea: '{snippet[:120]}...'?",
        f"Q2: Key point from '{snippet[120:250]}...'?",
        f"Q3: Summarize: '{snippet[250:400]}...'"
    ]
    if st.button("Generate Quick Revision Quiz"):
        st.info("Quiz mode activated. Answer the questions.")
        for q in questions:
            st.write(q)
            ans = st.text_input("Your answer", key=str(q))
            if st.button("Check Answer", key="check_"+str(q)[:20]):
                st.info("Answer checked! (Manual grading or LLM can validate here.)")
else:
    st.warning("Not completed — please drop a PDF and go further.")

st.divider()
# Footer
st.divider()
if st.session_state.user_api_key.strip():
    st.caption(f"🤖 Powered by Google Gemini with your API key ({st.session_state.api_model})")
else:
    st.caption(f"🤖 Powered by Google Gemini (default key) ({st.session_state.api_model})")
import streamlit as st
import time
import random
import requests
from datetime import datetime

def generate_buddy_response(user_input, buddy_name):
    """Generate a simple response based on user input"""
    user_input_lower = user_input.lower()
    
    # Greeting responses
    if any(word in user_input_lower for word in ["hello", "hi", "hey", "greetings"]):
        responses = [
            f"Hello there! I'm {buddy_name}, your friendly AI buddy! 👋",
            f"Hey! {buddy_name} here! How's your day going? 😊",
            f"Hi! Great to see you! I'm {buddy_name}, ready to help! ✨"
        ]
        return random.choice(responses)
    
    # How are you responses
    elif any(word in user_input_lower for word in ["how are you", "how do you do", "how's it going"]):
        responses = [
            f"I'm doing great! Thanks for asking. How about you? 😊",
            f"I'm feeling fantastic today! Ready to chat with you! 💫",
            f"Doing awesome! Always happy to talk with a friend like you! 🤗"
        ]
        return random.choice(responses)
    
    # Help/request responses
    elif any(word in user_input_lower for word in ["help", "assist", "support", "can you"]):
        responses = [
            f"Of course! I'm here to help you with whatever you need. What can I do for you today? 🤝",
            f"You've got it! {buddy_name} is at your service. What do you need help with? 💪",
            f"Always happy to help! Just tell me what you need and I'll do my best! 🙌"
        ]
        return random.choice(responses)
    
    # Joke requests
    elif any(word in user_input_lower for word in ["joke", "funny", "laugh", "humor"]):
        jokes = [
            "Why don't scientists trust atoms anymore? Because they make up everything! 😄",
            "I told my wife she was drawing her eyebrows too high. She looked surprised! 😳",
            "Why did the scarecrow win an award? Because he was outstanding in his field! 🌾",
            "What do you call a fake noodle? An impasta! 🍝",
            "Why don't eggs tell jokes? They'd crack each other up! 🥚"
        ]
        return random.choice(jokes)
    
    # Time/date queries
    elif any(word in user_input_lower for word in ["time", "date", "day", "clock"]):
        now = datetime.now()
        return f"It's currently {now.strftime('%I:%M %p')} on {now.strftime('%A, %B %d, %Y')}. Time flies when we're chatting! ⏰"
    
    # Thank you responses
    elif any(word in user_input_lower for word in ["thank", "thanks", "appreciate"]):
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
        
        # Build Gemini-style contents
        contents = [{"role": "user", "parts": [{"text": f"You are {buddy_name}. {user_input}"}]}]
        
        # Add recent history
        recent = chat_history[-10:] if len(chat_history) > 10 else chat_history
        for msg in recent:
            contents.append({
                "role": msg["role"],
                "parts": [{"text": msg["content"]}]
            })
        
        data = {
            "contents": contents,
            "generationConfig": {"maxOutputTokens": 500, "temperature": 0.7}
        }
        
        response = requests.post(url, json=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            return result["candidates"][0]["content"]["parts"][0]["text"]
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
    st.session_state.api_key = ""
if "api_url" not in st.session_state:
    st.session_state.api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
if "api_model" not in st.session_state:
    st.session_state.api_model = "gemini-1.5-flash"

# Sidebar
with st.sidebar:
    st.title("🤖 Buddy AI Settings")
    st.session_state.buddy_name = st.text_input(
        "Buddy's Name", 
        value=st.session_state.buddy_name,
        placeholder="Enter your AI buddy's name"
    )
    
    st.divider()
    
    st.session_state.api_key = st.text_input(
        "Gemini API Key", 
        value=st.session_state.api_key,
        type="password",
        placeholder="Enter your Gemini API key (starts with AI... or gsk_...)"
    )
    
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
    
    st.caption("💡 Gemini-only mode. Enter your Gemini API key to use Gemini AI.")
    
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

# Footer
st.divider()
if st.session_state.api_key:
    st.caption(f"🤖 Powered by Google Gemini ({st.session_state.api_model})")
else:
    st.caption("💡 Tip: Try asking for jokes, sharing how your day is going, or asking for help with something!")
    st.caption("🔑 Gemini-only mode activated — enter valid Gemini key to proceed!")
# 💡 Ideas to Level Up Your Memory Agent

You have a bot that remembers and uses tools. Now, let’s make it smarter!
Here are some fun challenges to customize your Day 2 project.

---

## 🧠 1. Long-Term Memory (Save Chats)
Right now, if you refresh the page, the memory is gone (Goldfish mode 🐠).
**Challenge:** Save the chat history to a file so it remembers you even after a restart.

**How:**
- Use Python’s `json` module.
- Create a `save_memory()` function that writes `st.session_state.memory` to a `chat_history.json` file.
- Create a `load_memory()` function that reads it back when the app starts.

---

## 🛠️ 2. Add More Tools!
Why stop at Wikipedia and Calculator? Add more superpowers!

### 🌦️ Weather Tool
- Use `requests` to fetch weather from an API (like OpenWeatherMap).
- **Trigger:** "What's the weather in Mumbai?"

### 🎲 Random Number / Coin Flip
- **Trigger:** "Flip a coin" or "Roll a dice."
- **Code:** `import random`, then `return random.choice(['Heads', 'Tails'])`.

### 🕒 Time Tool
- **Trigger:** "What time is it?"
- **Code:** `import datetime`, then `return datetime.datetime.now()`.

---

## 🧹 3. The "Forget-Me-Not" Button
Sometimes you want to start fresh.
**Challenge:** Add a "Clear Memory" button in the sidebar.

**How:**
```python
if st.sidebar.button("Clear Memory"):
    st.session_state.memory = []
    st.rerun()
```

---

## 🎭 4. Give It a Personality
Make the agent talk in a specific style.
- **Pirate Mode:** "Arrgh matey! The answer be 42."
- **Robot Mode:** "BEEP BOOP. COMPUTING... RESULT: 42."

**How:** Update the `prompt` variable in `agent_response()` to include:
> "You are a helpful pirate assistant. Always speak like a pirate."

---

## 🕵️ 5. "Secret Code" Mode
Teach the agent a secret password.
- If the user says "Project Alpha", the agent replies: "Access Granted. Welcome, Commander."
- If the user says "Project Beta", the agent replies: "Access Denied."

**How:** Add a simple `if` check in the `agent_response` function before calling the LLM.

---

*Experimenting is the best way to learn. Break things and fix them!* 🚀



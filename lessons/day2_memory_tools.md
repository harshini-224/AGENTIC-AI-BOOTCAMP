# 🧠 Day 2 — Memory + Tools for Agentic AI

**Theme:** “How Do Agents Remember + Use Tools?”  
**Goal:** Build an agent that remembers past messages and calls real tools like a calculator or Wikipedia.

---

# 1️⃣ Warm-Up Story: *“The Goldfish vs. The Elephant”*

Imagine:

- A **goldfish** has no memory. Every time it sees you, it’s like: “OMG who are you??”
- An **elephant** remembers everything you ever did. Forever.

Most chatbots = **goldfish** 🐠  
Agentic AI = **elephant** 🐘  

Today we turn your AI from a goldfish → elephant.  
And also teach it how to **use tools** like a smart helper. 🔧

---

# 2️⃣ What Is “Memory” for an AI Agent?

### 🧠 Simple Version (Explain like I'm 5)
Memory is when AI can say:

> “Earlier you told me you like coding. So I made a study plan for you.”

That means the agent:
- Stores old messages  
- Looks at them later  
- Uses them to answer better  

This is **short-term memory** (like remembering a conversation).

---

# 3️⃣ Why Do Agents Need Memory?

| Without Memory | With Memory |
|---------------|------------|
| “Who are you again?” | “Welcome back, Richard!” |
| Repeats questions | Builds on earlier context |
| No personalization | Smart + aware + helpful |
| Not an agent | Feels like a real assistant |

---

# 4️⃣ What Are “Tools” in Agentic AI?

### 🛠️ Explain like I’m 5  
Tools = **superpowers**.

If an AI does not know something, it can:
- Search Wikipedia  
- Calculate numbers  
- Fetch weather  
- Analyze files  
- Call APIs  

Just like humans use calculators, agents use **tools**.

---

# 5️⃣ Whiteboard Visuals (Draw These Today)

### 🎨 A. The Agent Brain

> 🤔 Thinking
> 🧠 Memory
> 🔧 Tools
> 🔁 Reflection

### 🪜 B. How the Agent Decides

> User message → Do I need a tool? →
> Yes → Use tool
> No → LLM responds

### 🔁 C. Memory Loop

> User → Agent → Memory → Agent uses memory → Better reply

---

# 6️⃣ Today’s Goal

We will build an agent that can:

### ✔️ Remember last few messages  
### ✔️ Use a calculator tool  
### ✔️ Use a Wikipedia search tool  
### ✔️ Decide when to use tools  
### ✔️ Talk naturally like a real helper

This is the **first real agent** students build.

---

# 7️⃣ Mini Project — “Memory + Tools Agent”

We will build a Streamlit app with:

### 1. **Short-term memory** (`st.session_state`)  
### 2. **Calculator tool**  
### 3. **Wikipedia search tool**  
### 4. **LLM fallback**  
### 5. **Smart decision-making**  

---

# 8️⃣ Project Code  

**Place this in:**  
`projects/day2_memory_tools/app.py`

```python
import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai
import requests

# -----------------------------
# LOAD API KEY
# -----------------------------
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    raise ValueError("Missing GOOGLE_API_KEY in .env file.")

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-flash-lite-latest")

# -----------------------------
# STREAMLIT UI
# -----------------------------
st.set_page_config(page_title="Memory + Tools Agent", page_icon="🧠")
st.title("🧠 Memory + Tools Agent")
st.write("This agent remembers the conversation AND uses external tools!")

# Session memory
if "memory" not in st.session_state:
    st.session_state.memory = []


# TOOL 1: CALCULATOR
def calculator(expression: str):
    try:
        result = eval(expression)
        return f"Result: {result}"
    except:
        return "Invalid expression. Try something like: 5*7 + 2"


# TOOL 2: WIKIPEDIA SEARCH
def wiki_search(query: str):
    try:
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{query}"
        data = requests.get(url).json()
        return data.get("extract", "No information found.")
    except:
        return "Error fetching data from Wikipedia."


TOOLS = {
    "calculator": calculator,
    "wiki": wiki_search
}


# AGENT LOGIC
def agent_response(user_msg):
    # Add conversation memory
    st.session_state.memory.append(f"User: {user_msg}")

    # Detect if tool needed
    if "calculate" in user_msg.lower() or "math" in user_msg.lower():
        expression = user_msg.replace("calculate", "").replace("math", "").strip()
        tool_output = calculator(expression)
        st.session_state.memory.append(f"Tool (Calculator): {tool_output}")
        return tool_output

    if "wiki" in user_msg.lower() or "search" in user_msg.lower():
        topic = user_msg.replace("wiki", "").replace("search", "").strip()
        tool_output = wiki_search(topic)
        st.session_state.memory.append(f"Tool (Wikipedia): {tool_output}")
        return tool_output

    # Otherwise use LLM with memory
    prompt = f"""
You are an AI assistant with memory.

Conversation so far:
{chr(10).join(st.session_state.memory)}

User just said: {user_msg}

Reply clearly, simply, and continue the conversation naturally.
"""
    response = model.generate_content(prompt)
    bot_msg = response.text

    st.session_state.memory.append(f"Agent: {bot_msg}")
    return bot_msg


# -----------------------------
# CHAT UI
# -----------------------------
st.subheader("💬 Chat With the Agent")

user_input = st.text_input("Type something...")

if st.button("Send"):
    if user_input.strip():
        output = agent_response(user_input)
        st.write("🤖:", output)
    else:
        st.warning("Please type a message.")


# -----------------------------
# SHOW MEMORY
# -----------------------------
st.markdown("---")
st.subheader("🧠 Agent Memory (Short-Term)")

for msg in st.session_state.memory[-6:]:  # show last 6 messages
    st.write("-", msg)
```

# 9️⃣ Student Exercise Ideas (Whiteboard + Practice)

### ✔️ Add long-term memory
Store memory in a `.json` file.

### ✔️ Add another tool
Examples:
- Weather search
- YouTube search
- Dictionary lookup
- Joke generator

### ✔️ Add reflection
Agent checks:
> “Is my answer good? Should I improve it?”

### ✔️ Add persona switching
Student / Teacher / Senior Mentor modes.

# 🔟 Day Summary (Simple Table)

| Concept | What You Learned |
|---------|------------------|
| What is memory? | AI remembers conversation history |
| What are tools? | External abilities (calculator/wiki) |
| Agent flow | Choose tool → OR use LLM |
| Project | Memory + Tools Agent |
| Skills gained | Real agent design |

# 1️⃣1️⃣ Resume Line for Students

> Built an AI agent with short-term memory and tool-use capabilities (calculator + Wikipedia) using Gemini API and Streamlit.

# 1️⃣2️⃣ Homework

1. Add a Weather API tool
2. Make the memory last 20 turns
3. Add a “Clear Memory” button

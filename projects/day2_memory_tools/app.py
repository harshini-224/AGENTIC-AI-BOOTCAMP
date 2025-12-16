import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai
import requests
import re
import ast
import operator

# -----------------------------
# LOAD API KEY
# -----------------------------
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    try:
        API_KEY = st.secrets["GOOGLE_API_KEY"]
    except:
        pass

if not API_KEY:
    st.error("❌ Missing GOOGLE_API_KEY. Please set it in a .env file or Streamlit secrets.")
    st.stop()

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-flash-lite-latest")

# -----------------------------
# STREAMLIT UI SETUP
# -----------------------------
st.set_page_config(page_title="Memory + Tools Agent", page_icon="🧠", layout="centered")
st.title("🧠 Memory + Tools Agent")
st.write("I remember our chat and can use tools (Calculator & Wikipedia) to help you!")

# Initialize Session Memory
if "memory" not in st.session_state:
    st.session_state.memory = []

# -----------------------------
# TOOL 1: CALCULATOR
# -----------------------------
def safe_calculate(expression: str):
    """
    Safely evaluates a mathematical expression string using the AST module 
    to prevent security risks associated with eval().
    """
    # 1. Clean the input: Remove any character that isn't a digit, operator, or decimal
    # Allowed: 0-9, +, -, *, /, (, ), . and space
    clean_expr = re.sub(r'[^0-9+\-*/(). ]', '', expression)
    
    # 2. Check for empty input
    if not clean_expr.strip():
        return "Error: Empty or invalid math expression."

    # 3. Define safe operators
    ops = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.USub: operator.neg,
    }

    def _eval(node):
        if isinstance(node, ast.Num): # <number>
            return node.n
        elif isinstance(node, ast.BinOp): # <left> <operator> <right>
            return ops[type(node.op)](_eval(node.left), _eval(node.right))
        elif isinstance(node, ast.UnaryOp): # <operator> <operand> e.g., -1
            return ops[type(node.op)](_eval(node.operand))
        else:
            raise TypeError(node)

    try:
        # Parse the expression into an AST (Abstract Syntax Tree)
        tree = ast.parse(clean_expr, mode='eval')
        result = _eval(tree.body)
        
        # Limit decimal places for cleaner output
        if isinstance(result, float):
            result = round(result, 4)
            
        return f"Calculated Result: {result}"
        
    except ZeroDivisionError:
        return "Error: Cannot divide by zero."
    except Exception:
        return f"Error: Could not calculate '{expression}'. Please use simple math like '5 * 10'."

# -----------------------------
# TOOL 2: WIKIPEDIA SEARCH
# -----------------------------
def wiki_search(query: str):
    """
    Searches Wikipedia API and returns a summary. 
    Handles empty results and connection errors.
    """
    if not query.strip():
        return "Error: Search query is empty."

    try:
        # Use the standard API endpoint
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{query.strip()}"
        response = requests.get(url, timeout=5) # 5-second timeout
        
        if response.status_code == 200:
            data = response.json()
            return data.get("extract", "I found the page, but there's no summary available.")
        elif response.status_code == 404:
            return f"I couldn't find any Wikipedia article for '{query}'."
        else:
            return "Wikipedia is currently unavailable (Status Code: {}).".format(response.status_code)
            
    except requests.exceptions.Timeout:
        return "Search timed out. Wikipedia might be slow right now."
    except Exception as e:
        return f"An error occurred while searching: {e}"

# -----------------------------
# AGENT LOGIC
# -----------------------------
def agent_response(user_msg):
    # 1. Add User Message to Memory
    st.session_state.memory.append(f"User: {user_msg}")

    # 2. Tool Routing Logic (Simple Keyword Detection)
    user_lower = user_msg.lower()
    tool_result = None
    tool_name = ""

    # Check for Calculator
    if any(keyword in user_lower for keyword in ["calculate", "math", "solve", "+", "*", "/"]):
        # Extract potential math part - simple heuristic
        # If explicit command
        if "calculate" in user_lower:
            expression = user_msg.lower().split("calculate")[-1]
        elif "solve" in user_lower:
            expression = user_msg.lower().split("solve")[-1]
        else:
            expression = user_msg # Try the whole string if it looks like math
            
        result = safe_calculate(expression)
        
        # Only use it if it didn't return a generic error for non-math text
        if "Error" not in result or "invalid" not in result.lower():
            tool_result = result
            tool_name = "Calculator"

    # Check for Wikipedia (only if calculator didn't run or failed)
    if not tool_result and any(keyword in user_lower for keyword in ["wiki", "search for", "who is", "what is"]):
        # Extract query
        query = user_msg
        for keyword in ["wiki search", "wiki", "search for", "who is", "what is"]:
            if keyword in user_lower:
                query = re.split(keyword, user_msg, flags=re.IGNORECASE)[-1]
                break
        
        tool_result = wiki_search(query)
        tool_name = "Wikipedia"

    # 3. Handle Tool Output (if any)
    if tool_result:
        st.session_state.memory.append(f"Tool ({tool_name}): {tool_result}")
        # We return the tool result directly to show it clearly
        # Optionally, we could feed this back into the LLM to summarize
        return f"🛠️ **{tool_name} Output:** {tool_result}"

    # 4. Fallback to LLM (Chat Mode)
    # Construct the Prompt with Memory
    conversation_history = "\n".join(st.session_state.memory[-10:]) # Keep last 10 turns for context
    
    system_prompt = f"""
    You are a helpful and friendly AI assistant.
    
    CONTEXT:
    {conversation_history}
    
    INSTRUCTION:
    Reply to the user's last message naturally. 
    If they asked a question you can't answer, suggest using a tool like "Calculate..." or "Search wiki...".
    Keep your answer concise (under 3 sentences).
    """

    try:
        response = model.generate_content(system_prompt)
        bot_msg = response.text
        st.session_state.memory.append(f"Agent: {bot_msg}")
        return bot_msg
    except Exception as e:
        return f"⚠️ Error calling AI model: {e}"

# -----------------------------
# CHAT INTERFACE
# -----------------------------
st.subheader("💬 Chat")

# Container for chat history to keep it organized
chat_container = st.container()
with chat_container:
    # Display last 5 exchanges nicely
    recent_history = st.session_state.memory[-10:] 
    for msg in recent_history:
        if msg.startswith("User:"):
            st.chat_message("user").write(msg.replace("User:", "").strip())
        elif msg.startswith("Agent:"):
            st.chat_message("assistant").write(msg.replace("Agent:", "").strip())
        elif msg.startswith("Tool"):
            st.chat_message("robot").code(msg) # Display tool output as code/monospaced

# Input Area
with st.form(key="chat_form", clear_on_submit=True):
    col1, col2 = st.columns([8, 1])
    with col1:
        user_input = st.text_input("Message...", placeholder="Type 'Calculate 5*5' or 'Who is Tesla'", label_visibility="collapsed")
    with col2:
        submit_button = st.form_submit_button("Send")

    if submit_button and user_input.strip():
        with st.spinner("Thinking..."):
            response = agent_response(user_input)
            # Rerun to update the chat history immediately
            st.rerun()

# -----------------------------
# SIDEBAR: MEMORY VIEW
# -----------------------------
with st.sidebar:
    st.header("🧠 Brain Dump")
    st.caption("This is what the agent remembers:")
    st.text_area("Raw Memory", value="\n".join(st.session_state.memory), height=400, disabled=True)
    
    if st.button("🗑️ Clear Memory"):
        st.session_state.memory = []
        st.rerun()

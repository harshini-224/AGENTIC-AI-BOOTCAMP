# 🧠 Day 1 — Foundations of Agentic AI

**Theme:** From Chatbots → to Thinkers → to Agents  
**Goal:** Understand what Agentic AI is, why it matters, and build your first mini-agent.

---

# 1️⃣ Warm-Up Story: *“The Robot That Could Think”*

Imagine you built a robot.

At first, it only answers questions.  
But one day, you say:

> “I want to get better at studying.”

And the robot replies:

> “Okay! I created a 2-week plan for you.”

That robot didn’t just answer…  
It **thought**, **planned**, and **acted**.

That’s **Agentic AI**.

---

# 2️⃣ What Exactly Is Agentic AI?

### 🧠 Simple definition  
**Agentic AI = AI that can think, decide, and act toward a goal.**

Not just responding…  
But **planning** what to do next.

### ✨ Difference (Simple Table)

| Normal AI | Agentic AI |
|----------|------------|
| Waits for your questions | Understands your goal |
| Gives answers | Makes a plan |
| No memory | Can remember |
| No actions | Uses tools & APIs |
| Cannot reflect | Improves its mistakes |

---

# 3️⃣ How Did AI Evolve Into Agents?

| Stage | Example | What It Does | What It Can't Do |
|-------|---------|---------------|-------------------|
| 💬 Chatbots | Siri, Alexa | Answers basics | No reasoning |
| 🎨 Generative AI | ChatGPT, Gemini, SD | Creates content | Needs prompts |
| 🤖 Agentic AI | AutoGPT, Devin, CrewAI | Plans, acts, reflects | Still limited, but powerful |

---

# 4️⃣ The Agent Brain — 4 Building Blocks

Every useful agent has:

### 1. **Reasoning** 🧩  
Breaks big tasks into small, smart steps.

### 2. **Memory** 🧠  
Remembers what happened earlier.

### 3. **Tools** 🔧  
Uses APIs, Google search, calculators, files.

### 4. **Reflection** 🔁  
Thinks: “Did I do a good job? Should I improve this?”

---

# 5️⃣ Whiteboard Visuals (Draw These During Class)

### A. The Agent Loop

> Goal → Plan → Act → Observe → Improve

### B. The Agent Brain

> 🤔 Reasoning
> 💾 Memory
> 🔧 Tools
> 🪞 Reflection

### C. From Chatbot to Agent

> Chatbot → Smart Assistant → Planner → Autonomous Agent

---

# 6️⃣ How Agentic AI Thinks (Like a Smart Student)

### 🧠 Chain-of-Thought (Thinking step by step)

**Example:**  
“What should I do if it's raining tomorrow?”

> If raining → outdoor plans fail
>
> Indoor activities are better
> → Suggest indoor reading or a café

### 🔄 ReAct Framework (Reason + Act)

> Thought → Action → Observation → Reflection

**Example:**
Goal: “Find AI courses nearby”
- Thought: “Search for AI courses”
- Action: Google search API  
- Observation: Found 3  
- Reflection: Suggest the best one  

---

# 7️⃣ Mini Project — **Prompt to Planner Agent** 🧠✨

We will build a small “thinking agent” that:
- Takes a goal
- Breaks it into steps
- Uses simple reasoning instructions

### 🔧 Tools We Will Use
- Python  
- Streamlit  
- Gemini API (google.generativeai)  
- `.env` file for API keys (safe & professional)

---

# 8️⃣ Full Code (Put This in `projects/day1_prompt_to_planner/app.py`)

```python
import os

import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai

# -----------------------------
# 1. Load API key from .env
# -----------------------------
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    raise ValueError("GOOGLE_API_KEY is missing. Add it inside a .env file.")

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-flash-lite-latest")

# -----------------------------
# 2. UI
# -----------------------------
st.set_page_config(page_title="Goal Planner Agent", page_icon="🧠")
st.title("🧠 Goal Planner Agent")
st.write("Give me a goal, and I will turn it into smart steps!")

goal = st.text_input("🎯 What is your goal?")
steps = st.slider("How many steps should I create?", 3, 10, 5)

if st.button("✨ Generate Plan"):
    prompt = f"""
    You are a planning assistant.
    Break the goal "{goal}" into {steps} steps.
    Keep it simple, clear, and helpful.
    """
    response = model.generate_content(prompt)
    st.write(response.text)
```

# 9️⃣ Instructions for Students

### 📦 Install Requirements
```bash
pip install streamlit google-generativeai python-dotenv
```

### 🔑 Create .env
```
GOOGLE_API_KEY=your_key_here
```

### ▶️ Run the App
```bash
streamlit run app.py
```

# 🔟 Group Activity (20 Minutes)

1. Divide into groups of 3–4
2. Each group gives the agent a real college-life goal
3. Compare different plans
4. Share which plan seemed the smartest or most surprising

# 1️⃣1️⃣ Day Summary (Easy Table)

| Topic | What You Learned |
|-------|------------------|
| What is Agentic AI? | AI that can think, plan, act |
| How agents evolved | From chatbots → planners → doers |
| Agent thinking | Chain-of-thought + ReAct |
| Mini project | Planner agent using Gemini |
| Skills gained | Prompt engineering + reasoning |

# 1️⃣2️⃣ Resume Line for Students

> Built a reasoning-based AI planner using Gemini API that converts user goals into actionable stepwise plans.

# 1️⃣3️⃣ Homework

1. Add deadlines to the plan.
2. Make your agent add emojis to each step.
3. Write: “How is an agent different from a chatbot?” (5 lines)

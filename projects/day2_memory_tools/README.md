# Day 2 Project: Memory + Tools Agent 🧠🛠️

This project introduces two critical components of Agentic AI: **Memory** and **Tools**.

Unlike a simple chatbot, this agent:
1.  **Remembers** the context of your conversation (Short-term Memory).
2.  **Acts** by using external tools (Calculator, Wikipedia) when needed.

## Features
-   **Short-Term Memory:** Keeps track of the conversation history in `st.session_state`.
-   **Tool Selection:** Automatically detects if the user wants to "calculate" or "search" something.
-   **External APIs:** Connects to Wikipedia API for real-time information.

## How to Run

1.  **Install Dependencies:**
    ```bash
    pip install streamlit python-dotenv google-generativeai requests
    ```

2.  **Set Up API Key:**
    -   Create a `.env` file in this folder.
    -   Add your `GOOGLE_API_KEY`.

3.  **Run the App:**
    ```bash
    streamlit run app.py
    ```

## Usage Examples
-   **Chat:** "Hi, who are you?" -> "I am an AI assistant..."
-   **Math:** "Calculate 25 * 4" -> "Result: 100"
-   **Search:** "Wiki search Agentic AI" -> (Returns Wikipedia summary)

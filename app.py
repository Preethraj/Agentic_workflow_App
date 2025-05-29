import streamlit as st
import openai
import time

# --- Setup Groq API ---
openai.api_key = st.secrets["GROQ_API_KEY"]
openai.api_base = "https://api.groq.com/openai/v1"

# --- PlanAgent ---
def plan_tasks(query):
    prompt = f"Break this task into clear sub-tasks:\n\"{query}\"\nList them clearly."
    response = openai.ChatCompletion.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}]
    )
    text = response['choices'][0]['message']['content']
    return [line.strip("-• ").strip() for line in text.split("\n") if line.strip()]

# --- ToolAgent ---
def tool_agent(task):
    prompt = f"Please solve this task:\n{task}"
    response = openai.ChatCompletion.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}]
    )
    return response['choices'][0]['message']['content']

# --- Reflector ---
def reflect(task, result):
    prompt = f"""
    Task: {task}
    Result: {result}
    Does this result fully and accurately answer the task? Suggest improvements if needed.
    """
    response = openai.ChatCompletion.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}]
    )
    return response['choices'][0]['message']['content']

# --- Streamlit UI ---
st.title("🧠 Agentic Workflow using Groq API")
st.write("This app mimics a LangGraph-style intelligent workflow: Planning → Execution → Reflection.")

query = st.text_area("📌 Enter your complex query:")

if st.button("🚀 Run Agentic Workflow"):
    with st.spinner("🧠 Planning tasks..."):
        tasks = plan_tasks(query)
    
    st.success("✅ Subtasks identified:")
    for i, task in enumerate(tasks, 1):
        st.markdown(f"{i}. {task}")

    st.markdown("---")
    st.info("⚙️ Running ToolAgent and Reflector...")

    for task in tasks:
        st.markdown(f"**🔹 Task:** {task}")
        answer = tool_agent(task)
        time.sleep(2)
        reflection = reflect(task, answer)
        st.markdown(f"✅ **Answer:** {answer}")
        st.markdown(f"💡 **Improved Answer:** {reflection}")
        st.markdown("---")


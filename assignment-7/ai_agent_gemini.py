import os
import datetime
import json
from dotenv import load_dotenv
import google.generativeai as genai
from langchain.memory import ConversationBufferMemory
from langchain.schema import messages_from_dict, messages_to_dict

MEMORY_FILE = "agent_gemini_memory.json"

# 1. Setup API Key Gemini
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") or "YOUR_API_KEY"
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# 2. Langchain Memory (STM)
memory = ConversationBufferMemory(return_messages=True)

# 3. LTM sederhana (todo list)
long_term_memory = {
    "todo_list": [],
    "important_facts": []
}

def save_memory_to_json():
    """Simpan STM (Langchain) & LTM ke file JSON"""
    data = {
        "stm": messages_to_dict(memory.buffer) if hasattr(memory, "buffer") else [],
        "ltm": long_term_memory
    }
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_memory_from_json():
    """Muat STM & LTM dari file JSON (jika ada)"""
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                # Restore STM
                stm = data.get("stm", [])
                if stm:
                    memory.buffer.clear()
                    for msg in messages_from_dict(stm):
                        memory.buffer.append(msg)
                # Restore LTM
                ltm = data.get("ltm", {})
                if ltm:
                    long_term_memory.update(ltm)
            except Exception:
                pass

# 4. Tools (hanya todo & memory)
def tool_add_todo(user_input):
    task = user_input.replace("tambah", "").replace("todo", "").replace("task", "").strip()
    if not task:
        return (
            "❌ Mohon sebutkan task yang ingin ditambahkan.\n"
            "Format: tambah task [deskripsi tugas]\n"
            "Contoh: tambah task beli tiket pesawat"
        )
    long_term_memory["todo_list"].append({
        "task": task,
        "created": datetime.datetime.now().isoformat(),
        "completed": False
    })
    save_memory_to_json()
    return (
        f"✅ Task '{task}' ditambahkan ke todo list.\n"
        "Ketik 'tampilkan semua todo' untuk melihat seluruh todo list."
    )

def tool_show_memory():
    todos = long_term_memory["todo_list"]
    res = f"🧠 STM: {len(memory.buffer)} entries\n📝 Todo: {len(todos)} items\n"
    for i, t in enumerate(todos[-5:], 1):
        res += f"{i}. {'✅' if t['completed'] else '⏳'} {t['task']}\n"
    res += "\nKetik 'tampilkan semua todo' untuk melihat seluruh todo list."
    return res

def tool_show_all_todo():
    todos = long_term_memory["todo_list"]
    if not todos:
        return "Todo list kosong."
    res = "📝 Seluruh Todo List:\n"
    for i, t in enumerate(todos, 1):
        res += f"{i}. {'✅' if t['completed'] else '⏳'} {t['task']}\n"
    return res

TOOLS = {
    "add_todo": tool_add_todo,
    "show_memory": tool_show_memory,
    "show_all_todo": tool_show_all_todo
}

# 5. Prompt + RAG
def create_prompt(user_input):
    stm = memory.buffer[-5:] if hasattr(memory, "buffer") else []
    todos = long_term_memory["todo_list"][-5:]
    prompt = f"""
Anda adalah AI Personal Assistant.
TOOLS: add_todo, show_memory

KONTEKS TERAKHIR:
{stm}

TODO TERAKHIR:
{todos}

INSTRUKSI:
- Jawab dengan ramah.
- Gunakan tools jika perlu.
- Ingat konteks sebelumnya.
User: {user_input}
"""
    return prompt

# 6. Agent Loop
def agent_loop(user_input):
    prompt = create_prompt(user_input)
    try:
        response = model.generate_content(prompt)
        answer = response.text.strip()
    except Exception as e:
        answer = f"Error: {str(e)}"
    tool_response = None
    if any(word in user_input.lower() for word in ["tambah", "todo", "task"]):
        tool_response = tool_add_todo(user_input)
    elif any(word in user_input.lower() for word in ["memory", "ingat"]):
        tool_response = tool_show_memory()
    elif "tampilkan semua todo" in user_input.lower() or "lihat todo" in user_input.lower():
        tool_response = tool_show_all_todo()
    # Simpan ke memory (STM) SEKALI saja
    memory.save_context({"input": user_input}, {"output": tool_response or answer})
    save_memory_to_json()
    return tool_response or answer

# 7. Main Loop
def main():
    """
    AI Personal Assistant berbasis Gemini LLM + Langchain.
    - Agent Loop: Observe → Decide → Act
    - Memory: STM (Langchain ConversationBufferMemory), LTM (todo)
    - Tools: todo, show memory
    - Prompt: RAG (STM+LTM)
    - Memory disimpan di agent_memory.json
    """
    print("Gemini AI Assistant + Langchain (q untuk keluar)")
    print("------------------------------------------")
    load_memory_from_json()
    while True:
        user_input = input("Anda: ")
        if user_input.lower() == 'q':
            print("Sampai jumpa!")
            break
        response = agent_loop(user_input)
        print("\nAssistant:", response)
        print("------------------------------------------")

if __name__ == "__main__":
    main()
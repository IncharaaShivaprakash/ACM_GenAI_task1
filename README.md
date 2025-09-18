# ACM_GenAI_task1
Streamlit Open AI chatbot with multiple personalities and memory


# Persona ChatBot — ACM Task 1

**Simple chatbot built using Streamlit (UI) + LangChain + OpenAI (OpenAI only).**  

This project is a single file Streamlit app (`chatbot.py`), supports multiple personas (RoastBot, ShakespeareBot, Emoji Translator, Neutral) and keeps conversation memory going during the app session.



# Features
- Multi-persona chat: RoastBot ; ShakespeareBot ; Emoji Translator ; Neutral
- Conversation memory (you can chat continuously without restarting)
- Clean Streamlit UI
- Export chat as a `.txt` file
- No API key is stored in repo (you must provide your own)



# Files in this repository
- `chatbot.py` — main app (single-file)
- `.gitignore` — files to ignore
- `README.md` — this file



# Prerequisites
- Python 3.10+ installed
- An OpenAI API key (get one from https://platform.openai.com)
- Basic terminal or PyCharm knowledge



## Setup (quick)
1. Clone the repo:
```bash
git clone https://github.com/IncharaaShivaprakash/ACM_GenAI_task1.git
cd ACM-GenAI-task1
```
2.Create & activate a virtual environment:
python -m venv venv
# macOS / Linux
source venv/bin/activate
# Windows PowerShell
# .\venv\Scripts\Activate.ps1


3.Install dependencies use din the code

4.Set your OpenAI API key:
# macOS / Linux
export OPENAI_API_KEY="sk-..."
# Windows PowerShell
$env:OPENAI_API_KEY = "sk-..."


Run the app:
streamlit run streamlit_chatbot.py



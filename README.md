🤖 Ollama AI Chat Assistant (Streamlit + LangChain)

A modern interactive AI chatbot web application built using Streamlit, LangChain, and Ollama LLMs.
This project provides a smooth chat experience with support for multiple local models like Mistral, Gemma2, and LLaMA3.

🚀 Features
💬 Real-time conversational AI chat interface
🧠 Powered by Ollama local LLMs
🔁 Maintains chat history (memory in session state)
⚙️ Model selection (Mistral / Gemma2 / LLaMA3)
🎛️ Adjustable temperature & max tokens
🧹 Clear chat functionality
🎨 Modern UI with custom Streamlit styling
🔗 Built using LangChain expression pipeline (LCEL)
🏗️ Architecture
User enters a message via Streamlit chat UI
Message + chat history is formatted using LangChain prompt template
Selected Ollama model generates response
Output is parsed and displayed in chat UI
Conversation is stored in session state for memory
🧰 Tech Stack
Python 🐍
Streamlit 🌐
LangChain 🔗
Ollama 🦙
dotenv 🔐

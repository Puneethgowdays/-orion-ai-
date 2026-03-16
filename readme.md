<div align="center">

# 🤖 ORION AI Assistant

### Pragmatic AI Assistant with Personality, Voice, and Real-Time Search

[![Live Demo](https://img.shields.io/badge/Live_Demo-Available-success?style=for-the-badge)](https://orion-ai-76hk.onrender.com)
[![Python](https://img.shields.io/badge/Python-3.14-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge)]()

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Tech Stack](#️-tech-stack)
- [Architecture](#-architecture)
- [Live Demo](#-live-demo)
- [Screenshots](#-screenshots)
- [Installation](#-installation)
- [Usage](#-usage)
- [API Endpoints](#-api-endpoints)
- [Project Structure](#-project-structure)
- [Personality System](#-personality-system)
- [Future Enhancements](#-future-enhancements)
- [License](#-license)
- [Contact](#-contact)

---

## 🎯 Overview

**ORION** is a full-stack conversational AI assistant inspired by TARS from Interstellar. Built as a personal learning project to explore AI integration, cloud deployment, and cross-platform development. ORION features adjustable personality settings, real-time web search capabilities, voice interaction, and image analysis — accessible via both web browser and mobile app.

**Key Highlight:** Unlike generic chatbots, ORION allows users to customize the AI's personality (humor, honesty, mode) to create a unique, personalized assistant experience.

---

## ✨ Features

### 🧠 Core AI Capabilities
- **Fast LLM Responses** - Powered by Groq API (llama-3.3-70b) with 1-3 second response times
- **Real-Time Web Search** - Auto-detects when queries need current information via Tavily API
- **Image Analysis** - Upload images for ORION to analyze using Groq's llama-4-scout vision model
- **Context-Aware Conversations** - Maintains chat history with persistent JSON storage

### 🎭 Personality System
- **Adjustable Humor** (0-100%) - From serious to witty responses
- **Adjustable Honesty** (0-100%) - From diplomatic to brutally honest
- **Mode Selection** - Serious, Casual, or Dry communication styles
- Dynamic personality injection into system prompts

### 🎤 Voice Interaction
- **Voice Input** - Speech-to-text using Web Speech API (web) and Flutter package (mobile)
- **Voice Output** - Text-to-speech with customizable deep male voice profile
- Hands-free interaction support

### 💬 Chat Management
- **Multiple Chat Sessions** - Create, switch, and manage separate conversations
- **Persistent Storage** - Chats saved in JSON format, survive server restarts
- **Session History** - Sidebar navigation with delete functionality

### 🌐 Cross-Platform
- **Web Application** - Responsive design for desktop and mobile browsers
- **Android App** - Native Flutter APK (46.5MB) for mobile devices
- **Cloud Deployed** - Publicly accessible at [orion-ai-76hk.onrender.com](https://orion-ai-76hk.onrender.com)

---

## 🛠️ Tech Stack

### Backend
- **Python 3.14** - Core programming language
- **FastAPI** - Modern REST API framework
- **Uvicorn** - ASGI server for production
- **Groq API** - LLM inference (llama-3.3-70b, llama-4-scout)
- **Tavily API** - Real-time web search integration
- **Pydantic** - Data validation
- **python-multipart** - File upload handling

### Frontend (Web)
- **HTML5, CSS3** - Structure and styling
- **Vanilla JavaScript** - Client-side logic
- **Web Speech API** - Voice input
- **SpeechSynthesis API** - Voice output
- **Responsive Design** - Mobile and desktop compatible

### Mobile App
- **Flutter 3.41.4** - Cross-platform framework
- **Dart 3.11.1** - Programming language
- **Packages:**
  - `http` - API communication
  - `image_picker` - Image selection
  - `speech_to_text` - Voice input
  - `flutter_tts` - Text-to-speech

### Infrastructure
- **Render.com** - Cloud platform (free tier)
- **GitHub** - Version control
- **JSON File Storage** - Persistent chat history

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────┐
│          User Interface Layer                   │
│  ┌──────────────┐        ┌──────────────┐      │
│  │  Web Browser │        │ Flutter App  │      │
│  │ (HTML/CSS/JS)│        │   (Dart)     │      │
│  └──────────────┘        └──────────────┘      │
└─────────────┬──────────────────┬────────────────┘
              │                  │
              ▼                  ▼
     ┌────────────────────────────────────┐
     │      FastAPI Backend (Render)      │
     │  ┌──────────────────────────────┐  │
     │  │  REST API Endpoints          │  │
     │  │  - /chat                     │  │
     │  │  - /personality              │  │
     │  │  - /upload_image             │  │
     │  │  - /chat_history             │  │
     │  └──────────────────────────────┘  │
     └────────────┬───────────────────────┘
                  │
        ┌─────────┼─────────┐
        ▼         ▼         ▼
   ┌────────┐ ┌─────────┐ ┌──────────┐
   │ Groq   │ │ Tavily  │ │   JSON   │
   │  LLM   │ │ Search  │ │ Storage  │
   │  API   │ │   API   │ │ (chats)  │
   └────────┘ └─────────┘ └──────────┘
```

### Data Flow
1. User sends message via web/mobile interface
2. FastAPI receives request with personality settings
3. System checks if web search is needed (keyword detection)
4. Query sent to Groq LLM or Tavily Search API
5. Response processed and returned to user
6. Chat history saved to JSON file

---

## 🌐 Live Demo

**🔗 Web Application:** [orion-ai-76hk.onrender.com](https://orion-ai-76hk.onrender.com)

**Try these features:**
- Ask questions and see instant responses
- Adjust personality sliders (humor, honesty, mode)
- Use voice input/output (click microphone icon)
- Upload images for analysis
- Create multiple chat sessions

**Note:** First request may take 30-60 seconds (cold start on free tier hosting)

---

## 📸 Screenshots

### Web Interface
**Main Chat Screen:**
- Clean, sci-fi inspired dark theme
- Real-time message streaming
- Personality controls sidebar
- Voice input/output buttons

**Personality Settings:**
- Humor slider (0-100%)
- Honesty slider (0-100%)
- Mode selector (Serious/Casual/Dry)

**Chat History:**
- Multiple session management
- Quick switch between conversations
- Delete unwanted chats

*(Screenshots to be added)*

---

## 🚀 Installation

### Prerequisites
- Python 3.8+
- pip package manager
- Git

### Clone Repository
```bash
git clone https://github.com/puneethgowdays/orion-ai-assistant.git
cd orion-ai-assistant
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Environment Variables
Create a `.env` file in the root directory:
```env
GROQ_API_KEY=your_groq_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

**Get API Keys:**
- Groq API: [console.groq.com](https://console.groq.com)
- Tavily API: [tavily.com](https://tavily.com)

### Run Locally
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Access at: `http://localhost:8000`

---

## 💻 Usage

### Web Application

**Start a Conversation:**
1. Open ORION in your browser
2. Type a message or click the microphone for voice input
3. ORION responds in 1-3 seconds

**Customize Personality:**
1. Open settings panel (gear icon)
2. Adjust humor and honesty sliders
3. Select communication mode
4. Changes apply to new messages

**Upload Images:**
1. Click image upload icon
2. Select image from device
3. ORION analyzes and describes the image

**Manage Chats:**
1. Click "New Chat" to start fresh conversation
2. Use sidebar to switch between chats
3. Delete unwanted chat sessions

### Voice Commands
- **Activate voice input:** Click microphone icon
- **Speak your query:** Wait for recording indicator
- **Automatic transcription:** Message appears in input box
- **Voice output:** Toggle speaker icon for audio responses

---

## 📡 API Endpoints

### POST `/chat`
Send a message and receive AI response
```json
{
  "message": "What's the weather today?",
  "chat_id": "chat_123",
  "personality": {
    "humor": 50,
    "honesty": 80,
    "mode": "casual"
  }
}
```

### POST `/upload_image`
Upload image for analysis
```
Content-Type: multipart/form-data
File: image.jpg
```

### GET `/chat_history/{chat_id}`
Retrieve chat history for specific session

### GET `/all_chats`
List all available chat sessions

### DELETE `/chat_history/{chat_id}`
Delete a specific chat session

### GET `/personality`
Get current personality settings

### POST `/personality`
Update personality configuration

---

## 📁 Project Structure

```
orion-ai-assistant/
├── main.py                 # FastAPI application entry point
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (not in repo)
├── .gitignore             # Git ignore rules
├── README.md              # This file
├── static/                # Frontend files
│   ├── index.html         # Web interface
│   ├── styles.css         # Styling
│   └── script.js          # Client-side logic
├── data/
│   └── chats.json         # Persistent chat storage
└── mobile/                # Flutter app (optional)
    ├── lib/
    │   └── main.dart      # Flutter app code
    └── pubspec.yaml       # Flutter dependencies
```

---

## 🎭 Personality System

### How It Works

**Personality Parameters:**
- **Humor (0-100%):** Controls wit, playfulness, and casual tone
- **Honesty (0-100%):** Adjusts diplomatic vs. direct responses
- **Mode:** Serious, Casual, or Dry communication style

**Implementation:**
```python
system_prompt = f"""
You are ORION, a pragmatic AI assistant.
Humor level: {humor}% - {"Witty and playful" if humor > 70 else "Balanced" if humor > 30 else "Serious"}
Honesty level: {honesty}% - {"Direct and blunt" if honesty > 70 else "Balanced" if honesty > 30 else "Diplomatic"}
Mode: {mode}
"""
```

**Example Responses:**

**Query:** "Is this code good?"

| Humor | Honesty | Mode | Response |
|-------|---------|------|----------|
| 10% | 10% | Serious | "Your code follows standard conventions and should function correctly." |
| 50% | 50% | Casual | "It works, but there's room for improvement in readability." |
| 90% | 90% | Dry | "It runs. Whether it's 'good' is a philosophical question I'll leave to you." |

---

## 🔮 Future Enhancements

**Planned Features:**
- [ ] User authentication and multi-user support
- [ ] Advanced chat search functionality
- [ ] Export chat history to PDF/text
- [ ] Custom voice selection (different accents/languages)
- [ ] Integration with more LLM providers
- [ ] Dark/light theme toggle
- [ ] Mobile app on iOS (currently Android only)
- [ ] API rate limiting and caching
- [ ] Advanced image analysis (OCR, object detection)
- [ ] Plugin system for extensibility

**Technical Improvements:**
- [ ] Database migration (PostgreSQL/MongoDB)
- [ ] Redis caching for frequently asked queries
- [ ] WebSocket support for real-time updates
- [ ] Docker containerization
- [ ] Comprehensive test suite
- [ ] CI/CD pipeline

---

## 🧪 Technical Challenges Solved

### 1. API Key Management
**Challenge:** Accidentally pushed API keys to GitHub  
**Solution:** Migrated to environment variables, regenerated all keys, added `.gitignore`

### 2. Identity Confusion
**Challenge:** ORION sometimes claimed to be other AI assistants  
**Solution:** Strengthened system prompt with explicit identity rules and restrictions

### 3. Response Length Control
**Challenge:** Overly verbose responses  
**Solution:** Implemented 200-token hard limit in system prompt

### 4. Mobile UI Issues
**Challenge:** Input bar hidden by mobile browser UI  
**Solution:** Used `100dvh` + sticky positioning + safe-area-inset CSS

### 5. Real-Time Search Consistency
**Challenge:** Groq's built-in search was unreliable  
**Solution:** Replaced with Tavily API + custom keyword detection system

### 6. Cold Start Delays
**Challenge:** First request on Render takes 30-60 seconds  
**Solution:** Documented in README; considering paid tier or keep-alive pings

---

## 📊 Performance Metrics

- **Response Time:** 1-3 seconds average
- **Uptime:** 99%+ (Render free tier, subject to cold starts)
- **API Calls:** Optimized with 200-token response limit
- **File Size:** 
  - Web app: ~50KB (HTML/CSS/JS)
  - Android APK: 46.5MB
  - Backend: Minimal footprint

---

## 🔒 Security & Privacy

- ✅ API keys stored as environment variables (never in code)
- ✅ HTTPS enforced by Render automatically
- ✅ No user data collection or storage (beyond chat history)
- ✅ Chat history stored locally (JSON file on server)
- ⚠️ Currently single-user system (no authentication)

**Note:** This is a personal learning project. For production use, implement proper authentication, encryption, and data protection measures.

---

## 📝 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

**TL;DR:** Free to use, modify, and distribute with attribution.

---

## 👨‍💻 Author

**Puneeth Gowda Y S**

- 🎓 Information Science Engineering Graduate
- 💼 Data Science Enthusiast
- 📧 Email: puneethgowdays2003@gmail.com
- 🔗 LinkedIn: [linkedin.com/in/puneethgowdays](https://linkedin.com/in/puneethgowdays)
- 💻 GitHub: [github.com/puneethgowdays](https://github.com/puneethgowdays)

---

## 🙏 Acknowledgments

- **Groq** - For lightning-fast LLM inference API
- **Tavily** - For reliable real-time search capabilities
- **Render.com** - For free-tier cloud hosting
- **FastAPI** - For excellent Python web framework
- **Flutter** - For cross-platform mobile development
- **Interstellar (2014)** - For TARS inspiration

---

## 📚 Learning Outcomes

**This project taught me:**
- ✅ FastAPI backend development and deployment
- ✅ LLM API integration and prompt engineering
- ✅ Real-time search integration
- ✅ Cross-platform development (Web + Mobile)
- ✅ Cloud deployment on Render.com
- ✅ Environment variable management
- ✅ API design and REST principles
- ✅ Debugging deployment issues
- ✅ Performance optimization (token limits, caching strategies)

**Built in:** ~2-3 weeks (March 2026)

---

## 🐛 Known Issues

- Cold start delay on Render free tier (30-60 seconds for first request)
- Voice input may not work on all browsers (best on Chrome)
- Image upload limited to 5MB files
- No offline functionality (requires internet connection)
- Single-user system (no multi-user authentication)

---

## 💡 Contributing

While this is primarily a personal learning project, suggestions and feedback are welcome!

**To contribute:**
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Commit your changes (`git commit -m 'Add improvement'`)
4. Push to branch (`git push origin feature/improvement`)
5. Open a Pull Request

---

## 📞 Support

**Questions or Issues?**
- Open an issue on GitHub
- Email: puneethgowdays2003@gmail.com
- Connect on LinkedIn

---

<div align="center">

### ⭐ If you found this project interesting, please consider giving it a star!

**Made with ❤️ by Puneeth Gowda**

![Made with Python](https://img.shields.io/badge/Made_with-Python-blue?style=for-the-badge&logo=python)
![Powered by AI](https://img.shields.io/badge/Powered_by-AI-purple?style=for-the-badge)

</div>

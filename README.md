<div align="center">

# 🎓 Doubt Defuser
### AI-Powered Context-Aware Doubt Resolution & Learning Assistant

[![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Groq](https://img.shields.io/badge/Groq-Llama%203.3%2070B-FF6B35?style=for-the-badge&logo=meta&logoColor=white)](https://groq.com)
[![Tkinter](https://img.shields.io/badge/UI-Tkinter%20%2B%20Pillow-blue?style=for-the-badge)](https://docs.python.org/3/library/tkinter.html)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Hackathon](https://img.shields.io/badge/Built%20For-Hackinnovation%202026-purple?style=for-the-badge)](.)
[![Version](https://img.shields.io/badge/Version-v5.1-orange?style=for-the-badge)](.)

> **Resolve academic doubts instantly with AI — grounded in your own syllabus.**  
> Built by Team Doubt Defusers for Hackinnovation 2026 🏆

</div>

---

## 📌 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [Subjects & Topics](#-subjects--topics)
- [Screenshots](#-screenshots)
- [Tech Stack](#-tech-stack)
- [Getting Started](#-getting-started)
- [How to Use](#-how-to-use)
- [Build EXE](#-build-standalone-exe)
- [Project Structure](#-project-structure)
- [How It Works](#-how-it-works)
- [Team](#-team)

---

## 🧠 Overview

**Doubt Defuser** is a desktop application that acts as a personal AI tutor for college students. It uses **Groq's Llama 3.3 70B** model to answer academic questions in real time — and uniquely, it verifies every question against your **uploaded syllabus PDF** before answering.

If a question is outside the syllabus, it warns you. If the topic is mismatched, it auto-suggests the correct one. This makes Doubt Defuser not just a chatbot — but a **smart, syllabus-aware academic assistant**.

---

## ✨ Key Features

### 🔍 Syllabus-Aware AI Answers
Upload your syllabus (PDF, DOCX, PPTX, Excel, HTML, CSV, or plain text) and every question is **verified against it** before answering. Questions not in the syllabus are flagged as **Out of Syllabus** — preventing irrelevant answers.

### 🧩 Smart Topic Mismatch Detection
If your question belongs to a different topic than the one selected, the AI **detects the mismatch** and suggests the correct topic automatically — with a one-click switch.

### 🎚️ 3 Explanation Levels
Choose how deep you want the explanation:
| Level | Style |
|-------|-------|
| 🟢 **Beginner** | Simple language, real-life examples, no jargon |
| 🟡 **Intermediate** | Academic language with examples |
| 🔴 **Advanced** | Precise technical language, edge cases, proofs |

### 📎 File Attachment & Vision OCR
Attach images, PDFs, DOCX, or TXT files directly to your question. Images are processed using **AI Vision (Llama 4 Scout)** for text extraction — no Tesseract needed.

### 🧠 Auto Quiz Generator
After any AI answer, click **Generate Quiz** to get:
- **5 MCQs** with 4 options each and instant answer checking
- **2 Descriptive questions** with model answers
- Live score tracking with a final scorecard

### 📚 Syllabus Topic Scanner
Upload your syllabus and the AI **automatically extracts all chapter/topic names**, displays them as clickable chips, and even **auto-detects the subject** — switching it for you if there's a mismatch.

### 💾 Session Export & History
- Full **session history** in the sidebar — click any past question to reload it
- **Export session** as a JSON file for future reference
- **Copy answer** to clipboard in one click

### 🖥️ Beautiful Modern Dark UI
Custom-built dark theme with:
- Pillow-rendered **gradient headers**
- **Rounded cards** and smooth hover effects
- Animated **spinner** while AI is thinking
- Live **character counter** and **word count**

---

## 📚 Subjects & Topics

| Subject | Topics |
|---------|--------|
| **Elements of Mechanical Engineering** | Engineering Materials, Thermodynamics Basics, Fluid Mechanics, Simple Machines, Power Transmission, Manufacturing Processes |
| **Applied Mathematics 2** | Differential Equations, Laplace Transforms, Fourier Series, Complex Numbers, Vector Calculus, Numerical Methods |
| **Data Structure** | Arrays & Linked Lists, Stacks & Queues, Trees & Graphs, Sorting Algorithms, Searching Algorithms, Hashing |
| **English** | Grammar & Composition, Technical Writing, Reading Comprehension, Vocabulary, Communication Skills, Presentation Skills |
| **Web Development** | HTML & CSS, JavaScript, Responsive Design, Frontend Frameworks, Backend Basics, Databases & APIs |

> 📌 When a syllabus PDF is uploaded, the **PDF becomes the authority** — topics not in the PDF are flagged as Out of Syllabus even if they relate to the subject.

---

## 🖼️ Screenshots

```
┌─────────────────────────────────────────────────────────────────────┐
│  🎓 Doubt Defuser          Our Hackathon Team         🔑 API Key ••• │
├────────────────┬────────────────────────────────────────────────────┤
│  ⚙ Settings   │  ❓ Ask Your Doubt                                  │
│                │  ┌──────────────────────────────────────────────┐  │
│  Subject ▼     │  │ 💬 Your Question                   0 chars   │  │
│  Topic   ▼     │  │                                              │  │
│  Level   ▼     │  │  Type your question here…                    │  │
│                │  └──────────────────────────────────────────────┘  │
│  🟢 Beginner   │  🚀 Resolve Doubt  🔄 Clear  📎 Attach  🧠 Quiz    │
│  🟡 Intermed.  │                                                     │
│  🔴 Advanced   │  💡 Answer                                          │
│                │  ┌──────────────────────────────────────────────┐  │
│  📄 Syllabus   │  │ 💡 AI Response                    0 words    │  │
│  📂 Upload     │  │                                              │  │
│                │  │  Ask a question to see the AI response…      │  │
│  🕘 History    │  │                                              │  │
│                │  └──────────────────────────────────────────────┘  │
│                │  💾 Export Session   📋 Copy Answer                 │
├────────────────┴────────────────────────────────────────────────────┤
│  ● Ready — type your question and click Resolve Doubt               │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **Language** | Python 3.8+ |
| **GUI Framework** | Tkinter + ttk |
| **UI Graphics** | Pillow (PIL) — gradients, rounded cards |
| **AI Model** | Groq API — Llama 3.3 70B Versatile |
| **Vision / OCR** | Llama 4 Scout 17B (via Groq) |
| **PDF Reading** | PyPDF2 / pypdf |
| **Word Docs** | python-docx |
| **Excel** | openpyxl |
| **PowerPoint** | python-pptx |
| **HTML Parsing** | BeautifulSoup4 |
| **HTTP Requests** | requests + urllib (fallback) |
| **Threading** | Python threading (non-blocking AI calls) |
| **Data Format** | JSON (session export) |

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- A [Groq API key](https://console.groq.com) (free to get)
- Internet connection

### Installation

**Step 1 — Clone or download the project**
```bash
git clone https://github.com/your-team/doubt-defuser.git
cd doubt-defuser
```

**Step 2 — Install dependencies**
```bash
pip install requests Pillow PyPDF2 python-docx openpyxl python-pptx beautifulsoup4
```

> ℹ️ The app also auto-installs missing packages on first run.

**Step 3 — Run the app**
```bash
python DoubtDefusersMain.pyw
```

Or simply **double-click** `DoubtDefusersMain.pyw` if Python is associated with `.pyw` files.

---

## 📖 How to Use

### 1️⃣ Set Your API Key
Enter your **Groq API key** in the top-right field. Click the 👁 eye icon to show/hide it.  
Get your free key at: [console.groq.com](https://console.groq.com)

### 2️⃣ Select Subject & Topic
Use the sidebar dropdowns to choose your **Subject** and **Topic**. The topic list updates automatically when you change the subject.

### 3️⃣ Upload Your Syllabus *(Optional but Recommended)*
Click **📂 Upload File** in the Syllabus section. Supported formats:

| Format | Extension |
|--------|-----------|
| PDF | `.pdf` |
| Word | `.docx`, `.doc`, `.odt` |
| PowerPoint | `.pptx`, `.ppt`, `.odp` |
| Excel | `.xlsx`, `.xls`, `.ods` |
| Text | `.txt`, `.md`, `.csv`, `.rtf` |
| Web | `.html`, `.htm` |

After upload, the AI **scans and extracts all topics** from the document — click any topic chip to set it instantly.

### 4️⃣ Ask Your Doubt
Type your question in the question box and press **🚀 Resolve Doubt** or hit `Enter`.

The AI will:
1. **Check relevance** against your syllabus/topic
2. **Alert you** if the question is out of syllabus or on a different topic
3. **Generate a structured answer** with explanation, steps, and examples

### 5️⃣ Generate a Quiz 🧠
After any answer, click **🧠 Generate Quiz** to test your understanding with 5 MCQs + 2 descriptive questions auto-generated from that answer.

### 6️⃣ Attach Files 📎
Click **📎 Attach** to include an image or document with your question. Images are OCR-processed by AI vision automatically.

---

## 📦 Build Standalone EXE

To convert the app into a single `.exe` file that runs without Python installed:

### Quick Build (using the provided batch file)

1. Place `BUILD_EXE.bat` in the same folder as `DoubtDefusersMain.pyw`
2. **Right-click → Run as Administrator**
3. Wait 1–3 minutes
4. Find your EXE at `dist\DoubtDefuser.exe`

### Manual Build Command

```bash
# Step 1 — Install PyInstaller
pip install pyinstaller pyinstaller-hooks-contrib

# Step 2 — Copy .pyw to .py
copy DoubtDefusersMain.pyw DoubtDefusersMain.py

# Step 3 — Build
pyinstaller --onefile --windowed --name "DoubtDefuser" --icon=icon.ico ^
  --hidden-import=requests --hidden-import=PIL --hidden-import=PIL._imagingtk ^
  --hidden-import=PIL.Image --hidden-import=PIL.ImageDraw ^
  --hidden-import=PIL.ImageFilter --hidden-import=PIL.ImageTk ^
  --hidden-import=PyPDF2 --hidden-import=docx --hidden-import=docx.oxml ^
  --hidden-import=openpyxl --hidden-import=pptx --hidden-import=bs4 ^
  --hidden-import=tkinter --hidden-import=tkinter.ttk ^
  --hidden-import=tkinter.filedialog --hidden-import=tkinter.messagebox ^
  --collect-all=PIL --collect-all=requests --collect-all=docx ^
  --collect-all=openpyxl --collect-all=pptx --collect-all=bs4 ^
  --collect-all=PyPDF2 --noconfirm DoubtDefusersMain.py
```

---

## 📁 Project Structure

```
DoubtDefuser/
│
├── DoubtDefusersMain.pyw      # Main application file
├── icon.ico                   # App icon
├── BUILD_EXE.bat              # Auto EXE builder script
├── README.md                  # This file
│
└── dist/                      # Created after build
    └── DoubtDefuser.exe       # Standalone executable
```

---

## ⚙️ How It Works

```
Student asks a question
        │
        ▼
┌───────────────────┐
│  Relevance Check  │  ◄── Checks against uploaded syllabus PDF (primary)
│  (Groq AI)        │       or hardcoded topic list (fallback)
└───────────────────┘
        │
   ┌────┴────┐
   │         │
   ▼         ▼
  OK      Mismatch / OOS
   │         │
   │    ┌────┴──────────────┐
   │    │ Show Dialog:      │
   │    │ • Switch topic?   │
   │    │ • Still answer?   │
   │    └────────────────┘
   │              │ Yes
   ▼              ▼
┌──────────────────────────┐
│  Get AI Answer (Groq)    │
│  • Syllabus-grounded     │
│  • Level-adjusted        │
│  • Structured format     │
└──────────────────────────┘
        │
        ▼
┌──────────────────────────┐
│  Display Answer          │
│  + Save to History       │
│  + Enable Quiz Generator │
└──────────────────────────┘
```

### Syllabus Authority Logic
| Scenario | Behavior |
|----------|----------|
| **PDF uploaded + question in PDF** | ✅ Answer normally |
| **PDF uploaded + question NOT in PDF** | ⚠️ Out of Syllabus warning |
| **No PDF + question matches topic** | ✅ Answer normally |
| **No PDF + question is off-topic** | ⚠️ Topic mismatch dialog |
| **Completely unrelated question** | ⚠️ Out of Syllabus dialog |

---

## 👥 Team

<div align="center">

**Team Doubt Defusers** — Hackinnovation 2026

| Role | Responsibility |
|------|---------------|
| 👨‍💻 Developer | Core app, AI integration, UI |
| 🎨 Designer | UI/UX, color theme, layout |
| 📊 Presenter | Demo, documentation, slides |
| 🧪 Tester | QA, edge cases, feedback |

</div>

---

## 🔑 API Key Setup

1. Go to [console.groq.com](https://console.groq.com)
2. Sign up for a free account
3. Navigate to **API Keys** → **Create API Key**
4. Copy the key and paste it into the app's top-right field

> ⚠️ Keep your API key private. Do not commit it to public repositories.

---

## 🐛 Troubleshooting

| Problem | Fix |
|---------|-----|
| `No module named pyinstaller` | Use `pyinstaller` directly instead of `python -m pyinstaller` |
| App won't start | Run `pip install Pillow requests PyPDF2` |
| API error 401 | Check your Groq API key |
| API error 403 | Switch to mobile hotspot or use VPN |
| Rate limit (429) | Wait 30 seconds and try again |
| PDF not reading | Install `pip install PyPDF2` |
| EXE build fails | Run `BUILD_EXE.bat` as Administrator, disable antivirus temporarily |

---

## 📄 License

This project was built for **Hackinnovation 2026** by Team Doubt Defusers.  
Free to use for educational purposes.

---

<div align="center">

Made with ❤️ by **Team Doubt Defusers**  
*Hackinnovation 2026 — Turning doubts into understanding, one question at a time.*

⭐ Star this repo if Doubt Defuser helped you!

</div>

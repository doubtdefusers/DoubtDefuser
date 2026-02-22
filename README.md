# Doubt Defuser
AI-Powered Context-Aware Doubt Resolution & Learning Assistant

Built for Hackinnovation 2026

---

## Overview

Doubt Defuser is a desktop AI learning assistant for college students.  
It provides syllabus-aware academic answers using Groq’s Llama 3.3 70B model.

The application verifies every question against an uploaded syllabus before answering.  
If a question is outside the syllabus, it is flagged.  
If the topic is mismatched, the system suggests the correct topic.

---

## Features

### Syllabus-Aware Answering
- Upload syllabus files (PDF, DOCX, PPTX, Excel, HTML, CSV, TXT)
- Questions are verified against the syllabus
- Out-of-syllabus questions are flagged

### Topic Mismatch Detection
- Detects incorrect topic selection
- Suggests the correct topic
- One-click topic switching

### Explanation Levels
- Beginner – Simple explanations
- Intermediate – Academic explanations
- Advanced – Technical depth and detailed reasoning

### File Attachments
- Attach images or documents
- Vision-based OCR support
- Extracts text from images automatically

### Auto Quiz Generator
- 5 MCQs with answer checking
- 2 descriptive questions
- Score tracking

### Session Management
- Question history
- Export session as JSON
- Copy answers

---

## Supported Subjects

- Elements of Mechanical Engineering
- Applied Mathematics 2
- Data Structure
- English
- Web Development

When a syllabus file is uploaded, only topics inside that file are considered valid.

---

## Tech Stack

- Python 3.8+
- Tkinter + ttk
- Pillow
- Groq API (Llama 3.3 70B)
- PyPDF2
- python-docx
- openpyxl
- python-pptx
- BeautifulSoup4
- requests
- JSON

---

## Installation

### Clone Repository

```bash
git clone https://github.com/your-team/doubt-defuser.git
cd doubt-defuser

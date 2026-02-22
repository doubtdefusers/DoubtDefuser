"""
AI-Powered Context-Aware Doubt Resolution & Learning Assistant
Beautiful Modern UI — Tkinter Edition v5.1 -- Doubt Defusers
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import tkinter.font as tkfont
import threading, json, os, subprocess, sys
from datetime import datetime

# ── Auto-install ──────────────────────────────────────────────────
for _pkg in ["requests", "Pillow", "PyPDF2", "python-docx"]:
    try:
        __import__(_pkg.replace("Pillow","PIL").replace("python-docx","docx"))
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", _pkg, "-q"])

from PIL import Image, ImageDraw, ImageFilter, ImageTk

# ═════════════════════════════════════════════════════════════════
#  DATA
# ═════════════════════════════════════════════════════════════════
SUBJECT_TOPICS = {
    "Elements of Mechanical Engineering": [
        "Engineering Materials", "Thermodynamics Basics", "Fluid Mechanics",
        "Simple Machines", "Power Transmission", "Manufacturing Processes",
    ],
    "Applied Mathematics 2": [
        "Differential Equations", "Laplace Transforms", "Fourier Series",
        "Complex Numbers", "Vector Calculus", "Numerical Methods",
    ],
    "Data Structure": [
        "Arrays & Linked Lists", "Stacks & Queues", "Trees & Graphs",
        "Sorting Algorithms", "Searching Algorithms", "Hashing",
    ],
    "English": [
        "Grammar & Composition", "Technical Writing", "Reading Comprehension",
        "Vocabulary", "Communication Skills", "Presentation Skills",
    ],
    "Web Development": [
        "HTML & CSS", "JavaScript", "Responsive Design",
        "Frontend Frameworks", "Backend Basics", "Databases & APIs",
    ],
}

LEVEL_PROMPTS = {
    "Beginner":     "Use very simple language, real-life examples, and avoid jargon.",
    "Intermediate": "Use standard academic language with some examples.",
    "Advanced":     "Use precise technical language, include edge cases and proofs.",
}

GROQ_API_KEY = "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"

# ═════════════════════════════════════════════════════════════════
#  THEME  — Blue Accent + Rich Dark Palette
# ═════════════════════════════════════════════════════════════════
C = {
    "bg":           "#080B14",
    "sidebar":      "#0D1117",
    "card":         "#161B27",
    "card2":        "#1C2130",
    "input":        "#1E2436",
    "border":       "#252D42",
    "border2":      "#2E3A55",
    "accent":       "#3B82F6",
    "accent_light": "#60A5FA",
    "accent_dark":  "#1D4ED8",
    "accent_glow":  "#1E3A5F",
    "green":        "#10B981",
    "green_dark":   "#064E3B",
    "yellow":       "#F59E0B",
    "red":          "#EF4444",
    "text":         "#E2E8F0",
    "text2":        "#8B9AB5",
    "text3":        "#3D4F6B",
    "white":        "#FFFFFF",
    "header_top":   "#0F172A",
    "header_bot":   "#1E3A5F",
}

FF     = "Segoe UI"
FF_M   = "Segoe UI Semibold"
FF_B   = "Segoe UI Bold"

# ── OCR A Extended font resolution ────────────────────────────────
def _resolve_ocr_font():
    """Try OCR A Extended, then OCR A, then Courier New as fallback."""
    families = tkfont.families()
    for candidate in ("OCR A Extended", "OCR A", "OCR A Std", "Courier New"):
        if candidate in families:
            return candidate
    return "Courier New"

FF_OCR = "Courier New"   # resolved after Tk root exists


# ═════════════════════════════════════════════════════════════════
#  PILLOW HELPERS
# ═════════════════════════════════════════════════════════════════
def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def make_gradient_img(w, h, color1, color2, vertical=True):
    base = Image.new("RGB", (max(w,1), max(h,1)), color1)
    top  = Image.new("RGB", (max(w,1), max(h,1)), color2)
    mask = Image.new("L",   (max(w,1), max(h,1)))
    md   = ImageDraw.Draw(mask)
    steps = h if vertical else w
    for i in range(steps):
        val = int(255 * i / max(steps, 1))
        if vertical:
            md.line([(0, i), (w, i)], fill=val)
        else:
            md.line([(i, 0), (i, h)], fill=val)
    base.paste(top, mask=mask)
    return base

def make_rounded_rect(w, h, r, fill, border=None, border_width=1):
    img  = Image.new("RGBA", (max(w,1), max(h,1)), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([0, 0, w-1, h-1], radius=r,
                            fill=hex_to_rgb(fill) + (255,))
    if border:
        for t in range(border_width):
            draw.rounded_rectangle([t, t, w-1-t, h-1-t], radius=r,
                                    outline=hex_to_rgb(border) + (255,))
    return img


# ═════════════════════════════════════════════════════════════════
#  PILLOW WIDGETS
# ═════════════════════════════════════════════════════════════════
class RoundedCard(tk.Canvas):
    """Canvas with Pillow-drawn rounded rectangle background."""
    def __init__(self, parent, bg_color=None, radius=12,
                 border_color=None, border_w=1, **kw):
        bg_color     = bg_color     or C["card"]
        border_color = border_color or C["border"]
        super().__init__(parent, bg=parent["bg"],
                         highlightthickness=0, bd=0, **kw)
        self._fill, self._border = bg_color, border_color
        self._bw, self._r = border_w, radius
        self._photo = None
        self.bind("<Configure>", self._redraw)

    def _redraw(self, e=None):
        w, h = self.winfo_width(), self.winfo_height()
        if w < 4 or h < 4:
            return
        img = make_rounded_rect(w, h, self._r, self._fill,
                                 self._border, self._bw)
        self._photo = ImageTk.PhotoImage(img)
        self.delete("bg")
        self.create_image(0, 0, anchor="nw", image=self._photo, tags="bg")
        self.tag_lower("bg")

    def update_border(self, color):
        self._border = color
        self._redraw()


class GradientHeader(tk.Canvas):
    """Pillow gradient header bar."""
    def __init__(self, parent, h=70, color1="#0F172A", color2="#1E3A5F", **kw):
        super().__init__(parent, height=h, highlightthickness=0, bd=0, **kw)
        self._c1, self._c2, self._h = color1, color2, h
        self._photo = None
        self.bind("<Configure>", self._redraw)

    def _redraw(self, e=None):
        w = self.winfo_width()
        if w < 4:
            return
        img = make_gradient_img(w, self._h,
                                 hex_to_rgb(self._c1),
                                 hex_to_rgb(self._c2),
                                 vertical=False)
        draw = ImageDraw.Draw(img)
        accent = hex_to_rgb(C["accent"])
        draw.line([(0, self._h - 2), (w, self._h - 2)], fill=accent, width=2)
        self._photo = ImageTk.PhotoImage(img)
        self.delete("grad")
        self.create_image(0, 0, anchor="nw", image=self._photo, tags="grad")
        self.tag_lower("grad")


# ═════════════════════════════════════════════════════════════════
#  GROQ API
# ═════════════════════════════════════════════════════════════════
def call_groq(api_key: str, prompt: str) -> str:
    payload = json.dumps({
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.4,
        "max_tokens": 1024,
    })
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
        "User-Agent": "Mozilla/5.0",
    }
    url = "https://api.groq.com/openai/v1/chat/completions"
    try:
        import requests as rl
        r = rl.post(url, data=payload.encode(), headers=headers, timeout=30)
        if r.status_code == 200:
            return r.json()["choices"][0]["message"]["content"]
        raise Exception(f"{r.status_code}: {r.text[:200]}")
    except ImportError:
        pass
    import urllib.request, ssl
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    req = urllib.request.Request(url, data=payload.encode(), headers=headers)
    with urllib.request.urlopen(req, timeout=30, context=ctx) as r:
        return json.loads(r.read())["choices"][0]["message"]["content"]


def check_question_relevance(question, subject, topic, all_topics, syllabus_text, api_key) -> dict:
    """
    Returns a dict with keys:
      status : "ok" | "topic_mismatch" | "oos"
      suggested_topic : str  (only when status == "topic_mismatch")

    Logic:
      - If a syllabus PDF is uploaded, it is the PRIMARY authority.
        A question NOT covered in the PDF is OOS — even if it seems
        related to the subject.
      - If no PDF is uploaded, fall back to SUBJECT_TOPICS list check.
    """
    has_syllabus = bool(syllabus_text.strip())
    topics_list  = ", ".join(all_topics)

    if has_syllabus:
        # ── PDF-based check: PDF is the ground truth ───────────────
        prompt = (
            "You are a strict academic syllabus checker for a student doubt-resolution app.\n\n"
            "SUBJECT: " + subject + "\n"
            "SELECTED TOPIC: \"" + topic + "\"\n\n"
            "SYLLABUS CONTENT (this is the OFFICIAL syllabus — treat it as the ONLY authority):\n"
            "------\n"
            + syllabus_text[:3000] +
            "\n------\n\n"
            "STUDENT QUESTION: \"" + question + "\"\n\n"
            "Your task:\n"
            "1. Check whether the student's question is covered by the SYLLABUS CONTENT above.\n"
            "   - Even if the topic seems related to the subject, if it is NOT present in the "
            "syllabus text, it is OUT OF SYLLABUS.\n"
            "2. If the question IS in the syllabus AND matches the selected topic -> reply: OK\n"
            "3. If the question IS in the syllabus BUT matches a DIFFERENT topic "
            "(from this list: " + topics_list + ") -> reply: TOPIC:<matching topic name>\n"
            "4. If the question is NOT covered anywhere in the syllabus -> reply: OOS\n\n"
            "Reply with ONLY one of these formats: OK | TOPIC:<name> | OOS\n"
            "No explanation. No extra text."
        )
    else:
        # ── Fallback: use hardcoded topic list only ─────────────────
        prompt = (
            "You are an academic relevance checker for a student doubt app.\n"
            "Available topics for subject \"" + subject + "\": " + topics_list + "\n"
            "Student selected topic: \"" + topic + "\"\n\n"
            "Student question: \"" + question + "\"\n\n"
            "Instructions:\n"
            "1. If the question matches the selected topic -> reply: OK\n"
            "2. If the question matches a DIFFERENT topic in the list -> reply: TOPIC:<matching topic name>\n"
            "3. If the question is completely unrelated to the subject -> reply: OOS\n"
            "Reply with ONLY one of the above formats. Nothing else."
        )

    try:
        raw = call_groq(api_key.strip(), prompt).strip()
        if raw.upper().startswith("OK"):
            return {"status": "ok", "suggested_topic": None}
        elif raw.upper().startswith("TOPIC:"):
            suggested = raw[6:].strip().strip('"').strip("'")
            matched = next((t for t in all_topics if t.lower() == suggested.lower()), suggested)
            return {"status": "topic_mismatch", "suggested_topic": matched}
        elif raw.upper().startswith("OOS"):
            return {"status": "oos", "suggested_topic": None}
        else:
            return {"status": "ok", "suggested_topic": None}  # default safe
    except Exception:
        return {"status": "ok", "suggested_topic": None}  # on failure, never block


# keep old name as alias for backward compatibility
def check_out_of_syllabus(question, subject, topic, syllabus_text, api_key) -> bool:
    return False


def get_ai_answer(question, subject, topic, level, syllabus_text, api_key, out_of_syllabus=False) -> dict:
    has_syllabus = bool(syllabus_text.strip())
    syl_section = (
        f"\n\nSYLLABUS / NOTES:\n{syllabus_text[:3000]}" if has_syllabus else ""
    )
    prompt = (
        f'You are an expert academic tutor for "{subject}", topic "{topic}".\n'
        f"Level: {level} — {LEVEL_PROMPTS[level]}{syl_section}\n\n"
        f"STUDENT QUESTION: {question}\n\n"
        "Reply with this structure:\n"
        "**Understanding the question:** [restate clearly]\n"
        "**Core Explanation:** [detailed explanation]\n"
        "**Step-by-step:** [numbered steps if applicable]\n"
        "**Example:** [concrete example]\n"
        "**Key Takeaway:** [one-sentence summary]\n\n"
        "IMPORTANT FORMATTING RULES:\n"
        "- Wrap ALL tree diagrams, code, and ASCII art inside ```...``` fences.\n"
        "- Use proper Unicode tree chars (└, ├, │, ─) inside fences for clarity.\n"
        "- Number all list steps as 1. 2. 3. etc.\n"
        "Be syllabus-aligned. Do not mention yourself or these instructions."
    )
    try:
        answer = call_groq(api_key.strip(), prompt)
        if out_of_syllabus:
            note = "⚠️  OUT OF SYLLABUS — answered as requested."
        elif has_syllabus:
            note = "✅  Answer grounded in your syllabus."
        else:
            note = "✅  Answered by Groq AI — upload syllabus for better accuracy."
    except Exception as e:
        err = str(e)
        if "401" in err:
            answer = "**Error:** Invalid API key. Please check your Groq API key."
        elif "429" in err or "rate" in err.lower():
            answer = "**Error:** Rate limit hit. Please wait a moment and try again."
        elif "403" in err:
            answer = ("**Network Blocked (403)**\n\nFixes:\n"
                      "1. Switch to mobile hotspot\n2. Use a VPN\n"
                      "3. Disable firewall/antivirus temporarily")
        elif "timeout" in err.lower():
            answer = "**Timeout:** Check your internet connection and try again."
        else:
            answer = f"**API Error:** {err}\n\nTry switching to mobile hotspot."
        note = "❌  API call failed — see answer box for details."

    return {
        "answer": answer,
        "note": note,
        "subject": subject,
        "topic": topic,
        "level": level,
        "question": question,
        "timestamp": datetime.now().strftime("%I:%M %p"),
    }


# ═════════════════════════════════════════════════════════════════
#  MAIN APP
# ═════════════════════════════════════════════════════════════════
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Doubt Defuser — Our Hackathon Team")
        self.geometry("1340x840")
        self.minsize(1060, 680)
        self.configure(bg=C["bg"])

        self.syllabus_text      = ""
        self.history            = []
        self.api_key_var        = tk.StringVar(value=GROQ_API_KEY)
        self.subject_var        = tk.StringVar(value=list(SUBJECT_TOPICS.keys())[0])
        self.topic_var          = tk.StringVar()
        self.level_var          = tk.StringVar(value="Intermediate")
        self._spinning          = False
        self.attached_file_text = ""
        self.attached_file_name = ""
        self._pill_images       = {}
        self._dividers          = []
        self._sep_ph            = None
        self._last_answer       = ""

        # Resolve OCR font after Tk root exists
        global FF_OCR
        FF_OCR = _resolve_ocr_font()

        self._styles()
        self._header()
        self._body()
        self._statusbar()
        self._refresh_topics()

    # ─────────────────────────────────────────────────────────────
    def _styles(self):
        s = ttk.Style(self)
        s.theme_use("clam")
        s.configure("CB.TCombobox",
            fieldbackground=C["input"], background=C["input"],
            foreground=C["text"], selectbackground=C["accent"],
            selectforeground=C["white"], arrowcolor=C["accent_light"],
            borderwidth=0, relief="flat", padding=8, font=(FF, 9))
        s.map("CB.TCombobox",
            fieldbackground=[("readonly", C["input"])],
            foreground=[("readonly", C["text"])],
            background=[("readonly", C["input"])])
        s.configure("Dark.Vertical.TScrollbar",
            troughcolor=C["card"], background=C["border2"],
            borderwidth=0, arrowsize=12,
            arrowcolor=C["text2"], relief="flat", width=8)
        s.map("Dark.Vertical.TScrollbar",
            background=[("active", C["accent"]), ("pressed", C["accent_dark"])],
            arrowcolor=[("active", C["white"])])

    # ─────────────────────────────────────────────────────────────
    def _header(self):
        gh = GradientHeader(self, h=70,
                            color1=C["header_top"],
                            color2=C["header_bot"],
                            bg=C["bg"])
        gh.pack(fill="x")

        lf = tk.Frame(gh, bg=C["header_top"])
        lf.place(x=20, rely=0.5, anchor="w")

        ic = tk.Canvas(lf, width=42, height=42,
                        bg=C["header_top"], highlightthickness=0)
        ic.pack(side="left", padx=(0, 10))
        ic_img = make_rounded_rect(42, 42, 21, C["accent"], C["accent_light"], 2)
        self._ic_ph = ImageTk.PhotoImage(ic_img)
        ic.create_image(0, 0, anchor="nw", image=self._ic_ph)
        ic.create_text(21, 21, text="🎓", font=(FF, 18), fill=C["white"])

        name_f = tk.Frame(lf, bg=C["header_top"])
        name_f.pack(side="left")
        tk.Label(name_f, text="Doubt Defuser",
                 font=(FF_B, 15), bg=C["header_top"],
                 fg=C["white"]).pack(anchor="w")
        tk.Label(name_f, text="Our Hackathon Team",
                 font=(FF, 8), bg=C["header_top"],
                 fg=C["text2"]).pack(anchor="w")

        rf = tk.Frame(gh, bg=C["header_top"])
        rf.place(relx=1.0, rely=0.5, anchor="e", x=-20)

        ew, eh = 290, 36
        e_img = make_rounded_rect(ew, eh, 8, C["input"], C["border2"], 1)
        self._e_ph = ImageTk.PhotoImage(e_img)
        e_canvas = tk.Canvas(rf, width=ew, height=eh,
                              bg=C["header_top"], highlightthickness=0)
        e_canvas.pack(side="left", padx=(0, 8))
        e_canvas.create_image(0, 0, anchor="nw", image=self._e_ph)
        e_canvas.create_text(14, eh//2, text="🔑", font=(FF, 11),
                              fill=C["accent_light"], anchor="w")
        e_canvas.create_text(38, eh//2 - 1, text="API Key",
                              font=(FF, 7), fill=C["text2"], anchor="w")
        self._api_e = tk.Entry(e_canvas, textvariable=self.api_key_var,
                               font=(FF, 9), width=24, show="•",
                               bg=C["input"], fg=C["text"],
                               insertbackground=C["white"],
                               relief="flat", bd=0, highlightthickness=0)
        e_canvas.create_window(160, eh//2 + 1, window=self._api_e,
                                anchor="center", width=160, height=22)

        def toggle():
            self._api_e.config(
                show="" if self._api_e.cget("show") == "•" else "•")

        eye_img = make_rounded_rect(38, 32, 6, C["accent_dark"],
                                     C["accent"], 1)
        self._eye_ph = ImageTk.PhotoImage(eye_img)
        eye_c = tk.Canvas(rf, width=38, height=32,
                           bg=C["header_top"], highlightthickness=0,
                           cursor="hand2")
        eye_c.pack(side="left")
        eye_c.create_image(0, 0, anchor="nw", image=self._eye_ph)
        eye_c.create_text(19, 16, text="👁", font=(FF, 13), fill=C["white"])
        eye_c.bind("<Button-1>", lambda e: toggle())

    # ─────────────────────────────────────────────────────────────
    def _body(self):
        body = tk.Frame(self, bg=C["bg"])
        body.pack(fill="both", expand=True)

        sb_frame = tk.Frame(body, bg=C["sidebar"], width=340)
        sb_frame.pack(side="left", fill="y")
        sb_frame.pack_propagate(False)
        self._sidebar(sb_frame)

        sep = tk.Canvas(body, width=2, bg=C["bg"], highlightthickness=0)
        sep.pack(side="left", fill="y")
        sep.bind("<Configure>", lambda e: self._draw_sep(sep))

        main = tk.Frame(body, bg=C["bg"])
        main.pack(side="left", fill="both", expand=True)
        self._main(main)

    def _draw_sep(self, canvas):
        h = canvas.winfo_height()
        if h < 4:
            return
        canvas.delete("all")
        img = make_gradient_img(2, h,
                                 hex_to_rgb(C["border"]),
                                 hex_to_rgb(C["accent_dark"]),
                                 vertical=True)
        ph = ImageTk.PhotoImage(img)
        self._sep_ph = ph
        canvas.create_image(0, 0, anchor="nw", image=ph)

    # ─────────────────────────────────────────────────────────────
    def _sidebar(self, sb):
        sc = tk.Canvas(sb, bg=C["sidebar"], highlightthickness=0, bd=0)
        sv = ttk.Scrollbar(sb, orient="vertical",
                            style="Dark.Vertical.TScrollbar",
                            command=sc.yview)
        sc.configure(yscrollcommand=sv.set)
        sv.pack(side="right", fill="y")
        sc.pack(fill="both", expand=True)

        pad = tk.Frame(sc, bg=C["sidebar"])
        win_id = sc.create_window((0, 0), window=pad, anchor="nw")

        sc.bind("<Configure>", lambda e: sc.itemconfig(win_id, width=e.width))
        pad.bind("<Configure>",
                 lambda e: sc.configure(scrollregion=sc.bbox("all")))
        sc.bind_all("<MouseWheel>",
                    lambda e: sc.yview_scroll(int(-1*(e.delta/120)), "units"))

        inner = tk.Frame(pad, bg=C["sidebar"])
        inner.pack(fill="both", expand=True, padx=14, pady=16)

        # ── Settings ─────────────────────────────────────────────
        self._sec(inner, "⚙", "Context Settings")
        s1 = self._card(inner)
        self._field(s1, "Subject", self.subject_var,
                    list(SUBJECT_TOPICS.keys()),
                    lambda e: self._refresh_topics())
        self._divider(s1)
        self._field(s1, "Topic", self.topic_var, [])
        self._divider(s1)
        self._field(s1, "Explanation Level", self.level_var,
                    list(LEVEL_PROMPTS.keys()))

        self._spacer(s1, 10)
        pills = tk.Frame(s1, bg=C["card"])
        pills.pack(fill="x", padx=0)
        for lvl, bg, fg in [
            ("Beginner",     "#064E3B", "#10B981"),
            ("Intermediate", "#78350F", "#F59E0B"),
            ("Advanced",     "#7F1D1D", "#EF4444"),
        ]:
            self._pill_btn(pills, lvl, bg, fg)

        self._spacer(inner, 14)

        # ── Syllabus — REMOVED "Paste Text" button as requested ──
        self._sec(inner, "📄", "Syllabus")
        s2 = self._card(inner)

        self.syl_status = tk.Label(s2,
            text="No material uploaded",
            font=(FF, 8), fg=C["text2"], bg=C["card"],
            anchor="w", wraplength=250)
        self.syl_status.pack(fill="x", pady=(0, 10))

        br = tk.Frame(s2, bg=C["card"])
        br.pack(fill="x")
        # Only Upload File button — Paste Text removed
        self._btn(br, "📂  Upload File",
                  self._upload_syllabus,
                  C["green_dark"], hover=C["green"]).pack(side="left")

        self._spacer(s2, 10)
        self.syl_prev = tk.Text(s2, height=5, font=("Consolas", 7),
            bg=C["input"], fg=C["text2"],
            relief="flat", bd=0, wrap="word",
            state="disabled", padx=8, pady=8,
            highlightthickness=1,
            highlightbackground=C["border"])
        self.syl_prev.pack(fill="x")

        self._spacer(inner, 14)

        # ── History ──────────────────────────────────────────────
        self._sec(inner, "🕘", "Session History")
        s3 = self._card(inner)

        hist_wrap = tk.Frame(s3, bg=C["input"],
                              highlightthickness=1,
                              highlightbackground=C["border"])
        hist_wrap.pack(fill="x")
        self.hist_lb = tk.Listbox(hist_wrap,
            font=(FF, 8), bg=C["input"], fg=C["text"],
            selectbackground=C["accent_glow"],
            selectforeground=C["accent_light"],
            relief="flat", bd=0, activestyle="none",
            highlightthickness=0, height=8)
        self.hist_lb.pack(fill="both", expand=True, padx=2, pady=2)
        self.hist_lb.bind("<<ListboxSelect>>", self._load_hist)

        self._spacer(s3, 8)
        self._btn(s3, "🗑  Clear History",
                  self._clear_hist, C["border2"],
                  hover="#7F1D1D").pack(anchor="w")

        self._spacer(inner, 20)

    # ─────────────────────────────────────────────────────────────
    def _main(self, main):
        main.rowconfigure(1, weight=1)
        main.columnconfigure(0, weight=1)

        # ── Question Area ─────────────────────────────────────────
        top = tk.Frame(main, bg=C["bg"])
        top.grid(row=0, column=0, sticky="ew", padx=20, pady=(18, 8))
        top.columnconfigure(0, weight=1)

        self._sec(top, "❓", "Ask Your Doubt")

        q_outer = tk.Frame(top, bg=C["accent"], padx=3, pady=0)
        q_outer.pack(fill="x")

        qinner = tk.Frame(q_outer, bg=C["card"])
        qinner.pack(fill="both", expand=True)

        q_head = tk.Frame(qinner, bg=C["card2"])
        q_head.pack(fill="x")
        tk.Label(q_head, text="  💬  Your Question",
                 font=(FF, 8), fg=C["text2"],
                 bg=C["card2"]).pack(side="left", pady=7)
        self.char_lbl = tk.Label(q_head, text="0 chars",
            font=(FF, 7), fg=C["text3"], bg=C["card2"])
        self.char_lbl.pack(side="right", padx=12)

        div1 = tk.Canvas(qinner, height=2, bg=C["card"], highlightthickness=0)
        div1.pack(fill="x")
        div1.bind("<Configure>", lambda e: self._draw_div(div1))

        self.q_box = tk.Text(qinner, height=4,
            font=(FF, 11), bg=C["card"], fg=C["text2"],
            insertbackground=C["accent_light"],
            relief="flat", bd=0, wrap="word",
            padx=16, pady=14, highlightthickness=0)
        self.q_box.pack(fill="x")
        self.q_box.insert("1.0", "Type your question here…")
        self.q_box.bind("<FocusIn>",    self._qin)
        self.q_box.bind("<FocusOut>",   self._qout)
        self.q_box.bind("<KeyRelease>", self._update_char_count)
        self.q_box.bind("<Return>",
                        lambda e: (self._ask(), "break")[1])

        div2 = tk.Canvas(qinner, height=2, bg=C["card"], highlightthickness=0)
        div2.pack(fill="x")
        div2.bind("<Configure>", lambda e: self._draw_div(div2))

        # Toolbar — Confidence Meter removed as requested
        tb = tk.Frame(qinner, bg=C["card2"], pady=10)
        tb.pack(fill="x", padx=12)

        ask_wrap = tk.Frame(tb, bg=C["accent"], padx=2, pady=2)
        ask_wrap.pack(side="left")
        self.ask_btn = tk.Button(
            ask_wrap,
            text="🚀  Resolve Doubt",
            command=self._ask,
            font=(FF_B, 10),
            bg=C["accent"], fg=C["white"],
            relief="flat", bd=0,
            padx=22, pady=9, cursor="hand2",
            activebackground=C["accent_light"],
            activeforeground=C["white"])
        self.ask_btn.pack()
        self._add_hover(self.ask_btn, C["accent"], C["accent_light"])

        self._btn(tb, "🔄  Clear", self._clear_all,
                  C["border2"], hover=C["accent_dark"]
                  ).pack(side="left", padx=(10, 0))

        self.attach_btn = self._btn(tb, "📎  Attach",
                                     self._attach_file,
                                     C["green_dark"], hover=C["green"])
        self.attach_btn.pack(side="left", padx=(8, 0))

        # 🧠 Quiz button — right next to Attach
        quiz_wrap = tk.Frame(tb, bg="#A78BFA", padx=2, pady=2)
        quiz_wrap.pack(side="left", padx=(8, 0))
        self.quiz_btn = tk.Button(
            quiz_wrap,
            text="🧠  Generate Quiz",
            command=self._generate_quiz,
            font=(FF_B, 9),
            bg="#7C3AED", fg="#FFFFFF",
            relief="flat", bd=0,
            padx=16, pady=9,
            cursor="hand2",
            activebackground="#A78BFA",
            activeforeground="#FFFFFF")
        self.quiz_btn.pack()
        self.quiz_btn.bind("<Enter>", lambda e: self.quiz_btn.configure(bg="#A78BFA"))
        self.quiz_btn.bind("<Leave>", lambda e: self.quiz_btn.configure(bg="#7C3AED"))

        self.attach_lbl = tk.Label(tb, text="",
            font=(FF, 8), fg=C["green"], bg=C["card2"])
        self.attach_lbl.pack(side="left", padx=(6, 0))

        self.spin_lbl = tk.Label(tb, text="",
            font=(FF, 10), fg=C["accent_light"], bg=C["card2"])
        self.spin_lbl.pack(side="left", padx=14)

        # ── Answer Area ───────────────────────────────────────────
        bot = tk.Frame(main, bg=C["bg"])
        bot.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 12))
        bot.rowconfigure(1, weight=1)
        bot.columnconfigure(0, weight=1)

        self.note_lbl = tk.Label(bot, text="",
            font=(FF, 8), fg=C["text2"], bg=C["bg"],
            anchor="w", wraplength=900)
        self.note_lbl.grid(row=0, column=0, sticky="ew", pady=(0, 4))

        self._sec_grid(bot, "💡", "Answer", row=0)

        self.ans_border_frame = tk.Frame(bot, bg=C["border2"], padx=3, pady=0)
        self.ans_border_frame.grid(row=1, column=0, sticky="nsew")

        acard_inner = tk.Frame(self.ans_border_frame, bg=C["card"])
        acard_inner.pack(fill="both", expand=True)

        ans_head = tk.Frame(acard_inner, bg=C["card2"])
        ans_head.pack(fill="x")
        tk.Label(ans_head, text="  💡  AI Response",
                 font=(FF, 8), fg=C["text2"],
                 bg=C["card2"]).pack(side="left", pady=7)
        self.ans_meta = tk.Label(ans_head, text="",
            font=(FF, 7), fg=C["text3"], bg=C["card2"])
        self.ans_meta.pack(side="right", padx=12)

        div3 = tk.Canvas(acard_inner, height=2, bg=C["card"], highlightthickness=0)
        div3.pack(fill="x")
        div3.bind("<Configure>", lambda e: self._draw_div(div3))

        ans_frame = tk.Frame(acard_inner, bg=C["card"])
        ans_frame.pack(fill="both", expand=True)

        self.ans_box = tk.Text(
            ans_frame,
            font=(FF_OCR, 10),
            bg=C["card"], fg=C["text"],
            insertbackground=C["text"],
            relief="flat", bd=0, wrap="word",
            state="disabled",
            padx=20, pady=18,
            spacing1=2, spacing3=3,
            highlightthickness=0)
        self.ans_box.pack(side="left", fill="both", expand=True)

        ans_scroll = ttk.Scrollbar(ans_frame, orient="vertical",
                                   style="Dark.Vertical.TScrollbar",
                                   command=self.ans_box.yview)
        ans_scroll.pack(side="right", fill="y", pady=4)
        self.ans_box.configure(yscrollcommand=ans_scroll.set)

        self.ans_box.tag_configure("h",
            font=(FF_B, 12), foreground=C["accent_light"],
            spacing1=14, spacing3=6, background=C["card2"],
            lmargin1=10, lmargin2=10)
        self.ans_box.tag_configure("hb",
            font=(FF_B, 11), foreground=C["accent_light"])
        self.ans_box.tag_configure("b",
            font=(FF, 11), foreground=C["text"],
            spacing1=2, spacing3=3, lmargin1=10, lmargin2=10)
        self.ans_box.tag_configure("m",
            font=(FF, 11, "italic"), foreground=C["text2"],
            lmargin1=10, lmargin2=10)
        self.ans_box.tag_configure("w",
            font=(FF_B, 11), foreground=C["yellow"],
            lmargin1=10, lmargin2=10)
        self.ans_box.tag_configure("code",
            font=(FF_OCR, 11), foreground="#4ADE80",
            background="#0D1117",
            spacing1=1, spacing3=1,
            lmargin1=24, lmargin2=24)
        self.ans_box.tag_configure("li",
            font=(FF, 11), foreground=C["text"],
            spacing1=3, spacing3=3,
            lmargin1=28, lmargin2=44)
        self.ans_box.tag_configure("placeholder",
            foreground=C["text3"], font=(FF, 11, "italic"))

        self._set_placeholder()

        div4 = tk.Canvas(acard_inner, height=2, bg=C["card"], highlightthickness=0)
        div4.pack(fill="x")
        div4.bind("<Configure>", lambda e: self._draw_div(div4))

        # ── Row 1: Export + Copy ─────────────────────────────────
        ft = tk.Frame(acard_inner, bg=C["card2"], pady=8)
        ft.pack(fill="x", padx=14)
        self._btn(ft, "💾  Export Session",
                  self._export, C["green_dark"],
                  hover=C["green"]).pack(side="left", padx=(0, 10))
        self._btn(ft, "📋  Copy Answer",
                  self._copy, C["border2"],
                  hover=C["accent_dark"]).pack(side="left")
        self.word_lbl = tk.Label(ft, text="",
            font=(FF, 7), fg=C["text3"], bg=C["card2"])
        self.word_lbl.pack(side="right")



    # ─────────────────────────────────────────────────────────────
    def _draw_div(self, canvas):
        """Gradient accent divider line."""
        w = canvas.winfo_width()
        if w < 4:
            return
        canvas.delete("all")
        img = make_gradient_img(w, 2,
                                 hex_to_rgb(C["accent_dark"]),
                                 hex_to_rgb(C["accent"]),
                                 vertical=False)
        ph = ImageTk.PhotoImage(img)
        self._dividers.append(ph)
        canvas.create_image(0, 0, anchor="nw", image=ph)

    # ─────────────────────────────────────────────────────────────
    def _statusbar(self):
        sb = tk.Frame(self, bg=C["card2"], height=30)
        sb.pack(fill="x", side="bottom")
        sb.pack_propagate(False)

        sb_top = tk.Canvas(sb, height=1, bg=C["card2"], highlightthickness=0)
        sb_top.pack(fill="x", side="top")
        sb_top.bind("<Configure>", lambda e: self._draw_div(sb_top))

        self.dot_lbl = tk.Label(sb, text="●",
            font=(FF, 8), fg=C["green"], bg=C["card2"])
        self.dot_lbl.pack(side="left", padx=(12, 4))

        self.status_var = tk.StringVar(
            value="Ready — type your question and click Resolve Doubt")
        tk.Label(sb, textvariable=self.status_var,
                 font=(FF, 8), fg=C["text2"],
                 bg=C["card2"], anchor="w").pack(side="left")

        badge_img = make_rounded_rect(200, 18, 9, C["input"], C["border2"], 1)
        self._badge_ph = ImageTk.PhotoImage(badge_img)
        badge_c = tk.Canvas(sb, width=200, height=18,
                             bg=C["card2"], highlightthickness=0)
        badge_c.pack(side="right", padx=12, pady=6)
        badge_c.create_image(0, 0, anchor="nw", image=self._badge_ph)
        badge_c.create_text(100, 9,
                             text="v5.1  ·  Groq Llama 3.3 70B  ·  Doubt Defuser",
                             font=(FF, 7), fill=C["text3"], anchor="center")

    # ── WIDGET HELPERS ────────────────────────────────────────────
    def _sec(self, p, icon, text):
        f = tk.Frame(p, bg=p["bg"])
        f.pack(fill="x", pady=(0, 7))
        tk.Label(f, text=icon, font=(FF, 9),
                 fg=C["accent"], bg=p["bg"]).pack(side="left")
        tk.Label(f, text=f"  {text}", font=(FF_M, 9),
                 fg=C["text2"], bg=p["bg"]).pack(side="left")
        tk.Frame(f, bg=C["border2"], height=1).pack(
            side="left", fill="x", expand=True, padx=(8, 0))

    def _sec_grid(self, p, icon, text, row):
        f = tk.Frame(p, bg=p["bg"])
        f.grid(row=row, column=0, sticky="ew", pady=(0, 6))
        tk.Label(f, text=icon, font=(FF, 9),
                 fg=C["accent"], bg=p["bg"]).pack(side="left")
        tk.Label(f, text=f"  {text}", font=(FF_M, 9),
                 fg=C["text2"], bg=p["bg"]).pack(side="left")
        tk.Frame(f, bg=C["border2"], height=1).pack(
            side="left", fill="x", expand=True, padx=(8, 0))

    def _card(self, parent):
        outer = tk.Frame(parent, bg=C["border"], padx=1, pady=1)
        outer.pack(fill="x")
        inner = tk.Frame(outer, bg=C["card"], padx=14, pady=12)
        inner.pack(fill="both", expand=True)
        return inner

    def _divider(self, p):
        tk.Frame(p, bg=C["border"], height=1).pack(fill="x", pady=8)

    def _spacer(self, p, h):
        tk.Frame(p, bg=p["bg"], height=h).pack(fill="x")

    def _field(self, p, label, var, values, cmd=None):
        tk.Label(p, text=label, font=(FF, 7, "bold"),
                 fg=C["text2"], bg=C["card"], anchor="w").pack(fill="x", pady=(0, 4))
        cb = ttk.Combobox(p, textvariable=var, values=values,
                          state="readonly", style="CB.TCombobox",
                          font=(FF, 9))
        cb.pack(fill="x")
        if cmd:
            cb.bind("<<ComboboxSelected>>", cmd)
        return cb

    def _pill_btn(self, parent, text, bg, fg):
        # Wider pills that fill the available card width evenly
        w, h, r = 76, 28, 14
        img_n = make_rounded_rect(w, h, r, bg, fg, 1)
        img_h = make_rounded_rect(w, h, r, C["accent_dark"], C["white"], 1)
        ph_n  = ImageTk.PhotoImage(img_n)
        ph_h  = ImageTk.PhotoImage(img_h)
        self._pill_images[text] = (ph_n, ph_h)

        c = tk.Canvas(parent, width=w, height=h,
                       bg=C["card"], highlightthickness=0, cursor="hand2")
        c.pack(side="left", padx=(0, 4))
        c.create_image(0, 0, anchor="nw", image=ph_n, tags="bg")
        c.create_text(w//2, h//2, text=text,
                       font=(FF, 7, "bold"), fill=fg,
                       tags="lbl", anchor="center")

        def enter(e):
            c.delete("bg"); c.create_image(0, 0, anchor="nw", image=ph_h, tags="bg")
            c.itemconfig("lbl", fill=C["white"]); c.tag_lower("bg")
        def leave(e):
            c.delete("bg"); c.create_image(0, 0, anchor="nw", image=ph_n, tags="bg")
            c.itemconfig("lbl", fill=fg); c.tag_lower("bg")
        c.bind("<Enter>",    enter)
        c.bind("<Leave>",    leave)
        c.bind("<Button-1>", lambda e, v=text: self.level_var.set(v))

    def _btn(self, p, text, cmd, color, hover=None, **kw):
        hover = hover or C["accent"]
        b = tk.Button(p, text=text, command=cmd,
                      font=(FF_M, 8), bg=color, fg=C["white"],
                      relief="flat", bd=0, padx=14, pady=7,
                      cursor="hand2",
                      activebackground=hover,
                      activeforeground=C["white"], **kw)
        self._add_hover(b, color, hover)
        return b

    def _add_hover(self, widget, normal_bg, hover_bg):
        widget.bind("<Enter>", lambda e: widget.configure(bg=hover_bg))
        widget.bind("<Leave>", lambda e: widget.configure(bg=normal_bg))

    # ── LOGIC ─────────────────────────────────────────────────────
    def _refresh_topics(self, *_):
        topics = SUBJECT_TOPICS.get(self.subject_var.get(), [])
        new_val = topics[0] if topics else ""
        self.topic_var.set(new_val)
        # Update combobox values — find and reconfigure the topic combobox
        for w in self.winfo_children():
            self._update_topic_combobox(w, topics)

    def _update_topic_combobox(self, widget, topics):
        """Recursively find the topic combobox and update its values."""
        try:
            if (isinstance(widget, ttk.Combobox) and
                    widget.cget("textvariable") == str(self.topic_var)):
                widget.configure(values=topics)
                return
        except Exception:
            pass
        for child in widget.winfo_children():
            self._update_topic_combobox(child, topics)

    def _qin(self, e):
        if self.q_box.get("1.0", "end-1c") == "Type your question here…":
            self.q_box.delete("1.0", "end")
            self.q_box.configure(fg=C["text"])

    def _qout(self, e):
        if not self.q_box.get("1.0", "end-1c").strip():
            self.q_box.insert("1.0", "Type your question here…")
            self.q_box.configure(fg=C["text2"])

    def _update_char_count(self, e=None):
        txt = self.q_box.get("1.0", "end-1c")
        if txt == "Type your question here…":
            self.char_lbl.configure(text="0 chars", fg=C["text3"])
        else:
            n = len(txt)
            self.char_lbl.configure(
                text=f"{n} chars",
                fg=C["yellow"] if n > 300 else C["text3"])

    def _ask(self):
        q = self.q_box.get("1.0", "end-1c").strip()
        if not q or q == "Type your question here…":
            messagebox.showwarning("No Question", "Please type your question first.")
            return
        api_key = self.api_key_var.get().strip()
        if not api_key:
            messagebox.showwarning("No API Key", "Please enter your Groq API key.")
            return

        subject   = self.subject_var.get()
        topic     = self.topic_var.get()
        all_topics = SUBJECT_TOPICS.get(subject, [])
        full_q    = q
        if self.attached_file_text.strip():
            full_q = (q + "\n\n[Attached file: " + self.attached_file_name + "]\n"
                      + self.attached_file_text[:2000])

        self.ask_btn.configure(state="disabled", bg=C["border2"])
        self.status_var.set("🔍  Checking topic relevance…")
        self.dot_lbl.configure(fg=C["yellow"])

        def check_worker():
            result = check_question_relevance(
                q, subject, topic, all_topics, self.syllabus_text, api_key)
            self.after(0, lambda: self._after_relevance_check(
                q, full_q, subject, topic, api_key, result))

        threading.Thread(target=check_worker, daemon=True).start()

    def _after_relevance_check(self, q, full_q, subject, topic, api_key, result):
        """Called on main thread after relevance check finishes."""
        status = result["status"]
        if status == "ok":
            self._run_ai(q, full_q, subject, topic, api_key, False)
        elif status == "topic_mismatch":
            self.ask_btn.configure(state="normal", bg=C["accent"])
            self.status_var.set("⚠️  Topic mismatch detected.")
            self._topic_mismatch_dialog(q, full_q, subject, topic,
                                        result["suggested_topic"], api_key)
        else:  # oos
            self.ask_btn.configure(state="normal", bg=C["accent"])
            self.status_var.set("⚠️  Question appears out of syllabus.")
            self._oos_dialog(q, full_q, subject, topic, api_key)

    def _topic_mismatch_dialog(self, q, full_q, subject, current_topic,
                                suggested_topic, api_key):
        """Windows-style dialog for topic mismatch — suggests correct topic."""
        d = tk.Toplevel(self)
        d.title("Doubt Defuser")
        d.resizable(False, False)
        d.grab_set()
        d.lift()
        d.focus_force()
        d.configure(bg="#F0F0F0")

        # Icon + message row
        row = tk.Frame(d, bg="#F0F0F0", padx=18, pady=18)
        row.pack(fill="x")

        tk.Label(row, text="⚠", font=("Segoe UI", 36, "bold"),
                 bg="#F0F0F0", fg="#E8A000").pack(side="left",
                 anchor="n", padx=(0, 14))

        msg_f = tk.Frame(row, bg="#F0F0F0")
        msg_f.pack(side="left", fill="x", expand=True)

        tk.Label(msg_f, text="Topic Mismatch Detected",
                 font=("Segoe UI", 10, "bold"),
                 bg="#F0F0F0", fg="#1A1A1A").pack(anchor="w")

        short_q = (q[:80] + "...") if len(q) > 80 else q
        body = (
            "Your question does not match the selected topic.\n\n"
            "  Your Topic         :  " + current_topic + "\n"
            "  Correct Topic   :  " + (suggested_topic or "Unknown") + "\n\n"
            "  Question  :  \"" + short_q + "\"\n\n"
            "Switch to the correct topic and continue?"
        )
        tk.Label(msg_f, text=body,
                 font=("Segoe UI", 9),
                 bg="#F0F0F0", fg="#333333",
                 justify="left", anchor="w",
                 wraplength=390).pack(anchor="w", pady=(6, 0))

        # Separator
        tk.Frame(d, bg="#C0C0C0", height=1).pack(fill="x")

        # Button bar
        bar = tk.Frame(d, bg="#F0F0F0", pady=10, padx=12)
        bar.pack(fill="x")

        def on_cancel():
            d.destroy()
            self.ask_btn.configure(state="normal", bg=C["accent"])
            self.status_var.set("Cancelled.")
            self.dot_lbl.configure(fg=C["red"])

        def on_switch():
            """Switch topic and run AI."""
            if suggested_topic:
                self.topic_var.set(suggested_topic)
                self.status_var.set(
                    f"✅  Switched topic to: {suggested_topic}")
            d.destroy()
            self._run_ai(q, full_q, subject,
                         suggested_topic or current_topic, api_key, False)

        cancel_btn = tk.Button(bar, text="Cancel", command=on_cancel,
                               font=("Segoe UI", 9), width=8,
                               relief="raised", bd=1, pady=4,
                               bg="#E1E1E1", fg="#1A1A1A",
                               activebackground="#FFD0D0", cursor="hand2")
        cancel_btn.pack(side="right", padx=(4, 0))

        switch_btn = tk.Button(bar,
                               text="Yes, Switch Topic",
                               command=on_switch,
                               font=("Segoe UI", 9, "bold"), width=15,
                               relief="raised", bd=1, pady=4,
                               bg="#E1E1E1", fg="#0078D7",
                               activebackground="#CCE4F7", cursor="hand2")
        switch_btn.pack(side="right", padx=(4, 0))

        # Enter = Switch, Escape = Cancel
        d.bind("<Return>",  lambda e: on_switch())
        d.bind("<Escape>",  lambda e: on_cancel())

        d.update_idletasks()
        w = d.winfo_reqwidth()
        h = d.winfo_reqheight()
        x = (d.winfo_screenwidth()  - w) // 2
        y = (d.winfo_screenheight() - h) // 2
        d.geometry(f"{w}x{h}+{x}+{y}")

    def _oos_dialog(self, q, full_q, subject, topic, api_key):
        """Windows-style caution dialog when question is fully out of syllabus."""
        d = tk.Toplevel(self)
        d.title("Doubt Defuser")
        d.resizable(False, False)
        d.grab_set()
        d.lift()
        d.focus_force()
        d.configure(bg="#F0F0F0")

        row = tk.Frame(d, bg="#F0F0F0", padx=18, pady=18)
        row.pack(fill="x")

        tk.Label(row, text="⚠", font=("Segoe UI", 36, "bold"),
                 bg="#F0F0F0", fg="#E8A000").pack(side="left",
                 anchor="n", padx=(0, 14))

        msg_f = tk.Frame(row, bg="#F0F0F0")
        msg_f.pack(side="left", fill="x", expand=True)

        tk.Label(msg_f, text="Out of Syllabus Detected",
                 font=("Segoe UI", 10, "bold"),
                 bg="#F0F0F0", fg="#1A1A1A").pack(anchor="w")

        short_q = (q[:90] + "...") if len(q) > 90 else q
        has_syl = bool(self.syllabus_text.strip())
        syl_note = "your uploaded syllabus PDF" if has_syl else "the subject topics"
        body = (
            "Your question was not found in " + syl_note + ".\n\n"
            "  Subject  :  " + subject + "\n"
            "  Topic      :  " + topic + "\n\n"
            "  Question :  \"" + short_q + "\"\n\n"
            "Do you still want to run this question?"
        )
        tk.Label(msg_f, text=body,
                 font=("Segoe UI", 9),
                 bg="#F0F0F0", fg="#333333",
                 justify="left", anchor="w",
                 wraplength=380).pack(anchor="w", pady=(6, 0))

        tk.Frame(d, bg="#C0C0C0", height=1).pack(fill="x")

        bar = tk.Frame(d, bg="#F0F0F0", pady=10, padx=12)
        bar.pack(fill="x")

        def on_no():
            d.destroy()
            self.ask_btn.configure(state="normal", bg=C["accent"])
            self.status_var.set("Cancelled.")
            self.dot_lbl.configure(fg=C["red"])

        def on_yes():
            d.destroy()
            self._run_ai(q, full_q, subject, topic, api_key, True)

        no_btn = tk.Button(bar, text="No", command=on_no,
                           font=("Segoe UI", 9), width=8,
                           relief="raised", bd=1, pady=4,
                           bg="#E1E1E1", fg="#1A1A1A",
                           activebackground="#FFD0D0", cursor="hand2")
        no_btn.pack(side="right", padx=(4, 0))

        yes_btn = tk.Button(bar, text="Yes", command=on_yes,
                            font=("Segoe UI", 9, "bold"), width=8,
                            relief="raised", bd=1, pady=4,
                            bg="#E1E1E1", fg="#1A1A1A",
                            activebackground="#CCE4F7", cursor="hand2")
        yes_btn.pack(side="right", padx=(4, 0))

        d.bind("<Return>",  lambda e: on_yes())
        d.bind("<Escape>",  lambda e: on_no())

        d.update_idletasks()
        w = d.winfo_reqwidth()
        h = d.winfo_reqheight()
        x = (d.winfo_screenwidth()  - w) // 2
        y = (d.winfo_screenheight() - h) // 2
        d.geometry(f"{w}x{h}+{x}+{y}")

    def _run_ai(self, q, full_q, subject, topic, api_key, out_of_syllabus=False):
        """Actually run the AI prompt after all pre-checks pass."""
        self.ask_btn.configure(state="disabled", bg=C["border2"])
        self._set_ans("")
        self.note_lbl.configure(text="")
        self.ans_meta.configure(text="")
        self.word_lbl.configure(text="")
        self.status_var.set("⏳  AI is thinking…")
        self.dot_lbl.configure(fg=C["yellow"])
        self.ans_border_frame.configure(bg=C["border2"])
        self._spin_start()

        def worker():
            result = get_ai_answer(
                full_q, subject, topic,
                self.level_var.get(), self.syllabus_text,
                api_key, out_of_syllabus=out_of_syllabus)
            self.after(0, lambda: self._show(q, result))

        threading.Thread(target=worker, daemon=True).start()

    # ── Smart line classifier ─────────────────────────────────────
    @staticmethod
    def _is_tree_or_code(line: str) -> bool:
        """Detect ASCII tree / diagram lines (outside fenced blocks)."""
        s = line.rstrip()
        if not s:
            return False
        tree_chars = set(r"/\|─└├┘┐┌┬┤┼")
        if any(c in tree_chars for c in s):
            return True
        # 4-space indented (classic code indent)
        if s.startswith("    ") and len(s) > 4:
            return True
        return False

    def _show(self, question, r):
        self._spin_stop()
        self.ask_btn.configure(state="normal", bg=C["accent"])

        self.note_lbl.configure(text=r["note"])
        has_error = r["note"].startswith("❌")
        self.ans_border_frame.configure(
            bg=C["red"] if has_error else C["green"])
        self.dot_lbl.configure(fg=C["green"])

        self.ans_box.configure(state="normal")
        self.ans_box.delete("1.0", "end")
        word_count  = 0
        in_fence    = False   # inside ```...``` block

        for raw_line in r["answer"].split("\n"):
            s = raw_line.strip()

            # ── backtick fence toggle ─────────────────────────────
            if s.startswith("```"):
                in_fence = not in_fence
                if in_fence:
                    lang = s[3:].strip() or "code"
                    self.ans_box.insert("end",
                        f"  ◆ {lang.upper()}  \n", "h")
                else:
                    self.ans_box.insert("end", "\n")
                continue

            if in_fence:
                self.ans_box.insert("end",
                    raw_line.rstrip("\n") + "\n", "code")
                word_count += len(s.split())
                continue

            # ── auto-detect tree / diagram outside fence ──────────
            if self._is_tree_or_code(raw_line):
                self.ans_box.insert("end",
                    raw_line.rstrip("\n") + "\n", "code")
                word_count += len(s.split())
                continue

            # ── blank line ────────────────────────────────────────
            if s == "":
                self.ans_box.insert("end", "\n")
                continue

            # ── whole-line heading  **Heading:** ──────────────────
            if s.startswith("**") and s.endswith("**") and s.count("**") == 2:
                label = s.strip("*").strip()
                self.ans_box.insert("end", f"  {label}\n", "h")
                word_count += len(label.split())
                continue

            # ── numbered list  1. / 2. ────────────────────────────
            if len(s) > 2 and s[0].isdigit() and s[1] in ".)":
                self.ans_box.insert("end", s + "\n", "li")
                word_count += len(s.split())
                continue

            # ── bullet list  -  or  •  or  * ─────────────────────
            if s.startswith(("- ", "• ", "* ")):
                self.ans_box.insert("end", "  • " + s[2:] + "\n", "li")
                word_count += len(s.split())
                continue

            # ── mixed inline bold  **word** ───────────────────────
            if "**" in s:
                parts = s.split("**")
                for i, p in enumerate(parts):
                    self.ans_box.insert("end", p,
                        "hb" if i % 2 == 1 else "b")
                self.ans_box.insert("end", "\n")
                word_count += len(s.split())
                continue

            # ── error / warning ───────────────────────────────────
            if s.lower().startswith("error") or "❌" in s:
                self.ans_box.insert("end", s + "\n", "w")
                word_count += len(s.split())
                continue

            # ── normal body ───────────────────────────────────────
            self.ans_box.insert("end", s + "\n", "b")
            word_count += len(s.split())

        self.ans_box.configure(state="disabled")

        self.ans_meta.configure(
            text=f"{word_count} words  ·  {r['timestamp']}", fg=C["text3"])
        self.word_lbl.configure(
            text=f"~{word_count} words in response", fg=C["text3"])

        self.history.append(r)
        short = question[:44] + ("…" if len(question) > 44 else "")
        self.hist_lb.insert("end", f"  {r['timestamp']}   {short}")
        self.status_var.set(
            f"✅  {r['subject']}  →  {r['topic']}  │  {r['timestamp']}")
        # Enable quiz generator now that we have an answer
        self._last_answer = r["answer"]
        self.quiz_btn.configure(bg="#7C3AED", fg=C["white"])
        self._add_hover(self.quiz_btn, "#7C3AED", "#A78BFA")

    def _load_hist(self, e):
        sel = self.hist_lb.curselection()
        if not sel or sel[0] >= len(self.history):
            return
        item = self.history[sel[0]]
        self.subject_var.set(item["subject"])
        self.topic_var.set(item["topic"])
        self.level_var.set(item["level"])
        self.note_lbl.configure(text=item["note"])
        self.q_box.delete("1.0", "end")
        self.q_box.insert("1.0", item["question"])
        self.q_box.configure(fg=C["text"])
        self.ans_box.configure(state="normal")
        self.ans_box.delete("1.0", "end")
        self.ans_box.insert("end", item["answer"])
        self.ans_box.configure(state="disabled")

    def _clear_hist(self):
        self.history.clear()
        self.hist_lb.delete(0, "end")
        self.status_var.set("History cleared.")

    def _clear_all(self):
        self._set_ans("")
        self._set_placeholder()
        self.note_lbl.configure(text="")
        self.ans_meta.configure(text="")
        self.word_lbl.configure(text="")
        self.ans_border_frame.configure(bg=C["border2"])
        self.q_box.delete("1.0", "end")
        self._qout(None)
        self._update_char_count()
        self.attached_file_text = ""
        self.attached_file_name = ""
        self.attach_lbl.configure(text="")
        self._add_hover(self.attach_btn, C["green_dark"], C["green"])
        self.attach_btn.configure(bg=C["green_dark"])

    def _set_placeholder(self):
        self.ans_box.configure(state="normal")
        self.ans_box.delete("1.0", "end")
        self.ans_box.insert("1.0",
            "\n\n\n        Ask a question to see the AI response here…",
            "placeholder")
        self.ans_box.configure(state="disabled")

    # ── ATTACH FILE ───────────────────────────────────────────────
    def _attach_file(self):
        path = filedialog.askopenfilename(
            title="Attach Image or Document",
            filetypes=[
                ("All supported", "*.png *.jpg *.jpeg *.bmp *.pdf *.txt *.docx"),
                ("Images",        "*.png *.jpg *.jpeg *.bmp"),
                ("PDF",           "*.pdf"),
                ("Text",          "*.txt"),
                ("Word",          "*.docx"),
            ])
        if not path:
            return
        try:
            ext  = os.path.splitext(path)[1].lower()
            name = os.path.basename(path)
            if ext in (".png", ".jpg", ".jpeg", ".bmp"):
                extracted = self._ocr_image(path)
            elif ext == ".pdf":
                extracted = self._read_pdf(path)
            elif ext == ".docx":
                extracted = self._read_docx(path)
            else:
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    extracted = f.read()
            if not extracted.strip():
                messagebox.showwarning("Empty",
                    "Could not extract text from this file.")
                return
            self.attached_file_text = extracted
            self.attached_file_name = name
            short = name[:26] + ("…" if len(name) > 26 else "")
            self.attach_lbl.configure(text=f"📎 {short}")
            self.attach_btn.configure(bg=C["accent_dark"])
            self.status_var.set(
                f"✅  Attached: {name} — AI will use this in your answer!")
        except Exception as ex:
            messagebox.showerror("Attach Error", str(ex))

    def _ocr_image(self, path: str) -> str:
        try:
            import base64
            with open(path, "rb") as f:
                img_data = base64.b64encode(f.read()).decode("utf-8")
            ext  = os.path.splitext(path)[1].lower().replace(".", "")
            mime = {"jpg": "image/jpeg", "jpeg": "image/jpeg",
                    "png": "image/png", "bmp": "image/bmp"}.get(ext, "image/png")
            payload = json.dumps({
                "model": "meta-llama/llama-4-scout-17b-16e-instruct",
                "messages": [{"role": "user", "content": [
                    {"type": "image_url",
                     "image_url": {"url": f"data:{mime};base64,{img_data}"}},
                    {"type": "text",
                     "text": "Extract ALL text from this image exactly as written."}
                ]}],
                "max_tokens": 1024,
            })
            headers = {"Content-Type": "application/json",
                       "Authorization": f"Bearer {self.api_key_var.get().strip()}",
                       "User-Agent": "Mozilla/5.0"}
            import requests as rl
            r = rl.post("https://api.groq.com/openai/v1/chat/completions",
                        data=payload.encode(), headers=headers, timeout=30)
            if r.status_code == 200:
                return r.json()["choices"][0]["message"]["content"]
            raise Exception(f"Vision API {r.status_code}: {r.text[:100]}")
        except ImportError:
            try:
                import importlib
                PIL_img = importlib.import_module("PIL.Image")
                pytesseract = importlib.import_module("pytesseract")
                return pytesseract.image_to_string(PIL_img.open(path))
            except Exception:
                return "[Image attached — describe your doubt in text above]"

    # ── SYLLABUS ──────────────────────────────────────────────────
    def _upload_syllabus(self):
        path = filedialog.askopenfilename(
            title="Select Any Study Material",
            filetypes=[
                ("All supported files",
                 "*.txt *.pdf *.docx *.doc *.xlsx *.xls *.pptx *.ppt "
                 "*.csv *.md *.html *.htm *.rtf *.odt *.ods *.odp"),
                ("Text files",         "*.txt *.md *.csv *.rtf"),
                ("PDF",                "*.pdf"),
                ("Word documents",     "*.docx *.doc *.odt"),
                ("Excel spreadsheets", "*.xlsx *.xls *.ods"),
                ("PowerPoint slides",  "*.pptx *.ppt *.odp"),
                ("Web / Markup",       "*.html *.htm"),
                ("All files",          "*.*"),
            ])
        if not path:
            return
        try:
            ext  = os.path.splitext(path)[1].lower()
            name = os.path.basename(path)
            self.status_var.set(f"📂  Reading {name}…")
            self.update()
            if ext == ".pdf":
                self.syllabus_text = self._read_pdf(path)
            elif ext in (".docx", ".doc", ".odt"):
                self.syllabus_text = self._read_docx(path)
            elif ext in (".xlsx", ".xls", ".ods"):
                self.syllabus_text = self._read_excel(path)
            elif ext in (".pptx", ".ppt", ".odp"):
                self.syllabus_text = self._read_pptx(path)
            elif ext == ".csv":
                self.syllabus_text = self._read_csv(path)
            elif ext in (".html", ".htm"):
                self.syllabus_text = self._read_html(path)
            else:
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    self.syllabus_text = f.read()
            if not self.syllabus_text.strip():
                messagebox.showwarning("Empty",
                    f"No readable text found in:\n{name}")
                return
            self._update_syl_ui(name)
            self._detect_topics_async()
        except Exception as ex:
            messagebox.showerror("Upload Error", str(ex))

    # ── FILE READERS ──────────────────────────────────────────────
    def _read_pdf(self, path):
        import importlib
        def _try(name):
            try:
                m = importlib.import_module(name)
                pages = []
                with open(path, "rb") as f:
                    for pg in m.PdfReader(f).pages:
                        t = pg.extract_text()
                        if t: pages.append(t)
                return "\n".join(pages) if pages else None
            except ImportError:
                return None
        for mod in ("PyPDF2", "pypdf"):
            r = _try(mod)
            if r: return r
        self.status_var.set("Installing PDF reader…")
        self.update()
        subprocess.check_call([sys.executable, "-m", "pip",
                               "install", "PyPDF2", "-q"])
        return _try("PyPDF2") or ""

    def _read_docx(self, path):
        import importlib
        try:
            docx = importlib.import_module("docx")
        except ImportError:
            self.status_var.set("Installing python-docx…")
            self.update()
            subprocess.check_call([sys.executable, "-m", "pip",
                                   "install", "python-docx", "-q"])
            docx = importlib.import_module("docx")
        doc = docx.Document(path)
        return "\n".join(p.text for p in doc.paragraphs if p.text.strip())

    def _read_excel(self, path: str) -> str:
        try:
            import importlib
            openpyxl = importlib.import_module("openpyxl")
            wb = openpyxl.load_workbook(path, data_only=True)
            lines = []
            for sheet in wb.worksheets:
                lines.append(f"[Sheet: {sheet.title}]")
                for row in sheet.iter_rows(values_only=True):
                    row_text = "  |  ".join(str(c) for c in row if c is not None)
                    if row_text.strip():
                        lines.append(row_text)
            return "\n".join(lines)
        except ImportError:
            self.status_var.set("Installing openpyxl…")
            self.update()
            subprocess.check_call([sys.executable, "-m", "pip",
                                   "install", "openpyxl", "-q"])
            return self._read_excel(path)

    def _read_pptx(self, path: str) -> str:
        try:
            import importlib
            prs_mod = importlib.import_module("pptx")
            prs = prs_mod.Presentation(path)
            lines = []
            for i, slide in enumerate(prs.slides, 1):
                lines.append(f"[Slide {i}]")
                for shape in slide.shapes:
                    if hasattr(shape, "text") and shape.text.strip():
                        lines.append(shape.text.strip())
            return "\n".join(lines)
        except ImportError:
            self.status_var.set("Installing python-pptx…")
            self.update()
            subprocess.check_call([sys.executable, "-m", "pip",
                                   "install", "python-pptx", "-q"])
            return self._read_pptx(path)

    def _read_csv(self, path: str) -> str:
        import csv
        lines = []
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            for row in csv.reader(f):
                row_text = "  |  ".join(cell for cell in row if cell.strip())
                if row_text.strip():
                    lines.append(row_text)
        return "\n".join(lines)

    def _read_html(self, path: str) -> str:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            raw = f.read()
        try:
            import importlib
            bs4 = importlib.import_module("bs4")
            return bs4.BeautifulSoup(raw, "html.parser").get_text(separator="\n")
        except ImportError:
            import re
            clean = re.sub(r"<[^>]+>", " ", raw)
            return re.sub(r"\s{2,}", "\n", clean).strip()

    def _subject_mismatch_dialog(self, current_subject, detected_subject, topics):
        """Auto-switches subject immediately without any dialog."""
        self.subject_var.set(detected_subject)
        self._refresh_topics()
        first_topic = topics[0] if topics else SUBJECT_TOPICS.get(detected_subject, [""])[0]
        self.topic_var.set(first_topic)
        words = len(self.syllabus_text.split())
        self.syl_status.configure(
            text=f"✅  Loaded ({words:,} words) — {len(topics)} topics found",
            fg=C["green"])
        self.status_var.set(f"✅  Auto-switched to: {detected_subject}")
        self._show_detected_topics_window(topics)

    def _update_syl_ui(self, name):
        words = len(self.syllabus_text.split())
        self.syl_status.configure(
            text=f"✅  {name}  ({words:,} words)", fg=C["green"])
        self.syl_prev.configure(state="normal")
        self.syl_prev.delete("1.0", "end")
        self.syl_prev.insert("1.0", self.syllabus_text[:400] +
            ("…" if len(self.syllabus_text) > 400 else ""))
        self.syl_prev.configure(state="disabled")

    def _detect_topics_async(self):
        self.status_var.set("🔍  AI is scanning your syllabus for topics…")
        self.syl_status.configure(text="🔍  Detecting topics…", fg=C["yellow"])

        subjects_list = ", ".join(SUBJECT_TOPICS.keys())

        def worker():
            api_key = self.api_key_var.get().strip()
            try:
                # ── Step A: Extract topics ──────────────────────────
                topic_prompt = (
                    "You are a syllabus analyzer. Extract ALL chapter names, "
                    "topic names, and unit titles.\n\n"
                    "Return ONLY a JSON array of strings, nothing else.\n"
                    f"DOCUMENT:\n{self.syllabus_text[:4000]}"
                )
                raw   = call_groq(api_key, topic_prompt).strip()
                start = raw.find("["); end = raw.rfind("]") + 1
                topics = json.loads(raw[start:end]) if start != -1 and end > start else []

                # ── Step B: Detect which subject this syllabus belongs to ──
                subject_prompt = (
                    "You are a subject classifier for a college syllabus.\n"
                    "Given the syllabus text below, pick the SINGLE best matching subject.\n"
                    "Available subjects:\n" + subjects_list + "\n\n"
                    "Reply with ONLY the exact subject name from the list above, nothing else.\n"
                    f"SYLLABUS:\n{self.syllabus_text[:2000]}"
                )
                detected_subject = call_groq(api_key, subject_prompt).strip()

                # Clean up — ensure it exactly matches one of our subjects
                matched_subject = None
                for s in SUBJECT_TOPICS.keys():
                    if s.lower() in detected_subject.lower() or detected_subject.lower() in s.lower():
                        matched_subject = s
                        break

                self.after(0, lambda: self._show_detected_topics(
                    topics, detected_subject=matched_subject))

            except Exception as ex:
                self.after(0, lambda: self._show_detected_topics([], error=str(ex)))

        threading.Thread(target=worker, daemon=True).start()

    def _show_detected_topics(self, topics: list, error: str = "",
                               detected_subject: str = None):
        words = len(self.syllabus_text.split())
        if error or not topics:
            self.syl_status.configure(
                text=f"✅  Loaded ({words:,} words) — topic scan failed",
                fg=C["yellow"])
            self.status_var.set("⚠️  Could not detect topics automatically.")
            return

        self.syl_status.configure(
            text=f"✅  Loaded ({words:,} words) — {len(topics)} topics found",
            fg=C["green"])
        self.status_var.set(
            f"✅  Syllabus scanned — {len(topics)} topics detected by AI!")

        # ── Auto-switch subject if mismatch detected ───────────────
        current_subject = self.subject_var.get()
        if (detected_subject
                and detected_subject != current_subject
                and detected_subject in SUBJECT_TOPICS):
            self._subject_mismatch_dialog(
                current_subject, detected_subject, topics)
            return

        self._show_detected_topics_window(topics)

    def _show_detected_topics_window(self, topics: list):
        """Open the topics chip window (shared by normal flow and auto-switch flow)."""
        win = tk.Toplevel(self)
        win.title("📚 Topics Detected in Syllabus")
        win.geometry("680x540")
        win.configure(bg=C["card"])
        win.grab_set()
        win.resizable(True, True)

        pop_hdr = GradientHeader(win, h=56,
                                  color1=C["header_top"],
                                  color2=C["header_bot"],
                                  bg=C["card"])
        pop_hdr.pack(fill="x")
        hf = tk.Frame(pop_hdr, bg=C["header_top"])
        hf.place(x=18, rely=0.5, anchor="w")
        tk.Label(hf, text="📚  Topics Found in Your Syllabus",
                 font=(FF_B, 13), bg=C["header_top"],
                 fg=C["white"]).pack(side="left")

        badge_f = tk.Frame(pop_hdr, bg=C["accent"], padx=10, pady=3)
        badge_f.place(relx=1.0, rely=0.5, anchor="e", x=-18)
        tk.Label(badge_f, text=f"{len(topics)} topics",
                 font=(FF_B, 8), bg=C["accent"], fg=C["white"]).pack()

        tk.Label(win,
                 text="  Click any topic chip to set it as your current topic.",
                 font=(FF, 9), fg=C["text2"], bg=C["card"]
                 ).pack(padx=18, pady=(12, 4), anchor="w")
        tk.Frame(win, bg=C["border"], height=1).pack(fill="x", padx=18)

        canvas  = tk.Canvas(win, bg=C["card"], highlightthickness=0)
        scrollb = ttk.Scrollbar(win, orient="vertical",
                                style="Dark.Vertical.TScrollbar",
                                command=canvas.yview)
        canvas.configure(yscrollcommand=scrollb.set)
        scrollb.pack(side="right", fill="y", padx=(0, 6), pady=8)
        canvas.pack(fill="both", expand=True, padx=18, pady=8)

        chip_frame  = tk.Frame(canvas, bg=C["card"])
        canvas_win  = canvas.create_window((0, 0), window=chip_frame, anchor="nw")
        canvas.bind("<Configure>",
                    lambda e: canvas.itemconfig(canvas_win, width=e.width))
        chip_frame.bind("<Configure>",
                        lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        chip_imgs = {}
        chip_colors = [
            ("#1E3A5F", "#60A5FA"), ("#064E3B", "#34D399"),
            ("#3B1F5E", "#A78BFA"), ("#78350F", "#FBBF24"),
            ("#7F1D1D", "#F87171"),
        ]

        def make_chip(parent, text, idx):
            bg, fg = chip_colors[idx % len(chip_colors)]
            cw, ch, cr = 182, 40, 10
            img_n = make_rounded_rect(cw, ch, cr, bg,          fg,         1)
            img_h = make_rounded_rect(cw, ch, cr, C["accent"], C["white"], 1)
            ph_n  = ImageTk.PhotoImage(img_n)
            ph_h  = ImageTk.PhotoImage(img_h)
            chip_imgs[f"{idx}n"] = ph_n
            chip_imgs[f"{idx}h"] = ph_h

            cv = tk.Canvas(parent, width=cw, height=ch,
                            bg=C["card"], highlightthickness=0, cursor="hand2")
            cv.create_image(0, 0, anchor="nw", image=ph_n, tags="bg")
            cv.create_text(cw//2, ch//2, text=text,
                            font=(FF_M, 8), fill=fg,
                            tags="lbl", anchor="center", width=cw-16)

            def on_enter(e, v=cv, h=ph_h, n=ph_n):
                v.delete("bg"); v.create_image(0,0,anchor="nw",image=h,tags="bg")
                v.itemconfig("lbl", fill=C["white"]); v.tag_lower("bg")
            def on_leave(e, v=cv, h=ph_h, n=ph_n, f=fg):
                v.delete("bg"); v.create_image(0,0,anchor="nw",image=n,tags="bg")
                v.itemconfig("lbl", fill=f); v.tag_lower("bg")
            def on_click(e, t=text):
                self.topic_var.set(t)
                self.status_var.set(f"✅  Topic set to: '{t}' — now ask your doubt!")
                win.after(200, win.destroy)

            cv.bind("<Enter>",    on_enter)
            cv.bind("<Leave>",    on_leave)
            cv.bind("<Button-1>", on_click)
            return cv

        cols = 3
        for i, topic in enumerate(topics):
            row_, col_ = divmod(i, cols)
            chip = make_chip(chip_frame, topic, i)
            chip.grid(row=row_, column=col_, padx=6, pady=5, sticky="ew")
        for ci in range(cols):
            chip_frame.columnconfigure(ci, weight=1)

        tk.Frame(win, bg=C["border"], height=1).pack(fill="x", padx=18)
        ft = tk.Frame(win, bg=C["card"])
        ft.pack(fill="x", padx=18, pady=10)
        tk.Label(ft,
                 text="💡  Topics extracted from your syllabus by AI.",
                 font=(FF, 8), fg=C["text3"], bg=C["card"]
                 ).pack(side="left")
        self._btn(ft, "✖  Close", win.destroy,
                  C["border2"], hover="#7F1D1D").pack(side="right")


    # ── QUIZ ENGINE ───────────────────────────────────────────────
    def _generate_quiz(self):
        if not self._last_answer.strip():
            messagebox.showinfo("No Answer", "Ask a question first to generate a quiz.")
            return
        self.quiz_btn.configure(text="⏳  Generating…", bg=C["border2"])
        self.status_var.set("🧠  Generating quiz questions from this explanation…")

        answer_snapshot = self._last_answer

        def worker():
            prompt = (
                "You are an expert quiz generator. Based on the explanation below, "
                "generate a quiz in STRICT JSON format.\n\n"
                "Return ONLY valid JSON — no extra text, no markdown fences.\n\n"
                "JSON structure:\n"
                "{\n"
                '  "mcqs": [\n'
                '    {"q": "Question text", "options": ["A) ...", "B) ...", "C) ...", "D) ..."], "answer": "A"}\n'
                "  ],\n"
                '  "descriptive": [\n'
                '    {"q": "Question text", "answer": "Model answer"}\n'
                "  ]\n"
                "}\n\n"
                "Rules:\n"
                "- Generate exactly 5 MCQs and 2 descriptive questions\n"
                "- MCQ answer must be just the letter: A, B, C, or D\n"
                "- Make questions test real understanding, not just recall\n\n"
                f"EXPLANATION:\n{answer_snapshot[:3000]}"
            )
            try:
                raw  = call_groq(self.api_key_var.get().strip(), prompt).strip()
                # Strip any accidental markdown fences
                if raw.startswith("```"):
                    raw = raw.split("```")[1]
                    if raw.startswith("json"):
                        raw = raw[4:]
                data = json.loads(raw.strip())
                self.after(0, lambda: self._open_quiz_window(data))
            except Exception as ex:
                self.after(0, lambda: self._quiz_error(str(ex)))

        threading.Thread(target=worker, daemon=True).start()

    def _quiz_error(self, err):
        self.quiz_btn.configure(text="🧠  Generate Quiz", bg="#7C3AED")
        self.status_var.set(f"❌  Quiz generation failed: {err[:80]}")

    def _open_quiz_window(self, data):
        self.quiz_btn.configure(text="🧠  Generate Quiz", bg="#7C3AED")
        self.status_var.set("✅  Quiz ready! Good luck 🎯")
        QuizWindow(self, data)


    # ── EXPORT / COPY ─────────────────────────────────────────────
    def _export(self):
        if not self.history:
            messagebox.showinfo("Empty", "No session history yet.")
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON", "*.json")],
            initialfile=f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        if not path:
            return
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.history, f, indent=2)
        messagebox.showinfo("Saved", f"Session saved to:\n{path}")

    def _copy(self):
        content = self.ans_box.get("1.0", "end-1c")
        if content.strip():
            self.clipboard_clear()
            self.clipboard_append(content)
            self.status_var.set("✅  Answer copied to clipboard.")
        else:
            self.status_var.set("⚠️  Nothing to copy yet.")

    # ── SPINNER ───────────────────────────────────────────────────
    def _spin_start(self):
        self._spinning = True
        frames = ["⠋","⠙","⠹","⠸","⠼","⠴","⠦","⠧","⠇","⠏"]
        self._si = 0
        def spin():
            if self._spinning:
                self.spin_lbl.configure(
                    text=f"{frames[self._si % len(frames)]}  AI thinking…")
                self._si += 1
                self.after(90, spin)
            else:
                self.spin_lbl.configure(text="")
        spin()

    def _spin_stop(self):
        self._spinning = False

    def _set_ans(self, text, muted=False):
        self.ans_box.configure(state="normal")
        self.ans_box.delete("1.0", "end")
        if text:
            self.ans_box.insert("1.0", text, "m" if muted else "b")
        self.ans_box.configure(state="disabled")



# ═════════════════════════════════════════════════════════════════
#  QUIZ WINDOW
# ═════════════════════════════════════════════════════════════════
class QuizWindow(tk.Toplevel):
    """Full-featured interactive quiz window with MCQ + descriptive."""

    def __init__(self, parent, data: dict):
        super().__init__(parent)
        self.title("🧠 Practice Quiz")
        self.geometry("820x780")
        self.minsize(700, 600)
        self.configure(bg=C["bg"])
        self.resizable(True, True)

        self.mcqs        = data.get("mcqs", [])
        self.descriptive = data.get("descriptive", [])
        self.score       = 0
        self.total_mcq   = len(self.mcqs)
        self.answered    = 0          # MCQs answered
        self.mcq_vars    = []         # StringVar per MCQ
        self.mcq_frames  = []         # frame refs
        self.desc_shown  = []         # booleans per descriptive

        self._build_ui()

    # ─────────────────────────────────────────────────────────────
    def _build_ui(self):
        # ── Gradient header ───────────────────────────────────────
        hdr = GradientHeader(self, h=64,
                              color1=C["header_top"],
                              color2="#1A0A2E",
                              bg=C["bg"])
        hdr.pack(fill="x")

        hf = tk.Frame(hdr, bg=C["header_top"])
        hf.place(x=18, rely=0.5, anchor="w")
        tk.Label(hf, text="🧠  Practice Quiz",
                 font=(FF_B, 15), bg=C["header_top"],
                 fg=C["white"]).pack(side="left")
        tk.Label(hf, text=f"   {self.total_mcq} MCQ  +  {len(self.descriptive)} Descriptive",
                 font=(FF, 9), bg=C["header_top"],
                 fg=C["text2"]).pack(side="left")

        # Score badge — top right
        score_f = tk.Frame(hdr, bg="#3B1F5E", padx=14, pady=6)
        score_f.place(relx=1.0, rely=0.5, anchor="e", x=-18)
        tk.Label(score_f, text="Score", font=(FF, 7),
                 bg="#3B1F5E", fg=C["text2"]).pack()
        self.score_lbl = tk.Label(score_f,
            text=f"0 / {self.total_mcq}",
            font=(FF_B, 13), bg="#3B1F5E", fg="#A78BFA")
        self.score_lbl.pack()

        # ── Scrollable body ───────────────────────────────────────
        sc = tk.Canvas(self, bg=C["bg"], highlightthickness=0)
        sb = ttk.Scrollbar(self, orient="vertical",
                           style="Dark.Vertical.TScrollbar",
                           command=sc.yview)
        sc.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        sc.pack(fill="both", expand=True, padx=0, pady=0)

        body = tk.Frame(sc, bg=C["bg"])
        win_id = sc.create_window((0, 0), window=body, anchor="nw")
        sc.bind("<Configure>",
                lambda e: sc.itemconfig(win_id, width=e.width))
        body.bind("<Configure>",
                  lambda e: sc.configure(scrollregion=sc.bbox("all")))
        sc.bind_all("<MouseWheel>",
                    lambda e: sc.yview_scroll(int(-1*(e.delta/120)), "units"))

        inner = tk.Frame(body, bg=C["bg"])
        inner.pack(fill="both", expand=True, padx=28, pady=20)

        # ── MCQ Section ───────────────────────────────────────────
        self._section_header(inner, "📝", "Multiple Choice Questions",
                             "#1E3A5F", C["accent_light"])

        for i, q in enumerate(self.mcqs):
            self._build_mcq(inner, i, q)

        if self.mcqs:
            self._spacer(inner, 16)
            check_f = tk.Frame(inner, bg=C["bg"])
            check_f.pack(fill="x")
            self._btn(check_f, "✅  Check All MCQs",
                      self._check_all_mcqs, C["accent"],
                      hover=C["accent_light"]).pack(side="left")
            self._btn(check_f, "🔄  Reset MCQs",
                      self._reset_mcqs, C["border2"],
                      hover=C["accent_dark"]).pack(side="left", padx=(10, 0))
            self.check_result_lbl = tk.Label(check_f, text="",
                font=(FF_B, 11), fg=C["green"], bg=C["bg"])
            self.check_result_lbl.pack(side="left", padx=18)

        # ── Descriptive Section ───────────────────────────────────
        if self.descriptive:
            self._spacer(inner, 24)
            self._section_header(inner, "✍️", "Descriptive Questions",
                                 "#064E3B", C["green"])
            for i, q in enumerate(self.descriptive):
                self._build_descriptive(inner, i, q)

        # ── Bottom bar ────────────────────────────────────────────
        self._spacer(inner, 24)
        bot = tk.Frame(inner, bg=C["card2"], pady=12)
        bot.pack(fill="x")
        self._btn(bot, "🏆  Final Score",
                  self._show_final_score, "#7C3AED",
                  hover="#A78BFA").pack(side="left", padx=(14, 10))
        self._btn(bot, "✖  Close",
                  self.destroy, C["border2"],
                  hover="#7F1D1D").pack(side="left")

    # ─────────────────────────────────────────────────────────────
    def _build_mcq(self, parent, idx: int, q: dict):
        """Build one MCQ block."""
        card = tk.Frame(parent, bg=C["card"],
                        highlightthickness=1,
                        highlightbackground=C["border"])
        card.pack(fill="x", pady=(0, 12))
        self.mcq_frames.append(card)

        # Question
        q_frame = tk.Frame(card, bg=C["card2"])
        q_frame.pack(fill="x")
        num_badge = tk.Label(q_frame,
            text=f"  Q{idx+1}  ",
            font=(FF_B, 9), bg=C["accent_dark"], fg=C["white"])
        num_badge.pack(side="left", pady=8, padx=(10, 0))
        tk.Label(q_frame, text=q.get("q", ""),
                 font=(FF, 11), bg=C["card2"], fg=C["text"],
                 wraplength=680, justify="left", anchor="w"
                 ).pack(side="left", padx=12, pady=8, fill="x", expand=True)

        # Options
        var = tk.StringVar(value="")
        self.mcq_vars.append(var)

        opts_frame = tk.Frame(card, bg=C["card"], pady=4)
        opts_frame.pack(fill="x", padx=16)

        for opt in q.get("options", []):
            letter = opt[0] if opt else "?"
            rb = tk.Radiobutton(
                opts_frame,
                text=opt,
                variable=var,
                value=letter,
                font=(FF, 10),
                bg=C["card"], fg=C["text"],
                selectcolor=C["accent_dark"],
                activebackground=C["card"],
                activeforeground=C["accent_light"],
                highlightthickness=0,
                cursor="hand2",
                anchor="w")
            rb.pack(anchor="w", pady=2)

        # Result label (hidden initially)
        res = tk.Label(card, text="",
                       font=(FF_B, 10), bg=C["card"],
                       anchor="w")
        res.pack(anchor="w", padx=16, pady=(2, 10))
        card._result_lbl = res
        card._correct_ans = q.get("answer", "A")

    # ─────────────────────────────────────────────────────────────
    def _build_descriptive(self, parent, idx: int, q: dict):
        """Build one descriptive question block."""
        card = tk.Frame(parent, bg=C["card"],
                        highlightthickness=1,
                        highlightbackground=C["border"])
        card.pack(fill="x", pady=(0, 12))

        # Question header
        qf = tk.Frame(card, bg=C["green_dark"])
        qf.pack(fill="x")
        tk.Label(qf, text=f"  D{idx+1}  ",
                 font=(FF_B, 9), bg=C["green"], fg=C["white"]
                 ).pack(side="left", pady=8, padx=(10, 0))
        tk.Label(qf, text=q.get("q", ""),
                 font=(FF, 11), bg=C["green_dark"], fg=C["text"],
                 wraplength=680, justify="left", anchor="w"
                 ).pack(side="left", padx=12, pady=8, fill="x", expand=True)

        # Text box for student answer
        txt_wrap = tk.Frame(card, bg=C["input"],
                            highlightthickness=1,
                            highlightbackground=C["border2"])
        txt_wrap.pack(fill="x", padx=16, pady=(10, 6))
        txt = tk.Text(txt_wrap, height=4,
                      font=(FF, 10), bg=C["input"], fg=C["text"],
                      insertbackground=C["accent_light"],
                      relief="flat", bd=0, wrap="word",
                      padx=10, pady=8, highlightthickness=0)
        txt.pack(fill="x")
        txt.insert("1.0", "Write your answer here…")
        txt.bind("<FocusIn>",
                 lambda e, t=txt: t.delete("1.0","end")
                 if t.get("1.0","end-1c") == "Write your answer here…" else None)

        # Show answer button + model answer
        btn_row = tk.Frame(card, bg=C["card"])
        btn_row.pack(fill="x", padx=16, pady=(0, 10))

        model_frame = tk.Frame(card, bg=C["accent_glow"],
                               highlightthickness=1,
                               highlightbackground=C["accent_dark"])

        def toggle_answer(mf=model_frame, q_data=q, btn=None):
            if mf.winfo_ismapped():
                mf.pack_forget()
                if btn:
                    btn.configure(text="👁  Show Model Answer")
            else:
                # Build model answer panel lazily
                for w in mf.winfo_children():
                    w.destroy()
                tk.Label(mf, text="  💡 Model Answer",
                         font=(FF_B, 9), bg=C["accent_glow"],
                         fg=C["accent_light"]).pack(anchor="w", pady=(8,2), padx=10)
                tk.Label(mf, text=q_data.get("answer",""),
                         font=(FF, 10), bg=C["accent_glow"], fg=C["text"],
                         wraplength=700, justify="left", anchor="w"
                         ).pack(anchor="w", padx=14, pady=(0,10), fill="x")
                mf.pack(fill="x", padx=16, pady=(0,10))
                if btn:
                    btn.configure(text="🙈  Hide Model Answer")

        show_btn = self._btn(btn_row, "👁  Show Model Answer",
                             lambda: None,
                             C["accent_dark"], hover=C["accent"])
        show_btn.configure(command=lambda b=show_btn: toggle_answer(btn=b))
        show_btn.pack(side="left")

    # ─────────────────────────────────────────────────────────────
    def _check_all_mcqs(self):
        """Check all MCQ answers and update score."""
        correct = 0
        unanswered = 0
        for i, (var, frame) in enumerate(zip(self.mcq_vars, self.mcq_frames)):
            chosen = var.get()
            correct_ans = frame._correct_ans
            lbl = frame._result_lbl

            if not chosen:
                unanswered += 1
                lbl.configure(text="⚠️  Not answered",
                               fg=C["yellow"], bg=C["card"])
                frame.configure(highlightbackground=C["yellow"])
                continue

            if chosen == correct_ans:
                correct += 1
                lbl.configure(
                    text=f"✅  Correct!  Answer: {correct_ans}",
                    fg=C["green"], bg=C["card"])
                frame.configure(highlightbackground=C["green"])
            else:
                lbl.configure(
                    text=f"❌  Wrong. Correct answer: {correct_ans}",
                    fg=C["red"], bg=C["card"])
                frame.configure(highlightbackground=C["red"])

        self.score = correct
        self.score_lbl.configure(
            text=f"{correct} / {self.total_mcq - unanswered}")

        pct = int(correct / max(self.total_mcq, 1) * 100)
        color = C["green"] if pct >= 70 else C["yellow"] if pct >= 40 else C["red"]
        msg = (f"🏆  {correct}/{self.total_mcq - unanswered} correct  ({pct}%)"
               if not unanswered else
               f"⚠️  {unanswered} unanswered — "
               f"{correct}/{self.total_mcq - unanswered} correct so far")
        self.check_result_lbl.configure(text=msg, fg=color)

    def _reset_mcqs(self):
        for var in self.mcq_vars:
            var.set("")
        for frame in self.mcq_frames:
            frame._result_lbl.configure(text="")
            frame.configure(highlightbackground=C["border"])
        self.score = 0
        self.score_lbl.configure(text=f"0 / {self.total_mcq}")
        self.check_result_lbl.configure(text="")

    def _show_final_score(self):
        pct = int(self.score / max(self.total_mcq, 1) * 100)
        if pct >= 80:
            emoji, msg, col = "🏆", "Excellent work!", C["green"]
        elif pct >= 60:
            emoji, msg, col = "👍", "Good effort, keep practicing!", C["yellow"]
        else:
            emoji, msg, col = "📚", "Review the explanation and try again.", C["red"]

        win = tk.Toplevel(self)
        win.title("Final Score")
        win.geometry("380x260")
        win.configure(bg=C["card"])
        win.grab_set()
        win.resizable(False, False)

        tk.Frame(win, bg=col, height=6).pack(fill="x")
        tk.Label(win, text=emoji, font=(FF, 40),
                 bg=C["card"], fg=col).pack(pady=(20, 4))
        tk.Label(win, text=f"{self.score} / {self.total_mcq}",
                 font=(FF_B, 28), bg=C["card"], fg=col).pack()
        tk.Label(win, text=f"{pct}%  —  {msg}",
                 font=(FF, 11), bg=C["card"], fg=C["text2"]).pack(pady=6)
        tk.Frame(win, bg=C["border"], height=1).pack(fill="x", padx=24, pady=12)
        self._btn(win, "  Close  ", win.destroy,
                  col, hover=C["white"]).pack(pady=4)

    # ── Widget helpers (self-contained) ──────────────────────────
    @staticmethod
    def _section_header(parent, icon, text, bg, fg):
        f = tk.Frame(parent, bg=bg, pady=10)
        f.pack(fill="x", pady=(0, 14))
        tk.Label(f, text=f"  {icon}  {text}",
                 font=(FF_B, 12), bg=bg, fg=fg).pack(side="left", padx=8)

    @staticmethod
    def _spacer(parent, h):
        tk.Frame(parent, bg=parent["bg"], height=h).pack(fill="x")

    @staticmethod
    def _btn(parent, text, cmd, color, hover=None, **kw):
        hover = hover or C["accent"]
        b = tk.Button(parent, text=text, command=cmd,
                      font=(FF_M, 9), bg=color, fg=C["white"],
                      relief="flat", bd=0, padx=16, pady=8,
                      cursor="hand2",
                      activebackground=hover,
                      activeforeground=C["white"], **kw)
        b.bind("<Enter>", lambda e: b.configure(bg=hover))
        b.bind("<Leave>", lambda e: b.configure(bg=color))
        return b



# ═════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    app = App()
    app.mainloop()

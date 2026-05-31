# Lumynary — Built with Claude

> A four-tool AI productivity suite: data analysis, PDF chat, food recipe generation from images, and natural-language CSV queries.  
> Built end-to-end using Claude as my primary coding partner.

---

## Why I built it

I had five messy Python scripts — each doing something interesting with Gemini APIs — but they were isolated, ugly, and broken in subtle ways (the homepage was literally spawning subprocesses to launch separate Streamlit instances on different ports). I wanted to learn Streamlit's multi-page architecture and Gemini's streaming and vision APIs properly, so I used this as the vehicle.

The rule I set myself: **don't ship anything I wouldn't use myself.** A dark-mode app with clashing fonts and hardcoded button hacks doesn't clear that bar. So I rebuilt everything from scratch around a shared design system.

---

## What I built

| Tool | Tech | Key challenge |
|---|---|---|
| 📊 Smart Data Analysis | Pandas, Plotly | Clean group-by UX with dynamic chart type switching |
| 📄 Chat with PDF | FAISS, LangChain, Gemini | True token-by-token streaming over RAG results |
| 🍽️ Recipe Generator | Gemini Vision, base64 | Streaming multimodal output with live cursor |
| 💬 CSV Chat | Gemini 1.5 Flash | Injecting full dataframe context into prompt for accurate NL answers |

The original code also used deprecated embedding models and a broken LangChain chain that wasn't streaming at all — it was looping over characters of the final string to fake the effect. I rewired everything to stream properly.

---

## My secret hacks for AI coding tools

### 1. Dump the entire codebase upfront — always

The biggest mistake I see people make with Claude is feeding it one file at a time. When I gave Claude all five `.py` files at once and said *"here's the full picture, now redesign the architecture"* — it caught the subprocess bug, identified the shared styling problem, and proposed the multi-page solution in a single response. Partial context produces partial solutions.

### 2. Ask AI to critique before you ask it to build

Before writing a single line of the redesign, I asked: *"What are the worst things about this codebase?"* The answer was more useful than any spec I could have written. It surfaced things I'd normalised — hardcoded API keys scattered across five files, a fake streaming loop, no empty states, no shared theme. Critique-first, build-second.

### 3. Scope prompts to one concern at a time

"Redesign the whole app" produces bloated, generic output. "Write only the CSS design system as a shared `theme.py` module — no page logic, just tokens and helper functions" produces something precise you can actually trust. I treat Claude like a focused engineer, not a magic wand.

### 4. Watch the output as the first customer, not the developer

The streaming UX was the thing I tested hardest — not by reading the code, but by sitting in front of the app and watching the `▌` cursor animate through a recipe response character by character. That's how I noticed the original code wasn't streaming at all. The code looked fine. The experience wasn't. Testing from the user's seat catches what code review misses.

---

## What I'd build next

- **Memory across sessions** — right now the PDF chat loses context on reload; I'd persist FAISS indexes per user with a session key
- **CSV auto-visualisation** — when the AI detects a numeric trend in its answer, automatically render a matching Plotly chart inline
- **Prompt library** — let users save and reuse their best queries per tool

---

## Stack

- **Frontend**: Streamlit 1.35+ (multi-page), custom CSS design system
- **AI**: Google Gemini 1.5 Flash (text + vision), LangChain, FAISS
- **Data**: Pandas, Plotly (dark theme)
- **Fonts**: Syne + DM Sans

---

*Built by [Your Name] · Applying for Product Engineering Intern @ TextCortex*  
*Repo: github.com/yourhandle/lumynary*

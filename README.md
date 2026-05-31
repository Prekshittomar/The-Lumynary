# ✦ Lumynary – AI Productivity Suite

> Four AI-powered tools in one sleek, dark-themed Streamlit workspace.

## Tools Included

| # | Tool | Description |
|---|------|-------------|
| 1 | 📊 Smart Data Analysis | Upload CSV/Excel → statistics, charts, group-by |
| 2 | 📄 Chat with PDF | RAG-powered PDF Q&A with streaming answers |
| 3 | 🍽️ Food Recipe Generator | Upload food photo → full streamed recipe via Gemini Vision |
| 4 | 💬 Chat with CSV | Natural-language queries over your CSV data |

## Setup

```bash
# 1. Clone / place all files in a folder
cd lumynary

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
streamlit run homepage.py
```

## Project Structure

```
lumynary/
├── homepage.py          ← Main entry point (run this)
├── theme.py             ← Shared design system & CSS
├── requirements.txt
└── pages/
    ├── 1_📊_Data_Analysis.py
    ├── 2_📄_PDF_Chat.py
    ├── 3_🍽️_Recipe_Generator.py
    └── 4_💬_CSV_Chat.py
```

## API Keys

All Gemini API keys are pre-configured in `theme.py` (`GOOGLE_API_KEY`).  
For production, move these to a `.env` file and use `python-dotenv`.

## Design System

- **Font**: Syne (headings) + DM Sans (body)
- **Theme**: Dark (`#09090f` base) with violet/pink/teal accent gradient
- **Streaming**: All AI responses stream token-by-token
- **Charts**: Plotly with matching dark theme

## Key Improvements Over Original

- ✅ Unified multi-page Streamlit app (no subprocess hacks)
- ✅ Shared dark design system across all pages
- ✅ Full streaming on PDF Chat, Recipe Generator & CSV Chat
- ✅ Hero headers, stat cards, pill badges, custom scrollbars
- ✅ Ambient glow blobs + noise texture on homepage
- ✅ Quick-question suggestions on CSV Chat
- ✅ Download button for generated recipes
- ✅ Auto-plotly chart trigger on CSV Chat for visual queries
- ✅ Better error handling and empty states everywhere

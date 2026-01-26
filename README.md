# Agentic Content Reviewer

AI-powered content analysis demonstrating agentic patterns, evaluation frameworks, and safety guardrails.

## Features

- **Multi-step reasoning** - Transparent chain-of-thought analysis showing how the AI processes content
- **Quality scoring** - Evaluates clarity, grammar, and tone on a 1-10 scale
- **PII detection** - Identifies sensitive personal information (emails, phone numbers, SSNs, etc.)
- **Content improvement** - Generates enhanced versions while preserving original intent

## Tech Stack

- **Backend**: Flask, Python
- **AI**: Claude API (Anthropic)
- **Frontend**: HTML, CSS, JavaScript
- **Deployment**: Gunicorn, Render/Heroku ready

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure environment:
   ```bash
   cp .env.example .env
   # Edit .env and add your ANTHROPIC_API_KEY
   ```
4. Run the application:
   ```bash
   python app.py
   ```
5. Open http://localhost:5001 in your browser

## API

### POST /analyze

Analyzes text content and returns structured results.

**Request:**
```json
{
  "text": "Your content to analyze..."
}
```

**Response:**
```json
{
  "success": true,
  "analysis": {
    "content_type": "email",
    "pii_detected": {
      "has_pii": false,
      "types": [],
      "locations": []
    },
    "quality_scores": {
      "clarity": 7,
      "tone": 8,
      "grammar": 6,
      "overall": 7
    },
    "quality_feedback": "...",
    "improved_version": "..."
  }
}
```

---

*This is a portfolio project demonstrating AI product management skills, including prompt engineering, evaluation framework design, and building user-facing AI applications with appropriate safety guardrails.*

import os
import json
from flask import Flask, request, jsonify, send_from_directory
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
client = Anthropic()

ANALYSIS_PROMPT = """Analyze the following text and provide a structured analysis in JSON format.

Text to analyze:
<text>
{text}
</text>

Provide your analysis as a JSON object with these fields:
1. "content_type": Classify the content (e.g., "email", "article", "social_media_post", "technical_documentation", "marketing_copy", "personal_message", "formal_letter", "creative_writing", "resume", "other")
2. "pii_detected": An object containing:
   - "has_pii": boolean indicating if SENSITIVE PII was found
   - "types": array of PII types found
   - "locations": array of brief descriptions of where PII appears (do not include the actual PII values)
   
   IMPORTANT - Only flag these as PII:
   - Social Security Numbers (SSN)
   - Credit card numbers
   - Bank account numbers
   - Full home addresses (street address with city/state/zip)
   - Phone numbers
   
   DO NOT flag these as PII (they are normal professional information):
   - First names or last names alone
   - Company names or employer names
   - Job titles or professional roles
   - Professional/work email addresses
   - LinkedIn URLs or professional profiles
   - Dates of employment
   
3. "quality_scores": An object with scores from 1-10 for:
   - "clarity": How clear and understandable the text is
   - "tone": How appropriate and consistent the tone is
   - "grammar": Grammatical correctness
   - "overall": Overall quality score
4. "guardrails_feedback": An object with brief, specific feedback (max 6 words each) explaining WHY each score was given:
   - "grammar_feedback": Specific grammar issues found (e.g., "Missing apostrophes and commas", "Run-on sentences throughout", "No issues detected")
   - "tone_feedback": Specific tone observations (e.g., "Too casual for business context", "Overly formal for audience", "Appropriate and professional")
   - "clarity_feedback": Specific clarity issues (e.g., "Vague claims lack specifics", "Well-structured and focused", "Rambling without clear point")
5. "quality_feedback": Brief explanation of the scores and areas for improvement
6. "improved_version": A rewritten version of the text with improvements to clarity, tone, and grammar while preserving the original meaning and intent

Respond ONLY with the JSON object, no additional text."""


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()

    if not data or "text" not in data:
        return jsonify({"error": "Missing 'text' field in request body"}), 400

    text = data["text"]

    if not text or not text.strip():
        return jsonify({"error": "Text cannot be empty"}), 400

    try:
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2048,
            messages=[
                {
                    "role": "user",
                    "content": ANALYSIS_PROMPT.format(text=text)
                }
            ]
        )

        response_text = message.content[0].text

        # Strip markdown code blocks if present
        if response_text.startswith("```"):
            lines = response_text.split("\n")
            # Remove first line (```json) and last line (```)
            lines = lines[1:-1] if lines[-1] == "```" else lines[1:]
            response_text = "\n".join(lines)

        analysis = json.loads(response_text)

        return jsonify({
            "success": True,
            "analysis": analysis
        })

    except json.JSONDecodeError:
        return jsonify({
            "error": "Failed to parse analysis response",
            "raw_response": response_text
        }), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy"})


@app.route("/")
def index():
    return send_from_directory("static", "index.html")


if __name__ == "__main__":
    app.run(debug=True, port=5001)

from pydantic import BaseModel
from typing import Literal

class ExtractTheme(BaseModel):
    subject: Literal["Payments", "POS Performance", "Reporting & Analytics", "User Experience (UX)", "Hardware", "Onboarding & Training", "Support Quality", "Integrations", "Pricing & Billing", "Feature Request", "Reliability & Stability", "Other"]
    sentiment: Literal["Positive", "Neutral", "Negative", "Frustrated"]

THEME_EXTRACTION_PROMPT = """
Your task is to categorize customer feedback into predefined product themes.

You must follow these rules:

1. Only use themes and sentiment from the provided lists.
2. Do NOT invent new themes or sentiment.
3. If no theme fits well, use "Other".
4. Output must be valid JSON only.

Allowed Themes:
- Payments
- POS Performance
- Reporting & Analytics
- User Experience (UX)
- Hardware
- Onboarding & Training
- Support Quality
- Integrations
- Pricing & Billing
- Feature Request
- Reliability & Stability
- Other

Also classify sentiment as one of:
- Positive
- Neutral
- Negative
- Frustrated

Feedback Text:
{feedback_text}

"""

class FeedbackSummary(BaseModel):
    summary: str
    risk_level: str
    recommended_action: str

FEEDBACK_SUMMARY_PROMPT = """
Your task is to analyze all feedback and produce a summary of the merchant's experience and potential risk.

Instructions:
1. Carefully review all feedback entries.
2. Identify recurring problems, complaints, or positive signals.
4. Provide a summary describing the key issues or topics.
5. Assign a risk level based on the feedback.

Risk level definitions:
- Low: Mostly positive feedback with minor issues.
- Medium: Some recurring complaints or moderate dissatisfaction.
- High: Frequent negative feedback, operational problems, or strong dissatisfaction.

Also provide a consice recommended action that the company should take.

Merchant Feedback Data:
{feedback_data}

"""
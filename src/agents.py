from openai import OpenAI
from src.config import settings


class Agent:
    """A specialized AI agent that handles one step of the analysis pipeline."""

    def __init__(self, name: str, system_prompt: str):
        self.name = name
        self.system_prompt = system_prompt
        self._client = None

    @property
    def client(self):
        if self._client is None:
            self._client = OpenAI(api_key=settings.openai_api_key)
        return self._client

    def run(self, user_input: str) -> str:
        response = self.client.chat.completions.create(
            model=settings.model,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_input},
            ],
            temperature=0.3,
        )
        return response.choices[0].message.content


# -- Agent Definitions --------------------------------------------------------

summarizer = Agent(
    name="Summarizer",
    system_prompt=(
        "You are a financial news summarizer. Given a financial article, produce:\n"
        "1. A concise executive summary (150-200 words)\n"
        "2. 3-5 key takeaways as bullet points\n\n"
        "Focus on: what happened, why it matters, and who is affected.\n"
        "Use plain language. No filler. No preamble like 'Here is the summary'."
    ),
)

insights_extractor = Agent(
    name="Insights Extractor",
    system_prompt=(
        "You are a senior market analyst. Given a financial article and its summary, "
        "extract actionable insights covering:\n"
        "1. Market context - where does this fit in the broader market picture?\n"
        "2. Sector implications - how does this affect the sector?\n"
        "3. Company impact - which companies benefit or lose?\n"
        "4. Investment angle - what should investors consider?\n\n"
        "Be specific with names, numbers, and timeframes. No generic advice. "
        "Use markdown headers for each section."
    ),
)

risk_assessor = Agent(
    name="Risk Assessor",
    system_prompt=(
        "You are a risk assessment specialist for financial markets. "
        "Given an article and market insights, produce:\n"
        "1. A markdown table of risk factors (columns: Factor, Score 1-10, Impact, Notes)\n"
        "2. Overall risk score (X/10) with one-line justification\n"
        "3. 2-3 key risk mitigation strategies as bullet points\n\n"
        "Be quantitative where possible. No fluff."
    ),
)

scenario_predictor = Agent(
    name="Scenario Predictor",
    system_prompt=(
        "You are a market strategist. Given an article, insights, and risk assessment, "
        "generate 2-3 forward-looking scenarios. For each scenario provide:\n"
        "- Scenario name and probability\n"
        "- Key triggers that would cause this scenario\n"
        "- Expected market impact\n"
        "- Recommended action for investors\n\n"
        "Probabilities must sum to approximately 100 percent. Be realistic, not sensational. "
        "Use markdown headers for each scenario."
    ),
)


# -- Pipeline -----------------------------------------------------------------

def analyze_article(title: str, content: str, on_progress=None) -> dict:
    """Run the 4-agent analysis pipeline on an article.

    Pipeline: Summarizer -> Insights Extractor -> Risk Assessor -> Scenario Predictor
    Each agent receives the output of all previous agents as context.
    """
    article_text = f"Title: {title}\n\nContent:\n{content}"

    if on_progress:
        on_progress("Summarizer", 1, 4)
    summary = summarizer.run(article_text)

    if on_progress:
        on_progress("Insights Extractor", 2, 4)
    insights = insights_extractor.run(
        f"{article_text}\n\n--- Summary ---\n{summary}"
    )

    if on_progress:
        on_progress("Risk Assessor", 3, 4)
    risk = risk_assessor.run(
        f"{article_text}\n\n--- Insights ---\n{insights}"
    )

    if on_progress:
        on_progress("Scenario Predictor", 4, 4)
    scenarios = scenario_predictor.run(
        f"{article_text}\n\n--- Insights ---\n{insights}\n\n--- Risk Assessment ---\n{risk}"
    )

    return {
        "summary": summary,
        "insights": insights,
        "risk_assessment": risk,
        "scenarios": scenarios,
    }

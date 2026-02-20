# Article Summary & Insights

Multi-agent AI system that analyzes financial articles and generates structured investment insights.

Give it a URL — it scrapes the article, runs it through 4 specialized AI agents, and outputs a markdown report with summary, market insights, risk scoring, and scenario predictions.

## How It Works

```
Article URL
     |
     v
[Scraper] ── extract article text from URL
     |
     v
[Summarizer Agent] ── executive summary + key takeaways
     |
     v
[Insights Agent] ── market context, sector impact, company analysis
     |
     v
[Risk Agent] ── risk factor table with quantitative scores
     |
     v
[Scenario Agent] ── 2-3 forward-looking scenarios with probabilities
     |
     v
Markdown Report
```

Each agent builds on the previous agent's output. The Summarizer condenses the article, the Insights agent uses that summary to extract market implications, the Risk agent scores threats based on those insights, and the Scenario agent projects outcomes from everything above.

| Agent | What It Does |
|-------|-------------|
| **Summarizer** | 150-200 word executive summary + bullet-point takeaways |
| **Insights Extractor** | Market context, sector implications, company impact, investment angles |
| **Risk Assessor** | Risk factor matrix (scored 1-10) + overall risk rating + mitigation strategies |
| **Scenario Predictor** | 2-3 probability-weighted scenarios with triggers and recommended actions |

## Setup

```bash
git clone https://github.com/Mohit1053/Article-Summary-Insights.git
cd Article-Summary-Insights
pip install -r requirements.txt
cp .env.example .env   # add your OpenAI API key
```

## Usage

```bash
# Analyze an article
python main.py "https://economictimes.com/some-financial-article"

# Specify output file
python main.py "https://..." -o report.md

# Use a different model
python main.py "https://..." -m gpt-4o
```

Output:

```
Scraping: https://economictimes.com/...
Title: Top Dynamic Bond Funds to Invest in August 2025
Extracted: 4,230 characters

Running analysis pipeline:
  [1/4] Summarizer...
  [2/4] Insights Extractor...
  [3/4] Risk Assessor...
  [4/4] Scenario Predictor...
Done.

Report saved: outputs/top-dynamic-bond-funds-to-invest-in-august-2025.md
```

Reports are saved to `outputs/` by default.

## Sample Report

See [examples/sample_report.md](examples/sample_report.md) for what a generated report looks like.

## Configuration

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `OPENAI_API_KEY` | Yes | — | Your OpenAI API key |
| `MODEL` | No | `gpt-4o-mini` | OpenAI model to use |
| `OUTPUT_DIR` | No | `outputs` | Where reports are saved |

## Project Structure

```
Article-Summary-Insights/
├── src/
│   ├── agents.py       # 4 specialized analysis agents + pipeline
│   ├── scraper.py      # Article extraction from URLs
│   ├── report.py       # Markdown report builder
│   └── config.py       # Environment configuration
├── examples/
│   └── sample_report.md
├── main.py             # CLI entry point
├── .env.example
├── requirements.txt
└── README.md
```

## Tech Stack

- **Python 3.10+**
- **OpenAI API** — powers all 4 analysis agents
- **BeautifulSoup4 + lxml** — article scraping and text extraction
- **Click** — CLI interface
- **python-dotenv** — environment configuration

## License

MIT

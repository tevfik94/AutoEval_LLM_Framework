# ⚖️ AutoJudge: Arabic-Focused LLM Evaluation Framework

**AutoJudge** is a modular, automated framework for evaluating Large Language Models (LLMs) using an "LLM-as-a-Judge" approach. 

Designed by **Tevfik Istanbullu**, this tool automates the Quality Assurance process for Arabic and English LLM outputs, replacing manual human annotation with rigorous, rubric-based AI evaluation.

## 🚀 Key Features
- **Config-Driven:** Fully customizable via `config.yaml`. Bring your own data and column names.
- **Multilingual Support:** Specialized rubrics for **Arabic** (Grammar, Dialect/MSA) and English.
- **Model Agnostic:** currently supports **Google Gemini 1.5** (Flash/Pro) as the Judge, with architecture ready for OpenAI/Anthropic.
- **Detailed Reporting:** Outputs JSON for machines and CSV for human analysis, including step-by-step reasoning for every score.

## 🛠️ Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/AutoJudge.git
   cd AutoJudge
2. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
3. **Set up API Keys:**

    Create a .env file in the root directory:
    ```
    GEMINI_API_KEY=your_google_api_key_here

## 📊 Usage

1. **Prepare your Data:**

    Place your CSV file in the data/ folder. It should have columns for the Question, Answer, and (Optionally) Ground Truth.
2. **Configure:**

    Edit config.yaml to map your CSV columns to the system.
3. **Run the Judge:**
    ```bash
    python main.py
4. **View Results:**
Check `data/evaluation_results.csv` for the Scores (1-5) and Reasoning.

## 🧠 Rubric Examples

The system uses "Chain of Thought" reasoning. Example criteria for Arabic Summarization:
- Coverage: Does the summary include all key points?
- Hallucination: Is there information not present in the source?
- Language: Is the Arabic phrasing natural (MSA)?

## 🛡️ License

MIT License

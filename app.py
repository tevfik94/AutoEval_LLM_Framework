import gradio as gr
import pandas as pd
import os
from src.judges import GeminiJudge
from src.prompts import get_prompt


# 1. Define the Logic for the Web UI
def evaluate_csv(file_obj, api_key):
    """
    Takes a CSV file upload and an API Key, runs the judge, returns the path to the result.
    """
    # Security: Use the key provided by the user in the UI
    if not api_key:
        return None, "⚠️ Please enter a Google Gemini API Key."

    # Temporarily set the env var for our Judge Class to find it
    os.environ["GEMINI_API_KEY"] = api_key

    try:
        # Load the uploaded CSV
        df = pd.read_csv(file_obj.name)

        # Initialize Judge
        judge = GeminiJudge()
        results = []

        # Process rows (Limit to first 10 rows for the Demo to be fast)
        # In a real app, you would process all.
        max_rows = 10
        subset = df.head(max_rows)

        for index, row in subset.iterrows():
            # Heuristic: Try to guess column names if not configured
            # (Or assume the user follows our template)
            q_col = next(
                (
                    c
                    for c in df.columns
                    if "question" in c.lower() or "input" in c.lower()
                ),
                df.columns[0],
            )
            a_col = next(
                (
                    c
                    for c in df.columns
                    if "answer" in c.lower() or "output" in c.lower()
                ),
                df.columns[1],
            )
            cap = "default"  # Default capability for demo

            prompt = get_prompt(cap, row[q_col], row[a_col])
            eval_result = judge.evaluate(prompt)

            # Save result
            row["AutoJudge_Score"] = eval_result.get("score")
            row["AutoJudge_Reasoning"] = eval_result.get("reasoning")
            results.append(row)

        # Create Result DataFrame
        result_df = pd.DataFrame(results)
        output_path = "evaluated_results.csv"
        result_df.to_csv(output_path, index=False)

        return output_path, "✅ Evaluation Complete! Download your CSV below."

    except Exception as e:
        return None, f"Error: {str(e)}"


# 2. Build the UI
with gr.Blocks(title="AutoJudge Framework") as demo:
    gr.Markdown("# ⚖️ AutoJudge: AI-Powered LLM Evaluator")
    gr.Markdown(
        "Upload a CSV file with columns like 'question' and 'answer' to automatically grade them using Gemini Pro."
    )

    with gr.Row():
        api_input = gr.Textbox(
            label="Enter Gemini API Key", type="password", placeholder="AIzaSy..."
        )

    file_input = gr.File(label="Upload CSV (Max 10 rows for demo)")
    run_btn = gr.Button("Run Judge", variant="primary")

    status_text = gr.Textbox(label="Status", interactive=False)
    file_output = gr.File(label="Download Results")

    run_btn.click(
        evaluate_csv, inputs=[file_input, api_input], outputs=[file_output, status_text]
    )

# 3. Launch
if __name__ == "__main__":
    demo.launch()

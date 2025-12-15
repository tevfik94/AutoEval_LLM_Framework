"""
This file stores the Evaluation Rubrics (Criteria) for different capabilities.
"""

# The Master Instruction tells the LLM how to behave generally.
# We enforce JSON output to make it machine-readable.
SYSTEM_PROMPT_TEMPLATE = """
You are an impartial expert AI Judge evaluating a response in {language}.
Your task is to evaluate the 'Model Answer' based on the provided 'Question' and 'Rubric'.

Input Data:
- Question: {question}
- Model Answer: {answer}
- Ground Truth (Optional): {ground_truth}

Evaluation Steps:
1. Analyze the Question and the Model Answer carefully.
2. Compare the Model Answer against the Rubric and Ground Truth (if available).
3. Think step-by-step about the quality (Accuracy, Relevance, Style).
4. Assign a score from 1 to 5.
5. Output ONLY a valid JSON object in the following format:

{{
    "reasoning": "Your step-by-step explanation here...",
    "score": <integer_1_to_5>
}}
"""

# The Rubrics define what "Good" looks like for specific tasks.
RUBRICS = {
    "default": """
        Criteria:
        - Relevance: Does the answer directly address the question?
        - Accuracy: Is the information factually correct?
        - Clarity: Is the language clear and easy to understand?
    """,
    "math": """
        Criteria:
        - Logic: Are the mathematical steps logically sound?
        - Calculation: Are the final values correct?
        - Format: Is the solution presented clearly?
        - If the reasoning is correct but the final number is wrong, give a maximum score of 3.
    """,
    "summarization": """
        Criteria:
        - Coverage: Does the summary include all key points from the source?
        - Conciseness: Is the summary free of unnecessary details?
        - Hallucination: Does the summary contain information NOT present in the source? (If yes, Score = 1).
    """,
    "translation": """
        Criteria:
        - Fidelity: Is the meaning preserved accurately?
        - Fluency: Does the translated text sound natural in the target language?
        - Grammar: Are there any syntax or morphology errors?
    """,
    # You can add "arabic_grammar", "coding", etc. here.
}


def get_prompt(capability, question, answer, ground_truth=None, language="Arabic"):
    """
    Constructs the final prompt sent to the LLM.
    """
    # 1. Select the specific rubric, fallback to 'default' if not found
    rubric_text = RUBRICS.get(capability.lower(), RUBRICS["default"])

    # 2. Format the template
    gt_text = ground_truth if ground_truth else "N/A"

    final_prompt = SYSTEM_PROMPT_TEMPLATE.format(
        language=language, question=question, answer=answer, ground_truth=gt_text
    )

    # Append the specific rubric at the end to keep it fresh in context
    final_prompt += f"\n\nSPECIFIC RUBRIC TO USE:\n{rubric_text}"

    return final_prompt

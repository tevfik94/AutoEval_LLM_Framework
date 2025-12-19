import time
from tqdm import tqdm
from src.dataloader import DataLoader
from src.judges import get_judge
from src.prompts import get_prompt
from src.reporter import Reporter


def main():
    print("🚀 Starting AutoJudge Framework...")

    # 1. Initialize Components
    try:
        loader = DataLoader("config.yaml")
        data = loader.load_data()

        config = loader.config
        judge = get_judge(config)
        reporter = Reporter(config)

        print(f"🔹 Model Selected: {config['judge_model']}")
        print(f"🔹 Records to Process: {len(data)}")

    except Exception as e:
        print(f"❌ Initialization Error: {e}")
        return

    # 2. Processing Loop
    results = []

    # tqdm creates the progress bar
    for record in tqdm(data, desc="Evaluating"):
        try:
            # A. Prepare the Prompt
            prompt_text = get_prompt(
                capability=record["capability"],
                question=record["question"],
                answer=record["answer"],
                ground_truth=record.get("ground_truth"),
                language=config.get("language", "Arabic"),
            )

            # B. Call the Judge
            evaluation = judge.evaluate(prompt_text)

            # C. Merge Results
            # We add the score/reasoning back into the record object
            record["score"] = evaluation.get("score", 0)
            record["reasoning"] = evaluation.get("reasoning", "Error parsing output")

            # D. Add to results list
            results.append(record)

            # Sleep briefly to avoid hitting API rate limits (Good practice)
            time.sleep(1)

        except Exception as e:
            print(f"\n⚠️ Error processing ID {record['id']}: {e}")
            record["score"] = -1
            record["reasoning"] = f"Pipeline Error: {str(e)}"
            results.append(record)

    # 3. Save Final Report
    reporter.save_results(results)
    print("\n✅ Evaluation Complete.")


if __name__ == "__main__":
    main()

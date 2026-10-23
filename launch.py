"""Run this file in PyCharm or: python3 launch.py"""
import getpass
import os
import webbrowser
import agents


def main():
    agents.load_env(agents.ROOT / ".env")
    print("\nRAVELYA LABS | Synthetic Student Agents\n")
    print("1. Preview five profiles + baseline (no API calls)")
    print("2. Live smoke test: one profile, two conditions (4 API calls)")
    print("3. Live charter rehearsal: five profiles + baseline (24 API calls)")
    choice = input("Choose 1, 2, or 3 [1]: ").strip() or "1"
    if choice not in {"1", "2", "3"}:
        raise ValueError("Please choose 1, 2, or 3")
    options = ["--baseline"] if choice in {"1", "3"} else ["--profile", "conscientiousness"]
    if choice == "1":
        options.append("--preview")
    else:
        print("Live calls use your OpenAI API billing; ChatGPT subscription does not supply an API key.")
        if not os.environ.get("OPENAI_API_KEY"):
            os.environ["OPENAI_API_KEY"] = getpass.getpass("API key (hidden, held only in this process): ")
        model = os.environ.get("OPENAI_MODEL") or input("Model ID available to your API project: ").strip()
        if not model:
            raise ValueError("A model ID is required for live mode")
        options += ["--model", model]
    args = agents.parser().parse_args(options)
    out, records = agents.run(args)
    webbrowser.open((out / "report.html").as_uri())
    if any(r["status"] == "failed" for r in records):
        print("A trial failed; inspect the report before retrying.")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, KeyboardInterrupt) as exc:
        print(f"Stopped: {exc}")

import argparse

from src.extract_text import extract_text
from src.llm_extractor import extract_data
from src.comparator import load_job_description, compare_resume
from src.report import generate_report, save_report
from src.scorer import calculate_score

def main():
    parser = argparse.ArgumentParser(
        description="CareerLens AI - Resume Screening System"
    )

    parser.add_argument(
        "resume",
        help="Path to resume PDF or DOCX"
    )

    args = parser.parse_args()

    try:
        resume_text = extract_text(args.resume)

        resume = extract_data(resume_text)

        job = load_job_description("data/job_description.json")

        match_result = compare_resume(job, resume)

        score = calculate_score(match_result)

        match_result.score = score

        generate_report(resume, match_result)

        save_report(resume, job, match_result)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
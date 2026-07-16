import argparse
from pathlib import Path

from src.extract_text import extract_text
from src.llm_extractor import extract_data, extract_job
from src.comparator import compare_resume
from src.report import (
    generate_report,
    save_report,
    save_rankings,
    get_candidate_status
)
from src.scorer import calculate_score

def main():
    parser = argparse.ArgumentParser(
        description="CareerLens AI - Resume Screening System"
    )

    parser.add_argument(
        "resume_folder",
        help="Folder containing PDF/DOCX resumes"
    )

    parser.add_argument(
        "--job",
        required=True,
        help="Path to the job description (.txt/.pdf/.docx)"
    )

    args = parser.parse_args()

    try:
        resume_folder = Path(args.resume_folder)

        job_text = extract_text(args.job)
        job = extract_job(job_text)

        resume_files = [
            file for file in resume_folder.iterdir()
            if file.suffix.lower() in [".pdf", ".docx"]
        ]

        print(f"Found {len(resume_files)} resume(s).\n")

        results = []

        for resume_file in resume_files:

            print(f"\nProcessing: {resume_file.name}")

            resume_text = extract_text(str(resume_file))

            resume = extract_data(resume_text)

            match_result = compare_resume(job, resume)

            score = calculate_score(match_result)

            match_result.score = score

            generate_report(resume, match_result)

            save_report(resume, job, match_result)

            status, decision = get_candidate_status(match_result.score)

            results.append({
                "name": resume.name,
                "score": match_result.score,
                "status": status,
                "decision": decision
            })

        results.sort(
            key=lambda candidate: candidate["score"],
            reverse=True
        )

        print()

        print("=" * 100)
        print(
            f"{'Rank':<6}"
            f"{'Candidate':<28}"
            f"{'Score':<10}"
            f"{'Status':<20}"
            f"{'Decision'}"
        )

        print("=" * 100)

        for index, candidate in enumerate(results, start=1):

            print(
                f"{index:<6}"
                f"{candidate['name']:<28}"
                f"{candidate['score']:<10.1f}"
                f"{candidate['status']:<20}"
                f"{candidate['decision']}"
            )

        print("=" * 100)
        save_rankings(results)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
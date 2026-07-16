import argparse
from pathlib import Path

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
        "resume_folder",
        help="Folder containing PDF/DOCX resumes"
    )

    args = parser.parse_args()

    try:
        resume_folder = Path(args.resume_folder)

        job = load_job_description("data/job_description.json")

        results = []

        for resume_file in resume_folder.iterdir():

            if resume_file.suffix.lower() not in [".pdf", ".docx"]:
                continue

            print(f"\nProcessing: {resume_file.name}")

            resume_text = extract_text(str(resume_file))

            resume = extract_data(resume_text)

            match_result = compare_resume(job, resume)

            score = calculate_score(match_result)

            match_result.score = score

            generate_report(resume, match_result)

            save_report(resume, job, match_result)

            results.append({
                "name": resume.name,
                "score": match_result.score
            })

        results.sort(
            key=lambda candidate: candidate["score"],
            reverse=True
        )

        print("\n" + "=" * 50)
        print("          FINAL RANKINGS")
        print("=" * 50)

        for index, candidate in enumerate(results, start=1):
            print(f"{index}. {candidate['name']} - {candidate['score']:.1f}%")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
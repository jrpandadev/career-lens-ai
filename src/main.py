import argparse
from pathlib import Path
from src.model import JobD, Resume

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

SUPPORTED_EXTENSIONS = {".pdf", ".docx"}

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
        required=False,
        default="jobs/amazon.txt",
        help="Path to the job description (.txt/.pdf/.docx)"
    )

    args = parser.parse_args()

    try:
        resume_folder = Path(args.resume_folder)

        if not resume_folder.exists():
            raise FileNotFoundError(f"Resume folder not found: {resume_folder}")

        job_text = extract_text(args.job)
        job = extract_job(job_text)

        job_specific_skills = set(job.required_skill_keywords + job.preferred_skill_keywords)

        resume_files = [
            file for file in resume_folder.iterdir()
            if file.suffix.lower() in SUPPORTED_EXTENSIONS
        ]

        if not resume_files:
            print("No PDF or DOCX resumes found.")
            return

        print(f"Found {len(resume_files)} resume(s).\n")

        results = []

        for index, resume_file in enumerate(resume_files, start=1):

            print(f"\n[{index}/{len(resume_files)}] Processing: {resume_file.name}")

            try:
                resume_text = extract_text(str(resume_file))
                resume = extract_data(resume_text, job_specific_skills)

                match_result = compare_resume(job, resume)

                match_result = calculate_score(match_result, job, resume)

                generate_report(resume, match_result)

                save_report(resume, job, match_result)

                status, decision = get_candidate_status(match_result.score)

                results.append({
                    "name": resume.name,
                    "score": match_result.score,
                    "req_match": f"{len(match_result.matched_required_skills)}/{len(job.required_skills)}",
                    "pref_match": f"{len(match_result.matched_preferred_skills)}/{len(job.preferred_skills)}",
                    "exp_match": "[+]" if match_result.experience_match else "[-]",
                    "status": status,
                    "decision": decision,
                    "match_result": match_result
                })
            except Exception as e:
                print(f"Failed to process {resume_file.name}")
                print(e)
                continue

        results.sort(
            key=lambda candidate: candidate["score"],
            reverse=True
        )

        save_rankings(results)

        print()

        print("=" * 105)
        print(
            f"{'Rank':<6}"
            f"{'Candidate':<20}"
            f"{'Score':<10}"
            f"{'Required':<11}"
            f"{'Preferred':<12}"
            f"{'Experience':<13}"
            f"{'Decision'}"
        )

        print("=" * 105)

        for index, candidate in enumerate(results, start=1):
            name = str(candidate['name'] or "Unknown").replace("\r\n", " ").replace("\r", " ").replace("\n", " ")
            name = (name[:17] + '...') if len(name) > 17 else name
            
            score_str = f"{candidate['score']:.1f}%"
            print(
                f"{index:<6}"
                f"{name:<20}"
                f"{score_str:<10}"
                f"{candidate['req_match']:<11}"
                f"{candidate['pref_match']:<12}"
                f"{candidate['exp_match']:<13}"
                f"{candidate['decision']}"
            )

        print("=" * 105)

        top_2 = results[:2]
        worst_2 = results[-2:] if len(results) >= 2 else []

        print("\nTOP 2 CANDIDATES")
        print("-" * 20)
        for candidate in top_2:
            mr = candidate['match_result']
            print(f"{candidate['name']} - {candidate['score']:.1f}%")
            if mr.strengths:
                print(f"Strengths: {', '.join(mr.strengths)}")
            if mr.weaknesses:
                print(f"Weaknesses: {', '.join(mr.weaknesses)}")
            print()

        if len(results) > 2:
            print("LOWEST 2 CANDIDATES")
            print("-" * 23)
            for candidate in worst_2:
                mr = candidate['match_result']
                print(f"{candidate['name']} - {candidate['score']:.1f}%")
                if mr.strengths:
                    print(f"Strengths: {', '.join(mr.strengths)}")
                if mr.weaknesses:
                    print(f"Weaknesses: {', '.join(mr.weaknesses)}")
                print()

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
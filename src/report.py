import json
import os
from datetime import datetime
from src.model import MatchResult, JobD

OUTPUT_DIR = "output"
REPORT_FILE = os.path.join(OUTPUT_DIR, "report.json")

def generate_report(resume, match_result: MatchResult) -> None:

    print("\n" + "=" * 50)
    print("        RESUME MATCH REPORT")
    print("=" * 50)

    print(f"\nCandidate : {resume.name}")
    print(f"Match Score : {match_result.score}%")

    print("\nMatched Skills")
    print("-" * 20)
    for skill in match_result.matched_skills:
        print(f"✓ {skill}")

    print("\nMissing Skills")
    print("-" * 20)
    for skill in match_result.missing_skills:
        print(f"✗ {skill}")

    print("\nStrengths")
    print("-" * 20)
    for strength in match_result.strengths:
        print(f"★ {strength}")

    print("\nWeaknesses")
    print("-" * 20)
    for weakness in match_result.weaknesses:
        print(f"⚠ {weakness}")

    print("\nRecommendation")
    print("-" * 20)
    print(match_result.recommendation)

def get_candidate_status(score: float) -> tuple[str, str]:
    """
    Returns (status, decision)
    """

    if score >= 85:
        return "⭐ Strong Hire", "Shortlist"

    if score >= 70:
        return "✅ Good Match", "Interview"

    if score >= 50:
        return "🟡 Review", "Manual Review"

    return "❌ Reject", "Reject"

def save_report(resume, job: JobD, match_result: MatchResult) -> None:
    report = {
        "generated_at": datetime.now().isoformat(),
        "candidate": resume.name,
        "job_role": job.role,
        "match_score": match_result.score,
        "matched_skills": match_result.matched_skills,
        "missing_skills": match_result.missing_skills,
        "strengths": match_result.strengths,
        "weaknesses": match_result.weaknesses,
        "recommendation": match_result.recommendation
    }

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    candidate_name = resume.name or "Unknown"

    safe_name = (
        candidate_name
        .replace(" ", "_")
        .replace("/", "_")
        .replace("\\", "_")
    )

    file_path = f"output/{safe_name}_report.json"

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(report, file, indent=4)

def save_rankings(results):
    os.makedirs("output", exist_ok=True)

    formatted_results = []
    for index, candidate in enumerate(results, start=1):
        formatted_results.append({
            "rank": index,
            "candidate": candidate.get("name", "Unknown"),
            "score": candidate.get("score", 0.0),
            "status": candidate.get("status", "Unknown"),
            "decision": candidate.get("decision", "Unknown")
        })

    with open("output/rankings.json", "w", encoding="utf-8") as file:
        json.dump(
            formatted_results,
            file,
            indent=4,
            ensure_ascii=False
        )
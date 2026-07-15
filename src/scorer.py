def calculate_score(comparison_result, hr):
    # ----------- Skills Score (60%) -----------

    total_skills = len(hr["skills"])
    matched_skills = len(comparison_result["matched_skills"])

    skill_score = (matched_skills / total_skills) * 60

    # ----------- Experience Score (20%) -----------

    experience_score = 20 if comparison_result["experience_match"] else 0

    # ----------- Projects Score (20%) -----------

    project_score = 20 if comparison_result["projects_match"] else 0

    total_score = skill_score + experience_score + project_score

    return round(total_score, 2)

    
    



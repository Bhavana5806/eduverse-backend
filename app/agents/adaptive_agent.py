def generate_recommendation(status: str, percentage: float):

    if status == "Critical Weakness":
        level = "Beginner"
        strategy = "Revise fundamentals, practice 10 basic problems daily."
    elif status == "Needs Improvement":
        level = "Intermediate"
        strategy = "Practice mixed difficulty problems and review mistakes."
    elif status == "Good":
        level = "Advanced"
        strategy = "Solve previous year questions and timed quizzes."
    else:
        level = "Expert"
        strategy = "Attempt competitive level problems."

    improvement_target = min(percentage + 20, 100)

    return {
        "recommended_level": level,
        "strategy": strategy,
        "target_score_percentage": improvement_target
    }
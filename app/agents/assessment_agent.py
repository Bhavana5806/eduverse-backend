def analyze_performance(score: float, max_score: float):
    percentage = (score / max_score) * 100

    if percentage < 40:
        status = "Critical Weakness"
    elif percentage < 60:
        status = "Needs Improvement"
    elif percentage < 80:
        status = "Good"
    else:
        status = "Strong"

    return percentage, status
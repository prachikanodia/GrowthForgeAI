
def choose_frameworks(req):
    text = f"{req.decision} {req.goal} {req.context}".lower()
    frameworks = []

    # Always include a risk lens if urgency high or low tolerance
    if req.urgency == "high" or req.risk_tolerance == "low":
        frameworks += ["Risk Matrix", "Experiment Design"]

    # If cost/budget/pricing mentioned
    if any(k in text for k in ["budget", "cost", "pricing", "roi", "spend", "revenue"]):
        frameworks.append("Cost-Benefit")

    # If competition / market mentioned
    if any(k in text for k in ["competitor", "competition", "market", "rival", "substitute"]):
        frameworks.append("Porter")

    # Default 
    frameworks.append("SWOT")

    frameworks = list(dict.fromkeys(frameworks))[:4]
    return frameworks
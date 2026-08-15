# test.py
import re
from job_matcher import JobMatcher
from roadmap_generator import RoadmapGenerator
from skill_extractor import SkillExtractor

# 1. Text Cleaner
TOKEN_MAP = {
    r"(?<!\w)c\+\+(?!\w)": "TOKEN_CPP",
    r"(?<!\w)c#(?!\w)": "TOKEN_CSHARP",
    r"(?<!\w)\.net(?!\w)": "TOKEN_DOTNET",
    r"(?<!\w)node\.js(?!\w)": "TOKEN_NODEJS",
    r"(?<!\w)ci/cd(?!\w)": "TOKEN_CICD",
    r"(?<!\w)scikit-learn(?!\w)": "TOKEN_SKLEARN",
}
REVERSE_TOKEN_MAP = {
    "token_cpp": "c++",
    "token_csharp": "c#",
    "token_dotnet": ".net",
    "token_nodejs": "node.js",
    "token_cicd": "ci/cd",
    "token_sklearn": "scikit-learn",
}


def clean_text(text: str) -> str:
    normalized = text.lower()
    for pattern, placeholder in TOKEN_MAP.items():
        normalized = re.sub(pattern, placeholder, normalized, flags=re.IGNORECASE)
    normalized = re.sub(r"http\S+|www\.\S+", " ", normalized)
    normalized = re.sub(r"\S+@\S+", " ", normalized)
    normalized = re.sub(r"\+?\d[\d -]{8,12}\d", " ", normalized)
    normalized = re.sub(r"[^\w\s]", " ", normalized)
    for token_placeholder, original_skill in REVERSE_TOKEN_MAP.items():
        normalized = re.sub(
            rf"\b{token_placeholder}\b",
            original_skill,
            normalized,
            flags=re.IGNORECASE,
        )
    return re.sub(r"\s+", " ", normalized).strip()


if __name__ == "__main__":
    # Test resume snippet
    sample_resume = """
    Computer Science student with experience in Python, SQL, and Pandas.
    Developed predictive models using scikit-learn.
    Built automated data analytics dashboards with Power BI and Excel.
    Familiar with Git and basic Docker containers.
    """

    print("=== Step 1: Cleaning Resume ===")
    cleaned_resume = clean_text(sample_resume)

    print("\n=== Step 2: Extracting Skills ===")
    extractor = SkillExtractor("skills.csv")
    extraction_results = extractor.extract_skills(cleaned_resume)
    candidate_skills = extraction_results["skills_found"]
    print(f"Extracted Skills ({len(candidate_skills)}): {candidate_skills}")

    print("\n=== Step 3: Evaluating Target Job Roles ===")
    matcher = JobMatcher("job_roles.csv")
    rankings = matcher.evaluate_resume(cleaned_resume, candidate_skills)

    for idx, role in enumerate(rankings, 1):
        print(
            f"{idx}. {role['role_title']} | Match Score: {role['match_score']}%"
        )
        print(f"   - Matched Skills: {role['matched_skills']}")
        print(f"   - Missing Skills: {role['missing_skills']}")

    print("\n=== Step 4: Generating Learning Roadmap for Top Role ===")
    top_role = rankings[0]
    print(f"Target Role: {top_role['role_title']}")
    roadmap = RoadmapGenerator.generate_roadmap(top_role["missing_skills"])
    for step in roadmap:
        print(f"• {step['week']} ({step['focus']}): {step['action']}")
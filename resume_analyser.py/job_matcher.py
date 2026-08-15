"""
job_matcher.py
Calculates TF-IDF cosine similarity and skill coverage across target job roles.
"""

from typing import Any, Dict, List
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class JobMatcher:

    def __init__(self, job_roles_path: str = "job_roles.csv"):
        self.jobs_df = pd.read_csv(job_roles_path)
        # Parse required skills from comma-separated strings to clean sets
        self.jobs_df["skill_set"] = self.jobs_df["required_skills"].apply(
            lambda x: {
                s.strip().lower()
                for s in str(x).split(",")
                if s.strip()
            }
        )

    def evaluate_resume(
        self, cleaned_resume_text: str, candidate_skills: List[str]
    ) -> List[Dict[str, Any]]:
        """Compares the candidate resume against all job roles in the database.

        Returns a ranked list of roles with match statistics.
        """
        candidate_skills_set = set(s.lower() for s in candidate_skills)
        all_descriptions = self.jobs_df["role_description"].tolist()

        # Step 1: Compute TF-IDF Cosine Similarity
        # Vectorize job descriptions + candidate resume together
        documents = all_descriptions + [cleaned_resume_text]
        vectorizer = TfidfVectorizer(stop_words="english")
        tfidf_matrix = vectorizer.fit_transform(documents)

        # Resume vector is the last row; job descriptions are the preceding rows
        job_vectors = tfidf_matrix[:-1]
        resume_vector = tfidf_matrix[-1:]
        cosine_sims = cosine_similarity(resume_vector, job_vectors).flatten()

        results = []

        # Step 2: Calculate Skill Coverage & Hybrid Score
        for idx, row in self.jobs_df.iterrows():
            required_skills = row["skill_set"]
            matched_skills = candidate_skills_set.intersection(required_skills)
            missing_skills = required_skills - candidate_skills_set

            coverage_ratio = (
                len(matched_skills) / len(required_skills)
                if required_skills
                else 0.0
            )
            cosine_score = float(cosine_sims[idx])

            # Hybrid Score Formula (60% Skill Coverage + 40% Semantic Similarity)
            hybrid_score = round(
                (0.6 * coverage_ratio + 0.4 * cosine_score) * 100, 2
            )

            results.append(
                {
                    "role_title": row["role_title"],
                    "category": row["category"],
                    "match_score": hybrid_score,
                    "semantic_similarity": round(cosine_score * 100, 2),
                    "skill_coverage": round(coverage_ratio * 100, 2),
                    "matched_skills": sorted(list(matched_skills)),
                    "missing_skills": sorted(list(missing_skills)),
                    "required_skills": sorted(list(required_skills)),
                    "description": row["role_description"],
                }
            )

        # Step 3: Sort roles by highest match score
        results.sort(key=lambda x: x["match_score"], reverse=True)
        return results
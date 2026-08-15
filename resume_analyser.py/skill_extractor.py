"""
src/skill_extractor.py
Extracts and categorizes technical skills from cleaned resume text.
"""

import os
import re
from typing import Dict, List, Set
import pandas as pd


class SkillExtractor:
    def __init__(self, skill_dict_path: str = "skills.csv"):
        """
        Loads skill taxonomy from CSV.
        Expected CSV format: skill_name,category
        """
        # Fallback to local path or data/ folder
        if not os.path.exists(skill_dict_path):
            alt_path = os.path.join("data", skill_dict_path)
            if os.path.exists(alt_path):
                skill_dict_path = alt_path

        self.skills_df = pd.read_csv(skill_dict_path)
        # Normalize skill names for consistent matching
        self.skills_df["skill_name"] = self.skills_df["skill_name"].str.strip().str.lower()
        self.skills_df["category"] = self.skills_df["category"].str.strip()

        # Build lookup mappings
        self.skill_to_category = dict(
            zip(self.skills_df["skill_name"], self.skills_df["category"])
        )
        
        # Sort skills by length (descending) so longer multi-word phrases match first
        # (e.g., 'power bi' matches before 'r' or 'c')
        self.skill_set = sorted(list(self.skill_to_category.keys()), key=len, reverse=True)

    def extract_skills(self, cleaned_text: str) -> Dict[str, object]:
        """
        Scans cleaned resume text for known technical skills.
        Returns:
            - 'skills_found': list of unique matched skills
            - 'categorized_skills': dictionary grouping skills by category
        """
        found_skills: Set[str] = set()

        for skill in self.skill_set:
            # Handle special symbols safely using lookarounds
            escaped_skill = re.escape(skill)
            pattern = rf"(?<!\w){escaped_skill}(?!\w)"

            if re.search(pattern, cleaned_text, flags=re.IGNORECASE):
                found_skills.add(skill)

        # Categorize detected skills
        categorized: Dict[str, List[str]] = {}
        for skill in found_skills:
            category = self.skill_to_category.get(skill, "General")
            categorized.setdefault(category, []).append(skill)

        # Sort for clean presentation
        for cat in categorized:
            categorized[cat].sort()

        return {
            "skills_found": sorted(list(found_skills)),
            "categorized_skills": categorized,
            "total_count": len(found_skills),
        }
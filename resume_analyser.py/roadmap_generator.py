"""
roadmap_generator.py
Generates phased weekly learning plans targeting identified skill gaps.
"""

from typing import Any, Dict, List


class RoadmapGenerator:

    @staticmethod
    def generate_roadmap(missing_skills: List[str]) -> List[Dict[str, Any]]:
        """Distributes missing skills across a practical 4-week learning progression."""
        if not missing_skills:
            return [
                {
                    "week": "All Set!",
                    "goal": "Skill Gap Free",
                    "focus": "Portfolio & Interview Prep",
                    "action": "All key skills are present in your resume. Focus on building real-world end-to-end projects and system design.",
                }
            ]

        # Break missing skills into weekly chunks
        total_skills = len(missing_skills)
        chunk_size = max(1, (total_skills + 3) // 4)

        weeks = [
            ("Week 1: Core Fundamentals", "Concepts & Syntax Mastery"),
            ("Week 2: Practical Integration", "Hands-on Exercises & Tooling"),
            ("Week 3: Project Implementation", "End-to-End Component Building"),
            ("Week 4: Deployment & Optimization", "Best Practices & Portfolio"),
        ]

        roadmap = []
        for i in range(4):
            start = i * chunk_size
            end = min(start + chunk_size, total_skills)
            assigned_skills = missing_skills[start:end]

            if assigned_skills:
                skills_str = ", ".join(s.title() for s in assigned_skills)
                roadmap.append(
                    {
                        "week": weeks[i][0],
                        "focus": weeks[i][1],
                        "skills": assigned_skills,
                        "action": f"Learn foundational concepts and complete mini-projects using: {skills_str}.",
                    }
                )
            else:
                # If fewer than 4 skills were missing, dedicate remaining weeks to review
                roadmap.append(
                    {
                        "week": weeks[i][0],
                        "focus": "Review & Capstone Project",
                        "skills": [],
                        "action": "Consolidate learning by building a complete capstone project integrating newly acquired skills.",
                    }
                )

        return roadmap
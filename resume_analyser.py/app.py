"""
app.py
AI Resume Analyzer & Job Recommendation System
Galactic Nebula & Cyber-Aesthetic Edition
"""

import io
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Custom NLP & Matcher modules
from job_matcher import JobMatcher
from resume_parser import parse_resume
from roadmap_generator import RoadmapGenerator
from skill_extractor import SkillExtractor
from text_cleaner import clean_text

# --- Page Configuration ---
st.set_page_config(
    page_title="ASTRA // AI Resume Telemetry",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Cosmic Galactic CSS Styling ---
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800&family=Space+Grotesk:wght@400;600;700&display=swap');

    /* Global Dark Space Canvas */
    .stApp {
        background: radial-gradient(circle at 20% 15%, #130b29 0%, #08071a 45%, #030208 100%);
        font-family: 'Outfit', sans-serif;
        color: #E2E8F0;
    }

    /* Sidebar Nebula Styling */
    [data-testid="stSidebar"] {
        background: rgba(10, 8, 26, 0.85);
        backdrop-filter: blur(16px);
        border-right: 1px solid rgba(139, 92, 246, 0.25);
    }

    /* Radiant Title */
    .galactic-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2.6rem;
        font-weight: 800;
        background: linear-gradient(135deg, #38BDF8 0%, #A855F7 50%, #EC4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.5px;
        margin-bottom: 0.2rem;
    }

    .galactic-subtitle {
        font-size: 1.05rem;
        color: #94A3B8;
        font-weight: 400;
        margin-bottom: 1.8rem;
    }

    /* Glassmorphic Metric Cards */
    .cosmic-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(168, 85, 247, 0.2);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37), inset 0 0 12px rgba(139, 92, 246, 0.05);
        backdrop-filter: blur(12px);
        border-radius: 16px;
        padding: 18px 22px;
        transition: all 0.3s ease-in-out;
    }
    .cosmic-card:hover {
        border-color: rgba(56, 189, 248, 0.5);
        transform: translateY(-2px);
        box-shadow: 0 12px 40px 0 rgba(14, 165, 233, 0.2);
    }
    .card-label {
        font-size: 0.82rem;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        color: #94A3B8;
        margin-bottom: 4px;
    }
    .card-value {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.8rem;
        font-weight: 700;
        color: #F8FAFC;
    }

    /* Glowing Skill Chips */
    .chip-found {
        display: inline-block;
        background: rgba(16, 185, 129, 0.12);
        color: #34D399;
        border: 1px solid rgba(52, 211, 153, 0.35);
        box-shadow: 0 0 10px rgba(52, 211, 153, 0.15);
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 4px;
    }
    .chip-missing {
        display: inline-block;
        background: rgba(244, 63, 94, 0.12);
        color: #FB7185;
        border: 1px solid rgba(251, 113, 133, 0.35);
        box-shadow: 0 0 10px rgba(251, 113, 133, 0.15);
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 4px;
    }

    /* Roadmap Timeline Box */
    .roadmap-node {
        background: rgba(15, 23, 42, 0.55);
        border: 1px solid rgba(56, 189, 248, 0.2);
        border-left: 4px solid #38BDF8;
        border-radius: 12px;
        padding: 16px 20px;
        margin-bottom: 14px;
        backdrop-filter: blur(8px);
    }
    .node-week {
        font-family: 'Space Grotesk', sans-serif;
        color: #38BDF8;
        font-weight: 700;
        font-size: 1.1rem;
        margin-bottom: 3px;
    }
    .node-focus {
        color: #E2E8F0;
        font-weight: 600;
        font-size: 0.95rem;
        margin-bottom: 6px;
    }
    .node-desc {
        color: #94A3B8;
        font-size: 0.88rem;
        line-height: 1.4;
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: rgba(15, 23, 42, 0.6);
        padding: 6px;
        border-radius: 14px;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        color: #94A3B8;
        font-weight: 600;
        padding: 8px 18px;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(168, 85, 247, 0.3), rgba(56, 189, 248, 0.3)) !important;
        color: #FFFFFF !important;
        border: 1px solid rgba(56, 189, 248, 0.4) !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# --- Load Engines Safely ---
@st.cache_resource
def load_engines():
    return SkillExtractor("skills.csv"), JobMatcher("job_roles.csv")


try:
    skill_extractor, job_matcher = load_engines()
except Exception as e:
    st.error(f"⚠️ Engine Initialization Failure: {e}")
    st.stop()

# --- Header ---
st.markdown(
    '<div class="galactic-title">✨ ASTRA // AI RESUME INTELLIGENCE</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="galactic-subtitle">Neural resume decomposition, hybrid role benchmarking, and orbital career roadmaps.</div>',
    unsafe_allow_html=True,
)

# --- Sidebar ---
with st.sidebar:
    st.markdown("### 🛰️ Resume Telemetry")
    uploaded_file = st.file_uploader(
        "Upload Candidate Resume (PDF/DOCX)",
        type=["pdf", "docx"],
        help="Protected sandbox environment. Documents are parsed purely in-memory.",
    )

    st.markdown("---")
    st.markdown("### 🎯 Mission Orbit")
    role_options = ["Autonomous Match (All Sectors)"] + list(
        job_matcher.jobs_df["role_title"]
    )
    selected_target = st.selectbox("Benchmark Target Role", options=role_options)

    st.markdown("---")
    st.markdown(
        """
        <div style="font-size: 0.8rem; color: #64748B;">
        <b>Engine Specs:</b><br>
        • Vector Model: TF-IDF Sublinear<br>
        • Similarity: Cosine Angle Metric<br>
        • Skill Weights: Lookaround Regex Matrix
        </div>
        """,
        unsafe_allow_html=True,
    )

# --- Main Application State ---
if uploaded_file is None:
    st.markdown(
        """
        <div style="text-align: center; padding: 60px 20px; border: 1px dashed rgba(168, 85, 247, 0.3); border-radius: 20px; background: rgba(15, 23, 42, 0.3);">
            <div style="font-size: 3rem; margin-bottom: 10px;">🌌</div>
            <h3 style="color: #F8FAFC; margin-bottom: 6px;">No Resume in Orbit</h3>
            <p style="color: #94A3B8; max-width: 500px; margin: 0 auto 20px auto;">
                Drop a PDF or DOCX file into the left sidebar console to trigger neural extraction, calculate vector match distances, and generate personalized skill roadmaps.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("🔭 Inspect Supported Orbital Roles Database"):
        st.dataframe(
            job_matcher.jobs_df[["role_title", "category", "required_skills"]],
            use_container_width=True,
        )

else:
    file_ext = uploaded_file.name.split(".")[-1].lower()

    with st.spinner("⚡ Decoding document stream and vectorizing tokens..."):
        try:
            file_bytes = io.BytesIO(uploaded_file.read())
            raw_text = parse_resume(file_bytes, file_ext)
            cleaned_resume = clean_text(raw_text)
        except Exception as e:
            st.error(f"Ingestion Error: {str(e)}")
            st.stop()

    if not cleaned_resume.strip():
        st.warning("⚠️ Extracted stream is empty. Check if document is an unparsed image scan.")
        st.stop()

    # Run Analysis Engines
    extraction = skill_extractor.extract_skills(cleaned_resume)
    candidate_skills = extraction["skills_found"]
    categorized_skills = extraction["categorized_skills"]

    all_evaluations = job_matcher.evaluate_resume(cleaned_resume, candidate_skills)

    if selected_target == "Autonomous Match (All Sectors)":
        focus_role = all_evaluations[0]
    else:
        focus_role = next(
            (r for r in all_evaluations if r["role_title"] == selected_target),
            all_evaluations[0],
        )

    # --- Top KPI Hologram Cards ---
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(
            f"""
            <div class="cosmic-card">
                <div class="card-label">Target Role</div>
                <div class="card-value" style="font-size: 1.3rem; color: #38BDF8;">{focus_role['role_title']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            f"""
            <div class="cosmic-card">
                <div class="card-label">Match Score</div>
                <div class="card-value" style="color: #A855F7;">{focus_role['match_score']}%</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col3:
        st.markdown(
            f"""
            <div class="cosmic-card">
                <div class="card-label">Skills Verified</div>
                <div class="card-value" style="color: #34D399;">{len(focus_role['matched_skills'])} <span style="font-size: 1rem; color:#64748B;">/ {len(focus_role['required_skills'])}</span></div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col4:
        st.markdown(
            f"""
            <div class="cosmic-card">
                <div class="card-label">Identified Gaps</div>
                <div class="card-value" style="color: #FB7185;">{len(focus_role['missing_skills'])}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # --- Interactive Visualisation Tabs ---
    tab_matrix, tab_radar, tab_gaps, tab_roadmap, tab_raw = st.tabs(
        [
            "📊 Sector Alignment",
            "🕸️ Neural Radar",
            "🔮 Skill Spectrum",
            "🚀 Launch Roadmap",
            "📜 Document Telemetry",
        ]
    )

    # Tab 1: Horizontal Cosmic Bar Chart
    with tab_matrix:
        c_chart, c_top = st.columns([1.3, 1])
        with c_chart:
            st.markdown("#### 🌌 Sector Compatibility Vector")

            chart_data = pd.DataFrame(all_evaluations)[
                ["role_title", "match_score", "skill_coverage", "semantic_similarity"]
            ].sort_values(by="match_score", ascending=True)

            fig_bar = go.Figure()
            fig_bar.add_trace(
                go.Bar(
                    x=chart_data["match_score"],
                    y=chart_data["role_title"],
                    orientation="h",
                    text=[f"{val}%" for val in chart_data["match_score"]],
                    textposition="outside",
                    marker=dict(
                        color=chart_data["match_score"],
                        colorscale=[[0, "#4C1D95"], [0.5, "#8B5CF6"], [1, "#38BDF8"]],
                        line=dict(color="rgba(255, 255, 255, 0.2)", width=1),
                    ),
                    hoverinfo="x+y",
                )
            )

            fig_bar.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=20, r=40, t=10, b=10),
                height=340,
                font=dict(family="Outfit", color="#94A3B8"),
                xaxis=dict(
                    showgrid=True,
                    gridcolor="rgba(255,255,255,0.06)",
                    range=[0, 115],
                    zeroline=False,
                ),
                yaxis=dict(showgrid=False),
            )
            st.plotly_chart(fig_bar, use_container_width=True)

        with c_top:
            st.markdown("#### 🏆 Prime Target Roles")
            for idx, r in enumerate(all_evaluations[:3], 1):
                badge_color = "#38BDF8" if idx == 1 else "#A855F7" if idx == 2 else "#EC4899"
                st.markdown(
                    f"""
                    <div style="background: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255,255,255,0.07); border-radius: 12px; padding: 12px 16px; margin-bottom: 10px;">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <span style="font-weight: 700; color: #F8FAFC;">#{idx} {r['role_title']}</span>
                            <span style="font-family: 'Space Grotesk'; font-weight: 700; color: {badge_color};">{r['match_score']}%</span>
                        </div>
                        <div style="font-size: 0.8rem; color: #64748B; margin-top: 4px;">
                            Skill Coverage: {r['skill_coverage']}% • Context Fit: {r['semantic_similarity']}%
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    # Tab 2: Cosmic Radar Chart
    with tab_radar:
        st.markdown(f"#### 🛰️ Multi-Axis Readiness: {focus_role['role_title']}")
        
        categories = ["Skill Coverage", "Contextual Fit", "Keyword Density", "Domain Alignment"]
        scores = [
            focus_role["skill_coverage"],
            focus_role["semantic_similarity"],
            min(100, round((len(candidate_skills) / 10) * 100, 2)),
            focus_role["match_score"],
        ]

        fig_radar = go.Figure()
        fig_radar.add_trace(
            go.Scatterpolar(
                r=scores + [scores[0]],
                theta=categories + [categories[0]],
                fill="toself",
                fillcolor="rgba(168, 85, 247, 0.25)",
                line=dict(color="#38BDF8", width=2),
                marker=dict(size=7, color="#A855F7"),
            )
        )

        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100],
                    gridcolor="rgba(255, 255, 255, 0.1)",
                    linecolor="rgba(255, 255, 255, 0.1)",
                    tickfont=dict(color="#64748B"),
                ),
                angularaxis=dict(
                    gridcolor="rgba(255, 255, 255, 0.1)",
                    linecolor="rgba(255, 255, 255, 0.1)",
                    tickfont=dict(color="#E2E8F0", size=11, family="Outfit"),
                ),
                bgcolor="rgba(0,0,0,0)",
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            height=380,
            margin=dict(l=40, r=40, t=20, b=20),
        )
        st.plotly_chart(fig_radar, use_container_width=True)

    # Tab 3: Skill Spectrum & Gaps
    with tab_gaps:
        col_g1, col_g2 = st.columns(2)
        with col_g1:
            st.markdown(f"##### 🟢 Verified Assets for {focus_role['role_title']}")
            if focus_role["matched_skills"]:
                chips = "".join(
                    [f'<span class="chip-found">✦ {s.title()}</span>' for s in focus_role["matched_skills"]]
                )
                st.markdown(chips, unsafe_allow_html=True)
            else:
                st.write("No matching role-specific skills found in resume.")

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("##### 🌐 All Detected Resume Skills")
            for cat, s_list in categorized_skills.items():
                st.markdown(
                    f"<div style='font-size:0.85rem; color:#94A3B8; margin-bottom:4px;'><strong style='color:#E2E8F0;'>{cat}:</strong> {', '.join([s.title() for s in s_list])}</div>",
                    unsafe_allow_html=True,
                )

        with col_g2:
            st.markdown(f"##### 🔴 Skill Gaps (Target: {focus_role['role_title']})")
            if focus_role["missing_skills"]:
                chips_missing = "".join(
                    [f'<span class="chip-missing">⚠ {s.title()}</span>' for s in focus_role["missing_skills"]]
                )
                st.markdown(chips_missing, unsafe_allow_html=True)
                st.markdown(
                    "<p style='color: #64748B; font-size: 0.85rem; margin-top: 12px;'>Integrating projects or certifications with these skills directly raises the hybrid match score.</p>",
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    "<div style='color:#34D399; font-weight:600;'>✨ 100% Skill Coverage Achieved!</div>",
                    unsafe_allow_html=True,
                )

    # Tab 4: 4-Week Launch Roadmap
    with tab_roadmap:
        st.markdown(f"#### 🛰️ Orbital Upskilling Trajectory for {focus_role['role_title']}")
        roadmap = RoadmapGenerator.generate_roadmap(focus_role["missing_skills"])

        for step in roadmap:
            st.markdown(
                f"""
                <div class="roadmap-node">
                    <div class="node-week">{step['week']}</div>
                    <div class="node-focus">🎯 {step['focus']}</div>
                    <div class="node-desc">{step['action']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # Tab 5: Raw Cleaned Text
    with tab_raw:
        st.markdown("#### 📄 Document Stream Telemetry")
        st.text_area(
            "Normalized & Token-Preserved Stream",
            cleaned_resume,
            height=240,
            disabled=True,
        )
import plotly.graph_objects as go
import plotly.express as px


def create_ats_gauge(ats_score: float) -> go.Figure:
    """
    Create a gauge chart showing the ATS score (0-100).
    Like a speedometer — instantly shows how good the score is.
    """
    if ats_score >= 80:
        color = "#2ecc71"
    elif ats_score >= 60:
        color = "#3498db"
    elif ats_score >= 40:
        color = "#f39c12"
    else:
        color = "#e74c3c"

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=ats_score,
        title={"text": "ATS Score", "font": {"size": 20}},
        number={"suffix": "/100", "font": {"size": 28}},
        gauge={
            "axis": {"range": [0, 100], "tickwidth": 1},
            "bar": {"color": color},
            "steps": [
                {"range": [0, 40],  "color": "#fadbd8"},
                {"range": [40, 60], "color": "#fdebd0"},
                {"range": [60, 80], "color": "#d6eaf8"},
                {"range": [80, 100],"color": "#d5f5e3"},
            ],
            "threshold": {
                "line": {"color": color, "width": 4},
                "thickness": 0.75,
                "value": ats_score,
            },
        },
    ))

    fig.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        font={"color": "white"},
    )
    return fig


def create_score_breakdown_chart(breakdown: dict) -> go.Figure:
    """
    Create a horizontal bar chart showing score breakdown.
    Shows how much each component contributes to the final score.
    """
    categories = [
        "Skill Match (50%)",
        "Text Similarity (40%)",
        "Keyword Score (10%)",
    ]
    values = [
        breakdown["skill_match_contribution"],
        breakdown["similarity_contribution"],
        breakdown["keyword_contribution"],
    ]
    colors = ["#2ecc71", "#3498db", "#9b59b6"]

    fig = go.Figure(go.Bar(
        x=values,
        y=categories,
        orientation="h",
        marker_color=colors,
        text=[f"{v}" for v in values],
        textposition="outside",
    ))

    fig.update_layout(
        title="Score Breakdown",
        xaxis_title="Points Contributed",
        xaxis={"range": [0, 55]},
        height=250,
        margin=dict(l=20, r=60, t=40, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"color": "white"},
    )
    return fig


def create_skill_match_chart(
        matched: list,
        missing: list,
        extra: list,
) -> go.Figure:
    """
    Create a donut chart showing skill distribution.
    Instantly shows the ratio of matched vs missing vs extra skills.
    """
    labels = ["Matched Skills", "Missing Skills", "Extra Skills"]
    values = [len(matched), len(missing), len(extra)]
    colors = ["#2ecc71", "#e74c3c", "#3498db"]

    # Avoid empty chart if all zeros
    if sum(values) == 0:
        values = [1, 1, 1]

    fig = go.Figure(go.Pie(
        labels=labels,
        values=values,
        hole=0.5,
        marker_colors=colors,
        textinfo="label+percent",
        hoverinfo="label+value",
    ))

    fig.update_layout(
        title="Skill Distribution",
        height=320,
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        font={"color": "white"},
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5,
        ),
    )
    return fig


def create_keyword_bar_chart(resume_text: str, jd_text: str) -> go.Figure:
    """
    Create a bar chart comparing top keyword frequencies
    between resume and job description.
    """
    from sklearn.feature_extraction.text import TfidfVectorizer
    import numpy as np

    if not resume_text or not jd_text:
        return go.Figure()

    try:
        vectorizer = TfidfVectorizer(
            stop_words="english",
            max_features=10,
        )
        vectorizer.fit([jd_text])
        feature_names = vectorizer.get_feature_names_out()

        resume_vec = vectorizer.transform([resume_text]).toarray()[0]
        jd_vec = vectorizer.transform([jd_text]).toarray()[0]

        fig = go.Figure()
        fig.add_trace(go.Bar(
            name="Job Description",
            x=feature_names,
            y=jd_vec,
            marker_color="#3498db",
        ))
        fig.add_trace(go.Bar(
            name="Your Resume",
            x=feature_names,
            y=resume_vec,
            marker_color="#2ecc71",
        ))

        fig.update_layout(
            title="Top Keywords: JD vs Resume",
            barmode="group",
            xaxis_title="Keywords",
            yaxis_title="TF-IDF Score",
            height=320,
            margin=dict(l=20, r=20, t=40, b=80),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font={"color": "white"},
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.4,
                xanchor="center",
                x=0.5,
            ),
        )
        return fig

    except Exception as e:
        print(f"[visualizer.py] Error: {e}")
        return go.Figure()

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path
from html import escape

# =====================================================
# IPL PERFORMANCE ANALYTICS
# BLACK AND GOLD STATISTICAL EDITION
# =====================================================

st.set_page_config(
    page_title="IPL Performance Analytics",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="collapsed"
)

GOLD = "#FFC94A"
BLUE = "#21B9FF"
PURPLE = "#9164FF"
GREEN = "#28DC8A"
RED = "#FF5B72"
WHITE = "#F5F7FF"

STATES = ["Strong", "Stable", "Weak"]

STATE_COLORS = {
    "Strong": GREEN,
    "Stable": BLUE,
    "Weak": RED
}

TEAM_CODES = {
    "Chennai Super Kings": "CSK",
    "Delhi Capitals": "DC",
    "Gujarat Titans": "GT",
    "Kolkata Knight Riders": "KKR",
    "Lucknow Super Giants": "LSG",
    "Mumbai Indians": "MI",
    "Punjab Kings": "PBKS",
    "Rajasthan Royals": "RR",
    "Royal Challengers Bengaluru": "RCB",
    "Sunrisers Hyderabad": "SRH"
}

TEAM_COLORS = {
    "CSK": "#FFE13B",
    "DC": "#3C9EFF",
    "GT": "#72C6E8",
    "KKR": "#B58AFF",
    "LSG": "#65D8FF",
    "MI": "#3F83FF",
    "PBKS": "#FF5969",
    "RR": "#F48CC8",
    "RCB": "#FF4242",
    "SRH": "#FF9C42"
}

# =====================================================
# CUSTOM DESIGN
# =====================================================

st.markdown("""
<style>
.stApp {
    background:
        radial-gradient(
            ellipse at 50% 5%,
            rgba(20, 65, 130, 0.32),
            transparent 45%
        ),
        radial-gradient(
            ellipse at 85% 75%,
            rgba(75, 25, 150, 0.16),
            transparent 40%
        ),
        #030710;
    color: #F5F7FF;
}

.block-container {
    max-width: 1450px;
    padding-top: 1.2rem;
    padding-bottom: 2rem;
}

header[data-testid="stHeader"] {
    background: transparent;
}

h1, h2, h3 {
    color: white !important;
}

p, label {
    color: #DDE8F7;
}

.brand-header {
    padding: 20px 25px;
    background: rgba(3, 11, 25, 0.94);
    border: 1px solid #285183;
    border-radius: 15px;
    margin-bottom: 15px;
    box-shadow: 0 0 30px rgba(25, 105, 255, 0.12);
}

.brand-title {
    color: #FFC94A;
    font-size: clamp(25px, 3vw, 39px);
    font-weight: 900;
    font-style: italic;
}

.brand-subtitle {
    color: #B4C6E0;
    font-size: 13px;
}

.hero {
    position: relative;
    overflow: hidden;
    min-height: 400px;
    border: 1px solid #285183;
    border-radius: 20px;
    padding: 30px;
    text-align: center;
    background:
        radial-gradient(
            ellipse at 50% 100%,
            rgba(50, 70, 190, 0.35),
            transparent 50%
        ),
        linear-gradient(
            135deg,
            #07172F,
            #02060F 55%,
            #0B0924
        );
    box-shadow: 0 15px 50px rgba(0, 0, 0, 0.45);
}

.hero-kicker {
    color: #21B9FF;
    font-size: 13px;
    font-weight: 800;
    letter-spacing: 3px;
}

.hero-title {
    color: white;
    font-size: clamp(38px, 5vw, 75px);
    font-weight: 900;
    font-style: italic;
    line-height: 1.05;
    margin: 18px 0;
}

.hero-title span {
    color: #FFC94A;
}

.hero-description {
    color: #D5E1F5;
    font-size: 17px;
    margin: 15px 0;
}

.hero-formulas {
    display: flex;
    justify-content: space-between;
    gap: 20px;
    color: #A9BBE1;
    font-size: 14px;
    margin-bottom: 25px;
}

.cricket-art {
    font-size: 60px;
    margin: 12px 0;
    filter: drop-shadow(
        0 0 18px rgba(255, 201, 74, 0.4)
    );
}

.small-note {
    color: #AABBD2;
    font-size: 12px;
    letter-spacing: 1px;
}

.data-strip {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    margin-top: 18px;
}

.data-item {
    background: rgba(9, 24, 49, 0.92);
    border: 1px solid #214873;
    border-radius: 12px;
    padding: 17px;
    text-align: center;
}

.data-number {
    color: #FFC94A;
    font-size: 34px;
    font-weight: 900;
}

.data-label {
    color: #AABBD2;
    font-size: 12px;
}

.section-head {
    color: #FFC94A;
    font-size: 27px;
    font-weight: 900;
    margin: 22px 0 12px;
    border-bottom: 1px solid #244268;
    padding-bottom: 8px;
}

.team-banner {
    padding: 20px;
    border: 1px solid #2C5688;
    border-radius: 15px;
    background: linear-gradient(
        115deg,
        rgba(12, 35, 70, 0.96),
        rgba(5, 12, 28, 0.96)
    );
    margin: 12px 0;
}

.team-banner-name {
    font-size: 37px;
    font-weight: 900;
    color: white;
}

[data-testid="stMetric"] {
    background: linear-gradient(
        140deg,
        #101E36,
        #07111F
    );
    border: 1px solid #264D78;
    border-radius: 12px;
    padding: 15px;
}

[data-testid="stMetricLabel"] {
    color: #AABBD2;
}

[data-testid="stMetricValue"] {
    color: #FFC94A;
}

[data-testid="stPlotlyChart"] {
    background: rgba(8, 18, 36, 0.88);
    border: 1px solid #244875;
    border-radius: 13px;
    padding: 5px;
}

[data-testid="stSelectbox"] {
    background: rgba(8, 18, 36, 0.9);
    border: 1px solid #325C8D;
    border-radius: 10px;
    padding: 8px;
}

div.stButton > button[kind="primary"] {
    background: linear-gradient(
        100deg,
        #FFD96B,
        #FFB828
    );
    color: #07101F;
    font-weight: 900;
    border: none;
    border-radius: 10px;
}

div.stButton > button[kind="secondary"] {
    background: #0C1930;
    border: 1px solid #36577C;
    color: #E8F1FF;
    border-radius: 10px;
}

.stDownloadButton button {
    background: #FFC94A;
    color: #07101F;
    font-weight: 800;
}

.form-chip {
    display: inline-block;
    padding: 8px 14px;
    margin: 4px;
    border-radius: 8px;
    color: #06101B;
    font-weight: 900;
    font-size: 17px;
}

@media(max-width: 750px) {
    .hero {
        padding: 20px 12px;
    }

    .hero-formulas {
        flex-direction: column;
    }

    .data-strip {
        grid-template-columns: repeat(2, 1fr);
    }
}
</style>
""", unsafe_allow_html=True)

# =====================================================
# LOAD DATA
# =====================================================

@st.cache_data
def load_data():
    base = Path("data/processed")

    performance = pd.read_csv(
        base / "team_performance.csv"
    )

    matches = pd.read_csv(
        base / "ipl_matches.csv"
    )

    team_matches = pd.read_csv(
        base / "team_matches.csv"
    )

    history = pd.read_csv(
        base / "team_state_history.csv"
    )

    matrix = pd.read_csv(
        base / "transition_matrix.csv",
        index_col=0
    )

    return (
        performance,
        matches,
        team_matches,
        history,
        matrix
    )


try:
    (
        performance,
        matches,
        team_matches,
        history,
        matrix
    ) = load_data()

except FileNotFoundError as error:
    st.error(f"Missing CSV file: {error}")
    st.stop()

team_matches["date"] = pd.to_datetime(
    team_matches["date"]
)

history["date"] = pd.to_datetime(
    history["date"]
)

matrix = matrix.reindex(
    index=STATES,
    columns=STATES,
    fill_value=0
).fillna(0)

teams = sorted(performance["team"].unique())

# =====================================================
# HELPER FUNCTIONS
# =====================================================

def style_chart(fig, height=400):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            color=WHITE,
            size=12
        ),
        height=height,
        margin=dict(
            l=40,
            r=20,
            t=65,
            b=40
        )
    )

    fig.update_xaxes(
        gridcolor="rgba(100,150,220,0.10)"
    )

    fig.update_yaxes(
        gridcolor="rgba(100,150,220,0.15)"
    )

    return fig


def section(title):
    st.markdown(
        f'<div class="section-head">{escape(title)}</div>',
        unsafe_allow_html=True
    )


# =====================================================
# NAVIGATION
# =====================================================

if "page" not in st.session_state:
    st.session_state.page = "Overview"

st.markdown("""
<div class="brand-header">
<div class="brand-title">
🏏 IPL PERFORMANCE ANALYTICS
</div>
<div class="brand-subtitle">
TEAM PERFORMANCE · MARKOV STATE MODELLING ·
STATISTICAL ANALYSIS · 2022–2025
</div>
</div>
""", unsafe_allow_html=True)

pages = [
    "Overview",
    "Team Analysis",
    "Markov Model",
    "Comparisons",
    "Methodology"
]

nav_cols = st.columns(5)

for col, page in zip(nav_cols, pages):
    with col:
        if st.button(
            page,
            key=f"nav_{page}",
            width="stretch",
            type=(
                "primary"
                if st.session_state.page == page
                else "secondary"
            )
        ):
            st.session_state.page = page
            st.rerun()

# =====================================================
# OVERVIEW PAGE
# =====================================================

if st.session_state.page == "Overview":

    # IMPORTANT:
    # HTML is not indented inside triple quotes.
    # This prevents Streamlit displaying raw HTML.

    st.markdown("""
<div class="hero">
<div class="hero-formulas">
<span>P(i → j) = N(i,j) / Σ N(i,k)</span>
<span>WIN RATE = WINS / MATCHES × 100</span>
</div>

<div class="cricket-art">🏏 🏆 📊</div>

<div class="hero-kicker">
CRICKET MEETS PROBABILITY
</div>

<div class="hero-title">
<span>IPL</span> PERFORMANCE
ANALYTICS
</div>

<div class="hero-description">
Team Performance & Markov State Modelling (2022–2025)
</div>

<div class="small-note">
REAL MATCH DATA · STATISTICAL INSIGHTS ·
HISTORICAL STATE TRANSITIONS
</div>
</div>
""", unsafe_allow_html=True)

    left, middle, right = st.columns([2, 1, 2])

    with middle:
        if st.button(
            "GET STARTED →",
            type="primary",
            width="stretch",
            key="get_started"
        ):
            st.session_state.page = "Team Analysis"
            st.rerun()

    st.markdown(f"""
<div class="data-strip">
<div class="data-item">
<div class="data-number">{len(matches)}</div>
<div class="data-label">IPL MATCHES</div>
</div>

<div class="data-item">
<div class="data-number">{len(teams)}</div>
<div class="data-label">TEAMS</div>
</div>

<div class="data-item">
<div class="data-number">{matches["season"].nunique()}</div>
<div class="data-label">SEASONS</div>
</div>

<div class="data-item">
<div class="data-number">{len(history)}</div>
<div class="data-label">STATE RECORDS</div>
</div>
</div>
""", unsafe_allow_html=True)

    section("PROJECT RESEARCH FOCUS")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.info(
            "🏏 TEAM PERFORMANCE\n\n"
            "Analyze wins, losses, batting runs "
            "and recent team form."
        )

    with c2:
        st.info(
            "🔄 MARKOV MODELLING\n\n"
            "Study transitions between Strong, "
            "Stable and Weak performance states."
        )

    with c3:
        st.info(
            "📊 STATISTICAL COMPARISON\n\n"
            "Compare IPL franchises using "
            "historical performance metrics."
        )

# =====================================================
# TEAM ANALYSIS PAGE
# =====================================================

elif st.session_state.page == "Team Analysis":

    section("TEAM PERFORMANCE LAB")

    selected_team = st.selectbox(
        "Select IPL Franchise",
        teams,
        key="team_selector"
    )

    team = performance[
        performance["team"] == selected_team
    ].iloc[0]

    code = TEAM_CODES.get(selected_team, "")
    team_color = TEAM_COLORS.get(code, GOLD)

    st.markdown(f"""
<div class="team-banner"
style="border-left:6px solid {team_color}">
<div style="color:{team_color};font-weight:800">
{escape(code)} / TEAM INTELLIGENCE
</div>
<div class="team-banner-name">
{escape(selected_team.upper())}
</div>
<div style="color:#B5C7DF">
HISTORICAL IPL PERFORMANCE · 2022–2025
</div>
</div>
""", unsafe_allow_html=True)

    a, b, c, d = st.columns(4)

    a.metric(
        "MATCHES",
        int(team["matches"])
    )

    b.metric(
        "VICTORIES",
        int(team["wins"])
    )

    c.metric(
        "WIN RATE",
        f'{team["win_rate"]:.2f}%'
    )

    d.metric(
        "AVERAGE RUNS",
        f'{team["average_runs"]:.2f}'
    )

    section("RECENT FIVE-MATCH FORM")

    left, right = st.columns(2)

    with left:
        form_html = ""

        for result in str(team["recent_form"]):
            color = GREEN if result == "W" else RED

            form_html += (
                f'<span class="form-chip" '
                f'style="background:{color}">'
                f'{escape(result)}</span>'
            )

        st.markdown(
            form_html,
            unsafe_allow_html=True
        )

    with right:
        a, b = st.columns(2)

        a.metric(
            "RECENT WIN RATE",
            f'{team["recent_win_rate"]:.1f}%'
        )

        b.metric(
            "CURRENT STATE",
            str(team["current_state"])
        )

    section("SEASON-WISE PERFORMANCE")

    subset = team_matches[
        team_matches["team"] == selected_team
    ].copy()

    subset["result"] = (
        subset["result"].astype(str).str.lower()
    )

    subset = subset[
        subset["result"].isin(["win", "loss"])
    ]

    seasons = (
        subset.groupby("season")
        .agg(
            matches=("result", "size"),
            wins=("won", "sum")
        )
        .reset_index()
    )

    seasons["win_rate"] = (
        seasons["wins"]
        / seasons["matches"]
        * 100
    )

    seasons["season"] = (
        seasons["season"].astype(str)
    )

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=seasons["season"],
            y=seasons["win_rate"],
            mode="lines+markers+text",
            line=dict(
                color=GOLD,
                width=4
            ),
            marker=dict(
                size=12,
                color=BLUE
            ),
            text=[
                f"{x:.1f}%"
                for x in seasons["win_rate"]
            ],
            textposition="top center"
        )
    )

    fig.update_layout(
        title=f"{code} Season-wise Win Rate",
        yaxis_range=[0, 105],
        xaxis_title="IPL Season",
        yaxis_title="Win Rate (%)"
    )

    style_chart(fig)

    st.plotly_chart(
        fig,
        width="stretch",
        key="season_chart"
    )

# =====================================================
# MARKOV MODEL PAGE
# =====================================================

elif st.session_state.page == "Markov Model":

    section("MARKOV STATE TRANSITION ENGINE")

    st.write(
        "The Markov model estimates historical "
        "transitions between Strong, Stable and "
        "Weak performance states using rolling "
        "five-match win rates within each season."
    )

    fig = go.Figure(
        go.Heatmap(
            z=matrix.values,
            x=STATES,
            y=STATES,
            zmin=0,
            zmax=1,
            colorscale=[
                [0, "#08142A"],
                [0.5, "#1659A6"],
                [1, "#21B9FF"]
            ],
            text=[
                [f"{v:.1%}" for v in row]
                for row in matrix.values
            ],
            texttemplate="%{text}",
            textfont=dict(
                size=20,
                color="white"
            ),
            hovertemplate=(
                "Current: %{y}<br>"
                "Next: %{x}<br>"
                "Probability: %{z:.1%}"
                "<extra></extra>"
            )
        )
    )

    fig.update_layout(
        title="Historical Transition Probability Matrix",
        xaxis_title="Next State",
        yaxis_title="Current State"
    )

    style_chart(fig, 460)

    st.plotly_chart(
        fig,
        width="stretch",
        key="markov_heatmap"
    )

    section("NEXT-STATE PROBABILITY EXPLORER")

    current_state = st.selectbox(
        "Choose Current State",
        STATES,
        key="state_selector"
    )

    probabilities = matrix.loc[current_state]

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "NEXT: STRONG",
        f'{probabilities["Strong"]:.1%}'
    )

    c2.metric(
        "NEXT: STABLE",
        f'{probabilities["Stable"]:.1%}'
    )

    c3.metric(
        "NEXT: WEAK",
        f'{probabilities["Weak"]:.1%}'
    )

    fig_prob = go.Figure(
        go.Bar(
            x=STATES,
            y=[
                probabilities[state] * 100
                for state in STATES
            ],
            marker_color=[
                STATE_COLORS[state]
                for state in STATES
            ],
            text=[
                f"{probabilities[state]:.1%}"
                for state in STATES
            ],
            textposition="outside"
        )
    )

    fig_prob.update_layout(
        title=f"Next-State Probabilities | {current_state}",
        yaxis_range=[0, 105],
        yaxis_title="Probability (%)"
    )

    style_chart(fig_prob, 340)

    st.plotly_chart(
        fig_prob,
        width="stretch",
        key="probability_chart"
    )

    st.caption(
        "These are historical pooled probabilities, "
        "not guaranteed future predictions."
    )

# =====================================================
# COMPARISONS PAGE
# =====================================================

elif st.session_state.page == "Comparisons":

    section("IPL TEAM COMPARISON CENTER")

    comparison = performance.sort_values(
        "win_rate",
        ascending=False
    ).copy()

    comparison["code"] = comparison["team"].map(
        TEAM_CODES
    )

    fig = go.Figure(
        go.Bar(
            x=comparison["code"],
            y=comparison["win_rate"],
            marker_color=[
                TEAM_COLORS.get(code, BLUE)
                for code in comparison["code"]
            ],
            text=[
                f"{v:.1f}%"
                for v in comparison["win_rate"]
            ],
            textposition="outside",
            customdata=comparison["team"],
            hovertemplate=(
                "%{customdata}<br>"
                "Win Rate: %{y:.2f}%"
                "<extra></extra>"
            )
        )
    )

    fig.update_layout(
        title="IPL Team Win Rate Rankings | 2022–2025",
        yaxis_range=[0, 80],
        yaxis_title="Win Rate (%)"
    )

    style_chart(fig, 470)

    st.plotly_chart(
        fig,
        width="stretch",
        key="comparison_chart"
    )

    section("TWO-TEAM STATISTICAL COMPARISON")

    a, b = st.columns(2)

    with a:
        team_a = st.selectbox(
            "Team A",
            teams,
            index=0,
            key="compare_a"
        )

    with b:
        team_b = st.selectbox(
            "Team B",
            teams,
            index=1,
            key="compare_b"
        )

    if team_a == team_b:
        st.warning("Please select two different teams.")

    else:
        row_a = performance[
            performance["team"] == team_a
        ].iloc[0]

        row_b = performance[
            performance["team"] == team_b
        ].iloc[0]

        metrics = [
            "Win Rate (%)",
            "Average Runs",
            "Recent Win Rate (%)"
        ]

        values_a = [
            float(row_a["win_rate"]),
            float(row_a["average_runs"]),
            float(row_a["recent_win_rate"])
        ]

        values_b = [
            float(row_b["win_rate"]),
            float(row_b["average_runs"]),
            float(row_b["recent_win_rate"])
        ]

        fig_compare = go.Figure()

        fig_compare.add_trace(
            go.Bar(
                name=TEAM_CODES.get(team_a, team_a),
                x=metrics,
                y=values_a,
                marker_color=GOLD
            )
        )

        fig_compare.add_trace(
            go.Bar(
                name=TEAM_CODES.get(team_b, team_b),
                x=metrics,
                y=values_b,
                marker_color=BLUE
            )
        )

        fig_compare.update_layout(
            title="Team Statistical Profile Comparison",
            barmode="group",
            showlegend=True
        )

        style_chart(fig_compare, 400)

        st.plotly_chart(
            fig_compare,
            width="stretch",
            key="head_to_head_chart"
        )

        st.caption(
            "This chart compares overall team "
            "statistics, not just direct meetings."
        )

    section("TEAM PERFORMANCE TABLE")

    st.dataframe(
        comparison[
            [
                "team",
                "matches",
                "wins",
                "losses",
                "win_rate",
                "average_runs",
                "recent_win_rate",
                "current_state"
            ]
        ],
        width="stretch",
        hide_index=True
    )

# =====================================================
# METHODOLOGY PAGE
# =====================================================

elif st.session_state.page == "Methodology":

    section("STATISTICAL RESEARCH METHODOLOGY")

    st.markdown("""
### 1. Data Source

Historical IPL match records from Cricsheet,
covering the selected seasons 2022–2025.

### 2. Win Percentage

**Win Rate = (Wins / Decisive Matches) × 100**

### 3. Recent Performance

The latest five decisive matches determine
the team's current performance state.

### 4. State Classification

- **Strong:** Win rate at least 60%
- **Stable:** Win rate 40% to below 60%
- **Weak:** Win rate below 40%

### 5. Markov Transition Probability

**P(i → j) = N(i,j) / Σ N(i,k)**

N(i,j) represents the observed number
of transitions from state i to state j.

### 6. Season Boundaries

Rolling five-match windows reset at
the beginning of each season.

### 7. Exclusions

Tied and no-result matches are excluded
from the win/loss-based state model.

### 8. Interpretation

The transition matrix contains historical
empirical probabilities, not guaranteed
future predictions.
""")

    section("TRANSITION PROBABILITY TABLE")

    st.dataframe(
        matrix.style.format("{:.1%}"),
        width="stretch"
    )

    section("EXPORT PERFORMANCE DATA")

    st.download_button(
        "DOWNLOAD TEAM PERFORMANCE CSV",
        data=performance.to_csv(index=False),
        file_name="ipl_team_performance.csv",
        mime="text/csv",
        key="download_csv"
    )

# =====================================================
# FOOTER
# =====================================================

st.divider()

st.caption(
    "IPL Performance Analytics | "
    "Applied Statistics & Stochastic Probability | "
    "Historical IPL Data 2022–2025"
)

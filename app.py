import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from storage.database import get_session, EvalResult
from datetime import datetime

st.set_page_config(page_title="LLM Eval Framework", layout="wide",)

st.markdown("""
<style>
    .stApp { background-color: #0a0f1e; }
    [data-testid="stSidebar"] {
        background-color: #0d1526;
        border-right: 1px solid #1e3a5f;
    }
    .block-container { padding-top: 1.5rem; padding-left: 2rem; padding-right: 2rem; }
    h1, h2, h3, h4 { color: #e2e8f0 !important; }
    p, label, .stMarkdown { color: #94a3b8; }
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, #0f2744, #0d1f3c);
        border: 1px solid #1e3a5f;
        border-radius: 12px;
        padding: 1rem 1.25rem;
    }
    [data-testid="stMetricLabel"] { color: #64748b !important; font-size: 13px; }
    [data-testid="stMetricValue"] { color: #38bdf8 !important; font-size: 26px !important; }
    hr { border-color: #1e3a5f !important; }
    [data-testid="stDataFrame"] {
        border: 1px solid #1e3a5f;
        border-radius: 10px;
        overflow: hidden;
    }
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] .stMarkdown { color: #94a3b8; }
    .stat-badge {
        display: inline-block;
        background: #0f2744;
        border: 1px solid #1e3a5f;
        border-radius: 8px;
        padding: 6px 14px;
        font-size: 13px;
        color: #94a3b8;
        margin-right: 8px;
        margin-bottom: 8px;
    }
    .stat-badge span { color: #38bdf8; font-weight: 600; }
    .header-bar {
        background: linear-gradient(90deg, #0f2744, #0a1929);
        border: 1px solid #1e3a5f;
        border-radius: 12px;
        padding: 1.25rem 1.5rem;
        margin-bottom: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

session = get_session()
results = session.query(EvalResult).all()
session.close()

if not results:
    st.warning("No eval results found. Run main.py first!")
    st.stop()

df = pd.DataFrame([{
    "model": r.model_name,
    "version": r.model_version,
    "benchmark": r.benchmark_name,
    "score": r.score,
    "latency_ms": r.latency_ms,
    "timestamp": r.timestamp,
} for r in results])


with st.sidebar:
    st.markdown("###  LLM Eval")
    st.markdown("---")
    st.markdown("**Filters**")
    versions = sorted(df["version"].unique().tolist())
    selected_versions = st.multiselect("Version", versions, default=versions)
    benchmarks = sorted(df["benchmark"].unique().tolist())
    selected_benchmarks = st.multiselect("Benchmark", benchmarks, default=benchmarks)
    st.markdown("---")
    st.markdown("**Model info**")
    st.markdown(f"🤖 `{df['model'].iloc[-1]}`")
    st.markdown(f"📅 Since `{df['timestamp'].min().strftime('%b %d, %Y')}`")
    st.markdown(f"🔁 `{len(df)}` total runs logged")
    st.markdown("---")
    st.caption("Built with Streamlit · SQLite · Plotly")

filtered_df = df[
    df["version"].isin(selected_versions) &
    df["benchmark"].isin(selected_benchmarks)
]


st.markdown(f"""
<div class="header-bar">
  <div style="display:flex; justify-content:space-between; align-items:center;">
    <div>
      <h2 style="margin:0; font-size:20px; color:#e2e8f0;"> LLM Eval Framework Dashboard</h2>
      <p style="margin:4px 0 0; font-size:13px; color:#64748b;">
        Tracking model quality, latency & regression across versions
      </p>
    </div>
    <div style="text-align:right;">
      <div style="font-size:13px; color:#38bdf8;">● Live</div>
      <div style="font-size:12px; color:#64748b;">Updated {datetime.now().strftime('%b %d, %Y · %H:%M')}</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)


m1, m2, m3, m4 = st.columns(4)
best = filtered_df.loc[filtered_df["score"].idxmax()]
worst = filtered_df.loc[filtered_df["score"].idxmin()]

m1.metric(" Total Runs", len(filtered_df))
m2.metric(" Avg Score", round(filtered_df["score"].mean(), 2))
m3.metric(" Avg Latency", f"{round(filtered_df['latency_ms'].mean(), 1)}ms")
m4.metric(" Versions", len(filtered_df["version"].unique()))

st.markdown("<br>", unsafe_allow_html=True)


st.markdown(f"""
<div>
  <span class="stat-badge"> Best: <span>{best['benchmark']}</span> · <span>{best['score']}</span></span>
  <span class="stat-badge"> Weakest: <span>{worst['benchmark']}</span> · <span>{worst['score']}</span></span>
  <span class="stat-badge"> Fastest: <span>{round(filtered_df['latency_ms'].min())}ms</span></span>
  <span class="stat-badge"> Slowest: <span>{round(filtered_df['latency_ms'].max())}ms</span></span>
</div>
""", unsafe_allow_html=True)

st.divider()

COLORS = ["#38bdf8", "#4ade80", "#fbbf24", "#f472b6", "#a78bfa"]
FILL_COLORS = ["rgba(56,189,248,0.15)", "rgba(74,222,128,0.15)", "rgba(251,191,36,0.15)"]


c1, c2 = st.columns(2)

with c1:
    st.markdown("#### Score by Benchmark")
    st.caption("v1 vs v2 side-by-side")
    fig1 = px.bar(filtered_df, x="benchmark", y="score", color="version",
                  barmode="group", range_y=[0, 1],
                  color_discrete_sequence=["#38bdf8", "#4ade80"])
    fig1.update_layout(
        height=280, margin=dict(t=10, b=10),
        plot_bgcolor="#0a0f1e", paper_bgcolor="#0a0f1e",
        font_color="#94a3b8", legend_title_text="Version",
        legend=dict(bgcolor="#0d1526", bordercolor="#1e3a5f", borderwidth=1)
    )
    fig1.update_xaxes(showgrid=False, color="#64748b")
    fig1.update_yaxes(gridcolor="#1e3a5f", color="#64748b")
    st.plotly_chart(fig1, use_container_width=True)

with c2:
    st.markdown("####  Latency by Benchmark")
    st.caption("Response time in milliseconds")
    fig2 = px.bar(filtered_df, x="benchmark", y="latency_ms", color="version",
                  barmode="group",
                  color_discrete_sequence=["#38bdf8", "#4ade80"])
    fig2.update_layout(
        height=280, margin=dict(t=10, b=10),
        plot_bgcolor="#0a0f1e", paper_bgcolor="#0a0f1e",
        font_color="#94a3b8", legend_title_text="Version",
        legend=dict(bgcolor="#0d1526", bordercolor="#1e3a5f", borderwidth=1)
    )
    fig2.update_xaxes(showgrid=False, color="#64748b")
    fig2.update_yaxes(gridcolor="#1e3a5f", color="#64748b")
    st.plotly_chart(fig2, use_container_width=True)


st.markdown("####  Score Drift Over Time")
st.caption("Regression tracking — see how each benchmark changes across versions")
fig3 = px.line(filtered_df, x="timestamp", y="score", color="benchmark",
               markers=True, color_discrete_sequence=COLORS)
fig3.update_layout(
    height=300, margin=dict(t=10, b=10),
    plot_bgcolor="#0a0f1e", paper_bgcolor="#0a0f1e",
    font_color="#94a3b8",
    legend=dict(bgcolor="#0d1526", bordercolor="#1e3a5f", borderwidth=1)
)
fig3.update_xaxes(showgrid=False, color="#64748b")
fig3.update_yaxes(gridcolor="#1e3a5f", color="#64748b", range=[0, 1])
fig3.update_traces(line=dict(width=2.5), marker=dict(size=8))
st.plotly_chart(fig3, use_container_width=True)


st.markdown("####  Benchmark Radar — Model Strengths")
st.caption("Visual overview of model capability across all benchmarks")

radar_df = filtered_df.groupby(["benchmark", "version"])["score"].mean().reset_index()

fig4 = go.Figure()
for i, ver in enumerate(radar_df["version"].unique()):
    vdf = radar_df[radar_df["version"] == ver]
    fig4.add_trace(go.Scatterpolar(
        r=vdf["score"].tolist() + [vdf["score"].tolist()[0]],
        theta=vdf["benchmark"].tolist() + [vdf["benchmark"].tolist()[0]],
        fill="toself",
        name=ver,
        line_color=COLORS[i],
        fillcolor=FILL_COLORS[i]
    ))
fig4.update_layout(
    height=400, margin=dict(t=30, b=10),
    paper_bgcolor="#0a0f1e",
    polar=dict(
        bgcolor="#0d1526",
        radialaxis=dict(visible=True, range=[0, 1], color="#64748b", gridcolor="#1e3a5f"),
        angularaxis=dict(color="#94a3b8", gridcolor="#1e3a5f")
    ),
    legend=dict(bgcolor="#0d1526", bordercolor="#1e3a5f", borderwidth=1, font_color="#94a3b8"),
    font_color="#94a3b8"
)
st.plotly_chart(fig4, use_container_width=True)

st.divider()


st.markdown("####  Full Eval Results Log")
st.caption(f"{len(filtered_df)} records · sorted by latest first")

display_df = filtered_df.copy()
display_df["timestamp"] = display_df["timestamp"].dt.strftime("%b %d, %Y · %H:%M")
display_df = display_df.sort_values("timestamp", ascending=False).reset_index(drop=True)

def color_score(val):
    if val >= 0.5:
        return "background-color: #052e16; color: #4ade80"
    elif val >= 0.3:
        return "background-color: #1c1407; color: #fbbf24"
    else:
        return "background-color: #1c0a0a; color: #f87171"

st.dataframe(
    display_df.style.applymap(color_score, subset=["score"]),
    use_container_width=True,
    height=320
)

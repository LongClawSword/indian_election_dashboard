import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import json
import os
import time

# Page config with custom theme
st.set_page_config(
    page_title="Indian Election Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better aesthetics
st.markdown("""
    <style>
    .main {
        padding-top: 2rem;
    }
    .stPlotlyChart {
        background-color: white;
        border-radius: 10px;
        padding: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    h1 {
        color: #FF9933;
        font-weight: 700;
        padding-bottom: 1rem;
        border-bottom: 3px solid #138808;
    }
    h3 {
        color: #000080;
        font-weight: 600;
        margin-top: 2rem;
    }
    .stDataFrame {
        border-radius: 10px;
        overflow: hidden;
    }
    div[data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🇮🇳 Indian Election Dashboard")

API_BASE = "http://election-backend:8000/api"

# Sidebar styling
st.sidebar.markdown("### 📅 Select Election Year")

@st.cache_data
def get_years():
    resp = requests.get(f"{API_BASE}/years")
    return resp.json()["years"]

years = get_years()
selected_year = st.sidebar.selectbox("", years, index=len(years)-1, label_visibility="collapsed")

st.sidebar.markdown("---")
st.sidebar.markdown(f"**Viewing:** {selected_year} Elections")

@st.cache_data
def get_election_data(year):
    resp = requests.get(f"{API_BASE}/elections/{year}")
    return pd.DataFrame(resp.json()["data"])

df = get_election_data(selected_year)
winners = df[df["is_winner"]]

# Key metrics at the top
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Constituencies", len(df['constituency'].unique()))
with col2:
    st.metric("Total Candidates", len(df))
with col3:
    st.metric("Parties", len(df['party'].unique()))
with col4:
    st.metric("States", len(df['state'].unique()))

st.markdown("---")

# Party Seat Share
@st.cache_data
def get_seat_share(year):
    resp = requests.get(f"{API_BASE}/seat_share/{year}")
    return pd.DataFrame(resp.json()["seat_share"])

party_seats = get_seat_share(selected_year)
fig_seat = px.bar(
    party_seats, 
    x="party", 
    y="seats", 
    color="party",
    text="seats",
    labels={"seats": "Seats Won", "party": "Party"}
)
fig_seat.update_traces(textposition='outside')
fig_seat.update_layout(
    showlegend=False,
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    margin=dict(t=20, b=80),
    xaxis_tickangle=-45,
    height=400
)
st.markdown("### 🪧 Party-wise Seat Distribution")
st.plotly_chart(fig_seat, use_container_width=True)

# Two column layout for map and gender
col_left, col_right = st.columns([1.2, 1])

with col_left:
    st.markdown("### 🗺️ State-wise Voter Turnout")
    @st.cache_data
    def get_state_turnout(year):
        resp = requests.get(f"{API_BASE}/state_turnout/{year}")
        return pd.DataFrame(resp.json()["turnout"])

    state_turnout = get_state_turnout(selected_year)
    state_turnout["state"] = state_turnout["state"].str.title()

    @st.cache_data
    def load_india_geojson():
        path = "/app/india_states.geojson"
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Could not find GeoJSON file at path: {path}")

    india_geo = load_india_geojson()

    fig_map = px.choropleth(
        state_turnout,
        geojson=india_geo,
        locations="state",
        featureidkey="properties.name",
        color="votes",
        hover_name="state",
        color_continuous_scale="YlOrRd",
        projection="mercator"
    )
    fig_map.update_geos(fitbounds="locations", visible=False)
    fig_map.update_layout(
        margin={"r":0,"t":0,"l":0,"b":0},
        height=400
    )
    st.plotly_chart(fig_map, use_container_width=True)

with col_right:
    st.markdown("### 🚻 Gender Representation Trend")
    @st.cache_data
    def get_gender_trends():
        resp = requests.get(f"{API_BASE}/gender_trends")
        return pd.DataFrame(resp.json()["trend"])

    gender_trend = get_gender_trends()
    fig_gender = px.line(
        gender_trend, 
        x="year", 
        y="count", 
        color="gender", 
        markers=True,
        labels={"count": "Number of Candidates", "year": "Election Year"}
    )
    fig_gender.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=0, b=0),
        height=400,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_gender, use_container_width=True)

st.markdown("---")

# Vote share and margin in two columns
col_vote, col_margin = st.columns(2)

with col_vote:
    st.markdown("### 🥇 Top Parties by Vote Share")
    @st.cache_data
    def get_top_parties(year, top_n=5):
        resp = requests.get(f"{API_BASE}/top_parties/{year}?top_n={top_n}")
        return pd.DataFrame(resp.json()["top_parties"])

    top_parties = get_top_parties(selected_year)
    fig_vote = go.Figure(data=[go.Pie(
        labels=top_parties["party"], 
        values=top_parties["vote_share_percentage"],
        hole=0.45,
        marker=dict(line=dict(color='white', width=2))
    )])
    fig_vote.update_layout(
        margin=dict(t=0, b=0, l=0, r=0),
        height=400,
        showlegend=True,
        legend=dict(orientation="v", yanchor="middle", y=0.5)
    )
    st.plotly_chart(fig_vote, use_container_width=True)

with col_margin:
    st.markdown("### 📊 Top 10 Closest Contests")
    @st.cache_data
    def get_margin(year):
        resp = requests.get(f"{API_BASE}/margin/{year}")
        return pd.DataFrame(resp.json()["margin"])

    margin_df = get_margin(selected_year)
    margin_df_sorted = margin_df.sort_values("margin", ascending=True).head(10)

    fig_margin = px.bar(
        margin_df_sorted,
        y="constituency",
        x="margin",
        color="party",
        orientation='h',
        hover_data=["state","candidate","votes"],
        labels={"margin":"Margin (Votes)", "constituency":""}
    )
    fig_margin.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=0, b=0, l=0, r=0),
        height=400,
        showlegend=True,
        yaxis={'categoryorder':'total ascending'}
    )
    st.plotly_chart(fig_margin, use_container_width=True)

st.markdown("---")

# Search section
st.markdown("### 🔍 Search Election Results")
col_search, col_button = st.columns([4, 1])
with col_search:
    query = st.text_input("", placeholder="Enter Candidate or Constituency Name", label_visibility="collapsed")

if query:
    resp = requests.get(f"{API_BASE}/search", params={"query": query, "year": selected_year})
    results = pd.DataFrame(resp.json()["results"])
    if len(results) > 0:
        st.markdown(f"**Found {len(results)} result(s)**")
        st.dataframe(results, use_container_width=True, hide_index=True)
    else:
        st.info("No results found. Try a different search term.")
else:
    st.markdown("**Sample Results** (10 random entries)")
    st.dataframe(df.sample(10), use_container_width=True, hide_index=True)
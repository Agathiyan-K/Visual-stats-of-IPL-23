import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

st.title("IPL 2023 Analysis")
st.sidebar.title("Select Cap Type")
cap_type = st.sidebar.selectbox("Choose cap type to analyze:", ["Orange Cap", "Purple Cap"])

# Scrape and display data based on the selected cap type
@st.cache_data
def fetch_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table')
    data = []

    if cap_type == "Orange Cap":
        for row in table.find_all('tr')[1:]:
            columns = row.find_all('td')
            data.append([
                columns[0].text.strip(), columns[1].text.strip(), columns[2].text.strip(),
                columns[3].text.strip(), columns[4].text.strip(), columns[5].text.strip(),
                columns[6].text.strip(), columns[7].text.strip(), columns[8].text.strip(),
                columns[9].text.strip()
            ])
        columns = ["POS", "PLAYER", "TEAM", "RUNS", "MATCHES", "INNS", "AVG", "SR", "4S", "6S"]
    else:
        for row in table.find_all('tr')[1:]:
            columns = row.find_all('td')
            data.append([
                columns[0].text.strip(), columns[1].text.strip(), columns[2].text.strip(),
                columns[3].text.strip(), columns[4].text.strip(), columns[5].text.strip(),
                columns[6].text.strip(), columns[7].text.strip(), columns[8].text.strip(),
                columns[9].text.strip(), columns[10].text.strip(), columns[11].text.strip(),
                columns[12].text.strip()
            ])
        columns = ["POS", "PLAYER", "TEAM", "WKTS", "RUNS", "OVR", "BBF", "AVG", "EC", "SR", "3W", "5W", "MDNS"]

    return pd.DataFrame(data, columns=columns)

# Load data
url = "https://www.news18.com/cricketnext/ipl-2023/orange-cap-holder.html" if cap_type == "Orange Cap" else "https://www.news18.com/cricketnext/ipl-2023/purple-cap-holder.html"
df = fetch_data(url)

st.write(f"### {cap_type} Data")
st.dataframe(df)

if cap_type == "Orange Cap":
    # Analyze top 10 batsmen by runs
    df["RUNS"] = df["RUNS"].astype(int)
    top_10_batsmen = df.sort_values(by="RUNS", ascending=False).head(10)
    total_runs_top_10 = top_10_batsmen["RUNS"].sum()
    total_runs = df["RUNS"].sum()
    percentage_runs_top_10 = (total_runs_top_10 / total_runs) * 100

    st.write("#### Total Runs Analysis")
    st.write(f"Total Runs of Top 10 Batsmen: {total_runs_top_10}")
    st.write(f"Percentage of Top 10 Runs to Total Runs: {percentage_runs_top_10:.2f}%")

    # Line graph of team total runs
    teams = df["TEAM"].unique()
    team_total_runs = df.groupby("TEAM")["RUNS"].sum()
    st.write("#### Total Runs by Team")
    fig, ax = plt.subplots()
    ax.plot(team_total_runs.index, team_total_runs.values, marker='o', color='skyblue')
    ax.set_title("Total Runs Scored by Each Team")
    ax.set_xlabel("Team")
    ax.set_ylabel("Total Runs")
    st.pyplot(fig)

    # Additional analyses for 4s, 6s, and other statistics
    df["4S"] = df["4S"].astype(int)
    df["6S"] = df["6S"].astype(int)
    df["SR"] = df["SR"].astype(float)

    # 4s Analysis
    st.subheader("4s Analysis")
    total_4s = df["4S"].sum()
    total_runs_through_4s = (df["4S"] * 4).sum()
    st.write(f"Total Number of 4s: {total_4s}")
    st.write(f"Total Runs Scored through 4s: {total_runs_through_4s}")

    # 6s Analysis
    st.subheader("6s Analysis")
    total_6s = df["6S"].sum()
    total_runs_through_6s = (df["6S"] * 6).sum()
    st.write(f"Total Number of 6s: {total_6s}")
    st.write(f"Total Runs Scored through 6s: {total_runs_through_6s}")

    # Strike Rate Analysis
    st.subheader("Strike Rate Analysis")
    avg_strike_rate = df["SR"].mean()
    st.write(f"Average Strike Rate: {avg_strike_rate:.2f}")

    # Team-wise 4s and 6s distribution
    st.subheader("Team-wise 4s and 6s Distribution")
    team_4s = df.groupby("TEAM")["4S"].sum()
    team_6s = df.groupby("TEAM")["6S"].sum()

    # Bar chart for team-wise 4s and 6s
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(team_4s.index, team_4s.values, color='blue', alpha=0.6, label='4s')
    ax.bar(team_6s.index, team_6s.values, color='orange', alpha=0.6, label='6s')
    ax.set_title("Team-wise 4s and 6s Distribution")
    ax.set_xlabel("Team")
    ax.set_ylabel("Count")
    ax.legend()
    st.pyplot(fig)

if cap_type == "Purple Cap":
    # Additional analyses for Purple Cap can be added here (e.g., wickets, economy rates)
    df["WKTS"] = df["WKTS"].astype(int)
    total_wickets = df["WKTS"].sum()
    st.write(f"Total Wickets Taken: {total_wickets}")

    # Team-wise Wickets Analysis
    team_wickets = df.groupby("TEAM")["WKTS"].sum()
    st.subheader("Team-wise Wickets Distribution")
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(team_wickets.index, team_wickets.values, color='purple')
    ax.set_title("Total Wickets Taken by Each Team")
    ax.set_xlabel("Team")
    ax.set_ylabel("Total Wickets")
    st.pyplot(fig)

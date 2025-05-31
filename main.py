import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np

st.title("CSV Dashboard")

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    # Read CSV and limit rows
    df = pd.read_csv(uploaded_file)
    df = df.head(5)
    st.dataframe(df)

    grouped_data = df.groupby('year')['income'].sum().reset_index()

    # Smaller sizes
    matplotlib_figsize = (4, 3)  # smaller than before (6,4)
    plotly_width = 400  # smaller than before 600
    plotly_height = 300  # smaller than before 400

    charts = []

    # Pie Chart (Plotly)
    fig_pie = px.pie(
        grouped_data,
        names="year",
        values="income",
        title="INCOME DISTRIBUTION BY YEAR",
        width=plotly_width,
        height=plotly_height
    )
    charts.append(("plotly", fig_pie, "Pie Chart"))

    # Line Chart (matplotlib)
    fig_line, ax_line = plt.subplots(figsize=matplotlib_figsize)
    ax_line.plot(grouped_data['year'], grouped_data['income'], marker='o', linestyle='-', color='green')
    ax_line.set_xlabel("Year")
    ax_line.set_ylabel("Income")
    ax_line.set_title("Income Trend by Year")
    charts.append(("matplotlib", fig_line, "Line Chart"))

    # Bar Chart (matplotlib)
    fig_bar, ax_bar = plt.subplots(figsize=matplotlib_figsize)
    ax_bar.bar(grouped_data['year'], grouped_data['income'], color='skyblue')
    ax_bar.set_xlabel("Year")
    ax_bar.set_ylabel("Income")
    ax_bar.set_title("Income by Year")
    charts.append(("matplotlib", fig_bar, "Bar Chart"))

    # Donut Chart (Plotly)
    fig_donut = px.pie(
        grouped_data,
        names='year',
        values='income',
        hole=0.5,
        title="Donut Chart: Income by Year",
        width=plotly_width,
        height=plotly_height
    )
    charts.append(("plotly", fig_donut, "Donut Chart"))

    # Scatter Plot (matplotlib)
    fig_scatter, ax_scatter = plt.subplots(figsize=matplotlib_figsize)
    ax_scatter.scatter(grouped_data['year'], grouped_data['income'], color='red', marker='o', s=100)
    ax_scatter.set_xlabel("Year")
    ax_scatter.set_ylabel("Income")
    ax_scatter.set_title("Scatter Plot of Income by Year")
    charts.append(("matplotlib", fig_scatter, "Scatter Plot"))

    # Ribbon (Area) Chart (matplotlib)
    fig_ribbon, ax_ribbon = plt.subplots(figsize=matplotlib_figsize)
    ax_ribbon.fill_between(grouped_data['year'], grouped_data['income'], color='purple', alpha=0.4)
    ax_ribbon.plot(grouped_data['year'], grouped_data['income'], color='purple', marker='o')
    ax_ribbon.set_xlabel("Year")
    ax_ribbon.set_ylabel("Income")
    ax_ribbon.set_title("Ribbon (Area) Chart of Income by Year")
    charts.append(("matplotlib", fig_ribbon, "Ribbon (Area) Chart"))

    # Funnel Chart (Plotly)
    funnel_data = grouped_data.sort_values(by='income', ascending=False)
    fig_funnel = px.funnel(
        funnel_data,
        x='income',
        y='year',
        title="Funnel Chart: Income by Year",
        width=plotly_width,
        height=plotly_height
    )
    charts.append(("plotly", fig_funnel, "Funnel Chart"))

    # Initialize chart index in session state
    if "chart_idx" not in st.session_state:
        st.session_state.chart_idx = 0

    # Display current chart
    chart_type, fig, title = charts[st.session_state.chart_idx]
    st.subheader(f"Chart {st.session_state.chart_idx + 1} of {len(charts)}: {title}")

    if chart_type == "plotly":
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.pyplot(fig)

    # Navigation buttons below the chart
    col_back, col_next = st.columns(2)
    with col_back:
        if st.button("Back"):
            st.session_state.chart_idx = (st.session_state.chart_idx - 1) % len(charts)
    with col_next:
        if st.button("Next"):
            st.session_state.chart_idx = (st.session_state.chart_idx + 1) % len(charts)

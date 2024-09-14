#!/usr/bin/env python
# coding: utf-8

# In[1]:


import streamlit as st
import pandas as pd
import altair as alt
import os

# Enable VegaFusion data transformer
alt.data_transformers.enable("vegafusion")

# Define the path to your CSV file
file_path = 'https://raw.githubusercontent.com/MashalFatima305/fifth/main/altman_z_scores.csv'

# Check if the file exists in the specified path
try:
    # Load data from the CSV file
    df = pd.read_csv(file_path)

    # Clean column names to remove any extra spaces or newline characters
    df.columns = df.columns.str.strip()

    # Add a Period column with numerical values ranging from 1 to the length of the dataframe
    df['Period'] = range(1, len(df) + 1)

    # Ensure the score columns are numeric
    df['Altman Z-Score'] = pd.to_numeric(df['Altman Z-Score'], errors='coerce')
    df['Springate Score'] = pd.to_numeric(df['Springate Score'], errors='coerce')
    df['Ohlson O-score'] = pd.to_numeric(df['Ohlson O-score'], errors='coerce')
    df['Zmijewski Score'] = pd.to_numeric(df['Zmijewski Score'], errors='coerce')

    # Streamlit app
    st.title('Financial Scores Dashboard')

    # Display the data
    st.write(df)

    # Function to plot scores
    def plot_score(data, score_column, title, safe_zone=None, distress_zone=None):
        # Create the base chart
        base = alt.Chart(data).encode(
            x=alt.X('Period:Q', title='Period'),  # Use the 'Period' column for the x-axis
            y=alt.Y(f'{score_column}:Q', title=title)  # Ensure your CSV has the correct column name
        )

        # Line chart for the score
        line = base.mark_line().encode(
            tooltip=['Period', score_column]
        )

        # Safe zone
        safe = alt.Chart(pd.DataFrame({'y': [safe_zone]})).mark_rule(color='green', strokeDash=[5, 5]).encode(y='y:Q') if safe_zone is not None else None

        # Distress zone
        distress = alt.Chart(pd.DataFrame({'y': [distress_zone]})).mark_rule(color='red', strokeDash=[2, 2]).encode(y='y:Q') if distress_zone is not None else None

        # Combine the charts
        charts = [line]
        if safe is not None:
            charts.append(safe)
        if distress is not None:
            charts.append(distress)

        chart = alt.layer(*charts).properties(
            title=f'{title} Over Time',
            width=800,
            height=400
        ).interactive()

        return chart

    # Display the charts
    st.altair_chart(plot_score(df, 'Altman Z-Score', 'Altman Z-Score', safe_zone=2.99, distress_zone=1.81), use_container_width=True)
    st.altair_chart(plot_score(df, 'Springate Score', 'Springate Score', distress_zone=0.862), use_container_width=True)
    st.altair_chart(plot_score(df, 'Ohlson O-score', 'Ohlson O-score', distress_zone=0.5), use_container_width=True)
    st.altair_chart(plot_score(df, 'Zmijewski Score', 'Zmijewski Score', distress_zone=0.0), use_container_width=True)

except Exception as e:
    st.error(f"An error occurred while loading the file: {e}")


# In[ ]:





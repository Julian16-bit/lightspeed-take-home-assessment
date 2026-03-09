import streamlit as st
import pandas as pd
import plotly.express as px
from src.llm_functions import create_feedback_summary

st.set_page_config(page_title="Feedback Analytics Dashboard", layout="wide")

st.title("Customer Feedback Monitoring Application")

df = pd.read_csv("output_with_generated_fields.csv")

tab1, tab2, tab3 = st.tabs(["Dashboard", "AI Insights", "Info"])

with tab1:
    st.header("Dashboard")

    # Filters
    col_filter1, col_filter2 = st.columns(2)

    with col_filter1:
        sources = ["All"] + df["source_type"].unique().tolist()
        selected_source = st.selectbox("Filter by Source", sources)

    with col_filter2:
        all_subjects = df["subject"].unique().tolist()
        selected_subjects = st.multiselect("Filter by Theme", all_subjects, default=all_subjects)

    # Filter dataframe
    filtered_df = df.copy()
    if selected_source != "All":
        filtered_df = filtered_df[filtered_df["source_type"] == selected_source]
    if selected_subjects:
        filtered_df = filtered_df[filtered_df["subject"].isin(selected_subjects)]

    # KPI Metrics Summary
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Feedback", len(filtered_df))

    with col2:
        most_common_sentiment = filtered_df["sentiment"].mode()[0] if len(filtered_df) > 0 else "N/A"
        st.metric("Most Common Sentiment", most_common_sentiment)

    with col3:
        avg_score = filtered_df["raw_score"].mean() if len(filtered_df) > 0 else 0
        st.metric("Average Score", f"{avg_score:.1f}")

    st.divider()

    # Sentiment distribution chart
    st.subheader("Sentiment Distribution")
    sentiment_counts = filtered_df["sentiment"].value_counts().reset_index()
    sentiment_counts.columns = ["sentiment", "count"]

    color_map = {
        "Positive": "#22c55e",
        "Neutral": "#64748b",
        "Negative": "#ef4444",
        "Frustrated": "#dc2626"
    }

    sentiment_chart = px.pie(sentiment_counts, names="sentiment", values="count",
                 color="sentiment",
                 color_discrete_map=color_map)
    st.plotly_chart(sentiment_chart, use_container_width=True)


    st.subheader("Average Rating by Theme")
    avg_rating_by_theme = filtered_df.groupby("subject")["raw_score"].mean().reset_index()
    avg_rating_by_theme.columns = ["subject", "avg_score"]
    avg_rating_by_theme = avg_rating_by_theme.sort_values("avg_score", ascending=True)

    theme_chart = px.bar(avg_rating_by_theme, x="avg_score", y="subject", orientation="h",
                         labels={"avg_score": "Average Score", "subject": "Theme"})
    st.plotly_chart(theme_chart, use_container_width=True)

    st.subheader("Feedback Count by Theme")
    theme_counts = filtered_df["subject"].value_counts().reset_index()
    theme_counts.columns = ["subject", "count"]
    theme_counts = theme_counts.sort_values("count", ascending=True)

    count_chart = px.bar(theme_counts, x="count", y="subject", orientation="h",
                         labels={"count": "Number of Feedback", "subject": "Theme"})
    st.plotly_chart(count_chart, use_container_width=True)

with tab2:
    st.header("AI Insights")

    merchants = df["merchant_id"].unique().tolist()
    selected_merchant = st.selectbox("Select a Merchant", merchants)

    summary_button = st.button("Generate Feedback Summary")

    if summary_button:
        filtered_merchant_df = df[df["merchant_id"]==selected_merchant]
        merchant_data_csv = filtered_merchant_df[["content", "sentiment", "subject", "raw_score"]].to_csv(index=False)

        with st.expander("View Raw Data"):
            st.write(filtered_merchant_df[:10])

        with st.spinner("Generating..."):
            output = create_feedback_summary(merchant_data_csv)

        # Display the results in formatted way
        st.subheader("Feedback Summary")
        st.write(output.summary)

        risk_emojis = {
            "low": "🟢",
            "medium": "🟡",
            "high": "🔴"
        }
        risk_emoji = risk_emojis.get(output.risk_level.lower(), "⚪")

        col1, col2 = st.columns(2, gap="large")
        with col1:
            st.subheader("Recommended Action")
            st.info(output.recommended_action)
        with col2:
            st.subheader("Risk Level")
            st.write(f"{risk_emoji} {output.risk_level.capitalize()}")

with tab3:
    st.header("About This Application")

    st.markdown("""
    This Customer Feedback Monitoring Application helps you analyze and understand customer feedback
    from various sources, providing actionable insights to improve merchant satisfaction.
    """)

    st.subheader("How to Use")

    st.markdown("""
    1. **Start with the Dashboard**: Get an overview of all feedback across your merchants
    2. **Apply Filters**: Use the source and theme filters to focus on specific areas of interest
    3. **Analyze Trends**: Review the sentiment and rating distributions to identify patterns
    4. **AI Analysis**: Switch to the AI Insights tab for detailed merchant analysis
    5. **Generate Summaries**: Select a merchant and click "Generate Feedback Summary" to get AI powered insights
    6. **Review Output**: AI will produce a summary, risk level, and recommended action. Verify the source data by expanding "View Raw Data".
    """)

    st.subheader("Key Insights")
    
    st.markdown("""
    **Sentiment Overview:**
    - Overall sentiment skews negative: 54.2% of feedback is negative/frustrated vs. 35.3% positive
    - Support tickets show the most negative sentiment (77.7%), while surveys are predominantly positive (53.3%)

    **Theme Performance:**
    - Highest rated: POS Performance (9.2/10) and Integration (7.5/10)
    - Lowest rated: Reliability & Stability (3.7/10) and Pricing & Billing (2.5/10)
                
    **Feedback Volume:**
    - Most discussed: Reliability & Stability (17 entries)
    - Least discussed: Pricing & Billing and Feature Requests (1 entry each)
    """)

    st.subheader("Data Sources")

    st.markdown("""
    This application processes feedback from multiple sources (AI generated data):
    - **App Store Reviews**: Public reviews from App Store platforms
    - **Surveys**: Direct customer survey responses
    - **Support Tickets**: Customer support interactions
    """)


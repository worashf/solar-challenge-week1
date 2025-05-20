import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from utils import (
    load_solar_data,
    analyze_missing_data,
    detect_outliers,
    prepare_comparison_data
)

# Page Configuration
st.set_page_config(
    page_title="Solar Analytics",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .header {font-size:24px !important; color:#2c3e50; border-bottom:1px solid #eee; padding-bottom:10px}
    .metric {background:#f8f9fa; border-radius:10px; padding:15px; margin-bottom:15px}
    .plot-container {background:white; border-radius:10px; padding:15px; margin-bottom:20px}
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<div class="header">🌍 Solar Data Analytics</div>', unsafe_allow_html=True)
st.caption("Compare solar potential metrics across West Africa")


# Data Loading
@st.cache_data
def load_data():
    return {
        'raw': load_solar_data('raw'),
        'clean': load_solar_data('clean')
    }


data = load_data()

# Sidebar Controls
with st.sidebar:
    st.header("Settings")
    analysis_mode = st.radio(
        "Analysis Mode",
        ["Data Quality", "Country Comparison"],
        index=0
    )

    if analysis_mode == "Country Comparison" and not data['clean'].empty:
        countries = st.multiselect(
            "Select Countries",
            options=data['clean']['Country'].unique(),
            default=data['clean']['Country'].unique()[:2]
        )
        metric = st.selectbox(
            "Select Metric",
            options=['GHI', 'DNI', 'DHI'],
            index=0
        )

# Main Content
if analysis_mode == "Data Quality":
    st.header("Data Quality Assessment")

    if data['raw'].empty:
        st.warning("No raw data available")
    else:
        tab1, tab2 = st.tabs(["Missing Data", "Outliers"])

        with tab1:
            missing_analysis = analyze_missing_data(data['raw'])
            if missing_analysis:
                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("Missing Values Count")
                    st.dataframe(missing_analysis['missing_counts'])
                with col2:
                    st.subheader(f"Significant Missing (>5%)")
                    st.dataframe(missing_analysis['significant_missing'])

                st.subheader("Missing Data Pattern")
                fig, ax = plt.subplots(figsize=(12, 4))
                sns.heatmap(data['raw'].isnull(), cbar=False, cmap='viridis')
                st.pyplot(fig)

        with tab2:
            numeric_cols = ['GHI', 'DNI', 'DHI', 'ModA', 'ModB', 'WS', 'WSgust']
            outliers = detect_outliers(data['raw'], numeric_cols)

            selected_col = st.selectbox(
                "Select Column",
                options=list(outliers.keys())
            )

            if selected_col:
                col1, col2 = st.columns(2)
                with col1:
                    st.subheader(f"Outliers in {selected_col}")
                    st.dataframe(outliers[selected_col])
                with col2:
                    st.subheader("Distribution")
                    fig, ax = plt.subplots(figsize=(10, 5))
                    sns.boxplot(x=data['raw'][selected_col])
                    st.pyplot(fig)

elif analysis_mode == "Country Comparison":
    st.header("Country Comparison")

    if data['clean'].empty:
        st.warning("No cleaned data available")
    else:
        comparison = prepare_comparison_data(
            data['clean'],
            countries,
            metric
        )

        if comparison:
            col1, col2 = st.columns(2)
            with col1:
                st.subheader(f"{metric} Distribution")
                fig, ax = plt.subplots(figsize=(10, 6))
                sns.boxplot(
                    data=comparison['filtered_data'],
                    x='Country',
                    y=metric,
                    palette="viridis"
                )
                st.pyplot(fig)

            with col2:
                st.subheader("Summary Statistics")
                st.dataframe(
                    comparison['stats'].style.format("{:.2f}"),
                    use_container_width=True
                )

            if len(comparison['samples']) >= 2:
                from scipy import stats

                st.subheader("Statistical Tests")

                col1, col2 = st.columns(2)
                with col1:
                    _, p_anova = stats.f_oneway(*comparison['samples'])
                    st.metric("ANOVA p-value", value=f"{p_anova:.4f}")
                with col2:
                    _, p_kw = stats.kruskal(*comparison['samples'])
                    st.metric("Kruskal-Wallis p-value", value=f"{p_kw:.4f}")

                st.info("""
                **Interpretation Guide:**
                - p < 0.05: Significant differences exist
                - p ≥ 0.05: No significant differences
                """)

# Footer
st.markdown("---")
st.caption("Solar Analytics Dashboard | Data through " +
           pd.Timestamp.now().strftime("%Y-%m-%d"))
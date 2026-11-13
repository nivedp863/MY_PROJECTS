import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title="Athletics EDA Dashboard",
    page_icon="🏃",
    layout="wide"
)

sns.set_theme(style="whitegrid")
st.title("🏃 Strategic Preparation in Athletics")
st.caption("Exploratory Data Analysis Dashboard")

st.sidebar.header("Data")
uploaded_file = st.sidebar.file_uploader("Upload your athletics CSV file", type=["csv"])

@st.cache_data
def load_data(file):
    return pd.read_csv(file)

if uploaded_file is not None:
    try:
        raw_df = load_data(uploaded_file)
    except Exception as exc:
        st.error(f"Could not read the CSV file: {exc}")
        st.stop()
else:
    st.info("Upload `strategic_preparation_in_athletics.csv` in the sidebar to begin. The dashboard will use your uploaded dataset.")
    st.stop()

# Match the cleaning step in the original notebook.
df = raw_df.drop(columns=["Unnamed: 0"], errors="ignore").copy()

st.sidebar.success(f"Loaded {len(df):,} rows × {len(df.columns):,} columns")
st.sidebar.markdown("---")
st.sidebar.subheader("Analysis settings")
use_cleaned = st.sidebar.toggle("Use mode-imputed data for charts", value=False)

clean_df = df.copy()
for col in clean_df.columns:
    modes = clean_df[col].mode(dropna=True)
    if not modes.empty:
        clean_df[col] = clean_df[col].fillna(modes.iloc[0])

analysis_df = clean_df if use_cleaned else df

tabs = st.tabs([
    "Overview", "Data Quality", "Statistics", "Unique Values",
    "Outliers", "Correlation", "Visualizations"
])

with tabs[0]:
    st.subheader("Dataset Overview")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Rows", f"{df.shape[0]:,}")
    c2.metric("Columns", f"{df.shape[1]:,}")
    c3.metric("Total cells", f"{df.size:,}")
    c4.metric("Duplicate rows", f"{df.duplicated().sum():,}")

    st.markdown("#### Dataset preview")
    st.dataframe(df.head(10), use_container_width=True)
    with st.expander("View last 5 rows"):
        st.dataframe(df.tail(), use_container_width=True)

    st.markdown("#### Column information")
    info_df = pd.DataFrame({
        "Column": df.columns,
        "Data type": df.dtypes.astype(str).values,
        "Non-null values": df.notna().sum().values,
        "Missing values": df.isna().sum().values
    })
    st.dataframe(info_df, use_container_width=True)

    st.download_button(
        "Download current dataset as CSV",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="athletics_dataset.csv",
        mime="text/csv"
    )

with tabs[1]:
    st.subheader("Data Quality Analysis")
    missing_count = df.isna().sum()
    missing_pct = (df.isna().mean() * 100).round(2)
    quality = pd.DataFrame({
        "Missing values": missing_count,
        "Missing (%)": missing_pct,
        "Data type": df.dtypes.astype(str)
    }).sort_values("Missing (%)", ascending=False)

    a, b = st.columns(2)
    a.metric("Duplicate records", f"{df.duplicated().sum():,}")
    b.metric("Columns with missing values", f"{(missing_count > 0).sum():,}")
    st.dataframe(quality, use_container_width=True)

    missing_plot = quality[quality["Missing values"] > 0]
    if not missing_plot.empty:
        fig, ax = plt.subplots(figsize=(10, max(3, len(missing_plot) * 0.35)))
        sns.barplot(data=missing_plot.reset_index(names="Column"),
                    x="Missing (%)", y="Column", ax=ax)
        ax.set_title("Missing Values by Column")
        st.pyplot(fig)
        plt.close(fig)
    else:
        st.success("No missing values found.")

    st.markdown("#### Mode imputation")
    st.write("This follows the notebook's approach: fill each column's missing values with its most frequent value (mode).")
    st.dataframe(pd.DataFrame({
        "Missing before": df.isna().sum(),
        "Missing after": clean_df.isna().sum()
    }), use_container_width=True)
    st.download_button(
        "Download mode-imputed dataset",
        data=clean_df.to_csv(index=False).encode("utf-8"),
        file_name="athletics_dataset_mode_imputed.csv",
        mime="text/csv"
    )

with tabs[2]:
    st.subheader("Descriptive Statistics")
    st.markdown("#### Numeric columns")
    st.dataframe(analysis_df.describe(), use_container_width=True)
    st.markdown("#### All columns")
    st.dataframe(analysis_df.describe(include="all").transpose(), use_container_width=True)

with tabs[3]:
    st.subheader("Unique Values")
    for col in analysis_df.columns:
        with st.expander(f"{col} — {analysis_df[col].nunique(dropna=False)} unique values"):
            vals = analysis_df[col].dropna().unique().tolist()
            st.write(vals[:500])
            if len(vals) > 500:
                st.caption(f"Showing first 500 of {len(vals)} non-null unique values.")
            st.caption(f"Missing values: {analysis_df[col].isna().sum():,}")

with tabs[4]:
    st.subheader("Outlier Detection")
    numeric_cols = analysis_df.select_dtypes(include=np.number).columns.tolist()
    if not numeric_cols:
        st.warning("No numeric columns are available for boxplots.")
    else:
        selected_outlier_cols = st.multiselect(
            "Choose numeric columns", numeric_cols, default=numeric_cols[:min(6, len(numeric_cols))]
        )
        if selected_outlier_cols:
            for start in range(0, len(selected_outlier_cols), 2):
                cols = st.columns(2)
                for j, col in enumerate(selected_outlier_cols[start:start+2]):
                    fig, ax = plt.subplots(figsize=(6, 3.5))
                    sns.boxplot(x=analysis_df[col].dropna(), ax=ax)
                    ax.set_title(f"Boxplot of {col}")
                    cols[j].pyplot(fig, use_container_width=True)
                    plt.close(fig)
        else:
            st.info("Select at least one column to display boxplots.")

with tabs[5]:
    st.subheader("Correlation Analysis")
    numeric_df = analysis_df.select_dtypes(include="number")
    if numeric_df.shape[1] < 2:
        st.warning("At least two numeric columns are required to calculate correlation.")
    else:
        corr = numeric_df.corr()
        st.dataframe(corr, use_container_width=True)
        fig, ax = plt.subplots(figsize=(max(8, len(corr.columns) * 0.8),
                                        max(5, len(corr.columns) * 0.6)))
        sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
        ax.set_title("Correlation Heatmap — Strategic Preparation in Athletics")
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

with tabs[6]:
    st.subheader("Data Visualizations")
    columns = analysis_df.columns.tolist()
    numeric_cols = analysis_df.select_dtypes(include=np.number).columns.tolist()

    # Scatter plot: original notebook's intended variables, with selectable fallback.
    st.markdown("#### Training Hours vs Performance Score")
    if len(numeric_cols) >= 2:
        default_x = "Training_Hours_Per_Week" if "Training_Hours_Per_Week" in numeric_cols else numeric_cols[0]
        default_y = "Performance_Score" if "Performance_Score" in numeric_cols else numeric_cols[1]
        xcol, ycol = st.columns(2)
        x_var = xcol.selectbox("X-axis", numeric_cols, index=numeric_cols.index(default_x), key="scatter_x")
        y_var = ycol.selectbox("Y-axis", numeric_cols, index=numeric_cols.index(default_y), key="scatter_y")
        scatter_data = analysis_df[[x_var, y_var]].dropna()
        if len(scatter_data) > 3000:
            scatter_data = scatter_data.sample(3000, random_state=42)
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.scatterplot(data=scatter_data, x=x_var, y=y_var, alpha=0.5, ax=ax)
        ax.set_title(f"{x_var} vs {y_var}")
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)
    else:
        st.info("At least two numeric columns are needed for a scatter plot.")

    st.divider()
    st.markdown("#### Performance Score Distribution")
    if "Performance_Score" in analysis_df.columns and pd.api.types.is_numeric_dtype(analysis_df["Performance_Score"]):
        fig, ax = plt.subplots(figsize=(8, 4.5))
        sns.histplot(data=analysis_df, x="Performance_Score", bins=30, kde=True, ax=ax)
        ax.set_title("Distribution of Performance Scores")
        ax.set_xlabel("Performance Score")
        ax.set_ylabel("Number of Athletes")
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)
    elif numeric_cols:
        hist_col = st.selectbox("Choose a numeric column for histogram", numeric_cols, key="hist_col")
        fig, ax = plt.subplots(figsize=(8, 4.5))
        sns.histplot(data=analysis_df, x=hist_col, bins=30, kde=True, ax=ax)
        ax.set_title(f"Distribution of {hist_col}")
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)
    else:
        st.info("No numeric columns available for a histogram.")

    st.divider()
    st.markdown("#### Average Performance by Sport Type")
    if {"Sport_Type", "Performance_Score"}.issubset(analysis_df.columns):
        sport_avg = (analysis_df.groupby("Sport_Type", dropna=False)["Performance_Score"]
                     .mean().sort_values(ascending=False))
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.barplot(x=sport_avg.index.astype(str), y=sport_avg.values, ax=ax)
        ax.set_title("Average Performance Score by Sport Type")
        ax.set_xlabel("Sport Type")
        ax.set_ylabel("Average Performance Score")
        ax.tick_params(axis="x", rotation=45)
        fig.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)
    else:
        st.info("This chart requires 'Sport_Type' and 'Performance_Score' columns.")

    st.divider()
    st.markdown("#### Training Hours vs Average Performance Trend")
    if {"Training_Hours_Per_Week", "Performance_Score"}.issubset(analysis_df.columns):
        trend_data = analysis_df[["Training_Hours_Per_Week", "Performance_Score"]].dropna().copy()
        trend_data["Training_Hours_Group"] = trend_data["Training_Hours_Per_Week"].round()
        trend = trend_data.groupby("Training_Hours_Group")["Performance_Score"].mean().sort_index()
        fig, ax = plt.subplots(figsize=(9, 4.5))
        ax.plot(trend.index, trend.values, marker="o", linewidth=2)
        ax.set_title("Training Hours vs Average Performance Trend")
        ax.set_xlabel("Training Hours Per Week (Rounded)")
        ax.set_ylabel("Average Performance Score")
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)
    else:
        st.info("This chart requires 'Training_Hours_Per_Week' and 'Performance_Score' columns.")

    st.divider()
    st.markdown("#### Athlete Distribution by Gender")
    if "Gender" in analysis_df.columns:
        gender_counts = analysis_df["Gender"].dropna().value_counts()
        if not gender_counts.empty:
            fig, ax = plt.subplots(figsize=(7, 5))
            ax.pie(gender_counts.values, labels=gender_counts.index.astype(str),
                   autopct="%1.1f%%", startangle=90)
            ax.set_title("Athlete Distribution by Gender")
            ax.axis("equal")
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)
        else:
            st.info("The Gender column contains no non-missing values.")
    else:
        st.info("The dataset does not contain a 'Gender' column.")

st.sidebar.markdown("---")
st.sidebar.caption("Built with Streamlit, Pandas, Matplotlib and Seaborn.")

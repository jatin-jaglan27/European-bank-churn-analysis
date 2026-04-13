import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------
# PAGE CONFIG
# -------------------------
st.set_page_config(layout="wide", page_title="European Bank Dashboard")

# -------------------------
# PREMIUM DARK GLASS THEME
# -------------------------
st.markdown("""
<style>

/* MAIN BACKGROUND (Gradient + Blur Feel) */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0f172a, #020617);
}

/* GLASS EFFECT CARDS */
[data-testid="stMetric"], .css-1r6slb0, .stPlotlyChart {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(12px);
    border-radius: 15px;
    padding: 15px;
    border: 1px solid rgba(255,255,255,0.1);
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background: #020617;
    border-right: 1px solid rgba(255,255,255,0.1);
}

/* TEXT */
h1, h2, h3, h4 {
    color: #F9FAFB;
}

p, label {
    color: #E5E7EB !important;
}

/* INPUTS */
input, div[data-baseweb="select"] {
    background-color: #020617 !important;
    color: white !important;
    border-radius: 10px !important;
}

/* KPI LEFT BORDER COLORS */
[data-testid="stMetric"] {
    border-left: 5px solid #6366F1;
}

/* REMOVE WHITE SPACE */
.block-container {
    padding-top: 2rem;
}

/* SCROLLBAR */
::-webkit-scrollbar {
    width: 8px;
}
::-webkit-scrollbar-thumb {
    background: #4F46E5;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# -------------------------
# LOAD DATA
# -------------------------
df = pd.read_csv("European_Bank.csv")

# -------------------------
# SIDEBAR FILTERS
# -------------------------
st.sidebar.title("Filters")

country = st.sidebar.selectbox("Country", ["All"] + sorted(df["Geography"].unique()))
gender = st.sidebar.selectbox("Gender", ["All"] + sorted(df["Gender"].unique()))
products = st.sidebar.slider("Max Products", 1, int(df["NumOfProducts"].max()), int(df["NumOfProducts"].max()))
balance = st.sidebar.slider("Min Balance", 0, int(df["Balance"].max()), 0)

# -------------------------
# FILTER DATA
# -------------------------
filtered_df = df.copy()

if country != "All":
    filtered_df = filtered_df[filtered_df["Geography"] == country]

if gender != "All":
    filtered_df = filtered_df[filtered_df["Gender"] == gender]

filtered_df = filtered_df[filtered_df["NumOfProducts"] <= products]
filtered_df = filtered_df[filtered_df["Balance"] >= balance]

if filtered_df.empty:
    st.warning("No data available")
    st.stop()

# -------------------------
# DERIVED FEATURES
# -------------------------
filtered_df["HighValueInactive"] = filtered_df.apply(
    lambda row: "Yes" if row["Balance"] > 100000 and row["IsActiveMember"] == 0 else "No",
    axis=1
)

# -------------------------
# KPIs
# -------------------------
total = len(filtered_df)
churn = filtered_df[filtered_df["Exited"] == 1].shape[0]
churn_rate = (churn / total) * 100

avg_age = filtered_df["Age"].mean()
avg_balance = filtered_df["Balance"].mean()
avg_salary = filtered_df["EstimatedSalary"].mean()

# -------------------------
# HEADER
# -------------------------
st.title("European Bank Dashboard")
st.caption("Power BI Styled • Glass UI • Advanced Analytics")

# -------------------------
# KPI SECTION
# -------------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric("Customers", total)
col2.metric("Churn Rate", f"{churn_rate:.2f}%")
col3.metric("Avg Balance", f"{avg_balance:,.0f}")
col4.metric("Avg Salary", f"{avg_salary:,.0f}")

# -------------------------
# PLOTLY TEMPLATE (GLOBAL STYLE)
# -------------------------
custom_template = dict(
    layout=dict(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        title=dict(font=dict(size=20)),
    )
)

# =========================================================
# CHURN ANALYSIS
# =========================================================
st.subheader("Churn Analysis")

colA, colB = st.columns(2)

fig1 = px.pie(
    filtered_df,
    names="Exited",
    color="Exited",
    color_discrete_sequence=["#22C55E", "#EF4444"],
    title="Churn Distribution"
)
fig1.update_layout(template=custom_template)

colA.plotly_chart(fig1, use_container_width=True)

fig2 = px.bar(
    filtered_df,
    x="IsActiveMember",
    y="Exited",
    color="IsActiveMember",
    title="Churn vs Activity",
    color_discrete_sequence=["#6366F1", "#F59E0B"]
)
fig2.update_layout(template=custom_template)

colB.plotly_chart(fig2, use_container_width=True)

# =========================================================
# BALANCE
# =========================================================
st.subheader("Balance Insights")

colC, colD = st.columns(2)

fig3 = px.histogram(
    filtered_df,
    x="Balance",
    nbins=50,
    color_discrete_sequence=["#3B82F6"]
)
fig3.update_layout(template=custom_template)

colC.plotly_chart(fig3, use_container_width=True)

fig4 = px.box(
    filtered_df,
    x="Exited",
    y="Balance",
    color="Exited",
    color_discrete_sequence=["#22C55E", "#EF4444"]
)
fig4.update_layout(template=custom_template)

colD.plotly_chart(fig4, use_container_width=True)

# =========================================================
# PRODUCTS
# =========================================================
st.subheader("Product Intelligence")

fig5 = px.line(
    filtered_df.groupby("NumOfProducts")["Exited"].mean().reset_index(),
    x="NumOfProducts",
    y="Exited",
    markers=True,
    color_discrete_sequence=["#A855F7"]
)
fig5.update_layout(template=custom_template)

st.plotly_chart(fig5, use_container_width=True)

# =========================================================
# DEMOGRAPHICS
# =========================================================
st.subheader("Customer Segmentation")

colE, colF = st.columns(2)

fig6 = px.histogram(filtered_df, x="Age", color_discrete_sequence=["#F59E0B"])
fig6.update_layout(template=custom_template)

colE.plotly_chart(fig6, use_container_width=True)

fig7 = px.histogram(filtered_df, x="EstimatedSalary", color_discrete_sequence=["#10B981"])
fig7.update_layout(template=custom_template)

colF.plotly_chart(fig7, use_container_width=True)

# -------------------------
# INSIGHTS
# -------------------------
st.subheader("Key Insights")

st.info("""
• Inactive users show significantly higher churn probability  
• Customers with higher product count are more stable  
• High balance inactive users are the most critical risk segment  
""")

# -------------------------
# DATA TABLE
# -------------------------
with st.expander("View Dataset"):
    st.dataframe(filtered_df)

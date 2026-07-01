"""
Nassau Candy Distributor
Product Line Profitability & Margin Performance Dashboard
=========================================================
Run: streamlit run streamlit_app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Nassau Candy — Profitability Dashboard",
    page_icon="🍬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# STYLING
# ─────────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #FAFAFA; }
    .block-container { padding: 1.5rem 2rem 2rem 2rem; }
    .kpi-box {
        background: linear-gradient(135deg, #fff 0%, #f5f5f5 100%);
        border-radius: 16px;
        padding: 1.5rem 1rem;
        min-height: 110px;
        text-align: center;
        border-left: 5px solid #6B3E26;
        box-shadow: 0 8px 18px rgba(0,0,0,0.18);
    }
    .kpi-value { font-size: 1.7rem; font-weight: 700; color: #1a1a1a; }
    .kpi-label { font-size: 0.82rem; color: #555; margin-top: 6px; text-transform: uppercase; letter-spacing: 0.05em; }
    .risk-badge {
        background-color: #FFF3CD; border: 1px solid #FFCA28;
        border-radius: 6px; padding: 0.3rem 0.7rem;
        font-size: 0.8rem; color: #7D5000; display: inline-block; margin: 2px;
    }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        background: #242733; border-radius: 14px;
        padding: 12px 24px; font-weight: 600; color: #D6D8E0;
            border: 1px solid #3A3D4A; transition: all 0.25s ease;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, #A86A3A, #D58A43) !important;
        color: white !important;
        font-weight: 700;
            box-shadow: 0 4px 12px rgba(213,138,67,0.35);
    }
    h1 { color: #3D1E0F; }
    .section-title { font-size: 1.35rem; font-weight: 700; color: #FFFFFF; margin-top: 10px; margin-bottom: 8rem; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# COLORS
# ─────────────────────────────────────────────
DIV_COLORS = {"Chocolate": "#6B3E26", "Other": "#5B8DB8", "Sugar": "#E8A838"}

# ─────────────────────────────────────────────
# DATA LOADING
# ─────────────────────────────────────────────
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("../data/Nassau_Candy_Distributor.csv")
    except FileNotFoundError:
        df = pd.read_csv("data/Nassau_Candy_Distributor.csv")

    df["Order Date"] = pd.to_datetime(df["Order Date"], dayfirst=True)
    df["Ship Date"]  = pd.to_datetime(df["Ship Date"],  dayfirst=True)
    df["Product Name"] = df["Product Name"].str.strip()
    df = df[df["Sales"] > 0]

    df["Gross Margin (%)"] = (df["Gross Profit"] / df["Sales"]) * 100
    df["Profit per Unit"]  = df["Gross Profit"] / df["Units"]
    df["Cost Ratio (%)"]   = (df["Cost"] / df["Sales"]) * 100
    df["Month"]    = df["Order Date"].dt.to_period("M")
    df["Quarter"]  = df["Order Date"].dt.to_period("Q")
    df["Month_dt"] = df["Order Date"].dt.to_period("M").dt.to_timestamp()
    return df

df_raw = load_data()

# SIDEBAR FILTERS

with st.sidebar:
    st.markdown("""
# 🍬 Nassau Candy

### Profitability Dashboard
""")

    st.caption("Data Analytics Project")
    st.markdown("---")
    st.markdown("### 🔧 Filters")

    # Date range
    min_date = df_raw["Order Date"].min().date()
    max_date = df_raw["Order Date"].max().date()
    date_range = st.date_input("Order Date Range", value=(min_date, max_date),
                                min_value=min_date, max_value=max_date)

    # Division
    all_divs = sorted(df_raw["Division"].unique())
    selected_divs = st.multiselect("Division", all_divs, default=all_divs)

    # Margin threshold
    margin_min = st.slider("Min Margin % (filter products)", 0, 100, 0, step=5)

    # Product search
    product_search = st.text_input("🔍 Search Product Name", "")

    st.markdown("---")

    st.caption("""
---
© 2026 Anirudh Singh

Version 1.0

Built with
Python • Streamlit • Plotly • Pandas
""")
    


# ─────────────────────────────────────────────
# APPLY FILTERS
# ─────────────────────────────────────────────
df = df_raw.copy()
if len(date_range) == 2:
    df = df[(df["Order Date"].dt.date >= date_range[0]) &
            (df["Order Date"].dt.date <= date_range[1])]
if selected_divs:
    df = df[df["Division"].isin(selected_divs)]
if product_search:
    df = df[df["Product Name"].str.contains(product_search, case=False, na=False)]

# ─────────────────────────────────────────────
# AGGREGATIONS
# ─────────────────────────────────────────────
def make_product_df(df):
    p = df.groupby(["Division", "Product Name"]).agg(
        Total_Sales  =("Sales",            "sum"),
        Total_Cost   =("Cost",             "sum"),
        Total_Profit =("Gross Profit",     "sum"),
        Total_Units  =("Units",            "sum"),
        Avg_Margin   =("Gross Margin (%)", "mean"),
        Order_Count  =("Order ID",         "count"),
    ).reset_index()
    p["Profit_per_Unit"]       = p["Total_Profit"] / p["Total_Units"]
    p["Revenue_Contrib_%"]     = p["Total_Sales"]  / p["Total_Sales"].sum()  * 100
    p["Profit_Contrib_%"]      = p["Total_Profit"] / p["Total_Profit"].sum() * 100
    p["Cost_Ratio_%"]          = p["Total_Cost"]   / p["Total_Sales"]         * 100
    return p

def make_division_df(df):
    d = df.groupby("Division").agg(
        Total_Sales  =("Sales",            "sum"),
        Total_Cost   =("Cost",             "sum"),
        Total_Profit =("Gross Profit",     "sum"),
        Total_Units  =("Units",            "sum"),
        Avg_Margin   =("Gross Margin (%)", "mean"),
    ).reset_index()
    return d

product_df  = make_product_df(df)
division_df = make_division_df(df)

# margin threshold filter for product charts
pf = product_df[product_df["Avg_Margin"] >= margin_min]

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.markdown("""
<h1 style="font-size:2.7rem;
font-weight:800;
color:white;
margin-bottom:0;">
🍭 Nassau Candy Profitability Dashboard
</h1>
""", unsafe_allow_html=True)

st.markdown("""
<p style="font-size:18px;
color:#B8BCC8;
margin-top:-5px;
margin-bottom:20px;">
Analyze product profitability, gross margins, cost efficiency and revenue performance through interactive business analytics.
</p>
""", unsafe_allow_html=True)

st.divider()


# ─────────────────────────────────────────────
# KPI ROW
# ─────────────────────────────────────────────
k1, k2, k3, k4, k5 = st.columns(5)

total_rev    = df["Sales"].sum()
total_profit = df["Gross Profit"].sum()
avg_margin   = df["Gross Margin (%)"].mean()
total_units  = df["Units"].sum()
total_orders = df["Order ID"].nunique()

for col, val, label, fmt in [
    (k1, total_rev,    "Total Revenue",    f"${total_rev:,.0f}"),
    (k2, total_profit, "Gross Profit",     f"${total_profit:,.0f}"),
    (k3, avg_margin,   "Avg Gross Margin", f"{avg_margin:.1f}%"),
    (k4, total_units,  "Units Sold",       f"{total_units:,}"),
    (k5, total_orders, "Total Orders",     f"{total_orders:,}"),
]:
    col.markdown(f"""
    <div class="kpi-box">
        <div class="kpi-value">{fmt}</div>
        <div class="kpi-label">{label}</div>
    </div>""", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "📦 Product Profitability",
    "🏭 Division Performance",
    "💰 Cost & Margin Diagnostics",
    "📊 Pareto & Concentration",
])

# ─────────────────────────────────────────────
# TAB 1 — PRODUCT PROFITABILITY
# ─────────────────────────────────────────────
with tab1:
    st.markdown('<div class="section-title">Product-Level Gross Profit & Margin Leaderboard</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    with c1:
        fig = px.bar(
            pf.sort_values("Total_Profit"),
            x="Total_Profit", y="Product Name",
            color="Division", color_discrete_map=DIV_COLORS,
            orientation="h",
            labels={"Total_Profit": "Gross Profit ($)", "Product Name": ""},
            title="Total Gross Profit by Product",
            text=pf.sort_values("Total_Profit")["Total_Profit"].apply(lambda x: f"${x:,.0f}"),
        )
        fig.update_traces(textposition="outside", textfont_size=10)
        fig.update_layout(height=480, legend_title="Division",
                          margin=dict(l=0, r=30, t=15, b=20), showlegend=True)
        st.plotly_chart(fig, width="stretch")

    with c2:
        fig2 = px.bar(
            pf.sort_values("Avg_Margin"),
            x="Avg_Margin", y="Product Name",
            color="Division", color_discrete_map=DIV_COLORS,
            orientation="h",
            labels={"Avg_Margin": "Gross Margin (%)", "Product Name": ""},
            title="Average Gross Margin % by Product",
            text=pf.sort_values("Avg_Margin")["Avg_Margin"].apply(lambda x: f"{x:.1f}%"),
        )
        fig2.add_vline(x=50, line_dash="dash", line_color="red", annotation_text="50% threshold",
                       annotation_position="top right")
        fig2.update_traces(textposition="outside", textfont_size=10)
        fig2.update_layout(height=480, showlegend=False,
                            margin=dict(l=0, r=60, t=40, b=20), xaxis_range=[0, 100])
        st.plotly_chart(fig2, width="stretch")

    st.markdown('<div class="section-title">Profit Contribution by Product</div>', unsafe_allow_html=True)
    c3, c4 = st.columns([1, 1])

    with c3:
        fig3 = px.pie(
            pf, values="Profit_Contrib_%", names="Product Name",
            color="Division", color_discrete_map=DIV_COLORS,
            title="Profit Share by Product",
            hole=0.45,
        )
        fig3.update_traces(textinfo="percent+label", textfont_size=9)
        fig3.update_layout(height=380, showlegend=False, margin=dict(t=40, b=10, l=0, r=0))
        st.plotly_chart(fig3, width="stretch")

    with c4:
        st.markdown("**Product Margin Leaderboard**")
        leaderboard = pf[["Product Name","Division","Total_Sales","Total_Profit","Avg_Margin","Profit_per_Unit"]].copy()
        leaderboard.columns = ["Product","Division","Revenue","Profit","Margin %","Profit/Unit"]
        leaderboard = leaderboard.sort_values("Profit", ascending=False)
        leaderboard["Revenue"]     = leaderboard["Revenue"].apply(lambda x: f"${x:,.0f}")
        leaderboard["Profit"]      = leaderboard["Profit"].apply(lambda x: f"${x:,.0f}")
        leaderboard["Margin %"]    = leaderboard["Margin %"].apply(lambda x: f"{x:.1f}%")
        leaderboard["Profit/Unit"] = leaderboard["Profit/Unit"].apply(lambda x: f"${x:.2f}")
        st.dataframe(leaderboard.reset_index(drop=True), width="stretch", height=340)

    # Monthly margin trend
    st.markdown('<div class="section-title">Monthly Gross Margin Trend by Division</div>', unsafe_allow_html=True)
    monthly = df.groupby(["Month_dt","Division"])["Gross Margin (%)"].mean().reset_index()
    fig4 = px.line(
        monthly, x="Month_dt", y="Gross Margin (%)", color="Division",
        color_discrete_map=DIV_COLORS, markers=True,
        labels={"Month_dt": "Month", "Gross Margin (%)": "Avg Gross Margin (%)"},
        title="Monthly Average Gross Margin by Division",
    )
    fig4.add_hline(y=avg_margin, line_dash="dot", line_color="gray",
                   annotation_text=f"Overall Avg {avg_margin:.1f}%")
    fig4.update_layout(height=350, margin=dict(t=40, b=20, l=0, r=0))
    st.plotly_chart(fig4, width="stretch")

# ─────────────────────────────────────────────
# TAB 2 — DIVISION PERFORMANCE
# ─────────────────────────────────────────────
with tab2:
    st.markdown('<div class="section-title">Division Revenue, Profit & Margin Overview</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    with c1:
        fig = go.Figure()
        fig.add_trace(go.Bar(name="Total Revenue", x=division_df["Division"], y=division_df["Total_Sales"],
                             marker_color=[DIV_COLORS[d] for d in division_df["Division"]], opacity=0.9,
                             text=division_df["Total_Sales"].apply(lambda x: f"${x:,.0f}"), textposition="outside"))
        fig.add_trace(go.Bar(name="Gross Profit", x=division_df["Division"], y=division_df["Total_Profit"],
                             marker_color=[DIV_COLORS[d] for d in division_df["Division"]], opacity=0.5,
                             text=division_df["Total_Profit"].apply(lambda x: f"${x:,.0f}"), textposition="outside"))
        fig.update_layout(barmode="group", title="Revenue vs. Gross Profit by Division",
                          height=520, yaxis_tickprefix="$", margin=dict(t=40,b=20,l=0,r=0))
        st.plotly_chart(fig, width="stretch")

    with c2:
        fig2 = px.bar(
            division_df.sort_values("Avg_Margin", ascending=False),
            x="Division", y="Avg_Margin",
            color="Division", color_discrete_map=DIV_COLORS,
            title="Average Gross Margin % by Division",
            text=division_df.sort_values("Avg_Margin", ascending=False)["Avg_Margin"].apply(lambda x: f"{x:.1f}%"),
        )
        fig2.update_traces(textposition="outside")
        fig2.add_hline(y=50, line_dash="dash", line_color="red", annotation_text="50% min target")
        fig2.update_layout(height=380, showlegend=False, yaxis_range=[0, 90],
                           margin=dict(t=40, b=20, l=0, r=0))
        st.plotly_chart(fig2, width="stretch")

    st.markdown('<div class="section-title">Division Summary Table</div>', unsafe_allow_html=True)
    div_table = division_df.copy()
    div_table["Revenue Share %"] = div_table["Total_Sales"] / div_table["Total_Sales"].sum() * 100
    div_table["Profit Share %"]  = div_table["Total_Profit"] / div_table["Total_Profit"].sum() * 100
    div_table["Total_Sales"]     = div_table["Total_Sales"].apply(lambda x: f"${x:,.0f}")
    div_table["Total_Cost"]      = div_table["Total_Cost"].apply(lambda x: f"${x:,.0f}")
    div_table["Total_Profit"]    = div_table["Total_Profit"].apply(lambda x: f"${x:,.0f}")
    div_table["Total_Units"]     = div_table["Total_Units"].apply(lambda x: f"{x:,}")
    div_table["Avg_Margin"]      = div_table["Avg_Margin"].apply(lambda x: f"{x:.1f}%")
    div_table["Revenue Share %"] = div_table["Revenue Share %"].apply(lambda x: f"{x:.1f}%")
    div_table["Profit Share %"]  = div_table["Profit Share %"].apply(lambda x: f"{x:.1f}%")
    div_table.columns = ["Division","Revenue","Total Cost","Gross Profit","Units","Avg Margin","Rev Share","Profit Share"]
    st.dataframe(div_table, width="stretch",height=520)

    st.markdown('<div class="section-title">Regional Performance</div>', unsafe_allow_html=True)
    region_df = df.groupby("Region").agg(
        Total_Sales  =("Sales",            "sum"),
        Total_Profit =("Gross Profit",     "sum"),
        Avg_Margin   =("Gross Margin (%)", "mean"),
        Order_Count  =("Order ID",         "count"),
    ).reset_index()

    fig3 = px.bar(
        region_df.sort_values("Total_Profit", ascending=False),
        x="Region", y=["Total_Sales", "Total_Profit"],
        barmode="group", title="Revenue vs Profit by Region",
        color_discrete_sequence=["#5B8DB8", "#2ECC71"],
        labels={"value": "Amount ($)", "variable": "Metric"},
    )
    fig3.update_layout(height=520, yaxis_tickprefix="$", margin=dict(t=40,b=20,l=0,r=0))
    st.plotly_chart(fig3, width="stretch")

# ─────────────────────────────────────────────
# TAB 3 — COST & MARGIN DIAGNOSTICS
# ─────────────────────────────────────────────
with tab3:
    st.markdown('<div class="section-title">Sales vs. Gross Profit Scatter — Cost Diagnostic</div>', unsafe_allow_html=True)

    pf2 = pf.copy()
    pf2["Risk Flag"] = pf2["Cost_Ratio_%"].apply(lambda x: "⚠️ Cost Risk (>60%)" if x > 60 else "✅ Healthy")
    pf2["Bubble Size"] = np.sqrt(pf2["Total_Units"]) * 3

    fig = px.scatter(
        pf2, x="Total_Sales", y="Total_Profit",
        color="Division", size="Total_Units",
        color_discrete_map=DIV_COLORS,
        symbol="Risk Flag",
        symbol_map={"⚠️ Cost Risk (>60%)": "x", "✅ Healthy": "circle"},
        hover_name="Product Name",
        hover_data={"Total_Sales": ":$,.0f", "Total_Profit": ":$,.0f",
                    "Avg_Margin": ":.1f", "Cost_Ratio_%": ":.1f",
                    "Total_Units": ":,"},
        labels={"Total_Sales": "Total Sales ($)", "Total_Profit": "Gross Profit ($)"},
        title="Sales vs. Gross Profit — Bubble Size = Units Sold",
    )

    # Margin guide lines
    max_s = pf2["Total_Sales"].max()
    for pct, label, color in [(0.7, "70% margin", "green"), (0.5, "50% margin", "orange"), (0.3, "30% margin", "red")]:
        fig.add_trace(go.Scatter(x=[0, max_s], y=[0, max_s * pct], mode="lines",
                                 line=dict(dash="dot", color=color, width=1.2),
                                 name=label, showlegend=True))

    fig.update_layout(height=480, margin=dict(t=40, b=20, l=0, r=0))
    st.plotly_chart(fig, width="stretch")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="section-title">Cost Ratio by Product</div>', unsafe_allow_html=True)
        fig2 = px.bar(
            pf.sort_values("Cost_Ratio_%", ascending=False),
            x="Product Name", y="Cost_Ratio_%",
            color="Division", color_discrete_map=DIV_COLORS,
            title="Cost Ratio % by Product (lower = better)",
            labels={"Cost_Ratio_%": "Cost / Sales (%)"},
        )
        fig2.add_hline(y=60, line_dash="dash", line_color="red", annotation_text="Risk Threshold 60%")
        fig2.update_layout(height=350, showlegend=False,
                           margin=dict(t=40, b=60, l=0, r=0), xaxis_tickangle=-30)
        st.plotly_chart(fig2, width="stretch")

    with c2:
        st.markdown('<div class="section-title">⚠️ Margin Risk Flags</div>', unsafe_allow_html=True)
        risk_products = pf[pf["Cost_Ratio_%"] > 60].sort_values("Cost_Ratio_%", ascending=False)
        if len(risk_products) > 0:
            for _, r in risk_products.iterrows():
                st.markdown(f"""
                <div style="background:#FFF3CD;border:1px solid #FFCA28;border-radius:8px;
                             padding:0.7rem 1rem;margin-bottom:0.6rem;">
                  <strong>{r['Product Name']}</strong> ({r['Division']})<br>
                  Cost Ratio: <strong style="color:#c0392b">{r['Cost_Ratio_%']:.1f}%</strong> &nbsp;|&nbsp;
                  Margin: <strong>{r['Avg_Margin']:.1f}%</strong> &nbsp;|&nbsp;
                  Revenue: ${r['Total_Sales']:,.0f}
                  <br><small>Action: Repricing / Cost renegotiation / Discontinuation review</small>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.success("No products above 60% cost ratio with current filters.")

    st.markdown('<div class="section-title">Profit per Unit Heatmap (Quarter × Product)</div>', unsafe_allow_html=True)
    pivot = df.groupby(["Quarter", "Product Name"])["Profit per Unit"].mean().unstack(fill_value=0)
    pivot.index = pivot.index.astype(str)
    fig3 = px.imshow(
        pivot, text_auto=".2f", color_continuous_scale="YlOrRd",
        title="Average Profit per Unit — Quarter × Product",
        labels=dict(color="$/unit"),
    )
    fig3.update_layout(height=320, margin=dict(t=40, b=20, l=0, r=0))
    st.plotly_chart(fig3, width="stretch")

# ─────────────────────────────────────────────
# TAB 4 — PARETO & CONCENTRATION
# ─────────────────────────────────────────────
with tab4:
    st.markdown('<div class="section-title">Pareto Analysis — Profit Concentration</div>', unsafe_allow_html=True)

    pareto = pf.sort_values("Total_Profit", ascending=False).copy()
    pareto["Cum_Profit_%"] = pareto["Total_Profit"].cumsum() / pareto["Total_Profit"].sum() * 100
    pareto["Rank"] = range(1, len(pareto) + 1)

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    bar_colors = [DIV_COLORS.get(d, "#999") for d in pareto["Division"]]

    fig.add_trace(go.Bar(x=pareto["Product Name"], y=pareto["Total_Profit"],
                         name="Gross Profit", marker_color=bar_colors, opacity=0.85,
                         text=pareto["Total_Profit"].apply(lambda x: f"${x:,.0f}"),
                         textposition="outside"), secondary_y=False)

    fig.add_trace(go.Scatter(x=pareto["Product Name"], y=pareto["Cum_Profit_%"],
                             mode="lines+markers+text", name="Cumulative %",
                             line=dict(color="#E05C2A", width=2.5),
                             marker=dict(size=8),
                             text=pareto["Cum_Profit_%"].apply(lambda x: f"{x:.0f}%"),
                             textposition="top center", textfont=dict(size=9)),
                  secondary_y=True)

    fig.add_hline(y=80, secondary_y=True, line_dash="dash", line_color="red",
                  annotation_text="80% profit line", annotation_position="right")

    fig.update_layout(title="Pareto Chart — Cumulative Profit Concentration",
                      height=450, xaxis_tickangle=-30,
                      margin=dict(t=40, b=80, l=0, r=60))
    fig.update_yaxes(title_text="Gross Profit ($)", tickprefix="$", secondary_y=False)
    fig.update_yaxes(title_text="Cumulative Profit (%)", range=[0, 115], secondary_y=True)
    st.plotly_chart(fig, width="stretch")

    c1, c2 = st.columns(2)

    with c1:
        st.markdown('<div class="section-title">Revenue Contribution vs. Profit Contribution</div>', unsafe_allow_html=True)
        fig2 = px.scatter(
            pf, x="Revenue_Contrib_%", y="Profit_Contrib_%",
            color="Division", size="Total_Units",
            color_discrete_map=DIV_COLORS,
            hover_name="Product Name",
            title="Revenue Share vs. Profit Share",
            labels={"Revenue_Contrib_%": "Revenue Contribution (%)",
                    "Profit_Contrib_%": "Profit Contribution (%)"},
        )
        fig2.add_shape(type="line", x0=0, y0=0, x1=100, y1=100,
                       line=dict(dash="dot", color="gray", width=1))
        fig2.update_layout(height=380, margin=dict(t=40, b=20, l=0, r=0))
        st.plotly_chart(fig2, width="stretch")

    with c2:
        st.markdown('<div class="section-title">Pareto Table</div>', unsafe_allow_html=True)
        pareto_table = pareto[["Rank","Product Name","Division","Total_Profit","Profit_Contrib_%","Cum_Profit_%"]].copy()
        pareto_table["Total_Profit"]    = pareto_table["Total_Profit"].apply(lambda x: f"${x:,.0f}")
        pareto_table["Profit_Contrib_%"]= pareto_table["Profit_Contrib_%"].apply(lambda x: f"{x:.1f}%")
        pareto_table["Cum_Profit_%"]    = pareto_table["Cum_Profit_%"].apply(lambda x: f"{x:.1f}%")
        pareto_table.columns = ["#","Product","Division","Gross Profit","Contribution","Cumulative %"]
        st.dataframe(pareto_table, width="stretch", height=360)

    # Summary callouts
    st.markdown("---")
    top_n = len(pareto[pareto["Cum_Profit_%"] <= 80])
    total_skus = len(pareto)
    top5_pct = pareto.head(5)["Profit_Contrib_%"].sum() if len(pareto) >= 5 else pareto["Profit_Contrib_%"].sum()

    col1, col2, col3 = st.columns(3)
    col1.metric("Products driving 80% of profit", f"{top_n} of {total_skus}")
    col2.metric("Top 5 products profit share", f"{top5_pct:.1f}%")
    col3.metric("Concentration risk", "HIGH" if top5_pct > 80 else "MODERATE")

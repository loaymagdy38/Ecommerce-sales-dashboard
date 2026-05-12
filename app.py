import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

df = pd.read_csv("data/cleaned_data.csv", encoding="latin1")
#--------------------- Column Chart ------------------------
sales_by_category = df.groupby("category")["sales"].sum().reset_index()
sales_by_category = sales_by_category.sort_values("sales", ascending=False).reset_index(drop=True)

sales_by_category["type"] = "Standard"
sales_by_category.loc[0, "type"] = "Max"

fig_column = px.bar(
    sales_by_category,
    x="category",
    y="sales",
    title="Total Sales by Category",
    text=sales_by_category["sales"]/1000,
    color="type",
)

fig_column.update_traces(
    texttemplate="%{text:.0f}K",
    textposition="outside"
)

color_map = {
    "Max": "#1E88E5",
    "Standard": "#BBDEFB"
}

fig_column.for_each_trace(
    lambda t: t.update(marker_color=color_map[t.name])
)
fig_column.update_layout(
    xaxis_title="Product Category",
    yaxis_title="Total Sales",
    template="plotly_white",
    yaxis_showgrid=True,
    legend_title="Type",
    title={
    "text": "Total Sales by Category",
    "x": 0.5,
    "y": 0.9,
    "xanchor": "center"
},

)
fig_column.update_xaxes(showline=True, linewidth=1, linecolor='black')
fig_column.update_yaxes(showline=True, linewidth=1, linecolor='black')

fig_column.update_yaxes(range=[0, 950000])

#--------------  Bar Chart ----------------
profit_by_region = df.groupby("region")["profit"].sum().reset_index()
profit_by_region = profit_by_region.sort_values("profit", ascending=False).reset_index(drop=True)

profit_by_region["type"] = "Standard"
profit_by_region.loc[0, "type"] = "Max"

fig_bar = px.bar(
    profit_by_region,
    x="profit",
    y="region",
    title="Total Profit by Region",
    color="type",
    text=profit_by_region["profit"] / 1000
)

fig_bar.update_yaxes(autorange="reversed")

fig_bar.update_traces(
    texttemplate="%{text:.0f}K",
    textposition="outside"
)

color_map = {
    "Max": "#1E88E5",
    "Standard": "#BBDEFB"
}

fig_bar.for_each_trace(
    lambda t: t.update(marker_color=color_map[t.name])
)

fig_bar.update_layout(
    xaxis_title="Total Profit",
    yaxis_title="Region",
    template="plotly_white",
    xaxis_showgrid=True,
    legend_title="Type",
    title={
        "text": "Total Profit by Region",
        "x": 0.5,
        "y": 0.9,
        "xanchor": "center"
    }
)

fig_bar.update_xaxes(range=[0, 120000])
fig_bar.update_xaxes(showline=True, linewidth=2, linecolor='black')
fig_bar.update_yaxes(showline=True, linewidth=1, linecolor='black')
#--------------  Stacked Column Chart ----------------
sales_cat_seg=df.groupby(["category","segment"])["sales"].sum().reset_index()
sales_cat_seg=sales_cat_seg.sort_values(by="sales",ascending=False)

total_sales = sales_cat_seg.groupby("category")["sales"].sum().reset_index()

fig_Stacked_Column=px.bar(sales_cat_seg,
           color="segment",
           x="category",
           y="sales",
           title="Sales by Category and segment",
           text=sales_cat_seg["sales"] / 1000,
            orientation="v",
            barmode  = 'stack'
        )

fig_Stacked_Column.update_traces(
    texttemplate='%{text:.0f}K',
    textposition="inside"

)

for i, row in total_sales.iterrows():
    fig_Stacked_Column.add_annotation(
        x=row["category"],
        y=row["sales"],
        text=f"Total: {row['sales']/1000:.0f}K",
        showarrow=False,
        yshift=12,
        font=dict(size=12, color="black")
    )


fig_Stacked_Column.update_layout(
    xaxis_title="Product Category",
    yaxis_title="Total sales", 
    xaxis_showgrid=True, 
    template="plotly_white",
    legend_title="Segment",
      title={ "text": "Sales by Category and segment",
    "x": 0.5,
    "y": 0.9,
    "xanchor": "center"}
)

fig_Stacked_Column.update_xaxes(showline=True, linewidth=1, linecolor='black')
fig_Stacked_Column.update_yaxes(showline=True, linewidth=1, linecolor='black')
#--------------  Stacked Bar Chart ----------------

pro_reg_seg=df.groupby(["region","segment"])["profit"].sum().reset_index()
pro_reg_seg=pro_reg_seg.sort_values("profit",ascending=False)

Total_profit = pro_reg_seg.groupby("region")["profit"].sum().reset_index()

fig_Stacked_Bar=px.bar(
    pro_reg_seg,
    x="profit",
    y="region",
    title="Profit by Region & Segment",
    color="segment",
    text=pro_reg_seg["profit"]/1000,
    orientation="h",
    barmode  = 'stack',
)

fig_Stacked_Bar.update_yaxes(autorange="reversed")


fig_Stacked_Bar.update_traces(
    texttemplate='%{text:.0f}K',
    textposition="inside"
)

for i, row in Total_profit.iterrows():
    fig_Stacked_Bar.add_annotation(
        x=row["profit"],
        y=row["region"],
        text=f"Total: {row['profit']/1000:.0f}K",
        showarrow=False,
        xshift=40,
        font=dict(size=12, color="black")
    )


fig_Stacked_Bar.update_layout(
    xaxis_title="Total profit",
    yaxis_title="Region",
    xaxis_showgrid=True,
    template="plotly_white",
    legend_title="Segment",
    title={
        "text": "Profit Distribution",
        "x": 0.5,
        "y": 0.9,
        "xanchor": "center"
    }
    
)

fig_Stacked_Bar.update_xaxes(showline=True, linewidth=2, linecolor='black')
fig_Stacked_Bar.update_yaxes(showline=True, linewidth=1, linecolor='black')
#--------------       Clustred column Chart      ------------------
sale_cate_seg_col=df.groupby(["category","segment"])["sales"].sum().reset_index()
sale_cate_seg_col=sale_cate_seg_col.sort_values("sales",ascending=False)

fig_clus_clumon=px.bar(
    sale_cate_seg_col,
    x="category",
    y="sales",
    title="Sales by Category & Segment",
    color="segment",
    barmode="group", #*** 
    text=sale_cate_seg_col["sales"]/1000,
    orientation="v",
)

fig_clus_clumon.update_traces(
    texttemplate='%{text:.0f}K',
    textposition="outside"
    )
fig_clus_clumon.update_layout(
    xaxis_title="Product Category",
    yaxis_title="Total Sales",
    yaxis_showgrid=True,
    template="plotly_white",
    legend_title="Segment",
    title={ "text": "Sales by Category & Segment",
    "x": 0.5,
    "y": 0.9,
    "xanchor": "center"}

)
fig_clus_clumon.update_xaxes(showline=True, linewidth=1, linecolor='black')
fig_clus_clumon.update_yaxes(showline=True, linewidth=1, linecolor='black')
#--------------  Clustred Bar Chart ----------------
pro_reg_seg_bar=df.groupby(["region","segment"])["profit"].sum().reset_index()
pro_reg_seg_bar=pro_reg_seg_bar.sort_values("profit",ascending=False)

fig_clus_bar=px.bar(
    pro_reg_seg_bar,
    x="profit",
    y="region",
    title="Profit by Region & Segment",
    color="segment",
    text=pro_reg_seg_bar["profit"]/1000,
    barmode="group",
    orientation="h",
    )

fig_clus_bar.update_yaxes(autorange="reversed")


fig_clus_bar.update_traces(
    texttemplate='%{text:.0f}K',
    textposition="outside")

fig_clus_bar.update_layout(
    xaxis_title="Total Profit",
    yaxis_title="Region",
    xaxis_showgrid=True,
    template="plotly_white",
    legend_title="Segment",
    title={
        "text": "Profit by Region & Segment",
        "x": 0.5,
        "y": 0.9,
        "xanchor": "center"
    }

    )
fig_clus_bar.update_xaxes(showline=True, linewidth=1, linecolor='black')
fig_clus_bar.update_yaxes(showline=True, linewidth=1, linecolor='black')
#--------------  Scatter Plot ----------------
df["outlier"] = (df["sales"] > 1000) & (df["profit"] < 0)
df["point_type"] = df["outlier"].apply(
    lambda x: "Outlier" if x else "Normal"
)

fig_scatter = px.scatter(
    df,
    x="sales",
    y="profit",
    title="Sales vs Profit (Outliers Highlighted)",
    color="point_type",
    hover_data=["category", "sub_category", "region", "segment"],
    opacity=0.6
)

color_map = {
    "Normal": "#90CAF9",
    "Outlier": "#A6EF46"  
}

fig_scatter.for_each_trace(
    lambda t: t.update(marker_color=color_map[t.name])
)
fig_scatter.update_traces(
    marker=dict(size=7, line=dict(width=1, color="black"))
)

fig_scatter.update_layout(
    xaxis_title="Sales (K)",
    yaxis_title="Profit (K)",
    template="plotly_white",
    xaxis_showgrid=True,
    yaxis_showgrid=True,
    legend_title="Point Type",
    title={ "text": "Scatter Chart Sales vs Profit with Quantity",
    "x": 0.5,
    "y": 0.9,
    "xanchor": "center"}
)

fig_scatter.update_xaxes(showline=True, linewidth=1, linecolor='black')
fig_scatter.update_yaxes(showline=True, linewidth=1, linecolor='black')
#--------------  Bubble Plot ----------------
df["outlier"] = (df["profit"] < 0) | (df["quantity"] > df["quantity"].quantile(0.95))
df["point_type"] = df["outlier"].apply(
    lambda x: "Outlier" if x else "Normal"
)

fig_Bubble=px.scatter(
    df,
    x="sales",
    y="profit",
    size="quantity",
    color="point_type",
    title="Bubble Chart Sales vs Profit with Quantity",
    hover_data=["category", "sub_category", "region", "segment"],
    opacity=0.35,
    size_max=40
    )

color_map = {
    "Normal": "#90CAF9",
    "Outlier": "#A6EF46"  
}

fig_Bubble.for_each_trace(
    lambda t: t.update(marker_color=color_map[t.name])
)

fig_Bubble.update_traces(
    marker=dict(
        sizemode="area",
        sizeref=2.*max(df["quantity"])/(40**2),
        line=dict(width=1, color="black")
    )
)

fig_Bubble.update_layout(
    xaxis_title="Sales (K)",
    yaxis_title="Profit (K)",
    template="plotly_white",
    xaxis_showgrid=True,
    yaxis_showgrid=True,
    legend_title="Point Type",
    title={ "text": "Bubble Chart Sales vs Profit with Quantity",
    "x": 0.5,
    "y": 0.9,
    "xanchor": "center"}
)

fig_Bubble.add_scatter(
    x=[30000, 30000, 30000],
    y=[8000, 6000, 3500],
    mode="markers+text",
    marker=dict(
        size=[10, 25, 40],
        color="gray",
        opacity=0.5
    ),
    text=["Low", "Med", "High"],
    textposition="middle right",
    showlegend=False
)

fig_Bubble.update_xaxes(showline=True, linewidth=1, linecolor='black')
fig_Bubble.update_yaxes(showline=True, linewidth=1, linecolor='black')
#--------------  Histogram Chart ----------------

fig_hist = px.histogram(
    df,
    x="quantity",
    nbins=15,
    title="Distribution of Profit",
    color_discrete_sequence=["#7F8D80"]
)

fig_hist.update_traces(
    texttemplate='%{y}',
    textposition='outside',
    cliponaxis=False
)

fig_hist.update_layout(
    xaxis_title="quantity",
    yaxis_title="Frequency",
    template="plotly_white",
    yaxis_showgrid=True,
    title={ "text": "Histogram  — quantity Distribution",
    "x": 0.5,
    "y": 0.9,
    "xanchor": "center"},
        margin=dict(l=80, r=40, t=90, b=50)

)



fig_hist.update_xaxes(showline=True, linewidth=1, linecolor='black')
fig_hist.update_yaxes(showline=True, linewidth=1, linecolor='black')
#--------------  Box Chart ----------------
fig_Box = px.box(
    df,
    y="profit",
    title="Profit Distribution",
    color_discrete_sequence=["#3F51B5"]
    ,points='outliers',
    

)

fig_Box.update_traces(
    marker=dict(color="#E53935", size=6),
    line=dict(color="#90CAF9"))

fig_Box.add_scatter( ## legend
    x=[None],
    y=[None],
    mode="markers",
    marker=dict(color="#90CAF9", size=8), 
    name="Standard"
)

fig_Box.data[0].name = "Outliers"
fig_Box.data[0].showlegend = True

fig_Box.update_yaxes(range=[-500, 500])

fig_Box.update_layout(
    yaxis_title="Profit",
    template="plotly_white",
    yaxis_showgrid=True,
    xaxis_title="Profit",
    title={
        "text": "Profit Distribution",
        "x": 0.5,
        "y": 0.9,
        "xanchor": "center"
    }
)
median_profit = df["profit"].median()

fig_Box.add_annotation(
    x=0,
    y=median_profit,
    text=f"Median: {median_profit:.2f}",
    showarrow=True,
    arrowhead=2,
    ax=80,
    ay=0,
    bgcolor="white",
    bordercolor="black",
    font=dict(color="black")
)

fig_Box.update_xaxes(showline=True, linewidth=2, linecolor='black')
fig_Box.update_yaxes(showline=True, linewidth=2, linecolor='black')

q1 = df["profit"].quantile(0.25)
median = df["profit"].median()
q3 = df["profit"].quantile(0.75)
minimum = df["profit"].min()
maximum = df["profit"].max()

fig_Box.add_annotation(
    x=0.35,
    y=250,
    text=(
        f"Max: {maximum:.0f}<br>"
        f"Q3: {q3:.2f}<br>"
        f"Median: {median:.2f}<br>"
        f"Q1: {q1:.2f}<br>"
        f"Min: {minimum:.0f}"
    ),
    showarrow=False,
    align="left",
    bgcolor="white",
    bordercolor="black",
    font=dict(size=11, color="black")
)
#--------------  Violin Chart ----------------
fig_violin=px.violin(
    df,
    y="profit",
    box=True,
    title="Violin Plot — Profit Distribution",
    color_discrete_sequence=["#CAC1CE"]
)

fig_violin.update_layout(
    height=600,
    width=900,    
    yaxis_title="Profit",
    template="plotly_white",
    yaxis_showgrid=True,
    xaxis_title="Profit Distribution",
    title={ "text": "Violin Plot — Profit Distribution",
    "x": 0.5,
    "y": 0.9,
    "xanchor": "center"}
    
    )
fig_violin.update_yaxes(range=[-1000, 1000])

median_profit = df["profit"].median()

fig_violin.add_annotation(
    x=0,
    y=median_profit,
    text=f"Median: {median_profit:.2f}",
    showarrow=True,
    arrowhead=2,
    ax=80,
    ay=0,
    font=dict(size=12, color="black"),
    bgcolor="white",
    bordercolor="black"
)


fig_violin.update_xaxes(showline=True, linewidth=1, linecolor='black')
fig_violin.update_yaxes(showline=True, linewidth=1, linecolor='black')
#--------------  Line Chart ----------------
sales_over_time=df.groupby("year_month")["sales"].sum().reset_index()
sales_over_time["year_month"] = pd.to_datetime(sales_over_time["year_month"])

sales_over_time=sales_over_time.sort_values("year_month",ascending=True)



fig_line=px.line(
    sales_over_time,
    x="year_month",
    y="sales",
    title="Sales Trend Over Time",
    markers=True   #  يظهر نقط على الخط
    )

fig_line.update_layout(
    xaxis_title="Time",
    yaxis_title="Total Sales",
    xaxis_showgrid=True,
    yaxis_showgrid=True,
    template="plotly_white"
    )

#--------------  Area Chart ----------------
profit_over_time=df.groupby("year_month")["profit"].sum().reset_index()
profit_over_time["year_month"] = pd.to_datetime(profit_over_time["year_month"])
profit_over_time=profit_over_time.sort_values("year_month",ascending=True)

fig_area=px.area(
    profit_over_time,
    x="year_month",
    y="profit",
    title="(Area Chart) profit Over Time "
    )

fig_area.update_layout(
    xaxis_title="Time",
    yaxis_title="Total profit",
    template="plotly_white",
    xaxis_showgrid=True,
    yaxis_showgrid=True,
    title={ "text": "(Area Chart) profit Over Time",
    "x": 0.5,
    "y": 0.9,
    "xanchor": "center"}
)
fig_area.update_xaxes(showline=True, linewidth=1, linecolor='black')
fig_area.update_yaxes(showline=True, linewidth=1, linecolor='black')

#--------------  App ----------------

    
for fig in [
    fig_Stacked_Column,
    fig_Stacked_Bar,
    fig_clus_clumon,
    fig_clus_bar
]:
    fig.update_layout(
        height=300,
        margin=dict(l=80, r=40, t=60, b=50)
    )

for fig in [fig_hist, fig_Box, fig_violin]:
    fig.update_layout(
        height=220,
        width=None,
        autosize=True,
        margin=dict(l=80, r=40, t=60, b=50)
    )
app = Dash(__name__)

CARD_50 = {
    "width": "calc(50% - 10px)",
    "height": "360px",
    "backgroundColor": "white",
    "padding": "10px",
    "borderRadius": "14px",
    "boxShadow": "0 4px 12px rgba(0,0,0,0.08)",
    "boxSizing": "border-box"
}

CARD_33 = {
    "width": "calc(33.33% - 14px)",
    "height": "340px",
    "backgroundColor": "white",
    "padding": "10px",
    "borderRadius": "14px",
    "boxShadow": "0 4px 12px rgba(0,0,0,0.08)",
    "boxSizing": "border-box"
}

CARD_25 = {
    "width": "calc(33.33% - 14px)",
    "height": "260px",
    "backgroundColor": "white",
    "padding": "10px",
    "borderRadius": "14px",
    "boxShadow": "0 4px 12px rgba(0,0,0,0.08)",
    "boxSizing": "border-box",
    "overflow": "hidden"
}

ROW_STYLE = {
    "display": "flex",
    "gap": "20px",
    "flexWrap": "wrap",
    "marginBottom": "22px"
}

SECTION_TITLE = {
    "color": "#1E3A5F",
    "borderLeft": "6px solid #1E88E5",
    "paddingLeft": "12px",
    "marginTop": "30px"
}

app.layout = html.Div([

    html.Div([
        html.H1(
            "E-Commerce Sales Performance Dashboard",
            style={
                "textAlign": "center",
                "color": "#0B2545",
                "marginBottom": "8px"
            }
        ),
        html.P(
            "Interactive analysis of sales, profit, segments, categories, and time trends",
            style={
                "textAlign": "center",
                "color": "#607D8B",
                "fontSize": "16px"
            }
        )
    ], style={
        "backgroundColor": "white",
        "padding": "20px",
        "borderRadius": "16px",
        "boxShadow": "0 4px 14px rgba(0,0,0,0.08)",
        "marginBottom": "20px"
    }),

    html.Div([
        html.Div([
            html.Label("Select Region:", style={"fontWeight": "bold"}),
            dcc.Dropdown(
                id="region-filter",
                options=[{"label": r, "value": r} for r in sorted(df["region"].unique())],
                value="West",
                clearable=False
            )
        ], style={"flex": "1 1 30%", "minWidth": "280px"}),

        html.Div([
            html.Label("Select Categories:", style={"fontWeight": "bold"}),
            dcc.Checklist(
                id="category-filter",
                options=[{"label": c, "value": c} for c in sorted(df["category"].unique())],
                value=sorted(df["category"].unique()),
                inline=True
            )
        ], style={"flex": "1 1 35%", "minWidth": "300px"}),

        html.Div([
            html.Label("Select Year:", style={"fontWeight": "bold"}),
            dcc.Slider(
                id="year-slider",
                min=int(df["year"].min()),
                max=int(df["year"].max()),
                step=1,
                value=int(df["year"].max()),
                marks={int(y): str(y) for y in sorted(df["year"].unique())}
            )
        ], style={"flex": "1 1 30%", "minWidth": "300px"})

    ], style={
        **ROW_STYLE,
        "backgroundColor": "white",
        "padding": "18px",
        "borderRadius": "16px",
        "boxShadow": "0 4px 12px rgba(0,0,0,0.08)"
    }),

    html.H2("Comparison Charts", style=SECTION_TITLE),

    html.Div([
        dcc.Graph(id="column-chart", style=CARD_50, config={"displayModeBar": False}),
        dcc.Graph(id="bar-chart", style=CARD_50, config={"displayModeBar": False})
    ], style=ROW_STYLE),

    html.Div([
        dcc.Graph(figure=fig_Stacked_Column, style=CARD_50, config={"displayModeBar": False}),
        dcc.Graph(figure=fig_Stacked_Bar, style=CARD_50, config={"displayModeBar": False})
    ], style=ROW_STYLE),

    html.Div([
        dcc.Graph(figure=fig_clus_clumon, style=CARD_50, config={"displayModeBar": False}),
        dcc.Graph(figure=fig_clus_bar, style=CARD_50, config={"displayModeBar": False})
    ], style=ROW_STYLE),

    html.H2("Relationship Charts", style=SECTION_TITLE),

    html.Div([
        dcc.Graph(id="scatter-chart", style=CARD_50, config={"displayModeBar": False}),
        dcc.Graph(id="bubble-chart", style=CARD_50, config={"displayModeBar": False})
    ], style=ROW_STYLE),

    html.H2("Distribution Charts", style=SECTION_TITLE),

    html.Div([
        dcc.Graph(figure=fig_hist, style=CARD_25, config={"displayModeBar": False}),
        dcc.Graph(figure=fig_Box, style=CARD_25, config={"displayModeBar": False}),
        dcc.Graph(figure=fig_violin, style=CARD_25, config={"displayModeBar": False})
    ], style=ROW_STYLE),

    html.H2("Time Series Charts", style=SECTION_TITLE),

    html.Div([
        dcc.Graph(id="line-chart", style=CARD_50, config={"displayModeBar": False}),
        dcc.Graph(id="area-chart", style=CARD_50, config={"displayModeBar": False})
    ], style=ROW_STYLE)

], style={
    "maxWidth": "100%",
    "overflowX": "hidden",
    "padding": "20px",
    "boxSizing": "border-box",
    "backgroundColor": "#F4F7FB",
    "fontFamily": "Arial, sans-serif"
})


@app.callback(
    Output("column-chart", "figure"),
    Output("bar-chart", "figure"),
    Output("scatter-chart", "figure"),
    Output("bubble-chart", "figure"),
    Output("line-chart", "figure"),
    Output("area-chart", "figure"),
    Input("region-filter", "value"),
    Input("category-filter", "value"),
    Input("year-slider", "value")
)
def update_charts(selected_region, selected_categories, selected_year):

    if not selected_categories:
        selected_categories = sorted(df["category"].unique())

    selected_year = int(selected_year)

    filtered_df = df[
        (df["region"] == selected_region) &
        (df["category"].isin(selected_categories)) &
        (df["year"] == selected_year)
    ]

    color_map = {
        "Max": "#1E88E5",
        "Standard": "#BBDEFB"
    }

    # Column Chart
    sales_by_category = filtered_df.groupby("category")["sales"].sum().reset_index()
    sales_by_category = sales_by_category.sort_values("sales", ascending=False).reset_index(drop=True)

    sales_by_category["type"] = "Standard"
    if len(sales_by_category) > 0:
        sales_by_category.loc[0, "type"] = "Max"

    fig_column = px.bar(
        sales_by_category,
        x="category",
        y="sales",
        title=f"Sales by Category — {selected_region} — {selected_year}",
        color="type",
        text=sales_by_category["sales"] / 1000
    )

    fig_column.update_traces(
        texttemplate="%{text:.0f}K",
        textposition="outside",
        cliponaxis=False
    )

    fig_column.for_each_trace(
        lambda t: t.update(marker_color=color_map.get(t.name, "#BBDEFB"))
    )

    fig_column.update_layout(
        height=300,
        xaxis_title="Product Category",
        yaxis_title="Total Sales",
        template="plotly_white",
        yaxis_showgrid=True,
        legend_title="Type",
        margin=dict(l=45, r=20, t=80, b=45)
    )

    # Bar Chart
    profit_by_segment = filtered_df.groupby("segment")["profit"].sum().reset_index()
    profit_by_segment = profit_by_segment.sort_values("profit", ascending=False).reset_index(drop=True)

    profit_by_segment["type"] = "Standard"
    if len(profit_by_segment) > 0:
        profit_by_segment.loc[0, "type"] = "Max"

    max_profit = profit_by_segment["profit"].max() if len(profit_by_segment) > 0 else 1
    max_profit = max(abs(max_profit), 1)

    fig_bar = px.bar(
        profit_by_segment,
        x="profit",
        y="segment",
        title=f"Profit by Segment — {selected_region} — {selected_year}",
        color="type",
        text=profit_by_segment["profit"] / 1000
    )

    fig_bar.update_traces(
        texttemplate="%{text:.0f}K",
        textposition="outside"
    )

    fig_bar.for_each_trace(
        lambda t: t.update(marker_color=color_map.get(t.name, "#BBDEFB"))
    )

    fig_bar.update_layout(
        height=300,
        xaxis_title="Total Profit",
        yaxis_title="Segment",
        template="plotly_white",
        xaxis_showgrid=True,
        legend_title="Type",
        xaxis=dict(range=[0, max_profit * 1.25]),
        margin=dict(l=70, r=30, t=55, b=45)
    )

    fig_bar.update_yaxes(autorange="reversed")

    # Scatter Chart
    scatter_df = filtered_df.copy()
    scatter_df["outlier"] = (scatter_df["sales"] > 1000) & (scatter_df["profit"] < 0)
    scatter_df["point_type"] = scatter_df["outlier"].apply(
        lambda x: "Outlier" if x else "Normal"
    )

    fig_scatter = px.scatter(
        scatter_df,
        x="sales",
        y="profit",
        title=f"Sales vs Profit (Outliers Highlighted) — {selected_region} — {selected_year}",
        color="point_type",
        hover_data=["category", "sub_category", "region", "segment"],
        opacity=0.6
    )

    scatter_color_map = {
        "Normal": "#90CAF9",
        "Outlier": "#A6EF46"
    }

    fig_scatter.for_each_trace(
        lambda t: t.update(marker_color=scatter_color_map.get(t.name, "#90CAF9"))
    )

    fig_scatter.update_traces(
        marker=dict(size=7, line=dict(width=1, color="black"))
    )

    fig_scatter.update_layout(
        height=300,
        xaxis_title="Sales",
        yaxis_title="Profit",
        template="plotly_white",
        xaxis_showgrid=True,
        yaxis_showgrid=True,
        legend_title="Point Type",
        margin=dict(l=45, r=20, t=55, b=45)
    )

    # Bubble Chart
    bubble_df = filtered_df.copy()

    bubble_df["outlier"] = (
        (bubble_df["profit"] < 0) |
        (bubble_df["quantity"] > bubble_df["quantity"].quantile(0.95))
    )

    bubble_df["point_type"] = bubble_df["outlier"].apply(
        lambda x: "Outlier" if x else "Normal"
    )

    fig_bubble = px.scatter(
        bubble_df,
        x="sales",
        y="profit",
        size="quantity",
        color="point_type",
        title=f"Sales vs Profit with Quantity — {selected_region} — {selected_year}",
        hover_data=["category", "sub_category", "region", "segment", "quantity"],
        opacity=0.35,
        size_max=40
    )

    bubble_color_map = {
        "Normal": "#90CAF9",
        "Outlier": "#A6EF46"
    }

    fig_bubble.for_each_trace(
        lambda t: t.update(marker_color=bubble_color_map.get(t.name, "#90CAF9"))
    )

    if len(bubble_df) > 0:
        fig_bubble.update_traces(
            marker=dict(
                sizemode="area",
                sizeref=2 * bubble_df["quantity"].max() / (40 ** 2),
                line=dict(width=1, color="black")
            )
        )

    fig_bubble.update_layout(
        height=300,
        xaxis_title="Sales",
        yaxis_title="Profit",
        template="plotly_white",
        xaxis_showgrid=True,
        yaxis_showgrid=True,
        legend_title="Point Type",
        margin=dict(l=45, r=20, t=55, b=45)
    )

    fig_bubble.update_xaxes(showline=True, linewidth=1, linecolor="black")
    fig_bubble.update_yaxes(showline=True, linewidth=1, linecolor="black")

    # Line Chart
    sales_over_time = df[
        (df["region"] == selected_region) &
        (df["category"].isin(selected_categories))
    ].groupby("year_month")["sales"].sum().reset_index()

    sales_over_time["year_month"] = pd.to_datetime(sales_over_time["year_month"])
    sales_over_time = sales_over_time.sort_values("year_month")

    fig_line = px.line(
        sales_over_time,
        x="year_month",
        y="sales",
        title=f"(Line Chart) Sales Over Time — {selected_region}",
        markers=True
    )

    fig_line.update_layout(
        height=300,
        xaxis_title="Time",
        yaxis_title="Total Sales",
        template="plotly_white",
        xaxis_showgrid=True,
        yaxis_showgrid=True,
        margin=dict(l=45, r=20, t=55, b=45)
    )

    fig_line.update_xaxes(showline=True, linewidth=1, linecolor="black")
    fig_line.update_yaxes(showline=True, linewidth=1, linecolor="black")

    # Area Chart
    profit_over_time = df[
        (df["region"] == selected_region) &
        (df["category"].isin(selected_categories))
    ].groupby("year_month")["profit"].sum().reset_index()

    profit_over_time["year_month"] = pd.to_datetime(profit_over_time["year_month"])
    profit_over_time = profit_over_time.sort_values("year_month")

    fig_area = px.area(
        profit_over_time,
        x="year_month",
        y="profit",
        title=f"(Area Chart) Profit Over Time — {selected_region}"
    )

    fig_area.update_layout(
        height=300,
        xaxis_title="Time",
        yaxis_title="Total profit",
        template="plotly_white",
        xaxis_showgrid=True,
        yaxis_showgrid=True,
        margin=dict(l=45, r=20, t=55, b=45)
    )

    fig_area.update_xaxes(showline=True, linewidth=1, linecolor="black")
    fig_area.update_yaxes(showline=True, linewidth=1, linecolor="black")

    return fig_column, fig_bar, fig_scatter, fig_bubble, fig_line, fig_area


if __name__ == "__main__":
    app.run(debug=True)
    
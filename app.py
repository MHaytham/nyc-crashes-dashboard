import os
import re

import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc

# ==========================
# 1. LOAD DATA
# ==========================
# Use relative path for Railway deployment
csv_path = "df_full_features.csv"
if not os.path.exists(csv_path):
    raise FileNotFoundError(f"CSV file not found: {csv_path}")

df = pd.read_csv(csv_path)

# Ensure datetime
if "CRASH_DATETIME" in df.columns:
    df["CRASH_DATETIME"] = pd.to_datetime(df["CRASH_DATETIME"], errors="coerce")

# Drop rows without coords for map
df_map_base = df.dropna(subset=["LATITUDE", "LONGITUDE"])

# Useful lists for filters (exclude UNKNOWN)
BOROUGHS = sorted([b for b in df["BOROUGH"].dropna().unique() if b != "UNKNOWN"])
YEARS = sorted(df["CRASH_YEAR"].dropna().unique())

# Vehicle types from all 5 columns
veh_cols = [c for c in df.columns if c.startswith("VEHICLE TYPE CODE")]
vehicle_types = (
    pd.concat([df[c] for c in veh_cols])
    .dropna()
    .unique()
)
VEH_TYPES = sorted(vehicle_types)

cf_cols = [c for c in df.columns if c.startswith("CONTRIBUTING FACTOR VEHICLE")]
contrib_factors = (
    pd.concat([df[c] for c in cf_cols])
    .dropna()
    .unique()
)
CONTRIB_FACTORS = sorted(contrib_factors)

INJURY_TYPE_OPTIONS = [
    {"label": "Any", "value": "any"},
    {"label": "Pedestrian", "value": "pedestrian"},
    {"label": "Cyclist", "value": "cyclist"},
    {"label": "Motorist", "value": "motorist"},
]

# ==========================
# 2. HELPER: PARSE SEARCH QUERY
# ==========================

def parse_search_query(text: str):
    """
    Parse queries like: 'Brooklyn 2022 pedestrian crashes'
    Returns dict with: boroughs, years, injury_type
    
    FIXED: Borough names are uppercase in data (BROOKLYN, not Brooklyn)
    """
    if not text:
        return {"boroughs": None, "years": None, "injury_type": None}

    text_low = text.lower()

    # ---- Borough detection (convert to UPPERCASE to match data) ----
    detected_boros = []
    for b in BOROUGHS:
        if b and b.lower() in text_low:
            detected_boros.append(b)  # Keep as UPPERCASE
    detected_boros = detected_boros if detected_boros else None

    # ---- Year detection (4-digit years 2000-2099) ----
    year_matches = re.findall(r"\b(20\d{2})\b", text_low)
    detected_years = [int(y) for y in year_matches if int(y) in YEARS]
    detected_years = detected_years if detected_years else None

    # ---- Injury type ----
    injury = None
    if "pedestrian" in text_low:
        injury = "pedestrian"
    elif "cyclist" in text_low or "bicycle" in text_low or "bike" in text_low:
        injury = "cyclist"
    elif "motorist" in text_low or "driver" in text_low:
        injury = "motorist"

    return {
        "boroughs": detected_boros,
        "years": detected_years,
        "injury_type": injury,
    }

# ==========================
# 3. BUILD APP
# ==========================
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server  # for deployment (Railway/gunicorn)

app.title = "NYC Crashes Dashboard"

# ==========================
# 4. LAYOUT
# ==========================
app.layout = dbc.Container(
    [
        html.H2("NYC Motor Vehicle Collisions", className="mt-3 mb-4"),

        # ---- FILTERS + SEARCH ----
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Label("Borough"),
                        dcc.Dropdown(
                            options=[{"label": b, "value": b} for b in BOROUGHS],
                            id="borough-filter",
                            multi=True,
                            placeholder="Select borough(s)",
                        ),
                    ],
                    md=3,
                ),
                dbc.Col(
                    [
                        html.Label("Year"),
                        dcc.Dropdown(
                            options=[{"label": int(y), "value": int(y)} for y in YEARS],
                            id="year-filter",
                            multi=True,
                            placeholder="Select year(s)",
                        ),
                    ],
                    md=3,
                ),
                dbc.Col(
                    [
                        html.Label("Vehicle Type"),
                        dcc.Dropdown(
                            options=[{"label": v, "value": v} for v in VEH_TYPES],
                            id="vehicle-filter",
                            multi=True,
                            placeholder="Select vehicle type(s)",
                        ),
                    ],
                    md=3,
                ),
                dbc.Col(
                    [
                        html.Label("Contributing Factor (Vehicle 1)"),
                        dcc.Dropdown(
                            options=[{"label": c, "value": c} for c in CONTRIB_FACTORS],
                            id="factor-filter",
                            multi=True,
                            placeholder="Select contributing factor(s)",
                        ),
                    ],
                    md=3,
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Label("Injury Type"),
                        dcc.Dropdown(
                            options=INJURY_TYPE_OPTIONS,
                            id="injury-filter",
                            value="any",
                            clearable=False,
                        ),
                    ],
                    md=3,
                ),
                dbc.Col(
                    [
                        html.Label("Search (e.g., 'Brooklyn 2022 pedestrian crashes')"),
                        dcc.Input(
                            id="search-input",
                            type="text",
                            placeholder="Type query here...",
                            style={"width": "100%", "padding": "0.5em"},
                        ),
                    ],
                    md=9,
                ),
            ],
            className="mb-2",
        ),
        dbc.Row(
            dbc.Col(
                dbc.Button("Generate Report", id="generate-btn", color="primary", className="mb-4"),
                width="auto",
            )
        ),

        # ---- DEBUG INFO (optional, remove later) ----
        html.Div(id="debug-info", style={"fontSize": "12px", "color": "gray", "marginBottom": "1em"}),

        # ---- KPI CARDS ----
        dbc.Row(id="kpi-row", className="mb-4"),

        # ---- GRAPHS ----
        dbc.Row(
            [
                dbc.Col(dcc.Graph(id="borough-fig"), md=6),
                dbc.Col(dcc.Graph(id="trend-fig"), md=6),
            ],
            className="mb-4",
        ),
        dbc.Row(
            [
                dbc.Col(dcc.Graph(id="severity-fig"), md=6),
                dbc.Col(dcc.Graph(id="heatmap-fig"), md=6),
            ],
            className="mb-4",
        ),
        dbc.Row(
            [
                dbc.Col(dcc.Graph(id="map-fig"), md=12),
            ],
            className="mb-4",
        ),
    ],
    fluid=True,
)

# ==========================
# 5. CALLBACK
# ==========================
@app.callback(
    [
        Output("debug-info", "children"),
        Output("kpi-row", "children"),
        Output("borough-fig", "figure"),
        Output("trend-fig", "figure"),
        Output("severity-fig", "figure"),
        Output("heatmap-fig", "figure"),
        Output("map-fig", "figure"),
    ],
    Input("generate-btn", "n_clicks"),
    [
        State("borough-filter", "value"),
        State("year-filter", "value"),
        State("vehicle-filter", "value"),
        State("factor-filter", "value"),
        State("injury-filter", "value"),
        State("search-input", "value"),
    ],
    prevent_initial_call=True,  # Don't run on page load
)
def update_report(n_clicks, boroughs, years, vehicles, factors, injury_type, search_text):
    # Base dataframe
    dff = df.copy()

    # ---- Apply search query (if any) ----
    parsed = parse_search_query(search_text) if search_text else {
        "boroughs": None,
        "years": None,
        "injury_type": None,
    }

    # ========== BOROUGH FILTER ==========
    # Use dropdown if provided, otherwise use search result
    borough_filter = boroughs if boroughs else parsed["boroughs"]
    if borough_filter:
        dff = dff[dff["BOROUGH"].isin(borough_filter)]

    # ========== YEAR FILTER ==========
    # Use dropdown if provided, otherwise use search result
    year_filter = years if years else parsed["years"]
    if year_filter:
        dff = dff[dff["CRASH_YEAR"].isin(year_filter)]

    # ========== VEHICLE TYPE FILTER ==========
    if vehicles:
        mask_veh = False
        for c in veh_cols:
            mask_veh = mask_veh | dff[c].isin(vehicles)
        dff = dff[mask_veh]

    # ========== CONTRIBUTING FACTOR FILTER ==========
    if factors:
        mask_cf = False
        for c in cf_cols:
            mask_cf = mask_cf | dff[c].isin(factors)
        dff = dff[mask_cf]

    # ========== INJURY TYPE FILTER ==========
    # Priority 1: dropdown (if not "any")
    # Priority 2: search text (if dropdown = "any")
    effective_injury = None

    if injury_type and injury_type != "any":
        effective_injury = injury_type
    elif parsed["injury_type"]:
        effective_injury = parsed["injury_type"]

    if effective_injury == "pedestrian":
        dff = dff[dff["HAS_PEDESTRIAN"] == True]
    elif effective_injury == "cyclist":
        dff = dff[dff["HAS_CYCLIST"] == True]
    elif effective_injury == "motorist":
        dff = dff[dff["HAS_DRIVER"] == True]

    # ---- DEBUG INFO ----
    debug_text = f"Rows: {len(dff)} | Borough: {borough_filter} | Year: {year_filter} | Injury: {effective_injury}"

    # If no data after filters → return empty figs
    if dff.empty:
        empty_fig = px.scatter(title="No data for selected filters")
        kpi_cards = dbc.Row(
            dbc.Col(
                dbc.Card(dbc.CardBody([html.H6("No data", className="card-title"), html.P("Adjust filters or search.")])),
                md=12,
            )
        )
        return debug_text, kpi_cards, empty_fig, empty_fig, empty_fig, empty_fig, empty_fig

    # ---- KPI CARDS ----
    total_crashes = len(dff)
    total_injured = int(dff["TOTAL_INJURED"].sum())
    total_killed = int(dff["TOTAL_KILLED"].sum())
    most_common_borough = dff["BOROUGH"].mode().iloc[0] if not dff["BOROUGH"].dropna().empty else "N/A"

    kpi_cards = dbc.Row(
        [
            dbc.Col(
                dbc.Card(
                    dbc.CardBody([html.H6("Crashes", className="card-title"), html.H3(f"{total_crashes:,}")])
                ),
                md=3,
            ),
            dbc.Col(
                dbc.Card(
                    dbc.CardBody([html.H6("Injured", className="card-title"), html.H3(f"{total_injured:,}")])
                ),
                md=3,
            ),
            dbc.Col(
                dbc.Card(
                    dbc.CardBody([html.H6("Killed", className="card-title"), html.H3(f"{total_killed:,}")])
                ),
                md=3,
            ),
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H6("Most Dangerous Borough", className="card-title"),
                            html.H4(most_common_borough),
                        ]
                    )
                ),
                md=3,
            ),
        ]
    )

    # ---- FIGURE 1: Crashes by Borough ----
    b_counts = dff["BOROUGH"].value_counts().reset_index()
    b_counts.columns = ["BOROUGH", "COUNT"]
    fig_borough = px.bar(
        b_counts,
        x="BOROUGH",
        y="COUNT",
        title="Crashes by Borough",
        labels={"COUNT": "Number of crashes"},
    )

    # ---- FIGURE 2: Trend (Year-Month) ----
    if "CRASH_DATETIME" in dff.columns:
        temp = dff.copy()
        temp["YEAR_MONTH"] = temp["CRASH_DATETIME"].dt.to_period("M").astype(str)
        tm_counts = temp["YEAR_MONTH"].value_counts().sort_index().reset_index()
        tm_counts.columns = ["YEAR_MONTH", "COUNT"]
        fig_trend = px.line(
            tm_counts,
            x="YEAR_MONTH",
            y="COUNT",
            title="Monthly Crash Trend",
            labels={"YEAR_MONTH": "Year-Month", "COUNT": "Crashes"},
        )
    else:
        fig_trend = px.scatter(title="No datetime information")

    # ---- FIGURE 3: Severity Distribution ----
    if "SEVERITY_LEVEL" in dff.columns:
        sev_counts = dff["SEVERITY_LEVEL"].value_counts().reset_index()
        sev_counts.columns = ["SEVERITY_LEVEL", "COUNT"]
        fig_severity = px.bar(
            sev_counts,
            x="SEVERITY_LEVEL",
            y="COUNT",
            title="Severity Level Distribution",
            labels={"COUNT": "Number of crashes"},
        )
    else:
        fig_severity = px.scatter(title="Severity not available")

    # ---- FIGURE 4: Hour vs Weekday Heatmap ----
    pivot_hw = dff.pivot_table(
        index="CRASH_WEEKDAY",
        columns="CRASH_HOUR",
        values="COLLISION_ID",
        aggfunc="count",
    ).fillna(0)

    weekday_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    pivot_hw = pivot_hw.reindex(weekday_order)

    fig_heat = px.imshow(
        pivot_hw,
        aspect="auto",
        labels={"color": "Crash count"},
        title="Crashes by Hour and Weekday",
    )

    # ---- FIGURE 5: Map (Density) ----
    dff_map = dff.dropna(subset=["LATITUDE", "LONGITUDE"])
    # Sample if too many points (performance optimization)
    if len(dff_map) > 8000:
        dff_map = dff_map.sample(n=8000, random_state=42)

    if dff_map.empty or "SEVERITY_INDEX" not in dff_map.columns:
        fig_map = px.scatter_mapbox(
            dff_map,
            lat="LATITUDE",
            lon="LONGITUDE",
            zoom=9,
            height=500,
            title="Crash Locations",
            mapbox_style="open-street-map",
        )
    else:
        fig_map = px.density_mapbox(
            dff_map,
            lat="LATITUDE",
            lon="LONGITUDE",
            z="SEVERITY_INDEX",
            radius=10,
            center=dict(lat=40.71, lon=-74.00),
            zoom=9,
            mapbox_style="open-street-map",
            height=500,
            title="Crash Density (weighted by severity)",
        )

    return debug_text, kpi_cards, fig_borough, fig_trend, fig_severity, fig_heat, fig_map


# ==========================
# 6. RUN (Railway / local)
# ==========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8050))
    app.run_server(host="0.0.0.0", port=port, debug=False)
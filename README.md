NYC Motor Vehicle Collisions – Interactive Dash Dashboard

An interactive, data-driven dashboard that visualizes NYC motor vehicle collisions using Dash, Plotly, Pandas, and Bootstrap.
This project allows users to dynamically explore crash patterns based on:

Borough

Year

Vehicle Type

Contributing Factor

Injury Type

Natural-language search queries

Interactive "Generate Report" button

The dashboard includes KPIs, bar charts, time trends, heatmaps, and a geographic crash density map.

📊 Features
1. Fully Interactive Dashboard

Multi-filter dropdown controls

Natural-language search (e.g., “Brooklyn 2022 pedestrian crashes”)

“Generate Report” button to fetch updated insights

Lightweight preview mode + large-scale rendering optimization

Map sampling to avoid browser crashes

2. Visualizations

Crashes by Borough

Time Trend (Year-Month)

Severity Distribution

Heatmap (Crash Hour × Weekday)

Density Map of crash locations

KPI summary cards

3. Clean Data Integration

The app uses a pre-cleaned dataset:

df_full_features.csv


all preprocessing handled prior to visualization.

4. Production-Ready Deployment

Designed to run smoothly on Railway, Render, or any cloud hosting platform.

Includes:

Procfile

runtime.txt

requirements.txt

Environment-aware server binding

port = int(os.environ.get("PORT", 8050))
app.run_server(host="0.0.0.0", port=port)

📁 Project Structure
nyc-crashes-dashboard/
│
├── app.py                  # Main Dash application
├── df_full_features.csv    # Clean dataset used by the dashboard
│
├── requirements.txt        # Python dependencies
├── runtime.txt             # Python version for Railway/Render
├── Procfile                # Deployment startup command
│
└── README.md               # Project documentation

🚀 Installation (Local Development)
1. Clone the repository
git clone https://github.com/MHaytham/nyc-crashes-dashboard.git
cd nyc-crashes-dashboard

2. Create a virtual environment
python -m venv .venv

3. Activate the virtual environment
Windows
.venv\Scripts\activate

macOS/Linux
source .venv/bin/activate

4. Install dependencies
pip install -r requirements.txt

5. Run the application
python app.py

6. Open in browser

Visit:

http://127.0.0.1:8050

🌐 Deployment (Railway)

The project is pre-configured for Railway.

Push your code to GitHub

Create a new Railway project → Deploy from GitHub

Railway detects:

Python runtime

Procfile

runtime.txt

Once deployed, Railway exposes a public URL

The app runs on the assigned port using

os.environ.get("PORT")


If you get a "Failed to Respond" error:

Ensure the CSV file exists in the repo

Ensure filenames are correct

Check deploy logs → missing dependency or crash during startup

🔍 Search Query Examples

You can type natural-language queries:

Query Example	Meaning
“Brooklyn crashes 2020”	Filters to Brooklyn + 2020
“Manhattan cyclist accidents”	Filters to Manhattan + cyclist injuries
“2022 pedestrian severe crashes”	Filters by year + pedestrian involvement
“Queens 2021 truck collision”	Borough + year + vehicle type

Search is optional and works together with dropdown filters.

⚙️ Technologies Used

Dash (frontend UI framework)

Plotly Express (visualizations)

Pandas (data processing)

Dash Bootstrap Components

Python 3.11

Railway hosting

📦 Requirements

These are defined in requirements.txt:

dash==2.17.1
dash-bootstrap-components==1.6.0
pandas==2.2.2
plotly==5.22.0
gunicorn==23.0.0

📘 How It Works (Short Explanation)

The CSV loads into pandas

Filters convert into pandas masks

The callback rebuilds:

KPI cards

All charts (bar, line, heatmap, density map)

Dash updates the UI without page reloads

Search text is parsed into structured filters:

boroughs, years, injury_type

🛠️ Troubleshooting
1. Blank page on Railway

Missing CSV file

Incorrect filename

App crashes before server starts

Check Deploy Logs

2. Dataset too large / app freezing

Map automatically samples to 8,000 rows

Add more sampling if deploying on free plans

3. No data after clicking “Generate Report”

Check search query spelling (uses uppercase boroughs).

📄 License

This project is for educational and academic use.

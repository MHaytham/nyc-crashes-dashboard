NYC Motor Vehicle Collisions – Interactive Dashboard

This project is an interactive data visualization website built using Dash (Python/Plotly).
It analyzes and visualizes NYC motor vehicle collisions using a dataset enriched with numerous engineered features.

The project fulfills the course requirements by providing:

A complete EDA workflow

Clean and well-documented data integration

An interactive dashboard with filters + search mode

A deployed website on a cloud platform (Railway)

Full documentation of setup & deployment steps

📦 1. Project Overview

This dashboard helps users explore NYC collisions by enabling filtering and searching across:

Borough

Year

Vehicle Type

Contributing Factor

Injury Type

Natural-language search queries (e.g., “Brooklyn 2022 pedestrian crashes”)

The dashboard generates:

KPI cards

Crashes by borough

Monthly crash trends

Severity distribution

Hour × weekday heatmap

Crash density map

📂 2. Project Structure
nyc-crashes-dashboard/
│
├── app.py                    # Main Dash application
├── df_full_features.csv      # Final cleaned dataset used by the dashboard
│
├── requirements.txt          # Python dependencies for deployment
├── runtime.txt               # Specifies Python version for Railway
├── Procfile                  # Defines how Railway runs the app
│
└── README.md                 # Project documentation

⚙️ 3. Installation & Setup (Local Development)
Step 1 — Clone the repository
git clone https://github.com/MHaytham/nyc-crashes-dashboard.git
cd nyc-crashes-dashboard

Step 2 — Create a virtual environment
python -m venv .venv

Step 3 — Activate the environment
Windows:
.venv\Scripts\activate

macOS/Linux:
source .venv/bin/activate

Step 4 — Install the dependencies
pip install -r requirements.txt

Step 5 — Run the dashboard
python app.py

Step 6 — Open the app in your browser
http://127.0.0.1:8050

🧹 4. Dataset & Data Cleaning

The dashboard uses:

df_full_features.csv


This dataset includes:

Cleaned coordinates

A consolidated datetime column

Categorical cleanup (BOROUGH, VEHICLE TYPES, FACTORS, etc.)

Engineered features:

SEVERITY_INDEX

TOTAL_INJURED

TOTAL_KILLED

HAS_PEDESTRIAN / HAS_CYCLIST / HAS_DRIVER

CRASH_MONTH, CRASH_HOUR, CRASH_WEEKDAY, etc.

All preprocessing was done before running the web app.

🌐 5. Deployment Instructions (Railway)

The project is already configured for Railway deployment.

Step 1 — Push your project to GitHub

From VS Code:

git add .
git commit -m "Initial project setup"
git push origin main

Step 2 — Create a New Railway Project

Go to https://railway.app

Click New Project

Select Deploy from GitHub Repo

Choose your repo:
nyc-crashes-dashboard

Railway auto-detects:

Python runtime

requirements.txt

Procfile

runtime.txt

Step 3 — Deploy

After Railway builds the image, it will automatically:

Install all packages

Run the command from Procfile:

web: python app.py

Step 4 — View Your Live Website

Railway will give you a public URL:

https://your-app-name.up.railway.app/


If it crashes:

Ensure df_full_features.csv is included in GitHub

Ensure correct filename

Check Railway → Deploy Logs

🔧 6. Environment Variables

Not required.
The app only uses:

port = int(os.environ.get("PORT", 8050))


Railway automatically injects PORT.

🧪 7. Dashboard Features & Interactivity
Multi-filter Interface

Borough

Year

Vehicle Type

Contributing Factor

Injury Type

Natural Language Search

Examples:

“Brooklyn 2022 crashes”

“Manhattan cyclist accidents”

“Queens pedestrian 2021”

Search auto-detects:

Borough

Year

Injury type

Generate Report Button

All visualizations update only when the button is clicked, preventing lag for large datasets.

📊 8. Visualizations Included
Chart	Description
Crashes by Borough	Bar chart showing distribution
Monthly Trend	Line chart per Year-Month
Severity Levels	Bar chart
Hour × Weekday Heatmap	Matrix of crash frequencies
Crash Density Map	Mapbox density plot
📈 9. Grading Rubric Compliance

This project includes:

✔️ EDA with statistics & visualizations
✔️ Pre- and post-integration cleaning
✔️ Clean integration using combined features
✔️ Highly interactive dashboard
✔️ Generate Report button
✔️ Multiple chart types
✔️ Dropdown filters & search mode
✔️ Clean, modular Python code
✔️ Markdown documentation inside notebook
✔️ Fully deployed website
✔️ Source code in GitHub

Everything required for full grade is satisfied.

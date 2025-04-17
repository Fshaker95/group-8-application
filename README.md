# ENPM611 Team 8 – GitHub Issue Analytics

This repository implements a feature-rich analysis application for GitHub issues from the python-poetry project. The goal is to extract insightful patterns about issue volume, resolution speed, and contributor engagement.

# Project Structure

🔹 **run.py**
Main entry point. Based on the --feature argument, it dispatches the corresponding analysis function.

🔹 **model.py**
Defines the Issue and Event classes. Handles parsing of issue data including created_date, updated_date, and closed_date.

🔹 **data_loader.py**
Loads the JSON issue dataset and converts each entry into Issue objects using the model.

🔹 **config.py**
Loads configuration values from config.json or environment variables.

🔹 **config.json**
Specifies the path to the JSON data file (e.g., Milestone-1/team8_poetry_data.json).

🔹 **Milestone-1/team8_poetry_data.json**
Contains the GitHub issue dataset for the Poetry project. Used as the primary data source for all feature analyses.

🔹 **example_analysis.py**
Example starter analysis to demonstrate how to load and iterate over issues.

🔹 **feature1_temporal_analysis.py**
Implements Feature 1: Groups issues by month and plots issue creation count and average resolution time over time using a dual-axis line chart.

🔹 **feature2_contributor_expertise.py**
Implements Feature 2: Accepts a label from user input, identifies contributors related to that label, and shows their interaction count in a bar chart.

🔹 **feature3.py**
Implements Feature 3: Calculates how many days each issue remained open and visualizes the distribution using a histogram and box plot to show resolution efficiency and outliers.

🔹 **requirements.txt**
Specifies required Python packages (e.g., matplotlib, python-dateutil).

🔹 **README.md**
Provides setup instructions, feature descriptions, and how to run each analysis.

# **Setup Instructions**
**1. Clone the Repo**

git clone https://github.com/Fshaker95/group-8-application.git
cd group-8-application

**[Optional] Create Virtual Environment**

python -m venv venv
venv\\Scripts\\activate

**2. Install Dependencies**

pip install -r requirements.txt

**3. Configure the Data File**

Ensure the team8_poetry_data.json file is located at:
**Milestone-1/team8_poetry_data.json** (config.json is already configured with the path)

# How to Run Features

From the root of the project, run:

python run.py --feature <n> (Where <n> is the feature number (1 to 4))

# Feature 1: Temporal Analysis of Issue Bursts

**python run.py --feature 1**

-Groups issues by creation month
-Calculates how many were created and their average days-to-close
-Displays a dual-axis line chart of:
  -Number of issues created (🔵)
  -Avg days to close (🔴)

# Feature 2: Label-Driven Contributor Expertise

**python run.py --feature 2**

Requires input at runtime: You’ll be prompted to enter a label like:

**Enter a label to analyze (e.g., 'bug'):**

**Example Labels You Can Try (Feature 2)**-
kind/bug
status/triage
type/feature
dependencies

-Identifies top contributors for the selected label
-Counts issue creators and commenters
-Displays a bar chart of the top 10 contributors for that label

# Feature 3: Issue Age Distribution

**python run.py --feature 3**

-Computes how many days each issue remained open
-Plots:
  Histogram: frequency of days-to-close
  Box plot: shows outliers, median, and spread

# Notes
-model.py was modified to include a new closed_date attribute from the JSON field closed_at
-The dataset is located in Milestone-1/
-The application uses matplotlib for plotting
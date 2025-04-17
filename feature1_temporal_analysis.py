import matplotlib.pyplot as plt
from collections import defaultdict
from datetime import datetime
from data_loader import DataLoader


def run_feature_1():

    #Load issues
    issues = DataLoader().get_issues()

    #Group by month
    grouped = defaultdict(list)
    for issue in issues:
        created = issue.created_date
        closed = issue.closed_date
        if created:
            month_key = created.strftime("%Y-%m")
            grouped[month_key].append((created, closed))

    #Computation of counts and avg resolution
    months = []
    issue_counts = []
    avg_days_to_close = []

    for month in sorted(grouped.keys()):
        issues_in_month = grouped[month]
        count = len(issues_in_month)
        resolution_times = [
            (closed - created).days
            for created, closed in issues_in_month if closed
        ]
        avg = sum(resolution_times) / len(resolution_times) if resolution_times else 0

        months.append(month)
        issue_counts.append(count)
        avg_days_to_close.append(avg)

    #Visualization
    fig, ax1 = plt.subplots(figsize=(14, 6), dpi=120)

    ax1.set_xlabel("Month")
    ax1.set_ylabel("No. of Issues Created", color="blue")
    ax1.plot(months, issue_counts, color="blue", marker="o", linewidth=1.5, label="No. of Issues Created")
    ax1.tick_params(axis="y", labelcolor="blue")
    ax1.grid(axis='y', linestyle='--', alpha=0.5)

    ax2 = ax1.twinx()
    ax2.set_ylabel("Average Days to Close", color="red")
    ax2.plot(months, avg_days_to_close, color="red", marker="x", linewidth=1.5, label="Average Days to Close")
    ax2.tick_params(axis="y", labelcolor="red")

    
    plt.xticks(ticks=range(0, len(months), 6), labels=months[::6], rotation=45)

    plt.title("Issue Bursts and Resolution Efficiency")
    fig.tight_layout()
    plt.show()

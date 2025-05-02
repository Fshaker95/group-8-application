import matplotlib.pyplot as plt
from collections import defaultdict
from data_loader import DataLoader

def process_issues(issues):
    
    grouped = defaultdict(list)
    for issue in issues:
        created = issue.created_date
        closed  = issue.closed_date
        if created:
            key = created.strftime("%Y-%m")
            grouped[key].append((created, closed))

    months, counts, avgs = [], [], []
    for month in sorted(grouped):
        items = grouped[month]
        counts.append(len(items))
        deltas = [(c - o).days for (o, c) in items if c]
        avgs.append(sum(deltas)/len(deltas) if deltas else 0)
        months.append(month)

    return months, counts, avgs

def run_feature_1():
    issues = DataLoader().get_issues()
    months, counts, avgs = process_issues(issues)

    fig, ax1 = plt.subplots(figsize=(14, 6), dpi=120)
    ax1.set_xlabel("Month")
    ax1.set_ylabel("No. of Issues Created", color="blue")
    ax1.plot(months, counts, color="blue", marker="o", linewidth=1.5,
             label="No. of Issues Created")
    ax1.tick_params(axis="y", labelcolor="blue")
    ax1.grid(axis='y', linestyle='--', alpha=0.5)

    ax2 = ax1.twinx()
    ax2.set_ylabel("Average Days to Close", color="red")
    ax2.plot(months, avgs, color="red", marker="x", linewidth=1.5,
             label="Average Days to Close")
    ax2.tick_params(axis="y", labelcolor="red")

    plt.xticks(ticks=range(0, len(months), 6),
               labels=months[::6], rotation=45)
    plt.title("Issue Bursts and Resolution Efficiency")
    fig.tight_layout()
    plt.show()

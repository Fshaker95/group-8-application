from collections import defaultdict
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

from data_loader import DataLoader


def run_feature_2_heatmap():
    issues = DataLoader().get_issues()
    contributor_label_map = defaultdict(lambda: defaultdict(int))

    for issue in issues:
        normalized_labels = [lbl.strip().lower() for lbl in issue.labels]

        # Count issue creator's contributions
        if issue.creator:
            for label in normalized_labels:
                contributor_label_map[issue.creator][label] += 1

        # Count assignees
        for assignee in issue.assignees:
            if isinstance(assignee, dict) and 'login' in assignee:
                assignee_login = assignee['login']
            else:
                assignee_login = assignee  # if already a string
            for label in normalized_labels:
                contributor_label_map[assignee_login][label] += 1

        # Count commenters from events
        for event in issue.events:
            if event.author:
                for label in normalized_labels:
                    contributor_label_map[event.author][label] += 1

    if not contributor_label_map:
        print("❌ No contributor-label interactions found.")
        return

    # Convert to DataFrame for easier plotting
    df = pd.DataFrame(contributor_label_map).fillna(0).astype(int).T

    # Select top contributors based on total activity
    top_contributors = df.sum(axis=1).nlargest(10).index
    df_top = df.loc[top_contributors]

    # Heatmap
    plt.figure(figsize=(14, 6))
    sns.heatmap(df_top, annot=True, cmap="YlGnBu", linewidths=0.5, linecolor='gray')
    plt.title("Contributor Expertise by Label (Top 10 Contributors)")
    plt.xlabel("Issue Labels (Expertise Zones)")
    plt.ylabel("Contributors")
    plt.xticks(rotation=60, ha='right')  # rotated, aligned
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.show()

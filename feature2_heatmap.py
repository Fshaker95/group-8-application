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

        # Count contributions via comments
        for event in issue.events:
            if event.event_type == "commented" and event.author:
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
    plt.title("🔍 Contributor Expertise Zones by Label")
    plt.xlabel("Labels")
    plt.ylabel("Contributors")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

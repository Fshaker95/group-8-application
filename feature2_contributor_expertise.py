from collections import defaultdict, Counter
import matplotlib.pyplot as plt
from data_loader import DataLoader
from model import Issue

def run_feature_2():
    issues = DataLoader().get_issues()

    label_input = input("Enter a label to analyze (e.g., 'bug'): ").strip().lower()
    label_contributor_map = defaultdict(int)

    for issue in issues:
        normalized_labels = [lbl.strip().lower() for lbl in issue.labels]
        if label_input.strip().lower() in normalized_labels:
            print(f"[DEBUG] MATCHED ISSUE {issue.number} – labels: {normalized_labels}")
            # Count the issue creator
            if issue.creator:
                label_contributor_map[issue.creator] += 1
            # Count contributors via comments
            for event in issue.events:
                if event.event_type == "commented" and event.author:
                    label_contributor_map[event.author] += 1

    if not label_contributor_map:
        print(f"No contributors found for label: {label_input}")
        return

    # Get top contributors
    top_contribs = Counter(label_contributor_map).most_common(10)
    names, counts = zip(*top_contribs)

    # Plot the results
    plt.figure(figsize=(10, 6))
    plt.bar(names, counts, color='skyblue')
    plt.title(f"Top Contributors for Label: '{label_input}'")
    plt.xlabel("Contributors")
    plt.ylabel("Interactions")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
from collections import defaultdict
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
from data_loader import DataLoader

def run_feature_2_network():
    issues = DataLoader().get_issues()

    # contributor → label → count
    matrix = defaultdict(lambda: defaultdict(int))

    for issue in issues:
        labels = [label.strip().lower() for label in issue.labels if isinstance(label, str)]
        if not labels:
            continue

        if issue.creator:
            for label in labels:
                matrix[issue.creator][label] += 1

        for event in issue.events:
            if event.event_type == "commented" and event.author:
                for label in labels:
                    matrix[event.author][label] += 1

    if not matrix:
        print("No contributor-label interactions found.")
        return

    # --- Visualization Option 1: Heatmap ---
    contributors = list(matrix.keys())
    labels = sorted({label for contrib in matrix.values() for label in contrib})
    
    data = [
        [matrix[contrib].get(label, 0) for label in labels]
        for contrib in contributors
    ]

    plt.figure(figsize=(12, 6))
    sns.heatmap(data, xticklabels=labels, yticklabels=contributors, cmap="Blues", annot=True, fmt="d")
    plt.title("Contributor vs. Label Interaction Heatmap")
    plt.xlabel("Labels")
    plt.ylabel("Contributors")
    plt.tight_layout()
    plt.show()

    # --- Visualization Option 2: Network Graph ---
    G = nx.Graph()
    for contrib, label_counts in matrix.items():
        for label, count in label_counts.items():
            if count > 0:
                G.add_edge(contrib, label, weight=count)

    plt.figure(figsize=(14, 8))
    pos = nx.spring_layout(G, k=0.7)
    weights = [G[u][v]['weight'] for u, v in G.edges()]
    nx.draw(G, pos, with_labels=True, node_color='skyblue', edge_color=weights,
            width=[w * 0.2 for w in weights], edge_cmap=plt.cm.Blues, font_size=8)
    plt.title("Contributor-Label Network Graph")
    plt.tight_layout()
    plt.show()

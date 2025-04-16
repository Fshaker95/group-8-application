from data_loader import DataLoader

def list_unique_labels():
    issues = DataLoader().get_issues()
    label_set = set()

    for issue in issues:
        for label in issue.labels:
            label_set.add(label.strip().lower())

    print("✅ Available labels:")
    for label in sorted(label_set):
        print("-", label)

if __name__ == "__main__":
    list_unique_labels()
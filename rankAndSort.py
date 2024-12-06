import csv
import random
from collections import defaultdict


def read_items_from_csv():
    """Read a CSV file with a single column 'Name' and return the list of items."""
    items = []
    try:
        with open('items3.csv', mode='r') as file:
            reader = csv.DictReader(file)
            if "Name" not in reader.fieldnames:
                raise ValueError(
                    "CSV file must have a single column titled 'Name'.")
            items = [row["Name"].strip()
                     for row in reader if row["Name"].strip()]
    except FileNotFoundError:
        print(f"Error: File not found.")
    except ValueError as e:
        print(f"Error: {e}")
    return items


def compare_items(items):
    """Perform randomized pairwise comparisons of items and rank them based on user input."""
    scores = defaultdict(int)
    all_pairs = [(i, j) for i in range(len(items))
                 for j in range(i + 1, len(items))]
    random.shuffle(all_pairs)
    removed_indices = set()  # Track removed indices to prevent invalid accesses

    print("\nYou can rank the following pairs or exit at any time.")
    print("To exit, type 'exit' when prompted for input.\n")

    while all_pairs:
        # Fetch the next pair while ensuring no removed indices are accessed
        i, j = all_pairs.pop(0)

        # Skip pairs where one or both indices have been removed
        if i in removed_indices or j in removed_indices:
            continue

        while True:
            print(f"\nWhich item do you prefer?")
            print(f"1: {items[i]}")
            print(f"2: {items[j]}")
            print(f"3: Remove {items[i]}")
            print(f"4: Remove {items[j]}")
            print(f"5: Remove both items")
            print(f"Type 'exit' to stop comparing.")
            choice = input("Enter 1, 2, 3, 4, 5, or 'exit': ").strip()

            if choice == "1":
                scores[items[i]] += 1
                break
            elif choice == "2":
                scores[items[j]] += 1
                break
            elif choice == "3":
                removed_indices.add(i)
                print(f"Removed {items[i]}")
                break
            elif choice == "4":
                removed_indices.add(j)
                print(f"Removed {items[j]}")
                break
            elif choice == "5":
                removed_indices.update([i, j])
                print(f"Removed {items[i]} and {items[j]}")
                break
            elif choice.lower() == "exit":
                print("\nExiting comparisons early...")
                all_pairs.clear()
                break
            else:
                print("Invalid input. Please enter 1, 2, 3, 4, 5, or 'exit'.")

        # Stop processing further pairs if the user chose to exit
        if choice.lower() == "exit":
            break

        # Update the remaining pairs list to remove references to removed items
        all_pairs = [
            (x, y)
            for x, y in all_pairs
            if x not in removed_indices and y not in removed_indices
        ]

    # Only include items with scores in the final rankings
    ranked_items = [
        (item, scores[item])
        for idx, item in enumerate(items)
        if idx not in removed_indices and scores[item] > 0
    ]
    ranked_items.sort(key=lambda x: -x[1])  # Sort by score in descending order

    print("\nFinal Rankings:")
    if ranked_items:
        for rank, (item, score) in enumerate(ranked_items, start=1):
            print(f"{rank}. {item} (Score: {score})")
    else:
        print("No items were ranked.")


if __name__ == "__main__":
    # file_path = input("Enter the path to the CSV file: ").strip()
    items = read_items_from_csv()

    if not items:
        print("No items to compare. Please check the CSV file.")
    elif len(items) < 2:
        print("You need at least two items to perform comparisons.")
    else:
        compare_items(items)

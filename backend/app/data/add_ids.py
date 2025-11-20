import json

INPUT_PATH = "app/data/postings.json"
OUTPUT_PATH = "app/data/postings_with_id.json"

def add_ids():
    with open(INPUT_PATH, "r") as f:
        postings = json.load(f)

    updated = []
    for idx, posting in enumerate(postings, start=1):
        posting_id = f"JP{idx:03d}"
        posting["id"] = posting_id
        updated.append(posting)

    with open(OUTPUT_PATH, "w") as f:
        json.dump(updated, f, indent=2)

    print(f"Added IDs to {len(updated)} postings.")
    print(f"Saved updated JSON to {OUTPUT_PATH}")

if __name__ == "__main__":
    add_ids()

import json
import re
import html
import unicodedata

INPUT_FILE = "postings.json"
OUTPUT_FILE = "postings_cleaned.json"

# Matches patterns like #URL_xxx#, #EMAIL_xxx#, #PHONE_xxx#, etc.
GENERIC_TOKEN_PATTERN = re.compile(r"#([A-Z]+)_[A-Za-z0-9]+#")

HTML_TAG_PATTERN = re.compile(r"<[^>]+>")


def clean_text(s):
    if not isinstance(s, str):
        return s

    # Normalize unicode
    s = unicodedata.normalize("NFKC", s)

    # Replace all #TOKEN_xxxxxx# → <TOKEN>
    s = GENERIC_TOKEN_PATTERN.sub(lambda m: f"<{m.group(1)}> ", s)

    # HTML-decode entities (&amp; → &)
    s = html.unescape(s)

    # Remove raw HTML tags
    s = HTML_TAG_PATTERN.sub(" ", s)

    # Remove weird unicode whitespace
    s = s.replace("\u00a0", " ")

    # Remove control whitespace
    s = s.replace("\r", " ").replace("\t", " ").replace("\f", " ")

    # Collapse multiple whitespace
    s = re.sub(r"\s+", " ", s)

    return s.strip()


def clean_posting(posting):
    cleaned = {}
    for key, value in posting.items():
        if isinstance(value, str):
            cleaned[key] = clean_text(value)
        else:
            cleaned[key] = value
    return cleaned


def main():
    print("Loading postings...")

    with open(INPUT_FILE, "r") as f:
        postings = json.load(f)

    cleaned_posts = []
    replaced_total = 0

    for p in postings:
        p_str = json.dumps(p)

        # Count all generic tokens
        replaced_total += len(GENERIC_TOKEN_PATTERN.findall(p_str))

        cleaned_posts.append(clean_posting(p))

    with open(OUTPUT_FILE, "w") as f:
        json.dump(cleaned_posts, f, indent=2)

    print(f"Done. Cleaned {len(postings)} postings.")
    print(f"Replaced {replaced_total} placeholder tokens.")
    print(f"Output written to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()

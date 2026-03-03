#!/usr/bin/env python3
"""
Generates site_data.json for the GitHub Pages bird site.
Run this whenever new birds are added to bird_facts.json or bird_photos/.

Usage:
    python3 generate_site_data.py
"""

import os
import json

PHOTOS_DIR = "bird_photos"
FACTS_FILE = "bird_facts.json"
OUTPUT_FILE = "site_data.json"


def main():
    with open(FACTS_FILE) as f:
        all_facts = json.load(f)

    # Build a map from bird name → photo filename
    photo_map = {}
    for fname in os.listdir(PHOTOS_DIR):
        if fname.lower().endswith((".jpg", ".jpeg", ".png")):
            bird_name = os.path.splitext(fname)[0].replace("_", " ").title()
            photo_map[bird_name] = fname

    birds = []
    for bird_name in sorted(all_facts.keys()):
        if bird_name in photo_map:
            birds.append({
                "name": bird_name,
                "photo": f"{PHOTOS_DIR}/{photo_map[bird_name]}",
                "facts": all_facts[bird_name],
            })
        else:
            print(f"No photo for '{bird_name}' — skipping from site.")

    with open(OUTPUT_FILE, "w") as f:
        json.dump(birds, f, indent=2)

    print(f"Generated {OUTPUT_FILE} with {len(birds)} birds.")


if __name__ == "__main__":
    main()

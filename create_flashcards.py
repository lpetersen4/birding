#!/usr/bin/env python3
"""
Creates Anki flashcards from bird photos in the bird_photos/ folder.
- Front of card: bird photo
- Back of card: bird name + facts from bird_facts.json

Usage:
    python3 create_flashcards.py

Output: birds.apkg  (import this file into Anki)

Requirements:
    pip3 install genanki
"""

import os
import json
import genanki

PHOTOS_DIR = "bird_photos"
FACTS_FILE = "bird_facts.json"
OUTPUT_FILE = "birds.apkg"
DECK_ID = 1234567890
MODEL_ID = 9876543213

CARD_FRONT = """\
<div style="text-align:center; font-family:Arial, sans-serif;">
  {{Photo}}
</div>
"""

CARD_BACK = """\
<div style="font-family:Arial, sans-serif; max-width:600px; margin:auto; text-align:center;">
  {{Photo}}
  <h2 style="color:#2c5f2e; margin:12px 0;">{{BirdName}}</h2>
  {{Facts}}
</div>
"""

FACTS_STYLE = """\
<style>
  .facts { text-align:left; margin-top:12px; }
  .fact-section { margin-bottom:8px; }
  .fact-label { font-weight:bold; color:#2c5f2e; font-size:13px; text-transform:uppercase; letter-spacing:0.5px; }
  .fact-text { font-size:14px; color:#333; margin-top:2px; }
</style>
"""


def build_facts_html(facts: dict) -> str:
    sections = [
        ("Size & Shape",    facts.get("size_shape", "")),
        ("Color & Pattern", facts.get("color_pattern", "")),
        ("Where to Find",   facts.get("where_to_find", "")),
        ("What They Eat",   facts.get("what_they_eat", "")),
        ("Behavior",        facts.get("behavior", "")),
    ]
    html = FACTS_STYLE + '<div class="facts">'
    for label, text in sections:
        html += (
            f'<div class="fact-section">'
            f'<div class="fact-label">{label}</div>'
            f'<div class="fact-text">{text}</div>'
            f'</div>'
        )
    html += '</div>'
    return html


def main():
    # Rename any files with spaces to use underscores
    for f in os.listdir(PHOTOS_DIR):
        if " " in f:
            new_name = f.replace(" ", "_")
            os.rename(os.path.join(PHOTOS_DIR, f), os.path.join(PHOTOS_DIR, new_name))
            print(f"Renamed: '{f}' -> '{new_name}'")

    photos = [
        f for f in os.listdir(PHOTOS_DIR)
        if f.lower().endswith((".jpg", ".jpeg", ".png"))
    ]
    if not photos:
        raise SystemExit(
            f"No photos found in '{PHOTOS_DIR}/'. "
            "Add bird photos named like 'American Robin.jpg' and run again."
        )

    with open(FACTS_FILE) as f:
        all_facts = json.load(f)

    # Deduplicate: keep only the first photo per bird name
    seen = {}
    for photo_filename in sorted(photos):
        bird_name = os.path.splitext(photo_filename)[0].replace("_", " ").title()
        if bird_name in seen:
            print(f"Skipping duplicate: {photo_filename} (already have {seen[bird_name]})")
        else:
            seen[bird_name] = photo_filename
    photos = list(seen.values())

    print(f"Found {len(photos)} photo(s): {', '.join(photos)}\n")

    model = genanki.Model(
        MODEL_ID,
        "Bird Identification",
        fields=[
            {"name": "BirdName"},
            {"name": "Photo"},
            {"name": "Facts"},
        ],
        templates=[
            {
                "name": "Bird ID Card",
                "qfmt": CARD_FRONT,
                "afmt": CARD_BACK,
            }
        ],
    )

    deck = genanki.Deck(DECK_ID, "Bird Identification")
    media_files = []
    missing_facts = []

    for photo_filename in photos:
        bird_name = os.path.splitext(photo_filename)[0].replace("_", " ").title()

        if bird_name not in all_facts:
            missing_facts.append(bird_name)
            print(f"WARNING: No facts found for '{bird_name}' — skipping.")
            continue

        print(f"Adding card: {bird_name}")
        photo_html = f'<img src="{photo_filename}" style="max-width:480px; max-height:380px; border-radius:8px;">'
        facts_html = build_facts_html(all_facts[bird_name])

        note = genanki.Note(
            model=model,
            fields=[bird_name, photo_html, facts_html],
        )
        deck.add_note(note)
        media_files.append(os.path.join(PHOTOS_DIR, photo_filename))

    if missing_facts:
        print(f"\nSkipped (no facts): {', '.join(missing_facts)}")
        print(f"Add entries for these birds to {FACTS_FILE} and re-run.")

    if not deck.notes:
        raise SystemExit("No cards were created.")

    package = genanki.Package(deck)
    package.media_files = media_files
    package.write_to_file(OUTPUT_FILE)

    print(f"\nCreated {len(deck.notes)} card(s) -> {OUTPUT_FILE}")
    print("Import birds.apkg into Anki: File > Import")


if __name__ == "__main__":
    main()

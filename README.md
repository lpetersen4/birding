# Birds

A personal birding project with two outputs: Anki flashcards for learning bird identification, and a GitHub Pages site for browsing my life list.

**https://lpetersen4.github.io/birding/**

## Site

**[Bird Directory](index.html)** — searchable grid of every bird I've seen, with a photo and field guide facts for each one.

**[Life List](life-list.html)** — a simple numbered list of all species observed.

---

## Adding a new bird

1. Drop a photo into `bird_photos/` named after the bird (e.g. `American Robin.jpg`)
2. Run `/update-birds` in Claude Code

That's it. Claude will generate field guide facts for any new bird, rebuild the Anki deck, and regenerate the site data — all in one step.

---

## Project structure

```
bird_photos/            Bird photos (one per species, named by common name)
bird_facts.json         Field guide facts for each bird, keyed by common name
site_data.json          Generated — bird data consumed by the website (do not edit)
create_flashcards.py    Builds birds.apkg for import into Anki
generate_site_data.py   Regenerates site_data.json from bird_facts.json + bird_photos/
index.html              Bird directory page
life-list.html          Life list page
styles.css              Shared styles
```

## Manual usage

```bash
python3 create_flashcards.py   # → birds.apkg (import into Anki)
python3 generate_site_data.py  # → site_data.json (used by the website)
```

## Publishing the site

In your repository settings, go to **Settings → Pages** and set the source to the `main` branch, root folder.

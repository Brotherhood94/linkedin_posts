# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A personal system for writing LinkedIn posts in the author's voice. The root `.md` files are a style guide reverse-engineered from ~123 real posts (`Shares.csv`); the `post_N/` folders are individual posts produced with that guide.

## When asked to write a new post

1. Create a **new folder** named `post_N`, where `N` is the next unused integer (existing: `post_0`, `post_1` → next is `post_2`).
2. Write the post into `post_N/post.md`. Match the format of existing `post.md` files: a metadata header (Type, Language, Status, Media, Source, First-comment link), the copy-paste-ready post, the first-comment block, and review notes.
3. **Only generate a GIF if the author explicitly asks for one.** When asked, add `post_N/make_gif.py` — a self-contained matplotlib script (see `post_1/make_gif.py`) that renders a square, dark, looping diagram of the *idea* (not people) and outputs `research_copilot.gif`-style media plus a `preview.png` QA frame. Run it with `python post_N/make_gif.py` (needs `numpy`, `matplotlib`, Pillow).
4. Do **not** generate any media unless the post explicitly needs it and the author asked.

## Follow the style guide — don't restate it

Before drafting any post, read and apply these (they are the source of truth; do not duplicate their rules here):

| File | Use it for |
|------|-----------|
| `good_approaches.md` | The 6-block skeleton + the **pre-flight checklist to run before returning any post** |
| `bad_approaches.md` | 10 anti-patterns to cross-check against — none should be present |
| `tone_of_voice.md` | Voice, signature phrases, register by topic |
| `length_and_structure.md` | Length calibration + structural archetypes |
| `emoji_usage.md` | Emoji palette, semantics, placement |
| `post_templates.md` | 7 drop-in skeletons mapped to real posts |
| `README.md` | Index + TL;DR profile |

## Hard rules (surfaced here because they're easy to violate)

- **One language per post.** ~60% English / ~40% Italian overall, but **never mix EN and IT inside a single post.**
- **Links go in the FIRST COMMENT**, never in the post body. Point to it with `👇🏻`.
- **Acks at the bottom**, opened with `🙏🏻`; tag collaborators so they get notified.
- **Title is one emoji-first line** with the key noun in bold unicode (`𝗯𝗼𝗹𝗱`); every body paragraph starts with a meaningful emoji and is 1–3 lines.
- **3–5 inline hashtags**, not a bottom hashtag block.
- **Media: GIF > photo > video**, and it should convey the idea, not the people.
- Always run the `good_approaches.md` pre-flight and the `bad_approaches.md` cross-check before returning a post.

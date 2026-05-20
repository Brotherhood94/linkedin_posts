# Length & Structure — Quantitative profile of my LinkedIn posts

Based on 123 substantive posts (>50 chars), May 2019 → March 2026.

---

## Length statistics

| Statistic | Characters |
|-----------|-----------|
| Minimum (substantive) | ~90 |
| Median | **676** |
| Mean | **739** |
| Maximum | 2,933 |

### Length distribution

| Bucket | # of posts | Share | Typical use |
|--------|------------|-------|-------------|
| **<300 chars** | 32 | 26% | Quick news, share-a-link, "I'm at X" |
| **300–600 chars** | 16 | 13% | Short announcements, brief recaps |
| **600–1,000 chars** | 34 | 28% | **Sweet spot.** Research drops, talks, podcasts |
| **1,000–1,500 chars** | 28 | 23% | Multi-block posts (event + speakers + when/where) |
| **>1,500 chars** | 13 | 11% | Deep explainers, big event recaps, full essays |

**The default target is 600–1,000 characters.** That's where my best research-announcement posts sit (e.g., the QKNN post at 696, the QIP2026 poster at 657).

**Hard ceiling: ~1,500 characters.** Beyond that, only explainer essays or large event recaps justify it.

---

## Paragraph structure

- **Median paragraphs per post: 1** (per `\n\n` split — but note the CSV preserves paragraph breaks as `""\n""`, so visually each post has **5–10 short blocks**).
- **Visual paragraph rule:** each paragraph is **1–3 short lines** on a desktop view, separated by a blank line.
- **No 4+ line paragraphs.** If a paragraph hits 4 lines, split it.

---

## Hashtag profile

| Metric | Value |
|--------|-------|
| Total hashtags (corpus) | 429 |
| Unique hashtags | 307 |
| **Mean per post** | **3.5** |
| Top tags | `#quantum` (26), `#QuantumComputing` (7), `#PointerPodcast` (4), `#PhD` (3), `#Pisa` (3) |

**Rule:** 2–5 hashtags per post. Prefer INLINE placement (`the #parallelism of #quantum gates`) over a hashtag block at the bottom. Use a bottom hashtag cluster only for community/event tags (e.g., `#CodemotionCommunity`).

---

## Emoji profile

| Metric | Value |
|--------|-------|
| Mean emojis per post | **4.6** |
| Median emojis per post | **3** |
| Max emojis in one post | 17 |
| Posts starting with an emoji | **51%** (63/123) |

See `emoji_usage.md` for the full vocabulary and per-emoji semantics.

---

## Structural patterns (5 main archetypes)

### Archetype 1 — Research / preprint drop (target: 700–1300 chars)

```
🎊 𝗡𝗲𝘄 <thing> 𝗶𝘀 𝗼𝘂𝘁! 🎊
<EMOJI> <One-line problem framing>

🤔 <Rhetorical question to the target reader>
Usually, we 𝙖𝙨𝙨𝙪𝙢𝙚 <common assumption>.

⛔ <Why that assumption is fragile>

🛠️ We provide <our contribution in one sentence>.

📦 <Detail 1 with bold-styled key term>
🔑 <Detail 2 with bold-styled key term>

🚀 <Punchy summary of impact>

⏱️ 𝘞𝘩𝘢𝘵 𝘢𝘳𝘦 𝘰𝘶𝘳 𝘤𝘰𝘯𝘵𝘳𝘪𝘣𝘶𝘵𝘪𝘰𝘯𝘴?
― 🟣 <Bullet 1>
― 🟣 <Bullet 2>

<Italic re-statement of the question for the reader>
📺 Check the GIF for a high-level understanding
👉🏻 𝗧𝗵𝗲 <link type> link: <bitly>

🙏 Thanks to <co-authors>.
```

Reference: the QRAM preprint post (1,252 chars).

---

### Archetype 2 — Talk / podcast / event appearance (target: 600–900 chars)

```
🎙️ <Opener: hook about the appearance>

<EMOJI> <Who invited me + 1-line context>

During the podcast / talk, we covered:
🟣 <Topic 1>
🟣 <Topic 2>
🟣 <Topic 3>
🟣 <Topic 4>

🙏🏻 Thanks to <organizer>

👇🏻 If you're curious, check out the link in the first comment!
```

Reference: the Quantum.IT podcast post (913 chars), QKNN post (696 chars).

---

### Archetype 3 — Event announcement (target: 800–1400 chars)

```
🎊 <Event name> torna a <City>! / <Event name> is back!

🎟️ <Ticket / registration headline in 𝗯𝗼𝗹𝗱>

🤫 <Behind-the-scenes context>

🌍 <Track / theme description>

Sul palco / On stage: <list of speakers/companies>

🗓️ 𝗤𝘂𝗮𝗻𝗱𝗼/𝗪𝗵𝗲𝗻: <date>
📍 𝗗𝗼𝘃𝗲/𝗪𝗵𝗲𝗿𝗲: <location>

🔹 <Practical detail (free entry, limited seats, etc.)>
👇🏻 <Link to register> nel primo commento / in the first comment

⚠️ <Optional teaser for what's coming next>
```

Reference: Quantum Festival posts (1,174 / 1,771 chars).

---

### Archetype 4 — Provocative essay / explainer (target: 1,200–2,000 chars)

```
<EMOJI> <Provocative title or metaphor (the "elephant")>

🔥 <Hook: surprising claim>

👀 <Context: what most people don't realize>

👉🏻 <The "twist": the counterintuitive fact>

(<Italic aside in soft voice>)

🔬 <Deeper explanation, technical detail>

⛔ / 🚀 <Stake / implication>

🙏🏻 <Optional: tie to my/our work or research community>

<EMOJI> <CTA or invitation to discuss>
```

Reference: "L'elefante nella stanza" post (2,933 chars — exceptionally long), "F*ck Agentic Coding" (819 chars).

---

### Archetype 5 — Event recap / gratitude (target: 1,200–2,000 chars)

```
✨ What an amazing ride it has been!

<EMOJI> <One-line "it's over" / "we wrapped up" statement>

🎯 <Headline number: participants / talks / tracks>

🧠 <Memorable anecdote — a specific moment people will recognize>

👨‍🏫 A special thank you to <Names> for <specific contribution>

🎤 A huge shoutout to <group> — <why they mattered>

🤝🏻 Immense gratitude to my fellow co-organizers: <Names>

🎬 A heartfelt thanks to our staff: <Names>

⭐ And of course, a warm thank-you to our advisors: <Names>

❤️ <Closing emotional line + forward-looking promise>
```

Reference: Quantum Festival 2025 recap (1,883 chars).

---

### Archetype 6 — Quick news / "I just want to share this" (target: 100–300 chars)

```
🔥 <One-line news>
```
or
```
👀 Quick #interruption from your daily scrolling!

🔥 <One-line news>

🙌🏻 <Optional context>; link in the first comment!
```

Reference: the postdoc position post (92 chars), the Oracles update (232 chars).

---

## Language distribution

| Language | Share | Notes |
|----------|-------|-------|
| English | ~60% | Default for research, international audience |
| Italian | ~40% | Used for Pisa/Italy events, Italian community, podcasts |

Never mix EN + IT in one post (except for proper nouns and hashtags).

---

## "Pre-flight" length checklist

Before publishing:
- [ ] Total chars: between 400 and 1,500 (unless it's a deliberate quick-news or essay)?
- [ ] No paragraph longer than 3 lines?
- [ ] Title line is one line only?
- [ ] At least one blank line between every paragraph?
- [ ] 2–5 hashtags total?
- [ ] 3–8 emojis total (more is fine for long event recaps)?

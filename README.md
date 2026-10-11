<p align="center"><img src="assets/banner.png" alt="cropmark" width="100%"></p>

# cropmark

<p align="center"><a href="https://skills.sh/jdann1el/cropmark/cropmark"><img src="https://skills.sh/b/jdann1el/cropmark?style=flat-square" alt="skills.sh"></a> <img src="https://img.shields.io/badge/license-MIT-f4c430?style=flat-square" alt="MIT"> <img src="https://img.shields.io/badge/agents-Claude%20Code%20%C2%B7%20Codex%20%C2%B7%20Cursor%20%C2%B7%20OpenCode-111?style=flat-square" alt="agents"></p>

```bash
npx skills add jdann1el/cropmark -g
```

**An agent skill for portfolio-level social media design**: YouTube thumbnails, single posts and 4:5 carousels — made from scratch, or by upgrading a weak existing piece.

Most AI-made social graphics look like "a template with a stock photo". cropmark encodes how studio designers actually work — one idea per frame told by the image, type with real contrast, brand elements used as graphics, carousels built as an argument — plus the engines and QA to ship it.

<p align="center"><img src="examples/gallery.jpg" alt="examples made with cropmark" width="100%"></p>

## What's inside
Everything the agent loads lives in `skills/cropmark/`; the repo root only adds this README, examples and evals.
| | |
|---|---|
| `skills/cropmark/SKILL.md` | Short router: what to read for each task + non-negotiables |
| `formats/` | Thumbnail, post, carousel, other (story, X, square) — sizes, safe zones, feed tests |
| `styles/` | 18 style cards distilled from current Behance work (cinematic stakes, UI hero, editorial maximal, zine collage, luxury real estate, product hero dark…) |
| `techniques/` | Story in one frame, typography pairings, carousel system, upgrading, imagery |
| `engines/pillow` | `cm.py`: grading, text with tracking/stroke/shadow, in-scene cards, sticky notes, tags, halftone, torn paper, cutout cleanup, before/after sheets |
| `engines/html` | `render.mjs`: HTML/CSS → PNG with Playwright, panoramic carousels sliced automatically, bundled fonts injected |
| `qa/` | `qa.py` (size, safe zones, badge zone, contrast, word count, feed previews) + rubric |
| `adapters/` | Hark, Claude Code, Codex, generic |
| `fonts/` | 20+ OFL fonts (Anton, Bebas Neue, DM Serif Display, Instrument Sans/Serif, Outfit, Pinyon Script, Caveat…) |

## Install

**Any agent (Claude Code, Codex, Cursor, OpenCode…)** — via the open [`skills`](https://github.com/vercel-labs/skills) CLI:
```bash
npx skills add jdann1el/cropmark -g      # install globally, pick your agents
npx skills update                         # pull the latest version later
```

**Claude Code, as a plugin (can auto-update)**:
```
/plugin marketplace add jdann1el/cropmark
/plugin install cropmark@cropmark
```
Updates: `/plugin marketplace update cropmark`, or turn on auto-update in `/plugin` → Marketplaces → cropmark.

**Manual (git)** — clone and point your agent at `skills/cropmark/SKILL.md`; update with `git pull`:
```bash
git clone https://github.com/jdann1el/cropmark.git
ln -s "$PWD/cropmark/skills/cropmark" ~/.claude/skills/cropmark   # Claude Code
ln -s "$PWD/cropmark/skills/cropmark" ~/.agents/skills/cropmark   # Codex
```

**Engines** (once, inside the installed `cropmark/` skill folder):
```bash
pip install pillow
cd engines/html && npm i && npx playwright install chromium
```

Image generation is optional: with an image model the skill uses it for text-free bases; without one it falls back to user/stock photos or photo-free styles.

## Results
Baseline (same agent, no skill) vs cropmark on 12 frozen briefs: average 3.3 → 4.2 on a 7-criterion rubric, 11 of 12 pairs won (1 tie); unseen hold-out briefs 4.1. Self-scored — see `evals/`. Run your own: the briefs are there.

## Principles
1. Concept before pixels. 2. The image carries the story; text confirms it. 3. Type with character. 4. One focal point. 5. Generated images contain no text. 6. Never invent numbers, quotes or claims. 7. Look at every render at feed size before shipping.

## Credits & license
MIT (code and docs). Fonts: SIL OFL 1.1. Styles were learned from public portfolios and rewritten as original guidance; no third-party images are included (sources in `refs/index.md`). Ideas, not code, from anthropics/skills `canvas-design`, op7418 guizang social cards and charlie947 social-media-skills.

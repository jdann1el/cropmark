# Adapter: Claude Code
- Install: `npx skills add jdann1el/cropmark -g`, or `/plugin marketplace add jdann1el/cropmark` then `/plugin install cropmark@cropmark`, or copy this folder to `~/.claude/skills/cropmark/`. SKILL.md front matter is already in the Agent Skills format.
- Imagery: Claude Code has no built-in image generator. Use, in order: user/brand photos → free stock downloaded with curl (keep the URL) → an image API/MCP the user has configured (e.g. an OpenAI/Gemini image tool). If none, use the HTML engine with flat colour, type and shapes (styles: editorial-maximal-yellow, zine-collage without photo, brand-color-block with drawn shapes).
- Look at renders by reading the PNG file (Claude can view images).
- Engines: `pip install pillow`; `cd engines/html && npm i && npx playwright install chromium`.

# Adapter: any agent (Hermes, Cursor, custom)
Minimum capabilities: read files, run Python (Pillow) and/or Node (Playwright), view images.
1. Load SKILL.md, follow its routing table.
2. Map "generate image" to whatever image model you have; if none, use photo-free styles.
3. Always view outputs before delivering; never ship unseen.

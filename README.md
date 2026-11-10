# sutram-social

Public images and captions for the Sutram Instagram account (@sutramthread), scheduled through Metricool.
Images live at raw.githubusercontent.com links so Metricool can fetch them. Nothing private goes here: no birth details, no keys.

- posts/<post-id>/<post-id>-<n>.jpg  slides at 1080 x 1350
- captions/<post-id>.txt            caption for each post
- tools/                            slide theme, sky computation (Swiss Ephemeris, Lahiri), build scripts
- plan/                             daily system, lesson track, posting log

## Design v6 (10 Nov 2026)

- `python3 tools/render.py specs/<id>.json` draws the slides. It prints any slide whose text had to shrink; fix those by hand, text stays big.
- `python3 tools/motion.py specs/<id>.json` makes the moving cover, `posts/<id>/<id>-1.mp4`: an 8 second loop whose first frame is the still cover. A slide's `motion` key sets which rooms take the light (`order`), sparks between rooms (`spark`) and where the grahas walk in from (`from`).
- `python3 tools/buffer_assets.py <id> <commit-sha> [--video] [--slides 1,2,3,4]` prints the text and assets for a Buffer post, pinned to a commit.
- Rooms (`scene`): signs in order left to right, so ahead is right; inside a room the graha with more degrees stands further right; facing rooms hang from above.
- Other pictures: `figure` and `bodymap` (the person of Time), `north` with `hi` (one house lit), `rows` with `roworbs`, `compare` columns with a `scene`.

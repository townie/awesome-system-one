# Sources ingested

Ingest date: **2026-09-25 PT** (America/Los_Angeles).

| Source | URL | Artifact used |
| --- | --- | --- |
| AbdelStark/awesome-typesafe-jev | https://github.com/AbdelStark/awesome-typesafe-jev | README.md + resources.json |
| logicrw/awesome-jev-projects | https://github.com/logicrw/awesome-jev-projects | README.md |
| OmniJev/awesome-jev-gallery | https://github.com/OmniJev/awesome-jev-gallery | README.md |
| AppitStudio/awesome-jev | https://github.com/AppitStudio/awesome-jev | README.md |
| BeatAPI/awesome-jev | https://github.com/BeatAPI/awesome-jev | README.md + data/projects.json |
| rupeshpoojary9/awesome-open-system-one | https://github.com/rupeshpoojary9/awesome-open-system-one | README.md |
| kydlikebtc/awesome-jev | https://github.com/kydlikebtc/awesome-jev | README.md + catalog.json |
| MrJev/awesome-jev | https://github.com/MrJev/awesome-jev | README.md |
| systemonemodels.org alternatives | https://systemonemodels.org/examples/alternatives/ | HTML index |
| seed-official / seed-essays / seed-tier / seed-lists | (manual) | Official docs, essays, Tier A/B models, list self-links |
| seed-logicrw-refresh | https://logicrw.github.io/awesome-jev-projects/projects.json | 2026-09-24 evidenced projects missing from prior ingest |
| Reddit r/LLMDevs top-20 roundup | https://www.reddit.com/r/LLMDevs/comments/1wko2e5/i_reviewed_287_opensource_jev_projects_here_are/ | Community review post (credit) |

Normalization: strip trailing `/`, `.git`, `www.`, URL fragments/queries; exclude badge/shield hosts, issue templates, and known unrelated collisions (e.g. LayaAir).

Ordering: within each category/subsection, pinned and landmark URLs stay first; remaining entries are sorted by GitHub stars (descending), then title. Star counts live in `stars_cache.json` (fetched via `gh api graphql`). Non-GitHub URLs are treated as unknown and sort after starred repos. Refresh with `python3 build.py --refresh-stars`. This is a star-count proxy, not a citation-graph PageRank.

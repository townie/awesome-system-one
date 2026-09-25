#!/usr/bin/env python3
from __future__ import annotations
import json, re, collections, subprocess, sys, time, os
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse, urlunparse

ROOT = Path(__file__).resolve().parent
RAW, OUT = ROOT / "raw", ROOT
STARS_CACHE = OUT / "stars_cache.json"
# GraphQL batch size — polite to the API; ~1090 repos ≈ 22 calls.
STARS_BATCH = 50
# Skip re-fetching cache entries newer than this many days unless --refresh-stars.
STARS_TTL_DAYS = 14
GH_SKIP_OWNERS = {
    "topics", "orgs", "sponsors", "settings", "marketplace", "features", "pricing",
    "about", "login", "join", "explore", "collections", "events", "codespaces",
    "copilot", "enterprise", "security", "customer-stories", "readme", "pulls",
    "issues", "notifications", "stars", "watch", "new", "apps", "account",
}

def normalize_url(url: str) -> str:
    url = (url or "").strip()
    if not url or url.startswith(("#", "mailto:")): return ""
    url = url.split("#")[0].split("?")[0].rstrip("/")
    if url.endswith(".git"): url = url[:-4]
    if not urlparse(url).scheme:
        if url.startswith(("github.com/", "www.github.com/")): url = "https://" + url
        else: return ""
    p = urlparse(url)
    host = (p.netloc or "").lower()
    if host.startswith("www."): host = host[4:]
    path = (p.path or "").rstrip("/")
    while "//" in path: path = path.replace("//", "/")
    for suf in ("/README.md", "/index.html"):
        if path.endswith(suf): path = path[: -len(suf)]
    return urlunparse((p.scheme.lower(), host, path, "", "", ""))

EXCLUDE_HOST = {"awesome.re", "img.shields.io", "camo.githubusercontent.com", "cdn.jsdelivr.net", "raw.githubusercontent.com"}
EXCLUDE_SUB = ["badge", "shields.io", "all-contributors", "dependabot", "actions/workflows", "github.com/sindresorhus/awesome", "buymeacoffee", "opencollective.com", "paypal.com", "twitter.com/intent", "x.com/intent"]
EXCLUDE_REPOS = {"layabox/layaair", "layabox/layaair2.0", "layabox/layaair3.0"}
TITLE_BAD = re.compile(r"layaair|layabox", re.I)

def should_exclude(url: str, title: str = "") -> bool:
    if not url: return True
    n = normalize_url(url)
    if not n: return True
    p = urlparse(n); host = p.netloc.lower(); low = n.lower()
    if host in EXCLUDE_HOST: return True
    if any(s in low for s in EXCLUDE_SUB): return True
    m = re.match(r"^https?://github\.com/([^/]+)/([^/]+)", n, re.I)
    if m and f"{m.group(1).lower()}/{m.group(2).lower()}" in EXCLUDE_REPOS: return True
    if title and TITLE_BAD.search(title): return True
    if any(x in low for x in ("/issues/new", "/edit/main/", "/blob/main/CONTRIBUTING")): return True
    if low.endswith(("/license", "/contributing.md")): return True
    if "/assets/" in low and host == "github.com": return True
    if "opengraph.githubassets.com" in low: return True
    # deep github blob/tree evidence links — keep repo roots only
    if re.search(r"github\.com/[^/]+/[^/]+/(blob|tree)/", low): return True
    # radar secondary project pages (repo already listed)
    if "logicrw.github.io/awesome-jev-projects" in low and "/projects/" in low: return True
    if "abdelstark.github.io/awesome-typesafe-jev/projects/" in low: return True
    if "abdelstark.github.io/awesome-typesafe-jev/categories/" in low: return True
    return False

LINK_RE = re.compile(r"""^\s*[-*]\s+(?:\*\*)?\[(?:\*\*)?([^\*\]]+)(?:\*\*)?\](?:\*\*)?\(([^)]+)\)(?:\*\*)?\s*(?:[—–\-·]|\s+[—–]\s+|\s+·\s+)?(.*)$""", re.M)

CAT_HOSTED = "Hosted: TypeSafe Jev"
CAT_DOCS = "Docs & essays"
CAT_OS = "Open-source / local alternatives"
CAT_LISTS = "Awesome lists & indexes"
CAT_SDKS = "SDKs & tooling"
CAT_EVALS = "Evals & papers"
CAT_USE = "Use cases"
CAT_COMMUNITY = "Community"

# Docs home (live intro), primitives, HTTP API — the only TypeSafe sitemap we keep here.
HOSTED_KEEP = (
    "https://docs.typesafe.ai",
    "https://docs.typesafe.ai/primitives",
    "https://docs.typesafe.ai/api",
)
PIN_HOSTED = list(HOSTED_KEEP)

# Legacy names from earlier dumps / upstream headings
CAT_ALIASES = {
    "Official": CAT_HOSTED,
    "Open models & alternatives": CAT_OS,
    "Demos": CAT_USE,
}

SECTION_MAP = [
    (re.compile(r"research and writing|docs|essay|reference and reading|concepts|manifesto|blog|showcase", re.I), CAT_DOCS),
    (re.compile(r"open model|reproduction|alternative|local model|open.?source|local.?port|mlx|core.?ml", re.I), CAT_OS),
    (re.compile(r"awesome|index|directory|gallery|catalog|radar", re.I), CAT_LISTS),
    (re.compile(r"sdk|client librar|integration|developer tool|tooling|mcp|constrained|structured decoding|calibration and selective|agent and developer|cli|pipeline", re.I), CAT_SDKS),
    (re.compile(r"eval|benchmark|jevbench|independent research|paper|calibration audit", re.I), CAT_EVALS),
    (re.compile(r"demo|application|workflow|game|robot|browser|creative|use case|see jev at work|security|guardrail|data.?search|code navigation|model routing", re.I), CAT_USE),
    (re.compile(r"community|discord|show and tell|updates", re.I), CAT_COMMUNITY),
]

def category_from_heading(heading: str):
    for rx, cat in SECTION_MAP:
        if rx.search(heading or ""): return cat
    return None

def infer_category(url, title, heading, hint=None):
    if hint: return CAT_ALIASES.get(hint, hint)
    c = category_from_heading(heading)
    if c: return c
    low = (url + " " + title).lower()
    nu = normalize_url(url)
    if nu in HOSTED_KEEP:
        return CAT_HOSTED
    if any(x in low for x in ("typesafe.ai", "docs.typesafe", "console.typesafe", "evals.typesafe")):
        if "evals.typesafe" in low:
            return CAT_EVALS
        if any(x in low for x in ("/cookbooks", "/patterns", "/demos", "use-case-map")):
            return CAT_USE
        if any(x in low for x in ("console.typesafe", "agent-skill", "/sdk")):
            return CAT_SDKS
        return CAT_DOCS
    if any(x in low for x in ("arxiv.org", "benchmark", "eval", "jevals", "jevbench", "calibration", "paper")): return CAT_EVALS
    if "awesome" in low and "github.com" in low: return CAT_LISTS
    if any(x in low for x in ("laya", "nanojev", "semif", "openjev", "/kev", "nimble", "decider", "jevlike", "mini-jev", "jevmlx", "poorjev", "huggingface.co", "modernbert", "gliner", "setfit", "openthai", "reflex", "verdict", "litjev", "open-alternative", "pocketjev", "simple-jev", "simplejev", "coreml", "jevcoreml")):
        return CAT_OS
    if any(x in low for x in ("sdk", "client", "mcp", "outlines", "instructor", "xgrammar", "guidance", "dspy")): return CAT_SDKS
    if any(x in low for x in ("discord", "x.com/typesafe", "linkedin.com/company/typesafe")): return CAT_COMMUNITY
    if any(x in low for x in ("archerhume", "lilting.ch", "latent.space", "learnjev", "navinpai", "warmersun", "kevnu.com", "langchain.com/blog", "systemonemodels.org")): return CAT_DOCS
    if any(x in low for x in ("demo", "snake", "mario", "pokemon", "chess", "game", "play")): return CAT_USE
    return CAT_USE

def clean_desc(s):
    if not s: return ""
    s = re.sub(r"<[^>]+>", "", s)
    s = re.sub(r"\s+", " ", s).replace("**", "").replace("__", "")
    s = re.sub(r"(?<!\w)\*(?!\*)", "", s)
    s = re.sub(r"^[\s⭐★☆·•]+", "", s)
    s = re.sub(r"^(?:stars?\s*[·•|]\s*)+", "", s, flags=re.I)
    if len(s) > 240: s = s[:237].rsplit(" ", 1)[0] + "…"
    return s.strip(" -—–|")

def prefer_desc(a, b):
    a, b = a or "", b or ""
    if not a: return b
    if not b: return a
    fluff = ("awesome", "check it out", "amazing", "best ever")
    af, bf = sum(f in a.lower() for f in fluff), sum(f in b.lower() for f in fluff)
    if af != bf: return a if af < bf else b
    concrete = ("ece", "brier", "apache", "mit", "choice", "score", "noul", "mlx", "qwen", "modernbert", "calibration", "system one", "rlcd")
    ac, bc = sum(t in a.lower() for t in concrete), sum(t in b.lower() for t in concrete)
    if ac != bc: return a if ac > bc else b
    return a if len(a) >= len(b) else b

def prefer_title(a, b):
    a, b = (a or "").strip(), (b or "").strip()
    if not a: return b
    if not b: return a
    if a.lower() in ("link", "here", "repo", "github"): return b
    if b.lower() in ("link", "here", "repo", "github"): return a
    return a if len(a) <= len(b) + 10 else b

# Merge priority when the same URL appears in multiple sources (lower wins).
# Display order is ORDER in render_readme — not this map.
RANK = {
    CAT_HOSTED: 0,
    "Official": 0,
    CAT_DOCS: 1,
    CAT_OS: 2,
    CAT_EVALS: 3,
    CAT_LISTS: 4,
    CAT_COMMUNITY: 5,
    CAT_SDKS: 6,
    CAT_USE: 7,
    "Open models & alternatives": 2,
    "Demos": 7,
}

class Entry:
    __slots__ = ("url","title","description","category","sources","subsection")
    def __init__(self, url, title, description, category, source):
        self.url, self.title, self.description, self.category = url, title, description, CAT_ALIASES.get(category, category)
        self.sources = {source} if isinstance(source, str) else set(source or [])
        self.subsection = ""
    def merge(self, title, description, category, source):
        self.title = prefer_title(self.title, title)
        self.description = prefer_desc(self.description, description)
        category = CAT_ALIASES.get(category, category)
        if RANK.get(category, 9) < RANK.get(self.category, 9): self.category = category
        if source: self.sources.add(source)

def add(entries, url, title, desc, cat, source):
    if should_exclude(url, title): return
    nu = normalize_url(url)
    if not nu: return
    desc = clean_desc(desc)
    if nu in entries: entries[nu].merge(title, desc, cat, source)
    else: entries[nu] = Entry(nu, title, desc, cat, source)


def parse_markdown_all_links(text, source, entries, default_cat=None):
    """Fallback: harvest all markdown links on list lines, including - **[t](u)** · desc."""
    heading = ""
    for line in text.splitlines():
        hm = re.match(r"^#{1,3}\s+(.+)$", line)
        if hm:
            heading = hm.group(1).strip(); continue
        if not re.match(r"^\s*[-*|]\s+", line) and "| **" not in line and not line.strip().startswith("|"):
            # still allow table rows with links
            if "[" not in line: continue
        for m in re.finditer(r"\[([^\]]+)\]\((https?://[^)]+)\)", line):
            title, url = m.group(1).strip(), m.group(2).strip()
            if title.startswith("!"): continue  # images
            if title.lower() in {"source", "fixed-commit evidence", "original case", "code", "website", "model"}: continue
            # description: text after last link on the line, or between · and [
            desc = ""
            # try after emdash/· following this link
            idx = line.find(f"]({url})")
            after = line[idx+len(f"]({url})"):] if idx>=0 else ""
            after = re.sub(r"^(\*\*|\s|·|—|–|-|:)+", "", after)
            after = re.split(r"\[|\|", after)[0]
            desc = clean_desc(after)
            add(entries, url, title, desc, infer_category(url, title, heading) or default_cat or CAT_USE, source)

def parse_markdown(text, source, entries):
    heading = ""
    for line in text.splitlines():
        hm = re.match(r"^#{1,3}\s+(.+)$", line)
        if hm:
            heading = hm.group(1).strip(); continue
        m = LINK_RE.match(line)
        if not m: continue
        title, url, desc = m.group(1).strip(), m.group(2).strip(), (m.group(3) or "").strip()
        if url.startswith(("/", "./", "../", "#")): continue
        add(entries, url, title, desc, infer_category(url, title, heading), source)

def parse_abdelstark_json(path, entries):
    data = json.loads(path.read_text()); source = "AbdelStark/awesome-typesafe-jev"
    cat_map = {"client-libraries-and-integrations":CAT_SDKS,"agent-and-developer-tooling":CAT_SDKS,"browser-agents":CAT_USE,"applications-and-workflows":CAT_USE,"games-and-robotics":CAT_USE,"evaluations-and-independent-research":CAT_EVALS,"showcases-and-field-notes":CAT_DOCS}
    for cat in data.get("categories", []):
        hint = cat_map.get(cat.get("id"))
        for r in cat.get("resources", []):
            url, title = r.get("url") or "", r.get("name") or ""
            desc = r.get("description_markdown") or ""
            add(entries, url, title, desc, hint or infer_category(url, title, cat.get("name","")), source)

def parse_kyd_catalog(path, entries):
    data = json.loads(path.read_text()); source = "kydlikebtc/awesome-jev"
    kind_map = {"official-docs":CAT_DOCS,"sdk":CAT_SDKS,"integration":CAT_SDKS,"plugin":CAT_SDKS,"project":CAT_USE,"alternative":CAT_OS,"benchmark":CAT_EVALS,"article":CAT_DOCS,"tutorial":CAT_DOCS,"snippet":CAT_SDKS,"video":CAT_DOCS,"discussion":CAT_COMMUNITY}
    for r in data:
        url, title, desc = r.get("url") or "", r.get("title") or "", r.get("summary") or ""
        cat = kind_map.get(r.get("kind")) or infer_category(url, title, "")
        if r.get("official") and normalize_url(url) in HOSTED_KEEP: cat = CAT_HOSTED
        add(entries, url, title, desc, cat, source)


def parse_beatapi_json(path, entries):
    data = json.loads(path.read_text()); source = "BeatAPI/awesome-jev"
    cat_map = {
        "browser-computer-use":CAT_USE,"sdk-integrations":CAT_SDKS,"routing-optimization":CAT_USE,
        "open-models":CAT_OS,"search-data":CAT_USE,"safety-review":CAT_USE,
        "agent-workflows":CAT_USE,"interfaces":CAT_USE,"developer-tools":CAT_SDKS,"domain-tools":CAT_USE,
    }
    for r in data.get("projects", []):
        url = r.get("repoUrl") or ""
        title = r.get("name") or ""
        sm = r.get("summary") or {}
        desc = sm.get("en") if isinstance(sm, dict) else (sm or "")
        cat = cat_map.get(r.get("category"), None) or infer_category(url, title, r.get("category") or "")
        add(entries, url, title, desc, cat, source)
        # also capture non-github homepage if present
        for k in ("websiteUrl", "demoUrl", "hfUrl", "modelUrl"):
            u = r.get(k)
            if u: add(entries, u, title, desc, cat, source)

def parse_alternatives_html(path, entries):
    text = path.read_text(encoding="utf-8", errors="replace"); source = "systemonemodels.org/examples/alternatives"
    for m in re.finditer(r'href="(https://github\.com/[^"#?\s]+)"[^>]*>([^<]*)<', text):
        add(entries, m.group(1), m.group(2).strip() or m.group(1).rstrip("/").split("/")[-1], "", CAT_OS, source)
    for m in re.finditer(r'href="(https://huggingface\.co/[^"#?\s]+)"', text):
        url = m.group(1); add(entries, url, url.rstrip("/").split("/")[-1], "", CAT_OS, source)
    for m in re.finditer(r'href="(https://[^"#?\s]+)"[^>]*>', text):
        url = m.group(1)
        if "github.com" in url or "huggingface.co" in url: continue
        if any(x in url for x in ("simplejev.ai", "laya.convai", "systemonemodels")):
            add(entries, url, urlparse(url).netloc, "", CAT_OS, source)

SEEDS = [
("https://typesafe.ai","TypeSafe AI","Product site for TypeSafe System One models and Jev.","Docs & essays","seed-official"),
("https://docs.typesafe.ai","Documentation","TypeSafe docs home — what Jev is and how System One differs from text generation.","Hosted: TypeSafe Jev","seed-official"),
("https://docs.typesafe.ai/concepts/system-one","System One concept","Author definition of System One models and the typed-decision interface.","Docs & essays","seed-official"),
("https://docs.typesafe.ai/introduction","Introduction","What Jev is and how System One differs from text-generation models.","Docs & essays","seed-official"),
("https://docs.typesafe.ai/introduction/quickstart","Quickstart","Shortest path from an API key to a typed decision.","Docs & essays","seed-official"),
("https://docs.typesafe.ai/primitives","Primitives","Choice, Score, and Noul: result shapes and when to use each.","Hosted: TypeSafe Jev","seed-official"),
("https://docs.typesafe.ai/api","HTTP API reference","Request/response contract for POST /v1/systemone.","Hosted: TypeSafe Jev","seed-official"),
("https://docs.typesafe.ai/confidence","Confidence","How confidence differs from answer probability as an architectural control.","Docs & essays","seed-official"),
("https://docs.typesafe.ai/patterns","Patterns","Confidence-gated routing, composite scoring, speculative fan-out, intent routing.","Use cases","seed-official"),
("https://docs.typesafe.ai/demos","Interactive demos","TypeSafe hands-on examples including the smart-home assistant.","Use cases","seed-official"),
("https://console.typesafe.ai","TypeSafe Console","Create keys and inspect live Jev requests.","SDKs & tooling","seed-official"),
("https://evals.typesafe.ai","Workflow evals","TypeSafe published workflows, model comparisons, and methodology.","Evals & papers","seed-official"),
("https://typesafe.ai/blog/introducing-system-one-models-and-jev","Introducing System One Models & Jev","Launch post naming the category, thesis, results, and limitations.","Docs & essays","seed-official"),
("https://typesafe.ai/manifesto","Manifesto","Case for machine-native intelligence built for software rather than conversation.","Docs & essays","seed-official"),
("https://typesafe.ai/blog/bitterest-lesson","The Bitterest Lesson","Why optimizing the wrong task can dominate gains from scale.","Docs & essays","seed-official"),
("https://typesafe.ai/blog/ai-too-good-to-be-true-too-bad-to-be-useful-typesafe-ai","AI: too good to be true, too bad to be useful","Argument for moving beyond preference-optimized chat models in automation.","Docs & essays","seed-official"),
("https://github.com/typesafe-ai/typesafe-sdk-js","JavaScript SDK","Official JS/TS client with inferred answer types.","SDKs & tooling","seed-official"),
("https://github.com/typesafe-ai/typesafe-sdk-python","Python SDK","Official sync/async Python client.","SDKs & tooling","seed-official"),
("https://github.com/typesafe-ai/system-one-adapter-python","System One Adapter","Drop-in Python adapter for OpenAI/Anthropic-compatible LLMs behind the typed interface.","SDKs & tooling","seed-official"),
("https://github.com/typesafe-ai/skills","TypeSafe Agent Skills","Official agent skill for designing TypeSafe workflows.","SDKs & tooling","seed-official"),
("https://github.com/typesafe-ai","TypeSafe GitHub org","Source repositories maintained by TypeSafe.","SDKs & tooling","seed-official"),
("https://discord.gg/typesafe","TypeSafe Discord","Official community server.","Community","seed-official"),
("https://x.com/typesafeai","TypeSafe on X","Product and research updates.","Community","seed-official"),
("https://www.linkedin.com/company/typesafe-ai","TypeSafe on LinkedIn","Company announcements and hiring.","Community","seed-official"),
("https://vercel.com/ai-gateway/models/jev","Vercel AI Gateway — Jev","Hosted gateway entry for calling Jev through Vercel AI SDK.","SDKs & tooling","seed-official"),
("https://archerhume.com/posts/jevs-architecture-unmasked","Jev’s Architecture Unmasked","Archer Hume: architecture probe from ~10k API calls — shared state, isolated questions, parallel readouts.","Docs & essays","seed-essays"),
("https://lilting.ch/en/articles/typesafe-ai-jev-system-one-model","TypeSafe Jev vs LLMs and MDLM","lilting.ch architecture comparison: parallel sampler vs autoregressive and diffusion LMs.","Docs & essays","seed-essays"),
("https://www.latent.space/p/ainews-jev-a-system-one-model-that","Latent.Space AINews: Jev launch roundup","Community roundup of the System One / Jev launch and early reactions.","Docs & essays","seed-essays"),
("https://www.latent.space/p/jev","Latent.Space interview: Diogo Almeida","Interview on System One models for production, not AGI chat.","Docs & essays","seed-essays"),
("https://www.latent.space/p/ainews-here-are-6-clones-of-jev-in","Latent.Space: 6 clones of Jev in 2 days","Roundup of early open reproductions (Nimble, Kev, and others).","Docs & essays","seed-essays"),
("https://navinpai.github.io/decoding-jev","Decoding Jev","Independent walkthrough of architecture, inference, and RLCD evidence status.","Docs & essays","seed-essays"),
("https://learnjev.com/concepts/rlcd","RLCD: how Jev is trained","Learn Jev primer on what is and is not public about RLCD.","Docs & essays","seed-essays"),
("https://www.langchain.com/blog/building-a-harness-with-jev","Building a Harness with Jev","LangChain walkthrough of wiring a decision model into an agent harness.","Docs & essays","seed-essays"),
("https://systemonemodels.org/examples/alternatives","Jev alternatives index","Living index of open reproductions, classifiers, and structured-output libraries.","Awesome lists & indexes","seed-essays"),
("https://systemonemodels.org","System One Models","Independent living documentation site for the System One category.","Docs & essays","seed-essays"),
("https://warmersun.com/jev","Typed Decisions, Not Chat","Independent technical walkthrough distinguishing claims from public evidence.","Docs & essays","seed-essays"),
("https://www.kevnu.com/en/posts/typesafe-jev-technical-deconstruction-non-autoregressive-decision-primitives-rlcd-and-local-open-source-implementation","TypeSafe Jev technical deconstruction","Non-autoregressive primitives, RLCD, and local open-source implementations.","Docs & essays","seed-essays"),
("https://arxiv.org/abs/1706.04599","On Calibration of Modern Neural Networks","Guo et al. 2017 — temperature scaling and ECE foundations.","Evals & papers","seed-essays"),
("https://github.com/NandhaKishorM/laya","Laya","Convai Innovations decision head on ModernBERT/mmBERT; Choice/Score/Noul; ECE 0.081 after temperature fit; Apache-2.0.","Open models & alternatives","seed-tier"),
("https://laya.convaiinnovations.com","Laya (site)","Project site for the open Laya typed-decision engine.","Open models & alternatives","seed-tier"),
("https://github.com/TianyuCodings/NanoJev","NanoJev","0.6B from-scratch replica with weights, dataset, and training pipeline; Maze/Snake/ViZDoom demos.","Open models & alternatives","seed-tier"),
("https://github.com/TheoLeeCJ/SemIf","SemIf (formerly openjev)","Frozen-model logit reader for typed Choice on open models (e.g. Qwen3.5-4B); MIT.","Open models & alternatives","seed-tier"),
("https://github.com/jaredpalmer/kev","Kev","Trainable Jev-like family on Qwen3.5 (0.8B/4B/9B) with System One-compatible server.","Open models & alternatives","seed-tier"),
("https://github.com/vinnylarouge/jevlike","jevlike","Trained-from-scratch byte-embedding + option-attention decision model; MIT; CPU/Apple/CUDA.","Open models & alternatives","seed-tier"),
("https://github.com/ekzhang/openjev-sglang","openjev-sglang","Prefill-only server implementing TypeSafe wire format on Qwen3.6-35B-A3B via SGLang.","Open models & alternatives","seed-tier"),
("https://github.com/Mapika/decider","Decider","Fine-tuned Qwen3.5-2B System One reproduction serving POST /v1/systemone.","Open models & alternatives","seed-tier"),
("https://github.com/mizorewww/laya-mlx","laya-mlx","Native Apple Silicon MLX runtime for open Laya typed decisions.","Open models & alternatives","seed-tier"),
("https://github.com/bnsd55/jevmlx","jevmlx","Parallel constrained decisions for any MLX model on Apple Silicon; schema-valid JSON.","Open models & alternatives","seed-tier"),
("https://github.com/r-ms/mini-jev","mini-jev","Frozen Qwen3-4B next-token logit interface for Choice/Noul; not a full reproduction.","Open models & alternatives","seed-tier"),
("https://github.com/rorshopping/jev-on-a-laptop","jev-on-a-laptop","Study of parallel constrained decoding on stock 1.5B–8B models on Apple Silicon.","Open models & alternatives","seed-tier"),
("https://github.com/deepanwadhwa/OpenDecision","OpenDecision","Zero-shot NLI decision engine on ModernBERT-large (~400M) with Choice/Noul/Score vocabulary.","Open models & alternatives","seed-tier"),
("https://github.com/hr98w/jev-visual","jev-visual","Educational multimodal Jev-like inference on Apple Silicon (MLX) with browser UI and demos.","Open models & alternatives","seed-tier"),
("https://github.com/kshetrajna12/reflex","reflex","Open re-creation on Qwen3.5-4B: state + fixed-option questions → probability per option.","Open models & alternatives","seed-tier"),
("https://github.com/Heman10x-NGU/openJev-verdict-2.0","openJev-verdict-2.0","151M non-autoregressive decision model with LocalLLaMA typed-decisions benchmark numbers.","Open models & alternatives","seed-tier"),
("https://github.com/Heman10x-NGU/Verdict-open-jev","Verdict-open-jev","151M ModernBERT decision model with WebGPU playground and Jev audit.","Open models & alternatives","seed-tier"),
("https://github.com/SiliconLabAI/OpenJev","OpenJev (SiliconLabAI)","Decision engine scoring options via any OpenAI-compatible provider.","Open models & alternatives","seed-tier"),
("https://github.com/featherless-ai/simple-jev","simple-jev","Turns any open HF model into a typed classifier / Jev-style decision endpoint.","Open models & alternatives","seed-tier"),
("https://github.com/rupeshpoojary9/poorjev","poorjev","Local System One layer on commodity NLI models with temperature scaling and conformal abstention.","Open models & alternatives","seed-tier"),
("https://github.com/wfzyx/von","Von","Open local Choice/Noul/Score model with public weights and System One-shaped API.","Open models & alternatives","seed-tier"),
("https://github.com/ikermoel/open-alternative-jev","open-alternative-jev","One-pass option-token probabilities from open models via Transformers/vLLM + temperature scaling.","Open models & alternatives","seed-tier"),
("https://github.com/zhengxuyu/litjev","litjev","Independent Qwen reproduction serving /v1/systemone with Choice/Score/Noul + MMLU-Pro.","Open models & alternatives","seed-tier"),
("https://github.com/kikoncuo/jevfire","jevfire","Parallel typed decisions for CUDA LLMs via vLLM shared-prefix batching.","Open models & alternatives","seed-tier"),
("https://github.com/abhishek085/open-spark-jev","open-spark-jev","Local decision models on Qwen3 sized for NVIDIA DGX Spark.","Open models & alternatives","seed-tier"),
("https://github.com/NullPo-jp/PocketJev","PocketJev","SwiftUI on-device multiple-choice tool reading next-token logits on iPhone.","Open models & alternatives","seed-tier"),
("https://github.com/iapp-technology/openthai-systemone","OpenThai-SystemOne","Open Thai/English System One decision model (0.8B, 256-way slot head); Apache-2.0.","Open models & alternatives","seed-tier"),
("https://github.com/logan-markewich/jeff","jeff","Self-hosted GLiFormer 400M server for Choice/Score/Noul via Jev-compatible API.","Open models & alternatives","seed-tier"),
("https://github.com/scienthoon/luce","Luce","Open recipe: LLM teacher data → LoRA + decision head on Qwen3-4B-Base.","Open models & alternatives","seed-tier"),
("https://github.com/Yinsongxu/LLM2Jev","LLM2Jev","Read causal-model logits for Choice/Score/Noul via Transformers or SGLang.","Open models & alternatives","seed-tier"),
("https://github.com/daseinlabs/open-jev","open-jev (daseinlabs)","One-pass option scoring on local Gemma 3 4B with HTTP server and System One API.","Open models & alternatives","seed-tier"),
("https://simplejev.ai","Simple Jev","Hosted/open library giving HF models Jev-style structured decision output.","Open models & alternatives","seed-tier"),
("https://github.com/dottxt-ai/outlines","Outlines","Structured generation constraining LLMs to grammar/JSON schema.","SDKs & tooling","seed-tier"),
("https://github.com/567-labs/instructor","Instructor","Pydantic structured outputs from LLMs with validation and retries.","SDKs & tooling","seed-tier"),
("https://github.com/stanfordnlp/dspy","DSPy","Programming (not prompting) LMs with typed Signatures — closest open typed-question analogue.","SDKs & tooling","seed-tier"),
("https://github.com/trycua/cua","cua","Cua computer-use stack; includes System-1-style decision models distinct from TypeSafe Jev.","Open models & alternatives","seed-tier"),
("https://github.com/AnswerDotAI/ModernBERT","ModernBERT","Modernized BERT encoder — baseline backbone for many open decision heads.","Open models & alternatives","seed-tier"),
("https://github.com/urchade/GLiNER","GLiNER","Zero-shot NER with labels at inference time — extraction-shaped cousin of typed decisions.","Open models & alternatives","seed-tier"),
("https://github.com/huggingface/setfit","SetFit","Few-shot Sentence Transformer classification without prompting.","Open models & alternatives","seed-tier"),
("https://github.com/kuleshov-group/mdlm","MDLM","NeurIPS 2024 masked diffusion LMs — open non-autoregressive research line often compared to Jev.","Evals & papers","seed-tier"),
("https://github.com/fstandhartinger/jevbench","JevBench (text decisions)","Independent cross-model benchmark for typed decisions (accuracy, calibration, latency, cost).","Evals & papers","seed-tier"),
("https://jevbench.dev","JevBench","Interactive harness bench for Jev, open alternatives, and dual-brain (LLM + decision model) setups — starting with StarCraft II — measuring win/loss, task completion, and latency rather than a single typed-answer score.","Evals & papers","seed-tier"),
("https://jevals.com","Jevals.com","Independent hosted-Jev vs LLM benchmark with public methodology and per-decision logs.","Evals & papers","seed-tier"),
("https://github.com/AbdelStark/awesome-typesafe-jev","Awesome TypeSafe Jev","Large community field guide to Jev projects, SDKs, evals, and demos.","Awesome lists & indexes","seed-lists"),
("https://github.com/logicrw/awesome-jev-projects","Awesome Jev Projects","Commit-pinned radar of 688 curated Jev projects across 17 domains (live site + projects.json).","Awesome lists & indexes","seed-lists"),
("https://github.com/OmniJev/awesome-jev-gallery","Awesome Jev Gallery","Gallery-style curated Jev / System One projects.","Awesome lists & indexes","seed-lists"),
("https://github.com/AppitStudio/awesome-jev","Awesome Jev (AppitStudio)","Curated awesome list of Jev ecosystem links.","Awesome lists & indexes","seed-lists"),
("https://github.com/BeatAPI/awesome-jev","Awesome Jev (BeatAPI)","Curated awesome list of Jev ecosystem links.","Awesome lists & indexes","seed-lists"),
("https://github.com/rupeshpoojary9/awesome-open-system-one","Awesome Open System One","Open-only System One models, benchmarks, calibration, and constrained decoding.","Awesome lists & indexes","seed-lists"),
("https://github.com/kydlikebtc/awesome-jev","Awesome Jev (kydlikebtc)","Catalog-driven bilingual awesome list with link checks.","Awesome lists & indexes","seed-lists"),
("https://github.com/MrJev/awesome-jev","Awesome Jev (MrJev)","Curated awesome list of Jev ecosystem links.","Awesome lists & indexes","seed-lists"),
("https://abdelstark.github.io/awesome-typesafe-jev","Awesome TypeSafe Jev (live site)","Browsable live directory for the AbdelStark list.","Awesome lists & indexes","seed-lists"),
("https://logicrw.github.io/awesome-jev-projects/en","Awesome Jev Projects (live site)","Searchable English radar UI for logicrw listings.","Awesome lists & indexes","seed-lists"),
("https://logicrw.github.io/awesome-jev-projects","Awesome Jev Projects (site root)","Radar home (lang query stripped on normalize); English UI also at /en.","Awesome lists & indexes","seed-lists"),
("https://typesafeai.app","typesafeai.app","Independent directory of public Jev capabilities with evidence levels.","Awesome lists & indexes","seed-lists"),
("https://huggingface.co/akhilaaa3/Jev-Omni","Jev-Omni","Multimodal open System One classifier (text/image/audio/video) on Gemma 4 12B; Apache-2.0; author reports JevBench parity and <100ms on H100.","Open models & alternatives","seed-tier"),
("https://huggingface.co/datasets/akhilaaa3/decision-bench","DecisionBench","Public typed-decision eval set used with Jev-Omni (scenarios → questions with option probabilities).","Evals & papers","seed-tier"),
("https://x.com/Akhila_988/status/2102171891410825520","Jev-Omni launch thread","Announcement of Jev-Omni as a multimodal open System One model with HF weights.","Docs & essays","seed-essays"),
("https://github.com/mizorewww/laya-coreml","laya-coreml","Local Laya typed decisions on Apple Core ML / Neural Engine; ~5 ms short decisions on M3 Max.","Open models & alternatives","seed-tier"),
("https://github.com/GodModeAI2025/JevCoreML","JevCoreML","Native macOS Core ML decision stack for kev-0.6b and Laya without Python or cloud at runtime.","Open models & alternatives","seed-tier"),
("https://github.com/FluidInference/FluidUse","FluidUse","Local computer use on Apple silicon using Laya + CUA-S1-FORMS via Accessibility API.","Open models & alternatives","seed-tier"),
("https://github.com/bespokelabsai/nimble","Bespoke Nimble","Open Jev recipe: Qwen3.5-9B LoRA on contrastive data with public eval suite vs Jev 1.13.","Open models & alternatives","seed-tier"),
("https://github.com/Zefan-Cai/Open-Jev","Open-Jev (ZefanCai)","Qwen3.5-2B/9B LoRA adapters with scalar decision heads and public dataset.","Open models & alternatives","seed-tier"),
("https://github.com/PsiACE/dohnuts","Dohnuts","0.8B text+image decision model; authors report 65.8% on 231 public JevBench tasks.","Open models & alternatives","seed-tier"),
("https://github.com/nico-martin/open-jev","open-jev (browser)","Browser TypeScript runtime for Kev/DeBERTa decisions via Transformers.js (WebGPU/WASM).","Open models & alternatives","seed-tier"),
("https://github.com/ipenywis/laya-ultrafast","Laya Ultrafast","Local MLX port of Jev Ultrafast with narrow-decision policy for browser tasks.","Open models & alternatives","seed-tier"),
("https://beatapi.io/awesome-jev","BeatAPI Awesome JEV gallery","Live gallery UI for the BeatAPI curated ≥50-star JEV project catalogue.","Awesome lists & indexes","seed-lists"),
("https://x.com/thekitze/status/2102775497822503298","kitze thread: Kev / OpenJev / Laya","Community post threading open System One clones (Kev, OpenJev, Laya) and related serving work.","Docs & essays","seed-essays"),
("https://github.com/jaredpalmer/kev/releases/tag/kev-family","Kev family release","Packaged Kev-0.8B / 4B / 9B adapters + heads on Qwen3.5 with locked-test numbers and checksums.","Open models & alternatives","seed-tier"),
("https://github.com/razorback16/openjev","OpenJev","Apache-licensed System One decision server on DiffusionGemma 26B (vLLM NVIDIA + MLX Apple); Choice/Score/Noul, optional images.","Open models & alternatives","seed-tier"),
("https://huggingface.co/openjev/openjev","OpenJev (weights)","HF decision-model checkpoint for OpenJev; zero-shot classification / calibrated option probabilities; CC-BY-NC-4.0.","Open models & alternatives","seed-tier"),
("https://github.com/receptron/laya","Laya Node Runtime","Node.js / TypeScript ONNX Runtime for open Laya typed decisions.","Open models & alternatives","seed-tier"),
("https://github.com/wnzn/semif-go","semif-go","Go System One adapter over llama.cpp: Choice/Noul/Score from next-token option probs; multimodal state (text/image/audio/video).","Open models & alternatives","seed-tier"),
("https://github.com/vllm-project/vllm/pull/57250","vLLM PR #57250 — DiffusionGemma structured mode","Prototype structured-generation / Jev-like canvas read for DiffusionGemma with sample /v1/systemone interposer.","Open models & alternatives","seed-tier"),
("https://blog.google/innovation-and-ai/technology/developers-tools/diffusion-gemma-faster-text-generation/","Introducing DiffusionGemma","Google blog on DiffusionGemma — faster non-autoregressive text generation used by open System One servers.","Docs & essays","seed-essays"),
("https://x.com/togethercompute/status/2102882216950763814","Together AI: Tev1-4B-experimental","Announcement of Tev1 — Jev-like classifier on Qwen3.5 4B, serverless pricing, data recipe, and train-your-own tutorial.","Docs & essays","seed-essays"),
("https://github.com/togethercomputer/tev1","tev1","Together AI open recipe + training example for Tev1-4B-experimental (Jev-inspired decision LoRA on Qwen3.5-4B).","Open models & alternatives","seed-tier"),
("https://huggingface.co/togethercomputer/Tev1-4B-experimental","Tev1-4B-experimental","Open-weight Jev-inspired decision model finetuned from Qwen3.5-4B; Together serverless + HF weights.","Open models & alternatives","seed-tier"),
("https://www.together.ai/blog/how-to-train-your-own-jev","How to train your own Jev","Together tutorial / data recipe for fine-tuning a decision classifier (~$17 Tev1 training cost claimed).","Docs & essays","seed-essays"),
("https://api.together.ai/models/together/Tev1-4B-experimental","Tev1 on Together serverless","Hosted Tev1-4B-experimental endpoint on Together AI ($0.042/M input, $0/M output per announcement).","Open models & alternatives","seed-tier"),
# --- logicrw 2026-09-24 refresh + Reddit credit (seed-logicrw-refresh) ---
# 174 missing evidenced projects from logicrw projects.json (excl. mega-host adapters)
('https://www.reddit.com/r/LLMDevs/comments/1wko2e5/i_reviewed_287_opensource_jev_projects_here_are','Reddit: 287 open-source Jev projects (top 20)','r/LLMDevs roundup of 287 reviewed OSS Jev projects with 20 recommended starters (browser, compaction, MCP, games, finance).','Docs & essays',"seed-lists"),
('https://github.com/alpha-tales/alphaoptimizer','alphaoptimizer','AlphaOptimizer is an open-source tool from AlphaTales that helps Codex work with large command and tool outputs. Instead of sending a huge log or search result straight into the context window, AlphaOptimizer keeps…','SDKs & tooling',"seed-logicrw-refresh"),
('https://github.com/ReallyArtificial/jev-by-example','jev-by-example','Ten runnable Jev examples for agent decisions: memory conflicts, tool-result checks, recovery, context selection, and handoffs. JavaScript, zero dependencies.','SDKs & tooling',"seed-logicrw-refresh"),
('https://github.com/ReallyArtificial/stuntdouble','stuntdouble','Drop-in /v1/systemone proxy that shadows Jev with local decision models (Kev, Laya) and reports whether you can swap','Open models & alternatives',"seed-logicrw-refresh"),
('https://github.com/bytelabs-oss/clash-jev','clash-jev','A Clash Royale bot with no trained policy: Jev (TypeSafe System One) makes every decision from the live game state','Use cases',"seed-logicrw-refresh"),
('https://github.com/csskrtao/jev-to-answer','jev-to-answer','Jev returns a structured decision for the local program; consult the source for the exact decision policy.','SDKs & tooling',"seed-logicrw-refresh"),
('https://github.com/yushen100/wechat-jev-assistant','wechat-jev-assistant','Jev returns a structured decision for the local program; consult the source for the exact decision policy.','Use cases',"seed-logicrw-refresh"),
('https://github.com/muratcakmak/jev-guard','jev-guard',"Probability-scored guardrails for Claude Code: deny rule-breaking edits and unasked-for deploys, route your docs into each prompt, and check the final answer against the turn's own evidence.",'Use cases',"seed-logicrw-refresh"),
('https://github.com/0x7067/claude-jev','claude-jev','Claude Code plugin: Jev for rule checks, verbatim compaction, and prompt routing','Use cases',"seed-logicrw-refresh"),
('https://github.com/idovmamane/dejevu','dejevu','Jev? Déjà vu. Browser agents that run on instinct, no Jev needed. One look at the page, one call to any open model, one action. Faster than the Jev demo on Google Flights.','Use cases',"seed-logicrw-refresh"),
('https://github.com/ZephyrDeng/ego-jev','ego-jev','Jev (TypeSafe System One) inner loop for ego-browser — one ~0.4s typed decision per DOM step instead of an LLM turn. Agent skill for ego lite.','SDKs & tooling',"seed-logicrw-refresh"),
('https://github.com/Tongyun1/Jev-in-the-Loop','Jev-in-the-Loop','Researching how Jev can accelerate tasks that rely on LLM decision-making.','Use cases',"seed-logicrw-refresh"),
('https://github.com/Aimark-dai/jev-chat-windows-deepseek-jev','jev-chat-windows-deepseek-jev','Jev returns a structured decision for the local program; consult the source for the exact decision policy.','Use cases',"seed-logicrw-refresh"),
('https://github.com/jiayylu/jev-as-quant','jev-as-quant','Typed System-1 decisions (Laya/Jev) as the judgment layer of a quant research stack, with Claude as System 2. Requirements → design → code → experiments.','SDKs & tooling',"seed-logicrw-refresh"),
('https://github.com/waynesutton/ask-jev-ai','ask-jev-ai','Most AI demos generate text. Jev does not. It reads a sentence and returns typed answers with probabilities: a choice, a yes or no, a score. That makes it usable as a primitive inside ordinary code rather than a…','SDKs & tooling',"seed-logicrw-refresh"),
('https://github.com/davertor/jev-slop-guard','jev-slop-guard','Jev Slop Guard — a Chrome extension that scores and stamps AI slop on your X and LinkedIn feeds as you scroll','Use cases',"seed-logicrw-refresh"),
('https://github.com/vercel-labs/jev-ai-sdk-form-router','jev-ai-sdk-form-router','Route form submissions to the right people with Jev and AI SDK.','SDKs & tooling',"seed-logicrw-refresh"),
('https://github.com/hosseintoussi/jev-flappy-bird','jev-flappy-bird',"A live demo of TypeSafe's Jev model playing Flappy Bird, one flap-or-wait decision at a time.",'Use cases',"seed-logicrw-refresh"),
('https://github.com/jimmyliao/jev-storyboard-lab','jev-storyboard-lab',"(`agent_framework.foundry.FoundryChatClient` is a different client this repo doesn't use — its `credential` parameter only accepts Azure AD token credentials, not an API key. If you only have a key-based Azure OpenAI…",'Use cases',"seed-logicrw-refresh"),
('https://github.com/455-dIAO/jev-codex-router-skill','jev-codex-router-skill','Portable Codex Skill for Jev model and reasoning-effort routing, with safe installation and Chinese usage guides','Use cases',"seed-logicrw-refresh"),
('https://github.com/juanlentino/jev-connector','jev-connector','WordPress connector for the TypeSafe System One API (Jev): typed questions, confidence-scored answers, core Connectors API key management','Use cases',"seed-logicrw-refresh"),
('https://github.com/xianggelila177/VideoAdGuard-Jev','VideoAdGuard-Jev','Jev returns a structured decision for the local program; consult the source for the exact decision policy.','SDKs & tooling',"seed-logicrw-refresh"),
('https://github.com/dr-dimitru/claude-jev-plugin','claude-jev-plugin','TypeSafe Jev semantic guardrails for Claude Code','Use cases',"seed-logicrw-refresh"),
('https://github.com/shikaizhong-design/ego-jev-ultrafast','ego-jev-ultrafast','Jev drives your Ego Lite browser: one typed-choice request per step. Single-file, zero-dependency port of browser-use/jev-ultrafast with multi-model benchmarks and extra guardrails. Unofficial.','Use cases',"seed-logicrw-refresh"),
('https://github.com/himomohi/jev-skill-router','jev-skill-router','Keep skill catalogs outside the main LLM context. Jev selects relevant skills through one read-only MCP tool.','SDKs & tooling',"seed-logicrw-refresh"),
('https://github.com/liaoyuhua/jev-trip','jev-trip','Jev Trip is an explainable day-trip planner. The LLM plans ahead; Jev chooses and checks. Deterministic code handles route facts, time calculations, validation, and versioning.','Use cases',"seed-logicrw-refresh"),
('https://github.com/rxova/jev-planner','jev-planner','With **N** agents, `--mode ultra` makes **2N + 1** agent calls: drafts, reviews, and final synthesis, plus **N** if Jev requests another review. The default `balanced` makes as few as **N + 1** and never more than…','SDKs & tooling',"seed-logicrw-refresh"),
('https://github.com/wuxie888/jev-yaba-wechat','jev-yaba-wechat','Jev returns a structured decision for the local program; consult the source for the exact decision policy.','SDKs & tooling',"seed-logicrw-refresh"),
('https://github.com/kenhuangus/jev-usecases','jev-usecases','Production TypeSafe Jev (System One) use-case harnesses with confidence-gated decision logic','Docs & essays',"seed-logicrw-refresh"),
('https://github.com/nssmd/jev-bot','jev-bot','Self-hosted Jev decision workbench and Feishu bot: automatic choices, probabilities, and experimental word/character writing.','Use cases',"seed-logicrw-refresh"),
('https://github.com/moisesfilho/typesafe-jev-opencode','typesafe-jev-opencode','Jev is not a conversational replacement for Gemini, Claude, or GPT. It evaluates application state against typed questions and returns structured answers and probabilities that an agent can use to route or gate work.','SDKs & tooling',"seed-logicrw-refresh"),
('https://github.com/Ramneet-Singh/jevopt','jevopt','Making intelligent compiler optimisation decisions with Jev','SDKs & tooling',"seed-logicrw-refresh"),
('https://github.com/ZJemYoung/jev-chat-windows-laya','jev-chat-windows-laya','Jev returns a structured decision for the local program; consult the source for the exact decision policy.','Use cases',"seed-logicrw-refresh"),
('https://github.com/jjd-lab/jev-synthetic-survey','jev-synthetic-survey','New to synthetic survey respondents? [Start here](#new-to-this-start-here). For the raw runs, the scored reports and the code, see [where to go](#where-to-go).','Use cases',"seed-logicrw-refresh"),
('https://github.com/nekowasabi/jev-routing','jev-routing','Go Jev harness for Claude Code, Codex, and Grok Build. No npx. Not an MCP server.','SDKs & tooling',"seed-logicrw-refresh"),
('https://github.com/Arpit-Khandelwal/jev-linkedin-slop-filter','jev-linkedin-slop-filter','Judges every LinkedIn post as it scrolls into view and slams a rubber stamp on it — **BAIT**, **CORP**, or **BRAG** — with the confidence score printed on the stamp. The post stays readable underneath.','SDKs & tooling',"seed-logicrw-refresh"),
('https://github.com/ItisNoMatter/kojev','kojev','Kotlin Multiplatform client for Jev that returns your own enum/sealed types instead of string keys.','Use cases',"seed-logicrw-refresh"),
('https://github.com/proshunsuke/jev-tab-order','jev-tab-order','**Organize the entire window with a single Jev API request.** Grouping and ordering decisions are evaluated together, regardless of the number of tabs.','SDKs & tooling',"seed-logicrw-refresh"),
('https://github.com/Cairn-ink/cairn-jev-lab','cairn-jev-lab','Use it to test a memory policy before letting it decide what an agent keeps. The lab includes editable cases, a reusable JavaScript entry point, and reports that retain both successful judgments and mistakes. Node.js…','Use cases',"seed-logicrw-refresh"),
('https://github.com/chy4pro/jev-in-mcp','jev-in-mcp','MCP relay that adds use_jev to every server: Jev picks the tool calls, the calling model writes the values Jev cannot choose, the relay executes. Built on jev-dev-kit.','SDKs & tooling',"seed-logicrw-refresh"),
('https://github.com/AppChainAI/Jevatar','Jevatar','Jev returns a structured decision for the local program; consult the source for the exact decision policy.','Use cases',"seed-logicrw-refresh"),
('https://github.com/RileyCarney/JevTools','JevTools','A toolkit, knowledge base, web cockpit, and reference implementation for building AI applications with **Jev (TypeSafe System One)** via **OpenRouter Alpha Decisions** and **TypeSafe Direct API**.','Use cases',"seed-logicrw-refresh"),
('https://github.com/ChenYCL/jev-browser-skill','jev-browser-skill','Browser use & computer use for coding agents, powered by TypeSafe Jev: calibrated judgments from a System One model, control loop in code. ego lite / Chrome / Safari · CLI + MCP','Use cases',"seed-logicrw-refresh"),
('https://github.com/paramjeetn/jev-cookbook','jev-cookbook',"The complete cookbook for Jev by TypeSafe AI — 120+ use cases, 10 runnable examples, 4 composition patterns, and first-principles theory for the world's first System One AI model.",'Docs & essays',"seed-logicrw-refresh"),
('https://github.com/gualican/jev-model-router','jev-model-router',"Routes prompts to the right Claude tier (Haiku/Sonnet/Opus) using TypeSafe's Jev model",'SDKs & tooling',"seed-logicrw-refresh"),
('https://github.com/gavansmyth-arch/jev-chrome-extension','jev-chrome-extension','1. Open any website. 2. Click the Jev icon. The side panel opens on **Drive**. 3. Type a goal, e.g. *Search Wikipedia for "espresso" and open the article*, and press **Run**.','Use cases',"seed-logicrw-refresh"),
('https://github.com/kyle-chalmers/typesafe-jev-incident-router','typesafe-jev-incident-router','Confidence-gated incident routing with TypeSafe Jev','SDKs & tooling',"seed-logicrw-refresh"),
('https://github.com/Pasblinn/jev-lab','jev-lab','Open lab: Jev (TypeSafe System One) routing in front of Claude Code - measured bugs, patch, and a hard fallback with alerts','Use cases',"seed-logicrw-refresh"),
('https://github.com/harrymunro/jev-laya-benchmark','jev-laya-benchmark',"Speed and accuracy benchmark: TypeSafe's Jev API vs the local Laya MLX typed-decision model on synthetic tasks",'Evals & papers',"seed-logicrw-refresh"),
('https://github.com/clduab11/jev-test','jev-test','Pre-registered benchmark: can a 2B local model (Gemma 4 E2B) answer web questions without making things up when a decision model (TypeSafe Jev) makes every call? SearXNG for search, MemPalace for verbatim memory,…','Use cases',"seed-logicrw-refresh"),
('https://github.com/sathariels/jevcheck','jevcheck','Probabilities and model versions move. A raw `0.94` is not a release decision. jevcheck records a **production contract** (baseline model + fixtures + expected answers) and evals a candidate against that fixture.','SDKs & tooling',"seed-logicrw-refresh"),
('https://github.com/dtheofr/typesafe-jev-ruby','typesafe-jev-ruby',"Ruby client for Jev, TypeSafe's System One model: typed questions, probabilistic answers. Zero runtime dependencies.",'Use cases',"seed-logicrw-refresh"),
('https://github.com/Kaos599/jev-writer','jev-writer','Unlike generative writing assistants that flatter drafts, jev-writer enforces strict statistical safeguards: an observational power gate, date-confound controls, and Benjamini-Hochberg false-discovery corrections. It…','Use cases',"seed-logicrw-refresh"),
('https://github.com/onlyjq04/jev-agent-hooks','jev-agent-hooks','TypeSafe Jev hooks for Claude Code, Codex and pi: per-turn skill suggestion and subagent model routing','Use cases',"seed-logicrw-refresh"),
('https://github.com/WanLanglin/jev-skills','jev-skills',"Claude Code & Codex skills powered by Jev, TypeSafe's System One model. 256 calibrated judgements for $0.0005 in 0.72s — 360x cheaper than Claude Opus 5. Includes the first published Jev calibration curve, measured…",'SDKs & tooling',"seed-logicrw-refresh"),
('https://github.com/ccai40359-wq/jev-triage','jev-triage','Millisecond-class test-failure triage for coding agents: RETRY / FIX_CODE / FIX_ENV, powered by TypeSafe Jev.','Use cases',"seed-logicrw-refresh"),
('https://github.com/ItzSupra13/jev-is-not-odd','jev-is-not-odd',"A probabilistic, AI-powered utility to determine if a number is not odd (or not even) using TypeSafe's Jev model and the Vercel AI SDK.",'SDKs & tooling',"seed-logicrw-refresh"),
('https://github.com/vizuh/sabi','sabi','Adaptive inference scheduling for AI agents — per-round model, effort and provider routing for coding harnesses: a Command Code mod or a local OpenAI-compatible proxy.','Use cases',"seed-logicrw-refresh"),
('https://github.com/pc418/jev-calculator','jev-calculator','Vars live in `wrangler.jsonc`: `JEV_BASE_URL` / `JEV_MODEL` (gateway), `TYPESAFE_BASE_URL` / `TYPESAFE_MODEL` (direct fallback), `TURNSTILE_SITEKEY`, `TURNSTILE_HOSTNAMES`, `JEV_DISABLED` (kill switch). Rate limits…','Use cases',"seed-logicrw-refresh"),
('https://github.com/Liyucheng1997/332_lab-jev-chat','332_lab-jev-chat','The Windows app reads visible WeChat chat text via UI Automation or local OCR, uses Jev for structured intent judgment, and optionally uses DeepSeek to generate three copyable reply suggestions.','Use cases',"seed-logicrw-refresh"),
('https://github.com/stas4000/jev-papers','jev-papers','1,000 arXiv AI papers classified with one Jev decision each, checked against an LLM judge. Open rebuild, MIT.','Use cases',"seed-logicrw-refresh"),
('https://github.com/Bodila51/muse-jev-playbook','muse-jev-playbook','Jev decision layer for Muse: a fast, cheap TypeSafe AI gate before expensive agent work — confidence policy, recipes, reference router, honest measurement.','Use cases',"seed-logicrw-refresh"),
('https://github.com/Waxmell114514/jev-compaction','jev-compaction',"A context compactor that can only score, never write — so an agent's memory can't hold a fact the transcript never contained. Working demo, runs offline.",'SDKs & tooling',"seed-logicrw-refresh"),
('https://github.com/codejunkie99/jev-engineering','jev-engineering','Jev Engineering: Typed Decision Systems for Reliable Agent Workflows. Paper, diagrams, and companion examples by Av1dlive.','Use cases',"seed-logicrw-refresh"),
('https://github.com/jeffonelson/jev-bigquery-cloudrun','jev-bigquery-cloudrun','Classify support tickets in BigQuery with Jev and Cloud Run','Use cases',"seed-logicrw-refresh"),
('https://github.com/ClemensSchartmueller/jev-guard','jev-guard','High-speed, cross-agent safety gate plugin for **Claude Code**, **Codex CLI**, and **Antigravity**.','Use cases',"seed-logicrw-refresh"),
('https://github.com/satviksinha/jev-model-router','jev-model-router','Model router for Claude Code using Jev','Use cases',"seed-logicrw-refresh"),
('https://github.com/garry-schuette/browser-use-with-jev','browser-use-with-jev',"**Keep Browser Use's execution engine. Move bounded decisions to Jev.**",'Use cases',"seed-logicrw-refresh"),
('https://github.com/xinwang-nwpu/jev-mobile','jev-mobile','One TypeSafe Jev decision per step over the A11Y tree, executed via ADB. No screenshots and ultra fast!','Use cases',"seed-logicrw-refresh"),
('https://github.com/colinmcdermott/emoji-jev','emoji-jev','The app sends typed text to Jev to get parallel emoji Choice, emotion Choice, Score, and Boolean results displayed as an emoji keyboard.','Use cases',"seed-logicrw-refresh"),
('https://github.com/stas4000/jev-geo-audit','jev-geo-audit','300 public pages audited for AI citability with Jev decisions, checked against an LLM judge: agreement, cost and latency, measured','Use cases',"seed-logicrw-refresh"),
('https://github.com/redreamality/jev-skill-selection','jev-skill-selection','Pre-message hook: use TypeSafe Jev to keep/drop skills and shrink agent context','SDKs & tooling',"seed-logicrw-refresh"),
('https://github.com/rmosleydb/jev-smart-router','jev-smart-router','JEV Smart Router — a Databricks App that uses TypeSafe JEV to pick which model answers each message, then runs inference on the chosen Databricks Foundation Model API endpoint.','Use cases',"seed-logicrw-refresh"),
('https://github.com/Bring-AI/jev-rl','jev-rl','JEV Reinforcement Learning: four classic games trained with JEV-powered rewards, reproducible experiments and checkpoint replays.','Use cases',"seed-logicrw-refresh"),
('https://github.com/herval/openclaw-jev-plugin','openclaw-jev-plugin','A silenced message never reaches the language model, so it costs one Jev call and no model tokens. Direct messages always get an answer unless you choose to gate them too.','Use cases',"seed-logicrw-refresh"),
('https://github.com/wotai-dev/typesafe-jev-tools','typesafe-jev-tools','A Claude Code hook that asks whether the decision you are writing needs a model at all. Includes a measured 149-row comparison of TypeSafe Jev against Claude Haiku 4.5.','SDKs & tooling',"seed-logicrw-refresh"),
('https://github.com/wanghai673/jev-browser-skill','jev-browser-skill','This Codex Skill lets Codex drive Chrome through Jev to complete multi-step browser tasks from a goal description with preset inputs.','SDKs & tooling',"seed-logicrw-refresh"),
('https://github.com/wellkilo/codex-jev-preflight','codex-jev-preflight','Fail-open Codex UserPromptSubmit hook that injects TypeSafe Jev pre-task routing metadata.','SDKs & tooling',"seed-logicrw-refresh"),
('https://github.com/ajayk/jev-go-sdk','jev-go-sdk',"Dependency-free Go client for TypeSafe AI's System One API and the Jev model",'SDKs & tooling',"seed-logicrw-refresh"),
('https://github.com/royalpinto007/jev-msw','jev-msw','Mock Jev API decisions with MSW for deterministic tests without real API calls or credits.','SDKs & tooling',"seed-logicrw-refresh"),
('https://github.com/kataras/jev','jev',"A Go client for the TypeSafe AI's System One API and its model, Jev.",'SDKs & tooling',"seed-logicrw-refresh"),
('https://github.com/trycatchkamal/typesafe-jev-traffic-demo','typesafe-jev-traffic-demo',"This is a **simulation**. It is not connected to, and cannot control, any real traffic signal — Hong Kong's Transport Department publishes no write API for that, only a read-only feed of sensor data. Everything…",'Use cases',"seed-logicrw-refresh"),
('https://github.com/jiawei686/jev-screen-mcp','jev-screen-mcp','Single-purpose MCP server (one tool, one job): a content-moderation gate powered by TypeSafe Jev (System One decision model).','SDKs & tooling',"seed-logicrw-refresh"),
('https://github.com/jiawei686/jev-review-mcp','jev-review-mcp','Single-purpose MCP server (one tool, one job): a code-review gate powered by TypeSafe Jev (System One decision model).','SDKs & tooling',"seed-logicrw-refresh"),
('https://github.com/Anson-gzy/jev-paste','jev-paste','Contextual, inline clipboard decomposition for macOS — Tab-to-paste with full history and time-decay ranking. Powered by TypeSafe JEF.','Use cases',"seed-logicrw-refresh"),
('https://github.com/AABBAASS1/jev-router','jev-router','Route any task to the right AI agent in under 1 second using Jev (TypeSafe System One). Supports Claude, ChatGPT, Cursor, and Antigravity with auto-launch on macOS, Windows, and Linux.','SDKs & tooling',"seed-logicrw-refresh"),
('https://github.com/kylemclaren/jevsearch','jevsearch',"Site search that understands the question. Ranked by TypeSafe's Jev model.",'SDKs & tooling',"seed-logicrw-refresh"),
('https://github.com/ieee0824/jev-mcp','jev-mcp','A Rust MCP server for TypeSafe AI Jev structured decisions','SDKs & tooling',"seed-logicrw-refresh"),
('https://github.com/j341nono/jev-prompt-optimization','jev-prompt-optimization','automatically optimizing the instructions and decision criteria of TypeSafe Jev Choice from labeled data','Use cases',"seed-logicrw-refresh"),
('https://github.com/neo4j-field/jev-graphrag','jev-graphrag',"Small demos + use-case backlog: TypeSafe AI's Jev as a calibrated decision layer for GraphRAG pipelines on Neo4j.",'Use cases',"seed-logicrw-refresh"),
('https://github.com/TexasOct/jev-gateway','jev-gateway','Session-aware OpenAI-compatible model-routing gateway powered by JEV','Use cases',"seed-logicrw-refresh"),
('https://github.com/shimo4228/jev-research-pipeline','jev-research-pipeline','**Code owns the loop, Jev judges, Qwen writes: a daily research monitor for standing questions.**','Use cases',"seed-logicrw-refresh"),
('https://github.com/kaustav1996/reflex','reflex','A coding agent and personal assistant built on the Pi coding agent. Jev checks every tool call, turn and voice transcript, and code decides what happens next: allow, ask or block an action, which model tier to use,…','Open models & alternatives',"seed-logicrw-refresh"),
('https://github.com/RenaGao/jev-dataops','jev-dataops','An open-source JEV-powered workbench for streaming data selection, quality evaluation, automatic LoRA training and held-out model evaluation.','Use cases',"seed-logicrw-refresh"),
('https://github.com/HexyeDEV/JevPR','JevPR','PR Risk review, automated by Jev','Use cases',"seed-logicrw-refresh"),
('https://github.com/d-date/swift-jev','swift-jev',"A Swift client for TypeSafe AI's Jev — typed judgements, not text",'SDKs & tooling',"seed-logicrw-refresh"),
('https://github.com/Eliot5566/JEV-Paper-Radar','JEV-Paper-Radar','In GitHub Actions the links point at your own repo automatically (`GITHUB_REPOSITORY`), so a fork needs no configuration. Locally, set `output.feedback_repo = "owner/name"` or run `paper-radar harvest --repo owner/name`.','Use cases',"seed-logicrw-refresh"),
('https://github.com/sumanmichael/jevlang','jevlang','The simplest way to write decision workflows in Python. Python with a smart if.','SDKs & tooling',"seed-logicrw-refresh"),
('https://github.com/NicolaiLassen/open-bonsai-jev','open-bonsai-jev',"openjev's mechanism, Bonsai's weights: typed decisions read straight from one forward pass of a 1.75-bit 27B model. Credit to TheoLeeCJ (SemIf/OpenJev) and PrismML.",'Open models & alternatives',"seed-logicrw-refresh"),
('https://github.com/kuhung/ask-jev','ask-jev','Ask Jev is a Neo-Brutalism style web app where users enter everyday dilemmas and receive direct decisions from Jev.','Use cases',"seed-logicrw-refresh"),
('https://github.com/harshithsunku/learn-jev-end-to-end','learn-jev-end-to-end','**Learn Jev end to end** is a free, hands-on course. In 12 short notebooks you go from *"what is Jev?"* to building **13 real AI tools** with it: an email triage job, a scam-text detector, a code vulnerability…','Docs & essays',"seed-logicrw-refresh"),
('https://github.com/Mrlyk/jev-browser','jev-browser',"Browser automation CLI for AI agents, powered by the Jev model's millisecond decisions and near-zero inference costs",'Use cases',"seed-logicrw-refresh"),
('https://github.com/sarathi-aiml/jevsql','jevsql','Text-to-SQL where the model never writes SQL — typed, calibrated decisions (TypeSafe Jev) + code-assembled queries','Use cases',"seed-logicrw-refresh"),
('https://github.com/jmanhype/jev-dspy-lab','jev-dspy-lab','Reproducible calibration and selective-risk benchmarks for Jev/TypeSafe decisions in DSPy workflows','Evals & papers',"seed-logicrw-refresh"),
('https://github.com/dagfinndybvig/Jev_Ontology','Jev_Ontology',"We built a working MVP that pairs an LLM-authored ontology with Jev's calibrated classification, tested it against the live Jev API on 78 unique tickets across 5 sessions (86 classifications -- Session 4 re-runs…",'Use cases',"seed-logicrw-refresh"),
('https://github.com/joshLong145/jev-cli','jev-cli','A CLI wrapper written in python for Jev','SDKs & tooling',"seed-logicrw-refresh"),
('https://github.com/Chandler-Sun/chat2jev','chat2jev','Convert OpenAI-compatible Chat Completions requests into TypeSafe System One (Jev) **State / Questions**, compare generated text with structured judgments, and publish reusable question sets as proxy routes.','Use cases',"seed-logicrw-refresh"),
('https://github.com/taman-spirit/guardrail-chatbot-jev','guardrail-chatbot-jev','It is a library, not a service. You call it, you get a verdict, and your code decides what to do. It runs in **Python and TypeScript**, both reading the same policy file, so the two sides of your stack cannot drift…','Use cases',"seed-logicrw-refresh"),
('https://github.com/kylemclaren/jevpdf','jevpdf','`server/index.ts` is a small Bun server that serves `dist/` and the `/api/jev` proxy, which uses the same forwarding code as dev (`server/jev-upstream.ts`). Because the live proxy spends real credits, it only accepts…','Use cases',"seed-logicrw-refresh"),
('https://github.com/PenglongHuang/jev-demo','jev-demo',"A zero-dependency local web demo for TypeSafe's **Jev (System One)** decision model: send a state plus typed questions, get choices, scores and calibrated probabilities back.",'Use cases',"seed-logicrw-refresh"),
('https://github.com/AndreuVM/jev-reasoning-navigator','jev-reasoning-navigator','En lugar de depender de heurísticas matemáticas frágiles o distancias vectoriales locales de coseno, `JEV-Reasoning-Navigator` utiliza **TypeSafe AI (`typesafe-sdk`)** como motor único y autoritativo de decisión…','Use cases',"seed-logicrw-refresh"),
('https://github.com/jonathanavis96/jev-kit','jev-kit',"Everything you need to run TypeSafe's Jev with Claude Code: a tool-call guard, tier guard, file search, browser agent, review, belay, compaction and installers.",'Use cases',"seed-logicrw-refresh"),
('https://github.com/CompleteDotTech/jev-factorio-agent','jev-factorio-agent',"Jev picks what, code owns how - a System One Factorio agent driven by TypeSafe's Jev on FLE",'Use cases',"seed-logicrw-refresh"),
('https://github.com/Excalibur9527/dsh-jev','dsh-jev',"This DeepSeek Harness plugin sends each round's latest user message to the systemone (Jev) API for emotion and intent classification and injects the result as plugin-sourced runtime context, with API Key and all…",'SDKs & tooling',"seed-logicrw-refresh"),
('https://github.com/JYeswak/jev_playground','jev_playground','Jev answers typed questions about a state with calibrated numbers. This repo is where we find out which of those numbers deserve to drive code, and where a regex or a constant does the job better.','SDKs & tooling',"seed-logicrw-refresh"),
('https://github.com/Sanoy24/jevpolicy','jevpolicy','JevPolicy is an open-source TypeScript decision runtime that turns probabilistic judgments from Jev, accessed through Vercel AI Gateway, into versioned, deterministic, replayable, observable application decisions.','SDKs & tooling',"seed-logicrw-refresh"),
('https://github.com/Wing9897/jev.tg','jev.tg','Local Telegram filter stores channel messages locally and sends them in batches to Jev or a local model to keep only messages matching natural-language conditions.','SDKs & tooling',"seed-logicrw-refresh"),
('https://github.com/bladedevoff/stuntd','stuntd',"Local proxy that learns your app's typed LLM decisions and answers them with a Laya head. Jev and OpenAI compatible.",'Open models & alternatives',"seed-logicrw-refresh"),
('https://github.com/allebee/jevk5','jevk5','An open model that answers the same typed questions Jev answers — yes/no, choice, score — in one forward pass with zero generated tokens (~13 ms on an H100), plus a head-to-head harness that puts Jev and the open…','Open models & alternatives',"seed-logicrw-refresh"),
('https://github.com/romeromarcelo/jev-retrieval','jev-retrieval','Grep-shaped Rust CLI for coding agents that finds files matching a plain-language concept: a local BM25 pass recalls candidates, Jev verifies each file window-by-window with Noul gates, and one listwise Choice per…','Use cases',"seed-logicrw-refresh"),
('https://github.com/xuan7zhang/jev-toolspace','jev-toolspace',"Jev answers yes/no (`noul`) questions about a shared state and returns an independent probability for each one. One API call scores every tool in a menu with one question per tool, and a tool's score does not compete…",'SDKs & tooling',"seed-logicrw-refresh"),
('https://github.com/KantaHayashiAI/jev-does-not-play-dice','jev-does-not-play-dice','Code, recorded outputs, and analysis scripts for probability-output experiments with Jev: fair random draws, Noul (Yes/No) questions, and forecast documents.','SDKs & tooling',"seed-logicrw-refresh"),
('https://github.com/jsk4581/jev-blindspot','jev-blindspot','A side panel for Claude Code and Codex CLI that shows the blind spots of each prompt you submit: what the request would have needed to consider and shows no sign of. Jev decides, in one call per prompt, whether the…','SDKs & tooling',"seed-logicrw-refresh"),
('https://github.com/Alex314618-create/JevRev','JevRev','Your LLM can imagine, write, test, and revise. It should not have to make every cheap routing decision by itself.','SDKs & tooling',"seed-logicrw-refresh"),
('https://github.com/mattn/go-jev','go-jev','Go SDK and CLI for TypeSafe Jev: typed decisions (yes/no, choice, score) from a model','SDKs & tooling',"seed-logicrw-refresh"),
('https://github.com/Selmar/typesafe-jev-calibrate-for-code-review','typesafe-jev-calibrate-for-code-review','About calibrating Jev for code reviews','SDKs & tooling',"seed-logicrw-refresh"),
('https://github.com/boldbug1/jev-triage','jev-triage','Message triage CLI in Go, built on the Jev decision model from TypeSafe AI. Categorizes messages, scores urgency, and flags low-confidence ones for human review.','SDKs & tooling',"seed-logicrw-refresh"),
('https://github.com/Larkspur-Wang/Jev_steer_or_queue','Jev_steer_or_queue','Let TypeSafe Jev decide whether a message you send mid-turn should steer, queue, or interrupt your coding agent. Claude Code plugin; Codex CLI in testing.','SDKs & tooling',"seed-logicrw-refresh"),
('https://github.com/eran-broder/jev-skills','jev-skills',"Skills without the context tax. Claude Code and Codex plugin: TypeSafe's Jev decides on every turn which skills the model sees. Always-on context cost: 0 tokens.",'SDKs & tooling',"seed-logicrw-refresh"),
('https://github.com/erkamyaman/jev-enforce','jev-enforce','Claude Code plugin that makes Claude follow your CLAUDE.md: every reply and edit checked by TypeSafe Jev ✅','Use cases',"seed-logicrw-refresh"),
('https://github.com/matthew004-web/heyreach-jev-bot','heyreach-jev-bot','Signal-based LinkedIn outbound scoring for HeyReach, running on Jev (TypeSafe System One).','Use cases',"seed-logicrw-refresh"),
('https://github.com/g0runmezadam/jev-architecture-research','jev-architecture-research','Black-box reverse engineering research archive for the Jev decision model','Evals & papers',"seed-logicrw-refresh"),
('https://github.com/mahmut-gundogdu/bes-kelime-jev','bes-kelime-jev','Jev bir sohbet modeli değil, **evaluation** modeli. Serbest metin üretmez; tipli sorulara `choice` / `score` / `boolean` cevapları döner. Bu, "sadece şu 5 kelimeden birini söyle" kısıtını *prompt\'la rica etmek*…','Use cases',"seed-logicrw-refresh"),
('https://github.com/rahulthakore16/n8n-nodes-jev','n8n-nodes-jev','Jev by TypeSafe AI for n8n: typed decisions, probabilities, and confidence-aware workflows','SDKs & tooling',"seed-logicrw-refresh"),
('https://github.com/ZJU-REAL/CUA-JEV','CUA-JEV',"The [experimental open-task paths](docs/OPEN_TASKS.md) separate model planning from Jev's typed action selection. They discover browser DOM elements or Windows UI Automation controls dynamically and offer grounded…",'Use cases',"seed-logicrw-refresh"),
('https://github.com/h0j5bz0adh0-stack/jev-pilot','jev-pilot','Fast System-1 Decision, Arbitration & Safety Engine for Autonomous AI Agents (Powered by TypeSafe Jev)','SDKs & tooling',"seed-logicrw-refresh"),
('https://github.com/Eric-Zhou-0302/jev-A-share-trader','jev-A-share-trader','A Jev-powered technical analysis workspace for China A-shares, supporting AKShare/Tushare, market scans, and Buy/Hold/Sell assessments with time horizons and traceable evidence.','Use cases',"seed-logicrw-refresh"),
('https://github.com/mcftira/jev-route','jev-route','**Run it. Log it. Distill it. Own it.**','Use cases',"seed-logicrw-refresh"),
('https://github.com/0xwhrari/grok-jev-guard','grok-jev-guard','`grok-jev-guard` sits immediately before a meaningful Grok Bot tool sequence. It receives a compact description of the pending operation and returns one explicit action:','Use cases',"seed-logicrw-refresh"),
('https://github.com/LiuHao-1443/jev-table-tennis','jev-table-tennis',"Table tennis vs. TypeSafe's Jev (System One). Every paddle move on the right is a live model decision — no local prediction, just a lookup table and a servo.",'Use cases',"seed-logicrw-refresh"),
('https://github.com/Alpha-Harper-Franklin/jev-drive','jev-drive','Jev + autonomous driving: structured decisions, multimodal baselines, recovery research, and measured API diagnostics.','Use cases',"seed-logicrw-refresh"),
('https://github.com/tubone24/jev-practice-speed','jev-practice-speed',"A WebGL demo where you play the card game Speed against a CPU whose brain is TypeSafe AI's Jev. The whole point of the app is to measure and show Jev's decision speed and decision accuracy in real time.",'Use cases',"seed-logicrw-refresh"),
('https://github.com/gaborishka/jev-wrapped','jev-wrapped','The browser asks for up to four pages at a time (the plan says how many), which makes up to 24 Jev requests in flight, and shows every answer as it arrives. If a page comes back throttled, it goes to the end of the…','Use cases',"seed-logicrw-refresh"),
('https://github.com/llt22/jev-lab','jev-lab',"Hands-on research lab for TypeSafe's Jev (System One model): reproducible benchmarks of Noul/Choice/Score primitives, confidence gating, fan-out latency, agent control — plus a living audit of the Jev ecosystem.",'SDKs & tooling',"seed-logicrw-refresh"),
('https://github.com/TomRichner/can-jev-bayes','can-jev-bayes','How well can Jev make sequential decisions under uncertainty, and how can Bayesian methods help it learn and act more effectively?','Use cases',"seed-logicrw-refresh"),
('https://github.com/miounet11/jevcode','jevcode',"This repository provides an Astro-based multilingual documentation site explaining Jev's Choice, Score, and Noul decision primitives with architecture patterns and usage examples.",'SDKs & tooling',"seed-logicrw-refresh"),
('https://github.com/maxlibin/jev-toto','jev-toto','Counting and comparison happen in Rust, because Jev is documented as unreliable at arithmetic. Jev receives per-number facts plus plain-English labels and answers two questions per number in one request: a yes/no…','SDKs & tooling',"seed-logicrw-refresh"),
('https://github.com/arnab621/typesafe-jev-plugin','typesafe-jev-plugin','Jev from Typesafe.ai is a "System One" AI model that returns **typed, calibrated judgments** instead of generating text. You define what to classify (a Choice), score (a Score), or verify (a Noul), and Jev returns a…','SDKs & tooling',"seed-logicrw-refresh"),
('https://github.com/darthblanc/tictacjev','tictacjev',"A tic-tac-toe app where one player is Jev, TypeSafe AI's System One Model with live confidence scores and probabilities.",'Use cases',"seed-logicrw-refresh"),
('https://github.com/lianghsun/jev-tmmluplus-eval','jev-tmmluplus-eval','Jev is not a chat model. You hand it a `state` plus a map of typed questions, and it returns one typed answer each — with calibrated probabilities and **no generated text**.','Evals & papers',"seed-logicrw-refresh"),
('https://github.com/Nisaka520/JevIntent','JevIntent','It is a FkWeChat plugin that analyzes a long-pressed WeChat text message with the Jev model for intent, emotion, urgency and reply posture and shows the result in local Toasts.','Use cases',"seed-logicrw-refresh"),
('https://github.com/PyModel/jev-judge-mcp','jev-judge-mcp',"Typed judgment tools for MCP agents. TypeSafe's Jev model as verify, screen, find, classify, rerank, decide, compare, extract, review, gate, and score: the model judges, policy decides auto, review, or escalate.",'SDKs & tooling',"seed-logicrw-refresh"),
('https://github.com/bodepudimuneendra-netizen/laya-jev-GraphRAG','laya-jev-GraphRAG','Agentic GraphRAG engine using swappable System One decision models (local Laya / cloud Jev). Features a complete 4-phase pipeline (Ingestion, Pre-Retrieval, Traversal, Post-Retrieval) and evaluation across Neo4j,…','Use cases',"seed-logicrw-refresh"),
('https://github.com/6Mikao9/jev-agent-design-with-topk-logits-choices','jev-agent-design-with-topk-logits-choices','Research design for a Jev-native agent system: tool integration, speculative parameter proposals, external helper logits Top-k proposals with Jev-controlled fallback ,decision-aware hierarchical memory, and…','SDKs & tooling',"seed-logicrw-refresh"),
('https://github.com/Nisaka520/JevBystander','JevBystander','This Android accessibility app reads visible WeChat one-to-one chat text and uses Jev to judge intent, emotion, urgency and reply posture, showing the result as 3 Toasts without generating or sending replies.','Use cases',"seed-logicrw-refresh"),
('https://github.com/emirbartu/jev-for-all','jev-for-all','Jev for every agentic development workflow — the System One decision model wired into whatever harness an agent codes in: OpenCode today, Claude Code and Hermes adapters next.','Use cases',"seed-logicrw-refresh"),
('https://github.com/usail-hkust/JevLight','JevLight','Jev-powered traffic signal control on CityFlow with structured phase and green-time decisions.','Use cases',"seed-logicrw-refresh"),
('https://github.com/YidiDev/jev-benchmark','jev-benchmark','Rubric-Based Zero-Shot Classification Benchmark: Jev vs Claude Haiku 4.5 vs Claude Sonnet 5 vs OpenJev on rubric-conditioned classification, chained decision execution, and exam grading -- with full price tracking.','SDKs & tooling',"seed-logicrw-refresh"),
('https://github.com/xhongc/jev-music-tag','jev-music-tag','A minimal FastAPI and React workbench that sends local audio tags to Jev for decisions and writes the returned metadata updates back to the audio files.','Use cases',"seed-logicrw-refresh"),
('https://github.com/trietphan/jev-claw','jev-claw','Typed model routing for OpenClaw agents, powered by TypeSafe Jev','Use cases',"seed-logicrw-refresh"),
('https://github.com/AMMIROSOH/jev-2048-selenium','jev-2048-selenium','Selenium 2048 player powered by expectimax search and TypeSafe Jev, with portrait FFmpeg recording.','Use cases',"seed-logicrw-refresh"),
('https://github.com/Parthkomalwad/jevbrief','jevbrief','[Adapters](#adapters) &nbsp;·&nbsp; [Quick start](#quick-start) &nbsp;·&nbsp; [Game demo](#watch-jev-play-a-game) &nbsp;·&nbsp; [Python](#use-it-in-python) &nbsp;·&nbsp; [Viewer](#see-every-decision) &nbsp;·&nbsp;…','SDKs & tooling',"seed-logicrw-refresh"),
('https://github.com/CogFlux/opencode-jev-guard','opencode-jev-guard',"When FarHand is active, the agent's commands run on a remote host through the `farhand_remote_shell` MCP tool instead of `shell`. OpenCode's permission request for an MCP tool carries no arguments, so the plugin…",'Use cases',"seed-logicrw-refresh"),
('https://github.com/bl888m/jev-bot','jev-bot','JEV-powered market decision bot for stocks, crypto and memes. State in, BUY/SELL/HOLD/AVOID out, paper by default','Use cases',"seed-logicrw-refresh"),
('https://github.com/Nachom3/jevTrader','jevTrader','A High Frecuncy Trader made in Rust using Jev as a decision maker.','Use cases',"seed-logicrw-refresh"),
('https://github.com/Akramovic1/jev-pilot','jev-pilot',"Let Jev steer Claude Code: the right reasoning effort, subagent model and skill for every prompt. A Claude Code plugin powered by TypeSafe's Jev (OpenRouter / TypeSafe).",'Use cases',"seed-logicrw-refresh"),
('https://github.com/Bring-AI/jev-numeric','jev-numeric','**Both are multiway decision trees; decimal-digit decoding is a ten-way instance.** On an aligned decimal grid, they can have identical branches and leaves, expressed through different prompts. The digit is a…','SDKs & tooling',"seed-logicrw-refresh"),
('https://github.com/tusharck/jev-inbox-queue','jev-inbox-queue','Turn an inbox into a short action queue with Jev (TypeSafe System One)','SDKs & tooling',"seed-logicrw-refresh"),
('https://github.com/dingw530/playwright-jev','playwright-jev','This tool provides a Node CLI for goal-driven web E2E testing where Jev chooses the next step from a code-generated action space, playwright-cli observes and executes browser actions, and code controls inputs,…','Use cases',"seed-logicrw-refresh"),
('https://github.com/flazouh/ego-jev','ego-jev','Drive ego-browser pages with TypeSafe Jev: code builds the allowed actions, Jev picks one, code acts and re-checks.','Use cases',"seed-logicrw-refresh"),
('https://github.com/Zafer-Liu/jev-xiangqi','jev-xiangqi','Play Chinese Chess (Xiangqi) against Jev - TypeSafe System One decision model as the AI. Score fan-out over legal moves.','Use cases',"seed-logicrw-refresh"),
('https://github.com/Siim/jev-claim-vs-measured','jev-claim-vs-measured',"A post with ~400k views says TypeSafe's **Jev** is the fastest AI model ever built for trading, makes calibrated buy/sell decisions in under 100 ms, and shows how to build an HFT system on it. The article behind it…",'Use cases',"seed-logicrw-refresh"),
('https://github.com/dabaicai001/jeves-desk','jeves-desk','This repository implements a configurable customer-service platform combining ChatKit UI, Jev decision-making, generative chat, RAG knowledge lookup, plugin Tools, MCP data access, and YAML-driven Agent dispatch.','Use cases',"seed-logicrw-refresh"),
('https://github.com/Teylersf/WindowsJev','WindowsJev','Token-efficient Windows automation and durable research MCP server for Codex and Claude Code, powered by TypeSafe Jev.','Use cases',"seed-logicrw-refresh"),
('https://github.com/baize7815/jev-mcp-open-source','jev-mcp-open-source','Self-hosted Jev MCP on Cloudflare Workers with intent routing, retrieval reranking and batch judgments','SDKs & tooling',"seed-logicrw-refresh"),

# Daily X-scan 2026-09-24 — missing high-signal OS / serving / evals
("https://github.com/mithalouni/system-one-open","system-one-open","Open replica of TypeSafe Jev: typed calibrated decisions in one forward pass on Gemma 4 E2B / Gemma 3 270M (Modal).","Open models & alternatives","seed-x-scan"),
("https://github.com/kotoba-lang/typed-decisions","typed-decisions","Jev-shaped Choice/Score/Noul model on ModernBERT, DeBERTa, and LLaDA-MoE with measured latency, accuracy, and calibration.","Open models & alternatives","seed-x-scan"),
("https://github.com/VitaDAO/open-jev-tinfoil","open-jev-tinfoil","Attested CPU serving for the open Jev DeBERTa typed-decision model.","Open models & alternatives","seed-x-scan"),
("https://github.com/chengyongru/fastjev","fastjev","Independently maintained SemIf fork: self-hosted semantic decisions via Torch, vLLM, MLX, llama.cpp, and optional HTTP API.","Open models & alternatives","seed-x-scan"),
("https://github.com/franckverrot/lev","lev","Jev-style decision model on LiquidAI LFM2.5-350M with a TypeSafe-compatible /v1/systemone server.","Open models & alternatives","seed-x-scan"),
("https://github.com/Octalab-Inc/jqv","jqv","Stock Qwen3 decision API: shared-state prefill, choice-token readout, temperature-calibrated probabilities, TypeSafe-compatible.","Open models & alternatives","seed-x-scan"),
("https://codiv.ai","Codiv","Hosted inference for open System One models; serves OpenJev through a Jev-compatible API.","Open models & alternatives","seed-x-scan"),
("https://api.codiv.ai","Codiv API","Jev-compatible base URL for Codiv-hosted OpenJev (point TYPESAFE_BASE_URL here).","Open models & alternatives","seed-x-scan"),
("https://benchmarkheaven.com/jev-models","JevBench (Benchmark Heaven)","Interactive JevBench leaderboard: typed decision models scored on intelligence, calibration, speed, and cost.","Evals & papers","seed-x-scan"),
("https://who-is-right.app.mintapis.com","Who is right?","No-signup JevBench demo: typed decisions over a claim-dispute scenario.","Use cases","seed-x-scan"),
("https://is-it-ai-slop.app.mintapis.com","Is it AI slop?","No-signup JevBench demo: typed decisions for AI-slop detection.","Use cases","seed-x-scan"),

# Daily X-scan 2026-09-25 — paper/weights/index finds (live X search loginwalled; indexed + web)
("https://arxiv.org/abs/2609.29429","Just Ask Jev","RLCDAlignBench paper: Jev as zero-shot alignment-failure detector across 44 benchmarks (median AUROC 0.886).","Evals & papers","seed-x-scan"),
("https://github.com/sumleo/RLCDAlignBench","RLCDAlignBench","Code and data for Just Ask Jev — 44 alignment-failure detection benchmarks with cached Jev answers.","Evals & papers","seed-x-scan"),
("https://huggingface.co/datasets/sumleo/RLCDAlignBench","RLCDAlignBench (dataset)","Cached Jev responses and detection instances for RLCDAlignBench.","Evals & papers","seed-x-scan"),
("https://huggingface.co/AlexWortega/openjev","openjev (AlexWortega)","Qwen3.5 NLI/cross-encoder Jev-style models (0.8B–4B, MoE) with typed-decision adapter and public JevBench numbers.","Open models & alternatives","seed-x-scan"),
("https://huggingface.co/ZefanCai/Open-Jev-2B","Open-Jev-2B","LoRA + decision head on Qwen3.5-2B for Choice/Score/Noul; Apache-2.0 weights for Zefan-Cai/Open-Jev.","Open models & alternatives","seed-x-scan"),
("https://huggingface.co/ZefanCai/Open-Jev-9B","Open-Jev-9B","LoRA + decision head on Qwen3.5-9B for Choice/Score/Noul; Apache-2.0 weights for Zefan-Cai/Open-Jev.","Open models & alternatives","seed-x-scan"),
("https://zefan-cai.github.io/open-jev/","Open-Jev (site)","Project site for Open-Jev open-weight typed-decision checkpoints and evals.","Docs & essays","seed-x-scan"),
("https://huggingface.co/com-kotobalabs/open-jev-deberta-v3-large","open-jev-deberta-v3-large","DeBERTa-v3-large Jev-shaped Choice/Score/Noul model from kotoba-lang/typed-decisions; public-gold training.","Open models & alternatives","seed-x-scan"),
("https://huggingface.co/spaces/multimodalart/jev-decision-index","Jev Decision Index","HF Space indexing 30+ open-weight decision models across 35+ benchmarks / 130K questions.","Evals & papers","seed-x-scan"),
("https://huggingface.co/openjev/openjev-FP8","openjev-FP8","FP8 quantized OpenJev weights (~29 GB) for single-GPU serving.","Open models & alternatives","seed-x-scan"),
("https://huggingface.co/openjev/openjev-MLX","openjev-MLX","MLX 8-bit OpenJev build for Apple silicon (text-only).","Open models & alternatives","seed-x-scan"),
("https://x.com/airesearch12/status/2103267811480993858","JevBench v1.4.2 update","Benchmark Heaven post: JevBench v1.4.2 live; decider-4b v2 leads on the board.","Docs & essays","seed-x-scan"),

]

INGEST_DATE = "2026-09-25 PT"

# Display order (newcomers: OS alternatives + use cases before the SDK dump).
DISPLAY_ORDER = [CAT_HOSTED, CAT_OS, CAT_USE, CAT_DOCS, CAT_EVALS, CAT_SDKS, CAT_LISTS, CAT_COMMUNITY]

LANDMARK_OS = [
    "https://github.com/jaredpalmer/kev",
    "https://github.com/razorback16/openjev",
    "https://huggingface.co/togethercomputer/Tev1-4B-experimental",
    "https://github.com/NandhaKishorM/laya",
    "https://github.com/vinnylarouge/jevlike",
    "https://huggingface.co/akhilaaa3/Jev-Omni",
    "https://github.com/bespokelabsai/nimble",
    "https://github.com/TheoLeeCJ/SemIf",
    "https://github.com/bnsd55/jevmlx",
    "https://github.com/GodModeAI2025/JevCoreML",
    "https://github.com/mizorewww/laya-mlx",
    "https://github.com/mizorewww/laya-coreml",
]
PIN_EVALS = [
    "https://benchmarkheaven.com/jev-models",
    "https://jevbench.dev",
    "https://github.com/fstandhartinger/jevbench",
    "https://jevals.com",
]
CATEGORY_OVERRIDE = {
    "https://github.com/mithalouni/system-one-open": CAT_OS,
    "https://github.com/kotoba-lang/typed-decisions": CAT_OS,
    "https://github.com/VitaDAO/open-jev-tinfoil": CAT_OS,
    "https://github.com/chengyongru/fastjev": CAT_OS,
    "https://github.com/franckverrot/lev": CAT_OS,
    "https://github.com/Octalab-Inc/jqv": CAT_OS,
    "https://codiv.ai": CAT_OS,
    "https://api.codiv.ai": CAT_OS,
    "https://benchmarkheaven.com/jev-models": CAT_EVALS,
    "https://who-is-right.app.mintapis.com": CAT_USE,
    "https://is-it-ai-slop.app.mintapis.com": CAT_USE,

    "https://huggingface.co/akhilaaa3/Jev-Omni": CAT_OS,
    "https://huggingface.co/datasets/akhilaaa3/decision-bench": CAT_EVALS,
    "https://x.com/Akhila_988/status/2102171891410825520": CAT_DOCS,
    "https://x.com/thekitze/status/2102775497822503298": CAT_DOCS,
    "https://x.com/togethercompute/status/2102882216950763814": CAT_DOCS,
    "https://together.ai/blog/how-to-train-your-own-jev": CAT_DOCS,
    "https://huggingface.co/togethercomputer/Tev1-4B-experimental": CAT_OS,
    "https://github.com/togethercomputer/tev1": CAT_OS,
    "https://api.together.ai/models/together/Tev1-4B-experimental": CAT_OS,
    "https://blog.google/innovation-and-ai/technology/developers-tools/diffusion-gemma-faster-text-generation": CAT_DOCS,
    "https://huggingface.co/openjev/openjev": CAT_OS,
    "https://github.com/vllm-project/vllm/pull/57250": CAT_OS,
    "https://github.com/wnzn/semif-go": CAT_OS,
    "https://github.com/jaredpalmer/kev/releases/tag/kev-family": CAT_OS,
    "https://jevbench.dev": CAT_EVALS,
    "https://github.com/fstandhartinger/jevbench": CAT_EVALS,
    "https://jevals.com": CAT_EVALS,
    "https://github.com/iammrduncan/typesafe-ai-benchmark": CAT_EVALS,
    "https://github.com/kuleshov-group/mdlm": CAT_EVALS,
    "https://systemonemodels.org/examples/alternatives": CAT_LISTS,
    "https://github.com/kevinbadi/jev-voice": CAT_USE,
    "https://github.com/kevinbadi/hyperedit": CAT_USE,
    "https://github.com/OmniJev/PlayJev": CAT_USE,
    "https://github.com/virajbhartiya/laya-vs-jev": CAT_USE,
    "https://en.wikipedia.org/wiki/Thinking,_Fast_and_Slow": CAT_DOCS,
    "https://nobelprize.org/prizes/economic-sciences/2002/kahneman/lecture": CAT_DOCS,
    "http://incompleteideas.net/IncIdeas/BitterLesson.html": CAT_DOCS,
    "https://platform.openai.com/docs/guides/structured-outputs": CAT_DOCS,
    "https://explainx.ai/blog/how-does-jev-work-rlcd-system-one-model-explained-2026": CAT_DOCS,
    "https://agentpedia.codes/blog/jev-system-one-models": CAT_DOCS,
    "https://github.com/trycua/cua": CAT_USE,
    "https://github.com/FluidInference/FluidUse": CAT_USE,
    "https://openrouter.ai/typesafe/jev-1.13": CAT_SDKS,
    "https://anthonymaio.substack.com/p/jev-the-language-model-that-wont": CAT_DOCS,
    "https://doi.org/10.1016/j.ecolecon.2005.03.020": CAT_DOCS,
    "https://github.com/qingshungLI/everything-about-jev": CAT_DOCS,
    "https://github.com/Adkid-Zephyr/chinese-workflow-decision-bench": CAT_EVALS,
    "https://github.com/aangelopoulos/conformal-prediction": CAT_EVALS,
    "https://x.com/CompleteSkeptic/status/2099925682726002904": CAT_DOCS,
    'https://github.com/ReallyArtificial/stuntdouble': CAT_OS,
    'https://github.com/kenhuangus/jev-usecases': CAT_DOCS,
    'https://github.com/paramjeetn/jev-cookbook': CAT_DOCS,
    'https://github.com/harrymunro/jev-laya-benchmark': CAT_EVALS,
    'https://github.com/kaustav1996/reflex': CAT_OS,
    'https://github.com/NicolaiLassen/open-bonsai-jev': CAT_OS,
    'https://github.com/harshithsunku/learn-jev-end-to-end': CAT_DOCS,
    'https://github.com/jmanhype/jev-dspy-lab': CAT_EVALS,
    'https://github.com/bladedevoff/stuntd': CAT_OS,
    'https://github.com/allebee/jevk5': CAT_OS,
    'https://github.com/g0runmezadam/jev-architecture-research': CAT_EVALS,
    'https://github.com/lianghsun/jev-tmmluplus-eval': CAT_EVALS,
    "https://reddit.com/r/LLMDevs/comments/1wko2e5/i_reviewed_287_opensource_jev_projects_here_are": CAT_DOCS,
    "https://logicrw.github.io/awesome-jev-projects": CAT_LISTS,
    "https://arxiv.org/abs/2609.29429": CAT_EVALS,
    "https://github.com/sumleo/RLCDAlignBench": CAT_EVALS,
    "https://huggingface.co/datasets/sumleo/RLCDAlignBench": CAT_EVALS,
    "https://huggingface.co/AlexWortega/openjev": CAT_OS,
    "https://huggingface.co/ZefanCai/Open-Jev-2B": CAT_OS,
    "https://huggingface.co/ZefanCai/Open-Jev-9B": CAT_OS,
    "https://zefan-cai.github.io/open-jev/": CAT_DOCS,
    "https://huggingface.co/com-kotobalabs/open-jev-deberta-v3-large": CAT_OS,
    "https://huggingface.co/spaces/multimodalart/jev-decision-index": CAT_EVALS,
    "https://huggingface.co/openjev/openjev-FP8": CAT_OS,
    "https://huggingface.co/openjev/openjev-MLX": CAT_OS,
    "https://x.com/airesearch12/status/2103267811480993858": CAT_DOCS,

}

BLURBS = {
    CAT_HOSTED: "Three TypeSafe docs entry points. This catalog is an industry index, not a TypeSafe sitemap — cookbooks, SDKs, and essays live in the sections below.",
    CAT_OS: "Run Jev-style `Choice` / `Score` / `Noul` locally: open models, MLX and Core ML ports, adapters over existing LLMs, and related typed-output libraries.",
    CAT_USE: "Apps, demos, and TypeSafe cookbooks/patterns grouped by decision shape.",
    CAT_DOCS: "Explainers, launch coverage, TypeSafe concept pages, and background reading.",
    CAT_EVALS: "How these models are measured — including [JevBench](https://jevbench.dev/) — plus papers on calibration and structured decisions.",
    CAT_SDKS: "Clients, MCP servers, skills, and integrations — including TypeSafe’s SDKs. Application-shaped projects live under [Use cases](#use-cases).",
    CAT_LISTS: "Other curated indexes this catalog merges.",
    CAT_COMMUNITY: "TypeSafe chat, social, and the launch thread.",
}

def gh_anchor(heading: str) -> str:
    s = heading.lower().replace(" & ", "--").replace(" / ", "--").replace("/", "--").replace(" ", "-")
    return re.sub(r"[^a-z0-9\-]", "", s)

def _blob(e: Entry) -> str:
    return f"{e.title} {e.url} {e.description or ''}"

def rehome_typesafe(e: Entry) -> str:
    """Former Official dump → industry sections. Only HOSTED_KEEP stay in the pointer section."""
    if e.url in HOSTED_KEEP:
        return CAT_HOSTED
    u = e.url.lower()
    if "evals.typesafe" in u:
        return CAT_EVALS
    if any(x in u for x in (
        "github.com/typesafe-ai", "console.typesafe", "agent-skill",
        "vercel.com/ai-gateway", "openrouter.ai/typesafe",
    )):
        return CAT_SDKS
    if any(x in u for x in ("/cookbooks", "/patterns", "/demos", "use-case-map")):
        return CAT_USE
    if "typesafe" in u:
        return CAT_DOCS
    return CAT_DOCS

def recategorize(e: Entry) -> None:
    e.category = CAT_ALIASES.get(e.category, e.category)
    if e.url in HOSTED_KEEP:
        e.category = CAT_HOSTED
    elif e.category == CAT_HOSTED:
        e.category = rehome_typesafe(e)
    if e.url in CATEGORY_OVERRIDE and e.url not in HOSTED_KEEP:
        e.category = CATEGORY_OVERRIDE[e.url]
    titles = {
        "https://github.com/fstandhartinger/jevbench": "JevBench (text decisions)",
        "https://jevbench.dev": "JevBench",
        "https://docs.typesafe.ai": "Documentation",
        "https://docs.typesafe.ai/primitives": "Primitives",
        "https://docs.typesafe.ai/api": "HTTP API reference",
    }
    if e.url in titles:
        e.title = titles[e.url]
    if e.url in HOSTED_KEEP or (e.url in CATEGORY_OVERRIDE and e.url not in HOSTED_KEEP):
        return
    blob = _blob(e).lower()
    if e.category in (CAT_SDKS, CAT_USE, CAT_OS):
        if re.search(r"awesome[- ](jev|typesafe|open-system|open system)", blob) and "github.com" in e.url:
            e.category = CAT_LISTS
            return
        if "logicrw.github.io/awesome-jev-projects" in e.url and "/categories/" in e.url:
            e.category = CAT_LISTS
            return
        if "arxiv.org" in e.url or "doi.org" in e.url:
            e.category = CAT_EVALS if "arxiv.org" in e.url else CAT_DOCS
            return
        if "substack.com" in e.url:
            e.category = CAT_DOCS
            return
        if re.search(r"jevbench|jevals\.com", e.url.lower()):
            e.category = CAT_EVALS
            return
        if re.search(r"\b(bench|benchmark|eval)\b", e.title.lower()) and "sdk" not in blob and e.category == CAT_SDKS:
            e.category = CAT_EVALS
            return
    if e.category == CAT_USE:
        if any(h in e.url for h in ("wikipedia.org", "nobelprize.org", "incompleteideas.net")):
            e.category = CAT_DOCS

def _first(blob: str, rules, default: str) -> str:
    for name, rx in rules:
        if rx.search(blob):
            return name
    return default

def assign_subsection(e: Entry) -> str:
    blob = _blob(e)
    low = blob.lower()
    cat = e.category
    if cat == CAT_HOSTED:
        return ""
    if cat == CAT_OS:
        if e.url in LANDMARK_OS:
            return "Landmark projects"
        return _first(low, [
            ("Related classifiers & structured output", re.compile(r"instructor|outlines|\bdspy\b|gliner|setfit|modernbert|\bmdlm\b")),
            ("Adapters & logit readers", re.compile(r"adapter|logit|next-token|constrained decoding|anyjev|semif|simple-jev|simplejev|llm2jev|open-alternative|choosekit|poorjev|zero-shot nli")),
            ("Runtimes, ports & servers", re.compile(r"mlx|core.?ml|coreml|runtime|sglang|vllm|llama\.cpp|webgpu|transformers\.js|node\.js|cloud run|on-device|iphone|container|self-hosted|spark")),
        ], "Models & weights")
    if cat == CAT_USE:
        return _first(low, [
            ("Games, robotics & simulation", re.compile(r"\bgames?\b|snake|chess|mario|pokemon|doom|pong|starcraft|star.?craft|minecraft|robot|mujoco|vizdoom|gomoku|\b2048\b|tetris|t-rex|trex|civ2|grand prix|playjev|arcade|shooter|fighter|clash royale|vampire survivors|runescape|drone|airways|simulation")),
            ("Browser, computer use & OS", re.compile(r"browser|playwright|puppeteer|computer.?use|accessibility|chrome extension|firefox|\bcua\b|macos|os action|fluiduse")),
            ("Search, RAG & rerank", re.compile(r"rerank|re-rank|\brag\b|retriev|passage|semantic (find|search|line)|jevfind|jev-search|data.?search")),
            ("Guardrails, safety & review", re.compile(r"guardrail|prompt.?inject|moderat|safety|warden|permission|abuse|\bspam\b|adblock|containment|quarantine|code review|antivirus")),
            ("Routing & triage", re.compile(r"\brout(?:e|er|ing)\b|triage|dispatch|intent|ticket")),
            ("Extraction & structured data", re.compile(r"extract|document|\bner\b|entity|sql\b|duckdb|sqlite|pdf|folder filer")),
            ("Classification", re.compile(r"classif|taxonomy|label|sentiment")),
            ("Agents, tools & harnesses", re.compile(r"\bagents?\b|\bskill\b|harness|tool.?call|\bmcp\b")),
            ("Voice, mail & productivity", re.compile(r"voice|speech|mail|email|inbox|dictation|clipboard|transcript|wechat|linkedin|youtube|call coach|reading-practice|\basr\b")),
            ("Markets & operations", re.compile(r"\btrade\b|trading|stock|crypto|market|hedge.?fund|hyperliquid")),
            ("Creative tools", re.compile(r"blender|midi|music|comfyui|video editor|hyperedit|design-mock|shadcn|creative")),
            ("Playgrounds & live demos", re.compile(r"playground|try app|interactive|live demo|\bdemos?\b|\brepl\b")),
        ], "Other applications")
    if cat == CAT_SDKS:
        if any(x in e.url.lower() for x in ("github.com/typesafe-ai", "vercel.com/ai-gateway", "vercel.com/kb/guide/typesafe", "console.typesafe", "openrouter.ai/typesafe")):
            return "TypeSafe SDKs & gateways"
        return _first(low, [
            ("MCP, skills & agent plugins", re.compile(r"\bmcp\b|\bskill\b|plugin|claude code|codex|hermes|opencode|pretooluse|\bhook\b")),
            ("Community SDKs & clients", re.compile(r"\bsdk\b|\bclient\b|pypi|npm |library|package")),
            ("Integrations & data pipelines", re.compile(r"duckdb|sqlite|dbt|airflow|\bsql\b|gateway|provider|integration|polars|lang(?:chain|graph)|ai sdk")),
        ], "Other tooling")
    if cat == CAT_EVALS:
        if "arxiv.org" in e.url:
            return "Papers"
        if any(x in low for x in ("jevbench.dev", "starcraft", "harness", "interactive")) or e.url in PIN_EVALS[:1]:
            return "Harnesses & live benches"
        return "Typed-decision benchmarks"
    return ""

def pin_index(url: str, pins: list[str]) -> int:
    try:
        return pins.index(url)
    except ValueError:
        return 10_000

def github_repo_slug(url: str) -> str | None:
    """Return owner/repo for a GitHub repo-root URL, else None (HF/docs/X/deep paths skipped)."""
    nu = normalize_url(url)
    m = re.match(r"^https?://github\.com/([^/]+)/([^/]+)$", nu, re.I)
    if not m:
        return None
    owner, repo = m.group(1), m.group(2)
    if owner.lower() in GH_SKIP_OWNERS:
        return None
    if repo.lower() in {"followers", "following", "repositories", "projects", "packages", "sponsors"}:
        return None
    return f"{owner}/{repo}"

def load_stars_cache() -> dict:
    if not STARS_CACHE.exists():
        return {}
    try:
        data = json.loads(STARS_CACHE.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except (json.JSONDecodeError, OSError):
        return {}

def save_stars_cache(cache: dict) -> None:
    # Stable key order for cleaner diffs.
    ordered = {k: cache[k] for k in sorted(cache, key=str.lower)}
    STARS_CACHE.write_text(json.dumps(ordered, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

def _cache_entry_fresh(entry: dict, now: datetime) -> bool:
    if not isinstance(entry, dict) or "stars" not in entry:
        return False
    fetched = entry.get("fetched_at") or ""
    try:
        ts = datetime.fromisoformat(fetched.replace("Z", "+00:00"))
    except ValueError:
        return False
    if ts.tzinfo is None:
        ts = ts.replace(tzinfo=timezone.utc)
    return (now - ts).total_seconds() < STARS_TTL_DAYS * 86400

def _fetch_stars_graphql_batch(slugs: list[str]) -> dict[str, int | None]:
    """Batch-fetch stargazerCount via `gh api graphql`. Missing repos → None."""
    if not slugs:
        return {}
    parts = []
    alias_to_slug = {}
    for i, slug in enumerate(slugs):
        owner, repo = slug.split("/", 1)
        alias = f"r{i}"
        alias_to_slug[alias] = slug
        parts.append(
            f"{alias}: repository(owner: {json.dumps(owner)}, name: {json.dumps(repo)}) {{ stargazerCount }}"
        )
    # Single-line query body; pass via temp file so shell/-f quoting stays sane.
    query = "query { " + " ".join(parts) + " }"
    qpath = ROOT / ".stars_query.graphql"
    for attempt in range(4):
        qpath.write_text(query, encoding="utf-8")
        proc = subprocess.run(
            ["gh", "api", "graphql", "-F", f"query=@{qpath}"],
            capture_output=True, text=True, timeout=180,
        )
        # gh exits 1 when any alias is NOT_FOUND, but still returns partial data on stdout.
        try:
            payload = json.loads(proc.stdout or "")
        except json.JSONDecodeError:
            payload = {}
        data = payload.get("data")
        if isinstance(data, dict) and data:
            out: dict[str, int | None] = {}
            for alias, slug in alias_to_slug.items():
                node = data.get(alias)
                if node is None:
                    out[slug] = None
                else:
                    out[slug] = int(node.get("stargazerCount") or 0)
            return out
        err = (proc.stderr or proc.stdout or "").strip()
        # Rate limit / secondary limit — back off.
        if "rate limit" in err.lower() or "403" in err or "502" in err or "timeout" in err.lower():
            time.sleep(2 ** attempt)
            continue
        print(f"  graphql batch failed ({len(slugs)}): {err[:200]}", file=sys.stderr)
        return {s: None for s in slugs}
    print(f"  graphql batch gave up after retries ({len(slugs)})", file=sys.stderr)
    return {s: None for s in slugs}

def ensure_stars(entries: dict, force: bool = False) -> dict[str, int | None]:
    """
    Return map of normalized entry URL → star count (int) or None if unknown/non-GitHub.
    Cache lives in stars_cache.json (keyed by owner/repo). Uses `gh api graphql` in batches.
    """
    cache = load_stars_cache()
    now = datetime.now(timezone.utc)
    now_iso = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    needed: list[str] = []
    slug_by_url: dict[str, str] = {}
    for e in entries.values():
        slug = github_repo_slug(e.url)
        if not slug:
            continue
        slug_by_url[e.url] = slug
        key = slug.lower()
        # Prefer exact key, fall back to case-insensitive hit.
        entry = cache.get(slug) or cache.get(key)
        if entry is None:
            for k, v in cache.items():
                if k.lower() == key:
                    entry = v
                    break
        if force or not _cache_entry_fresh(entry or {}, now):
            needed.append(slug)

    # Dedupe while preserving order
    seen = set()
    todo = []
    for s in needed:
        k = s.lower()
        if k not in seen:
            seen.add(k)
            todo.append(s)

    if todo:
        print(f"Fetching GitHub stars for {len(todo)} repos (batch={STARS_BATCH})…")
        for i in range(0, len(todo), STARS_BATCH):
            batch = todo[i : i + STARS_BATCH]
            got = _fetch_stars_graphql_batch(batch)
            for slug, stars in got.items():
                cache[slug] = {"stars": stars, "fetched_at": now_iso}
            print(f"  …{min(i + STARS_BATCH, len(todo))}/{len(todo)}")
            time.sleep(0.2)  # polite pause between batches
        save_stars_cache(cache)
        print(f"Wrote {STARS_CACHE.name} ({len(cache)} entries)")
    else:
        print(f"Star cache fresh ({len(cache)} entries) — skip API")

    # Build URL → stars map (None = unknown / non-GitHub)
    url_stars: dict[str, int | None] = {}
    for e in entries.values():
        slug = slug_by_url.get(e.url) or github_repo_slug(e.url)
        if not slug:
            url_stars[e.url] = None
            continue
        entry = cache.get(slug)
        if entry is None:
            for k, v in cache.items():
                if k.lower() == slug.lower():
                    entry = v
                    break
        if isinstance(entry, dict) and entry.get("stars") is not None:
            url_stars[e.url] = int(entry["stars"])
        else:
            url_stars[e.url] = None
    return url_stars

def sort_key(e: Entry, pins: list[str] | None = None, stars_map: dict | None = None):
    """Pins/landmarks first (pin list order), then stars desc, then title. Unknown stars last."""
    pin = pin_index(e.url, pins or [])
    raw = (stars_map or {}).get(e.url)
    # Known counts (including 0) beat unknown; among known, higher first.
    if raw is None:
        star_rank = -1  # sorts after 0 via -star_rank
    else:
        star_rank = int(raw)
    return (pin, -star_rank, e.title.lower())

def raw_ready() -> bool:
    return RAW.is_dir() and (RAW / "AbdelStark-awesome-typesafe-jev.md").exists()

def ingest_raw(entries: dict) -> None:
    md_sources = {
        "AbdelStark/awesome-typesafe-jev": RAW/"AbdelStark-awesome-typesafe-jev.md",
        "logicrw/awesome-jev-projects": RAW/"logicrw-awesome-jev-projects.md",
        "OmniJev/awesome-jev-gallery": RAW/"OmniJev-awesome-jev-gallery.md",
        "AppitStudio/awesome-jev": RAW/"AppitStudio-awesome-jev.md",
        "BeatAPI/awesome-jev": RAW/"BeatAPI-awesome-jev.md",
        "rupeshpoojary9/awesome-open-system-one": RAW/"rupeshpoojary9-awesome-open-system-one.md",
        "kydlikebtc/awesome-jev": RAW/"kydlikebtc-awesome-jev.md",
        "MrJev/awesome-jev": RAW/"MrJev-awesome-jev.md",
    }
    for src, path in md_sources.items():
        text = path.read_text(encoding="utf-8", errors="replace")
        parse_markdown(text, src, entries)
        if src in ("BeatAPI/awesome-jev", "OmniJev/awesome-jev-gallery", "AppitStudio/awesome-jev", "MrJev/awesome-jev"):
            parse_markdown_all_links(text, src, entries)
    parse_abdelstark_json(RAW/"abdelstark-resources.json", entries)
    parse_kyd_catalog(RAW/"kydlikebtc-catalog.json", entries)
    parse_alternatives_html(RAW/"systemonemodels-alternatives.html", entries)
    if (RAW/"BeatAPI-projects.json").exists():
        parse_beatapi_json(RAW/"BeatAPI-projects.json", entries)

def load_links_json(entries: dict) -> None:
    path = OUT / "links.json"
    if not path.exists():
        return
    for row in json.loads(path.read_text(encoding="utf-8")):
        url, title = row.get("url") or "", row.get("title") or ""
        desc, cat = row.get("description") or "", row.get("category") or CAT_USE
        srcs = row.get("sources") or ["links.json"]
        add(entries, url, title, desc, cat, srcs[0])
        nu = normalize_url(url)
        if nu in entries:
            for s in srcs[1:]:
                entries[nu].sources.add(s)

def intro_lines(n: int) -> list[str]:
    return [
        "# Awesome System One",
        "",
        "[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)",
        "",
        "> Typed decision models for software control flow — not chatbots. A consolidated catalog of **System One** / **Jev-style** resources.",
        "",
        "**System One** models take unstructured state plus typed questions and return structured decisions (`Choice`, `Score`, `Noul`) with calibrated probabilities in one parallel pass. Software branches on those values. They do not generate chat replies.",
        "",
        "TypeSafe’s **[Jev](https://typesafe.ai)** is the first *widely known* System One product — the launch that popularized this framing. Related ideas (typed classifiers, constrained decoding, calibrated probabilities, encoder decision heads) have a longer history; after Jev, the ecosystem filled in with [open reproductions](#open-source--local-alternatives), local/OS runtimes, [evals](#evals--papers), and community lists. This catalog merges those threads (see [Sources](#sources)). It does not claim Jev invented the underlying techniques.",
        "",
        f"**[JevBench](https://jevbench.dev/)** benches Jev, Jev-compatible open alternatives, and dual-brain (guide LLM + decision model) setups on interactive harnesses — starting with StarCraft II — measuring win/loss, task completion, and latency rather than a single typed-answer score.",
        "",
        "Deduplicated by normalized URL across the ingested indexes.",
        "",
        "Within each section (and subsection), **pins / landmarks stay first**; remaining items are ordered by **GitHub stars** (descending), then title. Stars are a practical proxy — not a full citation PageRank. Non-GitHub URLs (docs, HF, X, etc.) sort after starred repos. See [`stars_cache.json`](stars_cache.json).",
        "",
        f"**{n} unique links** · Ingested **{INGEST_DATE}** · License for this compilation: [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/) (linked projects keep their own licenses).",
        "",
        "### Start here",
        "",
        "- [Hosted: TypeSafe Jev](#hosted-typesafe-jev) — Three docs entry points (home, primitives, HTTP API).",
        "- [Open-source / local alternatives](#open-source--local-alternatives) — Kev, Laya, Jevlike, adapters, Core ML / MLX ports.",
        "- [Use cases](#use-cases) — Routing, classification, extraction, guardrails, agents, search/rerank, and more.",
        "- [JevBench](https://jevbench.dev/) — Interactive harness bench for Jev and open alternatives.",
        "- [System One Models](https://systemonemodels.org) — Independent living docs for the category.",
        "- [Jev alternatives index](https://systemonemodels.org/examples/alternatives) — Living index of open reproductions and cousins.",
        "",
    ]

def render_entry(e: Entry) -> str:
    return f"- [{e.title}]({e.url}) — {e.description}"

def write_outputs(entries: dict, stars_map: dict | None = None) -> None:
    stars_map = stars_map or {}
    by_cat = collections.defaultdict(list)
    by_sub = collections.defaultdict(lambda: collections.defaultdict(list))
    for e in entries.values():
        recategorize(e)
        e.subsection = assign_subsection(e)
        by_cat[e.category].append(e)
        by_sub[e.category][e.subsection or ""].append(e)

    sub_order = {
        CAT_OS: ["Landmark projects", "Models & weights", "Runtimes, ports & servers", "Adapters & logit readers", "Related classifiers & structured output"],
        CAT_USE: [
            "Routing & triage", "Classification", "Extraction & structured data",
            "Guardrails, safety & review", "Agents, tools & harnesses", "Search, RAG & rerank",
            "Browser, computer use & OS", "Games, robotics & simulation",
            "Voice, mail & productivity", "Markets & operations", "Creative tools",
            "Playgrounds & live demos", "Other applications",
        ],
        CAT_SDKS: ["TypeSafe SDKs & gateways", "Community SDKs & clients", "MCP, skills & agent plugins", "Integrations & data pipelines", "Other tooling"],
        CAT_EVALS: ["Harnesses & live benches", "Typed-decision benchmarks", "Papers"],
    }

    for cat, items in by_cat.items():
        pins = PIN_HOSTED if cat == CAT_HOSTED else LANDMARK_OS if cat == CAT_OS else (PIN_EVALS if cat == CAT_EVALS else [])
        items.sort(key=lambda e: sort_key(e, pins, stars_map))
        for sub, sub_items in by_sub[cat].items():
            sub_items.sort(key=lambda e: sort_key(e, pins, stars_map))

    source_counts = collections.Counter()
    for e in entries.values():
        for s in e.sources:
            source_counts[s] += 1

    links = []
    for cat in DISPLAY_ORDER:
        ordered_subs = sub_order.get(cat)
        if ordered_subs:
            seen = set()
            for sub in ordered_subs:
                for e in by_sub[cat].get(sub, []):
                    links.append({"url": e.url, "title": e.title, "description": e.description, "category": e.category, "subsection": e.subsection, "sources": sorted(e.sources)})
                    seen.add(e.url)
            for e in by_cat.get(cat, []):
                if e.url not in seen:
                    links.append({"url": e.url, "title": e.title, "description": e.description, "category": e.category, "subsection": e.subsection, "sources": sorted(e.sources)})
        else:
            for e in by_cat.get(cat, []):
                links.append({"url": e.url, "title": e.title, "description": e.description, "category": e.category, "subsection": e.subsection, "sources": sorted(e.sources)})
    for cat in sorted(by_cat):
        if cat in DISPLAY_ORDER:
            continue
        for e in by_cat[cat]:
            links.append({"url": e.url, "title": e.title, "description": e.description, "category": e.category, "subsection": e.subsection, "sources": sorted(e.sources)})

    n = len(links)
    (OUT / "links.json").write_text(json.dumps(links, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    lines = intro_lines(n)
    lines += ["## Contents", ""]
    for cat in DISPLAY_ORDER:
        items = by_cat.get(cat, [])
        if not items:
            continue
        lines.append(f"- [{cat}](#{gh_anchor(cat)}) ({len(items)})")
        for sub in sub_order.get(cat, []):
            sub_items = by_sub[cat].get(sub, [])
            if sub_items:
                lines.append(f"  - [{sub}](#{gh_anchor(sub)}) ({len(sub_items)})")
    lines += ["- [Sources](#sources)", "- [Contributing](#contributing)", ""]

    for cat in DISPLAY_ORDER:
        items = by_cat.get(cat, [])
        if not items:
            continue
        lines += [f"## {cat}", "", BLURBS.get(cat, ""), ""]
        ordered_subs = [s for s in sub_order.get(cat, []) if by_sub[cat].get(s)]
        leftover = [e for e in items if e.subsection not in ordered_subs] if ordered_subs else items
        if ordered_subs:
            for sub in ordered_subs:
                lines += [f"### {sub}", ""]
                for e in by_sub[cat][sub]:
                    lines.append(render_entry(e))
                lines.append("")
            if leftover:
                lines += ["### Other", ""]
                for e in leftover:
                    lines.append(render_entry(e))
                lines.append("")
        else:
            for e in items:
                lines.append(render_entry(e))
            lines.append("")

    lines += ["## Sources", "", "This catalog consolidates and deduplicates entries from:", ""]
    for name, url in [
        ("AbdelStark/awesome-typesafe-jev", "https://github.com/AbdelStark/awesome-typesafe-jev"),
        ("logicrw/awesome-jev-projects", "https://github.com/logicrw/awesome-jev-projects"),
        ("OmniJev/awesome-jev-gallery", "https://github.com/OmniJev/awesome-jev-gallery"),
        ("AppitStudio/awesome-jev", "https://github.com/AppitStudio/awesome-jev"),
        ("BeatAPI/awesome-jev", "https://github.com/BeatAPI/awesome-jev"),
        ("rupeshpoojary9/awesome-open-system-one", "https://github.com/rupeshpoojary9/awesome-open-system-one"),
        ("kydlikebtc/awesome-jev", "https://github.com/kydlikebtc/awesome-jev"),
        ("MrJev/awesome-jev", "https://github.com/MrJev/awesome-jev"),
        ("systemonemodels.org/examples/alternatives", "https://systemonemodels.org/examples/alternatives/"),
        ("r/LLMDevs — 287 Jev projects / top 20", "https://www.reddit.com/r/LLMDevs/comments/1wko2e5/i_reviewed_287_opensource_jev_projects_here_are/"),
    ]:
        lines.append(f"- [{name}]({url})")
    lines += [
        "",
        "Plus official TypeSafe pages, independent essays (Archer Hume, lilting.ch, Latent.Space, Learn Jev, etc.), Tier A/B open reproductions, a 2026-09-24 logicrw projects.json refresh for missing evidenced integrations, and the [r/LLMDevs 287-project / top-20 roundup](https://www.reddit.com/r/LLMDevs/comments/1wko2e5/i_reviewed_287_opensource_jev_projects_here_are/).",
        "",
        "Machine-readable dump: [`links.json`](links.json). Star cache: [`stars_cache.json`](stars_cache.json). Ingest map: [`SOURCES.md`](SOURCES.md). Counts: [`stats.txt`](stats.txt).",
        "",
        "## Contributing",
        "",
        "Prefer fixing upstream awesome lists; this file is a merge. When adding here: one factual line, working URL, System One / Jev relevance, no LayaAir-style name collisions, no empty stubs.",
        "",
        "Regenerate with `python3 build.py`. If `raw/` ingest artifacts are present they are merged first; otherwise the script reloads [`links.json`](links.json) and re-renders. Keep category mapping in `build.py` in sync with README sections.",
        "",
        "Within-section order is **pin/landmark first**, then **GitHub star count** (cached in [`stars_cache.json`](stars_cache.json)), then title — not pure editorial PageRank. Refresh stars: `python3 build.py --refresh-stars` (uses authenticated `gh api graphql` in batches; skips non-GitHub URLs).",
        "",
        "## License",
        "",
        "This compilation is dedicated to the public domain under [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/). Individual projects and linked content retain their own licenses and terms.",
        "",
    ]
    (OUT / "README.md").write_text("\n".join(lines), encoding="utf-8")

    sources_md = [
        "# Sources ingested", "", f"Ingest date: **{INGEST_DATE}** (America/Los_Angeles).", "",
        "| Source | URL | Artifact used |", "| --- | --- | --- |",
        "| AbdelStark/awesome-typesafe-jev | https://github.com/AbdelStark/awesome-typesafe-jev | README.md + resources.json |",
        "| logicrw/awesome-jev-projects | https://github.com/logicrw/awesome-jev-projects | README.md |",
        "| OmniJev/awesome-jev-gallery | https://github.com/OmniJev/awesome-jev-gallery | README.md |",
        "| AppitStudio/awesome-jev | https://github.com/AppitStudio/awesome-jev | README.md |",
        "| BeatAPI/awesome-jev | https://github.com/BeatAPI/awesome-jev | README.md + data/projects.json |",
        "| rupeshpoojary9/awesome-open-system-one | https://github.com/rupeshpoojary9/awesome-open-system-one | README.md |",
        "| kydlikebtc/awesome-jev | https://github.com/kydlikebtc/awesome-jev | README.md + catalog.json |",
        "| MrJev/awesome-jev | https://github.com/MrJev/awesome-jev | README.md |",
        "| systemonemodels.org alternatives | https://systemonemodels.org/examples/alternatives/ | HTML index |",
        "| seed-official / seed-essays / seed-tier / seed-lists | (manual) | Official docs, essays, Tier A/B models, list self-links |",
        "| seed-logicrw-refresh | https://logicrw.github.io/awesome-jev-projects/projects.json | 2026-09-24 evidenced projects missing from prior ingest |",
        "| Reddit r/LLMDevs top-20 roundup | https://www.reddit.com/r/LLMDevs/comments/1wko2e5/i_reviewed_287_opensource_jev_projects_here_are/ | Community review post (credit) |",
        "",
        "Normalization: strip trailing `/`, `.git`, `www.`, URL fragments/queries; exclude badge/shield hosts, issue templates, and known unrelated collisions (e.g. LayaAir).",
        "",
        "Ordering: within each category/subsection, pinned and landmark URLs stay first; remaining entries are sorted by GitHub stars (descending), then title. Star counts live in `stars_cache.json` (fetched via `gh api graphql`). Non-GitHub URLs are treated as unknown and sort after starred repos. Refresh with `python3 build.py --refresh-stars`. This is a star-count proxy, not a citation-graph PageRank.",
        "",
    ]
    (OUT / "SOURCES.md").write_text("\n".join(sources_md), encoding="utf-8")

    stats = [f"unique_links\t{n}", "", "by_category"]
    for cat in DISPLAY_ORDER:
        stats.append(f"{cat}\t{len(by_cat.get(cat, []))}")
    for cat in sorted(by_cat):
        if cat not in DISPLAY_ORDER:
            stats.append(f"{cat}\t{len(by_cat[cat])}")
    stats += ["", "by_subsection"]
    for cat in DISPLAY_ORDER:
        for sub in sub_order.get(cat, []):
            k = len(by_sub[cat].get(sub, []))
            if k:
                stats.append(f"{cat} / {sub}\t{k}")
        extra_subs = sorted(s for s in by_sub[cat] if s not in sub_order.get(cat, []))
        for sub in extra_subs:
            stats.append(f"{cat} / {sub or '(none)'}\t{len(by_sub[cat][sub])}")
    stats += ["", "by_source_appearance_count", "# (a link counted once per source that mentioned it)"]
    for s, c in sorted(source_counts.items(), key=lambda x: (-x[1], x[0])):
        stats.append(f"{s}\t{c}")
    stats += ["", f"json_count_matches_unique\t{len(links) == n}", ""]
    (OUT / "stats.txt").write_text("\n".join(stats), encoding="utf-8")
    print(f"Wrote {n} unique links")
    for cat in DISPLAY_ORDER:
        print(f"  {cat}: {len(by_cat.get(cat, []))}")
        for sub in sub_order.get(cat, []):
            k = len(by_sub[cat].get(sub, []))
            if k:
                print(f"    {sub}: {k}")
    print("top sources:", source_counts.most_common(15))

def cleanup_entries(entries: dict) -> None:
    drop = [nu for nu, e in entries.items() if (not e.title) or e.title.lower() in {"link", "here", "readme", "license"} or "camo.githubusercontent" in nu]
    for nu in drop:
        del entries[nu]
    bad_desc = re.compile(r"edit [`']?\.env|replace the placeholder|keep this file private|do not paste the key|git ignores it", re.I)
    for e in entries.values():
        if not e.description:
            e.description = f"{e.title} — System One / Jev related resource."
        if bad_desc.search(e.description or ""):
            e.description = f"{e.title} — System One / Jev related project."
        e.description = re.sub(r"\[([^\]]+)\]\((?!https?:)[^)]+\)", r"\1", e.description or "")
        e.description = re.sub(r"^[\s⭐★☆·•]+(?:—\s*)?", "", e.description or "").strip()

def main(argv: list[str] | None = None):
    argv = list(sys.argv[1:] if argv is None else argv)
    force_stars = "--refresh-stars" in argv
    entries = {}
    if raw_ready():
        ingest_raw(entries)
    else:
        load_links_json(entries)
    for row in SEEDS:
        add(entries, *row)
    cleanup_entries(entries)
    stars_map = ensure_stars(entries, force=force_stars)
    qpath = ROOT / ".stars_query.graphql"
    if qpath.exists():
        try:
            qpath.unlink()
        except OSError:
            pass
    write_outputs(entries, stars_map)

if __name__ == "__main__":
    main()

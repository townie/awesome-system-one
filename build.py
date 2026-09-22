#!/usr/bin/env python3
from __future__ import annotations
import json, re, collections
from pathlib import Path
from urllib.parse import urlparse, urlunparse

ROOT = Path(__file__).resolve().parent
RAW, OUT = ROOT / "raw", ROOT

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
("https://github.com/logicrw/awesome-jev-projects","Awesome Jev Projects","Commit-pinned radar of 479+ Jev projects across 17 domains.","Awesome lists & indexes","seed-lists"),
("https://github.com/OmniJev/awesome-jev-gallery","Awesome Jev Gallery","Gallery-style curated Jev / System One projects.","Awesome lists & indexes","seed-lists"),
("https://github.com/AppitStudio/awesome-jev","Awesome Jev (AppitStudio)","Curated awesome list of Jev ecosystem links.","Awesome lists & indexes","seed-lists"),
("https://github.com/BeatAPI/awesome-jev","Awesome Jev (BeatAPI)","Curated awesome list of Jev ecosystem links.","Awesome lists & indexes","seed-lists"),
("https://github.com/rupeshpoojary9/awesome-open-system-one","Awesome Open System One","Open-only System One models, benchmarks, calibration, and constrained decoding.","Awesome lists & indexes","seed-lists"),
("https://github.com/kydlikebtc/awesome-jev","Awesome Jev (kydlikebtc)","Catalog-driven bilingual awesome list with link checks.","Awesome lists & indexes","seed-lists"),
("https://github.com/MrJev/awesome-jev","Awesome Jev (MrJev)","Curated awesome list of Jev ecosystem links.","Awesome lists & indexes","seed-lists"),
("https://abdelstark.github.io/awesome-typesafe-jev","Awesome TypeSafe Jev (live site)","Browsable live directory for the AbdelStark list.","Awesome lists & indexes","seed-lists"),
("https://logicrw.github.io/awesome-jev-projects/en","Awesome Jev Projects (live site)","Searchable English radar UI for logicrw listings.","Awesome lists & indexes","seed-lists"),
("https://typesafeai.app","typesafeai.app","Independent directory of public Jev capabilities with evidence levels.","Awesome lists & indexes","seed-lists"),
("https://github.com/mizorewww/laya-coreml","laya-coreml","Local Laya typed decisions on Apple Core ML / Neural Engine; ~5 ms short decisions on M3 Max.","Open models & alternatives","seed-tier"),
("https://github.com/GodModeAI2025/JevCoreML","JevCoreML","Native macOS Core ML decision stack for kev-0.6b and Laya without Python or cloud at runtime.","Open models & alternatives","seed-tier"),
("https://github.com/FluidInference/FluidUse","FluidUse","Local computer use on Apple silicon using Laya + CUA-S1-FORMS via Accessibility API.","Open models & alternatives","seed-tier"),
("https://github.com/bespokelabsai/nimble","Bespoke Nimble","Open Jev recipe: Qwen3.5-9B LoRA on contrastive data with public eval suite vs Jev 1.13.","Open models & alternatives","seed-tier"),
("https://github.com/Zefan-Cai/Open-Jev","Open-Jev (ZefanCai)","Qwen3.5-2B/9B LoRA adapters with scalar decision heads and public dataset.","Open models & alternatives","seed-tier"),
("https://github.com/PsiACE/dohnuts","Dohnuts","0.8B text+image decision model; authors report 65.8% on 231 public JevBench tasks.","Open models & alternatives","seed-tier"),
("https://github.com/nico-martin/open-jev","open-jev (browser)","Browser TypeScript runtime for Kev/DeBERTa decisions via Transformers.js (WebGPU/WASM).","Open models & alternatives","seed-tier"),
("https://github.com/ipenywis/laya-ultrafast","Laya Ultrafast","Local MLX port of Jev Ultrafast with narrow-decision policy for browser tasks.","Open models & alternatives","seed-tier"),
("https://beatapi.io/awesome-jev","BeatAPI Awesome JEV gallery","Live gallery UI for the BeatAPI curated ≥50-star JEV project catalogue.","Awesome lists & indexes","seed-lists"),

]

INGEST_DATE = "2026-09-22 PT"

# Display order (newcomers: OS alternatives + use cases before the SDK dump).
DISPLAY_ORDER = [CAT_HOSTED, CAT_OS, CAT_USE, CAT_DOCS, CAT_EVALS, CAT_SDKS, CAT_LISTS, CAT_COMMUNITY]

LANDMARK_OS = [
    "https://github.com/jaredpalmer/kev",
    "https://github.com/NandhaKishorM/laya",
    "https://github.com/vinnylarouge/jevlike",
    "https://github.com/bespokelabsai/nimble",
    "https://github.com/TheoLeeCJ/SemIf",
    "https://github.com/bnsd55/jevmlx",
    "https://github.com/GodModeAI2025/JevCoreML",
    "https://github.com/mizorewww/laya-mlx",
    "https://github.com/mizorewww/laya-coreml",
]
PIN_EVALS = [
    "https://jevbench.dev",
    "https://github.com/fstandhartinger/jevbench",
    "https://jevals.com",
]
CATEGORY_OVERRIDE = {
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

def sort_key(e: Entry, pins: list[str] | None = None):
    return (pin_index(e.url, pins or []), e.title.lower())

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

def write_outputs(entries: dict) -> None:
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
        items.sort(key=lambda e: sort_key(e, pins))
        for sub, sub_items in by_sub[cat].items():
            sub_items.sort(key=lambda e: sort_key(e, pins))

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
    ]:
        lines.append(f"- [{name}]({url})")
    lines += [
        "",
        "Plus official TypeSafe pages, independent essays (Archer Hume, lilting.ch, Latent.Space, Learn Jev, etc.), and Tier A/B open reproductions cross-checked against the alternatives index.",
        "",
        "Machine-readable dump: [`links.json`](links.json). Ingest map: [`SOURCES.md`](SOURCES.md). Counts: [`stats.txt`](stats.txt).",
        "",
        "## Contributing",
        "",
        "Prefer fixing upstream awesome lists; this file is a merge. When adding here: one factual line, working URL, System One / Jev relevance, no LayaAir-style name collisions, no empty stubs.",
        "",
        "Regenerate with `python3 build.py`. If `raw/` ingest artifacts are present they are merged first; otherwise the script reloads [`links.json`](links.json) and re-renders. Keep category mapping in `build.py` in sync with README sections.",
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
        "",
        "Normalization: strip trailing `/`, `.git`, `www.`, URL fragments/queries; exclude badge/shield hosts, issue templates, and known unrelated collisions (e.g. LayaAir).",
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

def main():
    entries = {}
    if raw_ready():
        ingest_raw(entries)
    else:
        load_links_json(entries)
    for row in SEEDS:
        add(entries, *row)
    cleanup_entries(entries)
    write_outputs(entries)

if __name__ == "__main__":
    main()

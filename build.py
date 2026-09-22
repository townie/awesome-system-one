#!/usr/bin/env python3
from __future__ import annotations
import json, re, collections
from pathlib import Path
from urllib.parse import urlparse, urlunparse

RAW, OUT = Path("/workspace/awesome-system-one/raw"), Path("/workspace/awesome-system-one")

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

SECTION_MAP = [
    (re.compile(r"official|product and documentation", re.I), "Official"),
    (re.compile(r"research and writing|docs|essay|reference and reading|concepts|manifesto|blog|showcase", re.I), "Docs & essays"),
    (re.compile(r"open model|reproduction|alternative|local model|open.?source", re.I), "Open models & alternatives"),
    (re.compile(r"awesome|index|directory|gallery|catalog|radar", re.I), "Awesome lists & indexes"),
    (re.compile(r"sdk|client librar|integration|developer tool|tooling|mcp|constrained|structured decoding|calibration and selective|agent and developer|cli|pipeline|context|security|guardrail|data.?search|code navigation|model routing", re.I), "SDKs & tooling"),
    (re.compile(r"eval|benchmark|independent research|paper|calibration audit", re.I), "Evals & papers"),
    (re.compile(r"demo|application|workflow|game|robot|browser|creative|see jev at work", re.I), "Demos"),
    (re.compile(r"community|discord|show and tell|updates", re.I), "Community"),
]

def category_from_heading(heading: str):
    for rx, cat in SECTION_MAP:
        if rx.search(heading or ""): return cat
    return None

def infer_category(url, title, heading, hint=None):
    if hint: return hint
    c = category_from_heading(heading)
    if c: return c
    low = (url + " " + title).lower()
    if any(x in low for x in ("typesafe.ai", "docs.typesafe", "console.typesafe", "evals.typesafe", "discord.gg/typesafe")):
        return "Docs & essays" if any(x in low for x in ("blog", "manifesto")) else "Official"
    if any(x in low for x in ("arxiv.org", "benchmark", "eval", "jevals", "calibration", "paper")): return "Evals & papers"
    if "awesome" in low and "github.com" in low: return "Awesome lists & indexes"
    if any(x in low for x in ("laya", "nanojev", "semif", "openjev", "/kev", "nimble", "decider", "jevlike", "mini-jev", "jevmlx", "poorjev", "huggingface.co", "modernbert", "gliner", "setfit", "openthai", "reflex", "verdict", "litjev", "open-alternative", "pocketjev", "simple-jev", "simplejev")):
        return "Open models & alternatives"
    if any(x in low for x in ("sdk", "client", "mcp", "outlines", "instructor", "xgrammar", "guidance", "dspy")): return "SDKs & tooling"
    if any(x in low for x in ("discord", "x.com/typesafe", "linkedin.com/company/typesafe")): return "Community"
    if any(x in low for x in ("archerhume", "lilting.ch", "latent.space", "learnjev", "navinpai", "warmersun", "kevnu.com", "langchain.com/blog", "systemonemodels.org")): return "Docs & essays"
    if any(x in low for x in ("demo", "snake", "mario", "pokemon", "chess", "game", "play")): return "Demos"
    return "Demos"

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

RANK = {"Official":0,"Docs & essays":1,"Open models & alternatives":2,"Awesome lists & indexes":3,"SDKs & tooling":4,"Evals & papers":5,"Community":6,"Demos":7}

class Entry:
    __slots__ = ("url","title","description","category","sources")
    def __init__(self, url, title, description, category, source):
        self.url, self.title, self.description, self.category = url, title, description, category
        self.sources = {source}
    def merge(self, title, description, category, source):
        self.title = prefer_title(self.title, title)
        self.description = prefer_desc(self.description, description)
        if RANK.get(category, 9) < RANK.get(self.category, 9): self.category = category
        self.sources.add(source)

def add(entries, url, title, desc, cat, source):
    if should_exclude(url, title): return
    nu = normalize_url(url)
    if not nu: return
    desc = clean_desc(desc)
    if nu in entries: entries[nu].merge(title, desc, cat, source)
    else: entries[nu] = Entry(nu, title, desc, cat, source)


def parse_markdown_all_links(text, source, entries, default_cat="Demos"):
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
            add(entries, url, title, desc, infer_category(url, title, heading) or default_cat, source)

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
    cat_map = {"client-libraries-and-integrations":"SDKs & tooling","agent-and-developer-tooling":"SDKs & tooling","browser-agents":"Demos","applications-and-workflows":"Demos","games-and-robotics":"Demos","evaluations-and-independent-research":"Evals & papers","showcases-and-field-notes":"Docs & essays"}
    for cat in data.get("categories", []):
        hint = cat_map.get(cat.get("id"))
        for r in cat.get("resources", []):
            url, title = r.get("url") or "", r.get("name") or ""
            desc = r.get("description_markdown") or ""
            add(entries, url, title, desc, hint or infer_category(url, title, cat.get("name","")), source)

def parse_kyd_catalog(path, entries):
    data = json.loads(path.read_text()); source = "kydlikebtc/awesome-jev"
    kind_map = {"official-docs":"Official","sdk":"SDKs & tooling","integration":"SDKs & tooling","plugin":"SDKs & tooling","project":"Demos","alternative":"Open models & alternatives","benchmark":"Evals & papers","article":"Docs & essays","tutorial":"Docs & essays","snippet":"SDKs & tooling","video":"Docs & essays","discussion":"Community"}
    for r in data:
        url, title, desc = r.get("url") or "", r.get("title") or "", r.get("summary") or ""
        cat = kind_map.get(r.get("kind")) or infer_category(url, title, "")
        if r.get("official") and cat == "Demos": cat = "Official"
        add(entries, url, title, desc, cat, source)


def parse_beatapi_json(path, entries):
    data = json.loads(path.read_text()); source = "BeatAPI/awesome-jev"
    cat_map = {
        "browser-computer-use":"Demos","sdk-integrations":"SDKs & tooling","routing-optimization":"SDKs & tooling",
        "open-models":"Open models & alternatives","search-data":"SDKs & tooling","safety-review":"SDKs & tooling",
        "agent-workflows":"SDKs & tooling","interfaces":"Demos","developer-tools":"SDKs & tooling","domain-tools":"Demos",
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
        add(entries, m.group(1), m.group(2).strip() or m.group(1).rstrip("/").split("/")[-1], "", "Open models & alternatives", source)
    for m in re.finditer(r'href="(https://huggingface\.co/[^"#?\s]+)"', text):
        url = m.group(1); add(entries, url, url.rstrip("/").split("/")[-1], "", "Open models & alternatives", source)
    for m in re.finditer(r'href="(https://[^"#?\s]+)"[^>]*>', text):
        url = m.group(1)
        if "github.com" in url or "huggingface.co" in url: continue
        if any(x in url for x in ("simplejev.ai", "laya.convai", "systemonemodels")):
            add(entries, url, urlparse(url).netloc, "", "Open models & alternatives", source)

SEEDS = [
("https://typesafe.ai","TypeSafe AI","Official product site for System One models and Jev.","Official","seed-official"),
("https://docs.typesafe.ai","TypeSafe documentation","Guides, SDK references, patterns, cookbooks, and HTTP API.","Official","seed-official"),
("https://docs.typesafe.ai/concepts/system-one","System One concept","Author definition of System One models and the typed-decision interface.","Official","seed-official"),
("https://docs.typesafe.ai/introduction","Introduction","What Jev is and how System One differs from text-generation models.","Official","seed-official"),
("https://docs.typesafe.ai/introduction/quickstart","Quickstart","Shortest path from an API key to a typed decision.","Official","seed-official"),
("https://docs.typesafe.ai/primitives","Primitives","Choice, Score, and Noul: result shapes and when to use each.","Official","seed-official"),
("https://docs.typesafe.ai/api","HTTP API reference","Request/response contract for POST /v1/systemone.","Official","seed-official"),
("https://docs.typesafe.ai/confidence","Confidence","How confidence differs from answer probability as an architectural control.","Official","seed-official"),
("https://docs.typesafe.ai/patterns","Patterns","Confidence-gated routing, composite scoring, speculative fan-out, intent routing.","Official","seed-official"),
("https://docs.typesafe.ai/demos","Interactive demos","Official hands-on examples including the smart-home assistant.","Official","seed-official"),
("https://console.typesafe.ai","TypeSafe Console","Create keys and inspect live Jev requests.","Official","seed-official"),
("https://evals.typesafe.ai","Workflow evals","TypeSafe published workflows, model comparisons, and methodology.","Official","seed-official"),
("https://typesafe.ai/blog/introducing-system-one-models-and-jev","Introducing System One Models & Jev","Launch post naming the category, thesis, results, and limitations.","Docs & essays","seed-official"),
("https://typesafe.ai/manifesto","Manifesto","Case for machine-native intelligence built for software rather than conversation.","Docs & essays","seed-official"),
("https://typesafe.ai/blog/bitterest-lesson","The Bitterest Lesson","Why optimizing the wrong task can dominate gains from scale.","Docs & essays","seed-official"),
("https://typesafe.ai/blog/ai-too-good-to-be-true-too-bad-to-be-useful-typesafe-ai","AI: too good to be true, too bad to be useful","Argument for moving beyond preference-optimized chat models in automation.","Docs & essays","seed-official"),
("https://github.com/typesafe-ai/typesafe-sdk-js","JavaScript SDK","Official JS/TS client with inferred answer types.","SDKs & tooling","seed-official"),
("https://github.com/typesafe-ai/typesafe-sdk-python","Python SDK","Official sync/async Python client.","SDKs & tooling","seed-official"),
("https://github.com/typesafe-ai/system-one-adapter-python","System One Adapter","Drop-in Python adapter for OpenAI/Anthropic-compatible LLMs behind the typed interface.","SDKs & tooling","seed-official"),
("https://github.com/typesafe-ai/skills","TypeSafe Agent Skills","Official agent skill for designing TypeSafe workflows.","SDKs & tooling","seed-official"),
("https://github.com/typesafe-ai","TypeSafe GitHub org","Source repositories maintained by TypeSafe.","Official","seed-official"),
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
("https://github.com/fstandhartinger/jevbench","JevBench","Independent cross-model benchmark for typed decisions (accuracy, calibration, latency, cost).","Evals & papers","seed-tier"),
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

def main():
    entries = {}
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
    for row in SEEDS:
        add(entries, *row)

    drop = [nu for nu,e in entries.items() if (not e.title) or e.title.lower() in {"link","here","readme","license"} or "camo.githubusercontent" in nu]
    for nu in drop: del entries[nu]
    for e in entries.values():
        if not e.description:
            e.description = f"{e.title} — System One / Jev related resource."
    # scrub bad/setup descriptions
    bad_desc = re.compile(r"edit [`']?\.env|replace the placeholder|keep this file private|do not paste the key|git ignores it", re.I)
    for e in entries.values():
        if bad_desc.search(e.description or ""):
            e.description = f"{e.title} — System One / Jev related project."
        # strip relative markdown leftovers
        e.description = re.sub(r"\[([^\]]+)\]\((?!https?:)[^)]+\)", r"\1", e.description or "")
        e.description = re.sub(r"^[\s⭐★☆·•]+(?:—\s*)?", "", e.description or "").strip()


    ORDER = ["Official","Docs & essays","Open models & alternatives","Awesome lists & indexes","SDKs & tooling","Evals & papers","Demos","Community"]
    by_cat = collections.defaultdict(list)
    for e in entries.values(): by_cat[e.category].append(e)
    for cat in by_cat: by_cat[cat].sort(key=lambda x: x.title.lower())

    source_counts = collections.Counter()
    for e in entries.values():
        for s in e.sources: source_counts[s] += 1

    links = []
    for cat in ORDER:
        for e in by_cat.get(cat, []):
            links.append({"url":e.url,"title":e.title,"description":e.description,"category":e.category,"sources":sorted(e.sources)})
    for cat in sorted(by_cat):
        if cat in ORDER: continue
        for e in by_cat[cat]:
            links.append({"url":e.url,"title":e.title,"description":e.description,"category":e.category,"sources":sorted(e.sources)})

    n = len(links)
    (OUT/"links.json").write_text(json.dumps(links, indent=2, ensure_ascii=False)+"\n", encoding="utf-8")

    lines = ["# Awesome System One", "", "[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)", "",
        "> A consolidated catalog of **System One** / **Jev** resources: official TypeSafe docs and SDKs, independent essays, open model reproductions, SDKs & tooling, evaluations, demos, and community indexes.", "",
        "TypeSafe’s **Jev** is a hosted System One model that returns typed decisions (`Choice`, `Score`, `Noul`) with calibrated probabilities in one parallel pass—built for software control flow, not chat. This list merges every unique link found across multiple community awesome lists and living indexes (see [Sources](#sources)), deduplicated by normalized URL.", "",
        f"**{n} unique links** · Ingested **2026-09-22 PT** · License for this compilation: [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/) (linked projects keep their own licenses).", "",
        "## Contents", ""]
    for cat in ORDER:
        items = by_cat.get(cat, [])
        if not items: continue
        anchor = cat.lower().replace(" & ", "--").replace(" ", "-")
        lines.append(f"- [{cat}](#{anchor}) ({len(items)})")
    lines += ["- [Sources](#sources)", "- [Contributing](#contributing)", ""]
    for cat in ORDER:
        items = by_cat.get(cat, [])
        if not items: continue
        lines += [f"## {cat}", ""]
        for e in items:
            lines.append(f"- [{e.title}]({e.url}) — {e.description}")
        lines.append("")
    lines += ["## Sources", "", "This catalog consolidates and deduplicates entries from:", ""]
    for name, url in [
        ("AbdelStark/awesome-typesafe-jev","https://github.com/AbdelStark/awesome-typesafe-jev"),
        ("logicrw/awesome-jev-projects","https://github.com/logicrw/awesome-jev-projects"),
        ("OmniJev/awesome-jev-gallery","https://github.com/OmniJev/awesome-jev-gallery"),
        ("AppitStudio/awesome-jev","https://github.com/AppitStudio/awesome-jev"),
        ("BeatAPI/awesome-jev","https://github.com/BeatAPI/awesome-jev"),
        ("rupeshpoojary9/awesome-open-system-one","https://github.com/rupeshpoojary9/awesome-open-system-one"),
        ("kydlikebtc/awesome-jev","https://github.com/kydlikebtc/awesome-jev"),
        ("MrJev/awesome-jev","https://github.com/MrJev/awesome-jev"),
        ("systemonemodels.org/examples/alternatives","https://systemonemodels.org/examples/alternatives/"),
    ]:
        lines.append(f"- [{name}]({url})")
    lines += ["", "Plus official TypeSafe pages, independent essays (Archer Hume, lilting.ch, Latent.Space, Learn Jev, etc.), and Tier A/B open reproductions cross-checked against the alternatives index.", "",
        "Machine-readable dump: [`links.json`](links.json). Ingest map: [`SOURCES.md`](SOURCES.md). Counts: [`stats.txt`](stats.txt).", "",
        "## Contributing", "", "Prefer fixing upstream awesome lists; this file is a merge. When adding here: one factual line, working URL, System One / Jev relevance, no LayaAir-style name collisions, no empty stubs.", "",
        "## License", "", "This compilation is dedicated to the public domain under [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/). Individual projects and linked content retain their own licenses and terms.", ""]
    (OUT/"README.md").write_text("\n".join(lines), encoding="utf-8")

    sources_md = ["# Sources ingested", "", "Ingest date: **2026-09-22 PT** (America/Los_Angeles).", "",
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
        "", "Normalization: strip trailing `/`, `.git`, `www.`, URL fragments/queries; exclude badge/shield hosts, issue templates, and known unrelated collisions (e.g. LayaAir).", ""]
    (OUT/"SOURCES.md").write_text("\n".join(sources_md), encoding="utf-8")

    stats = [f"unique_links\t{n}", "", "by_category"]
    for cat in ORDER: stats.append(f"{cat}\t{len(by_cat.get(cat, []))}")
    for cat in sorted(by_cat):
        if cat not in ORDER: stats.append(f"{cat}\t{len(by_cat[cat])}")
    stats += ["", "by_source_appearance_count", "# (a link counted once per source that mentioned it)"]
    for s,c in sorted(source_counts.items(), key=lambda x: (-x[1], x[0])): stats.append(f"{s}\t{c}")
    stats += ["", f"json_count_matches_unique\t{len(links)==n}", ""]
    (OUT/"stats.txt").write_text("\n".join(stats), encoding="utf-8")
    print(f"Wrote {n} unique links")
    for cat in ORDER: print(f"  {cat}: {len(by_cat.get(cat, []))}")
    print("top sources:", source_counts.most_common(15))

if __name__ == "__main__":
    main()

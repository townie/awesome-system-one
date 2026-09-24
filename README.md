# Awesome System One

[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

> Typed decision models for software control flow — not chatbots. A consolidated catalog of **System One** / **Jev-style** resources.

**System One** models take unstructured state plus typed questions and return structured decisions (`Choice`, `Score`, `Noul`) with calibrated probabilities in one parallel pass. Software branches on those values. They do not generate chat replies.

TypeSafe’s **[Jev](https://typesafe.ai)** is the first *widely known* System One product — the launch that popularized this framing. Related ideas (typed classifiers, constrained decoding, calibrated probabilities, encoder decision heads) have a longer history; after Jev, the ecosystem filled in with [open reproductions](#open-source--local-alternatives), local/OS runtimes, [evals](#evals--papers), and community lists. This catalog merges those threads (see [Sources](#sources)). It does not claim Jev invented the underlying techniques.

**[JevBench](https://jevbench.dev/)** benches Jev, Jev-compatible open alternatives, and dual-brain (guide LLM + decision model) setups on interactive harnesses — starting with StarCraft II — measuring win/loss, task completion, and latency rather than a single typed-answer score.

Deduplicated by normalized URL across the ingested indexes.

Within each section (and subsection), **pins / landmarks stay first**; remaining items are ordered by **GitHub stars** (descending), then title. Stars are a practical proxy — not a full citation PageRank. Non-GitHub URLs (docs, HF, X, etc.) sort after starred repos. See [`stars_cache.json`](stars_cache.json).

**1340 unique links** · Ingested **2026-09-24 PT** · License for this compilation: [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/) (linked projects keep their own licenses).

### Start here

- [Hosted: TypeSafe Jev](#hosted-typesafe-jev) — Three docs entry points (home, primitives, HTTP API).
- [Open-source / local alternatives](#open-source--local-alternatives) — Kev, Laya, Jevlike, adapters, Core ML / MLX ports.
- [Use cases](#use-cases) — Routing, classification, extraction, guardrails, agents, search/rerank, and more.
- [JevBench](https://jevbench.dev/) — Interactive harness bench for Jev and open alternatives.
- [System One Models](https://systemonemodels.org) — Independent living docs for the category.
- [Jev alternatives index](https://systemonemodels.org/examples/alternatives) — Living index of open reproductions and cousins.

## Contents

- [Hosted: TypeSafe Jev](#hosted-typesafe-jev) (3)
- [Open-source / local alternatives](#open-source--local-alternatives) (103)
  - [Landmark projects](#landmark-projects) (12)
  - [Models & weights](#models--weights) (49)
  - [Runtimes, ports & servers](#runtimes-ports--servers) (12)
  - [Adapters & logit readers](#adapters--logit-readers) (18)
  - [Related classifiers & structured output](#related-classifiers--structured-output) (12)
- [Use cases](#use-cases) (374)
  - [Routing & triage](#routing--triage) (35)
  - [Classification](#classification) (18)
  - [Extraction & structured data](#extraction--structured-data) (16)
  - [Guardrails, safety & review](#guardrails-safety--review) (13)
  - [Agents, tools & harnesses](#agents-tools--harnesses) (16)
  - [Search, RAG & rerank](#search-rag--rerank) (11)
  - [Browser, computer use & OS](#browser-computer-use--os) (71)
  - [Games, robotics & simulation](#games-robotics--simulation) (54)
  - [Voice, mail & productivity](#voice-mail--productivity) (12)
  - [Markets & operations](#markets--operations) (12)
  - [Creative tools](#creative-tools) (6)
  - [Playgrounds & live demos](#playgrounds--live-demos) (29)
  - [Other applications](#other-applications) (81)
- [Docs & essays](#docs--essays) (65)
- [Evals & papers](#evals--papers) (86)
  - [Harnesses & live benches](#harnesses--live-benches) (6)
  - [Typed-decision benchmarks](#typed-decision-benchmarks) (58)
  - [Papers](#papers) (22)
- [SDKs & tooling](#sdks--tooling) (649)
  - [TypeSafe SDKs & gateways](#typesafe-sdks--gateways) (11)
  - [Community SDKs & clients](#community-sdks--clients) (98)
  - [MCP, skills & agent plugins](#mcp-skills--agent-plugins) (186)
  - [Integrations & data pipelines](#integrations--data-pipelines) (47)
  - [Other tooling](#other-tooling) (307)
- [Awesome lists & indexes](#awesome-lists--indexes) (55)
- [Community](#community) (5)
- [Sources](#sources)
- [Contributing](#contributing)

## Hosted: TypeSafe Jev

Three TypeSafe docs entry points. This catalog is an industry index, not a TypeSafe sitemap — cookbooks, SDKs, and essays live in the sections below.

- [Documentation](https://docs.typesafe.ai) — TypeSafe docs home — what Jev is and how System One differs from text generation.
- [Primitives](https://docs.typesafe.ai/primitives) — What each primitive is for and how to write criteria, including the 255-option cap on Choice and the 2-10 level range on Score.
- [HTTP API reference](https://docs.typesafe.ai/api) — The one endpoint, POST /v1/systemone, with the exact request and answer shapes for all three question types.

## Open-source / local alternatives

Run Jev-style `Choice` / `Score` / `Noul` locally: open models, MLX and Core ML ports, adapters over existing LLMs, and related typed-output libraries.

### Landmark projects

- [Kev](https://github.com/jaredpalmer/kev) — Apache-licensed, locally runnable Jev-style Choice, Score, and Noul models at 0.8B, 4B, and 9B, with released weights, training code, a System One-compatible server, frozen evaluation suites, and a playground. Its author reports a 0.822…
- [openjev](https://github.com/razorback16/openjev) — Apache-licensed System One decision server on DiffusionGemma 26B (vLLM NVIDIA + MLX Apple); Choice/Score/Noul, optional images.
- [Tev1-4B-experimental](https://huggingface.co/togethercomputer/Tev1-4B-experimental) — Open-weight Jev-inspired decision model finetuned from Qwen3.5-4B; Together serverless + HF weights.
- [Laya](https://github.com/NandhaKishorM/laya) — Convai Innovations decision head on ModernBERT/mmBERT; Choice/Score/Noul; ECE 0.081 after temperature fit; Apache-2.0.
- [Jevlike](https://github.com/vinnylarouge/jevlike) — 1.2K stars — An independent starter model that scores a changing list of text or visual options in one pass. [Source](https://github.com/vinnylarouge/jevlike/blob/94f5fd1b0b11d52bbdfdf4e0ee6aa96b568f8452/README.md)
- [Jev-Omni](https://huggingface.co/akhilaaa3/Jev-Omni) — Multimodal open System One classifier (text/image/audio/video) on Gemma 4 12B; Apache-2.0; author reports JevBench parity and <100ms on H100.
- [Bespoke Nimble](https://github.com/bespokelabsai/nimble) — , Data, model and recipe for an open Jev: Qwen3.5-9B plus LoRA on contrastive examples, with a 13-subset public evaluation suite scored against Jev 1.13.…
- [SemIf](https://github.com/TheoLeeCJ/SemIf) — Frozen-model logit reader for typed Choice on open models (e.g. Qwen3.5-4B); MIT.
- [jevmlx](https://github.com/bnsd55/jevmlx) — MIT-licensed local decision layer for Apple Silicon that scores constrained Boolean, enum, and multi-select fields from MLX model logits in one prefill, returns schema-valid JSON, and offers a System One-compatible endpoint and…
- [JevCoreML](https://github.com/GodModeAI2025/JevCoreML) — Native macOS Core ML decision stack for kev-0.6b and Laya without Python or cloud at runtime.
- [Laya-MLX](https://github.com/mizorewww/laya-mlx) — Native Apple Silicon (MLX) runtime for running the open Laya typed-decision model locally, non-autoregressive with no text generation.
- [laya-coreml](https://github.com/mizorewww/laya-coreml) — Local Laya typed decisions on Apple Core ML / Neural Engine; ~5 ms short decisions on M3 Max.

### Models & weights

- [NanoJev](https://github.com/TianyuCodings/NanoJev) — Studies independent Qwen-based typed decision heads, local serving, and game controllers with recorded comparisons. Project guide.
- [DeepOpen](https://github.com/deepopen-com/deepopen) — A router and presets over Convai's Laya checkpoints, packaged as its own engine.
- [LocalJev](https://github.com/githubnext/localjev) — 704 stars — A local Jev-compatible server with benchmarks across small local models. [Source](https://github.com/githubnext/localjev/blob/3f23e36e1a3bff46c7e83e8e3781d3512bc82021/README.md)
- [Splash](https://github.com/incoai/splash) — 578 stars — A local Apple Silicon inference engine oriented around decision-style models. [Source](https://github.com/incoai/splash/blob/f53d5ab543a7accdc332c060fd594a693f33f529/README.md)
- [Von](https://github.com/wfzyx/von) — Open local Choice, Noul, and Score model with public weights, training code, and a System One-shaped API. Benchmark comparisons are author-reported: its README gives a 91.23% accuracy headline without a matching result artifact in the…
- [Rizzo Flow](https://github.com/Rizzo-AI-Academy/rizzo-flow) — Local, open-model decision server that reads answer-token probabilities instead of generating text, with a Jev-compatible Choice, Score, and Noul API plus its own numeric primitive. Its authors explicitly make no quality-parity claim…
- [decider](https://github.com/Mapika/decider) — , Qwen3.5-2B fine-tune that emits typed decisions with calibrated probabilities in one pass.…
- [openjev-verdict-2.0](https://github.com/heman10x-ngu/openjev-verdict-2.0) — openjev-verdict-2.0 — System One / Jev related resource.
- [Reflex](https://github.com/kshetrajna12/reflex) — 110 stars — A small open decision model that recreates the JEV/System One interface on Qwen. [Source](https://github.com/kshetrajna12/reflex/blob/e21b3b23afdfeee7021a6604fa38f57e7ff5187f/README.md)
- [OpenJev](https://github.com/SiliconLabAI/OpenJev) — Approximates the System One contract on top of any logprob-capable model: a fixed answer space, each option scored independently, all questions in parallel.
- [openjev](https://github.com/siliconlabai/openjev) — openjev — System One / Jev related resource.
- [Open JEV](https://github.com/daseinlabs/open-jev) — One-pass option scoring on local Gemma 3 4B with HTTP server and System One API.
- [verdict-open-jev](https://github.com/heman10x-ngu/verdict-open-jev) — verdict-open-jev — System One / Jev related resource.
- [jevk5](https://github.com/allebee/jevk5) — An open model that answers the same typed questions Jev answers — yes/no, choice, score — in one forward pass with zero generated tokens (~13 ms on an H100), plus a head-to-head harness that puts Jev and the open…
- [litjev](https://github.com/zhengxuyu/litjev) — Independent Qwen reproduction serving /v1/systemone with Choice/Score/Noul + MMLU-Pro.
- [Open Jev (intikhab49)](https://github.com/intikhab49/open-jev-typed-decision-engine) — A 150M encoder trained to answer typed questions in one pass, with the training notebook written to run on a free GPU.
- [OpenThai-SystemOne](https://github.com/iapp-technology/openthai-systemone) — Open (Apache-2.0) Thai and English System One decision model, 0.8B with a 256-way slot head.
- [solar-mini4-jev](https://github.com/hunkim/solar-mini4-jev) — A drop-in wrapper that exposes Upstage \\Solar Mini4\\ through the TypeSafe Jev System One API shape.
- [open-jev](https://github.com/JoshuaSP/open-jev) — , Typed JSON inference with DiffusionGemma: fixed JSON, parallel decisions. [![Code](https://img.shields.io/github/stars/JoshuaSP/open-jev?style=flat-square&logo=github&label=Code&color=181717)](https://github.com/JoshuaSP/open-jev)
- [system-one-open](https://github.com/mithalouni/system-one-open) — Open replica of TypeSafe Jev: typed calibrated decisions in one forward pass on Gemma 4 E2B / Gemma 3 270M (Modal).
- [openjev (zhihz)](https://github.com/zhihz/openjev) — , Local bilingual probability decisions from context, questions and candidate answers. [![Code](https://img.shields.io/github/stars/zhihz/openjev?style=flat-square&logo=github&label=Code&color=181717)](https://github.com/zhihz/openjev)
- [JevBERT](https://github.com/hawkymisc/typed-decision-bert) — A local server that speaks Jev's `/v1/systemone` shape from a BERT encoder, with a numbered account of every request it refuses that Jev might accept.
- [OpenJevPro](https://github.com/zhangcy122/OpenJev) — Asks an Ollama or OpenAI-compatible model to write a likelihood score per candidate, then softmaxes them with a fixed temperature. PolyForm Noncommercial, not an open-source licence.
- [Dohnuts](https://github.com/PsiACE/dohnuts) — , 0.8B text-and-image decision model trained on one RX 7900 XTX; authors report 65.8% accuracy on 231 public JevBench tasks; Apache-2.0 code and non-commercial CC BY-NC-SA 4.0 weights.…
- [Jev on a laptop](https://github.com/rorshopping/jev-on-a-laptop) — , Unofficial study of Jev-style parallel typed decisions on stock 1.5B to 8B models on Apple Silicon, with benchmarks.…
- [tev1](https://github.com/togethercomputer/tev1) — Together AI open recipe + training example for Tev1-4B-experimental (Jev-inspired decision LoRA on Qwen3.5-4B).
- [stuntd](https://github.com/bladedevoff/stuntd) — Local proxy that learns your app's typed LLM decisions and answers them with a Laya head. Jev and OpenAI compatible.
- [jevbetter](https://github.com/olanotolu/jevbetter) — , One-pass scorer over a variable option list: hashed n-gram encoder, rival-aware attention, gated head, temperature scaling.…
- [Luce](https://github.com/scienthoon/luce) — Open recipe for Jev-style decision models: a task description, an LLM teacher that writes the data, then LoRA plus a decision head on Qwen3-4B-Base returning calibrated choice, score, and boolean probabilities on a 12 GB GPU; the README…
- [lev](https://github.com/franckverrot/lev) — Jev-style decision model on LiquidAI LFM2.5-350M with a TypeSafe-compatible /v1/systemone server.
- [qwen-rlcd](https://github.com/shamazharikh/qwen-rlcd) — , Choice, Score and Noul on Qwen3.5-0.8B, the smallest decoder-based reproduction.…
- [reflex](https://github.com/kaustav1996/reflex) — A coding agent and personal assistant built on the Pi coding agent. Jev checks every tool call, turn and voice transcript, and code decides what happens next: allow, ask or block an action, which model tier to use,…
- [stuntdouble](https://github.com/ReallyArtificial/stuntdouble) — Drop-in /v1/systemone proxy that shadows Jev with local decision models (Kev, Laya) and reports whether you can swap
- [jqv](https://github.com/Octalab-Inc/jqv) — Stock Qwen3 decision API: shared-state prefill, choice-token readout, temperature-calibrated probabilities, TypeSafe-compatible.
- [NanoJev](https://github.com/chenyangcun/NanoJev) — A minimal nanoGPT-style replica of Jev: parallel decisions, dynamic candidates, and an end-to-end training pipeline.
- [open-jev-tinfoil](https://github.com/VitaDAO/open-jev-tinfoil) — Attested CPU serving for the open Jev DeBERTa typed-decision model.
- [Codiv](https://codiv.ai) — Hosted inference for open System One models; serves OpenJev through a Jev-compatible API.
- [Codiv API](https://api.codiv.ai) — Jev-compatible base URL for Codiv-hosted OpenJev (point TYPESAFE_BASE_URL here).
- [Laya](https://laya.convaiinnovations.com) — A 421M non-autoregressive System One decision engine with RLCD-trained calibrated probabilities and multilingual support.
- [LFM2.5-2.6B-RLCD](https://huggingface.co/monotykamary/LFM2.5-2.6B-RLCD) — , RLCD-style fine-tune of Liquid AI's LFM2.5-2.6B for typed decisions. [![Model](https://img.shields.io/badge/%F0%9F%A4%97%20Model-8B5CF6?style=flat-square)](https://huggingface.co/monotykamary/LFM2.5-2.6B-RLCD)
- [LFM2.5-350M-RLCD](https://huggingface.co/notnotsamuel/LFM2.5-350M-RLCD) — , 350M-parameter RLCD-style decision model, the smallest open attempt. [![Model](https://img.shields.io/badge/%F0%9F%A4%97%20Model-8B5CF6?style=flat-square)](https://huggingface.co/notnotsamuel/LFM2.5-350M-RLCD)
- [NanoJev](https://huggingface.co/C-Tianyu/NanoJev) — A 0.6B open replica of the JEV interface with parallel decisions and a training pipeline.
- [nanojev (single-file)](https://github.com/novvoo/nanojev) — A single-file, MIT-licensed educational implementation with a small serving UI and HTTP API.
- [OpenJev (weights)](https://huggingface.co/openjev/openjev) — HF decision-model checkpoint for OpenJev; zero-shot classification / calibrated option probabilities; CC-BY-NC-4.0.
- [ProtectAI prompt-injection DeBERTa v2](https://huggingface.co/protectai/deberta-v3-base-prompt-injection-v2) — , 184M DeBERTa returning a binary injection probability, the BERT-style encoder guardrail HN engineers mapped Jev onto.…
- [sales-conversion-model-reinf-learning](https://huggingface.co/DeepMostInnovations/sales-conversion-model-reinf-learning) — sales-conversion-model-reinf-learning — System One / Jev related resource.
- [system-one-mini](https://huggingface.co/DavidHatley/system-one-mini) — , DistilBERT-sized System One shape, a floor for how small the idea can go. [![Model](https://img.shields.io/badge/%F0%9F%A4%97%20Model-8B5CF6?style=flat-square)](https://huggingface.co/DavidHatley/system-one-mini)
- [system-one-qwen3.5-4b-scorer](https://huggingface.co/pngwn/system-one-qwen3.5-4b-scorer) — , Qwen3.5-4B base trained as a Score-style rubric rater. [![Model](https://img.shields.io/badge/%F0%9F%A4%97%20Model-8B5CF6?style=flat-square)](https://huggingface.co/pngwn/system-one-qwen3.5-4b-scorer)
- [Tev1 on Together serverless](https://api.together.ai/models/together/Tev1-4B-experimental) — Hosted Tev1-4B-experimental endpoint on Together AI ($0.042/M input, $0/M output per announcement).

### Runtimes, ports & servers

- [djev-run](https://github.com/taeold/djev-run) — Serves DiffusionGemma-Jev behind a compatible API on Cloud Run, with a small game demo on top.
- [Laya Node Runtime](https://github.com/receptron/laya) — 195 stars — A Node.js and TypeScript runtime for the open Laya JEV-compatible decision model. [Source](https://github.com/receptron/laya/blob/6478649e723122ca24bbf5fb69ed1010023c9750/src/laya.ts)
- [openjev-sglang](https://github.com/ekzhang/openjev-sglang) — Implements a Jev-shaped HTTP decision API using Qwen and SGLang; independent model behavior and unspecified code licensing. Project guide.
- [JEV Visual](https://github.com/hr98w/jev-visual) — Educational multimodal Jev-like inference on Apple Silicon (MLX) with browser UI and demos.
- [jeff](https://github.com/logan-markewich/jeff) — Self-hosted GLiFormer 400M server for Choice, Score, and Noul through a Jev-compatible API, with public benchmark code and per-item results. Its documented JevBench comparison finds weaker accuracy than Jev on reasoning-heavy items;…
- [djev-spark](https://github.com/mmastrac/djev-spark) — 168 stars — A DGX Spark container recipe for running DiffusionGemma NVFP4 structured decisions. [Source](https://github.com/mmastrac/djev-spark/blob/1444f3e927f83ba508e5b28a4fd4fdd9ecd0976b/README.md)
- [Laya Ultrafast](https://github.com/ipenywis/laya-ultrafast) — , Local MLX port of Jev Ultrafast with a redesigned narrow-decision policy; authors report five successful Google Flights runs in 7.5 to 12.1 seconds on an M1 Max.…
- [djev](https://github.com/mmastrac/djev) — , DiffusionGemma structured-read server that pins fixed answer text and denoises answer slots into per-option probabilities through Jev's API; requires the linked vLLM PR branch.…
- [jevfire](https://github.com/kikoncuo/jevfire) — Parallel typed decisions for CUDA LLMs via vLLM shared-prefix batching.
- [open-jev](https://github.com/nico-martin/open-jev) — Runs independent Kev and DeBERTa typed-decision models locally through Transformers.js, with browser WebGPU/WASM support; does not use official Jev weights. Project guide.
- [open-spark-jev](https://github.com/abhishek085/open-spark-jev) — Local decision models on Qwen3 sized for NVIDIA DGX Spark.
- [vLLM PR #57250 — DiffusionGemma structured mode](https://github.com/vllm-project/vllm/pull/57250) — Prototype structured-generation / Jev-like canvas read for DiffusionGemma with sample /v1/systemone interposer.

### Adapters & logit readers

- [Simple Jev](https://github.com/featherless-ai/simple-jev) — Apache-licensed local server that scores Choice, Score, and Noul with open-model logits; tokenizer support and decision calibration vary by model.
- [AnyJev](https://github.com/nokia-applied-research/AnyJev) — Turns any open-weights LLM into a typed decider by averaging the option logits over permutations and subtracting a label-free prior, so the answer barely moves when you reorder the options.
- [Open-Jev (ZefanCai)](https://github.com/Zefan-Cai/Open-Jev) — , Released Qwen3.5-2B and 9B LoRA adapters with scalar decision heads and a public dataset; the 9B model answers 179 of 231 public JevBench tasks correctly in the authors' evaluation.…
- [LLM2Jev](https://github.com/Yinsongxu/LLM2Jev) — Apache-licensed local toolkit that reads causal-model logits for Choice, Score, and Noul answers through Transformers or SGLang, with a System One-shaped HTTP endpoint, web and Snake demos, and shared-prefix cache measurements. Its…
- [mini-jev](https://github.com/r-ms/mini-jev) — Frozen Qwen3-4B next-token logit interface for Choice/Noul; not a full reproduction.
- [Open Alternative to Jev](https://github.com/ikermoel/open-alternative-jev) — Apache-licensed Python library that reads option-token probabilities from open models through Transformers or vLLM, with packed and separate question modes, temperature scaling, benchmark scripts, and raw result files; its measurements…
- [OpenSourceJev](https://github.com/sabeel111/OpenSourceJev) — Research experiment in local System One decisions through llama.cpp logits projection on consumer hardware.
- [choosekit](https://github.com/NotXf1le/choosekit) — Scores a finite set of choices with a model you already run in llama.cpp and returns a typed decision with a probability distribution.
- [fastjev](https://github.com/chengyongru/fastjev) — Independently maintained SemIf fork: self-hosted semantic decisions via Torch, vLLM, MLX, llama.cpp, and optional HTTP API.
- [poorjev](https://github.com/rupeshpoojary9/poorjev) — Open, local reproduction of the Choice/Score/Noul interface on commodity zero-shot NLI models with temperature scaling and conformal abstention; ships a reproducible calibration eval (ECE 0.170 to 0.071 on its own small labelled set,…
- [open-bonsai-jev](https://github.com/NicolaiLassen/open-bonsai-jev) — openjev's mechanism, Bonsai's weights: typed decisions read straight from one forward pass of a 1.75-bit 27B model. Credit to TheoLeeCJ (SemIf/OpenJev) and PrismML.
- [semif-go](https://github.com/wnzn/semif-go) — Go System One adapter over llama.cpp: Choice/Noul/Score from next-token option probs; multimodal state (text/image/audio/video).
- [PocketJev](https://github.com/NullPo-jp/PocketJev) — SwiftUI on-device multiple-choice tool reading next-token logits on iPhone.
- [Build Your Own JEV Locally: Run a 100% Private AI Agent on Your Machine](https://medium.com/coding-nexus/build-your-own-jev-locally-run-a-100-private-ai-agent-on-your-machine-bb98126d394a) — Despite the title, this does not run Jev. It builds a Jev-like decision engine from an open LLM using constrained next-token scoring.
- [Kev family release](https://github.com/jaredpalmer/kev/releases/tag/kev-family) — Packaged Kev-0.8B / 4B / 9B adapters + heads on Qwen3.5 with locked-test numbers and checksums.
- [Parallel Constrained Decision Engine](https://huggingface.co/spaces/drinkmoonshine/parallel-constrained-decoding) — , Live demo of the Qwen-2.5-1B-RLCD approach: KV-cache broadcast, logit slicing per candidate, 100 percent schema validity.…
- [Qwen-2.5-1B-RLCD](https://huggingface.co/harshatheg/Qwen-2.5-1B-RLCD) — , Qwen2.5-1.5B fine-tune plus parallel constrained decoding; all schema fields scored in one broadcast prefill, 5.6x to 7x faster on Apple Silicon.…
- [simplejev.ai](https://simplejev.ai) — Hosted/open library giving HF models Jev-style structured decision output.

### Related classifiers & structured output

- [dspy](https://github.com/stanfordnlp/dspy) — Programming (not prompting) LMs with typed Signatures — closest open typed-question analogue.
- [Outlines](https://github.com/dottxt-ai/outlines) — Structured generation that constrains a model to a grammar, regex, or JSON schema, so invalid output is impossible.
- [Instructor](https://github.com/567-labs/instructor) — Structured outputs from LLMs via typed schemas, with validation and retries; a common baseline for typed decisions today.
- [GLiNER](https://github.com/urchade/GLiNER) — Zero-shot NER with labels at inference time — extraction-shaped cousin of typed decisions.
- [setfit](https://github.com/huggingface/setfit) — Few-shot Sentence Transformer classification without prompting.
- [ModernBERT](https://github.com/AnswerDotAI/ModernBERT) — Modernized BERT encoder — baseline backbone for many open decision heads.
- [OpenJEV Verdict 2.0](https://github.com/Heman10x-NGU/openJev-verdict-2.0) — A 151M non-autoregressive decision model on ModernBERT with calibrated uncertainty and an in-browser WebGPU playground. Its LICENSE is not recognised as the Apache 2.0 its badge claims.
- [rlcd-modernbert-151m](https://github.com/Heman10x-NGU/Verdict-open-jev) — , Encoder-side reproduction: GLiClass ModernBERT base retrained for calibrated label probabilities.…
- [OpenDecision](https://github.com/deepanwadhwa/OpenDecision) — Zero-shot NLI decision engine on ModernBERT-large (~400M) with Choice/Noul/Score vocabulary.
- [Jev Local](https://github.com/Argos1111/jev_local) — A local `/v1/systemone` server with two backends: an LFM model zero-shot, and a fine-tuned ModernBERT-Ja cross-encoder. Japanese documentation.
- [typed-decisions](https://github.com/kotoba-lang/typed-decisions) — Jev-shaped Choice/Score/Noul model on ModernBERT, DeBERTa, and LLaDA-MoE with measured latency, accuracy, and calibration.
- [Laya](https://huggingface.co/convaiinnovations/laya) — , ModernBERT-large with RLCD-trained decision heads: Choice, Score and Noul in one 38 ms pass. [![Model](https://img.shields.io/badge/%F0%9F%A4%97%20Model-8B5CF6?style=flat-square)](https://huggingface.co/convaiinnovations/laya)…

## Use cases

Apps, demos, and TypeSafe cookbooks/patterns grouped by decision shape.

### Routing & triage

- [Jev Chat Assistant](https://github.com/jev-chat/jev-chat-jarvis) — , Android chat overlay where Jev judges intent and ranks replies while a separate LLM drafts them; the author reports roughly one-second judgments and device-tested WeChat, QQ, X and Lark adapters.…
- [Crush Monitor](https://github.com/FerryCorleone/crush-monitor) — `Open source` · `Free source build` · `BYOK`. Local WeChat-style chat analyzer: TypeSafe Jev labels emotion/intent, scores affinity, and rates replies (BYOK). Project guide.
- [hyperedit](https://github.com/kevinbadi/hyperedit) — An AI video editor routing an editing instruction to an operation, a target clip and a track, with a keyword router as fallback.
- [332_lab-jev-chat](https://github.com/Liyucheng1997/332_lab-jev-chat) — The Windows app reads visible WeChat chat text via UI Automation or local OCR, uses Jev for structured intent judgment, and optionally uses DeepSeek to generate three copyable reply suggestions.
- [lurk](https://github.com/getanyapi-com/lurk) — Self-hostable Reddit buyer-intent finder that uses Jev to judge every post and comment a scan reads.
- [Jevmail](https://github.com/fazlerocks/jevmail) — Read-only Gmail triage that sorts an inbox into five trays with an urgency score, running locally through a gateway key.
- [JevIntent](https://github.com/Nisaka520/JevIntent) — It is a FkWeChat plugin that analyzes a long-pressed WeChat text message with the Jev model for intent, emotion, urgency and reply posture and shows the result in local Toasts.
- [muse-jev-playbook](https://github.com/Bodila51/muse-jev-playbook) — Jev decision layer for Muse: a fast, cheap TypeSafe AI gate before expensive agent work — confidence policy, recipes, reference router, honest measurement.
- [sabi](https://github.com/vizuh/sabi) — Adaptive inference scheduling for AI agents — per-round model, effort and provider routing for coding harnesses: a Command Code mod or a local OpenAI-compatible proxy.
- [claude-jev](https://github.com/0x7067/claude-jev) — Claude Code plugin: Jev for rule checks, verbatim compaction, and prompt routing
- [jev-bigquery-cloudrun](https://github.com/jeffonelson/jev-bigquery-cloudrun) — Classify support tickets in BigQuery with Jev and Cloud Run
- [Jev_Ontology](https://github.com/dagfinndybvig/Jev_Ontology) — We built a working MVP that pairs an LLM-authored ontology with Jev's calibrated classification, tested it against the live Jev API on 78 unique tickets across 5 sessions (86 classifications -- Session 4 re-runs…
- [jev-model-router](https://github.com/satviksinha/jev-model-router) — Model router for Claude Code using Jev
- [jev-shield](https://github.com/vmendes90/jev-shield) — A Chrome ad-filtering extension that uses Jev to assess promotional intent in feed elements.
- [jev-trip](https://github.com/liaoyuhua/jev-trip) — Jev Trip is an explainable day-trip planner. The LLM plans ahead; Jev chooses and checks. Deterministic code handles route facts, time calculations, validation, and versioning.
- [jev-claw](https://github.com/trietphan/jev-claw) — Typed model routing for OpenClaw agents, powered by TypeSafe Jev
- [jev-for-engineers](https://github.com/Foadsf/jev-for-engineers) — Eight mechanical and electrical engineering experiments using Jev for task routing, log checks and component selection.
- [jev-smart-router](https://github.com/rmosleydb/jev-smart-router) — JEV Smart Router — a Databricks App that uses TypeSafe JEV to pick which model answers each message, then runs inference on the chosen Databricks Foundation Model API endpoint.
- [JevEmon](https://github.com/daniel4x/JevEmon) — Verified milestones so far: Jev can leave the Player's House, cross Pallet Town, deliver itself through Route 1 (fighting and winning any wild encounters along the way), and reach Viridian City. Further legs of the journey (Oak's…
- [JevSeek](https://github.com/morcoan/JevSeek) — Local coding workspace and agent decoupling tool routing via Jev from detailed argument generation via DeepSeek.
- [ha-conversation-jev](https://github.com/luxus/ha-conversation-jev) — A Home Assistant conversation integration routing simple lighting commands to services and other requests to Grok.
- [jev-agent-hooks](https://github.com/onlyjq04/jev-agent-hooks) — TypeSafe Jev hooks for Claude Code, Codex and pi: per-turn skill suggestion and subagent model routing
- [jev-codex-router-skill](https://github.com/455-dIAO/jev-codex-router-skill) — Portable Codex Skill for Jev model and reasoning-effort routing, with safe installation and Chinese usage guides
- [jev-route](https://github.com/mcftira/jev-route) — Run it. Log it. Distill it. Own it.
- [jev-lab](https://github.com/Pasblinn/jev-lab) — Open lab: Jev (TypeSafe System One) routing in front of Claude Code - measured bugs, patch, and a hard fallback with alerts
- [jev-triage](https://github.com/ccai40359-wq/jev-triage) — Millisecond-class test-failure triage for coding agents: RETRY / FIX_CODE / FIX_ENV, powered by TypeSafe Jev.
- [tc39-atlas](https://github.com/hemanth/tc39-atlas) — Interactive semantic explorer and taxonomy for TC39 proposals. Applies TypeSafe AI System One (Jev) to classify ECMAScript proposals across adoption pathways, cognitive overhead, web-compatibility risk, and foundational intent archetypes.
- [jev-gateway](https://github.com/TexasOct/jev-gateway) — Session-aware OpenAI-compatible model-routing gateway powered by JEV
- [JevZero](https://github.com/jayozer/jevzero) — `Open source` · `Free source build` · `BYOK`. Local Gmail triage with TypeSafe Jev: review proposed labels, apply with receipts, and undo. Project guide.
- [BTK audit studies](https://boringtoolskit.com/blog/seo-audit-cost-2026) — Production SEO studies driven by Jev striking-distance triage: 1,204 pages judged per run, 4,816 typed judgments in under 3 minutes, $0.0048 per 12-query batch (jev-1.13.0).
- [Confidence-gated routing](https://docs.typesafe.ai/patterns/confidence-routing) — Treat confidence as a second axis: the answer tells you what, the confidence tells you whether to act on it.
- [Intent routing](https://docs.typesafe.ai/patterns/intent-routing) — Classify an incoming request and route it to the cheapest adequate handler: deterministic code, a specialist LLM, or a person.
- [Jev Agent Skill Router](https://mrjev.com/projects/godsboy-jev-agent-skill-router) — Jev Agent Skill Router — System One / Jev related resource.
- [Patterns](https://docs.typesafe.ai/patterns) — Confidence-gated routing, composite scoring, speculative fan-out, and intent routing.
- [Read](https://mrjev.com/projects/gargpratyush-jev-router) — Read — System One / Jev related resource.

### Classification

- [Jev X Sentiment Analysis](https://github.com/brainstormity/Jev-X-Sentiment-Analysis) — Crypto terminal that reads up to 1,000 posts about a ticker alongside market and funding data and turns them into a buy, sell, hold, or take-profit call. No license file at the time of writing. Not financial advice.
- [Jev Column Race](https://github.com/goodrahstar/jev-column-race) — `Open source` · `Free source build` · `BYOK`. Labels 1,000 app reviews in parallel: TypeSafe Jev typed questions vs Gemini JSON, with free replay (hosted or local). [Try app](https://jev-column-race.vercel.app) · [Project…
- [Transcript Lens](https://github.com/sensahin/transcript-lens) — `Open source` · `Free source build` · `BYOK`. Next.js (Türkçe UI) YouTube transcript explorer: TypeSafe Jev classifies blocks for kind/value/signals without rewriting text. Project guide.
- [Jev Mail Classifier](https://github.com/parth-kp/jev-mail-classifier) — `Open source` · `Free source build` · `BYOK`. Classifies IMAP inbox messages with Jev category judgments, then tags, moves, flags, or notifies from a local Textual TUI and CLI. [Project…
- [typesafe-jev-workflow](https://github.com/GiesN/typesafe-jev-workflow) — An async LangGraph example that classifies mocked emails as invoice-related or general.
- [jev-papers](https://github.com/stas4000/jev-papers) — 1,000 arXiv AI papers classified with one Jev decision each, checked against an LLM judge. Open rebuild, MIT.
- [work-with-jev](https://github.com/Adkid-Zephyr/work-with-jev) — Work with Jev is a local-first message classifier that uses Jev to sort work messages into urgent, to-do, worth-reading, and skippable groups with cross-chat to-do management and Feishu and WeCom adapters.
- [let-jev-speak](https://github.com/suidouble/let-jev-speak) — TypeSafe's \`/v1/systemone\` endpoint classifies text — it returns a \`choice\`, a \`score\`, or a probability. It does not generate prose. This library makes it generate prose anyway: every word of the answer is a separate \`choice\`…
- [hfjev](https://github.com/hemanth/hfjev) — Classify Hugging Face datasets across typed semantic dimensions with TypeSafe Jev System One. Auto-adapts evaluation rubrics to dataset domains (reviews, news, LLM tuning, support) and classifies rows in a single parallel System One…
- [jev-prompt-optimization](https://github.com/j341nono/jev-prompt-optimization) — automatically optimizing the instructions and decision criteria of TypeSafe Jev Choice from labeled data
- [jevsome-projects](https://github.com/ozers/jevsome-projects) — A Jev project directory and discovery pipeline that stores integration evidence and can use Jev for classification.
- [leadgenrationaivoiceagent](https://github.com/sumitrevolt/leadgenrationaivoiceagent) — An experimental TypeSafe module in a marketing and voice platform chooses specialization labels for agent roles.
- [Jev Call Screener](https://github.com/SuchintK/jev-call-screener) — `Open source` · `Free source build` · `BYOK`. Self-hosted call screening: TypeSafe Jev classifies caller transcripts; Go policy forwards or rejects (Twilio adapter; fail-open defaults). [Project…
- [Cookbook: Classification using confidence](https://docs.typesafe.ai/cookbooks/classification_using_confidence) — Classifies annual reports into 75 industry groups, then reads the answer's own confidence to decide whether to report that group or the broader division above it.
- [Hierarchical classification](https://docs.typesafe.ai/cookbooks/hierarchical_classification) — Walks deep patent, retail, biomedical and source-code taxonomies with a parallel beam search over Choice probabilities.
- [Noul self-consistency](https://docs.typesafe.ai/cookbooks/consistency_noul_cookbook) — Routes uncertain probabilities to human review while keeping the underlying noul values visible rather than collapsing them to a label.
- [Read](https://mrjev.com/projects/kyotofin-tax-doc-classifier) — Read — System One / Jev related resource.
- [Structure recovery](https://docs.typesafe.ai/cookbooks/autoformat) — Reconstructs Markdown from plain text that lost its formatting, in two requests: one restitches hard-wrapped lines, one classifies every block.

### Extraction & structured data

- [jev-seo](https://github.com/AgriciDaniel/jev-seo) — \\PDF: how the audit was made, the scorecard and the priorities\\
- [polar\_llama](https://github.com/pnthn-ai/polar_llama) — A Polars library for parallel provider inference that also calls Jev per row as Noul, Choice, and Score questions, or as one typed contract over a document.
- [duckdb-jev](https://github.com/colliber/duckdb-jev) — A DuckDB extension that calls Jev from SQL and returns answers as ENUM, numeric, or STRUCT types.
- [ComfyUI-Jev](https://github.com/hndrr/ComfyUI-Jev) — Custom nodes for using Jev's text interpretation and judgments in ComfyUI. Use natural-language instructions to select candidates, evaluate conditions, score text, or extract numbers, then pass the results to other nodes. Jev judgments…
- [JEV Document Classification](https://github.com/Charlyhno-eng/jev-document-classification) — `Open source` · `Free source build` · `BYOK`. Local-first folder filer: TypeSafe Jev (Vercel AI Gateway) chooses category/confidentiality/injection/subject; audit preview and undo. [Project…
- [jevsql](https://github.com/sarathi-aiml/jevsql) — Text-to-SQL where the model never writes SQL — typed, calibrated decisions (TypeSafe Jev) + code-assembled queries
- [sqlite3-jev](https://github.com/mattn/sqlite3-jev) — SQLite C extension enabling TypeSafe Jev judgments as native SQL functions for semantic scoring and choices.
- [jev-information-extraction](https://github.com/abhishekmamdapure/jev-information-extraction) — Ask questions about a PDF. Use Jev to rank the source text that answers them. Inspect each match, its probability, and its location on the original page.
- [jevpdf](https://github.com/kylemclaren/jevpdf) — `server/index.ts` is a small Bun server that serves `dist/` and the `/api/jev` proxy, which uses the same forwarding code as dev (`server/jev-upstream.ts`). Because the live proxy spends real credits, it only accepts…
- [aegis: TypeSafe as a first-class provider](https://github.com/dvjn/aegis) — A personal Rust AI gateway with a TypeSafe provider, usage extraction and alias resolution tested against real response bodies.
- [Cookbook: Structured data extraction cascade](https://docs.typesafe.ai/cookbooks/sde_cascade) — A two-stage mini-then-verify-then-reasoning cascade that reaches most of a big reasoning model's quality at a fraction of the cost.
- [Date extraction](https://docs.typesafe.ai/cookbooks/date_extraction_cookbook) — Extracts absolute and relative dates by asking for the parts a document names, then resolving and validating them in code with confidence-based review.
- [Double-checking citations](https://docs.typesafe.ai/cookbooks/citation_check) — Catches wrong or invented citations against the source document with one Choice, using its confidence to flag borderline cases for review.
- [Example use cases](https://docs.typesafe.ai/concepts/use-case-map) — The vendor's own taxonomy: five headline categories, nineteen industry groups, and ten decision shapes from classification through to structured data extraction.
- [Knowledge graph entity alignment](https://docs.typesafe.ai/cookbooks/entity_alignment) — Decides which of 450 candidate pairs from two product catalogues describe the same thing, with one Score whose three levels are the three available actions.
- [Pre-parsed value extraction](https://docs.typesafe.ai/cookbooks/pre_parsed_value_extraction_cookbook) — Regexes find candidate emails, phone numbers and amounts; the model selects the requested span so code can normalise a verbatim value.

### Guardrails, safety & review

- [DeepChat: agent tool-permission review](https://github.com/ThinkInAIXYZ/deepchat) — Reviews each tool call on three axes — risk level, whether the user authorised it, and an explicit prompt-injection pressure check.
- [Clean Code Review](https://github.com/frostney/clean-code-review) — `Open source` · `Free source build` · `BYOK`. Hosted/source PR reviewer: TypeSafe Jev judges files on Clean Code questions; Luna writes evidence-first prose (MCP included). [Try app](https://clean-code-review.vercel.app) · [Project…
- [Jev Anti-Spam Bot](https://github.com/backmeupplz/jev_antispam_bot) — `Open source` · `Free source build` · `BYOK`. Self-hosted Telegram bot that deletes high-confidence spam using TypeSafe Jev Noul signals, with fail-open errors. Project guide.
- [jev-guard](https://github.com/muratcakmak/jev-guard) — Probability-scored guardrails for Claude Code: deny rule-breaking edits and unasked-for deploys, route your docs into each prompt, and check the final answer against the turn's own evidence.
- [jev-guard](https://github.com/ClemensSchartmueller/jev-guard) — High-speed, cross-agent safety gate plugin for Claude Code, Codex CLI, and Antigravity.
- [claude-jev-plugin](https://github.com/dr-dimitru/claude-jev-plugin) — TypeSafe Jev semantic guardrails for Claude Code
- [opencode-jev-guard](https://github.com/CogFlux/opencode-jev-guard) — When FarHand is active, the agent's commands run on a remote host through the `farhand_remote_shell` MCP tool instead of `shell`. OpenCode's permission request for an MCP tool carries no arguments, so the plugin…
- [guardrail-chatbot-jev](https://github.com/taman-spirit/guardrail-chatbot-jev) — It is a library, not a service. You call it, you get a verdict, and your code decides what to do. It runs in Python and TypeScript, both reading the same policy file, so the two sides of your stack cannot drift…
- [Choice self-consistency](https://docs.typesafe.ai/cookbooks/consistency_choice_cookbook) — Adds an explicit "uncertain" outcome to moderation decisions and measures label agreement against the share of actions taken automatically.
- [Cookbooks](https://docs.typesafe.ai/cookbooks/llm_guardrails) — Screens every message in and out of an LLM app in one request, naming hazards and scoring how much harm complying would do.
- [jevai.org community showcase cases](https://jevai.org/cases) — Nine worked community scenarios: intent routing, invoice classification, news filtering, product tagging, moderation, claim verification, CSV validation and more.
- [Jevtown](https://jevtown.ivanhabor.com) — Town of 10,000 computed personas that reads a post, listing, product, or headline: one opening request scores the text against about 60 audience attributes, 83 for a listing or a product, plus seven moderation questions, and plans the…
- [Read](https://mrjev.com/projects/devmortimer-pi-warden) — Read — System One / Jev related resource.

### Agents, tools & harnesses

- [Prism](https://github.com/irfndi/prism-liquidity-agent) — 69 stars — An autonomous liquidity agent that uses JEV inside its rebalancing decision service. [Source](https://github.com/irfndi/prism-liquidity-agent/blob/22c67bdbe30bab608226832256a5013ad826b707/engine/jev-service.ts)
- [JevScout](https://github.com/hqman/JevScout) — A demo job-search Skill for coding Agents that browses company careers pages in Chrome, uses Jev to screen AI and software-engineering roles, and saves the results.
- [hermes-jev](https://github.com/keeltrace/hermes-jev) — An asynchronous Jev companion for Hermes Agent covering relevance, completion, recovery and optional admission decisions.
- [Hearth](https://github.com/Nancy-Chauhan/hearth-jev-rental-search) — `Open source` · `Free source build` · `BYOK`. Local Chrome agent that searches four rental marketplaces with TypeSafe Jev action choice and returns a shortlist (read-only). Project guide.
- [jev-for-all](https://github.com/emirbartu/jev-for-all) — Jev for every agentic development workflow — the System One decision model wired into whatever harness an agent codes in: OpenCode today, Claude Code and Hermes adapters next.
- [cairn-jev-lab](https://github.com/Cairn-ink/cairn-jev-lab) — Use it to test a memory policy before letting it decide what an agent keeps. The lab includes editable cases, a reusable JavaScript entry point, and reports that retain both successful judgments and mistakes. Node.js…
- [jev-engineering](https://github.com/codejunkie99/jev-engineering) — Jev Engineering: Typed Decision Systems for Reliable Agent Workflows. Paper, diagrams, and companion examples by Av1dlive.
- [jev-gamepilot](https://github.com/newuser7171/jev-gamepilot) — \\Jev-GamePilot\\ is a universal autonomous AI gaming agent powered by \\Laya (local sub-30ms System One inference)\\ and \\TypeSafe's Jev System One\\ (\`Choice\`, \`Score\`, \`Noul\`). It captures real-time gameplay at 60+ FPS, fuses…
- [jev-predict-skill](https://github.com/DanielKillenberger/jev-predict-skill) — An Agent skill recipe that predicts another skill’s closed-set outcome from its rules and evidence.
- [jevscan](https://github.com/jevbook/jevscan) — An EVM Token screening tool with library, CLI and MCP interfaces for market-feature-based risk judgments.
- [jev-factorio-agent](https://github.com/CompleteDotTech/jev-factorio-agent) — Jev picks what, code owns how - a System One Factorio agent driven by TypeSafe's Jev on FLE
- [jev-pilot](https://github.com/Akramovic1/jev-pilot) — Let Jev steer Claude Code: the right reasoning effort, subagent model and skill for every prompt. A Claude Code plugin powered by TypeSafe's Jev (OpenRouter / TypeSafe).
- [WindowsJev](https://github.com/Teylersf/WindowsJev) — Token-efficient Windows automation and durable research MCP server for Codex and Claude Code, powered by TypeSafe Jev.
- [Jev Skills](https://mrjev.com/projects/wuyoscar-jev-skill) — Jev Skills — System One / Jev related resource.
- [jevai.org community site](https://jevai.org) — An unaffiliated community site with a playground, a preset decision API, an MCP server, downloadable skills and a gallery of community apps.
- [Skill suggestion](https://docs.typesafe.ai/cookbooks/skill_suggestion) — Picks at most one skill out of 182 for an agent turn: one request ranks every skill and asks whether the turn needs one at all, a second reads the top three.

### Search, RAG & rerank

- [laya-jev-GraphRAG](https://github.com/bodepudimuneendra-netizen/laya-jev-GraphRAG) — Agentic GraphRAG engine using swappable System One decision models (local Laya / cloud Jev). Features a complete 4-phase pipeline (Ingestion, Pre-Retrieval, Traversal, Post-Retrieval) and evaluation across Neo4j,…
- [reranker](https://github.com/hev/reranker) — A Python reranker that packs a query and up to 30 candidates into one Jev state, with one Noul relevance question per document.
- [Paper Trellis Citation Verifier](https://github.com/MarissaFamularo/citation-verifier) — Human-reviewed manuscript citation checker: code verifies retrieved passages, Claude proposes evidence, and Jev scores whether the cited passage supports the claim; citation text and paper content go to the selected providers, and the…
- [jev-search](https://github.com/larguesa/jev-search) — Experimental semantic line search with TypeSafe Jev via OpenRouter. Python CLI with no runtime dependencies.
- [JevFind](https://github.com/Peu77/JevFind) — Fast semantic code search powered by Jev. Find the relevant files, line ranges, and snippets
- [jev-scout](https://github.com/AkashPriyadarshii/jev-scout) — A repository and Rust crate search tool that asks Jev to score and select retrieved candidates for a request.
- [jeves-desk](https://github.com/dabaicai001/jeves-desk) — This repository implements a configurable customer-service platform combining ChatKit UI, Jev decision-making, generative chat, RAG knowledge lookup, plugin Tools, MCP data access, and YAML-driven Agent dispatch.
- [jev-retrieval](https://github.com/romeromarcelo/jev-retrieval) — Grep-shaped Rust CLI for coding agents that finds files matching a plain-language concept: a local BM25 pass recalls candidates, Jev verifies each file window-by-window with Noul gates, and one listwise Choice per…
- [Classifying RAG passages](https://docs.typesafe.ai/cookbooks/classifying_rag_passages) — Scores each retrieved passage, then decides in code which reach the answering model — keeping contradictory ones flagged and dropping ones carrying prompt injection.
- [Line-by-line search](https://docs.typesafe.ai/cookbooks/semantic_find) — Semantic search over a terms-of-service document: one request scores 218 line ids with a Choice, and a Noul checks whether the document answers at all.
- [Re-ranking](https://docs.typesafe.ai/cookbooks/rerank_typesafe) — Re-ranks 30-passage BM25 shortlists for 40 legal queries with one question per query-candidate pair, reporting large top-1 and top-10 gains.

### Browser, computer use & OS

- [cua](https://github.com/trycua/cua) — Cua’s preview jev-use example pairs Driver observation and execution with bounded Jev browser-action choices.
- [Jev Chat Assistant](https://github.com/Finderchangchang/jev-chat-JARVIS) — Android overlay that reads visible WeChat, QQ, and X conversations through accessibility, asks Jev for typed intent and action judgments, has a text model draft three replies, and can fill a selected reply without sending it; device…
- [TipTour](https://github.com/milind-soni/tiptour-macos) — `Open source` · `Free source build` · `BYOK`. macOS menu bar app that uses Jev to select desktop click targets from typed requests, alongside a separate Gemini voice mode. Project guide.
- [omg.dev](https://github.com/BennyKok/omg.dev) — 535 stars — An omg.dev mobile testing script can use Jev to read the accessibility tree and choose the next interaction. [Source](https://github.com/BennyKok/omg.dev/blob/a00f56684a569ee417be787c148eaa9874946f2b/mobile/scripts/jev.ts)
- [jev-browser-use](https://github.com/wy-coliney/jev-browser-use) — , Codex skill where Jev handles navigation, clicks, toggles and scrolling and Codex keeps text input and the final check; 5 to 10x faster browser operations in the authors' workflows.…
- [Third Hand](https://github.com/shhivv/third-hand) — 283 stars — A Swift client stack that calls JEV while driving local computer-use style helpers. [Source](https://github.com/shhivv/third-hand/blob/430394b35dbb44ff8b303bf19da29b0828d92bd2/Sources/ThirdHand/JevClient.swift)
- [Jev Browser](https://github.com/jkudish/jev-browser) — MIT-licensed Playwright navigator with MCP, CLI, and library interfaces: Jev chooses DOM actions and judges goal/stuck state while code bounds the loop and returns a trace, final page, and screenshot; early software without iframe,…
- [FluidUse](https://github.com/FluidInference/FluidUse) — Local computer use on Apple silicon using Laya + CUA-S1-FORMS via Accessibility API.
- [macbrow](https://github.com/timpratim/macbrow) — `Open source` · `Free source build` · `BYOK`. Experimental macOS voice assistant using Jev to route commands to AppleScript tools and Chrome browser tasks. Project guide.
- [Arc CUA · TypeSafe Policy](https://github.com/shhivv/arc-cua) — 127 stars — A fast computer-use action layer with a TypeSafe policy implementation. [Source](https://github.com/shhivv/arc-cua/blob/6d47ce6c906d7d8586d3553e277c1c3611c4f6af/src/arc_cua/policies/typesafe.py)
- [fastbrowse](https://github.com/agent-labs-dev/fastbrowse) — Pre-alpha browser agent where Jev picks actions from observed controls, an LLM plans and reads, and code requires page quotes for answer claims and explicit authorization for consequential actions; its author publishes per-run…
- [jev-use](https://github.com/savka777/jev-use) — 86 stars — A macOS computer-use harness that drives Accessibility controls without a vision model. [Source](https://github.com/savka777/jev-use/blob/8907f85354addfa3d2b78f6a462087e4c73310b8/README.md)
- [Jev Voice](https://github.com/kevinbadi/jev-voice) — `Open source` · `Free source build` · `BYOK`. Hands-free macOS voice assistant: local whisper.cpp plus one Jev call per command to select typed actions and arguments. Project guide.
- [typesafe-adblock](https://github.com/realZachi/typesafe-adblock) — `Open source` · `Free source build` · `BYOK`. Experimental Chrome extension that asks Jev whether heuristically selected DOM elements are ads, then removes or highlights matches. Project guide.
- [Jev Desktop](https://github.com/yikangy873-gif/jev-desktop) — Adds a bounded decision loop to Codex Computer Use for browser tabs and native macOS apps.
- [jev-paint](https://github.com/achimala/jev-paint) — Requires Python 3.9+ and a modern browser with module workers and OffscreenCanvas (current Chrome, Edge, Firefox, or Safari). No packages, build step, or Node installation needed.
- [Jev Social](https://github.com/socai-io/jev-social) — Local Instagram and TikTok research app where Jev makes confidence-gated typed choices over the platform and next socai operation, deterministic Node code validates each decision, and the local socai CLI performs read-only browser capture.
- [vibecheck](https://github.com/RafalWilinski/vibecheck) — `Source unverified` · `Pricing unverified` · `BYOK`. Chrome extension that uses Jev to score draft X posts and display a verdict, with optional OpenAI media descriptions. Project guide.
- [Live Jev](https://github.com/okinaaudio/live-jev) — `Open source` · `Free source build` · `BYOK`. Early macOS Ableton Live controller: hotkey bar + TypeSafe Jev picks typed mixer/device actions from short EN/JP phrases. Project guide.
- [Smart Paste](https://github.com/nomanjack/smart-paste) — `Open source` · `Free source build` · `BYOK`. Experimental Chrome extension that uses Jev to select and verify exact source text for web form fields, with paste and undo. Project guide.
- [jev-reviewer](https://github.com/choxos/jev-reviewer) — 32 stars — A browser app that pulls verbatim quotes from trial reports to fill systematic-review extraction forms. [Source](https://github.com/choxos/jev-reviewer/blob/da15868cdca5e64555e6643243a52ea71f60cf3b/docs/jev.js#L51)
- [Sharp](https://github.com/tshmieldev/sharp) — Browser extension that filters your X timeline by plain-language rules, with Jev as the default classifier.
- [jev-kit](https://github.com/jonathanavis96/jev-kit) — Everything you need to run TypeSafe's Jev with Claude Code: a tool-call guard, tier guard, file search, browser agent, review, belay, compaction and installers.
- [HookMeter](https://github.com/ehui1226/hookmeter-jev) — `Open source` · `Free source build` · `BYOK`. Chrome extension that scores social drafts as you type with TypeSafe Jev (curiosity/arousal/pattern/clickbait) via optional worker/backend. Project guide.
- [Jev for Chrome](https://github.com/chy4pro/jev-for-chrome) — `Open source` · `Free source build` · `BYOK`. Chrome extension that drives your current tab with TypeSafe Jev (community port of jev-ultrafast); separate text model for typing. Project guide.
- [JevBrowserExt](https://github.com/chy4pro/JevBrowserExt) — A Manifest V3 Chrome port of jev-ultrafast: Jev picks the operation and DOM element in one request per step; a small chat model fills TYPE\_TEXT.
- [Cheshi](https://github.com/CheshiAI/Cheshi) — macOS workspace for Codex where Jev finds past sessions and the decisions made in them. Apple silicon only.
- [jevfill](https://github.com/imohitmayank/jevfill) — `Open source` · `Free source build` · `BYOK`. Chrome extension that autofills forms from unstructured notes with TypeSafe Jev field matching (skips password/payment). Distinct from Smart Paste. [Project…
- [live-jev](https://github.com/vinilana/live-jev) — A browser-based top-down driving simulator using Jev for lane and speed choices, with an optional chat-model comparison.
- [x-scanner](https://github.com/oso95/x-scanner) — Chrome extension that labels every post you scroll past on X with six typed questions per post, and counts what it costs in the corner.
- [jev-ego](https://github.com/romaluev/jev-ego) — A browser Agent for ego lite that numbers actionable elements for Jev to choose the next step.
- [dejevu](https://github.com/idovmamane/dejevu) — Jev? Déjà vu. Browser agents that run on instinct, no Jev needed. One look at the page, one call to any open model, one action. Faster than the Jev demo on Google Flights.
- [Xtags](https://github.com/manifoldor/xtags) — `Open source` · `Free source build` · `BYOK`. Chrome extension/userscript that tags X posts with TypeSafe Jev intent and risk signals for personal local browsing. Project guide.
- [jev-agent-browser](https://github.com/forvela/jev-agent-browser) — Delegated browser execution for parent agents: Jev selects bounded typed actions, agent-browser performs them, and ambiguous or blocked flows escalate back to the parent.
- [JevBystander](https://github.com/Nisaka520/JevBystander) — This Android accessibility app reads visible WeChat one-to-one chat text and uses Jev to judge intent, emotion, urgency and reply posture, showing the result as 3 Toasts without generating or sending replies.
- [aside-jev](https://github.com/himomohi/aside-jev) — An MCP server and skill adding Jev decisions to Aside browser Agents.
- [AskJev](https://github.com/ranjan2829/AskJev) — Connects Agents to a browser over MCP, using Jev to choose page actions with confirmation gates for actions such as payment or deletion.
- [jev-clerk](https://github.com/stas4000/jev-clerk) — A macOS desktop clerk that books supplier invoices: Jev picks each click from a closed action list; a deep model only rewrites the playbook.
- [PageGrade](https://github.com/kitze/pagegrade) — `Open source` · `Free source build` · `BYOK`. Chrome extension that grades page sections for clarity, writing, and on-page SEO with TypeSafe Jev via Vercel AI Gateway. Project guide.
- [computer-use-jev](https://github.com/paulsmith/computer-use-jev) — A Go-based macOS controller that asks Jev to choose controls and actions from the accessibility tree.
- [ego-jev](https://github.com/jiangkoumo/ego-jev) — Drive the ego lite browser with Jev (TypeSafe System One): one indexed element table in, one operation + target out, single process. ~2x faster than a per-step LLM loop in our measurements.
- [jev-browser](https://github.com/Mrlyk/jev-browser) — Browser automation CLI for AI agents, powered by the Jev model's millisecond decisions and near-zero inference costs
- [jev-skip](https://github.com/valentynkit/jev-skip) — Browser extension that reads the YouTube caption track and paints a per-segment sponsor probability on the seek bar before the intro ends, with no crowd database; reports catching 77% of SponsorBlock's sponsor seconds across 23 videos…
- [Tab Bouncer](https://github.com/MANISH007700/tab-bouncer) — `Open source` · `Free source build` · `BYOK`. Chrome extension that rates open tabs for a typed task with TypeSafe Jev (keep noul + kind choice; batches of 120), then closes mismatches. Distinct from Jev for Chrome. [Project…
- [browser-use-with-jev](https://github.com/garry-schuette/browser-use-with-jev) — Keep Browser Use's execution engine. Move bounded decisions to Jev.
- [CUA-JEV](https://github.com/ZJU-REAL/CUA-JEV) — The experimental open-task paths separate model planning from Jev's typed action selection. They discover browser DOM elements or Windows UI Automation controls dynamically and offer grounded…
- [ego-jev-ultrafast](https://github.com/shikaizhong-design/ego-jev-ultrafast) — Jev drives your Ego Lite browser: one typed-choice request per step. Single-file, zero-dependency port of browser-use/jev-ultrafast with multi-model benchmarks and extra guardrails. Unofficial.
- [jev-browser-local](https://github.com/rorshopping/jev-browser-local) — Run jev-browser on a fully local JEV-style decision engine (no cloud API). Warm-browser fork, VRAM guard, measured benchmarks, run traces.
- [ego-jev](https://github.com/ZHUBoer/ego-jev) — Complete browser tasks with Ego Lite and actively call Jev for semantic target selection, filtering, ranking, classification and text evidence judgments.
- [jev-browser-pilot](https://github.com/aidil2105/jev-browser-pilot) — A bounded decision layer for browser and desktop automation: a decision-only model picks one next step; the code owns perception, content, actuation and verification.
- [jev-browser-qa](https://github.com/jonymusky/jev-browser-qa) — Browser QA where Playwright drives and films, and TypeSafe Jev judges. JSON-flow CLI for agents, run dashboard, agent skill.
- [jev-browser-skill](https://github.com/ChenYCL/jev-browser-skill) — Browser use & computer use for coding agents, powered by TypeSafe Jev: calibrated judgments from a System One model, control loop in code. ego lite / Chrome / Safari · CLI + MCP
- [jev-slop-guard](https://github.com/davertor/jev-slop-guard) — Jev Slop Guard — a Chrome extension that scores and stamps AI slop on your X and LinkedIn feeds as you scroll
- [ego-jev](https://github.com/phd-peter/ego-jev) — Connects Ego Lite snapshots and browser actions to a bounded Jev decision loop.
- [ego-jev](https://github.com/flazouh/ego-jev) — Drive ego-browser pages with TypeSafe Jev: code builds the allowed actions, Jev picks one, code acts and re-checks.
- [jev-paste](https://github.com/Anson-gzy/jev-paste) — Contextual, inline clipboard decomposition for macOS — Tab-to-paste with full history and time-decay ranking. Powered by TypeSafe JEF.
- [jev-tweet-radar](https://github.com/DDnim/jev-tweet-radar) — A Chrome extension that scores each X timeline post with one Jev Noul batch for engagement value and optional tags.
- [jev-wrapped](https://github.com/gaborishka/jev-wrapped) — The browser asks for up to four pages at a time (the plan says how many), which makes up to 24 Jev requests in flight, and shows every answer as it arrives. If a page comes back throttled, it goes to the end of the…
- [JevFilterForX](https://github.com/grayrepo-byte/jev_filter_for_x) — A browser extension that scores and filters X posts in real time with Jev, folding low-signal content while keeping it expandable. Without an API key, it defaults to local mock scoring.
- [JevPaste](https://github.com/taiki510/JevPaste) — `Open source` · `Free source build` · `BYOK`. macOS menu bar Smart Paste: TypeSafe Jev selects an exact clipboard/profile value for the focused field. Project guide.
- [playwright-jev](https://github.com/dingw530/playwright-jev) — This tool provides a Node CLI for goal-driven web E2E testing where Jev chooses the next step from a code-generated action space, playwright-cli observes and executes browser actions, and code controls inputs,…
- [PlotVeil](https://github.com/Dearest/plotveil) — Chrome extension (Manifest V3) that covers a YouTube comment while one Jev Noul question decides whether it reveals a concrete plot event, fate, ending or result of the video being watched or of any other title the user chose to…
- [Polymorph](https://github.com/moomooskycow/polymorph) — `Open source` · `Free source build` · `BYOK`. Chrome extension that collapses posts matching English rules judged by TypeSafe Jev via OpenRouter Decisions; replace with your media or restore. [Project…
- [ScrollPatrol](https://github.com/ennsharma/scrollpatrol) — `Open source` · `Free source build` · `BYOK`. Chrome extension that mutes feed posts by meaning with TypeSafe Jev Noul rules (LinkedIn/Reddit/HN + short-video beta). Project guide.
- [cline-plugin-jev-browser](https://github.com/abeatrix/cline-plugin-jev-browser) — A Cline plugin using an isolated Playwright browser and Jev decisions through Vercel AI Gateway.
- [Focus](https://github.com/bramtechs/Focus) — `Open source` · `Free source build` · `BYOK`. Browser extension that classifies domains as productive or distracting with TypeSafe Jev via OpenRouter Decisions and blocks distracting navigations. [Project…
- [JevEye](https://github.com/Adityakhalkar/JevEye) — `Open source` · `Free source build` · `BYOK`. Browser vision probes report calibrated facts; TypeSafe Jev plans probes and judges the text fact sheet (never pixels). Project guide.
- [jevx](https://github.com/hawkyre/jevx) — `Open source` · `Free source build` · `BYOK`. Chrome/Firefox extension: find relevant X posts and score drafts with TypeSafe Jev (BYOK; no backend). Project guide.
- [Slop Mop](https://github.com/tomfrazier/slopmop) — `Open source` · `Free` · `BYOK`. Chrome extension that judges LinkedIn post writing with TypeSafe Jev (not an AI detector); free hosted use with daily check limits, or self-host MIT with your own key. [Try app](https://slopmop.lol) ·…
- [Read](https://mrjev.com/projects/jkudish-jev-browser) — Read — System One / Jev related resource.
- [Read](https://mrjev.com/projects/awlevin-typesafe-computer-use) — Read — System One / Jev related resource.

### Games, robotics & simulation

- [Jev Minecraft Agent](https://github.com/rmalde/minecraft-agent) — Astra plans while Jev selects bounded actions from structured Minecraft state through Mineflayer. The author reports an 8-minute-43-second dragon kill and exit in Survival/Peaceful mode on a preselected seed with a naturally active End…
- [Embodied Jev](https://github.com/FBddcz/embodied-jev) — , MuJoCo robot decision workbench where Jev picks the next manipulation step. [![Code](https://img.shields.io/github/stars/FBddcz/embodied-jev?style=flat-square&logo=github&label=Code&color=181717)](https://github.com/FBddcz/embodied-jev)
- [Laya vs Jev: T-Rex arena](https://github.com/virajbhartiya/laya-vs-jev) — , Local Laya and hosted Jev play the same T-Rex course; both finish two published assisted rounds without deaths, with planner-provided move labels and safety interventions explicitly logged.…
- [jev-robot-control](https://github.com/openroboto-ai/jev-robot-control) — , Same task, different decisions: Jev against GPT-4.1 and GPT-4o mini on a robot arm, with cost and time per episode.…
- [RoboJEV](https://github.com/lykycy123/RoboJEV) — RoboJEV is a small, inspectable robotics laboratory. JEV receives \\structured simulator state, not images\\, selects an immediate intent, then selects X/Y/Z directions and a gripper command. A Cartesian controller executes the action…
- [clash-jev](https://github.com/bytelabs-oss/clash-jev) — A Clash Royale bot with no trained policy: Jev (TypeSafe System One) makes every decision from the live game state
- [OneVOneJev](https://github.com/emrickgarrett/OneVOneJev) — A browser-based 1v1 shooter where Jev reads structured match state and chooses movement, aim, and firing.
- [laya-vs-jev-arena](https://github.com/PromptEngineer48/laya-vs-jev-arena) — Laya (open source, local) vs TypeSafe Jev (API): two AI models race in Snake and fight in a Mortal-Kombat-style arena. Every move is a real model decision.
- [PlayJev](https://github.com/OmniJev/PlayJev) — Plays ten browser games from the frame alone with an open 0.8B model that scores the moves the game lists in one forward pass; independent of official Jev. Project guide
- [tsai-sc](https://github.com/phyous/tsai-sc) — , TypeSafe Jev controls the original StarCraft, one typed decision per game tick. [![Code](https://img.shields.io/github/stars/phyous/tsai-sc?style=flat-square&logo=github&label=Code&color=181717)](https://github.com/phyous/tsai-sc)
- [Jev plays Snake](https://github.com/sorrycc/typesafe-snake) — Snake autoplayer driven by TypeSafe Jev, executing one discrete System One decision per tick with code-enforced legal moves.
- [jev-reflex-autonomy-lab](https://github.com/khordoo/jev-reflex-autonomy-lab) — Multi-drone simulation where typed reflexes fly the fleet and an optional slower planner may advise but never takes control.
- [jev-doom-agent](https://github.com/lukaske/jev-doom-agent) — A browser Doom experiment comparing Jev-controlled players from the same initial state.
- [jev-askable-arm](https://github.com/TarunTomar122/jev-askable-arm) — Uses Jev to chain predefined skills for English-language goals in a ManiSkill robot-arm simulation.
- [jevscape](https://github.com/Skyvern-AI/jevscape) — A RuneBench extension using Jev and a bounded rs-sdk action catalog for RuneScape tasks.
- [HEIST//ONE](https://github.com/AbdelStark/heist-one) — Observable browser stealth game where Jev supplies batched typed judgments for six guards while deterministic code owns the simulation and validates every proposal; includes a Decision Lens, scripted offline mode, evidence traces,…
- [Jev Grand Prix](https://github.com/enoyola/jev-grand-prix) — `Open source` · `Free source build` · `BYOK`. Local F1 race: TypeSafe Jev picks line and pedals; code steers and plans next laps. Project guide.
- [JevBird](https://github.com/leftspace89/JevBird) — A Python Flappy Bird game where code simulates candidate routes and Jev picks one.
- [jev-plays-pokemon-red](https://github.com/valentynkit/jev-plays-pokemon-red) — Pokémon Red on PyBoy where deterministic code owns the route and arithmetic and Jev picks only at branches, with every battle turn's faint prediction scored by Brier against the emulator's RAM state.
- [doom-jev](https://github.com/AmoghCreator/doom-jev) — A ViZDoom Agent that uses Jev to choose movement, targets and firing from structured game state.
- [Jev Plays Pokémon](https://github.com/anxkhn/JevPlaysPokemon) — A Pokémon agent that lets you emulate GBA games and has Jev make the battle decisions based on the current stats, state, moves, and Pokémon.
- [jev-2048](https://github.com/ARCJ137442/jev-2048) — `Open source` · `Free` · `BYOK`. Instrumented 2048 web lab: every move is a TypeSafe Jev Choice with live probabilities (hosted trial or BYOK). [Try app](https://jev-2048-ultra.vercel.app) · [Project…
- [jev-little-airways](https://github.com/lbotinelly/jev-little-airways) — An island-airport simulator using Jev for routes, yielding, emergency broadcasts and landing order.
- [jev\_vampire\_survivors](https://github.com/oldmoldycake/jev_vampire_survivors) — TypeSafe's Jev model plays Vampire Survivors on Steam: BepInEx plugin + Python brain + live decision dashboard. Native Linux only.
- [jevchess](https://github.com/choxos/jevchess) — Jev, TypeSafe's System One model, plays chess against any OpenRouter LLM, Stockfish and you. One-page web app with live moves, Jev's move probabilities, saved games and win rates.
- [jev-arena-nanojev](https://github.com/liao96312/jev-arena-nanojev) — Jev Arena is a fully local grid tactical game arena where NanoJev, rule agents and search algorithms make per-step move, attack, shoot, heal, dash and environment-interaction decisions across multiple levels with a Chinese Pygame interface.
- [jev-robotics-demo](https://github.com/FazalAAli/jev-robotics-demo) — A MuJoCo arm demo where local code proposes candidate moves and Jev chooses the target, grasp or release, and completion.
- [soupbase](https://github.com/spoonnotfound/soupbase) — Soupbase is a bilingual Chinese-English Turtle Soup game where Jev judges player questions and reconstructions, and the app checks structured Choice results and confidence to decide clearance.
- [jev-2048-selenium](https://github.com/AMMIROSOH/jev-2048-selenium) — Selenium 2048 player powered by expectimax search and TypeSafe Jev, with portrait FFmpeg recording.
- [jev-broadcast-lab](https://github.com/4anti/jev-broadcast-lab) — A Jev experiment workbench centered on chess, with additional classification and matching exercises.
- [jev-chess](https://github.com/hemanth/jev-chess) — Chess moves, evaluations, persona opponents, and game classification using TypeSafe AI System One models. Resolves natural language move intents into legal moves, evaluates positional sharpness and king risk in parallel, and powers…
- [jev-flappy-bird](https://github.com/jaibhasin/jev-flappy-bird) — Jev learns to play flappy-bird game with physics based context and without it
- [jev-got](https://github.com/phureewat29/jev-got) — A Game of Thrones text-adventure demo where a language model writes the story and Jev labels the scene.
- [jev-physical-ai](https://github.com/robokrunch/jev-physical-ai) — Reproducible warehouse-fleet triage demo with 300 Jev calls, raw results, and a local-model cost comparison; incidents are simulated from templates, and no robot hardware or production accuracy was tested.
- [jev-play-ping-pong](https://github.com/Icohen007/jev-play-ping-pong) — Uses Jev to choose serve direction, return angle and pace in a browser table-tennis game.
- [jev-rl](https://github.com/Bring-AI/jev-rl) — JEV Reinforcement Learning: four classic games trained with JEV-powered rewards, reproducible experiments and checkpoint replays.
- [jevarena](https://github.com/raihankhan-rk/jevarena) — Two Jev Agents play Snake in side-by-side browser panes with visible per-step choices.
- [mk-jev-fly-brain](https://github.com/lavallee/mk-jev-fly-brain) — Compares a fly-connectome spiking simulation, Jev and rule policies in the mk.js fighting game.
- [robo-harness](https://github.com/grmkris/robo-harness) — SO-101 robot-arm workbench combining Bun/Effect and Python drivers, using Jev for joint action constraints.
- [tsai-civ2](https://github.com/phyous/tsai-civ2) — An experimental harness where TypeSafe Jev plays classic Civilization II in a browser, computing live action probability distributions.
- [Jev Pong](https://github.com/ably-labs/jev-pong) — Pong where the ball moves one step per model decision, pitting Jev against chat LLMs.
- [jev-clash-royale-test](https://github.com/JanDalhuysen/jev-clash-royale-test) — A Clash Royale-style sandbox whose Jev bot decides play-or-hold, card, lane, and depth in one System One call.
- [jev-practice-speed](https://github.com/tubone24/jev-practice-speed) — A WebGL demo where you play the card game Speed against a CPU whose brain is TypeSafe AI's Jev. The whole point of the app is to measure and show Jev's decision speed and decision accuracy in real time.
- [jev-xiangqi](https://github.com/Zafer-Liu/jev-xiangqi) — Play Chinese Chess (Xiangqi) against Jev - TypeSafe System One decision model as the AI. Score fan-out over legal moves.
- [snake-jev](https://github.com/siroccomask/snake-jev) — Real-time Snake game driven by parallel Jev assessments, deciding optimal turns in a single API call per tick.
- [typesafe-jev-traffic-demo](https://github.com/trycatchkamal/typesafe-jev-traffic-demo) — This is a simulation. It is not connected to, and cannot control, any real traffic signal — Hong Kong's Transport Department publishes no write API for that, only a read-only feed of sensor data. Everything…
- [Jev Asks Until Sure](https://github.com/mintannn/jev-asks-until-sure) — `Open source` · `Free` · `BYOK`. Twenty-questions web game: TypeSafe Jev keeps asking until calibrated confidence crosses a threshold (hosted demo or BYOK). [Try app](https://jev.mintan.org/) · [Project…
- [Jev Chess Lab](https://github.com/denikuchero/jev-chess-lab) — Recorded chess experiments with a candid result: Jev on its own still blunders pieces.
- [jev-experiments](https://github.com/mittal-parth/jev-experiments) — Uses Jev to play Chrome Dino and a local shooter arena while Python executes structured decisions.
- [turing-jail](https://github.com/bugkiwi/turing-jail) — Interactive three-level AI interrogation game powered by TypeSafe Jev; write responses and pass plea, logic, and paradox verdicts to earn release.
- [Jev Chess](https://jevchess.com) — Anyone can play Jev on a shared chessboard. One Choice question covers every legal move; probabilities shade the board. Its confidence panel uses a narrow, one-ply material check. Source is closed.
- [jevai.org community app gallery](https://jevai.org/apps) — Thirty-six community builds curated from social posts: browser agents, spreadsheet tooling, inbox search by intent, ad blocking with judgement, games and robotics.
- [Try app](https://jevchess.xera.ac) — Try app — System One / Jev related resource.
- [Try app](https://jev-2048-ultra.vercel.app) — Try app — System One / Jev related resource.

### Voice, mail & productivity

- [Inbox Zero: seven email decisions](https://github.com/elie222/inbox-zero) — Seven distinct email decisions, each with its own separately chosen threshold, falling back to the normal LLM on any error.
- [aiavatarkit](https://github.com/uezo/aiavatarkit) — 678 stars — An optional AIAvatarKit component uses Jev to judge turn endings from speech transcripts. [Source](https://github.com/uezo/aiavatarkit/blob/38b617b8b9269939734e70ef503d7ea6976acdbd/aiavatar/sts/vad/turn_end_gates/jev.py#L172)
- [Jev Chat Windows](https://github.com/jev-chat/jev-chat-windows) — `Open source` · `Free source build` · `BYOK`. Windows WeChat side panel: local OCR + TypeSafe Jev (OpenRouter) ranks fill-only reply candidates; send stays manual. Project guide.
- [OpenWhisper](https://github.com/Knuckles92/OpenWhisper) — 187 stars — A dictation and meeting-notes app with optional Jev checks for topic changes, note-taker instructions and sensitive text.…
- [Dasheng](https://github.com/wquguru/dasheng) — 119 stars — A reading-practice app that combines streaming ASR with per-word JEV judgments. [Source](https://github.com/wquguru/dasheng/blob/1bacff4a075527e6c02da242a72d117e7cb3286b/lib/jev.js)
- [Sponsor Skip](https://github.com/trungdq88/youtube-sponsor-detection) — `Source unverified` · `Pricing unverified` · `BYOK`. Locates YouTube sponsor reads with Jev-selected transcript boundaries and optional Deepgram audio analysis, with playback skipping. [Project…
- [jevmeter](https://github.com/ChetasLua/jevmeter) — Local video editor that transcribes speech, asks Jev preset Noul questions for each sentence, and renders a shareable debate, earnings, podcast, or sales meter; its probabilities are model judgments rather than fact checks, and its…
- [Call Coach](https://github.com/ZeroGold/call-coach-ai) — Listens to a live sales call and, after each sentence, tells the rep what to do next with a confidence score.
- [wechat-jev-assistant](https://github.com/yushen100/wechat-jev-assistant) — Jev returns a structured decision for the local program; consult the source for the exact decision policy.
- [jeveryword](https://github.com/jkrup/jeveryword) — Jev answers multiple-choice questions and does not generate text, so on its own it cannot return a name, an email address or a quote. jeveryword numbers the words of your text, offers those numbers as the answer options, and converts…
- [heyreach-jev-bot](https://github.com/matthew004-web/heyreach-jev-bot) — Signal-based LinkedIn outbound scoring for HeyReach, running on Jev (TypeSafe System One).
- [Jaste](https://jaste.app) — `Source unverified` · `Pricing unverified` · `BYOK`. Mac clipboard beta with a Direct Jev mode for selecting a saved text value that fits the focused field; BYOK applies to that optional mode. [Project…

### Markets & operations

- [ai-hedge-fund](https://github.com/virattt/ai-hedge-fund) — 63.7K stars — An educational hedge-fund prototype with an optional JEV adapter for structured strategy judgments. [Source](https://github.com/virattt/ai-hedge-fund/blob/154a8b2f46dca0f40764d814e4e747b0ad71f4c4/hedge_fund/llm/client.py)
- [Jev Trade](https://github.com/aowang-ai/jev-trade) — Live Hyperliquid desk across five isolated wallets: each tick packages book, tape, and position as state, Jev answers Choice questions for long/short, open/close/hold, and leverage, and application code places or pulls the quote (hold…
- [Jev-Trades](https://github.com/zadescoxp/Jev-Trades) — A dashboard combining live crypto market data with Jev-guided paper trading; no broker or live-order API is connected.
- [Jevinik](https://github.com/unicodeveloper/jevocks) — Stock decision terminal that gathers live market evidence and returns a typed view on the next thirty days, with the sources it used.
- [jev_stock](https://github.com/sosopop/jev_stock) — Experiment in forecasting Hong Kong stock direction: it builds a past-only state from market data, asks for an up, flat or down call, and renders a standalone report.
- [jev-trading](https://github.com/EthanAlgoX/jev-trading) — \\Jev Trading is a stock decision service that runs on your computer.\\ Use the web workbench or call it from your own software over HTTP. It sends market data, indicators, fundamentals, and news collected by AIStock to a model, then…
- [jev-A-share-trader](https://github.com/Eric-Zhou-0302/jev-A-share-trader) — A Jev-powered technical analysis workspace for China A-shares, supporting AKShare/Tushare, market scans, and Buy/Hold/Sell assessments with time horizons and traceable evidence.
- [jev-bot](https://github.com/bl888m/jev-bot) — JEV-powered market decision bot for stocks, crypto and memes. State in, BUY/SELL/HOLD/AVOID out, paper by default
- [jev-market-reflex](https://github.com/zzsong1023/jev-market-reflex) — Fast typed AI decisions on live crypto markets using TypeSafe AI Jev.
- [jev-claim-vs-measured](https://github.com/Siim/jev-claim-vs-measured) — A post with ~400k views says TypeSafe's Jev is the fastest AI model ever built for trading, makes calibrated buy/sell decisions in under 100 ms, and shows how to build an HFT system on it. The article behind it…
- [jev-trade](https://github.com/Waxmell114514/jev-trade) — A simulated crypto trading loop that sends BTC and ETH market features to Jev and models execution costs and latency.
- [Cookbook: Function calling](https://docs.typesafe.ai/cookbooks/function_calling) — Maps natural-language trading requests onto ordinary typed functions by turning function names and closed-set arguments into confidence-aware questions.

### Creative tools

- [jevthoven](https://github.com/cocktailpeanut/jevthoven) — Turns a music prompt into editable multitrack MIDI by asking Jev to choose instruments, harmony, and bar patterns.
- [ui-generator-instinct-jev](https://github.com/joevidev/ui-generator-instinct-jev) — Turns UI descriptions into selections from existing shadcn/ui components, fields and styles.
- [jev-in-blender-experiment](https://github.com/kolibril13/jev-in-blender-experiment) — Blender exposes ~2,500 operators; a TypeSafe \`Choice\` question holds at most 255 options, so the search is hierarchical (two requests per search):
- [jev-music-tag](https://github.com/xhongc/jev-music-tag) — A minimal FastAPI and React workbench that sends local audio tags to Jev for decisions and writes the returned metadata updates back to the audio files.
- [Apparite (jev2ui)](https://github.com/dglazkov/jev2ui) — `Open source` · `Free source build` · `BYOK`. Local design-mock lab: TypeSafe Jev chooses IA/anatomy; Gemini writes copy; code assembles A2UI-inspired mocks. Project guide.
- [jev-music-theory-1](https://github.com/adammichaelwood/jev-music-theory-1) — Explores Jev on harmony exercises and music-theory questions, alongside a piano demo driven by chord choices.

### Playgrounds & live demos

- [Jev Explained](https://github.com/davila7/jev-explained) — Interactive playground that walks through a typed request and its probabilities, with your own key.
- [typesafe-ai-playground](https://github.com/TypeSafeAI/typesafe-playground) — Community playground for TypeSafe AI and Jev featuring 110 real-world scenarios, dilemmas, and interactive experiments.
- [Jev demos](https://github.com/mayank953/Jev) — `Open source` · `Free source build` · `BYOK`. Six local side-by-side TypeSafe Jev demos with Claude/Kimi switcher and simulated mode without keys. Project guide.
- [jevtest](https://github.com/joshhu/jevtest) — It provides a web and CLI demo that sends user text to Jev through OpenRouter for Choice, Score, and Noul probability judgments and compares the results side-by-side with a general LLM.
- [jev-flappy-bird](https://github.com/hosseintoussi/jev-flappy-bird) — A live demo of TypeSafe's Jev model playing Flappy Bird, one flap-or-wait decision at a time.
- [JevSlop](https://github.com/TKY-27/JevSlop) — `Open source` · `Free source build` · `BYOK`. Scores note articles for AI-slop writing patterns with TypeSafe Jev (BYOK). [Try app](https://jevslop.pages.dev/) · Project guide.
- [tempo-jev-demo](https://github.com/mychaelangelo/tempo-jev-demo) — I created Tempo with OpenAI's Codex, using Astra and GPT-5.6 Sol, with my direction and guidance. Codex also came up with the name Tempo. I haven't personally reviewed all of the code. This is an experimental demo so don't use it for…
- [jev-demo](https://github.com/PenglongHuang/jev-demo) — A zero-dependency local web demo for TypeSafe's Jev (System One) decision model: send a state plus typed questions, get choices, scores and calibrated probabilities back.
- [jev-graphrag](https://github.com/neo4j-field/jev-graphrag) — Small demos + use-case backlog: TypeSafe AI's Jev as a calibrated decision layer for GraphRAG pipelines on Neo4j.
- [jev-playground](https://github.com/Little-Planet-Labs/jev-playground) — A web playground for entering state and decision questions, then inspecting Jev answers and probability distributions.
- [jevchat](https://github.com/kt3k/jevchat) — A chat-style Jev demo whose answers are selected from predefined or custom options rather than generated prose.
- [Fotocopiatrice](https://github.com/bnistor4/fotocopiatrice) — `Open source` · `Free source build` · `BYOK`. Italian Camera amendment explorer: code dedupes identical texts; TypeSafe Jev judges attributes and near-duplicate pairs (static site). [Try app](https://fotocopiatrice.vercel.app/) ·…
- [jev-repl](https://github.com/aoprisan/jev-ts-repl) — Terminal REPL for shaping System One requests before writing code. Simulates answers when no API key is set.
- [Watermelon](https://github.com/shashwatc12/watermelon) — `Open source` · `Free source build` · `BYOK`. Status-update honesty auditor: TypeSafe Jev judges language while code parses slip signals; live demo available. [Try app](https://watermelon.shashwatchavan.com) · [Project…
- [Crowdcheck](https://crowdcheck-ai.vercel.app) — Live demo that tests a 144-character post on 10,000 persistent synthetic personas: code decides who sees it, and batched Jev calls return read, like/dislike, agreement, repost, follow, and block probabilities per persona group; posting…
- [Demo: Smart home assistant](https://docs.typesafe.ai/demos/smart-home) — Runnable demo code for a smart home assistant that evaluates user requests with typed decisions.
- [Interactive demos](https://docs.typesafe.ai/demos) — Official hands-on examples, including the smart-home assistant.
- [Is it AI slop?](https://is-it-ai-slop.app.mintapis.com) — No-signup JevBench demo: typed decisions for AI-slop detection.
- [Try app](https://clean-code-review.vercel.app) — Try app — System One / Jev related resource.
- [Try app](https://fotocopiatrice.vercel.app) — Try app — System One / Jev related resource.
- [Try app](https://jev.mintan.org) — Try app — System One / Jev related resource.
- [Try app](https://jev-column-race.vercel.app) — Try app — System One / Jev related resource.
- [Try app](https://jev.s1.dev) — Try app — System One / Jev related resource.
- [Try app](https://jevslop.pages.dev) — Try app — System One / Jev related resource.
- [Try app](https://ai.quantdinger.com) — Try app — System One / Jev related resource.
- [Try app](https://slopmop.lol) — Try app — System One / Jev related resource.
- [Try app](https://watermelon.shashwatchavan.com) — Try app — System One / Jev related resource.
- [TypeSafe Typewriter](https://typesafe-demo.val.run) — Live Val Town demo that updates 16 typed judgments as text changes.
- [Who is right?](https://who-is-right.app.mintapis.com) — No-signup JevBench demo: typed decisions over a claim-dispute scenario.

### Other applications

- [Notra](https://github.com/usenotra/notra) — `Open source` · `Commercial` · `Paid`. Uses Jev judgments within a broader application for tracking brand mentions and placement in AI answers. [Product](https://www.usenotra.com) · [Pricing](https://www.usenotra.com/pricing) · [Project…
- [killmyidea](https://github.com/monteduro/killmyidea) — Scores a startup idea across several dimensions and returns a verdict of kill, fix or ship.
- [JEV Chat](https://github.com/w3cj/jev-chat) — 84 stars — A tool-using chat interface where JEV chooses only from code-supplied reply and tool options. [Source](https://github.com/w3cj/jev-chat/blob/e543aba8c21b57a28a748ef41966502130f0f69e/apps/server/src/jev/pools.ts)
- [jevchat](https://github.com/kyle-pena-nlp/jevchat) — Turns a decision model into a chat model by asking which symbol comes next, then sampling from the returned distribution.
- [Working-Memory-Jev](https://github.com/AustinAWay/Working-Memory-Jev) — Working-Memory-Jev — System One / Jev related project.
- [jev-dataops](https://github.com/RenaGao/jev-dataops) — An open-source JEV-powered workbench for streaming data selection, quality evaluation, automatic LoRA training and held-out model evaluation.
- [jev-curate](https://github.com/AkashPriyadarshii/jev-curate) — A Rust dataset-filtering experiment using Jev scores to keep or reject text records.
- [jeff (Alurith)](https://github.com/Alurith/jeff) — Read-only Go CLI that checks files against rules such as unclear responsibility or weak error handling with Jev, locally or in CI.
- [Jeved](https://github.com/mossyfield/ST-jeved) — SillyTavern extension that asks your own questions about each reply and, when a rule matches, adds a line to the prompt, rerolls, or runs a script.
- [refgarden](https://github.com/AlbionaHoti/refgarden) — `Open source` · `Free source build` · `BYOK`. Local spatial reference gallery where TypeSafe Jev chooses search phrases and highlights Met/NASA/Cosmos/Archive items from text metadata. Project guide.
- [jev-linkmap](https://github.com/stas4000/jev-linkmap) — Site: www.bles-software.com, 566 pages, 8,460 link decisions (15 candidate targets per page). Run on 19 Sep 2026. Every number below is from the run files in \`out/\` and \`runs/\`.
- [JevPR](https://github.com/HexyeDEV/JevPR) — PR Risk review, automated by Jev
- [jev\_deep\_rl](https://github.com/taodav/jev_deep_rl) — This project evaluates a fixed model. It records rewards and decisions without training or updating model weights. A seeded random policy provides a local baseline.
- [JEV-Paper-Radar](https://github.com/Eliot5566/JEV-Paper-Radar) — In GitHub Actions the links point at your own repo automatically (`GITHUB_REPOSITORY`), so a fork needs no configuration. Locally, set `output.feedback_repo = "owner/name"` or run `paper-radar harvest --repo owner/name`.
- [ask-jev](https://github.com/kuhung/ask-jev) — Ask Jev is a Neo-Brutalism style web app where users enter everyday dilemmas and receive direct decisions from Jev.
- [jev-chat-windows-deepseek-jev](https://github.com/Aimark-dai/jev-chat-windows-deepseek-jev) — Jev returns a structured decision for the local program; consult the source for the exact decision policy.
- [jev-yt-time-saver](https://github.com/jaibhasin/jev-yt-time-saver) — This project integrates Jev to provide structured decisions for its workflow. See the repository for implementation details.
- [jev-system-one](https://github.com/haseeb-heaven/jev-system-one) — A terminal Q&A app where OpenAI writes answers and Jev sets response policy and reviews drafts.
- [jev-bot](https://github.com/nssmd/jev-bot) — Self-hosted Jev decision workbench and Feishu bot: automatic choices, probabilities, and experimental word/character writing.
- [jev-chat-windows-laya](https://github.com/ZJemYoung/jev-chat-windows-laya) — Jev returns a structured decision for the local program; consult the source for the exact decision policy.
- [jev-enforce](https://github.com/erkamyaman/jev-enforce) — Claude Code plugin that makes Claude follow your CLAUDE.md: every reply and edit checked by TypeSafe Jev ✅
- [Jev-in-the-Loop](https://github.com/Tongyun1/Jev-in-the-Loop) — Researching how Jev can accelerate tasks that rely on LLM decision-making.
- [JevLight](https://github.com/usail-hkust/JevLight) — Jev-powered traffic signal control on CityFlow with structured phase and green-time decisions.
- [Hx](https://github.com/doitrous/hx) — `Open source` · `Free source build` · `BYOK`. Clinical note checklist that ticks items against clauses from the note using TypeSafe Jev (never generates text). Project guide.
- [jev-storyboard-lab](https://github.com/jimmyliao/jev-storyboard-lab) — (`agent_framework.foundry.FoundryChatClient` is a different client this repo doesn't use — its `credential` parameter only accepts Azure AD token credentials, not an API key. If you only have a key-based Azure OpenAI…
- [jevsume](https://github.com/unownone/jevsume) — A resume-review app that checks general writing and structure or compares a resume with a specific job description.
- [jevtown](https://github.com/gaborishka/jevtown) — A check costs from half a cent (a text that dies in the first wave) to ten cents (one that reaches all 10,000), and takes from 3 seconds to a minute. The interface comes in Ukrainian and English, and so do the personas: a text is read…
- [bes-kelime-jev](https://github.com/mahmut-gundogdu/bes-kelime-jev) — Jev bir sohbet modeli değil, evaluation modeli. Serbest metin üretmez; tipli sorulara `choice` / `score` / `boolean` cevapları döner. Bu, "sadece şu 5 kelimeden birini söyle" kısıtını prompt'la rica etmek*…
- [chat2jev](https://github.com/Chandler-Sun/chat2jev) — Convert OpenAI-compatible Chat Completions requests into TypeSafe System One (Jev) State / Questions, compare generated text with structured judgments, and publish reusable question sets as proxy routes.
- [emoji-jev](https://github.com/colinmcdermott/emoji-jev) — The app sends typed text to Jev to get parallel emoji Choice, emotion Choice, Score, and Boolean results displayed as an emoji keyboard.
- [grok-jev-guard](https://github.com/0xwhrari/grok-jev-guard) — `grok-jev-guard` sits immediately before a meaningful Grok Bot tool sequence. It receives a compact description of the pending operation and returns one explicit action:
- [jev-311-heatmap](https://github.com/CompleteTech-LLC-AI-Research/jev-311-heatmap) — The live run excluded 205 reports with missing or invalid coordinates, completed \\634 API calls without retries\\, and reported \\539,979 input tokens\\. Repeated descriptions share one evaluation.
- [jev-connector](https://github.com/juanlentino/jev-connector) — WordPress connector for the TypeSafe System One API (Jev): typed questions, confidence-scored answers, core Connectors API key management
- [jev-geo-audit](https://github.com/stas4000/jev-geo-audit) — 300 public pages audited for AI citability with Jev decisions, checked against an LLM judge: agreement, cost and latency, measured
- [jev-gpt](https://github.com/florian-hoenicke/jev-gpt) — Cascaded Choice questions that make Jev pick the next word from a word tree instead of generating text.
- [jev-mobile](https://github.com/xinwang-nwpu/jev-mobile) — One TypeSafe Jev decision per step over the A11Y tree, executed via ADB. No screenshots and ultra fast!
- [jevspeak](https://github.com/MM-sheng/jevspeak) — Jev can't generate text. So I made it talk anyway. A conversational interface built from probabilistic decisions and a deterministic language compiler — no generative LLM.
- [jevTrader](https://github.com/Nachom3/jevTrader) — A High Frecuncy Trader made in Rust using Jev as a decision maker.
- [kojev](https://github.com/ItisNoMatter/kojev) — Kotlin Multiplatform client for Jev that returns your own enum/sealed types instead of string keys.
- [openclaw-jev-plugin](https://github.com/herval/openclaw-jev-plugin) — A silenced message never reaches the language model, so it costs one Jev call and no model tokens. Direct messages always get an answer unless you choose to gate them too.
- [can-jev-bayes](https://github.com/TomRichner/can-jev-bayes) — How well can Jev make sequential decisions under uncertainty, and how can Bayesian methods help it learn and act more effectively?
- [jev-chrome-extension](https://github.com/gavansmyth-arch/jev-chrome-extension) — 1. Open any website. 2. Click the Jev icon. The side panel opens on Drive. 3. Type a goal, e.g. Search Wikipedia for "espresso" and open the article*, and press Run.
- [jev-drive](https://github.com/Alpha-Harper-Franklin/jev-drive) — Jev + autonomous driving: structured decisions, multimodal baselines, recovery research, and measured API diagnostics.
- [jev-reasoning-navigator](https://github.com/AndreuVM/jev-reasoning-navigator) — En lugar de depender de heurísticas matemáticas frágiles o distancias vectoriales locales de coseno, `JEV-Reasoning-Navigator` utiliza TypeSafe AI (`typesafe-sdk`) como motor único y autoritativo de decisión…
- [jev-research-pipeline](https://github.com/shimo4228/jev-research-pipeline) — Code owns the loop, Jev judges, Qwen writes: a daily research monitor for standing questions.
- [jev-synthetic-survey](https://github.com/jjd-lab/jev-synthetic-survey) — New to synthetic survey respondents? Start here. For the raw runs, the scored reports and the code, see where to go.
- [jev-table-tennis](https://github.com/LiuHao-1443/jev-table-tennis) — Table tennis vs. TypeSafe's Jev (System One). Every paddle move on the right is a live model decision — no local prediction, just a lookup table and a servo.
- [jev-test](https://github.com/clduab11/jev-test) — Pre-registered benchmark: can a 2B local model (Gemma 4 E2B) answer web questions without making things up when a decision model (TypeSafe Jev) makes every call? SearXNG for search, MemPalace for verbatim memory,…
- [jev-writer](https://github.com/Kaos599/jev-writer) — Unlike generative writing assistants that flatter drafts, jev-writer enforces strict statistical safeguards: an observational power gate, date-confound controls, and Benjamini-Hochberg false-discovery corrections. It…
- [Jevatar](https://github.com/AppChainAI/Jevatar) — Jev returns a structured decision for the local program; consult the source for the exact decision policy.
- [jevis](https://github.com/jaewgwon/jevis) — A Flutter integration\_test package that registers allowed UI actions and lets Jev pick the next action and whether the goal is done.
- [JevTools](https://github.com/RileyCarney/JevTools) — A toolkit, knowledge base, web cockpit, and reference implementation for building AI applications with Jev (TypeSafe System One) via OpenRouter Alpha Decisions and TypeSafe Direct API.
- [tictacjev](https://github.com/darthblanc/tictacjev) — A tic-tac-toe app where one player is Jev, TypeSafe AI's System One Model with live confidence scores and probabilities.
- [typesafe-jev-ruby](https://github.com/dtheofr/typesafe-jev-ruby) — Ruby client for Jev, TypeSafe's System One model: typed questions, probabilistic answers. Zero runtime dependencies.
- [Jev Radar](https://github.com/Eliovp-BV/Jev-Radar) — `Open source` · `Free source build` · `BYOK`. Local research workspace where Jev steers investigation over public sources with inspectable decisions and optional text-model drafting. Project guide.
- [jev-bfs](https://github.com/komikat/jev-bfs) — Wikipedia link race pathfinder guided by Jev: assesses outbound links to navigate between two articles in real time.
- [jev-calculator](https://github.com/pc418/jev-calculator) — Vars live in `wrangler.jsonc`: `JEV_BASE_URL` / `JEV_MODEL` (gateway), `TYPESAFE_BASE_URL` / `TYPESAFE_MODEL` (direct fallback), `TURNSTILE_SITEKEY`, `TURNSTILE_HOSTNAMES`, `JEV_DISABLED` (kill switch). Rate limits…
- [Jevflix](https://github.com/ArielBubis/Jevflix) — `Open source` · `Free source build` · `BYOK`. Hybrid FAISS+BM25 movie shortlist; TypeSafe Jev parses constraints and picks one film with a confidence gate. Project guide.
- [Composite scoring](https://docs.typesafe.ai/patterns/composite-scoring) — Break one broad judgement into atomic scores and combine them with weights that live in your code, not in the prompt.
- [Cookbook: Autoresearch feature discovery](https://docs.typesafe.ai/cookbooks/autoresearch_feature_discovery) — An autoresearch loop that proposes questions, turns free text into numeric features, and uses model error to improve a supervised gradient-boosting regressor.
- [Cookbooks](https://docs.typesafe.ai/cookbooks/parallel_questions) — A 13-question regulatory briefing over one long article, showing that batching every question into one call is far cheaper and faster with no change in answers.
- [Create a BeatAPI key](https://beatapi.io/dashboard/apikeys) — Create a BeatAPI key — System One / Jev related resource.
- [hermes-jev-approvals](https://mrjev.com/projects/anpicasso-hermes-jev-approvals) — hermes-jev-approvals — System One / Jev related resource.
- [JCR](https://mrjev.com/projects/niazmorshed2007-jcr) — JCR — System One / Jev related resource.
- [Jev DSH](https://mrjev.com/projects/devin-axis-jev-dsh-decision) — Jev DSH — System One / Jev related resource.
- [Jev Wrapped](https://wrapped.ivanhabor.com) — Live X-ray of a public Telegram channel: code reads up to 1,500 posts of the last twelve months from Telegram's public web preview, sampled evenly across the months when there are more, Jev answers a Choice over ten kinds of post and…
- [jev-fit](https://jev-fit.com) — Hosted fit checker and public API: paste a software idea, and one Jev call over a fixed typed rubric returns plain code, Jev, or a reasoning LLM with probabilities, while application code adds an image veto and a low-confidence "not…
- [jev-seo](https://mrjev.com/projects/akashpriyadarshii-jev-seo) — jev-seo — System One / Jev related resource.
- [jev-use](https://mrjev.com/projects/shitianfang-jev-use) — jev-use — System One / Jev related resource.
- [jevscan-evm](https://mrjev.com/projects/devtooligan-jevscan-evm) — jevscan-evm — System One / Jev related resource.
- [Jevvy](https://mrjev.com/projects/panachy-jevvy) — Jevvy — System One / Jev related resource.
- [mrjev.com/changelog](https://mrjev.com/changelog) — .
- [Pricing](https://usenotra.com/pricing) — Pricing — System One / Jev related resource.
- [Product](https://usenotra.com) — Product — System One / Jev related resource.
- [Product](https://quantdinger.com) — Product — System One / Jev related resource.
- [Read](https://mrjev.com/projects/coldteadotai-abide) — Read — System One / Jev related resource.
- [Read](https://mrjev.com/projects/sac-y-jev-cu) — Read — System One / Jev related resource.
- [Read](https://mrjev.com/projects/thruwire-foreman) — Read — System One / Jev related resource.
- [Read](https://mrjev.com/projects/alurith-jeff) — Read — System One / Jev related resource.
- [Read](https://mrjev.com/projects/wfzyx-von) — Read — System One / Jev related resource.
- [Speculative fan-out](https://docs.typesafe.ai/patterns/fan-out) — Pack many questions, including ones you may not need, into a single request and let your code decide afterwards what was relevant.

## Docs & essays

Explainers, launch coverage, TypeSafe concept pages, and background reading.

- [ai-cookbook: Jev track](https://github.com/daveebbelaar/ai-cookbook) — A graded course from a first call through each primitive, state shapes and criteria, to ticket triage and a multi-step workflow, mirroring all four official patterns.
- [learn-jev-end-to-end](https://github.com/harshithsunku/learn-jev-end-to-end) — Learn Jev end to end is a free, hands-on course. In 12 short notebooks you go from "what is Jev?" to building 13 real AI tools with it: an email triage job, a scam-text detector, a code vulnerability…
- [jev-usecases](https://github.com/kenhuangus/jev-usecases) — Production TypeSafe Jev (System One) use-case harnesses with confidence-gated decision logic
- [everything-about-jev](https://github.com/qingshungLI/everything-about-jev) — tell you everything about jev,TypeSafe AI's System One model for typed decisions.
- [jev-cookbook](https://github.com/paramjeetn/jev-cookbook) — The complete cookbook for Jev by TypeSafe AI — 120+ use cases, 10 runnable examples, 4 composition patterns, and first-principles theory for the world's first System One AI model.
- [jev-agent-skill](https://github.com/yuyang2230/jev-agent-skill) — Claude Code / ZCode skill that offloads small judgments (classify/route, batch screening, scoring, compliance pre-checks) from the main model to Jev on OpenCode Zen's free `/v1/systemone` endpoint; bundles a zero-dependency `jev.py`…
- [A deep dive into Jev](https://flaviocopes.com/jev) — The densest independent explainer: code in JS, Python and the AI SDK, all three answer shapes, the advanced patterns, and an honest list of where the model fails.
- [A new kind of AI model from a ChatGPT inventor is thrilling developers](https://techcrunch.com/2026/09/18/a-new-kind-of-ai-model-from-a-chatgpt-inventor-is-thrilling-developers) — The only launch coverage with first-hand developer quotes rather than vendor figures, including a caution that interpreting the thresholds is now your job.
- [Agentpedia claim-vs-evidence guide](https://agentpedia.codes/blog/jev-system-one-models) — , Claim-by-claim audit separating verified Jev pricing and latency from unproven calibration; puts aggregate accuracy at 67.8% versus Opus 5's 73.1%.…
- [AI model "Jev" to make machines decide faster](https://heise.de/en/news/AI-model-Jev-to-make-machines-decide-faster-11457071.html) — Focuses on the missing explainability — the model returns no reasoning in language — and on every published benchmark coming from the vendor.
- [AI: too good to be true, too bad to be useful](https://typesafe.ai/blog/ai-too-good-to-be-true-too-bad-to-be-useful-typesafe-ai) — The argument for moving beyond preference-optimized chat models in automation.
- [AINews: Jev, a System One Model that only decides](https://latent.space/p/ainews-jev-a-system-one-model-that) — Community roundup of the System One / Jev launch and early reactions.
- [Browser Use + Jev](https://x.com/gregpr07/status/2100411066966749359) — Gregor Zunic's real-time flight-search demo and short description of the dynamic DOM action space.
- [Building a Harness with Jev](https://langchain.com/blog/building-a-harness-with-jev) — LangChain's explainer and integration walkthrough: the three question types, plus model routing and gating risky tool calls before they run.
- [Confidence](https://docs.typesafe.ai/confidence) — How confidence is derived from the probability distribution, and why a threshold tuned on one question type does not transfer to another.
- [Current models](https://docs.typesafe.ai/models) — Find model versions, moving aliases, supported inputs, pricing, and current limits.
- [Decoding Jev](https://navinpai.github.io/decoding-jev) — Independent walkthrough of architecture, inference, and RLCD evidence status.
- [Founder launch thread on X](https://x.com/CompleteSkeptic/status/2099925682726002904) — , Diogo Almeida's thread arguing RLCD decision models reach economic value before chat models do.…
- [How does Jev work? RLCD and parallel inference](https://explainx.ai/blog/how-does-jev-work-rlcd-system-one-model-explained-2026) — , Explainer reconstructing the RLCD objective and the parallel sampler from public statements.…
- [How to build with TypeSafe](https://docs.typesafe.ai/concepts/how-to-build-with-system-one) — Design guidance for decomposing a workflow into narrow judgments while keeping policy and side effects in code.
- [How to train your own Jev](https://together.ai/blog/how-to-train-your-own-jev) — Together tutorial / data recipe for fine-tuning a decision classifier (~$17 Tev1 training cost claimed).
- [Internal classifier field note](https://x.com/identityTorn/status/2100475121324728615) — A builder's early matched-precision comparison against a private fine-tuned Qwen classifier; useful anecdotal evidence, not a reproducible benchmark.
- [Introducing DiffusionGemma](https://blog.google/innovation-and-ai/technology/developers-tools/diffusion-gemma-faster-text-generation) — Google blog on DiffusionGemma — faster non-autoregressive text generation used by open System One servers.
- [Introducing System One Models & Jev](https://typesafe.ai/blog/introducing-system-one-models-and-jev) — The launch post: what a System One model is, why decisions were split from generation, and the vendor's latency and cost claims.
- [Introduction](https://docs.typesafe.ai/introduction) — What Jev is, how System One models differ from text-generation models, and the Choice, Score, and Noul primitives.
- [Jev (AI model) on Wikipedia](https://en.wikipedia.org/wiki/Jev_(AI_model)) — Most useful as an index: its reference list is a fast route to the coverage worth reading.
- [Jev (AI model) on Wikipedia](https://en.wikipedia.org/wiki/Jev_(AI_model) — ) — Most useful as an index: its reference list is a fast route to the coverage worth reading.
- [Jev - The Ultimate Classification Model?](https://youtube.com/watch) — A review that puts the limitation in the title rather than burying it.
- [Jev 1.13 jaggedness](https://docs.typesafe.ai/model-jaggedness/jev-1.13) — The vendor's own list of where the model fails: literal reading, arithmetic and counting, date comparison, indirection, large noisy states, adversarial content.
- [Jev AI Use Cases](https://medium.com/data-science-in-your-pocket/jev-ai-use-cases-9a87d57ac3b4) — Walks through use case after use case — agent routing, an in-agent decision layer, ticket triage — each with a concrete option set and a sample response.
- [Jev by TypeSafe: A Decision Model for AI Agents](https://beam.ai/agentic-insights/jev-typesafe-ai-agents) — An agent-builder's framing of where a decision model sits in an agent stack.
- [Jev Cuts AI Decision Costs 100x And Vercel, Cloudflare Rushed To Add It](https://forbes.com/sites/josipamajic/2026/09/19/jev-cuts-ai-decision-costs-100x-and-vercel-cloudflare-rushed-to-add-it) — Mainstream coverage of the launch and the speed with which gateways added support.
- [Jev Explained: How to Add Fast, Typed Decisions to an AI Agent](https://aihubmix.com/blog/jev-explained-how-to-add-fast-typed-decisions-to-an-ai-agent) — A third-party explainer with a useful architecture sketch and an unusually honest list of cases where you should not use a decision model.
- [Jev Typewriter launch post](https://x.com/stevekrouse/status/2100287368221659289) — Steve Krouse's playable 16-judgment demo and video.
- [Jev vs auto-regressive LLMs vs MDLM](https://lilting.ch/en/articles/typesafe-ai-jev-system-one-model) — , Technical comparison of Jev's single-pass sampler with token-by-token decoding and masked diffusion.…
- [Jev-Omni launch thread](https://x.com/Akhila_988/status/2102171891410825520) — Announcement of Jev-Omni as a multimodal open System One model with HF weights.
- [Jev: System One models for Prod, not God](https://latent.space/p/jev) — Interview on System One models for production, not AGI chat.
- [Jev: The Language Model That Won't Talk](https://anthonymaio.substack.com/p/jev-the-language-model-that-wont) — Critical look at the "no hallucination" and benchmark claims.
- [Jev: TypeSafe's System One Model Explained](https://datacamp.com/blog/system-one-models-jev) — A neutral survey of the architecture, the claimed benchmarks and the pricing, which states plainly that no large independent reproduction had surfaced.
- [Jevons' paradox (Alcott 2005)](https://doi.org/10.1016/j.ecolecon.2005.03.020) — , The rebound effect Jev is named for, where cheaper decisions raise total decision volume. ![Ecological Economics 2005](https://img.shields.io/badge/Ecological_Economics_2005-4B5563?style=flat-square)…
- [Jev’s Architecture Unmasked](https://archerhume.com/posts/jevs-architecture-unmasked) — Archer Hume: architecture probe from ~10k API calls — shared state, isolated questions, parallel readouts.
- [kitze thread: Kev / OpenJev / Laya](https://x.com/thekitze/status/2102775497822503298) — Community post threading open System One clones (Kev, OpenJev, Laya) and related serving work.
- [Latent.Space: 6 clones of Jev in 2 days](https://latent.space/p/ainews-here-are-6-clones-of-jev-in) — Roundup of early open reproductions (Nimble, Kev, and others).
- [Manifesto](https://typesafe.ai/manifesto) — TypeSafe's case for machine-native intelligence built for software rather than conversation.
- [Maps of Bounded Rationality (Kahneman Nobel lecture)](https://nobelprize.org/prizes/economic-sciences/2002/kahneman/lecture) — , Kahneman's two-system account, intuition returning an answer directly while reasoning deliberates, the split Jev's design copies.…
- [On Calibration of Modern Neural Networks](https://arxiv.org/abs/1706.04599) — Guo et al., 2017. Introduces temperature scaling and ECE, the calibration foundations these models rely on.
- [OpenAI Structured Outputs](https://platform.openai.com/docs/guides/structured-outputs) — , The provider-side JSON-schema guarantee the CEO named on HN as what Jev replaces, shape enforced but no probability returned.…
- [Quick start](https://docs.typesafe.ai/introduction/quickstart) — The canonical first call: one support ticket, one Choice, one Score and one Noul in a single request, in Python, JS and cURL.
- [Qwen on Cerebras comparison](https://x.com/iamMrDuncan/status/2100467548298899918) — Shannon's video and source-backed comparison of a structured-output LLM baseline with Jev.
- [Reddit: 287 open-source Jev projects (top 20)](https://reddit.com/r/LLMDevs/comments/1wko2e5/i_reviewed_287_opensource_jev_projects_here_are) — r/LLMDevs roundup of 287 reviewed OSS Jev projects with 20 recommended starters (browser, compaction, MCP, games, finance).
- [RLCD explained: Reinforcement Learning for Calibrated Decisions](https://systemonemodels.org/guides/rlcd-explained) — An independent write-up whose most useful finding is a negative one: there is no paper, no reward function, no dataset description and no reproducible evaluation for RLCD.
- [RLCD: how Jev is trained](https://learnjev.com/concepts/rlcd) — Learn Jev primer on what is and is not public about RLCD.
- [System One (TypeSafe docs)](https://docs.typesafe.ai/concepts/system-one) — Author definition of System One models and the typed-decision interface.
- [System One Models](https://systemonemodels.org) — Independent living documentation site for the System One category.
- [The Bitter Lesson](http://incompleteideas.net/IncIdeas/BitterLesson.html) — , The essay TypeSafe's own Bitterest Lesson argues against, named in TypeSafe's materials as its starting point.…
- [The Bitterest Lesson](https://typesafe.ai/blog/bitterest-lesson) — Why optimizing the wrong task can dominate gains from scale.
- [The Register: TypeSafe AI debuts model for machines](https://theregister.com/ai-and-ml/2026/09/16/typesafe-ai-debuts-model-for-machines-that-plays-doom/5296711) — The most sceptical mainstream piece: it challenges the no-hallucination framing on the grounds that a well-formed answer is not the same as a correct one.
- [Thinking, Fast and Slow](https://en.wikipedia.org/wiki/Thinking,_Fast_and_Slow) — , The source TypeSafe cites for naming Jev after System 1, fast intuitive judgement with no deliberation.…
- [Together AI: Tev1-4B-experimental](https://x.com/togethercompute/status/2102882216950763814) — Announcement of Tev1 — Jev-like classifier on Qwen3.5 4B, serverless pricing, data recipe, and train-your-own tutorial.
- [Typed Decisions, Not Chat](https://warmersun.com/jev) — , Secondary analysis of TypeSafe's dashboard putting Jev at about 67.8% mean agreement against 74.1% for the best comparator.…
- [TypeSafe AI](https://typesafe.ai) — Official product site for System One models and Jev.
- [TypeSafe Jev technical deconstruction](https://kevnu.com/en/posts/typesafe-jev-technical-deconstruction-non-autoregressive-decision-primitives-rlcd-and-local-open-source-implementation) — Non-autoregressive primitives, RLCD, and local open-source implementations.
- [TypeSafe's Jev: Can decision models replace LLM judges?](https://arize.com/blog/typesafe-jev-llm-judge) — Collects the third-party evaluations that exist so far and frames the question of where a decision model can stand in for an LLM judge.
- [typesafeai.app](https://typesafeai.app) — Independent directory of public Jev capabilities: each record states what Jev was shown doing, links to its public sources, and carries an evidence level (author-reported to editor-reproduced) and an Official or Community label;…
- [Using TypeSafe Jev with the AI SDK](https://vercel.com/kb/guide/typesafe-jev-and-ai-sdk) — The richest Vercel walkthrough: single and multi-question calls, probability-threshold routing, and unit tests with a mock evaluation model.

## Evals & papers

How these models are measured — including [JevBench](https://jevbench.dev/) — plus papers on calibration and structured decisions.

### Harnesses & live benches

- [JevBench (Benchmark Heaven)](https://benchmarkheaven.com/jev-models) — Interactive JevBench leaderboard: typed decision models scored on intelligence, calibration, speed, and cost.
- [JevBench](https://jevbench.dev) — Interactive harness bench for Jev, open alternatives, and dual-brain (LLM + decision model) setups — starting with StarCraft II — measuring win/loss, task completion, and latency rather than a single typed-answer score.
- [Jev vs. ML](https://github.com/QuicqDev/Jev-vs-ML) — Compares a typed decision model with classical classification pipelines across eight datasets, with a published protocol and an interactive report.
- [typesafe-playground](https://github.com/kavehmz/typesafe-playground) — Interactive Jev experiments for support-routing previews and 3D driving simulations.
- [jev-research-eval](https://github.com/jgridifier/jev-research-eval) — , Reproducible harness scoring Jev ultrafast research-browser runs over 11 baseline cases plus 18 human and quant stress cases with QC grades.…
- [jev-benchmarks (frontier comparison harness)](https://github.com/thijmenkam/jev-benchmarks) — , Harness asking Jev and frontier LLMs identical typed questions, scoring accuracy, calibration, latency and schema validity; no measured run published yet.…

### Typed-decision benchmarks

- [JevBench (text decisions)](https://github.com/fstandhartinger/jevbench) — , 534-decision benchmark with public task results and a v1.3 composite over intelligence, calibration, speed and cost; Jev scores 74.4, with assumed latency adjustments for self-hosted endpoints disclosed.…
- [Jevals.com](https://jevals.com) — Independent benchmark of hosted Jev and six LLMs on PubMedQA, Banking77, and HelpSteer2, with human labels, proper scores, calibration, cost, and latency; [suite files and per-decision logs](https://github.com/Jevals/jevals-data) and…
- [worldmonitor: news threat classification](https://github.com/koala73/worldmonitor) — Two Choice questions over threat level and category, held in shadow mode after a blind evaluation found Jev merely tied the incumbent model.
- [no-mistakes: review context selection](https://github.com/kunchenguid/no-mistakes) — One Score per candidate file to pick review context, with a measured outcome: materially more billed input for essentially no wall-clock gain.
- [conformal-prediction](https://github.com/aangelopoulos/conformal-prediction) — Angelopoulos and Bates: lecture notes and runnable notebooks on conformal prediction and distribution-free uncertainty, the basis for principled abstention.
- [mdlm](https://github.com/kuleshov-group/mdlm) — NeurIPS 2024 masked diffusion LMs — open non-autoregressive research line often compared to Jev.
- [Probing Jev's behaviour with repeated API calls](https://github.com/ahastudio/til) — Independent Korean-language notes reporting that reversing the order of options shifted a probability enough to flip a 0.9 threshold.
- [jev-eval-agent](https://github.com/vinilana/jev-eval-agent) — , Jev routes 100 mocked tools behind a confidence gate, measuring steps, tool calls, tokens and cost against the LLM choosing directly.…
- [jevals](https://github.com/openlayer-ai/jevals) — Agent evals and guardrails as typed questions instead of an LLM judge, packing every eval for a trace into one request. From Openlayer, with a mock backend so the whole library runs without a key.
- [goodwatch-monorepo](https://github.com/alp82/goodwatch-monorepo) — A film-and-TV attribute-scoring experiment inside GoodWatch comparing Jev question designs and batch sizes.
- [TypeSafe AI Benchmark](https://github.com/iammrduncan/typesafe-ai-benchmark) — Side-by-side Jev and Qwen-on-Cerebras comparison with raw exports, cost accounting, methodology, and task-specific limitations.
- [jev-playground](https://github.com/mizchi/jev-playground) — A MoonBit and TypeScript Jev playground covering games, browsers, command risk and small languages.
- [jev-benchmarks](https://github.com/AbdelStark/jev-benchmarks) — , Jev versus GLiNER2.5 on 300 BTZSC examples with calibration and selective risk: 0.910 AG News, 0.870 Banking77, worse on emotion.…
- [jev-rag-benchmark](https://github.com/erendikmenn/jev-rag-benchmark) — Reproducible experiments on whether reranking with Jev improves a small RAG system, on a locked Turkish dataset, with quality, latency and cost reported together.
- [Jev Rerank Bench](https://github.com/anessbelbati/jev-rerank-bench) — Reranking comparison with raw provider responses, scoring code, dataset-level results, uncertainty intervals, and documented limitations.
- [jev-dspy-lab](https://github.com/jmanhype/jev-dspy-lab) — Reproducible calibration and selective-risk benchmarks for Jev/TypeSafe decisions in DSPy workflows
- [jev-benchmark](https://github.com/wondertwins/jev-benchmark) — , Jev no better than random picking chess moves from a FEN, but F1 0.96 on NPC addressee detection, 0.2s median.…
- [jev-lm](https://github.com/y0usaf/jev-lm) — A word-level generation experiment that asks Jev to select words or verify locally drafted continuations.
- [jev-search-rerank-eval](https://github.com/zhuyansen/jev-search-rerank-eval) — Retrieval evaluation system measuring Jev reranking against lexical, embedding, and fusion baselines across 9,831 query-document pairs.
- [jev-phishing-bench](https://github.com/anisselbd/jev-phishing-bench) — The signal result above was challenged on three points: no non-AI baseline, selection and evaluation on the same emails, and no equivalent decomposition for the LLM. Three controls were added (\`bench/heuristics.py\`,…
- [LegalForecastBench](https://github.com/johnhughes3/LegalForecastBench) — , Claim-level Brier scoring of federal motion-to-dismiss outcomes, a fixed binary with one probability per unit; no Jev row published yet.…
- [jev-chat](https://github.com/adhyaay-karnwal/jev-chat) — A research chat decoder that repeatedly asks Jev to choose words or phrases and assembles them in code.
- [sysone-bench](https://github.com/instax-dutta/sysone-bench) — , September 21 comparison of Jev, Laya and Qwen-PCD on 751 states across nine suites with identical questions; Jev leads moderation 98.9% to Laya's 83.3%, while Laya leads AG News 94% to 91%.…
- [Jev IDS](https://github.com/jev-ids/jev-ids) — MIT-licensed intrusion-detection prototype that asks Jev one Noul and one five-way Choice per network flow, comparing it with GPT-5.6 Luna and a Random Forest on NSL-KDD; it publishes run records and evidence limits, but the reported…
- [jev-behavior-study](https://github.com/RINNECODER/jev-behavior-study) — An independent Jev 1.13.0 behavior study recording successes and failures across question framing, input conditions and games.
- [jev-benchmark](https://github.com/YidiDev/jev-benchmark) — Rubric-Based Zero-Shot Classification Benchmark: Jev vs Claude Haiku 4.5 vs Claude Sonnet 5 vs OpenJev on rubric-conditioned classification, chained decision execution, and exam grading -- with full price tracking.
- [jev-exploration](https://github.com/SamuelSacco/jev-exploration) — A research repository tracking Jev claims and limitations, with calibration experiments and runnable examples.
- [jev-gomoku](https://github.com/XieChengYuan/jev-gomoku) — A nine-board, 15×15 Gomoku workbench comparing how two Jev players respond to different input representations.
- [jev-laya-benchmark](https://github.com/harrymunro/jev-laya-benchmark) — Speed and accuracy benchmark: TypeSafe's Jev API vs the local Laya MLX typed-decision model on synthetic tasks
- [jev-sec-bench](https://github.com/Gaurav-Gosain/jev-sec-bench) — Blind Jev-1.13.0 security evaluation with Go runner, raw per-sample results, and a TUI: 662 public prompt-injection messages and 200 matched vulnerable-code pairs; its reported classification scores use the study's stated context and a…
- [Jev Spam Eval](https://github.com/bitnovus/jev-spam-eval) — , Zero-shot spam Noul on 18,514 emails reaching 0.9833 accuracy, matching a TF-IDF classifier trained on 14,800 labels.…
- [jev-agent-failure-benchmark](https://github.com/TokenTrim/jev-agent-failure-benchmark) — Benchmarks TypeSafe Jev on Who&When Pro agent-failure attribution (who/when/what) against published LLM baselines. Project guide.
- [jev-architecture-research](https://github.com/g0runmezadam/jev-architecture-research) — Black-box reverse engineering research archive for the Jev decision model
- [jev-baselines-eval](https://github.com/ickma2311/jev-baselines-eval) — Pre-registered independent eval of Jev against a nano-class LLM, a frontier LLM, and a supervised encoder on Banking77 and CLINC150.
- [jev-frontend-qa](https://github.com/Nainish-Rai/jev-frontend-qa) — Frontend QA that uses Jev to choose browser actions and checks contracts through DOM, HTTP and database evidence.
- [ask-jev](https://github.com/omni-/ask-jev) — A Windows PowerShell tool for auditing recorded Codex execution evidence with :jev.
- [chinese-workflow-decision-bench](https://github.com/Adkid-Zephyr/chinese-workflow-decision-bench) — Feishu-style Chinese message classification bench: 64 frozen scenarios, Choice/four-Noul workflows, published TypeSafe Jev vs Laya results. Project guide.
- [hermes-jev-north-star](https://github.com/poponline63/hermes-jev-north-star) — A Hermes goal-checking skill that saves requirements, creates a run prompt and checks completion evidence.
- [jev-eval](https://github.com/4esv/jev-eval) — Independent eval of Jev vs a frontier LLM across labelled classification tasks: accuracy, calibration, latency, and cost.
- [jev-flash-review](https://github.com/TheBous/jev-flash-review) — An MCP review engine that evaluates Agent-supplied diffs against explicit rules.
- [jev-synergy-screening](https://github.com/PistachioAIHQ/jev-synergy-screening) — A Jev title-and-abstract screening experiment compared with Cohen Abstract Triage labels for an ADHD review.
- [jev-tmmluplus-eval](https://github.com/lianghsun/jev-tmmluplus-eval) — Jev is not a chat model. You hand it a `state` plus a map of typed questions, and it returns one typed answer each — with calibrated probabilities and no generated text.
- [padflow-jev-evals](https://github.com/zsavage8/padflow-jev-evals) — , Three production SaaS decisions published as schemas with auto-post confidence thresholds; LLM baseline rows filled, Jev row still empty.…
- [foreman-jev](https://github.com/Shifty-Eye-Games/foreman-jev) — An experimental Jev supervisor for Codex workers with programmer-selected acceptance commands.
- [Jev Enterprise Decision Fabric](https://github.com/ghubnab99/jev-enterprise-decision-fabric) — Experimental .NET decision architecture with a 111-case Jev-versus-Claude agent-action evaluation, public labels and raw JSONL, report-rebuild tooling, and a decision inspector; one annotator revised labels after reviewing a Jev pilot.
- [jev-calibration-audit](https://github.com/jujumilk3/jev-calibration-audit) — Audits Jev calibration, option-wording effects and Korean judgments through public APIs and datasets.
- [jev-demos](https://github.com/Bud-ro/jev-demos) — Maze experiments comparing Jev single-step choices with multi-step lookahead.
- [jev-measured](https://github.com/WallerChen/jev-measured) — Reproducible OpenRouter measurements of Jev's response shapes, cost, and latency across eight use cases, plus a small head-to-head on 27 author-written support tickets; the author publishes raw data and corrections to earlier comparison…
- [jev-orderby-bench](https://github.com/yodablocks/jev-orderby-bench) — Independent measurement of whether `ORDER BY` over a Jev probability is defensible, with a pre-registered gate on pairwise inversion, Score ordinality against a graded target, calibration, and negation and paraphrase invariants;…
- [jev-playground](https://github.com/hegargarcia/jev-playground) — , Tic-tac-toe and connect four pitting Jev against four frontier models on identical legal-move choice options; no aggregate results published yet.…
- [An early-access test of TypeSafe's Jev: calibrated judgments for half a cent](https://lindfors.no/blog/a-first-look-at-typesafes-jev) — The best independent test found: 24 Norwegian documents on one pinned model version, opening with a case the model got wrong while correctly reporting low confidence.
- [DecisionBench](https://huggingface.co/datasets/akhilaaa3/decision-bench) — Public typed-decision eval set used with Jev-Omni (scenarios → questions with option probabilities).
- [Evaluation & Observability (29)](https://logicrw.github.io/awesome-jev-projects/en/categories/evaluation-observability) — Evaluation & Observability (29) — System One / Jev related resource.
- [Every: Mini-Vibe Check](https://every.to/also-true-for-humans/mini-vibe-check-typesafe-s-jev-judged-everything-i-ve-written-in-0-7-seconds) — , 777 judgments over 37 articles in 0.7s for a quarter of a cent; caught six of seven planted defects, Fable seven.…
- [Jev is the fish at the poker table](https://backnotprop.com/blog/jev-poker) — , Poker probe finding 15 to 30 point swings from relabelling the same hand, and 16 of 16 bets against a made flush.…
- [Jev Judge vs Dimension Scores](https://agentjournal.dev/blog/llm-judge-vs-feature-extraction) — Independent measurement on three classification tasks: one direct Jev question per row against 12–14 Jev-scored dimensions with locally fitted weights, 5,477 test rows and 34.1M input tokens for $1.43; decomposition reached 0.9076…
- [Near Here event validation](https://nearhere.events/blog/typesafe-jev-mistral-gemini-event-validation) — The only three-way head-to-head found, with each model's prompt tuned separately and the scope limited to one task rather than a general ranking.
- [Workflow evals](https://evals.typesafe.ai) — , TypeSafe's own four-workflow dashboard, Jev at 61.7 to 76.0% accuracy and 0.3 to 0.5s per case against frontier baselines.…

### Papers

- [Calibration-Aware RL for Decision-Making LLMs](https://arxiv.org/abs/2601.13284) — , "Balancing Classification and Calibration Performance in Decision-Making LLMs via Calibration Aware Reinforcement Learning". RL that adjusts decision-token probabilities directly, keeping RLVR accuracy while cutting ECE, the closest…
- [Constitutional Classifiers](https://arxiv.org/abs/2501.18837) — , "Defending against Universal Jailbreaks across Thousands of Hours of Red Teaming". Input and output classifiers gating a frontier model on a fixed policy, the deployed slot Noul targets. !
- [DSPy](https://arxiv.org/abs/2310.03714) — , "Compiling Declarative Language Model Calls into Self-Improving Pipelines". Typed signatures compiled into prompts, named on the HN thread as the fair comparison for Jev's typed question interface. ![ICLR…
- [Generative or Discriminative?](https://arxiv.org/abs/2506.12181) — , "Revisiting Text Classification in the Era of Transformers". Controlled comparison of encoder, autoregressive and diffusion classifiers over fixed label sets on accuracy, calibration and ordinality. ![EMNLP…
- [GLiClass](https://arxiv.org/abs/2508.07662) — , "Generalist Lightweight Model for Sequence Classification Tasks". The open analogue HN pointed at: labels and text in one encoder pass, one probability per label, no decoding. !
- [GLiNER](https://arxiv.org/abs/2311.08526) — , "Generalist Model for Named Entity Recognition using Bidirectional Transformer". The span-and-label encoder family HN mapped Jev onto, types supplied at inference and scored in one bidirectional pass. !
- [GPT-4 Technical Report](https://arxiv.org/abs/2303.08774) — . Reports that RLHF destroys the base model's calibration, the finding RLCD is positioned against. ![arXiv](https://img.shields.io/badge/arXiv-2303.08774-B31B1B?style=flat-square) [![Daily…
- [InstructGPT reward model](https://arxiv.org/abs/2203.02155) — , "Training language models to follow instructions with human feedback". A Bradley-Terry head emits one scalar per response in a single pass, no text, co-authored by Jev's founder. !
- [JSONSchemaBench](https://arxiv.org/abs/2501.10868) — , "A Rigorous Benchmark of Structured Outputs for Language Models". 10k real schemas scored on validity, coverage and latency, the constrained-decoding route Jev's 0% type errors claim competes against. !
- [Let Me Speak Freely?](https://arxiv.org/abs/2408.02442) — , "A Study on the Impact of Format Restrictions on Performance of Large Language Models". Measures the accuracy format restrictions cost, the study behind the CEO's HN claim that constrained decoding makes models dumber. ![EMNLP 2024…
- [LLaDA](https://arxiv.org/abs/2502.09992) — , "Large Language Diffusion Models". The typesafe-ai GitHub org forked this masked diffusion LM, the strongest public hint at how Jev fills every answer slot in one pass. !
- [Llama Guard](https://arxiv.org/abs/2312.06674) — , "LLM-based Input-Output Safeguard for Human-AI Conversations". Fixed safety taxonomy with the verdict read off one safe/unsafe token probability, the guardrail classifier Noul replaces. !
- [Mercury](https://arxiv.org/abs/2506.17298) — , "Ultra-Fast Language Models Based on Diffusion". HN read Jev as a stripped down text diffusion model, and Mercury is that idea shipped commercially with parallel refinement. !
- [monoBERT](https://arxiv.org/abs/1901.04085) — , "Passage Re-ranking with BERT". Landmark cross-encoder: pair in, one scalar relevance probability out, no generation, the ancestor of Jev's Score primitive. !
- [MT-Bench](https://arxiv.org/abs/2306.05685) — , "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena". The landmark LLM-as-a-judge paper, named on the launch thread as the layer Jev's score and Noul primitives replace. ![NeurIPS…
- [Outlines](https://arxiv.org/abs/2307.09702) — , "Efficient Guided Generation for Large Language Models". The finite-state-machine guided decoding HN named as the incumbent way to get typed values, which Jev claims to replace. !
- [Rewarding Doubt](https://arxiv.org/abs/2503.02623) — , "A Reinforcement Learning Approach to Calibrated Confidence Expression of Large Language Models". Trains confidence expression by RL on the logarithmic scoring rule, an independent rediscovery of the proper-scoring-rule reward RLCD…
- [RLCR](https://arxiv.org/abs/2507.16806) — , "Beyond Binary Rewards: Training LMs to Reason About Their Uncertainty". Adds a Brier-score reward to RLVR so the model emits calibrated confidence, the closest published relative of TypeSafe's RLCD. ![ICLR…
- [RouteLLM](https://arxiv.org/abs/2406.18665) — , "Learning to Route LLMs with Preference Data". Router scores a fixed two model set and returns win probability per option before any text is generated. ![arXiv](https://img.shields.io/badge/arXiv-2406.18665-B31B1B?style=flat-square)…
- [Thinking Fast and Slow in AI](https://arxiv.org/abs/2010.06002) — . The AI charter for System 1 components that answer from experience without search, what System One Models productizes. ![AAAI 2021](https://img.shields.io/badge/AAAI_2021-4B5563?style=flat-square)…
- [vLLM](https://arxiv.org/abs/2309.06180) — , "Efficient Memory Management for Large Language Model Serving with PagedAttention". The typesafe-ai GitHub org forked this engine; paged KV cache plus prefix caching is what makes extra questions over one shared state nearly free. !
- [Zero-shot Classification as Entailment](https://arxiv.org/abs/1909.00161) — , "Benchmarking Zero-shot Text Classification: Datasets, Evaluation and Entailment Approach". Label set given at inference, an entailment model returns one probability per label, no text generated. ![EMNLP…

## SDKs & tooling

Clients, MCP servers, skills, and integrations — including TypeSafe’s SDKs. Application-shaped projects live under [Use cases](#use-cases).

### TypeSafe SDKs & gateways

- [TypeSafe Agent Skills](https://github.com/typesafe-ai/skills) — 1.6K stars — Official agent skills for building against TypeSafe’s System One / JEV API. [Source](https://github.com/typesafe-ai/skills/blob/65a39f393687675ce170e6094757de20370365b9/skills/typesafe-ai/SKILL.md)
- [System One Adapter](https://github.com/typesafe-ai/system-one-adapter-python) — 243 stars — A drop-in TypeSafeClient replacement that backs System One calls with ordinary LLM APIs.…
- [JavaScript SDK](https://github.com/typesafe-ai/typesafe-sdk-js) — The official TypeScript client. Ships ESM, CJS and type declarations, with lowercase choice()/score()/noul() helper factories.
- [Python SDK](https://github.com/typesafe-ai/typesafe-sdk-python) — The official Python client. Sync and async clients, retry policy with retry-after support, and Choice/Score/Noul helper classes.
- [Model page](https://openrouter.ai/typesafe/jev-1.13) — Model page — System One / Jev related resource.
- [Release notes](https://github.com/typesafe-ai/typesafe-sdk-python/releases/tag/v0.7.0) — Release notes — System One / Jev related resource.
- [Release notes](https://github.com/typesafe-ai/typesafe-sdk-js/releases/tag/v0.6.0) — Release notes — System One / Jev related resource.
- [TypeSafe Console](https://console.typesafe.ai) — Create keys and inspect live Jev requests.
- [TypeSafe GitHub organization](https://github.com/typesafe-ai) — Source repositories maintained by TypeSafe.
- [TypeSafe on OpenRouter](https://openrouter.ai/typesafe) — OpenRouter's listing for Jev, with its own model ids and the unusual pricing shape of paid input and free output.
- [Vercel AI Gateway](https://vercel.com/ai-gateway/models/jev) — Third-party hosted gateway entry for calling Jev through Vercel's AI SDK and gateway.

### Community SDKs & clients

- [oh-my-pi](https://github.com/can1357/oh-my-pi) — 32.4K stars — A coding agent with an optional TypeSafe judgment provider for bounded workflow decisions. [Source](https://github.com/can1357/oh-my-pi/blob/78b753124d11f8dd3ae73e2524125890ff7c977e/packages/ai/src/judgment/typesafe.ts#L4)
- [composio](https://github.com/ComposioHQ/composio) — 30.3K stars — A TypeSafe provider that uses JEV to choose among tools and bounded argument options. [Source](https://github.com/ComposioHQ/composio/blob/4b5920bf7aa55c8a44657b060d4bd25ce7b13a9a/ts/packages/providers/typesafe/src/decide.ts)
- [Guidance](https://github.com/guidance-ai/guidance) — , Constrained generation library named on the HN launch thread as what Jev's typed outputs get compared against.…
- [eliza](https://github.com/elizaOS/eliza) — 19.4K stars — An optional TypeSafe HTTP adapter in the Eliza agent operating system. [Source](https://github.com/elizaOS/eliza/blob/ebc808e3a67fb941e29153d89fc896524d32fe3c/packages/agent/src/services/typesafe/client.ts)
- [openchamber](https://github.com/openchamber/openchamber) — 10.2K stars — An optional automatic model router that classifies a message before model selection. [Source](https://github.com/openchamber/openchamber/blob/614d7f76e581a132a86575c03d3fa9aad5e624b6/packages/web/server/lib/routing/jev.js)
- [Vercel Eve](https://github.com/vercel/eve) — Agent framework whose `auto` model router defaults to Jev through Vercel AI Gateway and whose `evaluate` helper asks typed Choice, Score, and Boolean questions inside tools; the underlying AI SDK evaluation model specification is…
- [ax](https://github.com/ax-llm/ax) — 2.9K stars — A TypeSafe integration for boolean, finite-class, and native JEV signatures. [Source](https://github.com/ax-llm/ax/blob/5c43344f9ef3016db576fa2c3b59d48ef21b4d71/src/ax/ai/typesafe/client.ts#L1)
- [http4k · TypeSafe Client](https://github.com/http4k/http4k) — 2.8K stars — A typed Kotlin client and fake implementation for the TypeSafe System One API.…
- [MAPIE](https://github.com/scikit-learn-contrib/MAPIE) — Scikit-learn-compatible library for prediction intervals and sets with guaranteed coverage, usable for the "escalate when unsure" path.
- [vellum-assistant](https://github.com/vellum-ai/vellum-assistant) — 1.3K stars — An optional JEV provider that submits conversation state and explicit questions. [Source](https://github.com/vellum-ai/vellum-assistant/blob/ee5ba342719e72b67698c2e1a4a78837321d0b1d/assistant/src/providers/jev/client.ts)
- [Agent](https://github.com/AgentiLoop/Agent) — 622 stars — An optional Jev command-risk advisor inside a native macOS Agent, with a TypeSafeKit client. [Source](https://github.com/AgentiLoop/Agent/blob/078f87ceca1d1190cc73706ac8ec16442e766a27/README.md)
- [DocJev](https://github.com/jerryjliu/docjev) — Python library, CLI, and local app that uses LiteParse for document text and Jev to classify PDF, DOCX, and PPTX files or split mixed packets; optional LlamaParse provides cloud OCR. Its published 40-document, eight-packet comparison…
- [openai-scala-client](https://github.com/cequence-io/openai-scala-client) — 248 stars — A dedicated TypeSafe module in a Scala client that supports multiple AI providers. [Source](https://github.com/cequence-io/openai-scala-client/blob/cfabe8842344da713615d0121a7804840649eb46/README.md)
- [Vercel AI SDK for Python](https://github.com/vercel-labs/ai-python) — Vercel's public-beta Python SDK includes an experimental `evaluate` operation that asks typed Choice, Score, and Boolean questions through AI Gateway using `typesafe-ai/jev`; the evaluation API is still experimental and requires Gateway…
- [interlinked-cli](https://github.com/QuentinCody/interlinked-cli) — 177 stars — Interlinked adds optional Jev judgments and evidence checks to local coding-agent checks. [Source](https://github.com/QuentinCody/interlinked-cli/blob/207330d8131c5203ecc74e9fd4c24ba416463718/src/harness/jev/client.ts#L14)
- [NeuroLink](https://github.com/juspay/neurolink) — TypeScript SDK that exposes Jev as a third inference type alongside `generate` and `stream`, declared per provider through an `inferenceKinds` field rather than inferred from behaviour, and consumes it internally for model routing,…
- [Advocaat](https://github.com/pithings/advocaat) — TypeScript `ask` client that batches typed Jev choice, score, and yes/no questions about structured data, with optional Vercel AI Gateway support. Project guide.
- [Blink](https://github.com/ellipsis-dev/blink) — Bun CLI that searches a codebase with TypeSafe Jev walkers (Choice over directory entries via `@typesafe-ai/sdk`); upstream licensing unspecified. Project guide.
- [Save Token JEV Clean](https://github.com/IAmUnbounded/save-token-jev-clean) — 62 stars — A context cleaner that asks JEV which history to retain, truncate, or drop. [Source](https://github.com/IAmUnbounded/save-token-jev-clean/blob/a7007354a8d3747f06ff82130561edb2822a17df/src/client.ts)
- [ruby\_decision\_model](https://github.com/obie/ruby_decision_model) — Stdlib-lean Ruby client for Noul/Choice/Score decision models via Typesafe or OpenRouter. Project guide.
- [pi-typesafe](https://github.com/DevMortimer/pi-typesafe) — Pi extension and library that gives the agent and other extensions one consented, key-managed TypeSafe client with a batched `typesafe_evaluate` tool and offline-testable transport; requests are billable and opt-in per user.
- [Spring AI TypeSafe](https://github.com/spring-ai-community/spring-ai-typesafe) — Unofficial Java/Spring AI System One client with JevJudge, guardrail/RAG advisors, and starter (Maven `org.springaicommunity`; distinct from jev-java). Project guide.
- [synkora-ai](https://github.com/getsynkora/synkora-ai) — Synkora includes optional TypeSafe client tools for classification, scoring and yes/no judgments.
- [TypeSafe (Swift)](https://github.com/krzyzanowskim/TypeSafe) — SwiftPM client for TypeSafe System One Noul/Choice/Score questions, aligned with the official JS SDK shape. Project guide.
- [jgrep](https://github.com/kyu1204/jgrep) — Semantic grep CLI (`npm install -g jevgrep`) that splits files or git diff hunks into 5–60 line chunks, packs several chunks into one request with a Noul question per chunk, and prints `file:line` hits above a probability threshold with…
- [jev-cli](https://github.com/Nasrallah-AL/jev-cli) — TypeScript CLI (`npm install -g jevctl`) that turns Jev judgments into pipeable, exit-code-gated shell commands: `verify` claims against evidence, `screen` text for prompt injection before an agent reads it, `classify`, `extract`,…
- [jev-superpowers](https://github.com/AkashPriyadarshii/jev-superpowers) — Skills framework for coding agents with typed gates on package choices and task completion.
- [swift-typesafe](https://github.com/ainame/swift-typesafe) — A community Swift TypeSafe client with typed questions, dynamic questions and response parsing.
- [evoke](https://github.com/evoke-build/evoke) — Rust CLI and TypeScript SDK that ask Jev to select an installed reflex and bounded arguments, then gate the outcome in code as run, confirm, ask, or abstain. Reflexes fetched from Git run as your user without a sandbox, so inspect them…
- [go-jev](https://github.com/mattn/go-jev) — Go SDK and CLI for TypeSafe Jev: typed decisions (yes/no, choice, score) from a model
- [jevframe](https://github.com/ktaletsk/jevframe) — Early Python library adding async Jev Noul, Choice, Score, and multi-question evaluation to pandas and eager Polars, with full Choice and Score probability distributions, bounded row concurrency, and opt-in memory caching; each uncached…
- [TypeSafe AI for Rust](https://github.com/Twister915/typesafe-ai) — Rust client with asynchronous and blocking transports, typed responses, observable retries, and inspectable errors.
- [rift](https://github.com/exYze/rift) — An optional TypeSafe decision client in the Rust coding terminal Rift for bounded Jev judgments.
- [swift-jev](https://github.com/d-date/swift-jev) — A Swift client for TypeSafe AI's Jev — typed judgements, not text
- [AnyDecisionModel](https://github.com/mattt/AnyDecisionModel) — Swift 6.2 package with typed sessions, enum-backed choices, and ordered scores over either TypeSafe's Jev API or a local MLX language model on Apple silicon; the local backend reads answer-token probabilities without generating text,…
- [typesafe-sdk-go](https://github.com/Tangerg/typesafe-sdk-go) — A Go TypeSafe SDK for defining typed questions and reading Jev choices, scores, and probabilities.
- [typesafeai-dotnet-sdk](https://github.com/saibimajdi/typesafeai-dotnet-sdk) — Community .NET SDK for TypeSafe AI and Jev, providing asynchronous typed evaluation for Choice, Score, and Noul primitives.
- [jevgo](https://github.com/devbackend/jevgo) — Unofficial Go client for TypeSafe System One: typed Noul/Choice/Score in one call (stdlib HTTP). Project guide.
- [typesafe-sdk](https://github.com/joshmn/typesafe-sdk) — Community Ruby client for TypeSafe's System One API with typed Noul, Choice, and Score questions, retries, model listing, and thread-safe pooled HTTP connections; requires Ruby 3.1 or newer and has no async client.
- [JevOps](https://github.com/endomorphosis/JevOps) — Jev is a \\gate\\, not a generator. This package does \\not\\ write Lean. Lake (or another oracle) lives in the implementation that \uses\ the kernel.
- [scala-jev-sdk](https://github.com/ticofab/scala-jev-sdk) — Community Scala 3 client for TypeSafe's System One API with typed Noul, Choice, and Score questions whose answers are retrieved with the question value itself, no effect system of its own so the same code runs on any sttp backend from…
- [jev-ai-sdk-form-router](https://github.com/vercel-labs/jev-ai-sdk-form-router) — Route form submissions to the right people with Jev and AI SDK.
- [jev-go](https://github.com/Stumble/jev-go) — A community Go SDK and CLI supporting TypeSafe directly and Vercel AI Gateway.
- [jev-tool-permissions](https://github.com/NicolasMontone/jev-tool-permissions) — Adds tool-call approval and tool-list pruning to the Vercel AI SDK.
- [jev4k](https://github.com/pambrose/jev4k) — Kotlin DSL/client for TypeSafe Jev Noul/Choice/Score (Maven Central `com.pambrose:jev4k`; distinct from jev-java / jev-android). Project guide.
- [questions](https://github.com/nitoba/questions) — A TypeScript decision library that asks typed questions via Zod or native batches, defaulting to TypeSafe Jev, with optional Vercel or generative adapters.
- [typesafe-ai-rs](https://github.com/gilljon/typesafe-ai-rs) — An independently maintained Rust SDK with async and blocking clients, retries and response metadata.
- [typesafe_sdk](https://github.com/nshkrdotcom/typesafe_sdk) — Elixir SDK for TypeSafe AI and Jev with typed Choice, Score, and Noul structs, configurable retries, and upstream API parity.
- [goodall](https://github.com/bensyverson/goodall) — An optional TypeSafe package in a Go Agent library, using Jev as a tool or routing judge alongside chat models.
- [jev-android](https://github.com/dougsong/jev-android) — Kotlin Android UI-agent SDK: TypeSafe Jev or DeepSeek selects accessibility actions; local Maven sample (not on Maven Central). Project guide.
- [jev-go](https://github.com/Gaurav-Gosain/jev-go) — A Go TypeSafe System One client with typed questions, answers and batching helpers.
- [LlamaIndex Jev](https://github.com/WiktorB2004/llama-index-jev) — Unofficial LlamaIndex reranker and query-engine selector on the official Python SDK: Jev scores retrieved passages and chooses which tool handles a query; score mode is a 0–3 rubric, not cosine similarity.
- [TypeSafe AI Swift SDK](https://github.com/alterhq/typesafe-sdk-swift) — Dependency-free Swift 6 client for Choice, Score, and Noul questions with strict concurrency, configurable retries, and network-free transport tests; production Apple apps should proxy requests through a backend.
- [TypeSafe SDK for Java](https://github.com/Premo-Cloud/typesafe-sdk-java) — Community Java 17 client for TypeSafe's System One API with typed Noul, Choice, and Score questions, lambda-style builders for nested criteria, retries matching the official SDKs, status-specific exceptions, and a Spring Boot starter;…
- [zio-typesafe-ai](https://github.com/jamesward/zio-typesafe-ai) — A Scala 3 / ZIO client that asks typed Noul, Choice, and Score questions in one round-trip and returns a NamedTuple of answers.
- [jev](https://github.com/virolea/jev) — Ruby client for the typesafe AI Jev model
- [jev-java](https://github.com/gudcks0305/jev-java) — Unofficial Java 17+ SDK for TypeSafe Jev with OpenRouter/Vercel adapters and optional Spring Boot starter (`jev-typesafe` 0.1.1). Project guide.
- [tripwire](https://github.com/noelzappy/tripwire) — Runs seven checks on every LLM response in one Jev call, as AI SDK middleware or an OpenAI-compatible proxy.
- [typesafe-ai-rails](https://github.com/GenieRobot/typesafe-ai-rails) — Community Rails integration for TypeSafe's System One API, built on typesafe-sdk, with Rails configuration, persisted usage and cost telemetry, and opt-in confidence policies for Choice and Score answers.
- [typesafe-sdk-rust](https://github.com/codeitlikemiley/typesafe-sdk-rust) — A Rust client for TypeSafe with asynchronous and optional blocking calls plus typed question and answer wrappers.
- [Janus](https://github.com/FirasSX914/Janus) — Independent calibration measurement of Jev on two labelled datasets, Banking77 and Web of Science, with a Jev to frontier cascade priced per row from measured tokens, now also packaged as an installable tool (`pip install janus-decide`)…
- [jear](https://github.com/iJ03l/jear) — Rust Jev-routed client for NEAR AI Cloud inference and IronClaw agents using budget/quality/sensitivity decisions. Project guide.
- [jev-sdk-java](https://github.com/luigivis/jev-sdk-java) — Unofficial Java 21 System One client with sealed Question/Answer types (TypeSafe-only; source-build until Maven Central lists 0.1.0). Project guide.
- [jev-starter](https://github.com/hamakyo/jev-starter) — TypeScript patterns for thresholds, fallbacks, human review and evaluation on top of the TypeSafe SDK.
- [jevclient](https://github.com/AboveColin/jevclient) — An asynchronous Python Jev client that batches typed questions in one request.
- [jevgo](https://github.com/fgn/jevgo) — A community Go client with a standard-library core and optional Langfuse tracing.
- [typesafe-go](https://github.com/2389-research/typesafe-go) — A TypeSafe System One client that uses only the Go standard library to send Jev questions and read structured answers.
- [typesafe-go](https://github.com/zhirschtritt/typesafe-go) — An unofficial Go client without third-party dependencies for System One calls and model discovery.
- [TypeSafe.AI (.NET SDK)](https://github.com/typesafe-sdk-csharp/typesafe-sdk) — Unofficial .NET System One client (NuGet TypeSafe.AI) with DI, resilience, and OTel; distinct from TypeSafeAI.Net. Project guide.
- [TypeSafeAI.Net](https://github.com/Hawxy/TypeSafeAI.Net) — .NET client for TypeSafe's API with Noul, Choice, and Score question sets, HttpClientFactory and dependency injection support, plus Microsoft.Extensions.AI guardrail, routing, tool, and evaluator adapters.
- [jev](https://github.com/kataras/jev) — A Go client for the TypeSafe AI's System One API and its model, Jev.
- [Jev Symfony Bundle](https://github.com/vbcherepanov/jev-symfony-bundle) — Unofficial Symfony bundle for TypeSafe Jev: typed client, validator constraints, Messenger, Workflow guards, and profiler. Project guide.
- [jev-go](https://github.com/guillemus/jev-go) — A small unofficial Go SDK for Jev calls and model listing.
- [jev-go-sdk](https://github.com/ajayk/jev-go-sdk) — Dependency-free Go client for TypeSafe AI's System One API and the Jev model
- [jev-is-not-odd](https://github.com/ItzSupra13/jev-is-not-odd) — A probabilistic, AI-powered utility to determine if a number is not odd (or not even) using TypeSafe's Jev model and the Vercel AI SDK.
- [jev\_dart](https://github.com/Solido/jev_dart) — Jev Dart SDK to build cli, server and Flutter apps.
- [jevgrep (allebee)](https://github.com/allebee/jevgrep) — Streaming grep-by-meaning CLI (`jevgrep-cli` on PyPI) for logs and other text, including `tail -f`: it batches one Jev Noul per line and prints lines above a code-set threshold. Its hand-labelled, 195-line synthetic-log benchmark…
- [Swift SDK](https://github.com/marandaneto/typesafe-sdk-swift) — Unofficial, experimental Swift client with typed answers, async/await, and Swift Package Manager support.
- [System One Playground](https://github.com/DonaldMurillo/system-one-playground) — SysOneScript CLI/VS Code plus Go TypeSafe System One client and Studio; start offline, add live Jev when needed. Project guide.
- [TypeSafe Go](https://github.com/stacklok/typesafe-go) — Unofficial Go System One client (Stacklok): explicit auth options, no implicit env reads; distinct from jevgo. Project guide.
- [TypeSafe SDK for Go](https://github.com/SergeAx/typesafe-sdk-go) — Community Go 1.23 client for TypeSafe's System One API with typed Noul, Choice, and Score questions in a single request, options-over-environment configuration, retries that honor `Retry-After`, an `errors.Is`-matchable error tree, and…
- [typesafe-go](https://github.com/cole-gillespie/typesafe-go) — An unofficial Go SDK with typed answers, retries and context cancellation.
- [typesafe-rs](https://github.com/AbdelStark/typesafe-rs) — A community Rust Jev client with async requests, an optional blocking interface and local mock testing.
- [typesafe-sdk-java](https://github.com/kgonia/typesafe-sdk-java) — Zero-dependency Java client (Java 21+).
- [typesafe-sdk-php](https://github.com/Butochnikov/typesafe-sdk-php) — A community TypeSafe SDK for PHP 8.2+, with synchronous calls and Guzzle-based async requests.
- [kunobi-jev](https://github.com/kunobi-ninja/kunobi-jev) — Rust client, published on crates.io.
- [OCaml SDK](https://github.com/jonesmelton/verdict) — Unofficial eio-based client.
- [pkg-gate](https://github.com/hemanth/pkg-gate) — Pre-install security gate for npm lifecycle scripts using TypeSafe System One. Evaluates preinstall, install, and postinstall hooks across intent, threat severity, secret access, and remote execution to intercept supply-chain attacks…
- [TypeSafe SDK for Kotlin](https://github.com/ufec/typesafe-sdk-kotlin) — Community Kotlin port of the official JavaScript SDK covering TypeSafe's System One API with typed Noul, Choice, and Score questions, a retry policy matching upstream, status-specific exceptions, HTTP and SOCKS5 proxy support, and…
- [TypeSafe SDK for PHP](https://github.com/Fox-Islam/typesafe-sdk-php) — Community PHP 8.3 client for TypeSafe's System One API with typed Noul, Choice, and Score questions, a one-call switch between TypeSafe and OpenRouter's decisions endpoint, retries and per-call overrides, any PSR-18 transport, and a…
- [typesafe-ai-ruby](https://github.com/hnegishi/typesafe-ai-ruby) — A stdlib-only Ruby client that sends Choice, Score, or Noul questions to TypeSafe System One.
- [typesafe-api (Rust)](https://github.com/noahbclarkson/typesafe-api-rs) — Ergonomic Rust client for TypeSafe System One typed questions and answers (`typesafe-api` 0.1.0). Project guide.
- [typesafe-go](https://github.com/Nibir1/typesafe-go) — A zero-dependency community Go SDK, including a static analyser that flags poorly designed questions at compile time.
- [typesafe-go](https://github.com/Shubham510/typesafe-go) — Go client.
- [TypeSafeSDK](https://github.com/DotNetVibeCoderz/Vibe_SDK) — An unofficial .NET client that POSTs state and typed questions to TypeSafe /v1/systemone. The parent repo also contains unrelated SDK dumps.
- [Jev on Netlify AI Gateway](https://netlify.com/changelog/typesafe-jev-ai-gateway) — Zero-config access from a Netlify function: use the official SDK with no API key, base URL or provider setup, billed through Netlify credits.
- [Jev on Vercel AI SDK](https://ai-sdk.dev/providers/ai-sdk-providers/typesafe-ai) — The AI SDK provider package for calling TypeSafe directly, with a sample covering all three question types and nested criteria shapes.
- [TypeSafe-compatible API on Vercel AI Gateway](https://vercel.com/docs/ai-gateway/sdks-and-apis/typesafe) — Point the official TypeSafe SDK at Vercel by changing one baseURL, or call the gateway's systemone endpoint directly with cURL.

### MCP, skills & agent plugins

- [Hermes Agent: Jev compaction evaluation](https://github.com/NousResearch/hermes-agent) — Ported the Jev compaction approach, measured it against their shipping summariser, and published the conclusion not to adopt it.
- [OpenCode Zen: Jev resale](https://github.com/anomalyco/opencode) — A coding agent whose hosted gateway resells Jev, including a free tier model id.
- [jev-model-router](https://github.com/davila7/claude-code-templates) — Three independently installable Claude Code plugins — guardrails, model router and skill suggestion — each with its own hooks and tests.
- [Openwork](https://github.com/different-ai/openwork) — 23.7K stars — An open-source cowork-style agent workspace that can run JEV-backed reviews inside CI and skill workflows.…
- [fast-jev-compaction](https://github.com/tamaratran/fast-jev-compaction) — Claude Code plugin that replaces the compaction summary with Jev decisions. Every tool call and result is scored; stale ones are dropped or truncated, and everything kept stays verbatim.
- [jev-desktop](https://github.com/lahfir/agent-desktop) — Rust macOS accessibility CLI for desktop computer use; optional jev-desktop skill/scripts use TypeSafe Jev for target/command choice without putting the a11y tree in agent context (BYOK). [Project…
- [RNSkill · JEV Office Gate](https://github.com/Pluviobyte/rnskill) — 1.6K stars — An agent-skill collection containing a JEV gate for bounded office-document checks. [Source](https://github.com/Pluviobyte/rnskill/blob/83d1783b892bbaa29a137895ff8338264b6872fa/skills/jev-office-gate/scripts/jev_office_gate.py)
- [AI CLI](https://github.com/vercel-labs/ai-cli) — 810 stars — A terminal generator CLI that ships with an agent skill for creating content from the command line. [Source](https://github.com/vercel-labs/ai-cli/blob/6a0ed5d04ea60ee536029d469499b82898d1b214/skills/ai-cli/SKILL.md)
- [Hermes Jev Skills](https://github.com/kerpopule/hermes-jev-skills) — Agent skills and `jev` CLI using TypeSafe Jev for model routing, memory filtering, compaction, skill selection, triage, and computer/browser action choice on Hermes, Claude Code, and Codex. [Project…
- [Jev-cu](https://github.com/Sac-Y/Jev-cu) — Experimental Codex skill and JavaScript runtime for selecting macOS Accessibility targets with Jev, with action previews and optional result verification; execution-policy limitations require review. [Project…
- [jev-skill](https://github.com/wuyoscar/jev-skill) — An agent skill plus CLI that validates all three primitives, requires explicit consent before a billed call, and forbids inventing output when simulating.
- [vexjoy-agent](https://github.com/notque/vexjoy-agent) — Agent toolkit for Claude Code/Codex: `/do` routes work to specialist agents/skills; optional `/d` uses TypeSafe Jev to classify and gate intent before dispatch. Project guide.
- [jev-router](https://github.com/gargpratyush/jev-router) — 316 stars — A Claude Code and CLI proxy that asks Jev to score task complexity and pick a model from the account’s available set.…
- [jev-mcp](https://github.com/jkudish/jev-mcp) — Node MCP server with ten bounded Jev tools for checking claims against supplied evidence, screening content, choosing candidates, reranking, extraction, and patch review; it can use TypeSafe or configured gateways, but its judgments do…
- [TypeSafe MCP](https://github.com/itsmostafa/typesafe-mcp) — MCP server that lets agents such as Claude Code, Claude Desktop, and Codex call Jev directly for Choice, Score, and Noul decisions.
- [Jev Codex Router](https://github.com/0xNatoshi/jev-codex-router) — Routes each Codex turn through Jev tier and thinking-depth selection via a local Codex Router generic provider, with fail-open fallbacks and an optional Codex-dry tandem. Project guide.
- [Skillbox](https://github.com/kitze/skillbox) — Self-hosted agent skill library with opt-in Jev recommendations over task text and authorized active skill descriptions, using an owner-provided TypeSafe, OpenRouter, or Vercel AI Gateway key. Failed, oversized, or rate-limited…
- [jev-review](https://github.com/NiazMorshed2007/jev-review) — 196 stars — A local MCP code-quality reviewer returning structured scores to coding Agents. [Source](https://github.com/NiazMorshed2007/jev-review/blob/57690af54ef7d862c2483342c1e61c14dffcf727/README.md)
- [jev-gateway](https://github.com/vinilana/jev-gateway) — Local LLM gateway that asks TypeSafe Jev which tool to call for Codex, Claude Code, OpenCode, or Gemini while other traffic uses your usual LLM. Project guide.
- [JevRouter](https://github.com/BillionsBobby/JevRouter) — Routes each agent step to a model, subagent, Skill, MCP tool, or CLI with one Jev Choice, requiring confirmation for risky capabilities and keeping decision receipts.
- [Compact Adviser](https://github.com/kunchenguid/compact-adviser) — Agent plugin that asks Jev whether the session is at a safe point to `/compact`, and can run it automatically on Pi and Claude Code.
- [runline](https://github.com/Michaelliv/runline) — 163 stars — A TypeSafe plugin exposing Jev decisions as callable actions in Runline Agent JavaScript. [Source](https://github.com/Michaelliv/runline/blob/6bdddfa82cd95b6b9a07e57fd93a271ae83a0d1b/README.md)
- [jev-dsh-decision](https://github.com/Devin-AXIS/jev-dsh-decision) — Decision plugin for agent harnesses: Jev picks the tool, skill or owner and scores the output, while the agent keeps planning and execution. Ships for DeepSeek Harness and iPolloWork.
- [Building with JEV Skill](https://github.com/dbreunig/building-with-jev-skill) — 128 stars — An agent skill for writing and improving programs that call JEV / System One. [Source](https://github.com/dbreunig/building-with-jev-skill/blob/04fe3666c6b8b8abfec1271c0e581c823a181f6d/skills/jev/SKILL.md)
- [SkillRanker](https://github.com/Dicklesworthstone/skillranker) — Rust CLI that uses Jev Choice and Noul judgments to shortlist and rerank agent skills against the current task, with a real none option, local replay, and opt-in network disclosure; fresh ranking sends redacted session context and skill…
- [Formanator](https://github.com/timrogers/formanator) — CLI and MCP client for Forma benefit claims: with merchant and description supplied, optional Jev Choice selects from the account's valid benefit/category pairs, then code falls back to an LLM for no match or low confidence. Jev…
- [jev-browser](https://github.com/Ying-Kai-Liao/jev-browser) — 67 stars — A browser automation library, CLI, and MCP server pairing LLM plans with JEV actions. [Source](https://github.com/Ying-Kai-Liao/jev-browser/blob/578cff6e701a131733d03256078bb559a45ad188/src/jev.mjs)
- [Winnow](https://github.com/GhalebDweikat/winnow) — Claude Code context sieve: TypeSafe Jev (or System One adapter) judges tool-result blocks before they enter context; hidden text stays recallable. Project guide.
- [Canny](https://github.com/qkal/Canny) — Claude Code and Codex hooks that record edits and checks in an append-only ledger, flag a "done" claim without a passing check after the last code edit, and use optional Jev Noul judgments for advisory rule checks or to recognize a…
- [Agent Router](https://github.com/nidhi-singh02/agent-router) — Quota-aware Herdr launcher that uses TypeSafe System One (Jev) to pick Cursor/Claude Code/Codex/OpenCode model and effort after local eligibility rules. Project guide.
- [jevgrep](https://github.com/nassim-arifette/jevgrep) — Jev-powered semantic code search for coding agents — find behavior across repositories via CLI or MCP, with exact source excerpts and line numbers.
- [oxlint-plugin-jev](https://github.com/wobsoriano/oxlint-plugin-jev) — Experimental Oxlint plugin that asks Jev Noul questions about functions, calls, JSX elements, or files and reports matches above a chosen cutoff. It sends matched snippets to TypeSafe; API failures skip checks by default, so set `ci:…
- [agent-dispatcher](https://github.com/nahid-sparktales/agent-dispatcher) — Routes a Claude Code or Codex task to one of 27 specialist roles and defines what evidence will count as done.
- [jev-rules](https://github.com/EliaAlberti/jev-rules) — Selects Claude Code project rules and map documents with Jev judgments over prompts and file paths, with session caching and fallback context. Project guide.
- [pi-jev](https://github.com/TheoOliveira/pi-jev) — Semantic tool routing and skill discovery for the Pi coding agent: Jev picks which inactive tools to activate for the prompt at hand.
- [jev-mcp (burnigtm)](https://github.com/burnigtm/jev-mcp) — MCP server whose tools route the next step and decide whether a partner model is needed, for Cursor, Codex, and any MCP client.
- [jev-seo](https://github.com/AkashPriyadarshii/jev-seo) — Agent-oriented SEO/GEO CLI and MCP with local DuckDuckGo helpers and optional TypeSafe Jev scoring. Project guide.
- [Jevbridge](https://github.com/gamesonrblx/Jevbridge) — Exposes a shared structured-decision interface for Jev and other models through ACP, MCP and a CLI.
- [Jevbridge](https://github.com/tacticocc/Jevbridge) — ACP and MCP adapter that pairs Jev with any LLM agent, including Codex, Claude, Grok, and OpenCode, for typed decisions and computer use.
- [ask-jev-skill](https://github.com/shantanugoel/ask-jev-skill) — Hermes skill that asks TypeSafe Jev for typed Choice/Score/Noul tiebreaks when paths remain plausible. Project guide.
- [jev-skill-suggester](https://github.com/win4r/jev-skill-suggester) — A Python CLI and Codex Skill that recommends a suitable installed skill for the current task using TypeSafe Jev Choice and Noul checks without executing candidate skills.
- [jev-guard](https://github.com/leepokai/jev-guard) — Coding-agent security hooks: TypeSafe Jev risk-scores tool calls with session context (deny/ask/allow), flags prompt injection, and scans skills across Claude Code, Codex, Cursor, and more. [Project…
- [Sniff Test](https://github.com/DanRWilloughby/snifftest) — Prose linter with local countable rules and opt-in Jev Noul judgments over individual paragraphs, available as a CLI, pre-commit hook, and GitHub Action; its author-published comparison uses a small seeded corpus, with some judgment…
- [jevify](https://github.com/altryne/jevify) — Agent skill for finding where Jev fits in an existing codebase, designing the typed questions, and measuring whether it helped.
- [jev-use](https://github.com/shitianfang/jev-use) — Claude Code, Codex, and pi plugin that hands the steps needing no text output to Jev: `jev_judge` batches typed noul, choice, and score questions about one state into a single call, `jev_gate` is an opt-in PreToolUse gate that can only…
- [yoshi](https://github.com/compozy/yoshi) — Experimental local context-pruning proxy for Claude Code and Codex; TypeSafe Jev (Vercel AI Gateway) judges which history spans to omit. Project guide.
- [jev-judge-mcp](https://github.com/PyModel/jev-judge-mcp) — Typed judgment tools for MCP agents. TypeSafe's Jev model as verify, screen, find, classify, rerank, decide, compare, extract, review, gate, and score: the model judges, policy decides auto, review, or escalate.
- [Jev MCP](https://github.com/blakestone-x/jev-mcp) — Python MCP server exposing classify, score, check, match, and screen tools to MCP-compatible agents.
- [slop-grader](https://github.com/lukstei/slop-grader) — Rule-based CLI and agent skill that evaluates text and markdown files against custom rulesets for AI slop, grammar, and technical doc quality using Jev scores and line-by-line violation flags, then guides an AI agent to auto-fix violations.
- [agent-chaperone](https://github.com/agent-chaperone/agent-chaperone) — Calibrated firewall for agent tool calls: MCP proxy plus hooks adapter; TypeSafe Jev screening with shadow mode and a local judgment log. Project guide.
- [Pi Jev Guard](https://github.com/zszz3/Pi-Jev-Guide) — Pi coding-agent plugin with rules configured by timing, plus risk checks, output redaction, and reminders on repeated failures. Chinese documentation.
- [JCR](https://github.com/NiazMorshed2007/jcr) — Jev Capability Resolver: TypeSafe Jev searches a nested capability tree and returns deterministic command documentation for agents (MCP + harnesses). Project guide.
- [jev-belay](https://github.com/valentynkit/jev-belay) — Claude Code Stop hook that checks the transcript for evidence before trusting a "done" claim, spending one four-question Jev call only when files changed with no passing check since, and failing open on every error path.
- [jevwire](https://github.com/Brainwires/jevwire) — An MCP server, an embeddable decision library, and an escalate-only Claude Code plugin in one repository.
- [Jev Agent Skill Router](https://github.com/GodsBoy/jev-agent-skill-router) — Routes a request to the agent skills it needs, with a confidence floor below which it loads nothing.
- [lorenzini](https://github.com/Nanako0129/lorenzini) — Claude Code skills that wait for CodeRabbit, Copilot or Codex to finish reviewing a pull request, then judge whether the verdict actually permits a merge.
- [jev](https://github.com/BorisLeMeec/jev) — A Go Claude Code plugin using Jev to find files, answer bounded questions across code and handle large reads.
- [jev-studio](https://github.com/utk2103/jev-studio) — One pip install for experimenting: MCP tools for Choice, Noul and Score, prompt libraries and a slash command per cookbook recipe.
- [jevvy](https://github.com/PanAchy/jevvy) — Plugins for coding agents, starting with one that auto-approves shell permission requests it judges harmless and passes everything uncertain to the normal flow.
- [hermes-jev-approvals](https://github.com/anpicasso/hermes-jev-approvals) — Approvals provider for Hermes Agent: it judges shell commands and refuses every other task, registering no hooks.
- [jev-cli](https://github.com/tumf/jev-cli) — Unofficial PyPI CLI + stdio MCP for TypeSafe Jev noul/choice/score (distinct from okooo5km/jev, typesafe-cli, typesafeai-cli). Project guide.
- [typesafe-skill-router](https://github.com/DECRUX9812/typesafe-skill-router) — An opt-in Hermes Agent plugin that asks Jev to suggest one relevant skill before a model call.
- [jev-commit](https://github.com/valentynkit/jev-commit) — A commit-msg hook that scores the message against the staged diff with one Jev request of five Nouls and warns by default. Default blocking is a local regex belt on high-precision added-line hits; the secret\_shaped Noul blocks only…
- [jev (okooo5km)](https://github.com/okooo5km/jev) — Stdlib Python CLI + Agent Skill for TypeSafe Jev `yes`/`pick`/`score` via TypeSafe API or OpenRouter (distinct from typesafe-cli / typesafeai-cli). Project guide.
- [jev-security-scan](https://github.com/win4r/jev-security-scan) — Reviews Agent Skills and MCP configurations and source code with local static checks and TypeSafe Jev before installation or execution, reporting file and line evidence, risk categories, model probabilities, and coverage gaps.
- [Augustus](https://github.com/24601/Augustus) — Agent skill for choosing where typed judgments fit beside code, policy, and generation, with Jev examples on question design and abstention plus an offline probability/threshold evaluator.
- [jev-project-context](https://github.com/poiuyjie/jev_project_context) — Evidence-first experiment memory skill for coding agents with optional TypeSafe Jev semantic triage. Project guide.
- [pi-jev-sentinel](https://github.com/harshwasan/pi-jev-sentinel) — Adds TypeSafe Jev checks for Pi, Claude Code, and Codex tool calls, tool outputs, and replies, with secret scrubbing and fail-closed asks when unconfigured. Project guide.
- [jev-compact](https://github.com/fatelei/jev-compact) — Codex CLI plugin: TypeSafe Jev scores tool calls before compaction and restores critical outputs verbatim afterward (distinct from fast-jev-compaction for Claude Code). Project guide.
- [omp-jev-compaction](https://github.com/jerryfane/omp-jev-compaction) — omp plugin: verbatim TypeSafe/OpenRouter Jev-scored tool-context reduction with sticky cache-friendly rewrites (distinct from fast-jev-compaction / jev-compact). Project guide.
- [ego-jev](https://github.com/ZephyrDeng/ego-jev) — Jev (TypeSafe System One) inner loop for ego-browser — one ~0.4s typed decision per DOM step instead of an LLM turn. Agent skill for ego lite.
- [Jev-Auto-Router](https://github.com/miniLV/Jev-Auto-Router) — Jev Auto Router (Jev Router): experimental per-call GPT model routing for Codex via TypeSafe Jev and a local Responses proxy, with independent task verification.
- [jev-browser](https://github.com/tontoko/jev-browser) — Integrates Jev field selection and source-backed extraction with a Playwright SDK, CLI, MCP server, and explicit assertions. Project guide.
- [jev-mcp](https://github.com/rashedInt32/jev-mcp) — An MCP server and Claude Code plugin for Jev classification, scoring, checks and batched questions.
- [Switchboard](https://github.com/ruban-24/switchboard) — Switchboard is a local Claude Code and Codex router. It assesses a new conversation's task with Jev, applies deterministic confidence rules to select the model and reasoning effort, and pins that route through follow-ups, tool calls,…
- [daf-jev](https://github.com/docxology/daf-jev) — Composable Python toolkit for TypeSafe Jev: question builders, confidence gates, evaluator, calibration, CLI, and optional MCP server. Project guide.
- [tool-prune](https://github.com/hemanth/tool-prune) — Calibrated tool selection and schema pruning for AI agents. Dual-engine: zero-dependency offline TurboQuant or TypeSafe System One (Jev). Prunes candidate MCP tools and schemas down to the relevant set before calling LLMs to eliminate…
- [claude-jev](https://github.com/buchmark/claude-jev) — Adds Jev checks to Claude Code review findings, debugging hypotheses, design options and search results.
- [codex-jev-router](https://github.com/tiandee/codex-jev-router) — Local Codex CLI bridge: TypeSafe Jev selects model and reasoning effort per turn via a loopback Responses proxy (fail-open without a key). Project guide.
- [dsh-jev](https://github.com/zhangxaochen/dsh-jev) — Jev (System One decision model) plugin suite for DeepSeek Harness (dsh)
- [fast-dev-compaction](https://github.com/leonaaardob/fast-dev-compaction) — Codex plugin for context compaction, using Jev within session lifecycle hooks to preserve essential history while pruning noise.
- [fast-jev-opencode](https://github.com/nrdz-labs/fast-jev-opencode) — OpenCode V2 plugin: TypeSafe Jev prunes stale tool calls/results on the outgoing request (fail-open; leaves history/`/compact` alone). Project guide.
- [hermes-jev-plugin](https://github.com/ajensenwaud/hermes-jev-plugin) — TypeSafe Jev (System One) decision tools for Hermes Agent: jev\_check / jev\_route / jev\_score / jev\_evaluate
- [jev-codex-token-saver](https://github.com/jcressler/jev-codex-token-saver) — Codex plugin/MCP that scores bounded local evidence with TypeSafe Jev and returns selected exact excerpts (local fallback when Jev is unavailable). Project guide.
- [jev-skill-gate](https://github.com/ShivamPansuriya/jev-skill-gate) — Gates Claude Code skill manifests with TypeSafe Jev relevance scores and `skillOverrides` so irrelevant skills stay out of context. Project guide.
- [jev.nvim](https://github.com/valentynkit/jev.nvim) — Neovim plugin that splits the buffer into functions with Treesitter, has Jev score each one against a plain-language question, and lists the answers in the quickfix window ranked by probability.
- [jevriel](https://github.com/thehan-co/jevriel) — \\Codex · Claude Code · Portable skill\\ | \Apache-2.0 code and docs\ | Early release
- [TypeSafe AI for Agent Zero](https://github.com/3clyp50/a0-typesafe-ai) — Agent Zero plugin for typed Jev Choice/Noul/Score judgments with probability cards; bundles the official TypeSafe agent skill. Project guide.
- [claude-code-jev](https://github.com/RahulBalakavi/claude-code-jev) — Claude Code PreToolUse permission gate: TypeSafe Jev via OpenRouter Decisions classifies allow/block/ask, with fixture latency/cost benchmarks. Project guide.
- [jev-in-codex](https://github.com/teempai/jev-in-codex) — Codex MCP tools for TypeSafe Jev-ranked capability selection, workspace search, and output triage (experimental MVP). Project guide.
- [jev-ra](https://github.com/brnyxx/jev-ra) — MCP/CLI browser-use layer for coding agents: TypeSafe Jev picks each Chrome operation and target in one round trip (OpenRouter or TypeSafe key). Project guide.
- [mysql-ailike](https://github.com/maayanlevy/mysql-ailike) — MySQL native `AILIKE` / `ailike` UDFs for natural-language row filters and joins via TypeSafe Jev (Linux plugin; GPL-2.0). Project guide.
- [opencode-jev-orchestrator](https://github.com/aaronshaf/opencode-jev-orchestrator) — An OpenCode orchestrator that keeps a cheap sticky parent model and, when Jev flags a hard turn, escalates through a child subagent.
- [prompt2jev](https://github.com/sumleo/prompt2jev) — Agent skill and CLI that convert natural language, an LLM prompt, or prompt-running code into a TypeSafe Jev decision (typed questions + runnable script). Project guide.
- [agent-fastpath](https://github.com/abhishekswe/agent-fastpath) — MCP decision layer for coding agents: deterministic rules then TypeSafe Jev ship/risk/triage/browser tools. Project guide.
- [alphaoptimizer](https://github.com/alpha-tales/alphaoptimizer) — AlphaOptimizer is an open-source tool from AlphaTales that helps Codex work with large command and tool outputs. Instead of sending a huge log or search result straight into the context window, AlphaOptimizer keeps…
- [codex-jev-compaction](https://github.com/Wang-auspicious/codex-jev-compaction) — Curates Codex handoff context by using Jev to select old tool records while retaining selected text verbatim.
- [dsh-jev](https://github.com/noetion/dsh-jev) — DeepSeek Harness plugin registering `jev_ask` for TypeSafe Jev noul/choice/score (pin GitHub commit; npm name `dsh-jev` collides with another package). Project guide.
- [dsh-jev-prune](https://github.com/yangyu666/dsh-jev-prune) — DeepSeek Harness plugin: TypeSafe Jev keep/drop pruning plus deterministic receipt compaction (distinct from dsh-jev / dsh-jev-verify). Project guide.
- [jev-classifier](https://github.com/felpsdev/jev-classifier) — A local Jev tool-routing gateway for coding Agents, with an MCP suggestion interface.
- [jev-codex-model-and-effort-router](https://github.com/gholtzap/jev-codex-model-and-effort-router) — Copy and paste this into your coding agent:
- [jev-codex-pilot](https://github.com/Charlyhno-eng/jev-codex-pilot) — A Codex overlay incorporating JEV to make the best decisions regarding model selection and depth of reasoning. All while automating the process via an automated Kanban system.
- [jev-codex-plugin](https://github.com/integrate-your-mind/jev-codex-plugin) — Open-source Codex plugin for TypeSafe Jev decision consultation, failure diagnosis, and evidence-based completion review
- [jev-shield](https://github.com/caiovicentino/jev-shield) — Semantic MCP firewall and skill: TypeSafe Jev (Vercel AI Gateway) screens tool calls, results, and descriptions. Project guide.
- [jev-skill-router](https://github.com/himomohi/jev-skill-router) — Keep skill catalogs outside the main LLM context. Jev selects relevant skills through one read-only MCP tool.
- [jevex](https://github.com/jvsteiner/jevex) — An Agent experiment where Jev directs a tool loop, a chat model fills arguments and prose, and MCP tools execute.
- [jevkit](https://github.com/ariel-frischer/jevkit) — Rust CLI for TypeSafe Jev typed decisions plus offline `jev lint` before paid calls (distinct from Hermes's internal Python `jevkit` client). Project guide.
- [JMP](https://github.com/morcoan/JMP) — Local coding workspace where TypeSafe Jev selects the next tool action and DeepSeek/Codex/Bonsai supply arguments for OpenHands/MCP execution. Project guide.
- [limpet](https://github.com/noplan-inc/limpet) — A Stop hook guardrail for coding agents: prevents premature completion by judging plain-language rules via Jev.
- [oc-plugins](https://github.com/OpeOginni/oc-plugins) — The oc-auto-perms plugin in an OpenCode plugin collection uses Jev to check tool intent against natural-language rules.
- [open-jev-approvals](https://github.com/alexj11324/open-jev-approvals) — Binary approval gate for Codex and Claude Code — every intercepted tool call is reviewed by TypeSafe JEV and composed through a versioned local policy, with scoped authorization.
- [tenbin](https://github.com/simota/tenbin) — Documentation, an MCP server and a Skill for designing Jev judgments with question linting, batch evaluation and calibration.
- [todo-jev](https://github.com/maker-KK/todo-jev) — Task classifier and 3-tier router (local rule / Jev skill / foundation model) with skill profiles and offline fallback. Project guide.
- [actiongate-jev](https://github.com/omkarghugarkar007/actiongate-jev) — Open-source Jev tool-calling authorization gateway for AI agents: deterministic policy, exact-action single-use permits, MCP and HTTP enforcement.
- [clear-head](https://github.com/VladyslavHontar/clear-head) — Claude Code Stop hook that judges answer claims against session tool evidence with TypeSafe Jev. Project guide.
- [decision-first](https://github.com/harrymunro/decision-first) — Agent skill that tries TypeSafe Jev on bounded-judgment steps first and documents every attempt in a reusable decision lab. Project guide.
- [dsh-jev-decide](https://github.com/nanami-0713/dsh-jev-decide) — DeepSeek Harness plugin registering `jev_decide` for TypeSafe Jev noul/choice/score (distinct from dsh-jev / dsh-jev-verify / dsh-jev-prune). Project guide.
- [hermes-jev-curator](https://github.com/anpicasso/hermes-jev-curator) — Hermes plugin: TypeSafe Jev typed skill-relationship judgments and safe curator archive/guard plans (experimental 0.1.0). Project guide.
- [Jev MCP (Freepik)](https://github.com/freepik-company/jev-mcp) — Go MCP server for typed decide/classify/verify/rerank with Jev via OpenRouter or TypeSafe (binary/container releases). Project guide.
- [jev-blindspot](https://github.com/jsk4581/jev-blindspot) — A side panel for Claude Code and Codex CLI that shows the blind spots of each prompt you submit: what the request would have needed to consider and shows no sign of. Jev decides, in one call per prompt, whether the…
- [jev-browser-skill](https://github.com/zurfyx/jev-browser-skill) — Claude Code/Codex skill where TypeSafe Jev chooses browser operations and targets from a code-built element table (reference implementation; explainer site included). Project guide.
- [jev-browser-skill](https://github.com/wanghai673/jev-browser-skill) — This Codex Skill lets Codex drive Chrome through Jev to complete multi-step browser tasks from a goal description with preset inputs.
- [jev-decisions](https://github.com/bojansandhaus/jev-decisions) — Jev Decisions Plugin for Hermes (and other AI Agents): tool risk reviews, human approval recommendations, evidence checks, and a local decision journal.
- [jev-mcp](https://github.com/rajasekharponakala/jev-mcp) — MCP server wrapping TypeSafe's Jev System One models — typed noul/choice/score judgments for AI agents
- [jev-mcp](https://github.com/Songokou1983/jev-mcp) — Local MCP server exposing TypeSafe Jev (System One decision model) as native Claude Code / Codex tools
- [jev-mcp](https://github.com/BYK/jev-mcp) — An evaluation-focused Jev MCP server for individual questions, batch processing and question or threshold comparisons.
- [jev-mcp-server](https://github.com/wangkuangkuang/jev-mcp-server) — MCP server for Jev (TypeSafe System One): the three official question types — choice, score, noul — plus batch classify. Calibrated probabilities, ~0.5s, \<$0.001/call.
- [jev-mcp-spring](https://github.com/Ashfaqbs/jev-mcp-spring) — On success each tool returns its typed result directly. On failure the tool call fails at the MCP protocol level (\`isError: true\`) with a short, safe message — no response body or stack trace is ever echoed back.
- [jev-rust-review](https://github.com/kindintelligence/jev-rust-review) — Rust-aware code review for Claude Code and coding agents, powered by TypeSafe Jev
- [jev-skill-selection](https://github.com/redreamality/jev-skill-selection) — Pre-message hook: use TypeSafe Jev to keep/drop skills and shrink agent context
- [jev-skills](https://github.com/eran-broder/jev-skills) — Skills without the context tax. Claude Code and Codex plugin: TypeSafe's Jev decides on every turn which skills the model sees. Always-on context cost: 0 tokens.
- [Jev_steer_or_queue](https://github.com/Larkspur-Wang/Jev_steer_or_queue) — Let TypeSafe Jev decide whether a message you send mid-turn should steer, queue, or interrupt your coding agent. Claude Code plugin; Codex CLI in testing.
- [nf-jev](https://github.com/nextflow-io/nf-jev) — Nextflow plugin exposing TypeSafe Jev noul/choice/score as pipeline functions (beta). Project guide.
- [Prompt Rejector](https://github.com/revsmoke/promptrejectormcp) — MCP/HTTPS screening for prompts, skills, and tool descriptions with TypeSafe Jev plus deterministic checks. Project guide.
- [pytest-jev](https://github.com/allebee/pytest-jev) — pytest plugin for semantic assertions about LLM output: `jev.expect` batches Noul claims about one text, reports each probability, and by default fails uncertain claims (holds needs at least 0.8, lacks at most 0.2); Choice checks the…
- [toolgate](https://github.com/RiskAverseTech/toolgate) — Open Claude Code PreToolUse and MCP tool-call firewall with static rules, TypeSafe Jev judgments, YAML policy, and a local audit log. Project guide.
- [TypeSafe-as-a-Judge](https://github.com/E-FL/typesafe-as-a-judge) — Unofficial Codex/Claude Code MCP plugin for bounded TypeSafe Jev route/rank/extract/verify/judge tools with proceed/review gates. Project guide.
- [typesafe-jev-mcp](https://github.com/anasbekheit/typesafe-jev-mcp) — This repository is an MCP server for TypeSafe Jev that provides a single evaluate tool taking state plus typed questions and returning noul, choice, or score answers with probabilities.
- [typesafe-jev-opencode](https://github.com/moisesfilho/typesafe-jev-opencode) — Jev is not a conversational replacement for Gemini, Claude, or GPT. It evaluates application state against typed questions and returns structured answers and probabilities that an agent can use to route or gate work.
- [askjev](https://github.com/pZacca/askjev) — Unofficial MCP server for TypeSafe Jev (local stdio or hosted Worker): agents get calibrated Noul/Choice/Score answers over held context. Project guide.
- [claude-jev-mod](https://github.com/chrishan17/claude-jev-mod) — Typed decisions in Claude Code: adds $.jev over TypeSafe's Jev, through OpenRouter, Vercel AI Gateway, Cloudflare Workers AI, LiteLLM or the TypeSafe API.
- [claude-jev-warden](https://github.com/connectedGraph/claude-jev-warden) — Real-time quality gate and Art Director Warden for Claude Code powered by TypeSafe Jev 1.13 non-autoregressive decision model
- [codex-jev-preflight](https://github.com/wellkilo/codex-jev-preflight) — Fail-open Codex UserPromptSubmit hook that injects TypeSafe Jev pre-task routing metadata.
- [dsh-jev](https://github.com/Excalibur9527/dsh-jev) — This DeepSeek Harness plugin sends each round's latest user message to the systemone (Jev) API for emotion and intent classification and injects the result as plugin-sourced runtime context, with API Key and all…
- [dsh-jev-verify](https://github.com/xienda/dsh-jev-verify) — DeepSeek Harness plugin with TypeSafe Jev `jev_decision` plus live `jev_verify` benchmark (no mock fallback; distinct from dsh-jev). Project guide.
- [Graphlin](https://github.com/royosherove/graphlin) — Live architecture and activity diagrams for Claude Code or Codex while they explore code, with optional TypeSafe Jev classification. Project guide.
- [jev-agent-kit](https://github.com/walidboulanouar/jev-agent-kit) — Zero-dependency CLI + MCP tools (route/triage/guard/grep/rank/compact/judge/…) on TypeSafe Jev (`@walidboulanouar/jevkit`; distinct from Rust jevkit). Project guide.
- [jev-agent-toolkit](https://github.com/reiswaffel78/jev-agent-toolkit) — Jev-first portable Agent Skill and optional MCP bridge for Claude Code, Codex, Cursor and compatible agents.
- [jev-carryforward](https://github.com/Dharundp6/jev-carryforward) — What your last session knew, scored against what this one is doing. MCP server: a per-project ledger written as things happen, recalled per task with TypeSafe's Jev evaluation model via Vercel AI Gateway.
- [jev-context](https://github.com/zbush/jev-context) — A Codex search plugin that filters ripgrep passages through Jev before returning relevant code.
- [jev-engineering](https://github.com/eugeniughelbur/jev-engineering) — Decision layer for coding agents: deterministic rules run before any model call, then one Jev request, shipped as a Claude Code PreToolUse hook, an MCP server, a loopback service and a team policy where personal overrides may tighten…
- [jev-in-mcp](https://github.com/chy4pro/jev-in-mcp) — MCP relay that adds use_jev to every server: Jev picks the tool calls, the calling model writes the values Jev cannot choose, the relay executes. Built on jev-dev-kit.
- [jev-mcp](https://github.com/CodeIA-Academy/jev-mcp) — MCP local que expone Jev (TypeSafe) como herramienta para Claude Code, Codex, Hermes y cualquier agente: ask\_jev y list\_jev\_models, sin dependencias
- [jev-mcp](https://github.com/ieee0824/jev-mcp) — A Rust MCP server for TypeSafe AI Jev structured decisions
- [jev-mcp-open-source](https://github.com/baize7815/jev-mcp-open-source) — Self-hosted Jev MCP on Cloudflare Workers with intent routing, retrieval reranking and batch judgments
- [jev-preflight](https://github.com/muse0509/jev-preflight) — Claude Code Stop-hook risk check: TypeSafe Jev scores eight axes over a redacted turn diff, with optional one-shot reinspection. Project guide.
- [jev-review-mcp](https://github.com/jiawei686/jev-review-mcp) — Single-purpose MCP server (one tool, one job): a code-review gate powered by TypeSafe Jev (System One decision model).
- [jev-routing](https://github.com/nekowasabi/jev-routing) — Go Jev harness for Claude Code, Codex, and Grok Build. No npx. Not an MCP server.
- [jev-screen-mcp](https://github.com/jiawei686/jev-screen-mcp) — Single-purpose MCP server (one tool, one job): a content-moderation gate powered by TypeSafe Jev (System One decision model).
- [jev-skill-router](https://github.com/shimo4228/jev-skill-router) — Claude Code plugin that ports the skill-suggestion cookbook to a UserPromptSubmit hook over user, plugin, and project skills; it sends the prompt text and skill descriptions to TypeSafe, starts in a log-only shadow mode, and ships…
- [jev-skills](https://github.com/WanLanglin/jev-skills) — Claude Code & Codex skills powered by Jev, TypeSafe's System One model. 256 calibrated judgements for $0.0005 in 0.72s — 360x cheaper than Claude Opus 5. Includes the first published Jev calibration curve, measured…
- [jev-toolkit](https://github.com/jbt95/jev-toolkit) — MCP-first TypeSafe/Jev toolkit: `jev mcp` plus CLI triage/audit/label/route and optional Prometheus impact metrics. Project guide.
- [jev\_ampcode](https://github.com/thesammykins/jev_ampcode) — An Amp plugin for comparing supplied alternatives against supplied evidence and priorities.
- [jevaluate](https://github.com/ElshinQ/jevaluate) — Jevaluate: evaluate before you trust. Field notes, runnable scripts and an agent skill for TypeSafe Jev: gated evals, a browser loop, a product walk with DeepSeek vision, a UI text judge and a first-click tree test. Co-authored with…
- [jevex](https://github.com/jimmyhealer/jevex) — One MCP tool that returns the files a coding agent should read.
- [JevGuard](https://github.com/Jhonnyr97/JevGuard) — Claude Code/Codex plugin: generate project rules from CLAUDE.md/AGENTS.md and enforce them with TypeSafe Jev on PreToolUse/Stop (distinct from jev-guard risk scoring). Project guide.
- [mcp-server-jev](https://github.com/MattiooFR/mcp-server-jev) — Typed AI decisions for Codex, Claude and any MCP client, powered by TypeSafe Jev. Classify, score and evaluate with one generic tool.
- [PerfectRecall](https://github.com/arslanr-com/perfectrecall) — Hermes/Python agent memory using TypeSafe or OpenRouter Jev evidence questions over local SQLite (Mnemosyne-compatible; no embeddings). Project guide.
- [Skill Dash](https://github.com/48Nauts-Operator/skill-dash) — Local dashboard that judges Claude Code/Codex skills with TypeSafe Jev (usefulness, redundancy, clarity, action) plus transcript evidence. Project guide.
- [typesafe-jev-plugin](https://github.com/arnab621/typesafe-jev-plugin) — Jev from Typesafe.ai is a "System One" AI model that returns typed, calibrated judgments instead of generating text. You define what to classify (a Choice), score (a Score), or verify (a Noul), and Jev returns a…
- [typesafe-jev-tools](https://github.com/wotai-dev/typesafe-jev-tools) — A Claude Code hook that asks whether the decision you are writing needs a model at all. Includes a measured 149-row comparison of TypeSafe Jev against Claude Haiku 4.5.
- [agy-jevgate](https://github.com/catpotd/agy-jevgate) — Fail-closed Antigravity `PreToolUse` hook for shell commands using TypeSafe Jev risk scores. Project guide.
- [deslop](https://github.com/yoichiojima-2/deslop) — Agent skill/CLI that scores page bodies with TypeSafe Jev probabilities for ads, slop, SEO shape, and derivative content. Project guide.
- [jev-gates](https://github.com/rashedInt32/jev-gates) — Seven calibrated gates for Claude Code (rules, scope, intent, done, claims, proof, and commit honesty) that escalate but never approve.
- [jev-skill-scout](https://github.com/karanb192/jev-skill-scout) — Finds Claude Code turns where a skill should have loaded and did not (TypeSafe Jev audit CLI + live suggest mod). Project guide.
- [jevdevice](https://github.com/Xopher00/jevdevice) — MCP harness for Android (adb) or local shell: TypeSafe Jev (or local Laya) picks one runtime-discovered target per goal; code gates and executes. Project guide.
- [jevmod](https://github.com/ohernandezdev/jevmod) — Moderation CLI/SDK/API/MCP and optional chat bots with per-category TypeSafe Jev probabilities and thresholds you own. Project guide.
- [Note Filer](https://github.com/someka-vrc/obsidian-note-filer) — Obsidian plugin that classifies notes with TypeSafe Jev and moves them into Thema/IAB taxonomy folders after review. Project guide.
- [openclaw-typesafe-ai](https://github.com/Olli0103/openclaw-typesafe-ai) — OpenClaw plugin registering optional `typesafe_decide` for explicit TypeSafe Jev decisions (SecretRef credentials; no hooks). Project guide.
- [openrouter-jev-mcp](https://github.com/ctmx/openrouter-jev-mcp) — A Python decision gateway and Model Context Protocol (MCP) server exposing TypeSafe's Jev model through OpenRouter's decisions endpoint to Claude Code, Codex, and Cursor agents.
- [slopcheck-jev](https://github.com/harshpuri84/slopcheck-jev) — A prose linter that catches AI writing tells. Regex settles the 18 a pattern can settle. Jev takes the 15 that need reading, as 15 Nouls in one call, 604 ms median. It ships as a Claude Code \`Stop\` hook that scores Claude's own output…
- [stop-rules](https://github.com/haystackeditor/stop-rules) — Coding-agent stop hook that asks TypeSafe Jev yes/no per changed piece against written team rules (multi-agent; optional team server). Project guide.
- [The Jev-enator](https://github.com/jakenbear/the-jev-enator) — Claude Code hooks using TypeSafe Jev for a danger gate, failure notice, and optional completion check (cassette-tested offline). Project guide.
- [docs](https://docs.typesafe.ai/agent-skill) — Official docs for giving a coding agent API context and guidance when designing narrow System One / Jev decision questions (Claude Code plugin and skills.sh install paths).
- [Jev Atlas](https://github.com/v60samurai/jev-atlas) — Claude Code/Codex skill that maps where a codebase should (and should not) use TypeSafe Jev, then validates/implements survivors. Project guide.
- [Jev Checkpoint](https://github.com/ashishakkumar/Jev-Checkpoint) — Local MCP server that confidence-gates a bounded next-step Choice with TypeSafe Jev and returns an advisory route only. Project guide.

### Integrations & data pipelines

- [pydantic-ai](https://github.com/pydantic/pydantic-ai) — 20.1K stars — A TypeSafe model integration that maps supported structured outputs to JEV questions.…
- [langchainjs](https://github.com/langchain-ai/langchainjs) — 18.2K stars — A TypeSafeClassifier integration for JavaScript LangChain workflows. [Source](https://github.com/langchain-ai/langchainjs/blob/206d8b992bcf90ce7d46f2158f1ad85fc1d826c0/libs/providers/langchain-typesafe/src/classifier.ts)
- [json-render](https://github.com/vercel-labs/json-render) — Generative UI framework with an experimental Jev composer that selects components and layout from application-supplied candidates through Vercel AI Gateway. The [Jev API](https://json-render.dev/docs/jev) is unreleased and requires a…
- [rig-typesafeai](https://github.com/0xPlaygrounds/rig) — A Rust integration with compile-time-checked option counts, so an over-255 Choice fails to build rather than at runtime.
- [Bifrost · TypeSafe Provider](https://github.com/maximhq/bifrost) — 8.2K stars — Bifrost exposes TypeSafe as a native provider through its shared decision operation. [Source](https://github.com/maximhq/bifrost/blob/40c3f7ee3a1a4277c5b269b850ca7725d419907f/core/providers/typesafe/typesafe.go)
- [GPT-Load · JEV Provider](https://github.com/tbphp/gpt-load) — 6.9K stars — A self-hosted AI gateway with a first-class JEV channel and native Decisions routes. [Source](https://github.com/tbphp/gpt-load/blob/93502ced3a650018a35ed76c54573e90742b8ccc/internal/channel/modules/jev.go)
- [GreptimeDB · JEV SQL](https://github.com/GreptimeTeam/greptimedb) — 6.7K stars — GreptimeDB adds an experimental SQL predicate backed by JEV judgments. [Source](https://github.com/GreptimeTeam/greptimedb/blob/b5199bc59a199875187d808158357a33b09e5f60/src/common/function/src/scalars/jev.rs)
- [Open Connector · TypeSafe](https://github.com/oomol-lab/open-connector) — 5.9K stars — Open Connector exposes TypeSafe evaluation through its provider runtime. [Source](https://github.com/oomol-lab/open-connector/blob/4e6d8533ae436cba4781b6fb69d1bf31e5fb5ffe/src/providers/typesafe_ai/runtime.ts)
- [ruby_llm: TypeSafe provider](https://github.com/crmne/ruby_llm) — A Ruby provider with a dedicated System One protocol, the main route into Jev from Ruby.
- [fx](https://github.com/vercel-labs/fx) — Experimental Zig coding agent with an [optional Jev permission reviewer](https://github.com/vercel-labs/fx/blob/main/src/builtins/gateway/typesafe_permission_reviewer.zig): setting `review_model` to `typesafeai/jev` sends the composed…
- [Agent Router · TypeSafe](https://github.com/theagentrouter/agent-router) — 2.1K stars — Agent Router provides a native TypeSafe System One translator in its Envoy-based gateway.…
- [LLMGateway · System One](https://github.com/theopenco/llmgateway) — 1.7K stars — LLMGateway implements a native System One route with typed schemas and provider mappings. [Source](https://github.com/theopenco/llmgateway/blob/24de43b5f307ecbdee9aad386b68aee76de4ae8c/apps/gateway/src/systemone/systemone.ts)
- [Laravel AI](https://github.com/laravel/ai) — Provides typed classification and a TypeSafe provider for Laravel applications, with fake responses for application testing. Project guide.
- [req\_llm](https://github.com/agentjido/req_llm) — 581 stars — A TypeSafe provider for calling Jev through ReqLLM’s evaluate interface in Elixir. [Source](https://github.com/agentjido/req_llm/blob/9cb0ee7a0fea5f3520fc953911d352c93193615e/README.md)
- [unclutter](https://github.com/kitze/unclutter) — Chrome/Firefox extension that uses Jev through TypeSafe or Vercel AI Gateway to classify bounded page-element snippets, then stores reusable local hiding rules by page template. Paid analysis is manual by default; optional on-visit…
- [SiftRank · JEV](https://github.com/noperator/siftrank) — 202 stars — A command-line ranking tool that uses JEV to find relevant items in large collections. [Source](https://github.com/noperator/siftrank/blob/03e7afe3289a204ea3dcc51613cea91877a651de/pkg/siftrank/jev_provider.go)
- [webctl](https://github.com/dorkitude/webctl) — Agent web-search CLI that scores and judges multi-provider results (optional scrape chunks) with TypeSafe Jev. Project guide.
- [effect-agent](https://github.com/danieljvdm/effect-agent) — 121 stars — An Effect Agent TypeSafe decision provider for typed question sets and optional model selection. [Source](https://github.com/danieljvdm/effect-agent/blob/88005e497e9b627eeb16d670f278903c57601da9/README.md)
- [HA-Jev](https://github.com/AboveColin/HA-Jev) — Home Assistant integration that turns typed questions about entity state into sensors and automation actions, with entities reporting daily calls, tokens, and estimated cost and a token budget that halts evaluation; answers carry no…
- [Jeview](https://github.com/andududu/jeview) — Experimental unofficial loopback proxy and live map of Jev calls, grouping decisions by project and linking later calls to earlier answers; it forwards requests to TypeSafe and stores requests, responses, and the API key in local SQLite…
- [loki](https://github.com/wundercorp/loki) — Loki optionally adds Jev typed-judgment tools and routes a new session to a model within the selected gateway.
- [jev-agent-design-with-topk-logits-choices](https://github.com/6Mikao9/jev-agent-design-with-topk-logits-choices) — Research design for a Jev-native agent system: tool integration, speculative parameter proposals, external helper logits Top-k proposals with Jev-controlled fallback ,decision-aware hierarchical memory, and…
- [RubyLLM TypeSafe](https://github.com/kieranklaassen/ruby_llm-typesafe) — A TypeSafe provider for RubyLLM 2 that exposes Jev’s three judgment types through structured output.
- [patdown](https://github.com/tyler-dot-earth/patdown) — CLI, GitHub Action, and agent hooks that judge files or changes against Markdown rules with a provider-swappable Jev backend and configurable probability threshold; it sends matched file content to TypeSafe, has no request budget or…
- [pi-jev-router](https://github.com/mejiasd3v/pi-jev-router) — Automatic model router for Pi coding assistant: integrates Jev via Vercel AI Gateway to dispatch tasks efficiently.
- [Discern](https://github.com/doeixd/discern) — Effect Decision/DecisionModel patterns, policies, and procedures with an optional TypeSafe Jev provider (`@doeixd/discern`). Project guide.
- [jevql](https://github.com/kylemclaren/jevql) — A psql-shaped CLI and Go/TypeScript/Python SDKs that add `jev()`, `jev_prob`, `jev_choice`, and `jev_score` to queries against a vanilla Postgres with no extension. The SQL runs on the server and Jev judges the surviving rows in batches.
- [jev-ood-calibration](https://github.com/scienthoon/jev-ood-calibration) — Independent calibration test of TypeSafe's Jev on a task it cannot have seen: 900 rule-generated support tickets (choice / score / boolean) plus 3 public benchmarks via Vercel AI Gateway. Raw responses, ECE with noise floor, temperature…
- [jevsql](https://github.com/EugeneBoondock/jevsql) — Adds TypeSafe Jev natural-language predicates and decision tables to SQLite SQL with batching, caching, and review queues; distinct from pg-jev. Project guide.
- [safer-with-jev](https://github.com/andrelandgraf/safer-with-jev) — An HTTP inspection gateway that checks request content with Jev before optionally forwarding it to an HTTPS destination.
- [dbt_jev](https://github.com/smithclay/dbt_jev) — Classify warehouse SQL values with TypeSafe Jev (or OpenRouter→Jev) from dbt macros on DuckDB and ClickHouse. Project guide.
- [DuckDB Jev](https://github.com/prasanthj/duckdb-jev) — Native DuckDB extension for Jev predicates, Choice classification, Score rubrics, and streaming batched judgments over SQL rows, with per-query budgets, caching, and request telemetry; published live throughput uses a repeated synthetic…
- [jev-web-analyzer](https://github.com/replynodes/jev-web-analyzer) — See what Jev thinks about your SaaS website — powered by ReplyNodes web context and Vercel AI Gateway.
- [vgi-typesafe](https://github.com/Query-farm/vgi-typesafe) — DuckDB integration, loaded through the community VGI extension, that exposes Choice, Noul, and Score as SQL table functions to `LATERAL` join against a table, returning typed columns with confidence, probabilities, and per-row token…
- [jev-layer](https://github.com/typakon4/jev-layer) — Portable System-1 decision layer for agent harnesses: host-owned capability routing, receipts/replay, optional supervision, demo/OpenRouter/TypeSafe providers. Project guide.
- [jev-resilience](https://github.com/Vicente-MD/jev-resilience) — A Spring WebFlux integration that detects error messages hidden in HTTP 200 response bodies.
- [Jev Second Brain](https://github.com/fellowship-dev/jev-second-brain) — Local-first Markdown vault CLI: FTS index, source-linked related-note suggestions, optional TypeSafe Jev judgments via Vercel AI Gateway. Project guide.
- [jev-research](https://github.com/sherajdev/jev-research) — A Jev and Herdr integration guide with a prototype for routing tasks to different Agents.
- [jevpolicy](https://github.com/Sanoy24/jevpolicy) — JevPolicy is an open-source TypeScript decision runtime that turns probabilistic judgments from Jev, accessed through Vercel AI Gateway, into versioned, deterministic, replayable, observable application decisions.
- [typesafe-agent-gates](https://github.com/ThiagaoBR/typesafe_agent_gates) — LangChain/Deep Agents middleware using TypeSafe Jev for shell gates, issue triage, MR detection, and test-spec review. Project guide.
- [jev-agent-browser](https://github.com/mhingston/jev-agent-browser) — Confidence-gated browser actions for `agent-browser` with TypeSafe Jev (or Gateway/Cloudflare/custom providers). Project guide.
- [jev-decision-gateway](https://github.com/kuldeepsinh19/jev-decision-gateway) — A gateway that asks Jev continue / tool / verify questions and invokes a generative LLM only when policy says generation is needed.
- [Airflow LLMBranchOperator with Jev](https://airflow.apache.org/docs/apache-airflow-providers-common-ai/stable) — Turns downstream task ids into a choice option set, with a minimum-confidence gate that routes uncertain runs to a human.
- [Announcement](https://vercel.com/changelog/typesafe-ai-jev-now-available-on-ai-gateway) — Vercel's launch note for Jev on AI Gateway, with an experimental_evaluate sample using the model string typesafe-ai/jev.
- [Jev on AI/ML API](https://docs.aimlapi.com/api-references/decision-models/typesafe/jev) — Another gateway route, notable because its endpoint path and request envelope differ again from both the native API and Cloudflare's.
- [langchain-typesafe](https://docs.langchain.com/oss/python/integrations/providers/typesafe) — The LangChain integration: a classifier plus experimental middleware for model routing and for gating risky tool calls before they run.
- [Tracing Jev calls with Langfuse](https://langfuse.com/integrations/model-providers/typesafe) — The only platform with dedicated Jev observability: an OpenInference instrumentor that traces every decision call over OpenTelemetry.

### Other tooling

- [Sub2API · JEV Moderation](https://github.com/Wei-Shaw/sub2api) — Drops in as a moderation API by asking many parallel Noul questions in one request, one per hazard category, with an anti-injection prefix on every instruction.
- [OpenViking · JEV Rerank](https://github.com/volcengine/OpenViking) — One Noul per candidate document in a single batched request, with the yes-probability used directly as the relevance score.
- [Hindsight · TypeSafe Rerank](https://github.com/vectorize-io/hindsight) — 24.8K stars — An agent-memory system with a TypeSafe reranker that can prune irrelevant recall candidates.…
- [jcode: memory recall without embeddings](https://github.com/1jehuang/jcode) — Replaces the whole retrieval stack for memory recall — no embeddings, no BM25, no reranker — with one batched Noul per candidate memory.
- [@effect/ai-typesafe](https://github.com/Effect-TS/effect) — Implements Effect's DecisionModel interface over Jev, with an unusually candid caveat about unverified rounding behaviour.
- [firstmate](https://github.com/kunchenguid/firstmate) — 6.9K stars — An agent crew dispatcher that can match task briefs to rules with JEV. [Source](https://github.com/kunchenguid/firstmate/blob/4812db801628040b609dc25a2a8a91ed5efac662/bin/fm-dispatch-resolve.sh)
- [Kiln · JEV Adapter](https://github.com/Kiln-AI/Kiln) — A JSON-Schema-to-question compiler wired into the adapter registry, with an honest note on what it cannot serve.
- [latitude-llm](https://github.com/latitude-dev/latitude-llm) — Latitude includes an optional Jev preclassifier for conversation checks and their selection records.
- [jev-trader](https://github.com/jarrodwatts/jev-trader) — Studies Jev market-direction choices, simulated fills, and on-chain order execution through a Bun trading experiment. Project guide.
- [LM Format Enforcer](https://github.com/noamgat/lm-format-enforcer) — Enforces JSON schema or regex on LLM output during generation.
- [XGrammar](https://github.com/mlc-ai/xgrammar) — Fast, flexible structured-generation engine for constraining LLM outputs to a grammar with low overhead.
- [Beacon](https://github.com/Asymptote-Labs/agent-beacon) — Cross-harness agent memory tool with an explicit `beacon memory evaluations run` command: Jev judges bounded, redacted trace projections for reusable lessons, which a person reviews before adding to project memory or installing as a…
- [celesto](https://github.com/CelestoAI/celesto) — 958 stars — A Celesto PR-review example prepares sandbox checks and compares a general model with Jev on candidate findings.…
- [typesafe-computer-use](https://github.com/awlevin/typesafe-computer-use) — Combines local OCR and Accessibility observations with Jev decisions to operate macOS, with an optional writing model. Project guide.
- [atomic](https://github.com/bastani-inc/atomic) — 812 stars — An optional Jev decision backend in the Atomic coding Agent for bounded structured choices such as routing.…
- [Hippo Memory](https://github.com/kitfunso/hippo-memory) — Local agent memory system with an opt-in Jev reranker that batches Noul judgments over the top 40 recalled memories and falls back to a local cross-encoder on errors. The author's published study found better ranking on two corpora but…
- [Distill](https://github.com/samuelfaj/distill) — Coding agent harness that can use Jev to select a model and effort, route bounded utility tasks, and judge what context to retain. Code constrains the choices and validates utility results; failed or low-confidence decisions leave the…
- [kody](https://github.com/kentcdodds/kody) — 663 stars — Optional second-stage search: widen the hybrid pool, then Score-rerank candidates with Workers AI typesafe/jev.…
- [Jev Review](https://github.com/devagrawal09/jev-review) — Staged code-review workflow for JavaScript and TypeScript with a local dashboard. Jev screens correctness, security, reliability, compatibility, and test risk, then scores severity and suggests a reviewer, with no generative model involved.
- [Foreman](https://github.com/thruwire/foreman) — 472 stars — An independent supervisor loop that reads worker diffs, logs and tests, asks Jev Nouls about stuck / off-track / verify, then applies a Python policy.…
- [Jev Search](https://github.com/superagents-lab/jev-search) — Web search demo using Jev's typed Choice and Noul judgments to select sources, time ranges, and query candidates, then rank results retrieved through Search1API; relevance scores are model judgments, not verified accuracy.
- [Smithers](https://github.com/smithersai/smithers) — 418 stars — An agentic TypeScript workflow framework with a first-class JEV classify path. [Source](https://github.com/smithersai/smithers/blob/394ada6a3fb815b4b62cfc7bc2242e238d42ff44/apps/server/src/jev.ts)
- [Tax Document Classifier](https://github.com/kyotofin/tax-doc-classifier) — Apache-licensed, text-only classifier for 261 federal tax forms that sends PDF text to Jev; the author reports no wrong labels on two test corpora but 38 low-confidence pages, without committed page-level results.
- [Classifier.dev](https://github.com/mrmps/classifier-dev) — 406 stars — A zero-shot classification service with JEV as its primary typed-decision backend. [Source](https://github.com/mrmps/classifier-dev/blob/33ca63816f2bc7e93c3f2d0715f7896500370739/src/jev.ts)
- [TypeSafe Mario](https://github.com/fhshaik/typesafe-mario) — 338 stars — An experimental NES Mario controller that gives Jev structured emulator RAM and telemetry instead of screenshots. [Source](https://github.com/fhshaik/typesafe-mario/blob/ca22449ed187118d19326d1f54b01b6636578aa4/README.md)
- [jev-experiments](https://github.com/dabit3/jev-experiments) — A collection of Jev developer-tool experiments, including Commit Sentry for semantic checks on staged diff hunks.
- [Mobile Jev](https://github.com/droidrun/mobile-jev) — 329 stars — Controls an Android phone through Mobilerun, with a web studio and CLI showing Jev decisions. [Source](https://github.com/droidrun/mobile-jev/blob/395fc222beac4f059f9a0beb337d114a2b066e99/scripts/mobile-agent/policy.mjs#L224)
- [WrongStack](https://github.com/WrongStack/WrongStack) — 331 stars — An optional Jev dispatch classifier for choosing among WrongStack specialist Agents. [Source](https://github.com/WrongStack/WrongStack/blob/4cf97c0aa4f855751949ee8e99c719d06f4c26e0/README.md)
- [instructor-php](https://github.com/cognesy/instructor-php) — 327 stars — A TypeSafe Decision driver within Instructor PHP’s Polyglot module. [Source](https://github.com/cognesy/instructor-php/blob/bb1160ce2360dcf1434788c46ee97809fe782ea3/README.md)
- [pg-jev](https://github.com/realZachi/pg-jev) — PostgreSQL extension for Jev-powered `WHERE` predicates, probabilities, Choice, and Score over table rows; it batches rows, caches answers per session, and offers optional query spend caps. Every judged row goes to TypeSafe, and…
- [JevRev](https://github.com/Alex314618-create/JevRev) — Your LLM can imagine, write, test, and revise. It should not have to make every cheap routing decision by itself.
- [jev-align (Sutro)](https://github.com/sutro-sh/jev-align) — 1. Evaluates the configured dataset and measures uncertainty. 2. Selects ambiguous rows plus a random audit sample for you to label. 3. Uses your accumulated labels and optional rationales to run GEPA. 4. Shows the score, certainty…
- [orchestkit](https://github.com/yonatangross/orchestkit) — 281 stars — OrchestKit can optionally use Jev to classify coding sessions and set their colors when confidence meets a threshold.…
- [voice-browser](https://github.com/moritzkremb/jev-voice-browser) — Local voice-controlled Playwright browser: Jev chooses a typed intent and target from speech and a bounded page snapshot, while code applies confidence gates and asks for confirmation before actions it classifies as destructive. The Web…
- [pi-fabric](https://github.com/monotykamary/pi-fabric) — 244 stars — Pi’s programmable runtime includes an optional Jev loop for observing state, making decisions and running bounded actions.…
- [quackd](https://github.com/rokbenko/quackd) — Robot orchestration CLI with an optional Jev stepper for choosing among permitted discrete calls while an LLM still writes poses and prose and the executor enforces safety gates; one arm has run on hardware under the LLM pilot, but the…
- [Abide](https://github.com/coldteadotai/abide) — 207 stars — A coding-agent rule layer for constraints that ordinary linters cannot express. [Source](https://github.com/coldteadotai/abide/blob/ec3352e873163b74aca1ac9cf3bd0ea69a97723a/README.md)
- [jevpilot](https://github.com/standardagents/jevpilot) — A driving simulator autopilot asking two choices per tick, which short-circuits single-option questions locally instead of paying to send them.
- [perch](https://github.com/lakeday-org/perch) — 167 stars — Semantic code linting that asks JEV / System One whether findings should fire. [Source](https://github.com/lakeday-org/perch/blob/54a38d6034264dc507e97294b82316c347fe5a5e/src/systemone.js)
- [Jev Drone](https://github.com/RomanSlack/jev-drone) — 119 stars — A MuJoCo drone experiment deriving scene features from camera buffers for Jev tactical advice. [Source](https://github.com/RomanSlack/jev-drone/blob/cbeb53ce4f17a06ea490ae43effcdad231143610/tactics.py#L184)
- [System One Harness](https://github.com/HarnessRouter/SystemOneHarness) — Python controller: finite-action agent loops with TypeSafe Jev (OpenRouter or TypeSafe), confidence gates, and step traces. Project guide.
- [jev-pruner](https://github.com/tamaratran/jev-pruner) — Trims long shell output before the model sees it, asking one Noul per chunk.
- [pi-jev](https://github.com/y0usaf/pi-jev) — 134 stars — A Pi extension that flags tool risks before execution and checks output for secrets and failure types. [Source](https://github.com/y0usaf/pi-jev/blob/b3478fd4ca1ac8ffcb703f6dc8d6069b555f531e/README.md)
- [pi-warden](https://github.com/DevMortimer/pi-warden) — Pi guardrails built on pi-typesafe that return Jev's verdict to the agent as a held tool result or a short steer instead of a dialog, check writes against a project rules file, and grade their own holds against the user's next message…
- [jev-semgrep](https://github.com/uehaj/jev-semgrep) — Node CLI (`@uehaj/semgrep`) that batches Jev Noul questions per line for multilingual grep by meaning and combines queries with AND, OR, and NOT in code. Every searched line goes to TypeSafe, repeated searches pay for the corpus again,…
- [ai](https://github.com/hackclub/ai) — 133 stars — A Jev forwarding endpoint in the Hack Club AI proxy, using its authentication, limits and usage logging. [Source](https://github.com/hackclub/ai/blob/a76ea2cb159f707a60107935a5b2e0dbdc7455f5/README.md)
- [neo4jev](https://github.com/jexp/neo4jev) — Explores Neo4j paths using next-hop choices and goal judgments, with notebooks and a Streamlit interface. Project guide.
- [taskuary](https://github.com/ldbumble/taskuary) — 116 stars — An optional Jev judgment module in Taskuary for checking user-defined conditions on task state. [Source](https://github.com/ldbumble/taskuary/blob/4ad29d7b292a7899767338cfcc83b2dde8f43330/README.md)
- [jev-code](https://github.com/devagrawal09/jev-code) — Helps coding Agents locate code, check change intent, triage test failures, and organize review findings.
- [Stanley Code](https://github.com/devagrawal09/stanley-code) — Routes coding requests into bounded Jev review and triage workflows, with trusted repository extensions and an optional Pi coding-agent fallback. Project guide.
- [Jev × WebMCP](https://github.com/sdras/jev-webmcp-extension) — `Open source` · `Free source build` · `BYOK`. Chrome side panel that selects and populates page WebMCP tool calls with TypeSafe Jev from keystrokes (Chrome 149+ / WebMCP; BYOK; load unpacked). [Project…
- [Supercov](https://github.com/supercorp-ai/supercov) — Code quality and test coverage for coding agents: Jev scores each source file so the agent knows what to fix first. Project guide.
- [jev-shell-history](https://github.com/mrnugget/jev-shell-history) — Ranks recent zsh commands with Jev for inline suggestions; sends selected history to TypeSafe and requires a user-supplied API key. Project guide.
- [bluenoise](https://github.com/rokcso/bluenoise) — 90 stars — An X/Twitter filtering extension using local rules by default, with optional Jev checks for unmatched replies. [Source](https://github.com/rokcso/bluenoise/blob/ef81ea7a7c3677501d6de8f9235a4d6a866b573a/entrypoints/background.ts)
- [pg\_typesafe](https://github.com/giuliosmall/pg_typesafe) — Pre-alpha PostgreSQL C extension for TypeSafe Jev Choice/Noul/Score with batched multi-text helpers; distinct from pg-jev. Project guide.
- [grok-bot-jev](https://github.com/Bodila51/grok-bot-jev) — , Connects TypeSafe Jev to Grok Bot as a cheap decision layer. [![Code](https://img.shields.io/github/stars/Bodila51/grok-bot-jev?style=flat-square&logo=github&label=Code&color=181717)](https://github.com/Bodila51/grok-bot-jev)
- [jev-lint](https://github.com/mizchi/jev-lint) — Ast-grep + TypeSafe Jev natural-language semantic linter (name/body drift, stale comments, weak tests); distinct from huntedman/JevLint. Project guide.
- [jgrep](https://github.com/keltokhy/jgrep) — Filters text, structured records, functions, and diff hunks against plain-English descriptions using Jev Noul judgments. Project guide.
- [jevcache](https://github.com/hyperspaceai/jevcache) — Local decision cache keyed on (model, schema, state), with redaction and canonicalisation before hashing, for cheaper repeats and deterministic replay in CI. No license file at the time of writing.
- [captaincore](https://github.com/CaptainCore/captaincore) — 71 stars — Jev commands in the WordPress toolkit CaptainCore answer structured questions and prioritize malware scanner findings for review.…
- [dspy-typesafeify](https://github.com/typesafeainate/dspy-typesafeify) — , Decorator that routes DSPy typed Signatures to Jev where the signature is a pure decision.…
- [jev-libero](https://github.com/Dimweaker/jev-libero) — Two LIBERO tasks, one control engine. Each demo loads its own JSON task definition. Videos follow simulation time, with decision and physics-preview waiting omitted.
- [Jev-Mem](https://github.com/libingzheren/Jev-Mem) — System-One–controlled agentic memory: TypeSafe Jev steers admission, multi-relational linking, and adaptive retrieval before a text model answers. Project guide.
- [SemDecide](https://github.com/sharziki/semdecide) — Typed semantic decisions for Unix pipelines and CI with TypeSafe Jev predicates, routes, scores, and filters. Project guide.
- [hono-jev-router](https://github.com/yusukebe/hono-jev-router) — Experimental Hono router that matches HTTP requests to plain-English descriptions with TypeSafe Jev Noul judgments. Project guide.
- [Jev Sift](https://github.com/kbhuw/jev-sift) — Screens files, public webpages, and tool descriptions with Jev before an agent reads selected content; requires a TypeSafe key, and upstream licensing is unspecified. Project guide.
- [Jev-Moderation-Bot](https://github.com/brainstormity/Jev-Moderation-Bot) — A Discord moderation bot: a Choice tiers each message while a Noul carries ban urgency, and an admin pardon is fed back as a safe precedent in later requests.
- [Jev for Apple Foundation Models](https://github.com/peterfriese/jev-foundation-models) — Swift 6 bridge that translates Apple `@Generable` Boolean, enum, and bounded score fields into one Jev question set, then decodes the typed answers through `LanguageModelSession`; ships mock-transport tests and two demos, but requires…
- [commit-miner](https://github.com/devanshbatham/commit-miner) — Classifies Git commit messages and diffs with Jev for bug fixes, security fixes, CWEs, and change types.
- [jev-edge](https://github.com/kiwi0719/jev-edge) — Typed-judgment admission control at the traffic edge: three-layer prompt-injection and abuse filter for nginx/OpenResty, powered by TypeSafe Jev. Fail-open, cached, hot-reloadable.
- [jev-recall](https://github.com/samdotmak/jev-recall) — Retrieve by relevance, not resemblance: filter an AI assistant's memories with TypeSafe's Jev
- [jev](https://github.com/dannote/jev) — Integrates Jev as an asynchronous Elixir/OTP process whose replies are handled with GenServer pattern matching.
- [jev-calibrate](https://github.com/smkrv/jev-calibrate) — , CLI for tuning criteria and thresholds with a ledger of holdout reuse; the authors' small support-ticket example improves frustration accuracy from 0.69 to 0.92 on tuning data and scores 0.97 on holdout.…
- [plasmallm](https://github.com/joshuaeroman/plasmallm) — A Jev Decisions adapter in a KDE Plasma assistant widget for displaying structured judgments.
- [jevscan-evm](https://github.com/devtooligan/jevscan-evm) — Produces a heat map of likely bugs in EVM code. The author's own warning: a proof of concept whose code they did not read.
- [doc-router](https://github.com/misbahsy/doc-router) — Routes PDF pages between local text extraction and OCR using optional Jev judgments, with a Rust CLI and Python bindings. Project guide.
- [Jev Capability Atlas](https://github.com/Zaious/jev-capability-atlas) — This repository collects real Jev API-call receipts, test suites, and bilingual guides to map which narrow-decision tasks suit Jev and how Agents should evaluate and report fit.
- [SmartMoney-Cub](https://github.com/myc0576/SmartMoney-Cub) — Read-only trading journal and review harness with optional TypeSafe Jev typed judgments and a frozen finance-jev offline benchmark (no orders). Project guide.
- [minojev](https://github.com/zeredy879/minojev) — Decisions, not tokens: minojev reads calibrated, typed probability distributions straight from hidden states in one forward pass — zero output tokens, fully reproducible on a laptop CPU.
- [is-malicious](https://github.com/luantak/is-malicious) — Sends source, configuration, build, and CI files to Jev and points at the files and lines that look deceptive or data-stealing. Its README says a clean report is not proof a project is safe.
- [pi-jev-auto-mode](https://github.com/jomatsu/pi-jev-auto-mode) — Adds rule checks to Pi commands and file operations, then uses Jev to assess cases that need further judgment.
- [Jev Cookbook](https://github.com/nexibeo/jev-cookbook) — Fifteen runnable OpenRouter recipes for support triage, data cleanup, search, browser actions, and Gmail labeling, with small labelled samples and saved live results; the examples keep action thresholds in code, and their sample results…
- [jev-axi](https://github.com/shiftynick/jev-axi) — Agent-ergonomic CLI following the AXI conventions that gives coding agents Jev judgments for blocking risky tool calls, screening fetched content for prompt injection, triaging build logs, flagging risky diffs, and filtering or ranking…
- [jev-macos-loop](https://github.com/jcpsimmons/jev-macos-loop) — Native Apple silicon macOS computer-use agent: local OmniParser/Vision/Accessibility perception with text-only Jev action choice (BYOK Vercel/OpenRouter/TypesafeAI). Project guide.
- [jev-yaba-wechat](https://github.com/wuxie888/jev-yaba-wechat) — Jev returns a structured decision for the local program; consult the source for the exact decision policy.
- [jev-code](https://github.com/rhighs/jev-code) — An experimental coding CLI where Jev selects AST productions for Python or Bash, with a separate command-line decision mode.
- [jev-reranker (hotchpotch)](https://github.com/hotchpotch/jev-reranker) — Python RAG relevance filter/reranker with TypeSafe Jev (listwise/pointwise/pairwise); distinct from the shinpr Rust CLI. Project guide.
- [jevalyn](https://github.com/Ray-Hughes/jevalyn) — The decision layer for your Rails app. A Rails-native wrapper around TypeSafe's Jev System One API: typed, calibrated decisions in your control flow.
- [Jot](https://github.com/runta-dev/jot) — A general-purpose agent loop where Jev picks the next move and Jot runs it. No license file at the time of writing.
- [jsort](https://github.com/keltokhy/jsort) — Ranks text along a plain-English criterion using pairwise Jev Noul comparisons and a locally fitted Bradley-Terry scale.
- [invalidate](https://github.com/chopratejas/invalidate) — Semantic TTL for agent memory: TypeSafe Jev checks every stored fact against new evidence; code marks superseded memories without rewriting text. Project guide.
- [jev-to-answer](https://github.com/csskrtao/jev-to-answer) — Jev returns a structured decision for the local program; consult the source for the exact decision policy.
- [feelings](https://github.com/BoundaryML/feelings) — BAML `.feels()` / `.how()` / `.matches()` typed AI-if methods powered by TypeSafe Jev; upstream licensing unspecified. Project guide.
- [JevLoop](https://github.com/zjunlp/JevLoop) — The agent loop where decisions don't cost a large language model call. Zero deps, runs offline, no API key needed.
- [jev-test-filter](https://github.com/mizchi/jev-test-filter) — Scores each test against a git diff with TypeSafe Jev and emits filter args for vitest, Jest, node:test, Playwright, cargo, and go test. Project guide.
- [jeval](https://github.com/rlaope/jeval) — Measures probabilistic classifier calibration (incl. Jev confidence) and cost-optimal human hand-off thresholds; offline demo included. Project guide.
- [Hunch](https://github.com/carldaws/hunch) — Ruby gem that turns judgment calls into control flow: `if Hunch.likely?("fraudulent", given: order)` branches on a typed Jev answer, with `pick` for Choice, `rate` for Score, and graded predicates from `possibly?` to `definitely?`; not…
- [pi-jev-router](https://github.com/philippdubach/pi-jev-router) — Pi extension: TypeSafe Jev classifies tasks and local policy routes OpenRouter models (Pareto profiles; shadow mode default). Project guide.
- [yummy-pi-extensions](https://github.com/sugarforever/yummy-pi-extensions) — Extensions for the Pi coding agent, each released separately, including a Jev-based model router.
- [azdaja](https://github.com/kubet/azdaja) — Bare, open-source RLM layer for existing coding agents
- [elons-job](https://github.com/bugkiwi/elons-job) — Local-first Chrome extension that uses Jev to filter sexual and solicitation content in X replies with reversible hidden placeholders.
- [jev-harness](https://github.com/AntonioCoppe/jev-harness) — TypeScript decision harness: confidence-gated TypeSafe Jev policies, shadow mode, recipes, and `jev-eval` (distinct from super-jev / jev-layer). Project guide.
- [jevyoumean](https://github.com/syumai/jevyoumean) — Semantic CLI "Did you mean?": TypeSafe Jev matches unknown subcommands by intent from help text (`jym`). Project guide.
- [Eutrya](https://github.com/hellozenstrategist-lab/eutrya) — CLI-first agent (public alpha) with TypeSafe Jev in the decision loop for attention, candidate rubrics, and research micro-steps; offline `eutrya demo`. Project guide.
- [jev-router](https://github.com/prismhq/jev-router) — An open-source LLM router built on LiteLLM and Jev: dynamically routes requests based on task complexity and context.
- [beam-cli](https://github.com/whyashthakker/beam-cli) — AgentBeam local monitoring/safety CLI for coding agents, with optional TypeSafe Jev action judging (disabled by default; AGPL-3.0). Project guide.
- [jev-chat-for-twitch](https://github.com/ethanplusai/jev-chat-for-twitch) — Filter any live Twitch chat with Jev: a bring-your-own-key Chrome extension
- [jev-feels](https://github.com/Qew7/jev-feels) — Ruby gem for TypeSafe Jev as `feels?` / `decide` / `score` and Rails validations (distinct from BAML feelings and ruby_decision_model). Project guide.
- [JevLint](https://github.com/huntedman/JevLint) — Semantic lint CLI: plain-English conventions scored as file-level TypeSafe Jev Noul judgments (`@jevlint/cli`). Project guide.
- [jevlogs](https://github.com/reachjalil/jevlogs) — Scores OpenTelemetry logs for a separate analysis branch, with mock mode and conservative error handling. Project guide.
- [JevPokerBench](https://github.com/Prophetlab/JevPokerBench) — Texas Hold'em benchmark/playground with official TypeSafe Jev, cash/SNG boards, and BYOK agents. Project guide.
- [pi-fast-jev-compaction](https://github.com/joelhooks/pi-fast-jev-compaction) — A Pi extension that prunes stale tool history verbatim and falls back to Pi summary compaction when needed.
- [super-jev](https://github.com/Kevthetech143/super-jev) — Evidence-to-action TypeScript harness: typed Jev judgments, permitted tools, verified outcomes, and JSONL journals. Project guide.
- [jevcal](https://github.com/abhixhek/jevcal) — Calibrates, thresholds, and drift-checks the confidence scores of typed decision models so you stop guessing cutoffs.
- [jevernetes](https://github.com/sunil-sadasivan/jevernetes) — Live Kubernetes log analysis (CLI/dashboard) with optional TypeSafe Jev judgments or offline keyword rules and agent handoff prompts. Project guide.
- [pi-verdict](https://github.com/jesset/pi-verdict) — Pi permission gate that first applies deterministic rules (danger floor, user allow/deny, protected-path prompts) for clear decisions, then routes gray-zone cases to a fail-closed enforcing classifier (configurable via `classifierModel`…
- [J++](https://github.com/Towow-ai/jpp) — Experimental language and Rust runtime for composing semantic Jev questions with exact methods as values; offline fixtures included. Project guide.
- [jev-rs](https://github.com/yijunyu/jev-rs) — System One judgments (noul/choice/score) from any LLM in one prefill — a Rust, Jev-compatible /v1/systemone engine
- [jevcache](https://github.com/kushals256/jevcache) — OpenAI-compatible local cache proxy: TypeSafe Jev (OpenRouter Decisions) admits same-intent paraphrases so expensive chat completions can be skipped (fail-open on Jev errors). Project guide.
- [jevmory](https://github.com/romiluz13/jevmory) — Local coding-agent memory with verbatim quotes graded by TypeSafe Jev confidence and receipt-backed MEMORY.md audits. Project guide.
- [jev-auto-approve](https://github.com/metalbear-co/jev-auto-approve) — Jev is a decision model: it answers a typed question with a calibrated probability rather than prose. This action asks it one yes/no question per thing worth being sure about — answered in parallel in a single call — and approves only…
- [jev-router](https://github.com/rajdhakad9826/jev-router) — Cost-aware LLM router that picks the cheapest model capable of handling a query, using TypeSafe's Jev for fast classification instead of an LLM call.
- [jev-tree](https://github.com/reachjalil/jev-tree) — Recursive TypeSafe Jev Choice over a JSON taxonomy so catalogs can exceed the 255-option flat Choice cap. Project guide.
- [laya-jev-lab](https://github.com/yibie/laya-jev-lab) — Independent measurements of typed-decision models: Jev (TypeSafe API) vs Laya (open weights), and a local-first cascade that matches Jev's accuracy at 1.8x the speed
- [SpecPi](https://github.com/TannerMidd/SpecPi) — A Pi configuration and extension bundle with an optional Jev advisor for capabilities and workflow checks.
- [Typed Evals](https://github.com/TrustifAI/typed_evals) — Evaluate LLM/RAG/agent outputs with TypeSafe Jev judges, optional calibration, and tool guards. Project guide.
- [zod-jev](https://github.com/jomatsu/zod-jev) — Adds semantic rules to Zod validation, such as checking whether text matches a description or contains personal information.
- [Every](https://github.com/sufianetaouil/every) — Ask a yes/no question of every function in a codebase. Ranked answers in seconds, for cents. Grep whose pattern is a question, powered by TypeSafe Jev.
- [jev-dsl](https://github.com/inanna-malick/jev-dsl) — An early Haskell DSL that describes labeled Jev questions, renders requests and decodes matching answers.
- [jev-pref](https://github.com/doeixd/jev-pref) — CLI and GitHub Action that turn project-defined semantic preferences into Jev Noul or Choice checks over code changes, then map results to advisory or blocking outcomes in code; supports tuning on labelled diffs, and sends reviewed…
- [jev\_jsonschema](https://github.com/Kiln-AI/jev_jsonschema) — \`probabilities\` is keyed by your schema's values, not Jev's internal labels, so a score of \`1\`–\`5\` reads as \`"1"\`–\`"5"\` and not \`"0"\`–\`"4"\`. Noul questions carry no confidence of their own, so \`confidence\` is \`None\`…
- [pi-heed](https://github.com/Nyarlathoteppppp/pi-heed) — Pi extension that turns constraints stated in conversation (English and Chinese) into a scoped, replayable policy (deny, allow, exceptions, once/run permissions, ask-first, tests-before-push) and checks side-effecting tool calls against…
- [pi-jev-context](https://github.com/Nyarlathoteppppp/pi-jev-context) — Pi extension that shortens long tool output before it enters the context, so no cached prompt prefix is invalidated: Jev gives every block of the output a probability that the current request needs it, only blocks it is confident are…
- [Bicameral](https://github.com/AbdelStark/bicameral) — Pi coding harness where an LLM writes while Jev supplies typed reflexes for policy, loop detection, and review; explicitly not a sandbox.
- [Jev Lab](https://github.com/jammaru/jev-lab) — Local Hundred NPC-town and Jev Shogi labs where TypeSafe Jev chooses the next legal action (Rules mode without a key). Project guide.
- [jevc](https://github.com/doronp/jevc) — Compiles natural-language agent rules and JSON Schemas into TypeSafe Jev programs (typed questions + code reducers) you can test offline. Project guide.
- [JevNoiseGate](https://github.com/ufec/jev-block-android-ad) — Android app that asks Jev whether each incoming notification or SMS is noise and suppresses only what Jev explicitly flags, with a local pre-filter for verification codes that never reaches the API and a fail-open default on every…
- [riff](https://github.com/scale-venture-partners/riff) — Prose linter with ruff-style rule codes: local static rules plus optional TypeSafe Jev judgment rules (`riff-lint` 0.1.0). Project guide.
- [typesafe-jev-incident-router](https://github.com/kyle-chalmers/typesafe-jev-incident-router) — Confidence-gated incident routing with TypeSafe Jev
- [deepseek-harness-jev-pre-compaction](https://github.com/wjw66/deepseek-harness-jev-pre-compaction) — A pre-compaction advisor for DeepSeek Harness. Runs before the standard \`compaction-basic\` backend, using TypeSafe JEV to safely prune low-value tool results from model context. Original session events stay in the append-only log;…
- [jevlang](https://github.com/sumanmichael/jevlang) — The simplest way to write decision workflows in Python. Python with a smart if.
- [JevOnly](https://github.com/buluoray/JevOnly) — Pure-Jev browser agent: code enumerates page/goal options, Jev only picks, with verify/undo and an irreversible-action gate. Project guide.
- [jevsearch](https://github.com/kylemclaren/jevsearch) — Site search that understands the question. Ranked by TypeSafe's Jev model.
- [pi-jev-guard](https://github.com/Reindeer-AI/pi-jev-guard) — Check Pi code edits against repository Markdown rules with TypeSafe Jev
- [agi-jev-containment](https://github.com/carlosedm10/agi-jev-containment) — \\Open-source AI agent monitoring, malicious-agent detection, and escalate-only containment\\ for sandboxed LLM agents. Local HackSpain 2026 stack (AngryRobot dashboard): FastAPI, React/Vite, Neo4j. Classifies a \chain of actions\, not…
- [jev-compaction](https://github.com/Waxmell114514/jev-compaction) — A context compactor that can only score, never write — so an agent's memory can't hold a fact the transcript never contained. Working demo, runs offline.
- [jev-mobile](https://github.com/Friedjof/jev-mobile) — Experimental Android agent that uses Jev for bounded, per-step choices over prevalidated UI actions, with confidence gates, pagination, escalation, and optional LLM planning; currently a proof of concept tested mainly against Android…
- [jev-model-tokengate](https://github.com/Thanh-Mathieu95/jev-model-tokengate) — An OpenAI-compatible proxy that sits between your LLM and your users. It evaluates each sliding window of tokens \\while the response is still streaming\\ and cuts the stream \\before\\ a violating token can reach the screen.
- [jev-oas-sentinel](https://github.com/ShuhanSun/jev-oas-sentinel) — Compares OpenAPI documents with deterministic structural checks plus TypeSafe Jev semantic questions; policy code owns pass/review/block. Project guide.
- [jevopt](https://github.com/Ramneet-Singh/jevopt) — Making intelligent compiler optimisation decisions with Jev
- [jlink](https://github.com/keltokhy/jlink) — The string baselines are best-match Jaro-Winkler and best-match TF-IDF cosine; the table shows the better of the two. Exact matching after normalization scores 0.26, 0.41, 0.00, 0.00 and 0.22.
- [leanest](https://github.com/baronunread/leanest) — Adds Jev-based selection before an existing test runner using diffs and test source.
- [PiJ](https://github.com/tonyzdev/PiJ) — A Pi-based terminal coding Agent whose main model handles reasoning, edits and tools while Jev provides advice.
- [semantic-assert](https://github.com/mondaychen/semantic-assert) — Assert plain-English claims about captured UI/text state with TypeSafe Jev (Playwright helpers; thresholds in code). Project guide.
- [slidepilot](https://github.com/harshil1712/slidepilot) — Experimental Slidev addon that uses presenter voice, Cloudflare STT, and TypeSafe Jev to auto-advance when policy agrees. Project guide.
- [tink-route](https://github.com/jon-devlapaz/tink-route) — Confidence-aware Agent Skills router: TypeSafe Jev Noul/Choice gate, optional Tink install/prune. Project guide.
- [typesafe-cli](https://github.com/y0usaf/typesafe-cli) — Shell `jev` CLI for TypeSafe Jev noul/choice/score answers as numbers (distinct from Python typesafeai-cli). Project guide.
- [fast-compaction-dsh](https://github.com/kolawong/fast-compaction-dsh) — Verdict-based context compaction for DeepSeek Harness — replaces lossy LLM summaries with fast keep/truncate/drop decisions from jev-latest; everything kept stays verbatim. Port of tamaratran/fast-jev-compaction.
- [Jev](https://github.com/cobusgreyling/Jev) — Unofficial TypeSafe Jev showcase — System One decisions, not chat.
- [jev-as-quant](https://github.com/jiayylu/jev-as-quant) — Typed System-1 decisions (Laya/Jev) as the judgment layer of a quant research stack, with Claude as System 2. Requirements → design → code → experiments.
- [jev-assist](https://github.com/glud123/jev-assist) — Don't burn your expensive main model on grep-and-guess grunt work — let jev rank the whole repo, and save the main model for reading the right files and writing the right code.
- [jev-builder](https://github.com/collapseindex/jev-builder) — A browser form for building requests to TypeSafe's Jev: pick a template, fill in the blanks, copy the request. No JSON, no install, runs locally.
- [jev-cli](https://github.com/jtsang4/jev-cli) — A CLI for asking Jev classification, yes/no and scoring questions over text or JSON input.
- [jev-cli](https://github.com/joshLong145/jev-cli) — A CLI wrapper written in python for Jev
- [jev-does-not-play-dice](https://github.com/KantaHayashiAI/jev-does-not-play-dice) — Code, recorded outputs, and analysis scripts for probability-output experiments with Jev: fair random draws, Noul (Yes/No) questions, and forecast documents.
- [jev-judgment](https://github.com/HyunjunJeon/jev-judgment) — Adds judgment checks for authorization, operation risk, and failure causes to coding Agents.
- [jev-pilot](https://github.com/h0j5bz0adh0-stack/jev-pilot) — Fast System-1 Decision, Arbitration & Safety Engine for Autonomous AI Agents (Powered by TypeSafe Jev)
- [jev-plays](https://github.com/mansicer/jev-plays) — TypeSafe Jev plays Craftax: macro/raw action Choice with optional LLM planner-as-facts and a local web UI. Project guide.
- [jev-reranker](https://github.com/shinpr/jev-reranker) — Pipe JSON search candidates through TypeSafe Jev to rerank, filter evidence, or compress passages for LLM context. Project guide.
- [jev-triage](https://github.com/boldbug1/jev-triage) — Message triage CLI in Go, built on the Jev decision model from TypeSafe AI. Categorizes messages, scores urgency, and flags low-confidence ones for human review.
- [JevDroid](https://github.com/antiyro/jevdroid) — Experimental Python framework that uses Jev to choose Android actions from accessibility trees and executes them through ADB or UIAutomator2, with explicit action permissions and per-run budgets; goals and visible UI text are sent to…
- [jevmetrics](https://github.com/ishantanu/jevmetrics) — Use it to assess unfamiliar instrumentation, review candidates for reduced retention, and selectively filter metrics before they reach a primary backend. Inference runs asynchronously, and cached assessments let subsequent batches use…
- [jevrag](https://github.com/ajanm007/jevrag) — Replaces hardcoded RAG thresholds with explicit calibrated decision points. Five primitives (retrieval stopping, chunk splitting, context selection, answer abstention, cache trust) behind one swappable state → Decision → confidence →…
- [jevtok](https://github.com/LabGuy94/jevtok) — Exact token counting and request-cost prediction for TypeSafe Jev (tiktoken-style encoder reconstructed from API usage). Project guide.
- [jselect](https://github.com/keltokhy/jselect) — Selects source-linked evidence within a token budget using Jev Noul relevance judgments and local diversity-aware selection. Project guide.
- [laravel-typesafe-jev](https://github.com/Butochnikov/laravel-typesafe-jev) — A Laravel adapter for Jev with configuration, dependency injection, a Facade and a request-recording test fake.
- [pi-jev-compaction](https://github.com/nourhelmi/pi-jev-compaction) — Pi extension that asks Jev which older tool results to hide after context pressure rises, retains the original session messages, and exposes a `jev_read` tool to recover an output without rerunning its command; it protects recent…
- [pi-typesafe-jev](https://github.com/legacybridge-tech/pi-typesafe-jev) — A Pi extension exposing TypeSafe judgments as five narrow tools, keeping threshold and action control in host code.
- [tiershift](https://github.com/iamvatsalpatel/tiershift) — Policy-driven model routing framework routing every LLM call to the cheapest capable tier in ~180 ms via TypeSafe Jev.
- [typesafe-jev-calibrate-for-code-review](https://github.com/Selmar/typesafe-jev-calibrate-for-code-review) — About calibrating Jev for code reviews
- [antivirus](https://github.com/newuser7171/antivirus) — A file scanner that sends extracted features to Jev for a verdict, a 0–4 severity score, and Noul indicators, then applies local quarantine or review rules.
- [ask-jev-ai](https://github.com/waynesutton/ask-jev-ai) — Most AI demos generate text. Jev does not. It reads a sentence and returns typed answers with probabilities: a choice, a yes or no, a score. That makes it usable as a primitive inside ordinary code rather than a…
- [DecideKit](https://github.com/sameerkhan24/decidekit) — Typed decision policies for TypeScript/Python with Jev via OpenRouter or TypeSafe, offline fixtures, and explicit confidence fallbacks. Project guide.
- [git-jev-stage](https://github.com/ibrahemid/git-jev-stage) — Classifies Git hunks against a one-sentence staging intent with TypeSafe Jev, then stages confirmed blocks. Project guide.
- [hush](https://github.com/emreozyoruk/hush) — GitHub Action for issue triage that abstains: label, spam, needs-more-info, and possible-duplicate in one call, each applied only above a threshold the maintainer sets, and nothing at all below it.
- [Jev Classification for n8n](https://github.com/khmuhtadin/n8n-nodes-jev-classification) — Adds typed classification, scoring, yes/no checks, and batched questions to self-hosted n8n, with configurable review routing. Project guide.
- [jev-ci-selector](https://github.com/guilhem/jev-ci-selector) — GitHub Action that asks TypeSafe Jev which described CI tasks apply to the current PR diff and exports boolean job outputs. Project guide.
- [jev-cvss](https://github.com/Red5d/jev-cvss) — Scripts that use Jev to select CVSS metrics from vulnerability descriptions, then compute v3.0, v3.1 or v4.0 scores in Python.
- [jev-linkedin-slop-filter](https://github.com/Arpit-Khandelwal/jev-linkedin-slop-filter) — Judges every LinkedIn post as it scrolls into view and slams a rubber stamp on it — BAIT, CORP, or BRAG — with the confidence score printed on the stamp. The post stays readable underneath.
- [jev-mode](https://github.com/ddfeyes/jev-mode) — I kept watching coding agents burn context on decisions that aren't hard - triage 400 tickets, tag 600 files, route to one of six teams. jev-mode moves those verdicts to a typed-judgment model. I A/B'd it: 78% fewer tokens, 16x less…
- [jev-model-router](https://github.com/lucianfialho/jev-model-router) — Cost-optimized OpenRouter model router using TypeSafe's Jev, with a live full-catalog scorer instead of a hardcoded model list
- [jev-model-router](https://github.com/gualican/jev-model-router) — Routes prompts to the right Claude tier (Haiku/Sonnet/Opus) using TypeSafe's Jev model
- [jev-pii-checker](https://github.com/coo-quack/jev-pii-checker) — A CLI that sends text to TypeSafe Jev for PII category Nouls and a sensitivity Score, then locates spans with regex and segmentation.
- [jev-pr-judge](https://github.com/juanegido/jev-pr-judge) — Typed pull-request verdicts via one parallel TypeSafe Jev call, code-owned policy profiles, Next.js UI, and a sticky-comment GitHub Action. Project guide.
- [jev-router](https://github.com/AABBAASS1/jev-router) — Route any task to the right AI agent in under 1 second using Jev (TypeSafe System One). Supports Claude, ChatGPT, Cursor, and Antigravity with auto-launch on macOS, Windows, and Linux.
- [jev-router-playground](https://github.com/hugo-alves/jev-router-playground) — A model-routing playground where Jev picks a candidate and users compare the resulting answers.
- [jev-routing-experiment](https://github.com/TokenTrim/jev-routing-experiment) — Benchmarking TypeSafe's Jev decision model as a cost-efficient LLM router on RouterArena
- [jev-workbench](https://github.com/molis-ai/jev-workbench) — Defines, tests, and publishes Jev decision functions in a local UI so backends and Agents can call fixed versions.
- [Jev4Mellea](https://github.com/SoundBlaster/Jev4Mellea) — This is an unofficial, synchronous adapter. Jev evaluates text; it does not generate or repair it.
- [jevbrief](https://github.com/Parthkomalwad/jevbrief) — Adapters &nbsp;·&nbsp; Quick start &nbsp;·&nbsp; Game demo &nbsp;·&nbsp; Python &nbsp;·&nbsp; Viewer &nbsp;·&nbsp;…
- [jevbus](https://github.com/zkjoie/jevbus) — A streaming event bus whose routing, subscription and consumption are decided by a probabilistic judge. The reference judge is TypeSafe AI's Jev (System One) model: send it a payload and a set of typed questions, get back calibrated…
- [Jevonian](https://github.com/xinyao27/jevonian) — Local OpenAI/Anthropic/Responses proxy for coding agents where one Jev call answers both the model route and the thinking level for `jevonian/auto`, after code has filtered candidates by protocol, context window, effort floor, and spent…
- [jevshield](https://github.com/lgy1027/jevshield) — Sub-100ms security gate for AI agent tool calls, powered by TypeSafe's Jev (System-1) decision model. Single-request Choice/Noul/Score evaluation, dual-factor blocking matrix, calibrated-confidence routing, fail-closed parsing,…
- [n8n-nodes-jev](https://github.com/rahulthakore16/n8n-nodes-jev) — Jev by TypeSafe AI for n8n: typed decisions, probabilities, and confidence-aware workflows
- [n8n-nodes-typesafe-jev](https://github.com/n3ndor/n8n-nodes-typesafe-jev) — An n8n community node for submitting typed questions to TypeSafe Jev.
- [pi-fast-jev-compaction](https://github.com/KamilPostrozny/pi-fast-jev-compaction) — Fast JEV compaction extension for pi
- [pi-jev-context](https://github.com/kevinpita/pi-jev-context) — A reversible Pi context filter using Jev to judge whether older messages remain useful.
- [TypeSafe AI Playground](https://github.com/markjaquith/typesafe-ai-playground) — Rust CLI of Jev experiments, including PHI detection, code-comment review, live tone analysis, and occupation and industry classification.
- [typesafe-ai-jev-example](https://github.com/ItBayMax/typesafe-ai-jev-example) — This repository provides six runnable Python demos and four notes covering TypeSafe Jev primitives and composition patterns, with offline mock mode and committed live samples from jev-1.13.0.
- [typesafe-jev-examples](https://github.com/rajivkuriakose/typesafe-jev-examples) — Worked examples for TypeSafe's Jev System One decision model, runnable today through OpenRouter
- [VideoAdGuard-Jev](https://github.com/xianggelila177/VideoAdGuard-Jev) — Jev returns a structured decision for the local program; consult the source for the exact decision policy.
- [wellposed](https://github.com/suraj-phanindra/wellposed) — Zero-dependency linter for TypeSafe Jev requests: broken state paths, missing Choice escape hatches, bundled judgments (`wellposed` 0.4.0). Project guide.
- [your-signal](https://github.com/MithrilMan/your-signal) — A BYOK Chrome extension using Jev to score X posts against personal preferences and adjust their display.
- [ask-jev](https://github.com/logicrw/ask-jev) — Ultra-fast, fail-open advisory decisions and verbatim extractive reading view for AI coding agents and CLI pipelines
- [DataJev](https://github.com/zzz1YAO/DataJev) — Data-analysis agent loop where an LLM analyzes, Python executes, and TypeSafe Jev chooses CONTINUE/SWITCH/VERIFY/STOP (heuristic offline path). Project guide.
- [discoprint](https://github.com/lirantal/discoprint) — CLI that fetches an artist's discography and available lyrics, asks Jev five typed questions per song about theme, mood, complexity, explicit content, and perspective, then draws a terminal dashboard; full lyrics go to TypeSafe, missing…
- [Footwork](https://github.com/Tom-R-Main/Footwork) — Dual-process browser agent: TypeSafe Jev as System 1 in front of browser-use System 2, with a code-owned arbiter and evidence verification (`jevdual`). Project guide.
- [hunch](https://github.com/steven-shoemaker/hunch) — Python verbs (`classify`/`score`/`check`/`pick`/`rank`/`where`) over scalars, lists, and pandas columns backed by TypeSafe Jev (`hunch-jev`). Project guide.
- [Jev Score](https://github.com/a-Fig/jev-score) — Local CLI/web scoreboard that grades document revisions against your criteria with TypeSafe Jev via OpenRouter Decisions. Project guide.
- [jev-by-example](https://github.com/ReallyArtificial/jev-by-example) — Ten runnable Jev examples for agent decisions: memory conflicts, tool-result checks, recovery, context selection, and handoffs. JavaScript, zero dependencies.
- [jev-console](https://github.com/wenchenxi/jev-console) — Jev does not generate text. You send it a \\state\\ plus a set of \\typed questions\\, and it answers each one with a typed value and a calibrated probability:
- [jev-debtgate](https://github.com/smlayero/jev-debtgate) — Technical-debt gate for coding agents and CI: local metrics plus TypeSafe Jev typed questions and confidence policy (BYOK). Project guide.
- [jev-eyes](https://github.com/LeddoEngano/jev-eyes) — Also in the state: \`image\` (size, source), \`blocks\` (\`\[x, y, w, h\]\` boxes with OCR confidence) and, if installed, \`labels\`. \`see(img, compact=True)\` keeps only \`image\`, \`text\` and top label names when tokens matter more…
- [jev-frontier-100](https://github.com/softpudding/jev-frontier-100) — \\Jev scores 77.0%; Qwen3.5 2B with a 2,048-token thinking budget scores 82.0%; Qwen3.5 4B with the same budget scores 96.7%.\\ This small benchmark makes Jev's observed reasoning limits tangible through nine local-model settings.
- [jev-inbox-queue](https://github.com/tusharck/jev-inbox-queue) — Turn an inbox into a short action queue with Jev (TypeSafe System One)
- [jev-issue-radar](https://github.com/Patrick-SCH03/jev-issue-radar) — Jev Issue Radar is a read-only dashboard for GitHub duplicate-issue triage. It retrieves likely candidates, asks Jev whether each pair is duplicate, related, distinct, or insufficiently documented, and shows selected passages from both…
- [jev-lab](https://github.com/q93304989-bit/jev-lab) — This repository provides a single-page classifier demo that sends text with choice questions to Jev and displays the request JSON, probability distribution, confidence, latency, and token usage.
- [jev-lab](https://github.com/llt22/jev-lab) — Hands-on research lab for TypeSafe's Jev (System One model): reproducible benchmarks of Noul/Choice/Score primitives, confidence gating, fan-out latency, agent control — plus a living audit of the Jev ecosystem.
- [jev-labs](https://github.com/copyleftdev/jev-labs) — Never confidently wrong: a TLA+-verified consensus kernel around TypeSafe's Jev, run through 1,680 chaos-tested pharmacy decisions with zero wrong verdicts. Film, code, and every captured call.
- [jev-linter-action](https://github.com/sable-inc/jev-linter-action) — GitHub Action: configurable TypeSafe Jev yes/no suites over repo files with probability thresholds (distinct from jev-ci-selector and jev-lint CLIs). Project guide.
- [jev-logtriage](https://github.com/jyatesdotdev/jev-logtriage) — CLI that asks Jev Noul, Score, and Choice questions of collapsed Loki log batches and maps answers in code to suppress, watch, review, notify, or page; remediations stay candidates and nothing is executed.
- [jev-msw](https://github.com/royalpinto007/jev-msw) — Mock Jev API decisions with MSW for deterministic tests without real API calls or credits.
- [jev-numeric](https://github.com/Bring-AI/jev-numeric) — Both are multiway decision trees; decimal-digit decoding is a ten-way instance. On an aligned decimal grid, they can have identical branches and leaves, expressed through different prompts. The digit is a…
- [jev-review-action](https://github.com/fatwang2/jev-review-action) — Configurable GitHub Action: catalog or PR classification with TypeSafe Jev only (no text-gen), one template comment. Project guide.
- [jev-secret-detection](https://github.com/teyhouse/jev-secret-detection) — , 100 balanced secret-detection cases as single Noul questions scored by accuracy, AUC and Brier; server p50 75 to 90ms.…
- [jev-skills](https://github.com/laguagu/jev-skills) — Practical agent skills and examples for building with Jev. API setup, routing, ranking, and evidence checks.
- [jev-tab-order](https://github.com/proshunsuke/jev-tab-order) — Organize the entire window with a single Jev API request. Grouping and ordering decisions are evaluated together, regardless of the number of tabs.
- [jev-toolspace](https://github.com/xuan7zhang/jev-toolspace) — Jev answers yes/no (`noul`) questions about a shared state and returns an independent probability for each one. One API call scores every tool in a menu with one question per tool, and a tool's score does not compete…
- [jev-toto](https://github.com/maxlibin/jev-toto) — Counting and comparison happen in Rust, because Jev is documented as unreliable at arithmetic. Jev receives per-number facts plus plain-English labels and answers two questions per number in one request: a yes/no…
- [jev-zork](https://github.com/Resadan-dev/jev-zork) — TypeSafe Jev plays Zork I: Choice over Jericho valid actions with anti-loop policy and a French replay dashboard. Project guide.
- [jev_playground](https://github.com/JYeswak/jev_playground) — Jev answers typed questions about a state with calibrated numbers. This repo is where we find out which of those numbers deserve to drive code, and where a regex or a constant does the job better.
- [jevals](https://github.com/dayhaysoos/jevals) — Local TypeSafe Jev evaluation workbench: author Noul/Choice/Score cases with expected answers, run them, and compare saved results. Project guide.
- [jevcheck](https://github.com/sathariels/jevcheck) — Probabilities and model versions move. A raw `0.94` is not a release decision. jevcheck records a production contract (baseline model + fixtures + expected answers) and evals a candidate against that fixture.
- [jevcode](https://github.com/miounet11/jevcode) — This repository provides an Astro-based multilingual documentation site explaining Jev's Choice, Score, and Noul decision primitives with architecture patterns and usage examples.
- [jevcore](https://github.com/litshing/jevcore) — A judgement primitive for TypeSafe \\System One / Jev\\ — ask N things × K typed questions in bounded, cheap, fail-open requests — plus the \\JEV harness\\, the closed boundary in code that makes a Jev answer safe to consume. Standard…
- [jevinf](https://github.com/zerodegress/jevinf) — An inference engine for decision models of the Jev kind: each candidate path runs as segmented forwards with prefix reuse, and the Jev wire contract is served on top. NanoJev is the backend wired up today.
- [jevish](https://github.com/hemanth/jevish) — Every mode auto-curries when called with only the patterns:
- [jevnav](https://github.com/dtduc-git/jevnav) — Browser automation with TypeSafe Jev element choice, JSONL decision traces, risk gates, and offline CI replay (distinct from Ultrafast). Project guide.
- [Jevs-Garage](https://github.com/JGalego/Jevs-Garage) — System One turns unstructured or structured state into fast probabilistic judgments. Instead of asking for free-form prose, these demos ask \`Choice\`, \`Score\`, and \`Noul\` questions and receive typed values with uncertainty that…
- [jevscript](https://github.com/amberwhitehead/jevscript) — An early language experiment whose current implementation is a Jev request-batching spike.
- [JevTape](https://github.com/Hugo-DDT/JevTape) — Record/replay/inspect TypeSafe Jev decisions as JSON cassettes with Decision Contract fingerprints for offline CI. Project guide.
- [jevtriage](https://github.com/sathariels/jevtriage) — GitHub Action + CLI: triage PRs with TypeSafe Jev (`ready` / `needs_review` / `risky`) and confidence-gated exits. Project guide.
- [Metis](https://github.com/Ayush0054/metis) — GitHub Action and Python CLI that triage new issues with TypeSafe Jev category labels and missing-detail follow-ups. Project guide.
- [n8n-nodes-typesafe](https://github.com/zampierid4p/n8n-nodes-typesafe) — n8n community node for asking typed questions inside workflows.
- [openclaw-jev-compaction](https://github.com/SqaaSSL/openclaw-jev-compaction) — Verbatim context compaction for OpenClaw: a context engine powered by TypeSafe's Jev. Drops stale tool calls and results, never summarizes.
- [paper-radar-jev](https://github.com/LYchoon/paper-radar-jev) — An automated research paper radar that fetches the latest papers from arXiv, evaluates their relevance to a configurable research profile using TypeSafe AI, and ranks them by relevance score. Designed for personalized, daily literature…
- [pi-follow-through](https://github.com/Nabsku/pi-follow-through) — Pi extension that asks TypeSafe Jev whether useful work remains after a run and nudges only with verifiable unfinished evidence. Project guide.
- [pi-jev-compaction](https://github.com/Wang-auspicious/pi-jev-compaction) — Extractive context compaction for Pi that keeps selected original tool records instead of generating a summary.
- [pi-jev-permit](https://github.com/kurihada/pi-jev-permit) — Pi extension: TypeSafe Jev judges each bash/write/edit call after local hard-deny and read-only fast paths. Project guide.
- [pi-observational-memory-jev](https://github.com/willfish/pi-observational-memory-jev) — Jev decides what to keep. Compaction never rewrites the transcript.
- [pr-sieve](https://github.com/Thestral12/pr-sieve) — A GitHub Action that compiles \`.jev.yml\` rules into Jev questions and fails, comments, or passes from the numbers.
- [profanity-checker](https://github.com/4rays/profanity-checker) — Deploy this Worker once, then call it from your other Workers.
- [qualm](https://github.com/qddegtya/qualm) — A TypeScript wrapper for Jev decisions with an explicit unsure branch.
- [Responsible AI Harness](https://github.com/syabdulr/responsible-ai-harness) — Model-agnostic safety assessment harness: hard rules plus optional TypeSafe Jev judge for injection, leakage, unsafe tools, and policy bypass; checksummed evidence + report UI. [Project…
- [s1-rs](https://github.com/AbdelStark/s1-rs) — Rust derive layer for TypeSafe System One Choice/Score/Noul over optional `typesafe-rs` (distinct from typesafe-api). Project guide.
- [sgrep](https://github.com/Lagnajit09/sgrep) — Semantic grep for codebases: chunk files and ask TypeSafe Jev which chunks match a plain-English query (includes offline mock). Project guide.
- [traffic-guard](https://github.com/hemanth/traffic-guard) — High-throughput traffic and attack defense gate for incoming HTTP traffic with zero required dependencies, wire-order header validation, and TypeSafe System One acceleration for bot mitigation, exploit detection, and risk scoring.
- [triagedy](https://github.com/m0rphtail/triagedy) — UNIX-filter security-alert triage: JSONL in, typed TypeSafe Jev decisions out; policy routing stays in Rust code. Project guide.
- [typesafeai-cli](https://github.com/maddygoround/typesafeai-cli) — Python `typesafe` CLI for TypeSafe Jev ask/decide/screen/verify flows for humans and agents. Project guide.
- [unsafe-c-finder](https://github.com/etnt/unsafe-c-finder) — Classify C/C++ snippets and staged hunks with TypeSafe Jev through OpenRouter (unsafe probability then CWE bucket). Project guide.
- [AnchorLint](https://github.com/prantikmedhi/anchorlint) — Audits internal links in built HTML sites with deterministic checks plus optional TypeSafe Jev promise/relevance judgments. Project guide.
- [bitrate-advisor](https://github.com/affirmitv/bitrate-advisor) — Live-stream encoder settings from telemetry/history using TypeSafe Jev (OpenRouter) inside a deterministic safety envelope. Project guide.
- [Clay JEV People Ranker](https://github.com/promptgtm-shared/clay-jev-people-ranker) — Clay CLI people search plus TypeSafe Jev Choice/Noul qualification for semantic role fit (bundled operating-founder example). Project guide.
- [demo-expanso-jev](https://github.com/expanso-io/demo-expanso-jev) — Expanso Edge × TypeSafe Jev demos: fingerprint routine logs locally, ask Jev only on the remainder, route with hold-on-failure and live boards. Project guide.
- [DGP](https://github.com/numerous-com/dgp) — Experimental decision-based agent protocol with a Jev adapter, immutable evidence frames, typed assessments, and application-guarded commits; the local reference app simulates domain effects, and opt-in live mode sends decision evidence…
- [ExcelPilot](https://github.com/vikramlingam/excelpilot) — Live Excel agent with Qwen planning and TypeSafe Jev for intent routing, tool gating, and claim checks. Project guide.
- [fast-jev-compaction-pi](https://github.com/joslynSmall/fast-jev-compaction-pi) — This Pi extension asks Jev whether each completed tool call and its full result should be kept, then locally retains, truncates, or drops verbatim tool evidence in the compaction summary.
- [ghtriage](https://github.com/KalyanM45/GitHub-Issue-Classification-Using-Jev) — Classifies GitHub issues with TypeSafe Jev typed labels and calibrated confidence; writes are opt-in (`ghtriage`). Project guide.
- [japanese-jev-lint](https://github.com/pankona/japanese-jev-lint) — Go CLI (`jjl`) that flags Japanese sentences with TypeSafe Jev Noul probabilities (plus local です/ます regex); no rewrite generation. Project guide.
- [Jev the Janitor](https://github.com/kylehovance-ai/jev-the-janitor) — Markdown vault janitor: TypeSafe Jev votes on each note; code adds frontmatter or quarantines secrets (dry-run default; offline mode). Project guide.
- [jev-acp](https://github.com/formulahendry/jev-acp) — Standalone ACP agent for Jev Choice, Score, and Noul decisions, with guided input, reusable templates, and probability displays; requires a TypeSafe API key and sends decision inputs to TypeSafe.
- [jev-certify](https://github.com/nikkoxgonzales/jev-certify) — Early Python toolkit and CLINC150 study of conformal routing thresholds and prediction-powered audits over Jev 1.13 through OpenRouter, with request plans, 2,412 journalled answers and usage records, analysis code, and tests; its…
- [jev-corrective-rag](https://github.com/sudeshkar/jev-corrective-rag) — Corrective RAG demo: TypeSafe Jev typed gates for triage/grading/verify; generative LLM only writes answers. Project guide.
- [jev-demo](https://github.com/minghanminghan/jev-demo) — A customer-service routing demo that batches Jev questions before following the resulting route.
- [jev-evolve](https://github.com/novaleolin/jev-evolve) — Self-improving agents whose every decision is a typed TypeSafe Jev question, with reports separating real gains from selection noise. Project guide.
- [jev-gates](https://github.com/carlchou0dailyfresh/jev-gates) — Composable three-valued semantic logic circuits from TypeSafe Jev judgments and exact rules, with mock/offline demos (distinct from typesafe-agent-gates). Project guide.
- [jev-packs](https://github.com/dtduc-git/jev-packs) — Evidence-gated Jev question-pack registry with golden cases and a reproducible offline multi-backend scoreboard. Project guide.
- [jev-planner](https://github.com/rxova/jev-planner) — With N agents, `--mode ultra` makes 2N + 1 agent calls: drafts, reviews, and final synthesis, plus N if Jev requests another review. The default `balanced` makes as few as N + 1 and never more than…
- [jev-prompt-sentry](https://github.com/ca7ai/jev-prompt-sentry) — Anthropic Messages reverse proxy that screens jailbreaks/injections with one batched TypeSafe Jev call (PolyForm Noncommercial). Project guide.
- [jev-table](https://github.com/dtduc-git/jev-table) — Local-first CLI that adds TypeSafe Jev AI columns to CSV/JSONL with confidence, review queue, resume, and dry-run cost preview. Project guide.
- [jev.tg](https://github.com/Wing9897/jev.tg) — Local Telegram filter stores channel messages locally and sends them in batches to Jev or a local model to keep only messages matching natural-language conditions.
- [jevlens](https://github.com/k4its1t/jevlens) — Evaluate, calibrate, replay, and monitor TypeSafe Jev decisions from labeled datasets with threshold suggestions and optional Streamlit/CI. Project guide.
- [JevScope](https://github.com/jeiel85/jevscope) — Local-first visual workbench and JSONL regression testbench for TypeSafe Jev projects. Project guide.
- [Moongate](https://github.com/brickfrog/moongate) — GitHub Action that evaluates committed diffs against JSON semantic rules with TypeSafe Jev and reports annotations from your thresholds. Project guide.
- [n8n-nodes-typesafe](https://github.com/Biztactix/n8n-nodes-typesafe) — n8n community node for TypeSafe System One noul/choice/score questions over workflow text or JSON. Project guide.
- [pi-Jev-browser](https://github.com/laihenyi/pi-Jev-browser) — Pi extension where TypeSafe Jev chooses each Playwright browser action over a structured DOM observation in a bounded loop. Project guide.
- [pi-jev-compact](https://github.com/ilkerulusoy/pi-jev-compact) — A Pi context-pruning extension targeting tool history by default, with optional assistant-prose pruning.
- [pi-jev-effort](https://github.com/namenu/pi-jev-effort) — Pi extension: TypeSafe Jev scores prompt difficulty and sets thinking level, capped by remaining quota/burn (distinct from pi-jev-router). Project guide.
- [semgate](https://github.com/m-mizutani/semgate) — Go net/http middlewares that ask TypeSafe Jev typed questions about each request, then allow, block, or route. Project guide.
- [Testimonial miner](https://github.com/AppitStudio/testimonial-miner) — Python CLI that finds quotable user praise in Gmail mailboxes with one Jev request per email (message kind, app, praise quality, and a Noul per sentence) and stores verbatim quotes for review; requires a TypeSafe key and Google app…
- [typesafe-computer-use-win](https://github.com/Vatsa10/typesafe-computer-use-win) — Windows port of typesafe-computer-use: UI Automation + OCR with TypeSafe Jev decisions (`winclicker`). Project guide.
- [wakegate](https://github.com/shitianfang/wakegate) — Experimental TypeScript gate for long-running agents on Workers, Durable Objects, and Node: before a sleeping agent's LLM is resumed on a timer or incoming event, Jev answers one Choice (wake, not yet, unrelated) against the agent's own…
- [Jev on Cloudflare Workers AI](https://developers.cloudflare.com/ai/models/typesafe/jev) — Workers AI binding and REST samples asking a noul, a choice and a score in one call, with the full response including per-answer confidence.
- [spring-ai-typesafe](https://spring.io/blog/2026/09/21/spring-ai-typesafe-structured-judgment) — A community Spring AI starter bringing typed decisions to Java, with a builder API over the three question types.
- [Tripwire](https://github.com/anuran-de/tripwire) — Streaming proxy that trips on partial LLM output and can abort upstream mid-flight, with TypeSafe Jev or a heuristic detector. Project guide.
- [TypeSafe models in Pydantic AI](https://pydantic.dev/docs/ai/models/typesafe) — First-party Pydantic AI support: an Agent with output_type=bool over the typesafe:jev-latest model string.
- [TypeSafe pass-through on LiteLLM](https://docs.litellm.ai/docs/pass_through/typesafe) — Proxy Jev through LiteLLM for unified keys and cost tracking, with any path under /typesafe/ passed straight through.

## Awesome lists & indexes

Other curated indexes this catalog merges.

- [langchain](https://github.com/langchain-ai/langchain) — 146.8K stars — An optional JEV classifier integration for Python LangChain workflows. [Source](https://github.com/langchain-ai/langchain/blob/eba445b7563d1709427bd8072892975a6ea59fdc/libs/partners/typesafe/langchain_typesafe/classifier.py)
- [litellm](https://github.com/BerriAI/litellm) — 59.4K stars — LiteLLM can use JEV inside its complexity-based model router. [Source](https://github.com/BerriAI/litellm/blob/56116079c8022da0e8f7ff9ccb017ad5aca5aed2/litellm/router_strategy/complexity_router/jev_classifier.py#L70)
- [ai](https://github.com/vercel/ai) — SDK integration · 26.9K starsMaps choice, score, and yes/no questions onto a unified evaluate interface.
- [Jev Ultrafast](https://github.com/browser-use/jev-ultrafast) — , Browser agent whose every step is one Jev choice over an indexed element table, a small LLM types only when the action is TYPE_TEXT; Zürich to London on Google Flights in 7.1 seconds.…
- [QuantDinger](https://github.com/OpenByteInc/QuantDinger) — Self-hosted quantitative trading platform that uses Jev System One as an optional, auditable PASS / REJECT gate for strategy and Quick Trade entry orders, with LLM fallback and deterministic bypasses for exits and protective orders;…
- [agentgateway](https://github.com/agentgateway/agentgateway) — Three Score questions on a shared severity scale, blocking the request when two or more cross the line, and failing closed.
- [Awesome JEV (yibie)](https://github.com/yibie/awesome-jev) — 1.0K stars — A large community directory of public JEV projects, integrations, and discussions.
- [NewsJack](https://github.com/elvisun/newsjack) — 1.3K stars — An open-source PR workflow that screens a live news feed for timely brand opportunities. [Source](https://github.com/elvisun/newsjack/tree/092d882fc69912622f620c50eb493afe625f99dc/demos/news-desk-dealer)
- [Awesome JEV by TypeSafe](https://github.com/Anil-matcha/awesome-jev-by-typesafe) — 772 stars — An evidence-backed playbook of JEV use cases, patterns, prompts, and starter code.
- [Awesome JEV (HeyJunPenn)](https://github.com/heyjunpenn/awesome-jev) — 148 stars — A multilingual, community-maintained catalogue of open-source JEV projects.
- [Awesome JEV Tools](https://github.com/v-modal/awesome-jev-tools) — 628 stars — A curated directory focused on tools built for JEV and TypeSafe System One.
- [Awesome TypeSafe](https://github.com/AbdelStark/awesome-typesafe) — 431 stars — A curated list of official and community resources for TypeSafe, System One, and JEV.
- [Awesome TypeSafe JEV](https://github.com/AbdelStark/awesome-typesafe-jev) — 431 stars — A source-backed field guide to TypeSafe JEV projects, SDKs, demos, and evaluations.
- [Awesome JEV Projects](https://github.com/logicrw/awesome-jev-projects) — A sibling directory aiming at ecosystem breadth with commit-pinned sources, four README languages and a generated site.
- [Awesome JEV (cobanov)](https://github.com/cobanov/awesome-jev) — 316 stars — A source-backed list of projects built with JEV / TypeSafe System One.
- [Awesome JEV (AnotiaWang)](https://github.com/AnotiaWang/awesome-jev) — 257 stars — A curated list of JEV applications, libraries, and System One resources.
- [Awesome JEV Gallery](https://github.com/OmniJev/awesome-jev-gallery) — 159 stars — A gallery of System One papers, open reproductions, and independent evaluations.
- [Awesome Jev (kydlikebtc)](https://github.com/kydlikebtc/awesome-jev) — Catalog-driven bilingual awesome list with link checks.
- [Awesome JEV (fatwang2)](https://github.com/fatwang2/awesome-jev) — A sibling directory whose submissions are reviewed by Jev itself, with a notably thorough list of multi-language community clients.
- [Awesome Jev](https://github.com/hellogumbo/awesome-jev) — The largest list, with a searchable site.
- [Awesome JEV TypeSafe](https://github.com/valentynkit/awesome-jev-typesafe) — 125 stars — A TypeSafe JEV resource list centered on typed, confidence-aware decisions.
- [Awesome AI Scientist](https://github.com/Omni-Scientist/Awesome-AI-Scientist) — , Sibling list, AI systems that do science.
- [jegrep](https://github.com/can1357/jegrep) — 75 stars — Semantic grep for live code trees: describe what you need, get files and original line ranges without building an index. [Source](https://github.com/can1357/jegrep/blob/a280f14f6da8163bde67e0c49f58b23517a02882/src/jev.rs)
- [Awesome JEV (AppitStudio)](https://github.com/AppitStudio/awesome-jev) — 73 stars — A curated JEV resource list with runnable typed-decision examples.
- [yzfly/awesome-jev-zh](https://github.com/yzfly/awesome-jev-zh) — Chinese-language list, refreshed daily.
- [Awesome Jev (BeatAPI)](https://github.com/BeatAPI/awesome-jev) — Curated awesome list of Jev ecosystem links.
- [Awesome Jev (MrJev)](https://github.com/MrJev/awesome-jev) — Curated awesome list of Jev ecosystem links.
- [Awesome Open System One](https://github.com/rupeshpoojary9/awesome-open-system-one) — Open-only System One models, benchmarks, calibration, and constrained decoding.
- [Awesome RSI](https://github.com/Omni-Scientist/Awesome-RSI) — , Sibling list, systems whose improvement loop modifies itself.
- [#17](https://github.com/MrJev/awesome-jev/issues/17) — ). Two things get mixed up in that question, and they are worth separating.
- [Awesome Jev Projects (live site)](https://logicrw.github.io/awesome-jev-projects/en) — Searchable English radar UI for logicrw listings.
- [Awesome Jev Projects (site root)](https://logicrw.github.io/awesome-jev-projects) — Radar home (lang query stripped on normalize); English UI also at /en.
- [Awesome TypeSafe Jev (live site)](https://abdelstark.github.io/awesome-typesafe-jev) — Browsable live directory for the AbdelStark list.
- [Browse the live gallery](https://beatapi.io/awesome-jev) — Live gallery UI for the BeatAPI curated ≥50-star JEV project catalogue.
- [Browser & OS Action (38)](https://logicrw.github.io/awesome-jev-projects/en/categories/browser-os-action) — Browser & OS Action (38) — System One / Jev related resource.
- [Classification (2)](https://logicrw.github.io/awesome-jev-projects/en/categories/classification-taxonomy) — Classification (2) — System One / Jev related resource.
- [CLI & Pipelines (29)](https://logicrw.github.io/awesome-jev-projects/en/categories/cli-pipelines) — CLI & Pipelines (29) — System One / Jev related resource.
- [Code Navigation (13)](https://logicrw.github.io/awesome-jev-projects/en/categories/codebase-graph-pathfinding) — Code Navigation (13) — System One / Jev related resource.
- [Context GC (29)](https://logicrw.github.io/awesome-jev-projects/en/categories/context-gc-filter) — Context GC (29) — System One / Jev related resource.
- [Creative Tools (16)](https://logicrw.github.io/awesome-jev-projects/en/categories/creative-tools) — Creative Tools (16) — System One / Jev related resource.
- [Data & Search (28)](https://logicrw.github.io/awesome-jev-projects/en/categories/data-search) — Data & Search (28) — System One / Jev related resource.
- [Decision Tools (12)](https://logicrw.github.io/awesome-jev-projects/en/categories/decision-tools) — Decision Tools (12) — System One / Jev related resource.
- [Domain Tools (34)](https://logicrw.github.io/awesome-jev-projects/en/categories/domain-vertical-tools) — Domain Tools (34) — System One / Jev related resource.
- [High-Frequency / Games (40)](https://logicrw.github.io/awesome-jev-projects/en/categories/high-frequency-simulation) — High-Frequency / Games (40) — System One / Jev related resource.
- [JevList](https://jevlist.ai) — . Explore the projects in this directory through a searchable web interface. We're continually improving the experience—take a look and let us know what you think!
- [MCP & Integrations (30)](https://logicrw.github.io/awesome-jev-projects/en/categories/mcp-integrations) — MCP & Integrations (30) — System One / Jev related resource.
- [Model Routing (38)](https://logicrw.github.io/awesome-jev-projects/en/categories/routing-cost-optimization) — Model Routing (38) — System One / Jev related resource.
- [mrjev.com](https://mrjev.com/projects) — .
- [Original case · 583K views](https://x.com/elvissun/status/2100951347080421409) — Original case · 583K views — System One / Jev related resource.
- [SDK & Decision Frameworks (90)](https://logicrw.github.io/awesome-jev-projects/en/categories/sdk-decision-frameworks) — SDK & Decision Frameworks (90) — System One / Jev related resource.
- [SDK Integrations (6)](https://logicrw.github.io/awesome-jev-projects/en/categories/sdk-integrations) — SDK Integrations (6) — System One / Jev related resource.
- [Security & Guardrails (41)](https://logicrw.github.io/awesome-jev-projects/en/categories/security-guardrails) — Security & Guardrails (41) — System One / Jev related resource.
- [systemonemodels.org](https://systemonemodels.org/examples/alternatives) — Living index of open reproductions, classifiers, and structured-output libraries.
- [Voice & Conversation (4)](https://logicrw.github.io/awesome-jev-projects/en/categories/voice-conversation) — Voice & Conversation (4) — System One / Jev related resource.
- [what each tool sends](https://mrjev.com/best-jev-tools) — , Hands-on reviews of 72 community projects, 66 run in a container with a real key to record what leaves your machine; a password in a database URL and world-readable prompt logs, fixed upstream.…

## Community

TypeSafe chat, social, and the launch thread.

- [Discord](https://discord.gg/typesafe) — Official community server for builders, support, and discussion.
- [Hacker News launch thread](https://news.ycombinator.com/item) — The launch thread, and the densest single collection of scepticism: unsupported RLCD claims, apples-to-oranges latency comparisons, and the deliberate absence of public benchmarks.
- [LinkedIn](https://linkedin.com/company/typesafe-ai) — Company announcements and hiring updates.
- [Show and Tell](https://discord.com/channels/1483217544214085663/1483217545040232493) — Builder demos and work in progress; joining the Discord server is required.
- [X](https://x.com/typesafeai) — Product and research updates.

## Sources

This catalog consolidates and deduplicates entries from:

- [AbdelStark/awesome-typesafe-jev](https://github.com/AbdelStark/awesome-typesafe-jev)
- [logicrw/awesome-jev-projects](https://github.com/logicrw/awesome-jev-projects)
- [OmniJev/awesome-jev-gallery](https://github.com/OmniJev/awesome-jev-gallery)
- [AppitStudio/awesome-jev](https://github.com/AppitStudio/awesome-jev)
- [BeatAPI/awesome-jev](https://github.com/BeatAPI/awesome-jev)
- [rupeshpoojary9/awesome-open-system-one](https://github.com/rupeshpoojary9/awesome-open-system-one)
- [kydlikebtc/awesome-jev](https://github.com/kydlikebtc/awesome-jev)
- [MrJev/awesome-jev](https://github.com/MrJev/awesome-jev)
- [systemonemodels.org/examples/alternatives](https://systemonemodels.org/examples/alternatives/)
- [r/LLMDevs — 287 Jev projects / top 20](https://www.reddit.com/r/LLMDevs/comments/1wko2e5/i_reviewed_287_opensource_jev_projects_here_are/)

Plus official TypeSafe pages, independent essays (Archer Hume, lilting.ch, Latent.Space, Learn Jev, etc.), Tier A/B open reproductions, a 2026-09-24 logicrw projects.json refresh for missing evidenced integrations, and the [r/LLMDevs 287-project / top-20 roundup](https://www.reddit.com/r/LLMDevs/comments/1wko2e5/i_reviewed_287_opensource_jev_projects_here_are/).

Machine-readable dump: [`links.json`](links.json). Star cache: [`stars_cache.json`](stars_cache.json). Ingest map: [`SOURCES.md`](SOURCES.md). Counts: [`stats.txt`](stats.txt).

## Contributing

Prefer fixing upstream awesome lists; this file is a merge. When adding here: one factual line, working URL, System One / Jev relevance, no LayaAir-style name collisions, no empty stubs.

Regenerate with `python3 build.py`. If `raw/` ingest artifacts are present they are merged first; otherwise the script reloads [`links.json`](links.json) and re-renders. Keep category mapping in `build.py` in sync with README sections.

Within-section order is **pin/landmark first**, then **GitHub star count** (cached in [`stars_cache.json`](stars_cache.json)), then title — not pure editorial PageRank. Refresh stars: `python3 build.py --refresh-stars` (uses authenticated `gh api graphql` in batches; skips non-GitHub URLs).

## License

This compilation is dedicated to the public domain under [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/). Individual projects and linked content retain their own licenses and terms.

# COMP11212 — While Language Study Notebooks

Interactive study materials for *Fundamentals of Computation*, Part 2 (University of Manchester). A series of Jupyter notebooks built around a working interpreter for the **While** language.

> **🚀 Start here:** [`notebooks/00_pre_study.ipynb`](notebooks/00_pre_study.ipynb) — a 42-cell pre-study primer that gives the **whole-course map** in pure Python, with every formal-notation idea rendered side-by-side with its Python equivalent. Read it first (60–90 minutes); the formal notebooks below land much faster afterwards.

Currently covers:

- **Pre-study primer (Notebook 00):** the whole course in one continuous Python notebook, with every formal-notation idea rendered side-by-side with its Python equivalent. ~35 cells, 4 predict cells, one interactive `ipywidgets` small-step stepper. Read this first to break the ice.
- **Week 6 (Chapters 1–2):** syntax + small-step operational semantics. Traces in the formal `⟨S, σ⟩ ⇒ ⟨S', σ'⟩` notation, produced by Python you can read.
- **Week 7 (Chapter 3):** complexity and asymptotic analysis. Step counting, recognising classes, big O / Ω / Θ formal definitions, growth-rate plots.
- **Week 8 (Chapter 4):** Hoare logic — proving programs correct. Predicates, triples `{P} S {Q}`, the 6 partial-correctness rules, total correctness with loop variants, four worked examples (β, gcd, quadratic, Collatz).
- **Week 9 (Chapter 5):** Computability — what can be computed at all. Computable functions, decidability, semidecidability, the Halting Problem, universal programs, Church-Turing thesis.
- **Week 10 (Chapter 6):** Encodings — the bijections (β, φ, ψ, φ_S) that turn integers, pairs, lists, and While programs into natural numbers. Cantor's diagonal proof. Concrete Python implementations of every encoding.
- **Appendix (math + big-step):** Math background recap (functions, relations, countability) + the *big-step operational semantics* — an alternative to chapter 2's small-step. Five rules, worked example for division, exercises 58–67.

📎 **Cheatsheets:**
- [`CHEATSHEET.md`](CHEATSHEET.md) — chapters 1 and 2 (syntax + small-step semantics). Symbols with pronunciation, Python equivalents, the 6 inference rules, exam phrasing.
- [`CHEATSHEET_COMPLEXITY.md`](CHEATSHEET_COMPLEXITY.md) — chapter 3 (complexity). Symbols + pronunciation, class hierarchy, recognition rules, simplification rules.
- [`CHEATSHEET_HOARE.md`](CHEATSHEET_HOARE.md) — chapter 4 (Hoare logic). Symbols, the 6 partial rules, the total while rule, loop invariant + variant heuristics, exam-style derivation format.
- [`CHEATSHEET_COMPUTABILITY.md`](CHEATSHEET_COMPUTABILITY.md) — chapter 5 (computability). Symbols, decidable vs semidecidable, the Halting-Problem proof skeleton, Church-Turing.
- [`CHEATSHEET_ENCODINGS.md`](CHEATSHEET_ENCODINGS.md) — chapter 6 (encodings). β, φ, ψ, φ_S formulas, decoding recipes, Cantor diagonal proof template.
- [`CHEATSHEET_APPENDIX.md`](CHEATSHEET_APPENDIX.md) — appendix (math + big-step). Math vocabulary, the 5 big-step rules, big-step vs small-step comparison.

## Quick start

### Windows (PowerShell)

```powershell
# from the repo root
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r notebooks\requirements.txt
jupyter notebook notebooks\00_pre_study.ipynb
```

### macOS / Linux

```bash
# from the repo root
python3 -m venv .venv
source .venv/bin/activate
pip install -r notebooks/requirements.txt
jupyter notebook notebooks/00_pre_study.ipynb
```

That opens **the pre-study primer** in your browser. Read it through (60–90 min), then move on to N1 → N2 → N3 → N4 in order. The primer is ice-breaking; the formal notebooks are the deep dive.

If the `Activate.ps1` script is blocked on Windows, run PowerShell as admin once and `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`.

## What's in here

```
.
├── notebooks/
│   ├── while_lang.py              # the While interpreter (~900 lines: parser, semantics, complexity, Hoare, encoding, big-step)
│   ├── requirements.txt           # lark + jupyter + matplotlib
│   ├── 00_pre_study.ipynb         # N0 — pre-study primer (whole course in pure Python, side-by-side with formal notation)
│   ├── 01_interpreter.ipynb       # N1 — walk-through of the interpreter
│   ├── 02_syntax.ipynb            # N2 — Chapter 1 syntax + Examples 1-6 + Exercises 1-10
│   ├── 03_semantics.ipynb         # N3 — Chapter 2 §2.1-2.4 + Examples 7-11 + Exercises 11-16
│   ├── 04_reasoning.ipynb         # N4 — Propositions 2/3 + Exercises 17-18 + quiz + bridge
│   ├── 05_quiz.ipynb              # N5 — 20-question quiz on chapters 1-2
│   ├── 06_counting_steps.ipynb    # N6 — Chapter 3 §3.1, 3.4, 3.5 + Exercises 19, 20, 23, 24, 25
│   ├── 07_big_o.ipynb             # N7 — Chapter 3 §3.2, 3.3, 3.6 + Exercises 21, 22, 26, 27, 28, 29
│   ├── 08_quiz_chapter3.ipynb     # N8 — 20-question quiz on chapter 3
│   ├── 09_hoare_partial.ipynb     # N9 — Chapter 4 §4.1-4.5 + Exercises 30, 31
│   ├── 10_hoare_total.ipynb       # N10 — Chapter 4 §4.6-4.9 + Exercises 32-38
│   ├── 11_quiz_chapter4.ipynb     # N11 — 20-question quiz on chapter 4
│   ├── 12_computability.ipynb     # N12 — Chapter 5 §5.1-5.3 + Exercises 39-50
│   ├── 13_halting_universality.ipynb  # N13 — Chapter 5 §5.4-5.6 + Exercises 51, 52
│   ├── 14_quiz_chapter5.ipynb     # N14 — 20-question quiz on chapter 5
│   ├── 15_encodings.ipynb         # N15 — Chapter 6 (all of it) + Exercises 53-57
│   ├── 16_quiz_chapter6.ipynb     # N16 — 20-question quiz on chapter 6
│   ├── 17_appendix.ipynb          # N17 — Appendix A + B (math + big-step) + Ex 58-67
│   └── 18_quiz_appendix.ipynb     # N18 — 20-question quiz on the appendix
├── CHEATSHEET.md                  # cheatsheet for chapters 1-2
├── CHEATSHEET_COMPLEXITY.md       # cheatsheet for chapter 3
├── CHEATSHEET_HOARE.md            # cheatsheet for chapter 4
├── CHEATSHEET_COMPUTABILITY.md    # cheatsheet for chapter 5
├── CHEATSHEET_ENCODINGS.md        # cheatsheet for chapter 6
├── CHEATSHEET_APPENDIX.md         # cheatsheet for the appendix (math + big-step)
├── chapter1.txt ... chapter6.txt, Appendix.txt   # course material (untracked — Manchester copyright)
├── lecture_transcripts/           # lecture transcripts (untracked)
├── exersise*_solution.txt         # official solutions provided (untracked)
└── quiz.txt                       # week 6 quiz (untracked)
```

## How to use the notebooks

**Read them top-to-bottom in order — N0 → N1 → N2 → ...** Each builds on the previous. N0 (the primer) is read-along and friction-free; from N1 onwards the formal pass begins.

Throughout the notebooks you'll see cells labelled **🎯 PREDICT**. These are the active-practice mechanism: they ask you to fill in your guess into a Python variable *before* running the next cell. The next cell uses `check_state(...)` / `check_steps(...)` / `count_steps(...)` to tell you if you got it right.

**Don't skip the predict cells.** That's where the "real grok" lives. If you skim past them you're just reading code, not learning.

### What each notebook contains

| Notebook | Covers | Key artifact |
|---|---|---|
| **N0 (primer)** | All 6 chapters as one continuous Python story, with side-by-side formal notation. 4 predict cells, one ipywidgets stepper. | Read-along whole-course map. Read once, ~60–90 min. |
| N1 | Interpreter mechanics: AST, states, A/B, `step`, three trace views | First full formal trace of a real program |
| N2 | BNF grammar, ambiguity, all 6 chapter examples, exercises 1–10 | Working While programs for division, gcd, primality, sqrt, Fibonacci |
| N3 | States, σ-updates, the small-step rules, examples 7–11, exercises 11–16 | Exercise 14 (Diophantine) showpiece — full formal trace |
| N4 | Propositions 2 & 3 (associativity), exercises 17 & 18, quiz, bridge to exam notation | "Translate Python intuition → exam-style proofs" section |
| N5 | 20-question quiz on chapters 1–2 | Auto-scored; per-section breakdown |
| N6 | Counting steps, recognising classes by inspection, exercises 19, 20, 23, 24, 25 | `count_steps()` and `step_growth()` over the chapter's worked examples |
| N7 | Big O / Ω / Θ formal definitions, propositions 8–12, exercises 21, 22, 26, 27, 28, 29 | Growth-rate plots showing why O(n²) overtakes 100·n |
| N8 | 20-question quiz on chapter 3 | Auto-scored; per-section breakdown |
| N9 | Hoare-logic partial correctness, the 6 rules, full division proof, exercises 30, 31 | `verify_triple()` empirically sanity-checks any Hoare triple |
| N10 | Total correctness via loop variants, β / gcd / quadratic / Collatz, exercises 32–38 | Full Hoare-logic derivations for power, sum, integer log, divisibility |
| N11 | 20-question quiz on chapter 4 | Auto-scored; per-section breakdown |
| N12 | Computability via Hoare triples, decidable vs semidecidable, closure under logic, exercises 39–50 | Verified examples of decidable predicates (triangular numbers, primality) |
| N13 | The Halting Problem proof, universal partial function ζ, Parameterization Theorem, Church-Turing thesis | Walkthrough of the diagonal-contradiction proof; partial-function analysis for Ex 51 |
| N14 | 20-question quiz on chapter 5 | Auto-scored; per-section breakdown |
| N15 | Cantor diagonal, β / φ / ψ / φ_S encodings, exercises 53–57 | Working `encode_*` and `decode_*` Python — every chapter formula implemented |
| N16 | 20-question quiz on chapter 6 | Auto-scored; per-section breakdown |
| N17 | Math vocabulary recap + big-step operational semantics + exercises 58–67 | `big_step()` evaluator that agrees with small-step `run()` on all terminating programs |
| N18 | 20-question quiz on the appendix | Auto-scored; per-section breakdown |

## The interpreter — quick reference

If you already understand the material and just want to use the interpreter directly:

```python
from while_lang import parse, run, trace, check_state, check_steps

# Run a program, get final state as a dict
run('x := 1; y := 5; while !(y = 0) do (x := x * 2; y := y - 1)', {})
# → {'x': 32}

# Get a formal small-step trace
print(trace('x := 5; y := x + 1', {}, view='formal'))

# Get a state-tracking table (Example 8 / 11 style)
print(trace(prog, sigma, view='table'))

# Predict-and-check
check_state(predicted={'x': 32}, prog=power_program, state={'m': 2, 'n': 5})
```

### ASCII syntax (Greek-letter equivalents in the *output*)

When typing While programs into Python, use ASCII equivalents:

| Concept | Type this | Output renders as |
|---|---|---|
| less-than-or-equal | `<=` | `≤` |
| not | `!` | `¬` |
| and | `&` | `∧` |
| multiply | `*` | `×` |
| true / false | `tt` / `ff` | `tt` / `ff` |
| assignment | `:=` | `:=` |

There's no `<` (use `a <= b & !(a = b)`), no `>` (swap), no `∨` (De Morgan: `!(!a & !b)`).

## Caveats

- **Exercises 8 and 9** depend on Sections 6.2.1 / 6.2.2 of the course notes which weren't part of the materials provided. The corresponding cells in N2 explain the situation and sketch the standard candidates (β-style integer encoding, Cantor pairing). Verify with a GTA before relying on those.
- **Proof-style exercises 15, 17, 18** are presented in the chapter's argument style, but Manchester examiners may have a specific phrasing in mind. The notebooks flag these clearly. Verify with a GTA if exam phrasing matters.
- **Quiz Q3 in `quiz.txt`** is missing some brackets in the program text as written — the notebook adds them, since the BNF requires brackets around if/while bodies. The intended trace per the quiz feedback is preserved.

## Verification

All notebooks execute cleanly under the project's `.venv`: every cell runs, no errors. To re-verify yourself:

```bash
# from notebooks/
jupyter nbconvert --to notebook --execute 00_pre_study.ipynb --output _check.ipynb
# repeat for 01_ ... 18_; should produce no errors
```

## Why this approach

The standard way to teach operational semantics is on paper: stare at `⟨S, σ⟩ ⇒ ⟨S', σ'⟩` rules until they click. That works for some students. For others (probably the majority), it doesn't.

This project takes a different approach: **build the executable definition first, then read formal traces it produces.** The Python is the implementation; the formal notation is the rendering. One artifact, two views. When you watch the trace get built up step-by-step from code you understand, the symbols stop being decoration — they start being a recording of something that just happened.

The four-notebook structure plus exercise depth came out of a single `/office-hours` planning session; if you're curious, see `~/.gstack/projects/COMP11212/` (or the equivalent on whichever machine that ran on).

## Acknowledgements

Original course material designed by Dave Lester, adapted by Giles Reger and Gareth Henshall, completely rewritten by Andrea Schalk for 2024–25. This study companion is independent of the course staff.

# COMP11212 Week 6 — While Language Study Notebooks

Interactive study materials for *Fundamentals of Computation*, Part 2, Week 6 (University of Manchester). Four Jupyter notebooks built around a working interpreter for the **While** language that prints traces in the formal small-step operational-semantics notation — `⟨S, σ⟩ ⇒ ⟨S', σ'⟩` — produced by Python you can read.

📎 **See [CHEATSHEET.md](CHEATSHEET.md)** for a one-stop reference: every symbol with how to *pronounce* it, every concept mapped to its Python equivalent, the 6 inference rules, and exam-style phrasing.

## Quick start

### Windows (PowerShell)

```powershell
# from the repo root
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r notebooks\requirements.txt
jupyter notebook notebooks\01_interpreter.ipynb
```

### macOS / Linux

```bash
# from the repo root
python3 -m venv .venv
source .venv/bin/activate
pip install -r notebooks/requirements.txt
jupyter notebook notebooks/01_interpreter.ipynb
```

That opens N1 in your browser. Run cells top-to-bottom. Move on to N2 → N3 → N4 in order.

If the `Activate.ps1` script is blocked on Windows, run PowerShell as admin once and `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`.

## What's in here

```
.
├── notebooks/
│   ├── while_lang.py            # the While interpreter (~570 lines, all you need)
│   ├── requirements.txt         # lark + jupyter
│   ├── 01_interpreter.ipynb     # N1 — walk-through of the interpreter
│   ├── 02_syntax.ipynb          # N2 — Chapter 1 syntax + Examples 1-6 + Exercises 1-10
│   ├── 03_semantics.ipynb       # N3 — Chapter 2 §2.1-2.4 + Examples 7-11 + Exercises 11-16
│   ├── 04_reasoning.ipynb       # N4 — Propositions 2/3 + Exercises 17-18 + quiz + bridge
│   └── 05_quiz.ipynb            # N5 — 20-question self-quiz with auto-scoring
├── chapter1.txt, chapter2.txt   # course chapters (untracked — Manchester copyright)
├── lecture_transcripts/         # lecture transcripts (untracked)
├── exersise*_solution.txt       # official solutions provided (untracked)
└── quiz.txt                     # week 6 quiz (untracked)
```

## How to use the notebooks

**Read them top-to-bottom in order — N1 → N2 → N3 → N4.** Each builds on the previous.

Throughout the notebooks you'll see cells labelled **🎯 PREDICT**. These are the active-practice mechanism: they ask you to fill in your guess into a Python variable *before* running the next cell. The next cell uses `check_state(...)` or `check_steps(...)` to tell you if you got it right and shows the formal trace either way.

**Don't skip the predict cells.** That's where the "real grok" lives. If you skim past them you're just reading code, not learning.

### What each notebook contains

| Notebook | Covers | Key artifact |
|---|---|---|
| N1 | Interpreter mechanics: AST, states, A/B, `step`, three trace views | First full formal trace of a real program |
| N2 | BNF grammar, ambiguity, all 6 chapter examples, exercises 1–10 | Working While programs for division, gcd, primality, sqrt, Fibonacci |
| N3 | States, σ-updates, the small-step rules, examples 7–11, exercises 11–16 | Exercise 14 (Diophantine) showpiece — full formal trace |
| N4 | Propositions 2 & 3 (associativity), exercises 17 & 18 (proof-style), quiz, bridge to exam notation | "Translate Python intuition → exam-style proofs" section |
| N5 | 20-question self-quiz spanning everything: syntax, grammar, states, A/B, all 5 small-step rules, traces, termination, reasoning | Auto-scored. Section breakdown tells you which area to re-read if a section drops below 100% |

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

All four notebooks execute cleanly: 133 cells, 0 errors. 22 spot-checks against expected chapter results all pass — see the commit message for the full list. To re-verify yourself:

```bash
# from notebooks/
jupyter nbconvert --to notebook --execute 01_interpreter.ipynb --output _check.ipynb
# repeat for 02_, 03_, 04_; should produce no errors
```

## Why this approach

The standard way to teach operational semantics is on paper: stare at `⟨S, σ⟩ ⇒ ⟨S', σ'⟩` rules until they click. That works for some students. For others (probably the majority), it doesn't.

This project takes a different approach: **build the executable definition first, then read formal traces it produces.** The Python is the implementation; the formal notation is the rendering. One artifact, two views. When you watch the trace get built up step-by-step from code you understand, the symbols stop being decoration — they start being a recording of something that just happened.

The four-notebook structure plus exercise depth came out of a single `/office-hours` planning session; if you're curious, see `~/.gstack/projects/COMP11212/` (or the equivalent on whichever machine that ran on).

## Acknowledgements

Original course material designed by Dave Lester, adapted by Giles Reger and Gareth Henshall, completely rewritten by Andrea Schalk for 2024–25. This study companion is independent of the course staff.

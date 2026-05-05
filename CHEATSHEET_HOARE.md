# COMP11212 Chapter 4 — Hoare Logic Cheat Sheet

Symbols, pronunciation, the 6 partial-correctness rules, the total-correctness while rule, and recipes for finding loop invariants and variants. Companion to `CHEATSHEET_SEMANTICS.md` (chapters 1–2) and `CHEATSHEET_COMPLEXITY.md` (chapter 3).

---

## §1. Symbols — what to say out loud

### Hoare-logic notation

| Symbol | Name | Say it like | What it means |
|:-:|:--|:--|:--|
| **`{P} S {Q}`** | Hoare triple, partial | "P, S, Q" / "the Hoare triple P, S, Q" | If S terminates from P-state, ends in Q-state. |
| **`{P} S {⇓ Q}`** | Hoare triple, total | "P, S, totally Q" / "P, S, terminates and Q" | S terminates from P-state AND ends in Q-state. |
| **`⇓`** | down-arrow / falls-to | "terminates and" / "falls to" | Termination flag in total correctness. |
| **`P[x ↦ a]`** | substitution | "P with x replaced by a" | Predicate where every free `x` is swapped for `a`. |
| **`P → Q`** | implication | "P implies Q" / "if P then Q" | Logical implication (in the meta-language). |
| **`P ↔ Q`** | iff / biconditional | "P iff Q" / "P if and only if Q" | Both directions. |
| **`m̄, n̄, ī`** | bar-letters / ghost variables | "m-bar" / "the ghost m" | Italic mathematical names that capture *original* input values; never mutated. |

### Math you'll see in predicates

| Symbol | Say it like | Notes |
|:-:|:--|:--|
| **`∀x ∈ ℕ`** | "for all x in N" | Universal quantifier; allowed in predicates (not in While). |
| **`∃k ∈ ℤ`** | "there exists k in Z" | Existential quantifier. |
| **`m mod n`** | "m mod n" | Allowed in predicates even though While has no mod operator. |
| **`m div n`** | "m div n" / "m integer-divide n" | Same — meta-language can use any maths. |
| **`i \| n`** | "i divides n" | Divisibility relation. |
| **`gcd(m, n)`** | "gcd of m, n" | Greatest common divisor. |

---

## §2. The six rules of partial correctness — quick reference

### Rule 1 — Assignment

$$\{P[x \mapsto \mathcal{A}\,a]\}\ x := a\ \{P\}$$

**Read backwards:** to make `P` true *after*, the precondition is `P` with `x` substituted by `a`.

**Mental cheat-sheet:**
- After `x := 5`, `x = 5` is just `tt`.
- After `x := x + 1`, `x > 6` requires `x > 5` before.
- After `y := y + 1`, anything not mentioning `y` is unchanged.

### Rule 2 — Skip

$$\{P\}\ \textbf{skip}\ \{P\}$$

Trivial. State doesn't change.

### Rule 3 — Composition

$$\dfrac{\{P\}\ S\ \{Q\} \qquad \{Q\}\ S'\ \{R\}}{\{P\}\ S; S'\ \{R\}}$$

Glue two triples via shared middle `Q`.

### Rule 4 — Conditional

$$\dfrac{\{P \wedge \mathcal{B}\,b\}\ S\ \{Q\} \qquad \{P \wedge \neg \mathcal{B}\,b\}\ S'\ \{Q\}}{\{P\}\ \textbf{if } b \textbf{ then } S \textbf{ else } S'\ \{Q\}}$$

Both branches must establish the same `Q`. Each branch sees `P` plus knowledge of `b`'s truth.

### Rule 5 — While

$$\dfrac{\{P \wedge \mathcal{B}\,b\}\ S\ \{P\}}{\{P\}\ \textbf{while } b \textbf{ do } S\ \{P \wedge \neg \mathcal{B}\,b\}}$$

`P` is the **loop invariant**. Body preserves it when `b` is true. Post = `P ∧ ¬b` (we exited because `b` became false).

### Rule 6 — Consequence

$$\dfrac{P \to P' \quad \{P'\}\ S\ \{Q'\} \quad Q' \to Q}{\{P\}\ S\ \{Q\}}$$

**Strengthen pre, weaken post.** Lets you plug triples together when conditions don't match exactly.

---

## §3. The total-correctness while rule — the only rule that changes

$$\dfrac{P \to a \ge 0 \qquad \{P \wedge \mathcal{B}\,b \wedge \mathcal{A}\,a = k\}\ S\ \{\Downarrow P \wedge \mathcal{A}\,a < k\}}{\{P\}\ \textbf{while } b \textbf{ do } S\ \{\Downarrow P \wedge \neg\mathcal{B}\,b\}}$$

**Two extra ingredients beyond partial:**
1. **`P → a ≥ 0`** — the invariant guarantees the variant is non-negative.
2. **`a` strictly decreases** — encoded via fresh ghost `k` in pre, `a < k` in post.

The other 5 rules just gain the `⇓` arrow — the structure is identical to partial.

---

## §4. Loop invariant vs loop variant — the critical distinction

| Concept | What it is | What it does | Type |
|:--|:--|:--|:-:|
| **Loop invariant `P`** | A *predicate* preserved by the body | Encodes what the loop is *computing* — the relationship between variables that holds at every loop boundary | predicate |
| **Loop variant `a`** | A *non-negative arithmetic expression* that strictly decreases each iteration | Proves the loop *terminates* — finitely many decreases possible from any starting value | expression |

**Both are needed for total correctness.** Partial correctness needs only the invariant.

**Easy confusion to avoid:** "the variant" vs "the invariant" sound almost the same and both involve loops. Different concepts. The variant is one specific thing (an expression). The invariant is the entire predicate that captures what the loop is doing.

---

## §5. Loop invariant heuristics — finding good ones

A typical loop has *infinitely many* invariants. We want one **strong enough to imply the postcondition** when combined with `¬b`. Three guidelines:

1. **Look at the postcondition first.** Often a chunk of the post can be lifted directly. (Division: `m̄ = d·n̄ + r` is both invariant and core post.)
2. **Trace the loop on a small input** — `n = 4` or whatever. What relationship between the variables holds *every* iteration boundary?
3. **Include `≥ 0` clauses** when the invariant needs to support a variant for total correctness (e.g. `0 ≤ r` for division).

**Bad invariant signs:**
- It doesn't mention any variable changed by the body. (Then it's just a constant fact about inputs.)
- Combined with `¬b`, it doesn't imply the post.
- It fails on iteration 1 of a small example.

**Empirical sanity check:** use `verify_triple(invariant, body, invariant, [...some sample states with b true...])` from `while_lang.py`. If counter-examples appear, your candidate isn't an invariant.

---

## §6. Loop variant patterns

| Loop shape | Typical variant |
|:--|:--|
| `while x ≤ n do (...; x := x + 1)` | `n − x` (or `n + 1 − x`) |
| `while 1 ≤ x do (...; x := x − 1)` | `x` |
| `while x ≤ n do (...; x := x · 2)` | `n − x` (or `log₂ n − log₂ x` if you want exact) |
| `while ¬(x = y) do (decrease x or y)` | `x + y` (when neither alone monotonically decreases — gcd pattern) |
| `while ¬(switch = 1) do (...switch := 1...)` | Hard. Often need a domain-specific quantity. |
| `while ¬(y = 1) do (search forward via x := x + 1)` | `\|target\| − x` — works only if you know a target exists |

---

## §7. Recipes for proofs

### Standard proof template (partial correctness)

```
Goal: {P} S {Q}

If S = (S1; S2; ...; Sk):
  Apply ; rule repeatedly. Pick intermediate conditions that link them up.

If S has a loop:
  1. Find a candidate loop invariant I.
  2. Show {I ∧ b} body {I}.
  3. Apply while rule: {I} loop {I ∧ ¬b}.
  4. Use consequence + ; rules to glue with the rest.

For each assignment x := a:
  Apply := rule (read backwards).
  Pre = post[x ↦ a].

Use consequence whenever conditions don't match up exactly.
```

### Total-correctness extensions

```
Same as above, plus:
  - For each loop, find a variant a (non-negative arithmetic expression).
  - Show I → a ≥ 0.
  - In the body proof, introduce ghost k = a, show a < k in the post.
  - Apply the total while rule.
```

### Sanity checking a spec — the trivial-program attack

Before committing to a long proof, check: does the trivial program `m := 0; n := 1; ...` (or some other reset) satisfy the spec? If yes, you're missing a ghost variable. **Always check this.**

---

## §8. The compact derivation format (for exam answers)

The chapter's preferred format. Numbered lines, each citing the rule and which previous lines it depends on:

```
1. {P} ... {Q1}    by := rule
2. {Q1} ... {Q2}    by ; rule
3. {Q3} body {Q3}    by := rules + algebra
4. {Q3} loop {Q3 ∧ ¬b}    from 3 by while rule
5. {P} S {final}    from 1, 4 by ; rule and consequence
```

Each line states a triple and how it's justified. Use indentation/grouping in long lines to make the reading clear.

---

## §9. Things that are NOT in While but ARE in predicates

The predicate language is the meta-language — far richer than the program language:

| Construct | In While? | In predicates? |
|:--|:-:|:-:|
| `+`, `−`, `×` | ✓ | ✓ |
| `mod`, `div`, `√` | ✗ | ✓ |
| `<`, `≥`, `>` | ✗ (only `≤` and `=`) | ✓ |
| `∨`, `→`, `↔` | ✗ (only `∧` and `¬`) | ✓ |
| `∀`, `∃` | ✗ | ✓ |
| Divisibility `i \| n` | ✗ | ✓ |
| Powers `m^n` | ✗ (must compute via loop) | ✓ |
| `gcd`, `lcm`, factorials | ✗ | ✓ |
| Anything else from maths | ✗ | ✓ |

**Use this asymmetry.** Your spec can refer to `m̄ mod n̄` even though the program has no mod operator.

---

## §10. Common pitfalls

1. **Forgetting ghost variables.** `{m ≥ 0} S {m = d·n + r}` is satisfied by `m := 0; n := 0; d := 0; r := 0`. Pin the inputs with `m̄, n̄`.

2. **Mistaking "loop variant" for "loop invariant".** Variant is an expression that decreases. Invariant is a predicate that's preserved. They serve different purposes (termination vs correctness).

3. **Over-strong loop invariants.** If the invariant claims more than the body can re-establish, the proof gets stuck. Strengthen it just enough.

4. **Under-strong loop invariants.** If `I ∧ ¬b` doesn't imply the postcondition, the invariant is too weak. Add the missing piece.

5. **Forgetting `0 ≤ a` clauses for variants.** The total-correctness rule requires the invariant to imply `a ≥ 0`. If your invariant doesn't say `r ≥ 0` and your variant is `r`, the proof fails.

6. **Total correctness when termination is genuinely unprovable.** Quadratic search, Collatz, etc. Don't aim for `⇓` if the program might not terminate — settle for partial.

7. **The chapter's `B b` notation.** This means "the boolean evaluator B applied to expression b" — i.e. its truth value in the current state. When writing in pre/post conditions, you can usually just write `b` and have it mean "b is true."

---

## §11. The two systems on one page

```
PARTIAL CORRECTNESS — {P} S {Q}

  {P[x ↦ A a]} x := a {P}                      (assignment)
  {P} skip {P}                                  (skip)
  {P} S {Q}, {Q} S' {R} ⟹ {P} S; S' {R}        (composition)
  {P ∧ b} S {Q}, {P ∧ ¬b} S' {Q} 
      ⟹ {P} if b then S else S' {Q}            (if)
  {P ∧ b} S {P} ⟹ {P} while b do S {P ∧ ¬b}    (while — needs invariant)
  P→P', Q'→Q, {P'} S {Q'} ⟹ {P} S {Q}          (consequence)


TOTAL CORRECTNESS — {P} S {⇓ Q}

  Same as above, with ⇓ everywhere, EXCEPT the while rule:

  P → a ≥ 0,  {P ∧ b ∧ a = k} S {⇓ P ∧ a < k} 
      ⟹ {P} while b do S {⇓ P ∧ ¬b}            (while — needs invariant + variant)
```

---

## §12. The two-line elevator pitch

> **Hoare logic** lets us *prove* a program does the right thing.
> A triple `{P} S {Q}` says: starting in P, S either doesn't terminate or ends in Q.
> The total version `{P} S {⇓ Q}` adds termination — proven via a loop variant (a non-negative expression that strictly decreases each iteration).

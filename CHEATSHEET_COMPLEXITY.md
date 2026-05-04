# COMP11212 Chapter 3 — Complexity Cheat Sheet

Symbols, pronunciation, class hierarchy, recognition rules, and the propositions you'll use to simplify expressions. Companion to `CHEATSHEET.md` (which covers chapters 1–2).

---

## §1. Symbols — what to say out loud

### The three asymptotic classes

| Symbol | Name | Say it like | What it means |
|:-:|:--|:--|:--|
| **`O(f)`** | big O | "big O of f" | **Upper bound** — set of functions growing no faster than `f`. |
| **`Ω(f)`** | big Omega | "big Omega of f" / "big omega" | **Lower bound** — `f` grows no slower than the function. |
| **`Θ(f)`** | big Theta | "big Theta of f" / "big theta" | **Tight bound** — `f` grows at the same rate. |

Three more letters you'll see in passing:

| Symbol | Name | Say it like | What it means |
|:-:|:--|:--|:--|
| **o(f)** | little o | "little O of f" | Strict upper bound: `f` grows *strictly slower* (not used in this chapter, but mentioned in COMP26120). |
| **ω(f)** | little omega | "little omega" | Strict lower bound. |
| **`f ∼ g`** | tilde / equivalent | "f tilde g" / "f and g are asymptotically equivalent" | `O(f) = O(g)`. |

### Set theory + relations

| Symbol | Say it like | What it means |
|:-:|:--|:--|
| **`⊊`** | "strictly contained in" / "proper subset of" | `O(n) ⊊ O(n²)` — left side is a strictly smaller class. |
| **`⊆`** | "contained in" / "subset of" | Allows equality. |
| **`∈`** | "is in" / "is a member of" | `f ∈ O(g)` — `f` is in the big-O class. |
| **`⋃`** | "union" | `⋃ₘ O(nᵐ)` — union over all polynomial classes. |
| **`ℝ⁺`** | "the non-negative reals" / "R-plus" | `{x ∈ ℝ : x ≥ 0}` — domain of complexity functions. |

### Math you'll see in proofs

| Symbol | Say it like | What it means |
|:-:|:--|:--|
| **`⌊x⌋`** | "floor of x" | Greatest integer ≤ `x`. |
| **`⌈x⌉`** | "ceiling of x" | Smallest integer ≥ `x`. |
| **`\|f(x)\|`** | "absolute value of f of x" | Magnitude — used in big-O def to handle functions that might go negative. |
| **`log x`** | "log of x" | Logarithm — base doesn't matter for big-O (different bases differ by a constant). |
| **`logₐ b`** | "log base a of b" | Specific base. Identity: `logᵦ x = (1/logₐ b) · logₐ x`. |
| **`Σᵢ₌₁ⁿ`** | "sum from i equals 1 to n" | Summation. |
| **`Hₙ`** | "n-th harmonic number" | `Hₙ = 1 + 1/2 + 1/3 + ... + 1/n ≈ ln n`. Comes up in primality analysis. |

---

## §2. The big-O definition — three tightening notions

| Notion | Definition | Use when... |
|:--|:--|:--|
| **`f` dominates `g`** | For all `x`: `f(x) ≥ g(x)`. | Almost never — too strict. |
| **`f` eventually dominates `g`** | There exists `k`, for all `x ≥ k`: `f(x) ≥ g(x)`. | Captures "f beats g at large x." |
| **`g` is `O(f)`** | There exist `c, k ∈ ℝ⁺`, for all `x ≥ k`: `\|g(x)\| ≤ c · f(x)`. | The standard tool — ignores constant factors AND small inputs. |

**Practical takeaway:** in `O`, you get to pick BOTH a starting point `k` and a multiplier `c`. That's why constants and lower-order terms become invisible.

---

## §3. The class hierarchy — memorize this

```
O(1)  ⊊  O(log n)  ⊊  O(n)  ⊊  O(n log n)  ⊊  O(n²)  ⊊  O(n³)  ⊊  …  ⊊  O(2ⁿ)  ⊊  O(n!)
```

All inclusions strict. Each step grows asymptotically faster than the previous.

| Class | Name | Typical example | Tractable? |
|:-:|:--|:--|:-:|
| `O(1)` | constant | array access by index, hash lookup | ✓ |
| `O(log n)` | logarithmic | binary search | ✓ |
| `O(n)` | linear | linear scan, count occurrences | ✓ |
| `O(n log n)` | linearithmic / "n log n" | mergesort, heapsort | ✓ |
| `O(n²)` | quadratic | bubble sort, nested-loop comparison | ✓ |
| `O(n³)` | cubic | naive matrix multiplication | ✓ |
| `O(2ⁿ)` | exponential | brute-force subset enumeration | ✗ |
| `O(n!)` | factorial | brute-force permutations (TSP) | ✗ |

**Tractable ≈ polynomial.** If your algorithm is `O(nᵐ)` for any fixed `m`, it's tractable. Anything growing faster than every polynomial is intractable.

---

## §4. Recognising classes by inspection — the loop heuristic

Most of the time you don't need to count steps exactly. Look at the loops.

| Pattern | Class |
|:--|:-:|
| No loops | `O(1)` |
| Single loop bounded by `n`, body is `O(1)` | `O(n)` |
| Single loop bounded by `n`, body is `O(n)` | `O(n²)` |
| `k` nested loops, each bounded by `n` | `O(nᵏ)` |
| Loop counter halves each iteration (`x := x / 2`) | `O(log n)` |
| Loop counter doubles each iteration (`x := x * 2`) | `O(log n)` |
| Outer doubles, inner is `O(n)` | `O(n log n)` |
| Loop body itself doubles (recursive split with no work-saving) | `O(2ⁿ)` |
| Sequential loops (one after another) | The slower one wins |

**Two rules:**

1. **Nested loops multiply.** Two nested loops bounded by `n` give `O(n²)`. Three give `O(n³)`. And so on.
2. **Sequential loops add — but the bigger one wins.** `O(n) + O(n²) = O(n²)`. The smaller term gets absorbed.

---

## §5. Simplification rules (Proposition 9) — quick reference

Drop everything except the leading term:

| Rule | Says | Example |
|:--|:--|:--|
| (1) Positive scaling preserves O | `f ∈ O(h)` ⟹ `r·f ∈ O(h)` for `r > 0` | `5x ∈ O(x)` ⟹ `5·(5x) = 25x ∈ O(x)` |
| (2) Constants are invisible | `O(r·f) = O(f)` for `r > 0` | `O(100n) = O(n)` |
| (3) Sums in same class stay in class | `f, g ∈ O(h)` ⟹ `f+g ∈ O(h)` | `n ∈ O(n²)` and `100 ∈ O(n²)` ⟹ `n + 100 ∈ O(n²)` |
| (4) Smaller term invisible | `g ∈ O(f)` ⟹ `O(f+g) = O(f)` | `O(n² + 5n + 7) = O(n²)` |

**The recipe for simplifying `O(...)`:**

1. Identify the *leading term* (highest-order).
2. Drop everything else (Rule 4).
3. Drop the constant on the leading term (Rule 2).

So `O(7x³ + 100x² + 50)` → leading is `7x³` → drop the `+ 100x² + 50` → drop the `7` → `O(x³)`.

---

## §6. Polynomial classes (Propositions 10, 11)

**Proposition 10:** for `m < m'`, `O(nᵐ) ⊊ O(nᵐ')`. **Strictly** smaller. The hierarchy is real.

**Proposition 11:** every polynomial of degree `m` is `Θ(nᵐ)`. So:

- `5x³ + 3x² − 7` is `Θ(x³)`.
- `100x − 50` is `Θ(x)`.
- `42` is `Θ(1)`.

The leading-term degree is the entire complexity class.

---

## §7. Logarithmic class (Proposition 12)

`O(1) ⊊ O(log n) ⊊ O(n)`. Both inclusions strict.

**Why log base doesn't matter:** `logᵦ x = (1/logₐ b) · logₐ x`. The factor `(1/logₐ b)` is a positive constant — invisible by Rule 2. So `O(log₂ n) = O(log₁₀ n) = O(ln n)`. Just write `O(log n)` and don't specify the base.

---

## §8. Big Ω and Θ — the mirrors

| | Big O | Big Ω | Big Θ |
|:--|:--|:--|:--|
| **Pronounce** | "big O of g" | "big Omega of g" | "big Theta of g" |
| **Says** | `f` grows ≤ `g` | `f` grows ≥ `g` | `f` grows = `g` |
| **Definition** | `\|f(x)\| ≤ c · g(x)` for `x ≥ k` | `f(x) ≥ c · \|g(x)\|` for `x ≥ k` (Ex 26) | `c·\|g\| ≤ f ≤ c'·\|g\|` for `x ≥ k` (Ex 28) |
| **Equivalently** | — | `g ∈ O(f)` | `f ∈ O(g)` AND `g ∈ O(f)` |
| **Use for** | upper bound | lower bound | tight bound |

**When to use which:**

- **`O`** — you've shown your algorithm is *no worse than* something. "My program is `O(n²)`."
- **`Ω`** — you've shown a *problem* is *no easier than* something. "Sorting is `Ω(n log n)` (lower bound across all algorithms)."
- **`Θ`** — your algorithm is *exactly* this rate. Both bounds match. "Mergesort is `Θ(n log n)`."

---

## §9. What to count

The chapter (§3.1.4) chooses to count two things:

| Counts? | Operation |
|:-:|:--|
| ✓ | Assignment `x := a` (the `:=` rule) |
| ✓ | Boolean condition check (`if-tt`, `if-ff`, `while-tt`, `while-ff` rules) |
| ✗ | The `;` administrative rule |
| ✗ | The `skip-;` administrative rule |

**Why exclude admin rules?** They're not work the program is doing — they're how the small-step semantics propagates intermediate results. Counting them is like counting parentheses as separate operations.

**Different problems use different counters.** Sorting → comparisons. Search → lookups. Matrix work → entry accesses. As long as the count is *representative*, the asymptotic class comes out the same.

---

## §10. Best, worst, average

| Case | When to use |
|:--|:--|
| **Best** | Almost never — too optimistic to be useful. |
| **Average** | When you have a probability distribution over inputs, and average behaviour matters. Hard to compute rigorously. |
| **Worst** | The default. Gives an upper-bound *guarantee*: "no matter what input, ≤ this many steps." |

---

## §11. The `O` / `Ω` / `Θ` proofs you'll use most

### To show `f ∈ O(g)`

**Goal:** find specific `c, k ∈ ℝ⁺` with `\|f(x)\| ≤ c · g(x)` for `x ≥ k`.

**Standard trick:** factor out the dominant term, bound the rest by a constant.

Example: show `3n² + 5n + 7 ∈ O(n²)`.
- For `n ≥ 1`: `3n² + 5n + 7 ≤ 3n² + 5n² + 7n² = 15n²`.
- So `c = 15, k = 1` works.

### To show `f ∉ O(g)`

**Goal:** show that for *any* `c`, there exists arbitrarily large `x` with `f(x) > c · g(x)`.

**Standard trick:** pick `x` based on `c` to break the bound.

Example: show `n² ∉ O(n)`.
- Suppose `c, k` exist with `n² ≤ c · n` for `n ≥ k`. Equivalently `n ≤ c`.
- Pick `n = max(c, k) + 1`. Then `n > c` — contradiction.

### To show `f ∈ Θ(g)`

Show `f ∈ O(g)` AND `f ∈ Ω(g)` separately. Done.

---

## §12. Properties of the relation (Exercises 21, 22, 27)

| Property | Holds? | Why / Counter-example |
|:--|:-:|:--|
| Reflexive (`f ∈ O(f)`) | ✓ | Take `c = 1, k = 0`. |
| Transitive (`f ∈ O(g), g ∈ O(h)` ⟹ `f ∈ O(h)`) | ✓ | Multiply the constants `c₁ · c₂`. |
| Symmetric | ✗ | `n ∈ O(n²)` but `n² ∉ O(n)`. |
| Antisymmetric | ✗ | `n` and `2n` are both `O` of each other but `n ≠ 2n`. |

So `O` is a **pre-order**, not a partial order.

`f ∼ g` defined by `O(f) = O(g)` IS an equivalence relation (reflexive + symmetric + transitive — Exercise 27).

---

## §13. Common pitfalls

1. **`O(2n) ≠ O(n²)`.** `O(2n) = O(n)` — the `2` is a constant, not an exponent.
2. **`O(log² n)` (logarithmic squared) is NOT `O(log n²)`.** The first is `(log n)²`; the second is `log(n²) = 2 log n = O(log n)`. Different classes.
3. **Nested vs sequential matters.** `for ... for ...` (nested) is `O(n²)`. `for ...; for ...` (sequential) is `O(n)`.
4. **The leading coefficient doesn't determine which class.** `0.0001 · n³` is still `O(n³)` — slower in practice for small `n`, but asymptotically cubic.
5. **`O(f)` is an upper bound, not a description.** Saying "this is `O(n²)`" doesn't claim it's *not* `O(n)`. Use `Θ` if you want to claim a tight bound.
6. **The base of the log is irrelevant in `O`.** `log₂ n`, `log₁₀ n`, and `ln n` are all `Θ(log n)`.

---

## §14. The two-line elevator pitch

> **A program's complexity** is a function from input-size to step-count.
> **`O(f)`** is the set of functions growing no faster than `f`, up to a constant factor and beyond some starting point. **The whole point** is to ignore exact constants and lower-order terms so we can compare *growth rates* — that's what matters when input sizes get big.

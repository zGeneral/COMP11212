# COMP11212 Appendices — Math + Big-Step Cheat Sheet

Symbols, definitions for math vocabulary, and the 5 big-step rules. Companion to the chapter cheatsheets.

---

## §1. Math symbols and pronunciation

### Set theory and functions

| Symbol | Name | Say it like | Meaning |
|:-:|:--|:--|:--|
| **`f : S → T`** | function arrow | "f from S to T" | Total function. Every input has exactly one output. |
| **`f : S ⇀ T`** | partial-function arrow | "f from S to T (partial)" / "half-arrow" | Partial function. Some inputs may have no output. |
| **`f ∘ g`** | composition | "f after g" / "f compose g" | `(f ∘ g)(s) = f(g(s))`. |
| **`id_S`** | identity on S | "id sub S" | The function `s ↦ s`. |
| **`dom(f)`** | domain of definition | "domain of f" | The inputs where f is defined. |
| **`Fun(S, T)`** | function space | "Fun S T" | Set of all functions S → T. |
| **`PFun(S, T)`** | partial function space | "P Fun S T" | Set of all partial functions S → T. |

### Relations

| Symbol | Say it like | Meaning |
|:-:|:--|:--|
| **`R : S → T`** | "R from S to T" | A relation: subset of S × T. |
| **`(s, s') ∈ R`** | "s, s prime in R" | s and s' are related. |
| **`R ; R'`** | "R semicolon R prime" / "relational composition" | `(s, s'') ∈ R; R'` iff `∃s', (s, s') ∈ R ∧ (s', s'') ∈ R'`. |
| **`R^n`** | "R to the n" | n-fold composition. R^0 = id; R^{n+1} = R^n ; R. |
| **`⇒*`** | "yields star" / "reflexive-transitive closure" | `⋃_{n ≥ 0} R^n`. The smallest reflexive + transitive relation containing R. |

### Cardinality

| Symbol | Say it like | Meaning |
|:-:|:--|:--|
| **`\|S\|`** | "size of S" / "cardinality of S" | Cardinality. |
| **`\|S\| ≤ \|T\|`** | "S has size at most T" | There's an injection from S to T. |
| **`ℵ₀`** | "aleph null" / "aleph zero" | Cardinality of countably-infinite sets. |
| **`2^ℵ₀`** | "two to the aleph null" | Cardinality of P(ℕ) ≅ Fun(ℕ, 𝔹) ≅ ℝ. |

### The big-step ⇓ symbol

| Symbol | Name | Say it like | Meaning |
|:-:|:--|:--|:--|
| **`⟨S, σ⟩ ⇓ σ'`** | big-step judgment | "S, σ falls to σ'" / "S, σ terminates with σ'" | Executing S in σ terminates with state σ'. |

---

## §2. Function properties

| Property | Symbol/condition | Say it like |
|:--|:--|:--|
| **Injective** | `f(s) = f(s') ⟹ s = s'` | "one-to-one" / "injective" |
| **Surjective** | `∀t ∈ T, ∃s ∈ S, f(s) = t` | "onto" / "surjective" |
| **Bijective** | both injective and surjective | "bijective" / "one-to-one correspondence" |
| **Inverse function** | `g : T → S` with `g ∘ f = id_S` and `f ∘ g = id_T` | "g is the inverse of f" |

**Theorem 32:** `f` has an inverse iff `f` is bijective.

---

## §3. Relation properties

| Property | Definition |
|:--|:--|
| **Reflexive** | `∀s, (s, s) ∈ R` |
| **Symmetric** | `(s, s') ∈ R ⟹ (s', s) ∈ R` |
| **Antisymmetric** | `(s, s') ∈ R ∧ (s', s) ∈ R ⟹ s = s'` |
| **Transitive** | `(s, s') ∈ R ∧ (s', s'') ∈ R ⟹ (s, s'') ∈ R` |

**Closures:**
- *Reflexive closure*: `R ∪ id_S`.
- *Transitive closure*: smallest transitive relation containing R = `⋃ R^n` for n ≥ 1.
- *Reflexive-transitive closure*: `⋃ R^n` for n ≥ 0. This is the `⇒*` we use everywhere.

---

## §4. Countability

A set S is:

- **Finite** — has a finite number of elements. (Always countable.)
- **Countable** — there's an injection S → ℕ.
- **Countably infinite** — countable AND infinite. Cardinality ℵ₀.
- **Uncountable** — no injection S → ℕ exists.

| Countably infinite (size ℵ₀) | Uncountable (size 2^ℵ₀) |
|:--|:--|
| ℕ, ℤ, ℚ | ℝ, ℂ |
| Finite subsets of ℕ | All subsets of ℕ (P(ℕ)) |
| Strings over a finite alphabet | Functions ℕ → 𝔹 |
| All programs in any reasonable language | Functions ℕ → ℕ |

**Useful tool:** Cantor's diagonal argument shows that `Fun(ℕ, X)` is uncountable whenever `|X| ≥ 2`.

---

## §5. The 5 big-step rules

### Rule 1 — Skip

$$\langle \textbf{skip}, \sigma\rangle \Downarrow \sigma$$

### Rule 2 — Assignment

$$\langle x := a, \sigma\rangle \Downarrow \sigma[x \mapsto \mathcal{A}(a, \sigma)]$$

### Rule 3 — Composition

$$\dfrac{\langle S, \sigma\rangle \Downarrow \sigma' \qquad \langle S', \sigma'\rangle \Downarrow \sigma''}{\langle S; S', \sigma\rangle \Downarrow \sigma''}$$

### Rule 4 — Conditional (two cases)

$$\dfrac{\langle S, \sigma\rangle \Downarrow \sigma'}{\langle \textbf{if } b \textbf{ then } S \textbf{ else } S', \sigma\rangle \Downarrow \sigma'} \quad \mathcal{B}(b, \sigma) = \mathbf{tt}$$

$$\dfrac{\langle S', \sigma\rangle \Downarrow \sigma''}{\langle \textbf{if } b \textbf{ then } S \textbf{ else } S', \sigma\rangle \Downarrow \sigma''} \quad \mathcal{B}(b, \sigma) = \mathbf{ff}$$

### Rule 5 — While (two cases)

$$\dfrac{\langle S, \sigma\rangle \Downarrow \sigma' \qquad \langle \textbf{while } b \textbf{ do } S, \sigma'\rangle \Downarrow \sigma''}{\langle \textbf{while } b \textbf{ do } S, \sigma\rangle \Downarrow \sigma''} \quad \mathcal{B}(b, \sigma) = \mathbf{tt}$$

$$\langle \textbf{while } b \textbf{ do } S, \sigma\rangle \Downarrow \sigma \quad \mathcal{B}(b, \sigma) = \mathbf{ff}$$

---

## §6. Big-step vs small-step — at a glance

| Aspect | Small-step (⇒, Ch 2) | Big-step (⇓, App B) |
|:--|:--|:--|
| What's tracked | Each individual transition | Just the final state |
| Reasoning style | Forward, step-by-step | Recursive (works "backwards" through loops) |
| While loops | Unfold rule (`while-tt`) → body; loop | Recurse on same loop from post-body state |
| Step counts | Available directly | Lost — only ⇓ gives final state |
| Termination | Trace ends at ⟨skip, σ⟩ | No σ' satisfies ⇓ |
| Which is easier for proofs | Determinism, complexity | Final-state correctness, big invariants |
| Equivalence | `⟨S, σ⟩ ⇒* ⟨skip, σ'⟩` ⟺ `⟨S, σ⟩ ⇓ σ'` (Ex 67) |

---

## §7. Proof patterns

### Big-step termination via structural induction (Ex 58)

To show that all loop-free programs terminate (assignment, skip, if, ;):

```
Base cases:
  - skip:  ⟨skip, σ⟩ ⇓ σ.    (Always works.)
  - x:=a:  ⟨x:=a, σ⟩ ⇓ σ[x↦A(a,σ)].   (Always works.)

Inductive cases:
  - S₁; S₂:  By IH, both terminate. Apply ; rule.
  - if b:   By IH, the chosen branch terminates. Apply if rule.
  - while:  EXCLUDED by hypothesis.
```

### Big-step determinism (Ex 65)

By structural induction on S, each rule produces a unique σ'.

### Big-step ⟺ small-step (Ex 67)

Forward (⇓ → ⇒*): structural induction on big-step derivation.  
Reverse (⇒* → ⇓): induction on length of small-step trace.

Both work; both are tedious.

---

## §8. Common pitfalls

1. **Confusing ⇓ with ⇒.** ⇓ is BIG-STEP (one judgment per terminating execution). ⇒ is SMALL-STEP (one per transition). Distinct symbols, distinct judgments.

2. **Big-step claims about non-terminating programs.** None — ⇓ has no derivation for non-terminating programs. There's no "diverges" judgment in big-step.

3. **The big-step `;` rule.** Both premises must hold — neither program can run "in parallel" with the other. The post-state of the first IS the pre-state of the second.

4. **The big-step `while-tt` rule.** Requires a derivation of the SAME loop from the post-body state. This is recursive — proofs can be long for high-iteration loops.

5. **Confusing dom(f) and the source/target sets.** `dom(f) ⊆ S` for partial f; not all of S necessarily.

6. **Counting transitivity wrong for `⇒*`.** The reflexive-transitive closure includes 0-step relations: `s ⇒* s` always. Don't forget the reflexive part.

---

## §9. The two-line elevator pitch

> **Appendix A** is the math vocabulary the chapters use — functions, partial functions, relations, countability — mostly recap from COMP11120.
> **Appendix B** is the *big-step* operational semantics: a different way to talk about program execution that goes straight from ⟨S, σ⟩ to the final ⟨σ'⟩, skipping all the intermediate steps. Useful for proofs about *what programs compute*, complementing chapter 2's small-step view.

# COMP11212 Chapter 5 — Computability Cheat Sheet

Symbols, definitions, the Halting Problem proof skeleton, and the closure properties of decidable / semidecidable predicates. Companion to the chapter 1–4 cheatsheets.

---

## §1. Symbols — what to say out loud

### Computability notation

| Symbol | Name | Say it like | What it means |
|:-:|:--|:--|:--|
| **`f : ℕ → ℕ`** | total function | "f from N to N" | Every input has exactly one output. |
| **`f : ℕ ⇀ ℕ`** | partial function | "f partially from N to N" / "f from N to N partial" | Some inputs may be undefined. The half-arrow signals partial. |
| **`χ_P`** | characteristic function | "chi sub P" / "chi-of-P" | `χ_P(x) = tt if P(x), else ff`. Decidable predicate ⟺ χ_P computable. |
| **`⟦S⟧`** | semantic brackets / partial function computed by S | "the semantics of S" / "the function S computes" | The partial function `n ↦ k` such that S deterministically produces k from input n. |
| **`η_i`** | program-with-index-i's function | "eta sub i" | `η_i = ⟦S_i⟧` where `S_i` is the program with index i. |
| **`ζ`** | universal partial function | "zeta" | `ζ(i, j) = η_i(j)`. Single function that captures all computable partial functions. |
| **`U`** | universal program | "universal U" | The single program that computes ζ. |
| **`φ_S`** | program-encoding bijection | "phi sub S" / "phi-of-S" | Bijection between While programs and ℕ. |
| **`φ`** | pair-encoding bijection | "phi" | Bijection between ℕ × ℕ and ℕ (Cantor pairing). |
| **`β, β'`** | integer-encoding bijections | "beta", "beta prime" | Bijections between ℤ and ℕ. |

### Cardinality and other meta-language symbols

| Symbol | Say it like | What it means |
|:-:|:--|:--|
| **`ℵ₀`** | "aleph null" / "aleph zero" | The cardinality of countably infinite sets — same size as ℕ. |
| **`2^ℵ₀`** | "two to the aleph null" / "the cardinality of the continuum" | The cardinality of the power set of ℕ — same size as ℝ. **Strictly bigger** than ℵ₀. |
| **`Fun(S, T)`** | "the function space" / "S to T" | Set of all functions from S to T. `\|Fun(ℕ, ℕ)\| = 2^ℵ₀`. |
| **`PFun(S, T)`** | "the partial-function space" | Set of all partial functions from S to T. |
| **`⊨`** | "models" / "satisfies" | Used in Hoare-logic context: σ ⊨ P means state σ satisfies predicate P. |
| **`⇒*`** | "reduces to in many steps" | Reflexive-transitive closure of small-step (from chapter 2). |

---

## §2. The four levels of "answerable"

A predicate `P` on ℕ falls into exactly one of:

| Level | Definition | Example |
|:--|:--|:--|
| **Computable / decidable** | χ_P is computable; decision procedure always terminates | Primality, evenness, "is sum of triangular numbers" |
| **Semidecidable** | Partial χ_P is computable; semi-decider terminates iff P holds | Halting, first-order-logic validity |
| **Co-semidecidable** | ¬P is semidecidable | "Program does NOT halt" |
| **Neither** (truly undecidable) | Neither P nor ¬P is semidecidable | "Diophantine equation has solution" (Hilbert's 10th — actually undecidable, but is semi-decidable since you can search) |

**Hierarchy:** decidable ⊊ (semidecidable ∩ co-semidecidable) = decidable ⊊ semidecidable ⊊ all. Each containment strict.

---

## §3. Computability via Hoare triples

### Total function `f : ℕ → ℕ` (Definition 14)

$$f \text{ computable} \iff \exists\, S \text{ While program}.\ \{n = \bar n \in \mathbb{N}\}\ S\ \{\Downarrow x = f(\bar n)\}$$

### Partial function `f : ℕ ⇀ ℕ` (Definition 15)

$$f \text{ computable} \iff \exists\, S.\ \{n = \bar n \in \mathbb{N} \,\land\, f(\bar n) \text{ defined}\}\ S\ \{\Downarrow x = f(\bar n)\}$$

### Generalized: `f : S ⇀ T` (Definition 16)

Use injections `γ : ℕ → S` and `δ : T → ℕ`:

$$f \text{ computable} \iff \delta \circ f \circ \gamma : \mathbb{N} \rightharpoonup \mathbb{N} \text{ computable}$$

**Practical reading:** if you can encode S and T as natural numbers, computability reduces to ℕ ⇀ ℕ.

---

## §4. The 6 (or 7) building blocks of decidability proofs

Once you have a decidable predicate, you can build more:

| Construction | If P and Q are decidable, ... |
|:--|:--|
| **¬P** | ... is decidable. (Build T = S; if x = 0 then x := 1 else x := 0.) |
| **P ∧ Q** | ... is decidable. (Build T = S_P; if x = 1 then S_Q else skip.) |
| **P ∨ Q** | ... is decidable. (Build T = S_P; if x = 1 then skip else S_Q.) |
| **P → Q** | ... is decidable. (Equivalent to ¬P ∨ Q.) |
| **Bounded ∀** (`∀i < n. P(i)`) | ... is decidable. (Loop i = 0..n-1 running S_P, AND the results.) |
| **Bounded ∃** (`∃i < n. P(i)`) | ... is decidable. (Same loop but OR.) |

**For semidecidability:**

| Construction | If P, Q semidecidable... |
|:--|:--|
| **¬P** | ... NOT necessarily semidecidable. Counter-example: ¬Halting is *co-semidecidable* but not semi-decidable. |
| **P ∧ Q** | ... is semidecidable. (Run S_P then S_Q sequentially; both must halt.) |
| **P ∨ Q** | ... is semidecidable. (Dovetail: interleave steps of S_P and S_Q.) |
| **P → Q** | ... NOT necessarily semidecidable. (Equivalent to ¬P ∨ Q; the ¬P part can break it.) |

---

## §5. The Halting Problem proof skeleton

If you're asked to prove the Halting Problem on the exam, here's the template:

```
ASSUME (for contradiction) that H exists with:
  {m = m̄ ∈ ℕ ∧ n = n̄ ∈ ℕ} H {⇓ (P → x = 1) ∧ (¬P → x = 0)}
where P = "S_m̄ halts on input n̄".

STEP 1 — restrict H to the diagonal.
  Build H' = (n := m; H).
  Spec: {m = m̄} H' {⇓ (P' → x = 1) ∧ (¬P' → x = 0)}
  where P' = "S_m̄ halts on input m̄" (self-application).

STEP 2 — invert via H''.
  Build H'' = H'; if x = 1 then (while tt do skip) else x := 1.
  Reading: H'' diverges if H' says "halts," terminates with x = 1 if H' says "doesn't halt."

STEP 3 — Hoare-derive the contradiction.
  By construction (partial correctness only):
    {m = m̄} H'' {¬P' → x = 1}.

STEP 4 — feed H'' its own index, get a contradiction.
  Set m̄ = φ_S(H''). Then P' = "H'' halts on its own index."
  - If P' (H'' halts on m̄): by step 2, H' returned 1 ⟹ infinite loop ⟹ H'' doesn't halt. Contradiction.
  - If ¬P' (H'' doesn't halt on m̄): by step 7 we have ¬P' → x = 1, so if H'' terminates, it halts with x = 1. By step 2's else-branch, H'' DOES terminate. Contradiction.

CONTRADICTION ⟹ H cannot exist. ∎
```

**Memorise the four steps** and you can reproduce the proof from scratch.

---

## §6. The universal program

| Concept | What it is |
|:--|:--|
| **Universal partial function** ζ | ζ(i, j) = η_i(j). Captures ALL computable partials in one function. |
| **Universal program** U | A single While program computing ζ. Decodes input program from index, walks AST, simulates step-by-step. |
| **Parameterization Theorem** (Theorem 23) | Given computable f : ℕ × ℕ ⇀ ℕ, there's total computable h : ℕ → ℕ with f(i, j) = η_{h(i)}(j). |
| **s-m-n theorem** | Generalises Parameterization to any number of inputs. |

**Key idea:** generating program *text* from data is itself a computable operation. We can produce indices on demand.

---

## §7. The Church-Turing thesis

| Statement | Has it been proven? |
|:--|:-:|
| All sufficiently powerful models compute the same set of partial functions | **Empirically supported, not a theorem.** |
| Turing machines, λ-calculus, While, register machines compute the same set | ✓ (provable equivalences between specific models) |
| Quantum computers compute strictly MORE | ✗ (only faster on some problems, same set) |
| All physical computational devices compute exactly Turing-machine-computable | Almost certainly yes (no counter-example known) |

**Why it's a thesis, not a theorem:** "effectively computable" is an intuition, not a formal concept. We can't prove that two intuitive notions coincide; we can only prove that two formal notions do.

---

## §8. Things that are NOT quite obvious

1. **\"Most\" functions ℕ → ℕ are uncomputable.** The set of computable functions has cardinality ℵ₀; Fun(ℕ, ℕ) has cardinality 2^ℵ₀. Almost all functions can't be computed.

2. **The Halting Problem isn't "hard." It's *impossible*.** No algorithm of any kind, in any model, can solve it.

3. **You CAN run programs and see if they stop.** Halting is semidecidable. The interesting question is whether you can ALWAYS get an answer — and you can't.

4. **Decidable ⊊ Semidecidable.** A decidable predicate has more guarantees, so the inclusion is strict in one direction. The reverse inclusion fails: some semidecidable predicates (like halting) aren't decidable.

5. **The universal program U exists for While, but isn't trivial to write.** It would be a huge program — but it's finite. Writing one in a real programming language is straightforward (we already have one — `while_lang.py` + the `run` function). The While version requires the encoding from §6.3.

6. **\"Effectively computable\" might mean different things to different people.** That's OK — Church-Turing says all reasonable formalisations agree. The intuition is robust even if the words aren't.

---

## §9. Common pitfalls

1. **Confusing \"undecidable\" with \"hard.\"** Undecidable = no algorithm exists, ever. Hard = takes a long time but is solvable.

2. **Assuming negation preserves semidecidability.** It doesn't. Halting is semidecidable; non-halting is *co*-semidecidable, not semidecidable.

3. **Thinking the cardinality argument exhibits an uncomputable function.** It doesn't — it just proves existence. The Halting Problem (§5.4) is the explicit example.

4. **Treating ⟦S⟧ as a function of all input variables.** It's only a function of `n`. If S's output depends on other variables, ⟦S⟧ is undefined for *every* input, not partially defined.

5. **Treating Church-Turing as a theorem.** It isn't. The mathematical equivalences between specific models are theorems; the bridge to the intuitive concept is a thesis.

---

## §10. The two-line elevator pitch

> **Computability theory** asks "what can be computed at all?" — the answer is "less than you'd think."
> Most functions ℕ → ℕ have no algorithm. The Halting Problem is the classical example: no program can decide whether arbitrary programs halt on arbitrary inputs. But anything that *can* be computed in any reasonable model can be computed in any other — that's the Church-Turing thesis.

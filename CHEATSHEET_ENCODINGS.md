# COMP11212 Chapter 6 — Encodings Cheat Sheet

Symbols, bijections (β, φ, ψ, φ_A, φ_B, φ_S), and decoding recipes. Companion to the chapter 1–5 cheatsheets.

---

## §1. Symbols — what to say out loud

### The bijections

| Symbol | Name | Say it like | Type |
|:-:|:--|:--|:--|
| **β** | beta | "beta" | ℤ → ℕ (integer encoder) |
| **β'** | beta-prime | "beta prime" / "beta inverse" | ℕ → ℤ (integer decoder) |
| **φ** | phi | "phi" / "the pairing function" | ℕ × ℕ → ℕ (pair encoder) |
| **φ'** | phi-prime | "phi prime" / "phi inverse" | ℕ → ℕ × ℕ (pair decoder) |
| **ψ** | psi | "psi" / "the list encoding" | List(ℕ) → ℕ |
| **φ_V** | phi sub V | "phi-sub-V" / "the variable encoder" | Vars → ℕ |
| **φ_A** | phi sub A | "phi-sub-A" / "the AExp encoder" | AExp → ℕ |
| **φ_B** | phi sub B | "phi-sub-B" / "the BExp encoder" | BExp → ℕ |
| **φ_S** | phi sub S | "phi-sub-S" / "the program encoder" | Stmt → ℕ |

### Cardinality

| Symbol | Say it like | What it means |
|:-:|:--|:--|
| **ℵ₀** | "aleph null" / "aleph zero" | Cardinality of ℕ. The countable infinity. |
| **2^ℵ₀** | "two to the aleph null" / "the cardinality of the continuum" | Cardinality of P(ℕ) ≅ Fun(ℕ, 𝔹) ≅ ℝ. |
| **`Fun(S, T)`** | "function space S to T" | Set of all functions S → T. |
| **`PFun(S, T)`** | "partial function space" | Set of partial functions. |
| **`P(S)`** | "power set of S" | Set of all subsets of S. |

---

## §2. The bijections, in formula form

### β: ℤ → ℕ

$$\beta(x) = \begin{cases} 2x & x \ge 0 \\ -2x - 1 & x < 0\end{cases}$$

**Inverse:**

$$\beta'(n) = \begin{cases} n/2 & n \text{ even} \\ -(n+1)/2 & n \text{ odd}\end{cases}$$

**Pattern:** zigzag — `0 ↔ 0, -1 ↔ 1, 1 ↔ 2, -2 ↔ 3, 2 ↔ 4, ...`

### φ: ℕ × ℕ → ℕ

$$\varphi(m, n) = 2^m (2n + 1) - 1$$

**Decoding `k`:**
1. `s = k + 1`
2. `m` = largest power of 2 dividing `s`
3. `2n + 1 = s / 2^m`, so `n = (s / 2^m - 1) / 2`

### Tuples (k-tuples)

$$\text{encode}(x_1, x_2, \ldots, x_k) = \varphi(x_1, \varphi(x_2, \ldots, x_k))$$

Right-fold. Decode by repeated `φ'`.

### ψ: lists → ℕ

$$\psi([\,]) = 0, \qquad \psi(n :: l) = \varphi(n, \psi(l)) + 1$$

The `+1` distinguishes the empty list (encoded `0`) from `φ(0, 0) = 0`.

### φ_V: Vars → ℕ

By convention: `φ_V(x_i) = i`.

### φ_A: AExp → ℕ

| AExp form | Encoding |
|:--|:--|
| numeral `n` | `5 · β(n)` (residue 0 mod 5) |
| variable `x` | `1 + 5 · φ_V(x)` (residue 1 mod 5) |
| `a + a'` | `2 + 5 · φ(φ_A a, φ_A a')` (residue 2 mod 5) |
| `a − a'` | `3 + 5 · φ(φ_A a, φ_A a')` (residue 3 mod 5) |
| `a × a'` | `4 + 5 · φ(φ_A a, φ_A a')` (residue 4 mod 5) |

### φ_B: BExp → ℕ

| BExp form | Encoding |
|:--|:--|
| `ff` | `0` |
| `tt` | `1` |
| `a = a'` | `2 + 4 · φ(φ_A a, φ_A a')` |
| `a ≤ a'` | `3 + 4 · φ(φ_A a, φ_A a')` |
| `¬b` | `4 + 4 · φ_B b` |
| `b ∧ b'` | `5 + 4 · φ(φ_B b, φ_B b')` |

### φ_S: Stmt → ℕ

| Stmt form | Encoding |
|:--|:--|
| `skip` | `0` |
| `x := a` | `1 + 4 · φ(φ_V x, φ_A a)` |
| `S ; S'` | `2 + 4 · φ(φ_S S, φ_S S')` |
| `if b then S else S'` | `3 + 4 · φ(φ_B b, φ(φ_S S, φ_S S'))` |
| `while b do S` | `4 + 4 · φ(φ_B b, φ_S S)` |

---

## §3. Decoding recipes (work backwards from `n`)

### Decoding an AExp from `n`

```
r = n mod 5
q = n // 5

if r == 0:    return Num(β'(q))             // numeral
if r == 1:    return Var(name with index q) // variable
if r in 2..4: 
    (a_idx, b_idx) = φ'(q)
    left  = decode_aexp(a_idx)
    right = decode_aexp(b_idx)
    op = {2: Add, 3: Sub, 4: Mul}[r]
    return op(left, right)
```

### Decoding a BExp from `n`

```
if n == 0: return BFalse
if n == 1: return BTrue
r = n mod 4
q = n // 4

if r == 2: 
    (a_idx, b_idx) = φ'(q)
    return Eq(decode_aexp(a_idx), decode_aexp(b_idx))
if r == 3: 
    (a_idx, b_idx) = φ'(q)
    return Le(decode_aexp(a_idx), decode_aexp(b_idx))
if r == 0:                  // ¬, since n = 4 + 4·k for k = q-1
    return Not(decode_bexp(q - 1))
if r == 1:                  // ∧, since n = 5 + 4·k for k = q-1
    (a_idx, b_idx) = φ'(q - 1)
    return And(decode_bexp(a_idx), decode_bexp(b_idx))
```

### Decoding a Stmt from `n`

```
if n == 0: return Skip
r = n mod 4
q = n // 4

if r == 1:
    (v_idx, a_idx) = φ'(q)
    return Assign(x_{v_idx}, decode_aexp(a_idx))
if r == 2:
    (s_idx, s'_idx) = φ'(q)
    return Seq(decode_stmt(s_idx), decode_stmt(s'_idx))
if r == 3:
    (b_idx, rest) = φ'(q)
    (s_idx, s'_idx) = φ'(rest)
    return If(decode_bexp(b_idx), decode_stmt(s_idx), decode_stmt(s'_idx))
if r == 0:                  // while, since n = 4 + 4·k for k = q-1
    (b_idx, s_idx) = φ'(q - 1)
    return While(decode_bexp(b_idx), decode_stmt(s_idx))
```

---

## §4. Quick decoding examples

**Decode 13 as a pair.**

13 + 1 = 14 = 2¹ × 7. So m = 1, 2n+1 = 7, n = 3. Pair: `(1, 3)`. ✓

**Decode 40815 as a pair.**

40815 + 1 = 40816 = 2⁴ × 2551. m = 4, n = (2551 − 1)/2 = 1275. Pair: `(4, 1275)`.

**Decode 5 as a Stmt.**

5 mod 4 = 1, so this is an assignment. q = 1. φ'(1) = (1, 0). So `Assign(x_1, decode_aexp(0))`. `decode_aexp(0)`: 0 mod 5 = 0, so numeral with `β'(0) = 0`. Result: `x_1 := 0`.

**Encoding `skip; x_1 := 0`.**

φ_S(skip) = 0. φ_S(x_1 := 0) = 1 + 4·φ(1, 0) = 1 + 4·1 = 5. φ_S(skip; x_1 := 0) = 2 + 4·φ(0, 5) = 2 + 4·10 = **42**.

---

## §5. Cantor diagonal — proof template

To show `Fun(S, T)` is uncountable (where `S` is countably infinite and `|T| ≥ 2`):

1. **Suppose for contradiction** there's an enumeration `f₀, f₁, f₂, …` of all functions S → T.
2. **List the elements of S** as `s₀, s₁, s₂, …`.
3. **Construct a diagonal-flipping g** : for each `i`, choose `g(s_i) ∈ T` with `g(s_i) ≠ f_i(s_i)`. (Possible because `|T| ≥ 2`.)
4. **g is not on the list**: for any `i`, `g(s_i) ≠ f_i(s_i)`, so `g ≠ f_i`.
5. **Contradiction.** No enumeration exists. ∎

**Specialised to `Fun(ℕ, ℕ)`:** `g(n) = f_n(n) + 1`.
**Specialised to `Fun(ℕ, 𝔹)`:** `g(n) = ¬f_n(n)`.

---

## §6. Common pitfalls

1. **Confusing β and β'.** β goes ℤ → ℕ; β' goes ℕ → ℤ. The chapter sometimes mentions β' where β was intended (e.g., the formula `φ_A(n) = 5 · β'(n)` in the chapter is most consistent if read as `5 · β(n)`).

2. **Forgetting `+1` in ψ for lists.** Without it, the empty list and `[0]` collide.

3. **Treating `φ_V(x_i) = i` and `φ_V(x_0) = 1` as compatible.** They're not. The chapter's Example 23 has an arithmetic inconsistency here; the formal definition is `φ_V(x_i) = i`, so `φ_V(x_0) = 0`.

4. **Expecting Gödel numbers to be small.** They're not. A simple while loop has a 1900-digit encoding. The encoding is correct but not practical — it's a theoretical existence proof.

5. **Mistaking encoding/decoding for compilation.** Decoding produces an AST you can re-execute; it doesn't "translate" between languages in any meaningful sense — it's just unpacking nested tuples.

---

## §7. The encoding stack — how chapters 5 and 6 connect

```
Real-world data type          chapter 5 needs ℕ → ℕ
        |                              |
        v                              v
  encode_X (chapter 6)  -->  computability arguments work on ℕ
        ^                              |
        |                              v
  decode_X (chapter 6)  <--  result encoded as ℕ
        |
        v
  Real-world data type
```

**Three places this matters in chapter 5:**

1. **Halting Problem proof.** Need to feed program H'' to itself — requires `φ_S(H'')`.
2. **Universal program U.** Decodes input `(i, j)` into `(S_i, j)`, then simulates.
3. **Parameterization Theorem.** Needs to compute the index of a synthesised program.

Without chapter 6's encodings, chapter 5 would be unprovable.

---

## §8. The two-line elevator pitch

> **Chapter 6 is plumbing.** It provides the bijections that turn programs and data structures into natural numbers, so the abstract "computability for ℕ → ℕ" notion of chapter 5 covers everything in practice.
> The diagonal proof of Theorem 25 + the encoding of While programs as ℕ together imply: most functions ℕ → ℕ are uncomputable. That's the punchline of chapter 5, made rigorous by chapter 6.

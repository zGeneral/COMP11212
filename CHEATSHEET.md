# COMP11212 Week 6 — Cheat Sheet

One page (well, a few) covering: every symbol with how to actually pronounce it, every concept with the Python that *is* that concept, the 6 small-step rules, and the phrases to use in exam answers.

---

## §1. Symbols — what to say out loud

When you read a symbol in the chapter, this is how it gets said in lectures, and how to say it in your own head while you read.

### Greek letters (used as state names)

| Symbol | Name | Say it like | What it usually means |
|:-:|:--|:--|:--|
| **σ** | sigma | "SIG-mah" | A state (function from variables to integers) |
| **τ** | tau | "TAU" (rhymes with "now") | Another state, often the *final* one |
| **ρ** | rho | "ROW" | Another state, often an intermediate one |
| **σ′** | sigma-prime | "sig-mah PRIME" | The state after one step from σ |

You'll see `σ`, `σ'`, `σ''` everywhere — they're all states, just different ones in a chain. The prime (`'`) doesn't mean "different kind of thing," it just means "the next one."

### Logic and math symbols

| Symbol | Say it like | What it means |
|:-:|:--|:--|
| **¬** | "not" | Logical negation. `¬b` = "not b". |
| **∧** | "and" | Logical conjunction. `b ∧ b'` = "b and b'". |
| **∨** | "or" | Logical disjunction. (Not in While; encode via De Morgan.) |
| **→** | "implies" | Logical implication. (Not in While; encode as `¬a ∨ b`.) |
| **≡** | "is equivalent to" | Logical equivalence — same truth table. |
| **≤** | "less than or equal to" | Inequality on integers. |
| **=** | "equals" (in BExp) | Equality test, returns a boolean. |
| **×** | "times" | Multiplication. |
| **∈** | "is in" / "is a member of" | Set membership. `n ∈ ℤ` = "n is in the integers". |
| **∀** | "for all" | Universal quantifier. (Used in proofs.) |
| **∃** | "there exists" | Existential quantifier. |
| **∎** | "Q-E-D" / "end of proof" | Marks the end of a proof. (Halmos symbol.) |
| **iff** | "if and only if" | Two-way implication. |

### Number sets

| Symbol | Say it like | What it means |
|:-:|:--|:--|
| **ℤ** | "the integers" / "Z" | All whole numbers, positive and negative. {…, −2, −1, 0, 1, 2, …} |
| **ℕ** | "the naturals" / "N" | Non-negative integers. {0, 1, 2, …}. (Some books exclude 0; Manchester includes it.) |
| **𝔹** | "the booleans" / "B" | {tt, ff} — the truth values. |

### State manipulation

| Symbol | Say it like | What it means |
|:-:|:--|:--|
| **σ(x)** | "sigma of x" | The value of variable x in state σ. |
| **σx** | "sigma x" | Same as σ(x) — chapter writes it both ways. |
| **σ[x ↦ n]** | "sigma with x maps to n" | Update — new state where x has value n, everything else like σ. |
| **σ[x ↦ n, y ↦ m]** | "sigma with x maps to n, y maps to m" | Multiple updates left-to-right. |
| **{x ↦ 1, y ↦ 2}** | "the state where x maps to 1 and y maps to 2" | Description of a state — only non-zero entries listed. |

### The two evaluators

| Symbol | Say it like | What it means |
|:-:|:--|:--|
| **𝒜** (script A) | "script A" / "the A function" / "A" | Evaluates an arithmetic expression in a state to an integer. |
| **ℬ** (script B) | "script B" / "the B function" / "B" | Evaluates a boolean expression in a state to a truth value. |
| **𝒩** (script N) | "script N" / "numeral interpretation" | Maps a numeral (string) to the integer it denotes. Often elided. |
| **𝒜⟦a⟧σ** | "script A of a, sigma" / "A semantic-brackets a, sigma" | A applied to expression a in state σ. |

In our notebooks we just write `A(a, sigma)` and `B(b, sigma)`. Same thing.

### Configurations and transitions

| Symbol | Say it like | What it means |
|:-:|:--|:--|
| **⟨S, σ⟩** | "S and sigma" / "configuration S sigma" / "angle-bracket S sigma" | A *configuration* — program S together with state σ. |
| **⇒** | "yields" / "steps to" / "reduces to" / "transitions to" | One small-step transition. |
| **⇒ⁿ** | "yields in n steps" / "reduces to in n steps" | Exactly n transitions. |
| **⇒*** | "yields eventually" / "reduces to" / "yields star" | Reflexive transitive closure — *some* number of steps (possibly zero). |
| **⟨skip, σ⟩** | "skip sigma" / "the skip configuration" | Terminal configuration — no rule applies. Means "done, in state σ". |

The full thing `⟨S, σ⟩ ⇒ ⟨S', σ'⟩` reads as: "S in state sigma yields S-prime in state sigma-prime."

### BNF grammar notation

| Symbol | Say it like | What it means |
|:-:|:--|:--|
| **`<aexp>`** | "a-exp" / "an arithmetic expression" / "a non-terminal" | A category — gets defined by the grammar. |
| **`::=`** | "is defined as" / "produces" / "rewrites to" | Defines a grammar rule. |
| **`\|`** (in BNF) | "or" | Separates alternatives in a rule. |
| **`<>`** | "angle brackets" — surround non-terminals | Visual delimiter only; not part of programs. |

### While statements

| Symbol | Say it like | What it means |
|:-:|:--|:--|
| **`:=`** | "becomes" / "gets" / "is assigned" / "assignment" | Variable assignment. **NOT "equals"** — that's `=`. |
| **`;`** | "then" / "semicolon" / "do then" | Sequential composition: do this, then that. |
| **`tt`** | "true" / "tee-tee" | The boolean true. |
| **`ff`** | "false" / "ef-ef" | The boolean false. |
| **`skip`** | "skip" | A program that does nothing. (Crucial as the *terminal* program.) |

---

## §2. Concepts ↔ Python — one row per idea

For every theoretical concept in the chapter, here's what it *is* in Python (specifically in `while_lang.py`):

| Concept | In the chapter | In Python (`while_lang.py`) |
|:--|:--|:--|
| **Variable** | `x ∈ Vars`, name | `Var(name='x')` — a string-named AST node |
| **Numeral** | `n ∈ Num` | `Num(value=5)` — an int wrapped in a class |
| **Arithmetic expression (AExp)** | `<aexp> ::= <num> \| <var> \| <aexp> + <aexp> \| ...` | Union type: `Num \| Var \| Add \| Sub \| Mul` |
| **Boolean expression (BExp)** | `<bexp> ::= ff \| tt \| ...` | Union: `BTrue \| BFalse \| Eq \| Le \| Not \| And` |
| **Statement (Stmt)** | `<stmt> ::= := \| skip \| ; \| if \| while` | Union: `Skip \| Assign \| Seq \| If \| While` |
| **State σ** | Function `σ: Vars → ℤ`, finitely many non-zero | `dict[str, int]` with `.get(name, 0)` for default-zero |
| **State update σ[x ↦ n]** | New state agreeing with σ except at x | `{**sigma, 'x': n}` — copy + set |
| **Multi-update σ[x ↦ n, y ↦ m]** | Apply updates left-to-right | `{**sigma, 'x': n, 'y': m}` (last write wins on duplicates) |
| **The 𝒜 evaluator** | Recursive function: AExp × St → ℤ | `def A(expr, sigma) -> int:` with `isinstance` cases |
| **The ℬ evaluator** | Recursive function: BExp × St → 𝔹 | `def B(expr, sigma) -> bool:` with `isinstance` cases |
| **Configuration ⟨S, σ⟩** | Pair of program + state | `Config(stmt=S, state=sigma)` dataclass |
| **Transition ⇒** | One step of the small-step semantics | `step(cfg) -> Transition \| None` |
| **Transition labelled with rule** | Applied rule (`:=`, `if-tt`, etc.) | `Transition.rule: str` field |
| **Terminal configuration** | `⟨skip, σ⟩` — no further rule applies | `step()` returns `None` when stmt is Skip |
| **n-step relation ⇒ⁿ** | Exactly n transitions | A list of n transitions from `step_iter` |
| **Reflexive-transitive closure ⇒*** | Some number of steps (≥ 0) | The full `step_iter(prog, sigma)` generator |
| **Termination** | `⟨S, σ⟩ ⇒* ⟨skip, σ'⟩` exists | `run(prog, sigma)` returns a dict |
| **Non-termination** | No such σ' exists | `run(...)` raises `StepBudgetExceeded` |
| **Operational semantics** | Rules defining how programs behave | `step()` IS the operational semantics |
| **Determinism** | At most one rule applies at each step | `step()` is a function (not a relation) |

---

## §3. The six small-step rules — at a glance

These are the rules the exam tests. One line each: formal → plain English → which Python branch in `step()`.

| Rule | Formal | Plain English | Python branch |
|:--|:--|:--|:--|
| **`:=`** | `⟨x := a, σ⟩ ⇒ ⟨skip, σ[x ↦ 𝒜 a σ]⟩` | "Assign: store the value, replace with skip." | `isinstance(s, Assign)` |
| **`skip-;`** | `⟨skip; T, σ⟩ ⇒ ⟨T, σ⟩` | "Drop a finished skip from the front of a `;`." | `isinstance(s, Seq) and isinstance(s.first, Skip)` |
| **`;` (general)** | `⟨S, σ⟩ ⇒ ⟨S', σ'⟩` implies `⟨S; T, σ⟩ ⇒ ⟨S'; T, σ'⟩` | "Step the left side, drag the right side along unchanged." | `isinstance(s, Seq)` (other case) — recursive `step` on `s.first` |
| **`if-tt`** | When `ℬ b σ = tt`: `⟨if b then S else (S'), σ⟩ ⇒ ⟨S, σ⟩` | "Condition true → take the then-branch." | `isinstance(s, If) and B(s.cond, sigma)` |
| **`if-ff`** | When `ℬ b σ = ff`: `⟨if b then S else (S'), σ⟩ ⇒ ⟨S', σ⟩` | "Condition false → take the else-branch." | `isinstance(s, If) and not B(s.cond, sigma)` |
| **`while-tt`** | When `ℬ b σ = tt`: `⟨while b do (S), σ⟩ ⇒ ⟨S; while b do (S), σ⟩` | "Condition true → unfold: body, then loop again." | `isinstance(s, While) and B(s.cond, sigma)` |
| **`while-ff`** | When `ℬ b σ = ff`: `⟨while b do (S), σ⟩ ⇒ ⟨skip, σ⟩` | "Condition false → become skip." | `isinstance(s, While) and not B(s.cond, sigma)` |

**Two big things to notice:**
1. **All rules except `:=` leave σ unchanged.** Only assignment changes state.
2. **Only `while-tt` makes the program text grow.** Every other rule shrinks it or keeps it the same. That's why programs without while-loops always terminate.

---

## §4. Common While ↔ ASCII conversions

When typing a program into our interpreter (or onto a keyboard) you can't type `≤`. Here's the map:

| Chapter writes | Type instead | What it means |
|:-:|:-:|:--|
| `≤` | `<=` | less-than-or-equal |
| `¬` | `!` | not |
| `∧` | `&` | and |
| `×` | `*` | multiplication |
| `tt` | `tt` | true (same) |
| `ff` | `ff` | false (same) |
| `:=` | `:=` | assignment (same) |
| `=` | `=` | equality test (same) |

**No native `<`, `>`, `≥`, `∨`, `→`.** Workarounds:

| Want | Encode as |
|:--|:--|
| `a < b` | `a <= b & !(a = b)` |
| `a > b` | `b <= a & !(a = b)` |
| `a ≥ b` | `b <= a` |
| `a ∨ b` | `!((!a) & (!b))` (De Morgan) |
| `a → b` | `!(a & !b)` |

---

## §5. Properties and propositions to remember

These come up in exam-style questions. Memorize the *names* and *what they say* — proofs are by case-analysis on rules.

| Name | What it says | Why it matters |
|:--|:--|:--|
| **Determinism** (Ex 18) | If `⟨S, σ⟩ ⇒ ⟨S', ρ⟩` and `⟨S, σ⟩ ⇒ ⟨S', τ⟩` then ρ = τ. | While is single-threaded — each (S, σ) has at most one next step. |
| **State preservation** (Ex 17) | If S doesn't mention x and `⟨S, σ⟩ ⇒ ⟨S', σ'⟩`, then σ(x) = σ'(x). | Variables you don't touch stay put. |
| **Proposition 2** (decomposition) | `⟨S; T, σ⟩ ⇒ⁿ ⟨U, τ⟩` decomposes as either "still in S" or "done with S, working on T". | Sequential composition has a sharp boundary — S finishes *before* T starts. |
| **Proposition 3** (associativity of `;`) | `⟨(S; T); U, σ⟩ ⇒* ⟨skip, τ⟩` iff `⟨S; (T; U), σ⟩ ⇒* ⟨skip, τ⟩`. | The grammar's ambiguity for chained `;` is harmless. |

**`;` is associative but NOT commutative** — `S; T` and `T; S` do different things. This is the difference between math `+` (both) and While `;` (associative only).

---

## §6. Exam-style phrasing — how to say things on paper

When asked to "compute the transitions" or "argue why...", these phrases come up:

| What you want to say | Use this phrasing |
|:--|:--|
| "the assignment rule fires" | "by the := rule" |
| "the while-true case" | "by the while-tt rule" / "since `ℬ b σ = tt`, the while-tt rule applies" |
| "the program reaches a final state" | "the program terminates in state σ'" or "`⟨S, σ⟩ ⇒* ⟨skip, σ'⟩`" |
| "the program runs forever" | "the program does not terminate" or "no σ' satisfies `⟨S, σ⟩ ⇒* ⟨skip, σ'⟩`" |
| "I'm folding multiple `:=` and `;` rules into one super-step" | "`⇒ⁿ`" (with n counted) — chapter does this in Example 7 |
| "the body of the while loop" | abbreviate as `B`, with "where B is …" stated once |
| "the whole while statement" | abbreviate as `L` or `L₁`, define on first appearance |
| starting a structural induction proof | "By induction on the structure of S. We case-split on which rule applies." |
| ending a proof | "∎" or "QED" |

---

## §7. The three views of a trace, in one table

Our interpreter renders the same execution three ways. Here's when to use which:

| View | Looks like | When to use |
|:-:|:--|:--|
| `view='formal'` | `⟨S, σ⟩ ⇒ ⟨S', σ'⟩    [rule]` per line, with `L` abbreviations for repeated whiles | Studying the rules; matching what the chapter shows in Example 7 |
| `view='table'` | One row per transition, columns = changing variables | When asked to "track the execution" — Example 8 / Example 11 style |
| `view='dict'` | Just the final state as a Python dict | When you only care about the answer, e.g. asserting correctness |

---

## §8. Quick decision tree — "is this program correct?"

If asked: *"What does this program compute?"* or *"Will it terminate?"*

1. **Identify the inputs and outputs.** Which variables hold the input? Which hold the output? (The chapter says explicitly. If not, look at what's read first vs. assigned last.)
2. **Walk the loop conditions.** What invariant does each loop maintain? When does the condition first become false?
3. **Check termination.**
   - No loops → always terminates.
   - Bounded loops (e.g. counter increases towards a fixed bound) → terminates.
   - Unbounded loop search (e.g. Example 2's quadratic search) → might not terminate; need to argue from the *arithmetic* whether the exit condition is ever satisfied.
4. **For divisibility / non-existence arguments** (Exercise 14b(ii)): show all values reachable share a common factor that the target doesn't.

---

## §9. Conventions that aren't formal but matter for readability

The chapter uses several conventions that aren't *required* by the formal rules but make traces easier to read:

- **`⇒ⁿ` super-steps** — collapse a run of `:=`, `;`, and `skip-;` rules into one labelled super-step.
- **`B`, `L` abbreviations** — give names to the body of a loop (`B`) or the whole loop (`L`) on first appearance.
- **Indentation instead of brackets** — when writing programs over multiple lines, indentation replaces `( )` around if/while bodies.
- **State descriptions only show non-zero entries** — `{x ↦ 1}` means "x is 1, everything else is 0".

You're allowed to use these in exam answers. Read Example 7 carefully — that's the gold standard for what the marker expects to see.

---

## §10. Things that are NOT in While (so you don't waste time looking)

| Thing | Workaround |
|:--|:--|
| Division `/` | Subtraction loop (see Example 1) |
| Modulo `%` | Subtraction loop |
| Exponentiation `^` | Multiplication loop (see Section 1.7) |
| Strict less-than `<` | `a <= b & !(a = b)` |
| Greater-than `>`, `≥` | Swap operands of `<=` |
| OR `∨` | `!((!a) & (!b))` |
| Implication `→` | `!(a & !b)` |
| Boolean variables | All variables are integers; encode booleans as 0/1 |
| Floating-point | Not in the language; integers only |
| Strings, lists, arrays | Not in the language; integers only |
| Function definitions | Not in the language; everything is inline |
| Recursion | No functions, but `while` can simulate any recursion |

---

## §11. The two bits to memorize cold

Everything in the chapter ultimately boils down to two memorized things. If you only have 30 seconds before the exam, learn these:

### (a) The 6 inference rules

```
⟨x := a, σ⟩          ⇒ ⟨skip, σ[x ↦ 𝒜 a σ]⟩

⟨skip; T, σ⟩         ⇒ ⟨T, σ⟩

⟨S, σ⟩ ⇒ ⟨S', σ'⟩  implies  ⟨S; T, σ⟩ ⇒ ⟨S'; T, σ'⟩

⟨if b then S else S', σ⟩  ⇒ ⟨S, σ⟩  if 𝓑 b σ = tt
                          ⇒ ⟨S', σ⟩  otherwise

⟨while b do S, σ⟩    ⇒ ⟨S; while b do S, σ⟩  if 𝓑 b σ = tt
                     ⇒ ⟨skip, σ⟩  otherwise
```

### (b) The state update rule

$$(\sigma[x \mapsto n])(y) = \begin{cases} n & y = x \\ \sigma(y) & \text{otherwise} \end{cases}$$

In words: "the new state is just like σ, except on x it gives n."

Everything else is mechanics on top of these.

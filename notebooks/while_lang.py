"""
while_lang.py — an interpreter for the While language from COMP11212.

This module IS the executable definition of the operational semantics.
The trace printer's output renders the formal small-step semantics
(⟨S, σ⟩ ⇒ ⟨S', σ'⟩) — the Python is the implementation, the formal
notation is the rendering.

ASCII input syntax (because typing ≤, ¬, ∧ is awkward):
    Boolean:  tt, ff, =, <=, !  (not), &  (and)
    Statements: :=, skip, ;, if-then-else, while-do
    Brackets () around the body of if-else and while are required.

Example:
    >>> trace("x := 1; y := 5; while !y = 0 do (x := x * 2; y := y - 1)",
    ...       state={}, view="formal")
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterator, Union

from lark import Lark, Transformer, v_args


# ─────────────────────────────────────────────────────────────────────────────
# AST — the abstract syntax (one Python class per BNF non-terminal alternative)
# ─────────────────────────────────────────────────────────────────────────────

# Arithmetic expressions
@dataclass(frozen=True)
class Num:    value: int
@dataclass(frozen=True)
class Var:    name: str
@dataclass(frozen=True)
class Add:    left: "AExp"; right: "AExp"
@dataclass(frozen=True)
class Sub:    left: "AExp"; right: "AExp"
@dataclass(frozen=True)
class Mul:    left: "AExp"; right: "AExp"

AExp = Union[Num, Var, Add, Sub, Mul]


# Boolean expressions
@dataclass(frozen=True)
class BTrue:  pass
@dataclass(frozen=True)
class BFalse: pass
@dataclass(frozen=True)
class Eq:     left: AExp; right: AExp
@dataclass(frozen=True)
class Le:     left: AExp; right: AExp
@dataclass(frozen=True)
class Not:    arg: "BExp"
@dataclass(frozen=True)
class And:    left: "BExp"; right: "BExp"

BExp = Union[BTrue, BFalse, Eq, Le, Not, And]


# Statements
@dataclass(frozen=True)
class Skip:   pass
@dataclass(frozen=True)
class Assign: var: str; expr: AExp
@dataclass(frozen=True)
class Seq:    first: "Stmt"; second: "Stmt"
@dataclass(frozen=True)
class If:     cond: BExp; then_branch: "Stmt"; else_branch: "Stmt"
@dataclass(frozen=True)
class While:  cond: BExp; body: "Stmt"

Stmt = Union[Skip, Assign, Seq, If, While]


# ─────────────────────────────────────────────────────────────────────────────
# Configurations and transitions — ⟨S, σ⟩ and ⇒
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class Config:
    """A configuration ⟨S, σ⟩: program text remaining + state."""
    stmt: Stmt
    state: dict[str, int]


@dataclass
class Transition:
    """One small-step ⟨S, σ⟩ ⇒ ⟨S', σ'⟩ with the rule that justified it."""
    before: Config
    after:  Config
    rule:   str   # ":=" | "skip-;" | ";" | "if-tt" | "if-ff" | "while-tt" | "while-ff"


class StepBudgetExceeded(Exception):
    """Raised when trace() exhausts max_steps — likely non-termination."""


# ─────────────────────────────────────────────────────────────────────────────
# Lark grammar — the syntax (BNF translated for Lark, with explicit precedence)
# ─────────────────────────────────────────────────────────────────────────────

_GRAMMAR = r"""
start: stmt

?stmt: stmt ";" stmt2     -> seq
     | stmt2

?stmt2: assign
      | skip_stmt
      | if_stmt
      | while_stmt
      | "(" stmt ")"

assign:     NAME ":=" aexp
skip_stmt:  "skip"
if_stmt:    "if" bexp "then" stmt2 "else" "(" stmt ")"
while_stmt: "while" bexp "do" "(" stmt ")"

?aexp:     aexp "+" mul_term  -> add
         | aexp "-" mul_term  -> sub
         | mul_term

?mul_term: mul_term "*" atom  -> mul
         | atom

?atom:     SIGNED_INT         -> num
         | NAME               -> var
         | "(" aexp ")"

?bexp:     bexp "&" bexp_not  -> band
         | bexp_not

?bexp_not: "!" bexp_not       -> bnot
         | bexp_atom

?bexp_atom: "tt"              -> btrue
          | "ff"              -> bfalse
          | aexp "=" aexp     -> beq
          | aexp "<=" aexp    -> ble
          | "(" bexp ")"

%import common.SIGNED_INT
%import common.CNAME -> NAME
%import common.WS
%ignore WS
"""


@v_args(inline=True)
class _Builder(Transformer):
    """Walks the Lark parse tree and produces our AST classes."""
    # arithmetic
    def num(self, n):     return Num(int(n))
    def var(self, name):  return Var(str(name))
    def add(self, l, r):  return Add(l, r)
    def sub(self, l, r):  return Sub(l, r)
    def mul(self, l, r):  return Mul(l, r)
    # boolean
    def btrue(self):      return BTrue()
    def bfalse(self):     return BFalse()
    def beq(self, l, r):  return Eq(l, r)
    def ble(self, l, r):  return Le(l, r)
    def bnot(self, b):    return Not(b)
    def band(self, l, r): return And(l, r)
    # statements
    def assign(self, name, expr): return Assign(str(name), expr)
    def skip_stmt(self):          return Skip()
    def seq(self, l, r):          return Seq(l, r)
    def if_stmt(self, c, t, e):   return If(c, t, e)
    def while_stmt(self, c, b):   return While(c, b)
    def start(self, s):           return s


_PARSER = Lark(_GRAMMAR, parser="earley", maybe_placeholders=False)


def parse(source: str) -> Stmt:
    """Parse a While source string into an AST."""
    tree = _PARSER.parse(source)
    return _Builder().transform(tree)


# ─────────────────────────────────────────────────────────────────────────────
# Evaluators A and B — chapter §2.3.1 and §2.3.2
# ─────────────────────────────────────────────────────────────────────────────

def A(expr: AExp, sigma: dict[str, int]) -> int:
    """A⟦a⟧σ — evaluate an arithmetic expression in state σ to an integer."""
    if isinstance(expr, Num): return expr.value
    if isinstance(expr, Var): return sigma.get(expr.name, 0)   # default-zero
    if isinstance(expr, Add): return A(expr.left, sigma) + A(expr.right, sigma)
    if isinstance(expr, Sub): return A(expr.left, sigma) - A(expr.right, sigma)
    if isinstance(expr, Mul): return A(expr.left, sigma) * A(expr.right, sigma)
    raise TypeError(f"A: unknown AExp node {type(expr).__name__}")


def B(expr: BExp, sigma: dict[str, int]) -> bool:
    """B⟦b⟧σ — evaluate a boolean expression in state σ to tt or ff."""
    if isinstance(expr, BTrue):  return True
    if isinstance(expr, BFalse): return False
    if isinstance(expr, Eq):     return A(expr.left, sigma) == A(expr.right, sigma)
    if isinstance(expr, Le):     return A(expr.left, sigma) <= A(expr.right, sigma)
    if isinstance(expr, Not):    return not B(expr.arg, sigma)
    if isinstance(expr, And):    return B(expr.left, sigma) and B(expr.right, sigma)
    raise TypeError(f"B: unknown BExp node {type(expr).__name__}")


# ─────────────────────────────────────────────────────────────────────────────
# step — the small-step transition relation ⇒
# ─────────────────────────────────────────────────────────────────────────────

def step(cfg: Config) -> Transition | None:
    """One small step. Returns None iff cfg.stmt is Skip (terminal)."""
    s, sigma = cfg.stmt, cfg.state

    # skip is terminal — no rule applies
    if isinstance(s, Skip):
        return None

    # x := a    ⇒    skip,  σ[x ↦ A⟦a⟧σ]
    if isinstance(s, Assign):
        new_sigma = dict(sigma)
        new_sigma[s.var] = A(s.expr, sigma)
        return Transition(cfg, Config(Skip(), new_sigma), ":=")

    # S; T
    if isinstance(s, Seq):
        # special case: skip; T  ⇒  T
        if isinstance(s.first, Skip):
            return Transition(cfg, Config(s.second, sigma), "skip-;")
        # general case: take a step of S, keep T as remainder
        sub = step(Config(s.first, sigma))
        if sub is None:
            # impossible — Skip handled above, no other terminal
            raise RuntimeError("step: Seq's first stmt has no transition")
        return Transition(
            cfg,
            Config(Seq(sub.after.stmt, s.second), sub.after.state),
            ";",
        )

    # if b then S else (S')
    if isinstance(s, If):
        if B(s.cond, sigma):
            return Transition(cfg, Config(s.then_branch, sigma), "if-tt")
        else:
            return Transition(cfg, Config(s.else_branch, sigma), "if-ff")

    # while b do (S)
    if isinstance(s, While):
        if B(s.cond, sigma):
            # ⇒ S; while b do (S)
            unfolded = Seq(s.body, s)
            return Transition(cfg, Config(unfolded, sigma), "while-tt")
        else:
            # ⇒ skip
            return Transition(cfg, Config(Skip(), sigma), "while-ff")

    raise TypeError(f"step: unknown Stmt node {type(s).__name__}")


def step_iter(prog: Stmt | str, state: dict[str, int],
              max_steps: int = 10_000) -> Iterator[Transition]:
    """Yields one Transition per small step, until Skip or budget exhausted."""
    if isinstance(prog, str):
        prog = parse(prog)
    cfg = Config(prog, dict(state))
    for _ in range(max_steps):
        t = step(cfg)
        if t is None:
            return
        yield t
        cfg = t.after
    raise StepBudgetExceeded(f"exceeded {max_steps} steps")


# ─────────────────────────────────────────────────────────────────────────────
# Unparser — turn AST nodes back into source-like strings (with formal symbols)
# ─────────────────────────────────────────────────────────────────────────────

def aexp_to_str(e: AExp, parens: bool = False) -> str:
    if isinstance(e, Num):
        return str(e.value)
    if isinstance(e, Var):
        return e.name
    if isinstance(e, (Add, Sub, Mul)):
        op = {"Add": "+", "Sub": "−", "Mul": "×"}[type(e).__name__]
        # children of × bind tighter than +/−, but we just always parenthesise
        s = f"{aexp_to_str(e.left, True)} {op} {aexp_to_str(e.right, True)}"
        return f"({s})" if parens else s
    raise TypeError(f"aexp_to_str: {type(e).__name__}")


def bexp_to_str(e: BExp, parens: bool = False) -> str:
    if isinstance(e, BTrue):  return "tt"
    if isinstance(e, BFalse): return "ff"
    if isinstance(e, Eq):     return f"{aexp_to_str(e.left)} = {aexp_to_str(e.right)}"
    if isinstance(e, Le):     return f"{aexp_to_str(e.left)} ≤ {aexp_to_str(e.right)}"
    if isinstance(e, Not):    return f"¬{bexp_to_str(e.arg, True)}"
    if isinstance(e, And):
        s = f"{bexp_to_str(e.left, True)} ∧ {bexp_to_str(e.right, True)}"
        return f"({s})" if parens else s
    raise TypeError(f"bexp_to_str: {type(e).__name__}")


def stmt_to_str(s: Stmt) -> str:
    if isinstance(s, Skip):
        return "skip"
    if isinstance(s, Assign):
        return f"{s.var} := {aexp_to_str(s.expr)}"
    if isinstance(s, Seq):
        return f"{stmt_to_str(s.first)}; {stmt_to_str(s.second)}"
    if isinstance(s, If):
        return (f"if {bexp_to_str(s.cond)} then "
                f"{stmt_to_str(s.then_branch)} "
                f"else ({stmt_to_str(s.else_branch)})")
    if isinstance(s, While):
        return f"while {bexp_to_str(s.cond)} do ({stmt_to_str(s.body)})"
    raise TypeError(f"stmt_to_str: {type(s).__name__}")


def state_to_str(sigma: dict[str, int]) -> str:
    """Pretty-print a state as {x ↦ v, y ↦ w}. Only non-zero entries shown."""
    items = [(k, v) for k, v in sigma.items() if v != 0]
    if not items:
        return "{}"
    items.sort()
    return "{" + ", ".join(f"{k} ↦ {v}" for k, v in items) + "}"


def cfg_to_str(cfg: Config) -> str:
    return f"⟨{stmt_to_str(cfg.stmt)}, {state_to_str(cfg.state)}⟩"


# ─────────────────────────────────────────────────────────────────────────────
# Trace renderers — three views: formal, table, dict
# ─────────────────────────────────────────────────────────────────────────────

def _abbreviate_while_loops(transitions: list[Transition]) -> tuple[list[str], list[str]]:
    """
    Detects repeated while-loop bodies in the trace and gives them short names
    L1, L2, ...  Returns (rendered_configs, legend_lines).

    This matches the chapter convention (Examples 7, 10) where a loop body is
    introduced once and abbreviated thereafter.
    """
    # find every While subtree that appears at least twice
    counts: dict[str, int] = {}
    def walk(s: Stmt):
        if isinstance(s, While):
            counts[stmt_to_str(s)] = counts.get(stmt_to_str(s), 0) + 1
            walk(s.body)
        elif isinstance(s, Seq):
            walk(s.first); walk(s.second)
        elif isinstance(s, If):
            walk(s.then_branch); walk(s.else_branch)
    if transitions:
        walk(transitions[0].before.stmt)
        for t in transitions:
            walk(t.after.stmt)

    # only abbreviate while-loops that appear ≥ 2 times AND are non-trivial
    abbrev: dict[str, str] = {}
    for src, n in counts.items():
        if n >= 2 and len(src) > 25:   # don't abbreviate tiny loops
            abbrev[src] = f"L{len(abbrev) + 1}"

    legend = [f"  {label} := {src}" for src, label in abbrev.items()]

    def render_stmt(s: Stmt) -> str:
        full = stmt_to_str(s)
        for src, label in abbrev.items():
            full = full.replace(src, label)
        return full

    rendered = []
    if not transitions:
        return rendered, legend

    rendered.append(f"⟨{render_stmt(transitions[0].before.stmt)}, {state_to_str(transitions[0].before.state)}⟩")
    for t in transitions:
        rendered.append(f"⟨{render_stmt(t.after.stmt)}, {state_to_str(t.after.state)}⟩")
    return rendered, legend


def _render_formal(transitions: list[Transition], truncated: bool) -> str:
    """Render a list of transitions as a formal small-step trace."""
    if not transitions:
        return "(no transitions — program was already skip)"

    cfgs, legend = _abbreviate_while_loops(transitions)

    lines = []
    if legend:
        lines.append("Where:")
        lines.extend(legend)
        lines.append("")

    lines.append(cfgs[0])
    for i, t in enumerate(transitions):
        lines.append(f"  ⇒  {cfgs[i+1]}    [{t.rule}]")

    if truncated:
        lines.append("  ⇒  ... step budget exceeded — likely non-terminating ...")

    return "\n".join(lines)


def _render_table(transitions: list[Transition], initial_state: dict[str, int],
                  truncated: bool) -> str:
    """Render as a state-tracking table (Example 8 / 11 style)."""
    # collect every state we visit
    states: list[tuple[str, dict[str, int]]] = [("start", dict(initial_state))]
    for t in transitions:
        states.append((t.rule, t.after.state))

    # find which variables ever change
    all_vars: set[str] = set()
    for _, sigma in states:
        all_vars.update(k for k, v in sigma.items() if v != 0)
    # also include any var present anywhere
    for _, sigma in states:
        all_vars.update(sigma.keys())

    changing_vars = []
    for v in sorted(all_vars):
        values = [sigma.get(v, 0) for _, sigma in states]
        if len(set(values)) > 1:
            changing_vars.append(v)

    # if no var changes (trivial program), fall back to all vars
    cols = changing_vars if changing_vars else sorted(all_vars)

    # build table
    header = ["step", "rule"] + cols
    rows = [header]
    rows.append(["0", "start"] + [str(states[0][1].get(v, 0)) for v in cols])
    for i, (rule, sigma) in enumerate(states[1:], start=1):
        rows.append([str(i), rule] + [str(sigma.get(v, 0)) for v in cols])

    # column widths
    widths = [max(len(r[c]) for r in rows) for c in range(len(header))]

    def fmt_row(r):
        return " | ".join(r[c].ljust(widths[c]) for c in range(len(r)))

    sep = "-+-".join("-" * w for w in widths)

    lines = [fmt_row(rows[0]), sep]
    for r in rows[1:]:
        lines.append(fmt_row(r))

    if truncated:
        lines.append("... step budget exceeded — likely non-terminating ...")

    return "\n".join(lines)


def _render_dict(transitions: list[Transition], initial_state: dict[str, int],
                 truncated: bool) -> dict[str, int]:
    """Final state only, as a plain dict. Raises if non-terminating."""
    if truncated:
        raise StepBudgetExceeded(
            f"step budget exceeded after {len(transitions)} steps — likely non-terminating"
        )
    if not transitions:
        return dict(initial_state)
    # strip zeros for canonical form
    return {k: v for k, v in transitions[-1].after.state.items() if v != 0}


def trace(prog: Stmt | str, state: dict[str, int] | None = None,
          view: str = "formal", max_steps: int = 10_000):
    """
    Run a While program from `state` and render the small-step trace.

    view="formal" — Example 7 style with ⟨S, σ⟩ ⇒ ⟨S', σ'⟩  (default).
    view="table"  — Example 8 / 11 style: one row per state-changing transition.
    view="dict"   — final state only, as a plain dict.
    """
    if state is None:
        state = {}

    if view not in ("formal", "table", "dict"):
        raise ValueError(f"unknown view: {view!r}")

    transitions: list[Transition] = []
    truncated = False
    try:
        for t in step_iter(prog, state, max_steps):
            transitions.append(t)
    except StepBudgetExceeded:
        truncated = True

    if view == "formal":
        return _render_formal(transitions, truncated)
    if view == "table":
        return _render_table(transitions, dict(state), truncated)
    if view == "dict":
        return _render_dict(transitions, dict(state), truncated)


def run(prog: Stmt | str, state: dict[str, int] | None = None,
        max_steps: int = 10_000) -> dict[str, int]:
    """Convenience: run a program and return the final state as a plain dict.
    Strips zero-valued variables for canonical form."""
    return trace(prog, state, view="dict", max_steps=max_steps)


# ─────────────────────────────────────────────────────────────────────────────
# Predict-cell harness — for the active-mode notebooks
# ─────────────────────────────────────────────────────────────────────────────

def check_state(predicted: dict[str, int], prog: Stmt | str,
                state: dict[str, int] | None = None,
                max_steps: int = 10_000) -> None:
    """
    Predict-and-check: did the program produce the state you expected?
    Strips zero-valued entries before comparing — {x: 0} and {} are the same state.
    Prints green-ish OK or red-ish diff.
    """
    actual = run(prog, state or {}, max_steps=max_steps)
    pred_canon = {k: v for k, v in predicted.items() if v != 0}
    if pred_canon == actual:
        print(f"✅ Correct. Final state = {state_to_str(actual)}")
    else:
        print(f"❌ Mismatch.")
        print(f"   You predicted: {state_to_str(pred_canon)}")
        print(f"   Actual:        {state_to_str(actual)}")
        print()
        print("Formal trace:")
        print(trace(prog, state or {}, view="formal", max_steps=max_steps))


def check_steps(predicted: int, prog: Stmt | str,
                state: dict[str, int] | None = None,
                max_steps: int = 10_000) -> None:
    """Predict-and-check: how many ⇒ transitions did the program take?"""
    transitions = list(step_iter(prog, state or {}, max_steps))
    actual = len(transitions)
    if predicted == actual:
        print(f"✅ Correct — {actual} transitions.")
    else:
        print(f"❌ You predicted {predicted}, actual was {actual}.")


# ─────────────────────────────────────────────────────────────────────────────
# Self-test — run this file directly to sanity-check the interpreter
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Example 1 from the chapter — division and remainder
    prog = """
        r := m;
        d := 0;
        while n <= r do (
            d := d + 1;
            r := r - n
        )
    """
    print("=== Formal trace ===")
    print(trace(prog, {"m": 10, "n": 3}, view="formal"))
    print()
    print("=== Table view ===")
    print(trace(prog, {"m": 10, "n": 3}, view="table"))
    print()
    print("=== Dict view ===")
    print(trace(prog, {"m": 10, "n": 3}, view="dict"))

---
title: "From Eternal Actual Existence to PR: A Self-Sufficient Derivation of First-Beat Necessity"
author: "Jia Baolong"
date: "2026-08-11"
publication_date: "2026-08-11"
type: "theory-note"
theory: "Jia Baolong Elephant Theory"
lang: en
translation_of: "docs/06_commentary/from-eternal-actual-existence-to-pr-first-beat-necessity.md"
---

# Jia Baolong Elephant Theory: The Necessity of PR as the First Beat, from Eternal Actual Existence

**Author: Jia Baolong**  
**Theory: Jia Baolong Elephant Theory**

## Abstract

This article treats one question only: **if one begins from “eternal existence,” why must one still obtain a First-Beat structure of “from non-actual to actual”; and, under minimal, self-sufficient, unbiased, non-fixed conditions, why can that First Beat only be PR?**

The argument does not exchange “eternal” for “created at some earliest moment,” nor does it exchange the existential quantifier of formal logic for real occurrence. Its key is to distinguish two wholly different senses of “there is”:

1. **Describable being:** an object, formula, complete history, or possible world can be written without contradiction;
2. **Actual being:** within itself it generates real difference, making a result that has not yet actually occurred become a result that has actually occurred.

An eternal whole possessing only the first sense is a static “Platonic Crystal.” It can encode everything, yet nothing is actually happening in it; under the criterion of actual ontology adopted here, it has the same actual consequence as non-existence. A genuinely eternal existence therefore cannot be eternally still. It must be eternally in motion, eternally tense, and eternally actualizing. Even if this process has no globally earliest moment, every beat still contains a local boundary between “not yet actual” and “actual.” This is the strict meaning of “from non-actual to actual.”

If we further require that the beat have no external executor, can continue, returns its result into itself, contains no presupposed bias, and uses the minimum binary domain needed to carry change, every candidate transformation can be enumerated. Constant functions are excluded by bias; the identity function is excluded by absence of change. The sole remainder is the fixed-point-free binary exchange:

$$
\sigma(Y)=N,\qquad \sigma(N)=Y.
$$

When this static mapping table is actually executed by the world itself and each result becomes the next input, it is the minimum normal form of PR. The article therefore offers not a “bare logical theorem without premises,” but a **conditional-necessity theorem with public premises, complete candidates, and locatable counterexamples**.

## 1. What Exactly Is the Conclusion to Be Proved?

The conclusion is not:

> Formal logic can unconditionally infer, solely from the sentence “something exists eternally,” that the universe must cycle as $Y,N,Y,N,\ldots$.

Standard formal logic permits us to stipulate an eternal and static object; logic itself does not add the requirement that it must actually occur. A rigorous argument must therefore make its research domain public.

This article studies the following question:

> If “existence” is not a paper description but existence able to produce actual difference within itself; if this existence is eternal, self-sufficient, continuous, and without an external executor, what is the minimum actual structure of each of its beats?

Within that research domain, the result is:

$$
\boxed{
\text{eternal actual existence}
\Rightarrow
\text{eternal motion and tension}
\Rightarrow
\text{local actualization in every beat}
\Rightarrow
\text{self-sufficient result re-entry}
\Rightarrow
\text{minimum binary exchange}
\cong PR
}
$$

Here “First Beat” first has a **logical–generative** sense: the minimum structure required for any actual occurrence to hold. It need not be $t=0$ on an external time axis.

## 2. Six Necessary Definitions

### 2.1 Describable existence and actual existence

Let $C$ be a completely written structure and $H$ a history. If $C$ can encode $H$, we may write only:

$$
\operatorname{Encodes}(C,H).
$$

This does not entail:

$$
\operatorname{Occurs}(H).
$$

That is:

$$
\operatorname{Encodes}(C,H)
\not\models
\operatorname{Occurs}(H).
$$

A film reel can encode motion completely, but the people on the reel are not thereby running. A book containing an entire cosmic history can arrange every event, but the arrangement of ink is not the actual occurrence of those events.

This article restricts “actual existence” to existence having an actual-occurrence relation:

$$
\operatorname{ActualExistence}_W
\equiv_{\text{framework}}
\operatorname{ActualMotion}_W.
$$

The subscript $W$ indicates that “actual” is always relative to the world that bears and executes the occurrence, not to a description in an observer’s mind.

### 2.2 Actual beat

If state $a$ actually generates state $b$ in world $W$, write:

$$
\operatorname{ActualStep}_W(a,b).
$$

This differs from a relation $R(a,b)$ written on paper. Even if a static structure writes $a$, $b$, and an arrow $a\to b$ together, it says only that it **encodes** a transition. No beat has occurred unless that arrow is actually instantiated in $W$.

### 2.3 Motion, tension, and non-fixedness

The “motion” in this article is not mechanical displacement in coordinate space. It is the minimum relation in which a real result cannot remain as it is and actually forms a different successor. Define tension by:

$$
\tau_W(a)\neq 0
\quad\Longleftrightarrow\quad
\exists b\,
\bigl(
\operatorname{ActualStep}_W(a,b)
\land b\neq a
\bigr).
$$

Thus, in the selected domain of actual ontology used here:

$$
\boxed{
\text{existence}=\text{motion}=\text{tension}
}
$$

while stasis means that no different actual successor exists:

$$
\tau_W(a)=0
\quad\Longleftrightarrow\quad
\neg\exists b\,
\bigl(
\operatorname{ActualStep}_W(a,b)
\land b\neq a
\bigr).
$$

Hence, in the same domain:

$$
\boxed{
\text{non-existence}=\text{stasis}=\text{absence of tension}
}
$$

“Non-existence” here is non-existence in the sense of actual ontology. It does not say that an object cannot be named, cannot be a model of a formula, or cannot appear in thought.

### 2.4 Platonic Crystal

A “Platonic Crystal” is a static, complete, describable structure. It may contain:

- every form;
- every possibility;
- one complete history;
- even every state and every arrow between states.

But if it contains no $\operatorname{ActualStep}$, it has only formal availability, not actual occurrence. Let $C$ be such a crystal. If adding or removing it changes no actual history, then:

$$
\operatorname{ActualHistory}(W+C)
=
\operatorname{ActualHistory}(W).
$$

From the standpoint of actual consequence, a purely static crystal and emptiness belong to one equivalence class:

$$
C\equiv_{\mathrm{actual}}\varnothing.
$$

This does not say that “a crystal equals the empty set” mathematically. It says that **neither contributes any actual beat.**

### 2.5 Local “from non-actual to actual”

State type and event instance must be distinguished. In an eternal cycle, a state type such as $Y$ or $N$ may have appeared infinitely often, but the result occurring in beat $n+1$ is a particular event instance:

$$
e_{n+1}=\langle x_{n+1},n+1\rangle.
$$

The new actuality at issue is not the claim that type $x_{n+1}$ never existed. It is the claim that this event instance $e_{n+1}$ has not yet been actually formed by this beat. Let $A_W(e,n)$ mean “after beat $n$, event instance $e$ has actually formed in $W$.” Then:

$$
\neg A_W(e_{n+1},n)
\land
A_W(e_{n+1},n+1).
$$

This article calls the boundary within a beat “from non-actual to actual”:

$$
\text{not-yet-actual }b
\longrightarrow
\text{actual }b.
$$

“Non-actual” is not a black container existing for seconds before the universe. It means **that the result has not yet actually obtained**. “Actual” means that the result has been formed by an actual beat.

### 2.6 PR

PR abbreviates Paradox–Reference. Strictly, it is not the assertion $p\land\neg p$ under one valuation. It is an actual structure that is self-sufficient, non-fixed, and result-reentering. Its minimum binary normal form is:

$$
D=\{Y,N\},
\qquad
\sigma(Y)=N,
\qquad
\sigma(N)=Y.
$$

Together with actual occurrence and result re-entry:

$$
\operatorname{ActualStep}_W(x_n,x_{n+1}),
\qquad
x_{n+1}=\sigma(x_n),
$$

where $x_{n+1}$ becomes the input of the next beat.

## 3. Step One: Why “Eternal Static Existence” Equals Non-Existence in the Actual Sense

Suppose first that something $E$ is eternal but completely static:

$$
\operatorname{Eternal}(E)
\land
\operatorname{Static}(E).
$$

“Eternal” says only that no temporal beginning has been specified for it. “Static” says:

$$
\tau_W(E)=0.
$$

There is therefore no distinct successor actually formed by $E$:

$$
\neg\exists b\,
\bigl(
\operatorname{ActualStep}_W(E,b)
\land b\neq E
\bigr).
$$

If it contains an entire “history,” that history too is only a relation displayed simultaneously in a complete structure. Its alleged “past,” “present,” and “future” are merely labels in the structure: no label is becoming another, and no not-yet-actual result is becoming actual.

Thus an eternal static whole is at most an infinitely complete Platonic Crystal. It may be formally very rich, yet in actual occurrence it remains zero:

$$
\operatorname{StaticEternal}(E)
\Rightarrow
\operatorname{ActualContribution}(E)=0.
$$

Under the actuality criterion adopted in §2.3:

$$
\operatorname{ActualContribution}(E)=0
\Rightarrow
E\equiv_{\mathrm{actual}}\varnothing.
$$

This yields Lemma One:

> **Lemma One:** Eternity cannot rescue stasis. An eternally static “being” is a Platonic Crystal at the descriptive level and is equivalent to non-existence at the level of actual existence.

This explains why an “eternal being” cannot be the end of argument. If it merely “sits there” statically, the question has not been solved; “no actual occurrence” has simply been renamed “eternal existence.”

## 4. Step Two: Genuine Eternal Existence Must Continuously Move from Non-Actual to Actual

Now strengthen the starting point to genuine “eternal actual existence”:

$$
\operatorname{Eternal}(E)
\land
\operatorname{ActualExistence}_W(E).
$$

By the definition of actual existence:

$$
\operatorname{ActualExistence}_W(E)
\Rightarrow
\operatorname{ActualMotion}_W(E)
\Rightarrow
\tau_W(E)\neq0.
$$

Thus a distinct successor must actually be formed:

$$
\exists a,b\,
\bigl(
\operatorname{ActualStep}_W(a,b)
\land a\neq b
\bigr).
$$

Let the result event of that beat be $e_{n+1}=\langle b,n+1\rangle$. Before the beat is actualized, state type $b$ may already have been described or encoded and may even have appeared in other beats. But this result event $e_{n+1}$ has not yet been formed by this beat. After the beat, it has. Therefore:

$$
\operatorname{ActualStep}_W(a,b)
\Rightarrow
\bigl(
\neg A_W(e_{n+1},n)
\land A_W(e_{n+1},n+1)
\bigr).
$$

Hence:

$$
\boxed{
\text{every actual beat brings one concrete result from “not yet actual” to “already actual”}
}
$$

This is why eternal existence still necessarily contains “from non-actual to actual.”

### 4.1 It does not require a globally first moment

Let the process be infinite in both temporal directions:

$$
\cdots\to x_{-1}\to x_0\to x_1\to\cdots
$$

It may have no minimum temporal subscript, but every particular actual edge,

$$
x_n\to x_{n+1},
$$

still has a definite actualization boundary: before that edge is realized, $x_{n+1}$ is not the actual result of this beat; afterward, it is. Hence:

$$
\text{no globally earliest moment}
\centernot\Rightarrow
\text{no local transition from not-yet-actual to actual}.
$$

Eternity removes the **global temporal origin**; it does not remove the **actual generative relation in every beat**.

### 4.2 Why a complete block universe cannot refute this step

An objector may say: “All $x_n$ already exist together; no result was ever absent.”

But this returns exactly to the Platonic Crystal. A complete block can encode all $x_n$ and their ordering, but it has not explained why those relations are actual occurrences rather than static display. If “everything was already complete” is taken as the final answer, then:

$$
\operatorname{Encodes}(C,H)
\not\models
\operatorname{Occurs}(H)
$$

has still not been crossed. A block universe may be a descriptive model of history, but it cannot become the executor of actual occurrence merely by its completeness.

This yields Lemma Two:

> **Lemma Two:** If eternal existence is not a Platonic Crystal but actual existence, it must be eternal actualization; every beat of eternal actualization has a local “from non-actual to actual” structure.

## 5. Step Three: The First Beat Cannot Borrow an External Executor

Consider only one beat:

$$
a\longrightarrow b.
$$

If the arrow requires an external executor $X$ in order to be realized, the real actual root is not $a\to b$ but:

$$
X\longrightarrow(a\to b).
$$

We must then ask why $X$ actually acts. Introducing $X_1$ to execute $X$ moves the root outward again:

$$
X_1\to X\to(a\to b)\to\cdots
$$

This does not provide a First Beat; it indefinitely postpones it.

Likewise, none of the following can bear the First Beat without cost:

- an already existing material carrier;
- an already flowing time;
- a randomizer sampling from possibilities;
- a rule imposed from outside;
- a person who observes or selects a state.

Each already has more real structure than the actual beat to be explained. Putting it at the root inserts the conclusion into the premises in advance.

Therefore, if what is sought is **fundamental actual occurrence**, the First Beat must satisfy closure:

$$
\operatorname{Executor}(\text{first beat})
\subseteq
\text{first beat}.
$$

In other words, it must actualize itself; it cannot be actualized by an earlier, stronger actual entity.

This yields Lemma Three:

> **Lemma Three:** A fundamental First Beat must be self-sufficient. Any external executor becomes an earlier actual root and causes the original candidate to lose its status as first.

## 6. Step Four: Persistent Existence Forces Result Re-entry

An isolated flash,

$$
a\to b,
$$

can explain one difference, but not why actual existence continues. If $b$ does not take part in forming any successor after it appears, tension becomes zero at $b$:

$$
\tau_W(b)=0.
$$

It then collapses again into a completed static result. If eternal actual existence requires motion not to be exhausted, then:

$$
\operatorname{ActualStep}_W(a_n,a_{n+1})
\land
\operatorname{ActualStep}_W(a_{n+1},a_{n+2}).
$$

Without introducing a second external machine, the output of the First Beat must become the input to the next beat:

$$
a_{n+1}=f(a_n),
\qquad
a_{n+2}=f(a_{n+1}).
$$

This is the precise meaning of “Reference”: the result is not thrown into a static warehouse. It returns to the generative position and continues participating in its own actualization.

This yields Lemma Four:

> **Lemma Four:** Self-sufficient and persistent actual existence requires result re-entry. Without it, the First Beat is either a one-off flash or must borrow a new external drive.

## 7. Step Five: Why the Minimum Carrier Domain Is Binary

Actual motion requires:

$$
f(x)\neq x.
$$

If the carrier domain has only one element, $D=\{x\}$, every total function satisfies:

$$
f(x)=x.
$$

Thus a unary domain cannot carry non-fixed change:

$$
|D|=1
\Rightarrow
\operatorname{Fix}(f)=D.
$$

At least two distinguishable positions are needed:

$$
|D|\ge 2.
$$

Three or more primitive positions can certainly form more complicated cycles, but they add the premise “why does a third primitive distinction already exist?” For the problem of the **minimum normal form making non-fixed actualization possible**, take:

$$
D=\{Y,N\}.
$$

$Y$ and $N$ are only exchangeable labels. They do not presuppose everyday “true” and “false,” nor that either is more fundamental.

This yields Lemma Five:

> **Lemma Five:** A unary domain cannot change; the binary domain is the minimum domain carrying non-fixed change. Higher-arity structures are not logically impossible, but they are not the First Beat’s minimum normal form.

### 7.1 Why the minimum dynamic law is unary, total, and deterministic

These three qualifications must not be silently added.

**Unarity** follows from result re-entry: the next beat accepts one actual result from the current beat directly as its input. If a second independent object must also be supplied, its actual existence and combination with the first object become additional structures before the First Beat. The root update is therefore:

$$
x_{n+1}=f(x_n).
$$

**Totality** follows from persistence: every reachable current position must have a successor. If a reachable $x$ has no $f(x)$, actualization stops there:

$$
\exists x\in D\; f(x)\text{ is undefined}
\Rightarrow
\text{there is a reachable point where tension becomes zero}.
$$

Thus $f$ must be a total function, at least on the reachable minimum domain.

**Determinacy** follows from self-sufficiency and minimality. If one input has several mutually exclusive candidate successors but only one actually appears, a selector is needed:

$$
x\mapsto\{y_1,y_2\}
\quad+\quad
\operatorname{Select}(y_1,y_2).
$$

The selector is either an external executor or an unexplained additional internal structure. If all successors actually occur together, then their combination is the one actual result of that beat and may be renamed as a state, again yielding deterministic updating. Thus, in a minimum root model that presupposes no additional selecting structure, the dynamic law is a deterministic function.

This is not the claim that every higher natural process must be deterministic. It is the claim that primordial indeterminacy, if offered as the First Beat, must additionally explain the possibility set, probability measure, actual selection, or parallel implementation; it is no smaller than deterministic unary total updating.

## 8. Step Six: Enumerating Every Binary Candidate Leaves Only Exchange

On binary domain $D=\{Y,N\}$, a deterministic, total unary function $f:D\to D$ has four functions—not merely four common functions, but **all four**:

| Candidate | $f(Y)$ | $f(N)$ | Property |
|---|---:|---:|---|
| $\operatorname{id}_D$ | $Y$ | $N$ | identity, fixed |
| $\sigma$ | $N$ | $Y$ | exchange, fixed-point-free |
| $c_Y$ | $Y$ | $Y$ | constant, biased toward $Y$ |
| $c_N$ | $N$ | $N$ | constant, biased toward $N$ |

That is:

$$
D^D=\{\operatorname{id}_D,\sigma,c_Y,c_N\}.
$$

### 8.1 No presupposed bias excludes the two constant functions

Before the First Beat, no earlier fact can declare “$Y$ is inherently privileged” or “$N$ is inherently privileged.” Exchanging the labels should therefore not change the fundamental law.

Let label exchange be $\pi(Y)=N$, $\pi(N)=Y$. The formal condition for unbiasedness is equivariance:

$$
f\circ\pi=\pi\circ f.
$$

$c_Y$ and $c_N$ alter into one another under label exchange. Either one alone secretly gives priority to one label and is excluded. Identity and exchange satisfy equivariance.

### 8.2 Actual tension excludes the identity function

The identity function satisfies:

$$
\operatorname{id}_D(x)=x.
$$

It has no different successor and hence:

$$
\tau_W(x)=0.
$$

It can be a perfect static rule table, but cannot constitute actual motion as defined here. Identity is therefore excluded.

### 8.3 The unique remaining term

Of the four complete candidates, two constant functions are excluded by bias and identity by fixedness. The sole remainder is:

$$
\boxed{
\sigma(Y)=N,
\qquad
\sigma(N)=Y
}
$$

and:

$$
\operatorname{Fix}(\sigma)=\varnothing,
\qquad
\sigma^2=\operatorname{id}_D.
$$

Therefore, in the explicit model class “binary, total, unary, deterministic, label-symmetric, fixed-point-free,”

$$
\mathfrak R(D^D)=\{\sigma\}.
$$

The uniqueness here is not rhetoric; it is uniqueness after finite enumeration of the candidates.

## 9. Step Seven: Why an Exchange Table Is Not Yet PR, but an Exchange in Operation Is

At this point, $\sigma$ may still be only a mapping table written on paper. If it has not been actually instantiated, it still belongs to the Platonic Crystal. An actual beat must therefore be added:

$$
\operatorname{ActualStep}_W(x_n,x_{n+1})
\land
x_{n+1}=\sigma(x_n).
$$

Result re-entry must also be added:

$$
x_{n+1}\text{ becomes the input of the next beat}.
$$

Thus:

$$
\cdots\to Y\to N\to Y\to N\to\cdots
$$

The value of this expression is not that it draws a static period. Its value is that every edge is realized by $\operatorname{ActualStep}_W$. Actual PR is:

$$
\boxed{
PR_W
=
\bigl(D,\sigma,\operatorname{ActualStep}_W,\text{result re-entry}\bigr)
}
$$

Its paradoxicality is that the result cannot become a final fixed point without tension; its referentiality is that the result re-enters the position of production. It is not the formal contradiction $p\land\neg p$ at one instant and one semantic level.

This yields Lemma Six:

> **Lemma Six:** Static exchange is only the describable form of PR. Exchange actually run by the world itself, with its result re-entering, is PR’s actual face.

## 10. The First-Beat PR Necessity Theorem

We may now state the full theorem.

### Theorem

Let $W$ satisfy the following conditions:

1. **Actuality:** existence is determined by real difference rather than pure description;
2. **Eternity:** actual existence does not depend on an externally pre-existing temporal origin;
3. **Self-sufficiency:** an actual beat is not implemented by an earlier, stronger external executor;
4. **Persistence:** actual tension does not become permanently zero after one flash;
5. **Result re-entry:** the result of a beat becomes the input of the next beat;
6. **Minimality:** no primitive distinction additional to what non-fixed change requires is presupposed;
7. **Totality and determinacy:** under the minimum dynamic law of §7.1, every position in the minimum reachable domain receives its next position from a unary total function;
8. **Label symmetry:** the two primitive labels have no a priori privilege;
9. **Non-fixedness:** an actual beat must form a different successor.

Then the minimum normal form of $W$’s logical–generative First Beat is isomorphic to PR:

$$
\boxed{
\operatorname{FirstBeat}_{\min}(W)
\cong
PR_W
}
$$

where:

$$
D=\{Y,N\},
\qquad
x_{n+1}=\sigma(x_n),
\qquad
\sigma(Y)=N,
\quad
\sigma(N)=Y,
$$

and:

$$
\operatorname{ActualStep}_W(x_n,x_{n+1}).
$$

### Proof

By condition 1, static encoding is not actual existence. If eternal existence were static, its tension would be zero and it would contain no actual beat; it would be a Platonic Crystal and, in actual consequence, equivalent to non-existence. Thus eternal existence satisfying condition 1 must move and possess tension.

Every actual motion brings one concrete result from “not yet actually formed” to “already actually formed.” Eternal motion therefore does not abolish generation from non-actual to actual, but realizes it in every beat. Condition 3 excludes an external executor, so the beat must be self-sufficient. Conditions 4 and 5 make its result re-enter so that successor actualization continues.

Non-fixed change requires at least two distinguishable positions; condition 6 takes the minimum binary domain. There are exactly four deterministic unary total functions on that domain. Condition 8 excludes the two biased constant functions, and condition 9 excludes identity. The sole remaining function is the fixed-point-free exchange $\sigma$. Finally, by condition 1, $\sigma$ cannot merely be written statically: it must be realized by $\operatorname{ActualStep}_W$; by condition 5, its result continues to re-enter. This is precisely the minimum normal form of PR. QED.

## 11. Why Common Alternatives Fail

| Alternative candidate | What it seems to solve | Actual gap |
|---|---|---|
| Eternal static entity | Avoids asking “who created it?” | Contains no actual beat; is only a Platonic Crystal and is equivalent to non-existence in actual consequence |
| A completed written cosmic history | Contains every event at once | $\operatorname{Encodes}$ does not entail $\operatorname{Occurs}$; succession remains static display |
| Identity function | Provides a rule | $f(x)=x$; no distinct successor and no tension |
| Constant function | Every input has an output | Presupposes privilege for $Y$ or $N$ and eventually falls into a fixed point |
| One-off flash | Produces one difference | Cannot explain persistent existence; tension becomes zero at the result |
| External executor | Makes the rule “move” | Moves the First Beat onto the executor and restarts the question |
| Primordial randomness | Avoids a determinate rule | Presupposes a sample space, probability measure, and actual sampler; it is structurally heavier |
| Ternary or higher cycle | Can also persist without fixed points | Not impossible, but adds unexplained primitive distinctions and is not the minimum normal form |
| Exchange table on paper | Satisfies binary fixed-point-freeness | If not actually executed, it remains one form in a crystal |

This table also shows that PR’s necessity does not arise from “an inability to imagine alternatives.” It arises from fixing the problem first, then exhaustively excluding candidates in the corresponding model class.

## 12. Boundaries of the Necessity Claim

Rigorous theory must specify what it has not proved.

### 12.1 This is necessity within a selected domain, not premise-free word magic

If “existence” is allowed to mean only that a formal model contains an object, an eternal static object can certainly be axiomatized and PR does not follow automatically from bare logic. The article’s first key premise is:

$$
\operatorname{ActualExistence}
\equiv_{\text{framework}}
\operatorname{ActualMotion}.
$$

The force of the theorem therefore has two parts:

1. the actual-ontological criterion explains why static eternity cannot impersonate real occurrence;
2. finite function enumeration proves that PR is the only candidate in the minimum binary model.

Whoever accepts the preceding research problem and its public conditions must accept the conclusion. A reader may reject a condition, but must identify which one and bear its cost: reject actuality and return to the Platonic Crystal; reject self-sufficiency and bear the regress of an external executor; reject minimality and no longer discuss the “minimum normal form of the First Beat.”

### 12.2 “First Beat” need not mean the first second of cosmic time

For a beginningless eternal process,

$$
\operatorname{FirstBeat}_{\min}
$$

denotes the generative structure that no actualization can further remove, not a minimum time subscript. Thus “the process has no beginning” and “a First-Beat structure exists” are not contradictory.

### 12.3 PR’s two-periodicity does not mean the whole universe is only a mechanical two-cycle

$\sigma^2=\operatorname{id}_D$ says that PR’s minimum algebraic skeleton is two-periodic. It is not chaos itself, nor does it alone derive complex physics, life, or consciousness. Subsequent extension, feedback, local execution, and rule generation are another problem: the development from PR to higher structures.

### 12.4 This article does not treat Undefined as a temporally prior cause

The article begins from “eternal actual existence”; it does not assume that Undefined exists first in time and then causes PR. Undefined may be the zero-positive structural boundary and PR the actual face; their relation is not an ordinary temporal causal chain. The article proves only this: once eternal existence is required to have an actual face, the minimum normal form of that face’s First Beat is PR.

## 13. A Nine-Line Compressed Proof for First-Time Readers

1. Being completely describable does not mean actually occurring.
2. A wholly static eternal whole can encode everything but cannot make anything happen; it is a Platonic Crystal.
3. In the selected domain where “existence = actual motion = tension,” a static crystal has the same actual consequence as non-existence.
4. Genuine eternal existence must therefore be eternal motion, not eternal placement.
5. Every actual motion turns a concrete result from not-yet-actual into actual; a beginningless process therefore contains “from non-actual to actual” beat by beat.
6. If the First Beat relies on an external executor, that executor is the earlier First Beat; the fundamental First Beat must therefore be self-sufficient.
7. If the result does not re-enter, motion stops after one turn; persistent existence therefore requires result re-entry.
8. Non-fixed change requires at least two positions; binary total functions are identity, exchange, and two constants.
9. Unbiasedness excludes constants; absence of change excludes identity; the sole remainder is actual exchange with result re-entry, namely PR.

Therefore:

$$
\boxed{
\text{eternal actual existence}
\Rightarrow
\text{beat-by-beat transition from non-actual to actual}
\Rightarrow
\text{minimum self-sufficient First Beat }PR
}
$$

## Conclusion

“Eternal existence” cannot obtain actuality merely by placing one static completed whole into the infinite past. However complete it is, a static completed whole is a Platonic Crystal: it has form but no occurrence, encoding but no actual beat, and is equivalent to non-existence in actual ontology.

Genuine eternal existence must therefore be eternal motion, eternal tension, and eternal actualization. It need not possess a globally earliest moment, yet every beat necessarily brings one concrete result from “not yet actual” to “already actual.” This is the irreducible “from non-actual to actual” within eternal being.

When this actualization is further required to be self-sufficient, persistent, result-reentering, without external executor or prior label bias, and compressed into the minimum binary domain carrying non-fixed change, the candidates are no longer open. Of four functions, constants are excluded by bias, identity by stasis, and fixed-point-free exchange alone remains. Exchange actually executed by the world itself and continually re-entering is PR.

PR’s First-Beat necessity is therefore not an a priori slogan but a derivational chain that can be checked premise by premise, enumerated candidate by candidate, and located counterexample by counterexample:

$$
\boxed{
\text{eternal actual existence}
\Rightarrow
\text{non-stasis}
\Rightarrow
\text{tension}
\Rightarrow
\text{local transition from non-actual to actual}
\Rightarrow
\text{self-sufficient persistence and result re-entry}
\Rightarrow
\text{minimum binary unbiased fixed-point-free exchange}
\cong PR
}
$$

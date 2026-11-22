(* code/coq/F28_singular_root.v

   The owner's nineteenth Coq file (22 November 2026), which supersedes the eighteenth (it contains its theorem and adds two): unchanged except
   for this header.  Standalone.  For f(X) = X^3 + A X + B with f'(r) = 3 r^2 + A:
     F28_singular_root_nonzero : p | f'(r) and p not dividing A give p not dividing r (no hypothesis on p);
     F28_singular_B_relation   : p | f(r) and p | f'(r) give p | B - 2 r^3   (f(r) - r f'(r) = B - 2 r^3, checked by hand);
     F28_singular_B_nonzero    : p prime not dividing 2, p | f(r), p | f'(r), p not dividing A give p not dividing B
                                 (else p | 2 r^3, so p | r, contradiction).
   All correct and sound.  These are the nonvanishing inputs of the tangent equivalence of F28_tangent_character.v; the combined theorem there,
   F28_nodal_split_criterion (prime p >= 5, p | f(r), p | f'(r), p not dividing A: (-c6/p) = (3r/p) in certificate form), proves the same
   nondivisibility of B inline. *)
From Coq Require Import ZArith.
From Coq Require Import Znumtheory.
From Coq Require Import Ring.

Open Scope Z_scope.

Definition F28_cubic (A B r : Z) : Z :=
  r^3 + A*r + B.

Definition F28_derivative (A r : Z) : Z :=
  3*r^2 + A.

Lemma F28_divide_product :
  forall p x y : Z,
    (p | x) ->
    (p | x*y).
Proof.
  intros p x y H.
  destruct H as [k Hk].
  exists (k*y).
  rewrite Hk.
  ring.
Qed.

Lemma F28_divide_difference :
  forall p x y : Z,
    (p | x) ->
    (p | y) ->
    (p | x-y).
Proof.
  intros p x y Hx Hy.
  destruct Hx as [u Hu].
  destruct Hy as [v Hv].
  exists (u-v).
  rewrite Hu, Hv.
  ring.
Qed.

Theorem F28_singular_root_nonzero :
  forall p A r : Z,
    (p | F28_derivative A r) ->
    ~ (p | A) ->
    ~ (p | r).
Proof.
  intros p A r Hderivative Hnonzero Hr.

  assert (Hr2 : (p | r*r)).
  {
    apply F28_divide_product.
    exact Hr.
  }

  assert (Hthree : (p | 3*r^2)).
  {
    replace (3*r^2) with ((r*r)*3) by ring.
    apply F28_divide_product.
    exact Hr2.
  }

  apply Hnonzero.

  replace A with
    (F28_derivative A r - 3*r^2).
  - apply F28_divide_difference.
    + exact Hderivative.
    + exact Hthree.
  - unfold F28_derivative.
    ring.
Qed.

Theorem F28_singular_B_relation :
  forall p A B r : Z,
    (p | F28_cubic A B r) ->
    (p | F28_derivative A r) ->
    (p | B - 2*r^3).
Proof.
  intros p A B r Hcubic Hderivative.

  replace (B - 2*r^3) with
    (F28_cubic A B r -
     F28_derivative A r*r).
  - apply F28_divide_difference.
    + exact Hcubic.
    + apply F28_divide_product.
      exact Hderivative.
  - unfold F28_cubic, F28_derivative.
    ring.
Qed.

Theorem F28_singular_B_nonzero :
  forall p A B r : Z,
    prime p ->
    ~ (p | 2) ->
    (p | F28_cubic A B r) ->
    (p | F28_derivative A r) ->
    ~ (p | A) ->
    ~ (p | B).
Proof.
  intros p A B r
    Hp Hnot2 Hcubic Hderivative HnotA HB.

  assert (Hrnonzero : ~ (p | r)).
  {
    apply (F28_singular_root_nonzero p A r).
    - exact Hderivative.
    - exact HnotA.
  }

  assert (Hrelation : (p | B - 2*r^3)).
  {
    apply (F28_singular_B_relation p A B r).
    - exact Hcubic.
    - exact Hderivative.
  }

  assert (Htwor3 : (p | 2*r^3)).
  {
    replace (2*r^3) with
      (B - (B - 2*r^3)) by ring.
    apply F28_divide_difference.
    - exact HB.
    - exact Hrelation.
  }

  assert (Hr3 : (p | r^3)).
  {
    assert (Hsplit :
      (p | 2) \/ (p | r^3)).
    {
      eapply prime_mult.
      - exact Hp.
      - exact Htwor3.
    }
    destruct Hsplit as [Htwo | Hcube].
    - contradiction.
    - exact Hcube.
  }

  assert (Hr : (p | r)).
  {
    replace (r^3) with (r*(r*r)) in Hr3
      by ring.

    assert (Hsplit :
      (p | r) \/ (p | r*r)).
    {
      eapply prime_mult.
      - exact Hp.
      - exact Hr3.
    }

    destruct Hsplit as [Hfirst | Hsquare].
    - exact Hfirst.
    - assert (Hsplit2 :
        (p | r) \/ (p | r)).
      {
        eapply prime_mult.
        - exact Hp.
        - exact Hsquare.
      }
      destruct Hsplit2 as [Hleft | Hright].
      + exact Hleft.
      + exact Hright.
  }

  exact (Hrnonzero Hr).
Qed.

Check F28_singular_root_nonzero.
Check F28_singular_B_relation.
Check F28_singular_B_nonzero.

Print Assumptions F28_singular_B_nonzero.

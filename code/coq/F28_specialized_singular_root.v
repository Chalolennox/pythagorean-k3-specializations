(* code/coq/F28_specialized_singular_root.v

   The owner's thirtieth Coq file (22 November 2026), the integrated version of the 22nd-29th files.  The text is the owner's, with ONE change: the five imports
   "From Stdlib Require Import ..." are written "From Coq Require Import ..." (CI compiles with Coq 8.20.1, which has no Stdlib prefix).  Plus this header.  Standalone.
   WHAT IT PROVES, for the paper's integral model A = 4 a c^3, B = -8 b c^5, F = 4 a^3 + 27 b^2 c:
     F28_specialized_singular_root: prime p >= 5, p | F, p not dividing a, p not dividing c  ==>  there is an integer r with p | r^3 + A r + B and p | 3 r^2 + A.
   Proof (read by hand): p | F gives p | Delta = -64 c^9 F (F28_F_divides_discriminant); p not dividing A = 4 a c^3 (F28_specialized_A_nonzero); then
   F28_discriminant_gives_singular_root (r = -3 B u, with 2 A u = 1 mod p by Z.gcd_bezout).  The supporting lemmas (candidate identities, inverse, nonvanishing) are the
   ones of files 22-29.  This is the single closed theorem that the 29th file lacked: from p | F to an integer double root of the paper's model.
   WHAT IT DOES NOT PROVE: that p not dividing a, c follows from the Pythagorean hypotheses (F28_main_arithmetic in F28_arithmetic.v), nor the character relation
   (see F28_large_prime_tangent.v and F28_primitive_character.v) nor the Tate/Silverman bridge.  The files do not import each other, so the chain is not yet one theorem. *)

From Coq Require Import ZArith.
From Coq Require Import Znumtheory.
From Coq Require Import Zgcd_alt.
From Coq Require Import Ring.
From Coq Require Import Lia.

Open Scope Z_scope.

(* ======================================== *)
(* F.28: SPECIALIZED SINGULAR ROOT          *)
(* ======================================== *)

Definition F28_A (a c : Z) : Z :=
  4*a*c^3.

Definition F28_B (b c : Z) : Z :=
  -8*b*c^5.

Definition F28_F (a b c : Z) : Z :=
  4*a^3 + 27*b^2*c.

Definition F28_cubic (A B x : Z) : Z :=
  x^3 + A*x + B.

Definition F28_derivative (A x : Z) : Z :=
  3*x^2 + A.

Definition F28_discriminant (A B : Z) : Z :=
  -4*A^3 - 27*B^2.

Definition F28_root_numerator (B : Z) : Z :=
  -3*B.

Definition F28_root_denominator (A : Z) : Z :=
  2*A.

Definition F28_candidate_root (B u : Z) : Z :=
  F28_root_numerator B*u.

(* ======================================== *)
(* DIVISIBILITY HELPERS                     *)
(* ======================================== *)

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
  destruct Hx as [k Hk].
  destruct Hy as [l Hl].
  exists (k-l).
  rewrite Hk, Hl.
  ring.
Qed.

Lemma F28_prime_product_split :
  forall p x y : Z,
    prime p ->
    (p | x*y) ->
    (p | x) \/ (p | y).
Proof.
  intros p x y Hp Hxy.
  eapply prime_mult; eauto.
Qed.

Lemma F28_nonzero_product :
  forall p x y : Z,
    prime p ->
    ~ (p | x) ->
    ~ (p | y) ->
    ~ (p | x*y).
Proof.
  intros p x y Hp Hx Hy Hxy.
  destruct
    (F28_prime_product_split p x y Hp Hxy)
    as [Hpx | Hpy].
  - exact (Hx Hpx).
  - exact (Hy Hpy).
Qed.

(* ======================================== *)
(* LARGE PRIME NONDIVISIBILITY              *)
(* ======================================== *)

Lemma F28_large_prime_not_divide_two :
  forall p : Z,
    prime p ->
    5 <= p ->
    ~ (p | 2).
Proof.
  intros p Hp Hlarge Hdiv.
  destruct Hdiv as [k Hk].

  destruct (Z_le_gt_dec 0 k) as [Hnonneg | Hneg].
  - destruct (Z.eq_dec k 0) as [Hzero | Hnonzero].
    + subst k.
      lia.
    + assert (1 <= k) by lia.
      nia.
  - assert (k <= -1) by lia.
    nia.
Qed.

Lemma F28_large_prime_not_divide_four :
  forall p : Z,
    prime p ->
    5 <= p ->
    ~ (p | 4).
Proof.
  intros p Hp Hlarge Hfour.

  assert (Htwo : ~ (p | 2)).
  {
    apply (F28_large_prime_not_divide_two p).
    - exact Hp.
    - exact Hlarge.
  }

  assert (Hproduct : (p | 2*2)).
  {
    replace (2*2) with 4 by ring.
    exact Hfour.
  }

  destruct
    (F28_prime_product_split p 2 2 Hp Hproduct)
    as [Hleft | Hright].
  - exact (Htwo Hleft).
  - exact (Htwo Hright).
Qed.

Lemma F28_nonzero_cube :
  forall p c : Z,
    prime p ->
    ~ (p | c) ->
    ~ (p | c^3).
Proof.
  intros p c Hp HnotC.

  assert (Hc2 : ~ (p | c*c)).
  {
    apply (F28_nonzero_product p c c).
    - exact Hp.
    - exact HnotC.
    - exact HnotC.
  }

  assert (Hc3 : ~ (p | (c*c)*c)).
  {
    apply (F28_nonzero_product p (c*c) c).
    - exact Hp.
    - exact Hc2.
    - exact HnotC.
  }

  replace (c^3) with ((c*c)*c) by ring.
  exact Hc3.
Qed.

(* ======================================== *)
(* SPECIALIZED A IS NONZERO MODULO p        *)
(* ======================================== *)

Lemma F28_specialized_A_nonzero :
  forall p a c : Z,
    prime p ->
    5 <= p ->
    ~ (p | a) ->
    ~ (p | c) ->
    ~ (p | F28_A a c).
Proof.
  intros p a c Hp Hlarge HnotA HnotC.
  unfold F28_A.

  assert (Hfour : ~ (p | 4)).
  {
    apply (F28_large_prime_not_divide_four p).
    - exact Hp.
    - exact Hlarge.
  }

  assert (Hc3 : ~ (p | c^3)).
  {
    apply (F28_nonzero_cube p c).
    - exact Hp.
    - exact HnotC.
  }

  assert (H4a : ~ (p | 4*a)).
  {
    apply (F28_nonzero_product p 4 a).
    - exact Hp.
    - exact Hfour.
    - exact HnotA.
  }

  replace (4*a*c^3) with ((4*a)*c^3)
    by ring.

  apply (F28_nonzero_product p (4*a) (c^3)).
  - exact Hp.
  - exact H4a.
  - exact Hc3.
Qed.

(* ======================================== *)
(* SPECIALIZED DISCRIMINANT                 *)
(* ======================================== *)

Lemma F28_specialized_discriminant_identity :
  forall a b c : Z,
    F28_discriminant (F28_A a c) (F28_B b c) =
    -64*c^9*F28_F a b c.
Proof.
  intros a b c.
  unfold F28_discriminant,
    F28_A, F28_B, F28_F.
  ring.
Qed.

Lemma F28_F_divides_discriminant :
  forall p a b c : Z,
    (p | F28_F a b c) ->
    (p | F28_discriminant
       (F28_A a c) (F28_B b c)).
Proof.
  intros p a b c HF.
  rewrite F28_specialized_discriminant_identity.

  replace (-64*c^9*F28_F a b c)
    with (F28_F a b c*(-64*c^9))
    by ring.

  apply F28_divide_product.
  exact HF.
Qed.

(* ======================================== *)
(* MODULAR INVERSE VIA BEZOUT               *)
(* ======================================== *)

Lemma F28_bezout_to_inverse :
  forall p s k u : Z,
    p*k + s*u = 1 ->
    (p | s*u-1).
Proof.
  intros p s k u H.
  exists (-k).
  rewrite <- H.
  ring.
Qed.

Lemma F28_coprime_inverse :
  forall p s : Z,
    Z.gcd p s = 1 ->
    exists u : Z, (p | s*u-1).
Proof.
  intros p s Hgcd.

  pose proof
    (Z.gcd_bezout p s 1 Hgcd)
    as Hbezout.

  unfold Z.Bezout in Hbezout.
  destruct Hbezout as [k [u Hidentity]].

  exists u.
  apply (F28_bezout_to_inverse p s k u).
  rewrite <- Hidentity.
  ring.
Qed.

Lemma F28_prime_inverse :
  forall p s : Z,
    prime p ->
    ~ (p | s) ->
    exists u : Z, (p | s*u-1).
Proof.
  intros p s Hp Hnotdiv.

  apply F28_coprime_inverse.
  apply Zis_gcd_gcd.
  - lia.
  - apply prime_rel_prime.
    + exact Hp.
    + exact Hnotdiv.
Qed.

(* ======================================== *)
(* CANDIDATE ROOT IDENTITIES                *)
(* ======================================== *)

Lemma F28_candidate_derivative_identity :
  forall A B u : Z,
    F28_derivative A (F28_candidate_root B u) =
    -u^2*F28_discriminant A B
    - A*(F28_root_denominator A*u-1)*
        (F28_root_denominator A*u+1).
Proof.
  intros A B u.
  unfold F28_candidate_root,
    F28_derivative,
    F28_root_numerator,
    F28_root_denominator,
    F28_discriminant.
  ring.
Qed.

Lemma F28_candidate_cubic_identity :
  forall A B u : Z,
    F28_cubic A B (F28_candidate_root B u) =
    B*u^3*F28_discriminant A B
    -(F28_root_denominator A*u-1)*
     (A*(F28_root_numerator B)*u*
        (F28_root_denominator A*u+1)
      + B*((F28_root_denominator A*u)^2
           + F28_root_denominator A*u+1)).
Proof.
  intros A B u.
  unfold F28_candidate_root,
    F28_cubic,
    F28_root_numerator,
    F28_root_denominator,
    F28_discriminant.
  ring.
Qed.

Lemma F28_candidate_derivative_divisible :
  forall p A B u : Z,
    (p | F28_discriminant A B) ->
    (p | F28_root_denominator A*u-1) ->
    (p | F28_derivative A
       (F28_candidate_root B u)).
Proof.
  intros p A B u HD Hinv.
  rewrite F28_candidate_derivative_identity.

  apply F28_divide_difference.
  - replace (-u^2*F28_discriminant A B)
      with (F28_discriminant A B*(-u^2))
      by ring.
    apply F28_divide_product.
    exact HD.
  - replace
      (A*(F28_root_denominator A*u-1)*
         (F28_root_denominator A*u+1))
      with
      ((F28_root_denominator A*u-1)*
         (A*(F28_root_denominator A*u+1)))
      by ring.
    apply F28_divide_product.
    exact Hinv.
Qed.

Lemma F28_candidate_cubic_divisible :
  forall p A B u : Z,
    (p | F28_discriminant A B) ->
    (p | F28_root_denominator A*u-1) ->
    (p | F28_cubic A B
       (F28_candidate_root B u)).
Proof.
  intros p A B u HD Hinv.
  rewrite F28_candidate_cubic_identity.

  apply F28_divide_difference.
  - replace (B*u^3*F28_discriminant A B)
      with (F28_discriminant A B*(B*u^3))
      by ring.
    apply F28_divide_product.
    exact HD.
  - apply F28_divide_product.
    exact Hinv.
Qed.

(* ======================================== *)
(* GENERAL SINGULAR ROOT THEOREM            *)
(* ======================================== *)

Theorem F28_discriminant_gives_singular_root :
  forall p A B : Z,
    prime p ->
    5 <= p ->
    (p | F28_discriminant A B) ->
    ~ (p | A) ->
    exists r : Z,
      (p | F28_cubic A B r) /\
      (p | F28_derivative A r).
Proof.
  intros p A B Hp Hlarge HD HnotA.

  assert (Hden :
    ~ (p | F28_root_denominator A)).
  {
    unfold F28_root_denominator.
    apply (F28_nonzero_product p 2 A).
    - exact Hp.
    - apply (F28_large_prime_not_divide_two p).
      + exact Hp.
      + exact Hlarge.
    - exact HnotA.
  }

  destruct
    (F28_prime_inverse p
       (F28_root_denominator A)
       Hp Hden)
    as [u Hinv].

  exists (F28_candidate_root B u).

  split.
  - apply F28_candidate_cubic_divisible.
    + exact HD.
    + exact Hinv.
  - apply F28_candidate_derivative_divisible.
    + exact HD.
    + exact Hinv.
Qed.

(* ======================================== *)
(* MAIN SPECIALIZATION THEOREM              *)
(* ======================================== *)

Theorem F28_specialized_singular_root :
  forall p a b c : Z,
    prime p ->
    5 <= p ->
    (p | F28_F a b c) ->
    ~ (p | a) ->
    ~ (p | c) ->
    exists r : Z,
      (p | F28_cubic
         (F28_A a c) (F28_B b c) r)
      /\
      (p | F28_derivative
         (F28_A a c) r).
Proof.
  intros p a b c Hp Hlarge HF HnotA HnotC.

  apply F28_discriminant_gives_singular_root.
  - exact Hp.
  - exact Hlarge.
  - apply F28_F_divides_discriminant.
    exact HF.
  - apply F28_specialized_A_nonzero.
    + exact Hp.
    + exact Hlarge.
    + exact HnotA.
    + exact HnotC.
Qed.

(* ======================================== *)
(* FINAL VERIFICATION                       *)
(* ======================================== *)

Check F28_specialized_singular_root.

Print Assumptions F28_specialized_singular_root.

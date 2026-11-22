(* code/coq/F28_family_specialization.v

   The owner's twenty-ninth Coq file (22 November 2026).  The text is the owner's, with ONE change: the four imports "From Stdlib Require Import ..." are written
   "From Coq Require Import ..." (CI compiles with Coq 8.20.1, which has no Stdlib prefix).  Plus this header.  Standalone.
   Specialization of the discriminant machinery to the paper's integral model A = 4 a c^3, B = -8 b c^5, F = 4 a^3 + 27 b^2 c.  WHAT IT PROVES (checked by hand):
     F28_specialized_discriminant_identity: -4 A^3 - 27 B^2 = -256 a^3 c^9 - 1728 b^2 c^10 = -64 c^9 F;
     F28_F_divides_discriminant: p | F ==> p | -4 A^3 - 27 B^2;
     F28_specialized_A_nonzero: prime p >= 5, p not dividing a, c ==> p not dividing A = 4 a c^3 (p does not divide 4 = 2*2, nor c^3).
   This is the hypothesis package that F28_discriminant_gives_singular_root (F28_discriminant_singular_root.v) and F28_discriminant_split_criterion
   (F28_large_prime_tangent.v) need for the paper's model; the identity F28_specialized_discriminant_identity coincides with my F28_integral_discriminant_identity
   (F28_discriminant_root.v).  p not dividing a, c itself comes from F28_main_arithmetic (F28_arithmetic.v).  WHAT IT DOES NOT PROVE: one closed theorem
   "paper's model, p | F  ==>  integer double root" combining the files (they are standalone and do not import each other). *)

From Coq Require Import ZArith.
From Coq Require Import Znumtheory.
From Coq Require Import Ring.
From Coq Require Import Lia.

Open Scope Z_scope.

(* ======================================== *)
(* F.28: SPECIALIZATION TO THE FAMILY       *)
(* ======================================== *)

Definition F28_A (a c : Z) : Z :=
  4*a*c^3.

Definition F28_B (b c : Z) : Z :=
  -8*b*c^5.

Definition F28_F (a b c : Z) : Z :=
  4*a^3 + 27*b^2*c.

Definition F28_discriminant (A B : Z) : Z :=
  -4*A^3 - 27*B^2.

(* ======================================== *)
(* EXACT DISCRIMINANT IDENTITY              *)
(* ======================================== *)

Theorem F28_specialized_discriminant_identity :
  forall a b c : Z,
    F28_discriminant (F28_A a c) (F28_B b c) =
    -64*c^9*F28_F a b c.
Proof.
  intros a b c.
  unfold F28_discriminant,
    F28_A, F28_B, F28_F.
  ring.
Qed.

(* ======================================== *)
(* DIVISIBILITY                             *)
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
(* DISCRIMINANT DIVISIBILITY                *)
(* ======================================== *)

Theorem F28_F_divides_discriminant :
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
(* LARGE PRIME DOES NOT DIVIDE 2           *)
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

(* ======================================== *)
(* LARGE PRIME DOES NOT DIVIDE 4           *)
(* ======================================== *)

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

(* ======================================== *)
(* NONDIVISIBILITY OF c^3                   *)
(* ======================================== *)

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
(* NONDIVISIBILITY OF 4ac^3                 *)
(* ======================================== *)

Theorem F28_specialized_A_nonzero :
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
(* FINAL CHECKS                             *)
(* ======================================== *)

Check F28_specialized_discriminant_identity.
Check F28_F_divides_discriminant.
Check F28_nonzero_cube.
Check F28_specialized_A_nonzero.

Print Assumptions F28_specialized_A_nonzero.

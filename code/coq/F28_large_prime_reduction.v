(* code/coq/F28_large_prime_reduction.v

   The owner's forty-sixth Coq file (22 November 2026).  The text is the owner's, with ONE change: the import "From Stdlib Require Import ZArith Znumtheory Ring Lia." is written
   "From Coq Require Import ZArith Znumtheory Ring Lia." (CI compiles with Coq 8.20.1, which has no Stdlib prefix).  Plus this header.  Standalone.
   For the integral model Y^2 = X^3 + A X + B, A = 4 a c^3, B = -8 b c^5, F = 4 a^3 + 27 b^2 c, c4 = -48 A, c6 = -864 B, Delta = -16 (4 A^3 + 27 B^2):
     F28_not_divide_small: 0 < n < p ==> p not dividing n (case split on the cofactor; checked by hand);  F28_prime_192_nonzero: prime p >= 5 does not divide 192 = 2^6 * 3;
     c4 = -192 a c^3, c6 = 6912 b c^5, Delta = -1024 c^9 F (ring);
     F28_large_prime_c4_nonzero: prime p >= 5, p not dividing a, c ==> p not dividing c4 = -192 a c^3;
     F28_large_prime_reduction_certificate: prime p >= 5, p not dividing a, c, p | F ==> p | Delta and p not dividing c4  (the numerical criterion for multiplicative reduction).
   This discharges, in one theorem and with the hypothesis p not dividing a, c (F28_main_arithmetic for a primitive triple), the conditional statement that the 45th file left as an assumption on -192 a c^3;
   it duplicates F28_integral_model_conditions (F28_arithmetic.v) and F28_primitive_reduction_conditions (15th file).  The identification of "p | Delta, p not dividing c4" with multiplicative reduction
   (and minimality of the model at p) is Silverman VII.1.1 / Tate, not in Coq. *)

From Coq Require Import ZArith Znumtheory Ring Lia.

Open Scope Z_scope.

(* ============================================= *)
(* F.28: INVARIANT AND REDUCTION CERTIFICATE     *)
(* ============================================= *)

Definition F28_F (a b c : Z) : Z :=
  4*a^3 + 27*b^2*c.

Definition F28_A (a c : Z) : Z :=
  4*a*c^3.

Definition F28_B (b c : Z) : Z :=
  -8*b*c^5.

Definition F28_c4 (A : Z) : Z :=
  -48*A.

Definition F28_c6 (B : Z) : Z :=
  -864*B.

Definition F28_discriminant (A B : Z) : Z :=
  -16*(4*A^3 + 27*B^2).

Definition F28_invariant_certificate
  (p A B : Z) : Prop :=
  (p | F28_discriminant A B) /\
  ~ (p | F28_c4 A).

(* ============================================= *)
(* BASIC DIVISIBILITY                            *)
(* ============================================= *)

Lemma F28_not_divide_small :
  forall p n : Z,
    0 < n ->
    n < p ->
    ~ (p | n).
Proof.
  intros p n Hpos Hbound Hdiv.
  destruct Hdiv as [k Hk].
  destruct (Z_lt_ge_dec k 0) as [Hneg | Hnonneg].
  - nia.
  - destruct (Z.eq_dec k 0) as [Hzero | Hnonzero].
    + subst k.
      nia.
    + assert (Hpositive : 1 <= k) by lia.
      nia.
Qed.

Lemma F28_prime_product_nonzero :
  forall p x y : Z,
    prime p ->
    ~ (p | x) ->
    ~ (p | y) ->
    ~ (p | x*y).
Proof.
  intros p x y Hp Hx Hy Hxy.
  apply prime_mult in Hxy; [|exact Hp].
  destruct Hxy as [Hleft | Hright].
  - exact (Hx Hleft).
  - exact (Hy Hright).
Qed.

Lemma F28_prime_square_nonzero :
  forall p x : Z,
    prime p ->
    ~ (p | x) ->
    ~ (p | x*x).
Proof.
  intros p x Hp Hx.
  apply F28_prime_product_nonzero.
  - exact Hp.
  - exact Hx.
  - exact Hx.
Qed.

Lemma F28_prime_cube_nonzero :
  forall p x : Z,
    prime p ->
    ~ (p | x) ->
    ~ (p | x^3).
Proof.
  intros p x Hp Hx.
  replace (x^3) with (x*(x*x)) by ring.
  apply F28_prime_product_nonzero.
  - exact Hp.
  - exact Hx.
  - apply F28_prime_square_nonzero.
    + exact Hp.
    + exact Hx.
Qed.

(* ============================================= *)
(* PRIME p >= 5 DOES NOT DIVIDE 192              *)
(* ============================================= *)

Lemma F28_prime_192_nonzero :
  forall p : Z,
    prime p ->
    5 <= p ->
    ~ (p | 192).
Proof.
  intros p Hp Hlarge.

  assert (H2 : ~ (p | 2)).
  {
    apply F28_not_divide_small; lia.
  }

  assert (H3 : ~ (p | 3)).
  {
    apply F28_not_divide_small; lia.
  }

  replace 192 with
    (2*(2*(2*(2*(2*(2*3)))))) by ring.

  repeat
    (apply F28_prime_product_nonzero;
      [exact Hp | exact H2 |]).

  exact H3.
Qed.

(* ============================================= *)
(* EXACT INVARIANT IDENTITIES                    *)
(* ============================================= *)

Theorem F28_c4_identity :
  forall a c : Z,
    F28_c4 (F28_A a c) = -192*a*c^3.
Proof.
  intros a c.
  unfold F28_c4, F28_A.
  ring.
Qed.

Theorem F28_c6_identity :
  forall b c : Z,
    F28_c6 (F28_B b c) = 6912*b*c^5.
Proof.
  intros b c.
  unfold F28_c6, F28_B.
  ring.
Qed.

Theorem F28_discriminant_identity :
  forall a b c : Z,
    F28_discriminant
      (F28_A a c) (F28_B b c) =
    -1024*c^9*F28_F a b c.
Proof.
  intros a b c.
  unfold F28_discriminant, F28_A, F28_B, F28_F.
  ring.
Qed.

(* ============================================= *)
(* NONDIVISIBILITY OF c4                         *)
(* ============================================= *)

Theorem F28_large_prime_c4_nonzero :
  forall p a c : Z,
    prime p ->
    5 <= p ->
    ~ (p | a) ->
    ~ (p | c) ->
    ~ (p | F28_c4 (F28_A a c)).
Proof.
  intros p a c Hp Hlarge Ha Hc.

  rewrite F28_c4_identity.

  replace (-192*a*c^3)
    with ((-192)*(a*c^3)) by ring.

  apply F28_prime_product_nonzero.
  - exact Hp.
  - intro Hneg.
    apply (F28_prime_192_nonzero p Hp Hlarge).
    destruct Hneg as [k Hk].
    exists (-k).
    nia.
  - apply F28_prime_product_nonzero.
    + exact Hp.
    + exact Ha.
    + apply F28_prime_cube_nonzero.
      * exact Hp.
      * exact Hc.
Qed.

(* ============================================= *)
(* DISCRIMINANT DIVISIBILITY                     *)
(* ============================================= *)

Theorem F28_F_divides_discriminant :
  forall p a b c : Z,
    (p | F28_F a b c) ->
    (p | F28_discriminant
           (F28_A a c) (F28_B b c)).
Proof.
  intros p a b c HF.
  rewrite F28_discriminant_identity.
  destruct HF as [k Hk].
  exists ((-1024*c^9)*k).
  rewrite Hk.
  ring.
Qed.

(* ============================================= *)
(* FINAL INVARIANT CERTIFICATE                   *)
(* ============================================= *)

Theorem F28_large_prime_reduction_certificate :
  forall p a b c : Z,
    prime p ->
    5 <= p ->
    ~ (p | a) ->
    ~ (p | c) ->
    (p | F28_F a b c) ->
    F28_invariant_certificate
      p (F28_A a c) (F28_B b c).
Proof.
  intros p a b c Hp Hlarge Ha Hc HF.
  unfold F28_invariant_certificate.
  split.
  - apply F28_F_divides_discriminant.
    exact HF.
  - apply F28_large_prime_c4_nonzero.
    + exact Hp.
    + exact Hlarge.
    + exact Ha.
    + exact Hc.
Qed.

(* ============================================= *)
(* FINAL CHECKS                                  *)
(* ============================================= *)

Check F28_not_divide_small.
Check F28_prime_product_nonzero.
Check F28_prime_square_nonzero.
Check F28_prime_cube_nonzero.
Check F28_prime_192_nonzero.

Check F28_c4_identity.
Check F28_c6_identity.
Check F28_discriminant_identity.

Check F28_large_prime_c4_nonzero.
Check F28_F_divides_discriminant.
Check F28_large_prime_reduction_certificate.

Print Assumptions F28_large_prime_reduction_certificate.

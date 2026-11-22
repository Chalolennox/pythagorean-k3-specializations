(* code/coq/F28_stage4_certificate.v

   The owner's forty-seventh Coq file ("F.28 - Stage 4", 22 November 2026).  The text is the owner's, with ONE change: the import "From Stdlib Require Import ZArith Znumtheory Ring Lia." is written
   "From Coq Require Import ZArith Znumtheory Ring Lia." (CI compiles with Coq 8.20.1, which has no Stdlib prefix).  Plus this header.  Standalone; it contains the 46th file and the tangent files.
   F28_stage4_certificate: prime p >= 5, p not dividing a, c, p | F = 4 a^3 + 27 b^2 c, and p | f'(r) = 3 r^2 + A for A = 4 a c^3 ==> ALL of:
     (i) the invariant certificate: p | Delta = -16(4A^3 + 27B^2) and p not dividing c4 = -48 A  (A = 4ac^3, B = -8bc^5);
     (ii) p not dividing r;  (iii) p not dividing 3 r;  (iv) p not dividing the tangent cone v^2 - 3 r u^2 at (1, 0).
   Read by hand: (i) is F28_large_prime_reduction_certificate; p not dividing A follows because p | A would give p | c4 = -48 A, contradicting F28_large_prime_c4_nonzero; (ii)-(iv) are
   F28_nondegenerate_singular_root (A = (3 r^2 + A) + (-(3 r^2)); prime_mult with p not dividing 3).  Note that f(r) = 0 mod p is not used: only f'(r) = 0 mod p (a double root of the cubic is a root of f' and,
   when p | Delta, also of f).
   WHAT IT DOES NOT PROVE: that such an r exists (F28_complete_arithmetic_bridge.v, F28_specialized_singular_root.v), nor the class relation (40th file), nor the Tate/Silverman identification of
   (p | Delta, p not dividing c4) with multiplicative reduction, minimality; the files are standalone and not composed. *)

From Coq Require Import ZArith Znumtheory Ring Lia.

Open Scope Z_scope.

(* ============================================= *)
(* F.28 - STAGE 4                               *)
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

Definition F28_derivative (A x : Z) : Z :=
  3*x^2 + A.

Definition F28_tangent_cone (r u v : Z) : Z :=
  v^2 - 3*r*u^2.

(* ============================================= *)
(* ARITHMETIC FOUNDATION                       *)
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
(* SINGULAR ROOT CERTIFICATE                   *)
(* ============================================= *)

Lemma F28_divide_add :
  forall p x y : Z,
    (p | x) ->
    (p | y) ->
    (p | x+y).
Proof.
  intros p x y Hx Hy.
  destruct Hx as [kx Hkx].
  destruct Hy as [ky Hky].
  exists (kx+ky).
  rewrite Hkx, Hky.
  ring.
Qed.

Lemma F28_divide_neg :
  forall p x : Z,
    (p | x) ->
    (p | -x).
Proof.
  intros p x Hx.
  destruct Hx as [k Hk].
  exists (-k).
  rewrite Hk.
  ring.
Qed.

Lemma F28_divide_mul :
  forall p x y : Z,
    (p | x) ->
    (p | x*y).
Proof.
  intros p x y Hx.
  destruct Hx as [k Hk].
  exists (k*y).
  rewrite Hk.
  ring.
Qed.

Theorem F28_singular_root_nonzero :
  forall p A r : Z,
    ~ (p | A) ->
    (p | F28_derivative A r) ->
    ~ (p | r).
Proof.
  intros p A r HA Hder Hr.
  unfold F28_derivative in Hder.

  assert (Hrr : (p | r*r)).
  {
    apply F28_divide_mul.
    exact Hr.
  }

  assert (Hthree : (p | 3*r^2)).
  {
    replace (3*r^2) with ((r*r)*3) by ring.
    exact (F28_divide_mul p (r*r) 3 Hrr).
  }

  assert (Hnegative : (p | -(3*r^2))).
  {
    apply F28_divide_neg.
    exact Hthree.
  }

  apply HA.
  replace A with ((3*r^2+A)+(-(3*r^2))) by ring.
  apply F28_divide_add.
  - exact Hder.
  - exact Hnegative.
Qed.

Theorem F28_three_root_nonzero :
  forall p A r : Z,
    prime p ->
    5 <= p ->
    ~ (p | A) ->
    (p | F28_derivative A r) ->
    ~ (p | 3*r).
Proof.
  intros p A r Hp Hlarge HA Hder Hthree.

  assert (H3 : ~ (p | 3)).
  {
    apply F28_not_divide_small; lia.
  }

  assert (Hr : ~ (p | r)).
  {
    exact (F28_singular_root_nonzero p A r HA Hder).
  }

  exact
    (F28_prime_product_nonzero
       p 3 r Hp H3 Hr Hthree).
Qed.

Theorem F28_tangent_coefficient_identity :
  forall r : Z,
    F28_tangent_cone r 1 0 = -(3*r).
Proof.
  intro r.
  unfold F28_tangent_cone.
  ring.
Qed.

Theorem F28_tangent_coefficient_nonzero :
  forall p r : Z,
    ~ (p | 3*r) ->
    ~ (p | F28_tangent_cone r 1 0).
Proof.
  intros p r Hnonzero Hdiv.
  rewrite F28_tangent_coefficient_identity in Hdiv.
  apply Hnonzero.
  replace (3*r) with (-(-(3*r))) by ring.
  apply F28_divide_neg.
  exact Hdiv.
Qed.

Theorem F28_nondegenerate_singular_root :
  forall p A r : Z,
    prime p ->
    5 <= p ->
    ~ (p | A) ->
    (p | F28_derivative A r) ->
    ~ (p | r) /\
    ~ (p | 3*r) /\
    ~ (p | F28_tangent_cone r 1 0).
Proof.
  intros p A r Hp Hlarge HA Hder.

  assert (Hr : ~ (p | r)).
  {
    exact (F28_singular_root_nonzero p A r HA Hder).
  }

  assert (Hthree : ~ (p | 3*r)).
  {
    exact
      (F28_three_root_nonzero
         p A r Hp Hlarge HA Hder).
  }

  split.
  - exact Hr.
  - split.
    + exact Hthree.
    + exact
        (F28_tangent_coefficient_nonzero
           p r Hthree).
Qed.

(* ============================================= *)
(* COMPLETE STAGE 4 CERTIFICATE                 *)
(* ============================================= *)

Theorem F28_stage4_certificate :
  forall p a b c r : Z,
    prime p ->
    5 <= p ->
    ~ (p | a) ->
    ~ (p | c) ->
    (p | F28_F a b c) ->
    (p | F28_derivative (F28_A a c) r) ->
    F28_invariant_certificate
      p (F28_A a c) (F28_B b c)
    /\
    ~ (p | r)
    /\
    ~ (p | 3*r)
    /\
    ~ (p | F28_tangent_cone r 1 0).
Proof.
  intros p a b c r Hp Hlarge Ha Hc HF Hder.

  assert (Hinv :
    F28_invariant_certificate
      p (F28_A a c) (F28_B b c)).
  {
    exact
      (F28_large_prime_reduction_certificate
         p a b c Hp Hlarge Ha Hc HF).
  }

  assert (HA : ~ (p | F28_A a c)).
  {
    intro Hbad.

    assert (Hc4 : (p | F28_c4 (F28_A a c))).
    {
      unfold F28_c4.
      replace (-48*F28_A a c)
        with (F28_A a c*(-48)) by ring.
      apply F28_divide_mul.
      exact Hbad.
    }

    exact
      (F28_large_prime_c4_nonzero
         p a c Hp Hlarge Ha Hc Hc4).
  }

  pose proof
    (F28_nondegenerate_singular_root
       p (F28_A a c) r Hp Hlarge HA Hder)
    as Hnode.

  destruct Hnode as [Hr [Hthree Htangent]].

  split.
  - exact Hinv.
  - split.
    + exact Hr.
    + split.
      * exact Hthree.
      * exact Htangent.
Qed.

(* ============================================= *)
(* CI CHECKS                                    *)
(* ============================================= *)

Check F28_large_prime_reduction_certificate.
Check F28_singular_root_nonzero.
Check F28_three_root_nonzero.
Check F28_tangent_coefficient_nonzero.
Check F28_nondegenerate_singular_root.
Check F28_stage4_certificate.

Print Assumptions F28_stage4_certificate.

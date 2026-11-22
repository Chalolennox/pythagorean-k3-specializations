(* code/coq/F28_stage8_factorization.v

   The owner's fifty-second Coq file ("Stage 8: factorization certificate", 22 November 2026).  The text is the owner's, with ONE change: the import "From Stdlib Require Import ZArith Znumtheory Ring Lia." is written
   "From Coq Require Import ZArith Znumtheory Ring Lia." (CI compiles with Coq 8.20.1, which has no Stdlib prefix).  Plus this header.  Standalone.  (The owner's "Stage 8" is this file; my own file F28_stage8a_reduced_model.v, "8a", is a different file.)
   DEFINITIONS: F28_factor r x := (x - r)^2 (x + 2 r);  F28_factorization_certificate p A B r := (for all x, p | f(x) - factor_r(x)) and p | f(r) and p | f'(r) and p not dividing r - (-2r) and p | f(-2r) and p not dividing f'(-2r) and p not dividing the tangent cone at (1,0).
   WHAT IT PROVES (read by hand), for ANY integers A, B, any prime p, any r with p | f(r), p | f'(r) (f = x^3 + A x + B) and p not dividing 3 r  (no p >= 5, no a, b, c hypothesis needed):
     F28_factor_expansion: (x - r)^2 (x + 2r) = x^3 - 3 r^2 x + 2 r^3;  F28_factor_difference: f(x) - factor_r(x) = f'(r) (x - r) + f(r)  (both ring; checked by hand: the x-coefficient and constant term agree);
     F28_singular_factorization: p | f(x) - factor_r(x) for every integer x (the right side is divisible by p termwise);  so f is congruent mod p to (x - r)^2 (x + 2r);
     F28_second_root_on_cubic: p | f(-2r);  F28_distinct_roots_mod_p: r - (-2r) = 3 r, so the roots r and -2r are distinct mod p;
     F28_simple_root_derivative_nonzero: p not dividing f'(-2r)  (f'(-2r) - f'(r) = 9 r^2 = (3r)(3r), and p does not divide (3r)(3r));  F28_tangent_nonzero: the tangent cone v^2 - 3 r u^2 at (1,0) is nonzero (it is -3r);
     F28_local_equation_identity: v^2 - f(r+u) = (v^2 - 3 r u^2) - u^3 - f(r) - f'(r) u (ring);  F28_stage8_factorization / F28_stage8_family_certificate: the certificate, and its instance for A = 4 a c^3, B = -8 b c^5.
   WHY IT MATTERS: for a double root r with p not dividing 3r the reduced cubic is (x - r)^2 (x + 2r) with a simple second root -2r: a nodal cubic in the sense of the factorization, with nondegenerate tangent cone.
   WHAT IT DOES NOT PROVE: the existence of r (F28_complete_arithmetic_bridge.v / F28_stage8a_reduced_model.v), that p not dividing 3r holds for the model (F28_stage7_nodal_reduction.v: p >= 5, p not dividing a, c), the split/nonsplit class (F28_unconditional_bridge.v), the identification
   with split multiplicative reduction over Q_p (Tate/Silverman), minimality over Q_p, the local root number (Rohrlich).  Composition with the other standalone files is held until the owner says so. *)

From Coq Require Import ZArith Znumtheory Ring Lia.
Open Scope Z_scope.

Definition F28_A (a c : Z) : Z := 4*a*c^3.
Definition F28_B (b c : Z) : Z := -8*b*c^5.
Definition F28_cubic (A B x : Z) : Z := x^3 + A*x + B.
Definition F28_derivative (A x : Z) : Z := 3*x^2 + A.
Definition F28_factor (r x : Z) : Z := (x-r)^2*(x+2*r).
Definition F28_tangent_cone (r u v : Z) : Z := v^2 - 3*r*u^2.

Theorem F28_factor_expansion :
  forall r x : Z, F28_factor r x = x^3 - 3*r^2*x + 2*r^3.
Proof.
  intros r x. unfold F28_factor. ring.
Qed.

Theorem F28_factor_difference :
  forall A B r x : Z,
    F28_cubic A B x - F28_factor r x =
    F28_derivative A r*(x-r) + F28_cubic A B r.
Proof.
  intros A B r x.
  unfold F28_cubic, F28_derivative, F28_factor. ring.
Qed.

Theorem F28_double_root_factor :
  forall r : Z, F28_factor r r = 0.
Proof.
  intro r. unfold F28_factor. ring.
Qed.

Theorem F28_simple_root_factor :
  forall r : Z, F28_factor r (-2*r) = 0.
Proof.
  intro r. unfold F28_factor. ring.
Qed.

Theorem F28_root_difference :
  forall r : Z, r - (-2*r) = 3*r.
Proof.
  intro r. ring.
Qed.

Theorem F28_derivative_difference :
  forall A r : Z,
    F28_derivative A (-2*r) - F28_derivative A r = (3*r)*(3*r).
Proof.
  intros A r. unfold F28_derivative. ring.
Qed.

Lemma F28_divide_neg :
  forall p x : Z, (p | x) -> (p | -x).
Proof.
  intros p x H. destruct H as [k Hk].
  exists (-k). rewrite Hk. ring.
Qed.

Lemma F28_prime_product_nonzero :
  forall p x y : Z,
    prime p -> ~ (p | x) -> ~ (p | y) -> ~ (p | x*y).
Proof.
  intros p x y Hp Hx Hy Hxy.
  apply prime_mult in Hxy; [|exact Hp].
  destruct Hxy as [Hleft | Hright].
  - exact (Hx Hleft).
  - exact (Hy Hright).
Qed.

Theorem F28_singular_factorization :
  forall p A B r x : Z,
    (p | F28_cubic A B r) ->
    (p | F28_derivative A r) ->
    (p | F28_cubic A B x - F28_factor r x).
Proof.
  intros p A B r x Hf Hd.
  destruct Hf as [kf Hkf].
  destruct Hd as [kd Hkd].
  rewrite F28_factor_difference.
  exists (kd*(x-r)+kf).
  rewrite Hkd, Hkf. ring.
Qed.

Theorem F28_second_root_on_cubic :
  forall p A B r : Z,
    (p | F28_cubic A B r) ->
    (p | F28_derivative A r) ->
    (p | F28_cubic A B (-2*r)).
Proof.
  intros p A B r Hf Hd.
  pose proof (F28_singular_factorization p A B r (-2*r) Hf Hd)
    as Hfactor.
  rewrite F28_simple_root_factor in Hfactor.
  replace (F28_cubic A B (-2*r)-0)
    with (F28_cubic A B (-2*r)) in Hfactor by ring.
  exact Hfactor.
Qed.

Theorem F28_distinct_roots_mod_p :
  forall p r : Z, ~ (p | 3*r) -> ~ (p | r-(-2*r)).
Proof.
  intros p r Hthree.
  rewrite F28_root_difference. exact Hthree.
Qed.

Theorem F28_simple_root_derivative_nonzero :
  forall p A r : Z,
    prime p ->
    ~ (p | 3*r) ->
    (p | F28_derivative A r) ->
    ~ (p | F28_derivative A (-2*r)).
Proof.
  intros p A r Hp Hthree Hd Hbad.
  destruct Hd as [kd Hkd].
  destruct Hbad as [ks Hks].
  assert (Hsquare : (p | (3*r)*(3*r))).
  {
    exists (ks-kd).
    rewrite <- (F28_derivative_difference A r).
    rewrite Hks, Hkd. ring.
  }
  assert (Hnot : ~ (p | (3*r)*(3*r))).
  {
    apply F28_prime_product_nonzero.
    - exact Hp.
    - exact Hthree.
    - exact Hthree.
  }
  exact (Hnot Hsquare).
Qed.

Theorem F28_tangent_coefficient_identity :
  forall r : Z, F28_tangent_cone r 1 0 = -(3*r).
Proof.
  intro r. unfold F28_tangent_cone. ring.
Qed.

Theorem F28_tangent_nonzero :
  forall p r : Z,
    ~ (p | 3*r) -> ~ (p | F28_tangent_cone r 1 0).
Proof.
  intros p r Hthree Hbad.
  rewrite F28_tangent_coefficient_identity in Hbad.
  apply Hthree.
  replace (3*r) with (-(-(3*r))) by ring.
  apply F28_divide_neg. exact Hbad.
Qed.

Theorem F28_local_equation_identity :
  forall A B r u v : Z,
    v^2 - F28_cubic A B (r+u) =
    F28_tangent_cone r u v - u^3 -
    F28_cubic A B r - F28_derivative A r*u.
Proof.
  intros A B r u v.
  unfold F28_tangent_cone, F28_cubic, F28_derivative.
  ring.
Qed.

Definition F28_factorization_certificate (p A B r : Z) : Prop :=
  (forall x : Z, (p | F28_cubic A B x - F28_factor r x)) /\
  (p | F28_cubic A B r) /\
  (p | F28_derivative A r) /\
  ~ (p | r-(-2*r)) /\
  (p | F28_cubic A B (-2*r)) /\
  ~ (p | F28_derivative A (-2*r)) /\
  ~ (p | F28_tangent_cone r 1 0).

Theorem F28_stage8_factorization :
  forall p A B r : Z,
    prime p ->
    ~ (p | 3*r) ->
    (p | F28_cubic A B r) ->
    (p | F28_derivative A r) ->
    F28_factorization_certificate p A B r.
Proof.
  intros p A B r Hp Hthree Hf Hd.
  unfold F28_factorization_certificate.
  repeat split.
  - intro x.
    exact (F28_singular_factorization p A B r x Hf Hd).
  - exact Hf.
  - exact Hd.
  - exact (F28_distinct_roots_mod_p p r Hthree).
  - exact (F28_second_root_on_cubic p A B r Hf Hd).
  - exact (F28_simple_root_derivative_nonzero p A r Hp Hthree Hd).
  - exact (F28_tangent_nonzero p r Hthree).
Qed.

Theorem F28_stage8_family_certificate :
  forall p a b c r : Z,
    prime p ->
    ~ (p | 3*r) ->
    (p | F28_cubic (F28_A a c) (F28_B b c) r) ->
    (p | F28_derivative (F28_A a c) r) ->
    F28_factorization_certificate
      p (F28_A a c) (F28_B b c) r.
Proof.
  intros p a b c r Hp Hthree Hf Hd.
  exact (F28_stage8_factorization
           p (F28_A a c) (F28_B b c) r Hp Hthree Hf Hd).
Qed.

Check F28_factor_expansion.
Check F28_factor_difference.
Check F28_singular_factorization.
Check F28_second_root_on_cubic.
Check F28_distinct_roots_mod_p.
Check F28_simple_root_derivative_nonzero.
Check F28_tangent_nonzero.
Check F28_local_equation_identity.
Check F28_stage8_factorization.
Check F28_stage8_family_certificate.
Print Assumptions F28_stage8_factorization.
Print Assumptions F28_stage8_family_certificate.

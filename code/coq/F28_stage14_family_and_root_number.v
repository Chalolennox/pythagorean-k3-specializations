(* code/coq/F28_stage14_family_and_root_number.v

   STAGE 14.  NOT an owner file: written in review by Claude (a language model; no human check), at the owner's request ("finish all doable items and just leave what is outside of the scope of coq").  Standalone.  Compiled only by CI (Coq 8.20.1); read by hand beforehand, no local Coq.
   HOW IT IS BUILT: (1) the whole text of the Stage 13 file (F28_stage13_multiplicative_reduction.v), unchanged, its closing Check/Print lines dropped; (2) a section "NEW IN STAGE 14" which is mine.  The 21st file (F28_large_prime_tangent.v) is NOT reused: its statement (864 B square iff 3 r square) is re-proved here from the Stage 13 lemmas, in the form needed for the model.
   WHAT THE NEW SECTION PROVES:
     14.1  F28_minus_c6 B := 864 B (= -c6, F28_minus_c6_is_minus_c6).  F28_certificate_congruence / F28_certificate_scaling: squareness of x mod p is invariant under x -> y with p | x - y, and under x -> x w^2 with p not dividing w.
       F28_minus_c6_vs_three_r: at a double root r of f mod p (p | f(r), p | f'(r), p not dividing 3r), B = 2 r^3, 864 B = (3 r)(24 r)^2, hence -c6 square iff 3 r square.
       F28_model_minus_c6_criterion: for the model, F28_square_certificate p (-c6) iff F28_square_certificate p (a b).  F28_model_split_iff_minus_c6: split multiplicative iff -c6 square mod p; nonsplit iff not.  (The paper's step (d).)
     14.2  The Pythagorean family.  F28_F_paper U V = U^6 - 30 U^4 V^2 - 24 U^2 V^4 - V^6.  F28_family d U V a b c := (d a = V^2 - U^2, d b = 2 U V, d c = U^2 + V^2).
       F28_family_normalization: d^3 * F28_F a b c = -4 * F28_F_paper U V  (the normalization lemma: the paper's F and the primitive-triple F differ by this factor; for d = 1, the unreduced triple, Delta = 2^12 c0^9 F_paper).
       F28_family_pythagorean: d nonzero gives a^2 + b^2 = c^2.   F28_family_primitive_at_p: p >= 5 not dividing both U and V does not divide both a and b.
       F28_pythagorean_large_prime: p >= 5, p | F28_F, a^2 + b^2 = c^2, (a, b) not both divisible by p, then p divides none of a, b, c  (the paper's step (a)).
       F28_divides_F_iff: for d in {1, 2} and p >= 5: p | F28_F a b c iff p | F28_F_paper U V.
       F28_F_paper_nonzero: F_paper U V is nonzero when U, V are not both even (parity: F_paper is odd if exactly one of U, V is odd, and = 2 mod 4 if both are odd); F28_family_F_nonzero: F28_F a b c is nonzero.
       F28_family_hypotheses: from p | F_paper(U, V) (p >= 5), U, V not both divisible by 2 or by p, d in {1, 2}: p | F28_F, F28_F nonzero, p divides none of a, b, c.  So the hypotheses of all earlier stages are DERIVED for the family.
     14.3  Weierstrass change of coordinates.  F28_W_b2 ... F28_W_disc: the invariants b2, b4, b6, b8, c4, c6, Delta of an integral Weierstrass equation (Silverman III.1).  F28_W_short_model: for a1 = a2 = a3 = 0 they are -48 A, -864 B, -16 (4 A^3 + 27 B^2).
       F28_W_disc_identity: 1728 Delta = c4^3 - c6^2.  F28_W_change_of_coordinates: for x = u^2 x' + r, y = u^3 y' + s u^2 x' + t with u = m/n, r = R/n^2, s = S/n, t = T/n^3 (denominators cleared; the standard formulas a_i' u^i = ... times n^i),
       m^4 c4' = n^4 c4, m^6 c6' = n^6 c6, m^12 Delta' = n^12 Delta.
     14.4  F28_valuation_discriminant: p not dividing C, n^4 C = m^4 C', n^12 D = m^12 D', m nonzero: every power of p dividing D divides D' (v_p(D') >= v_p(D)).  F28_minimal_discriminant: for y^2 = x^3 + A x + B with p not dividing c4 = -48 A and ANY integral Weierstrass model related by such a change of
       coordinates, every power of p dividing Delta(A, B) divides Delta'.  F28_model_minimal_discriminant: the same for the model of the family.  This is the statement that the model has minimal discriminant at p (and F28_scaling_minimal of Stage 13 is its c4 form).
     14.5  F28_rohrlich_split_hypothesis w / F28_rohrlich_nonsplit_hypothesis w: the root-number theorem (-1 for split, +1 for nonsplit multiplicative reduction) as an EXPLICIT HYPOTHESIS on an arbitrary function w p A B.  F28_root_number_conditional: under them, w = -1 if a b is a square class mod p (equivalently -c6 is), w = +1 if not.
     14.6  F28_stage14_complete: the composed theorem for the family: from p | F_paper(U, V) (p >= 5), U and V not both even, not both divisible by p, d in {1, 2}: p | F, F nonzero, p does not divide a, b, c; p | Delta, Delta nonzero, p does not divide c4, multiplicative reduction; split iff ab square iff -c6 square;
       and, GIVEN the two Rohrlich hypotheses, w = -1 if ab is a square class and w = +1 if not.
   WHAT IT DOES NOT PROVE (outside the scope of Coq as set up here): ROHRLICH'S THEOREM ITSELF (the hypotheses of 14.5 are hypotheses, not theorems; there is no local root number, no epsilon-factor and no Q_p in this development);
   that F28_split_multiplicative / F28_nonsplit_multiplicative (Silverman's definition on integer representatives mod p) is "split / nonsplit multiplicative reduction over Q_p" in the sense of Tate's algorithm or the Neron model is the DEFINITION used, not derived;
   the factor f(t) of the root-number formula and the primes 2, 3 (the proofs need p >= 5), and the primes dividing c0 (the reduction there is not multiplicative of this form); the real place and the global product over all primes (W = product of local factors) and the statement W(E_t) = f(t) * prod_{p >= 5, p | F} (-(ab/p)) itself.
   Weierstrass change of coordinates are taken with the standard formulas as hypotheses (H1 ... H6 of F28_W_change_of_coordinates); that every integral model with the same j-invariant is obtained this way is not proved.  The divisibility form of v_p (F28_ppow p k | x) replaces the p-adic valuation. *)

From Coq Require Import
  ZArith Znumtheory Zgcd_alt Ring Lia.

Open Scope Z_scope.

(* ====================================================== *)
(* F.28 - STAGE 7                                        *)
(* ALGEBRAIC NODAL REDUCTION CERTIFICATE                 *)
(* Complete standalone development                       *)
(* ====================================================== *)

(* ------------------------------------------------------ *)
(* 1. CURVE AND INVARIANTS                               *)
(* ------------------------------------------------------ *)

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

Definition F28_cubic (A B r : Z) : Z :=
  r^3 + A*r + B.

Definition F28_derivative (A r : Z) : Z :=
  3*r^2 + A.

Definition F28_tangent_cone (r u v : Z) : Z :=
  v^2 - 3*r*u^2.

Definition F28_multiplicative_invariant_criterion
  (p A B : Z) : Prop :=
  (p | F28_discriminant A B) /\
  ~ (p | F28_c4 A).

Definition F28_ordinary_node
  (p A B r : Z) : Prop :=
  (p | F28_cubic A B r) /\
  (p | F28_derivative A r) /\
  ~ (p | 3*r).

Definition F28_nodal_reduction_certificate
  (p A B r : Z) : Prop :=
  F28_multiplicative_invariant_criterion p A B /\
  F28_ordinary_node p A B r.

(* ------------------------------------------------------ *)
(* 2. ELEMENTARY DIVISIBILITY                            *)
(* ------------------------------------------------------ *)

Lemma F28_divide_mul :
  forall p x y : Z,
    (p | x) -> (p | x*y).
Proof.
  intros p x y H.
  destruct H as [k Hk].
  exists (k*y).
  rewrite Hk.
  ring.
Qed.

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
    (p | x) -> (p | -x).
Proof.
  intros p x H.
  destruct H as [k Hk].
  exists (-k).
  rewrite Hk.
  ring.
Qed.

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
    + subst k. nia.
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

Lemma F28_prime_4_nonzero :
  forall p : Z,
    prime p ->
    5 <= p ->
    ~ (p | 4).
Proof.
  intros p Hp Hlarge.
  assert (H2 : ~ (p | 2)).
  {
    apply F28_not_divide_small; lia.
  }
  replace 4 with (2*2) by ring.
  apply F28_prime_product_nonzero.
  - exact Hp.
  - exact H2.
  - exact H2.
Qed.

Lemma F28_prime_3_nonzero :
  forall p : Z,
    5 <= p ->
    ~ (p | 3).
Proof.
  intros p Hlarge.
  apply F28_not_divide_small; lia.
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

(* ------------------------------------------------------ *)
(* 3. INVARIANT IDENTITIES                               *)
(* ------------------------------------------------------ *)

Theorem F28_c4_identity :
  forall a c : Z,
    F28_c4 (F28_A a c) =
    -192*a*c^3.
Proof.
  intros a c.
  unfold F28_c4, F28_A.
  ring.
Qed.

Theorem F28_c6_identity :
  forall b c : Z,
    F28_c6 (F28_B b c) =
    6912*b*c^5.
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
  unfold F28_discriminant.
  unfold F28_A, F28_B, F28_F.
  ring.
Qed.

Theorem F28_discriminant_vanishes :
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

(* ------------------------------------------------------ *)
(* 4. CORRECTED NONVANISHING OF A                        *)
(* ------------------------------------------------------ *)

Theorem F28_A_nonzero :
  forall p a c : Z,
    prime p ->
    5 <= p ->
    ~ (p | a) ->
    ~ (p | c) ->
    ~ (p | F28_A a c).
Proof.
  intros p a c Hp Hlarge Ha Hc.
  unfold F28_A.

  replace (4*a*c^3)
    with (4*(a*c^3)) by ring.

  apply F28_prime_product_nonzero.
  - exact Hp.
  - apply F28_prime_4_nonzero.
    + exact Hp.
    + exact Hlarge.
  - apply F28_prime_product_nonzero.
    + exact Hp.
    + exact Ha.
    + apply F28_prime_cube_nonzero.
      * exact Hp.
      * exact Hc.
Qed.

Theorem F28_c4_nonzero :
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

Theorem F28_multiplicative_invariants :
  forall p a b c : Z,
    prime p ->
    5 <= p ->
    ~ (p | a) ->
    ~ (p | c) ->
    (p | F28_F a b c) ->
    F28_multiplicative_invariant_criterion
      p (F28_A a c) (F28_B b c).
Proof.
  intros p a b c Hp Hlarge Ha Hc HF.
  unfold F28_multiplicative_invariant_criterion.
  split.
  - apply F28_discriminant_vanishes.
    exact HF.
  - apply F28_c4_nonzero.
    + exact Hp.
    + exact Hlarge.
    + exact Ha.
    + exact Hc.
Qed.

(* ------------------------------------------------------ *)
(* 5. NONDEGENERATE SINGULAR ROOT                        *)
(* ------------------------------------------------------ *)

Theorem F28_derivative_root_nonzero :
  forall p A r : Z,
    ~ (p | A) ->
    (p | F28_derivative A r) ->
    ~ (p | r).
Proof.
  intros p A r HA Hder Hr.

  assert (Hrr : (p | r*r)).
  {
    apply F28_divide_mul.
    exact Hr.
  }

  assert (Hthree : (p | 3*r^2)).
  {
    replace (3*r^2)
      with ((r*r)*3) by ring.
    apply F28_divide_mul.
    exact Hrr.
  }

  apply HA.

  replace A with
    ((3*r^2+A)+(-(3*r^2))) by ring.

  apply F28_divide_add.
  - exact Hder.
  - apply F28_divide_neg.
    exact Hthree.
Qed.

Theorem F28_three_root_nonzero :
  forall p A r : Z,
    prime p ->
    5 <= p ->
    ~ (p | A) ->
    (p | F28_derivative A r) ->
    ~ (p | 3*r).
Proof.
  intros p A r Hp Hlarge HA Hder.

  assert (H3 : ~ (p | 3)).
  {
    apply F28_prime_3_nonzero.
    exact Hlarge.
  }

  assert (Hr : ~ (p | r)).
  {
    exact
      (F28_derivative_root_nonzero
         p A r HA Hder).
  }

  exact
    (F28_prime_product_nonzero
       p 3 r Hp H3 Hr).
Qed.

Theorem F28_ordinary_node_from_singularity :
  forall p a b c r : Z,
    prime p ->
    5 <= p ->
    ~ (p | a) ->
    ~ (p | c) ->
    (p | F28_cubic
           (F28_A a c) (F28_B b c) r) ->
    (p | F28_derivative (F28_A a c) r) ->
    F28_ordinary_node
      p (F28_A a c) (F28_B b c) r.
Proof.
  intros p a b c r Hp Hlarge Ha Hc Hf Hd.
  unfold F28_ordinary_node.

  split.
  - exact Hf.
  - split.
    + exact Hd.
    + apply F28_three_root_nonzero
        with (A := F28_A a c).
      * exact Hp.
      * exact Hlarge.
      * apply F28_A_nonzero.
        -- exact Hp.
        -- exact Hlarge.
        -- exact Ha.
        -- exact Hc.
      * exact Hd.
Qed.

(* ------------------------------------------------------ *)
(* 6. LOCAL TRANSLATION AT THE SINGULAR POINT           *)
(* ------------------------------------------------------ *)

Theorem F28_cubic_translation_identity :
  forall A B r u : Z,
    F28_cubic A B (r+u) =
    F28_cubic A B r +
    F28_derivative A r*u +
    3*r*u^2 + u^3.
Proof.
  intros A B r u.
  unfold F28_cubic, F28_derivative.
  ring.
Qed.

Theorem F28_local_equation_identity :
  forall A B r u v : Z,
    v^2 - F28_cubic A B (r+u) =
    F28_tangent_cone r u v
    - u^3
    - F28_cubic A B r
    - F28_derivative A r*u.
Proof.
  intros A B r u v.
  unfold F28_tangent_cone.
  unfold F28_cubic, F28_derivative.
  ring.
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

(* ------------------------------------------------------ *)
(* 7. FINAL STAGE 7 CERTIFICATE                          *)
(* ------------------------------------------------------ *)

Theorem F28_stage7_nodal_reduction :
  forall p a b c r : Z,
    prime p ->
    5 <= p ->
    ~ (p | a) ->
    ~ (p | c) ->
    (p | F28_F a b c) ->
    (p | F28_cubic
           (F28_A a c) (F28_B b c) r) ->
    (p | F28_derivative (F28_A a c) r) ->
    F28_nodal_reduction_certificate
      p (F28_A a c) (F28_B b c) r.
Proof.
  intros p a b c r
         Hp Hlarge Ha Hc HF Hf Hd.

  unfold F28_nodal_reduction_certificate.
  split.
  - exact
      (F28_multiplicative_invariants
         p a b c Hp Hlarge Ha Hc HF).
  - exact
      (F28_ordinary_node_from_singularity
         p a b c r Hp Hlarge Ha Hc Hf Hd).
Qed.

(* ------------------------------------------------------ *)
(* 8. STRENGTHENED FINAL THEOREM                         *)
(* ------------------------------------------------------ *)

Theorem F28_stage7_complete_certificate :
  forall p a b c r : Z,
    prime p ->
    5 <= p ->
    ~ (p | a) ->
    ~ (p | c) ->
    (p | F28_F a b c) ->
    (p | F28_cubic
           (F28_A a c) (F28_B b c) r) ->
    (p | F28_derivative (F28_A a c) r) ->
    F28_nodal_reduction_certificate
      p (F28_A a c) (F28_B b c) r
    /\
    ~ (p | r)
    /\
    ~ (p | F28_tangent_cone r 1 0).
Proof.
  intros p a b c r
         Hp Hlarge Ha Hc HF Hf Hd.

  assert (HA :
    ~ (p | F28_A a c)).
  {
    exact
      (F28_A_nonzero
         p a c Hp Hlarge Ha Hc).
  }

  assert (Hr : ~ (p | r)).
  {
    exact
      (F28_derivative_root_nonzero
         p (F28_A a c) r HA Hd).
  }

  assert (Hthree : ~ (p | 3*r)).
  {
    exact
      (F28_three_root_nonzero
         p (F28_A a c) r
         Hp Hlarge HA Hd).
  }

  split.
  - exact
      (F28_stage7_nodal_reduction
         p a b c r
         Hp Hlarge Ha Hc HF Hf Hd).
  - split.
    + exact Hr.
    + exact
        (F28_tangent_coefficient_nonzero
           p r Hthree).
Qed.


(* ====================================================== *)
(* BLOCKS COPIED UNCHANGED FROM THE 50TH FILE (F28_unconditional_bridge.v) *)
(* ====================================================== *)

Definition F28_square_certificate
  (p x : Z) : Prop :=
  exists u v : Z,
    ~ (p | u) /\
    (p | x*u^2-v^2).

Definition F28_rational_tangent_directions
  (p r : Z) : Prop :=
  exists u v : Z,
    ~ (p | u) /\
    (p | F28_tangent_cone r u v).

Definition F28_split_node_certificate
  (p r : Z) : Prop :=
  ~ (p | 3*r) /\
  F28_rational_tangent_directions p r.

Definition F28_nonsplit_node_certificate
  (p r : Z) : Prop :=
  ~ (p | 3*r) /\
  ~ F28_rational_tangent_directions p r.

Lemma F28_divide_sub :
  forall p x y : Z,
    (p | x) ->
    (p | y) ->
    (p | x-y).
Proof.
  intros p x y Hx Hy.
  replace (x-y) with (x+(-y)) by ring.
  apply F28_divide_add.
  - exact Hx.
  - apply F28_divide_neg.
    exact Hy.
Qed.

Lemma F28_prime_cancel :
  forall p x y : Z,
    prime p ->
    ~ (p | x) ->
    (p | x*y) ->
    (p | y).
Proof.
  intros p x y Hp Hx Hxy.
  apply prime_mult in Hxy; [|exact Hp].
  destruct Hxy as [Hleft | Hright].
  - exfalso.
    exact (Hx Hleft).
  - exact Hright.
Qed.

Lemma F28_cube_nonzero :
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
  - apply F28_prime_product_nonzero.
    + exact Hp.
    + exact Hx.
    + exact Hx.
Qed.

Lemma F28_eight_nonzero :
  forall p : Z,
    prime p ->
    5 <= p ->
    ~ (p | 8).
Proof.
  intros p Hp Hlarge.
  assert (H2 : ~ (p | 2)).
  {
    apply F28_not_divide_small; lia.
  }
  replace 8 with (2*(2*2)) by ring.
  apply F28_prime_product_nonzero.
  - exact Hp.
  - exact H2.
  - apply F28_prime_product_nonzero.
    + exact Hp.
    + exact H2.
    + exact H2.
Qed.

Theorem F28_singular_linear_identity :
  forall a b c r : Z,
    3*F28_cubic
        (F28_A a c) (F28_B b c) r
    - r*F28_derivative (F28_A a c) r
    =
    8*c^3*(a*r-3*b*c^2).
Proof.
  intros a b c r.
  unfold F28_cubic, F28_derivative.
  unfold F28_A, F28_B.
  ring.
Qed.

Theorem F28_singular_linear_relation :
  forall p a b c r : Z,
    prime p ->
    5 <= p ->
    ~ (p | c) ->
    (p | F28_cubic
           (F28_A a c) (F28_B b c) r) ->
    (p | F28_derivative (F28_A a c) r) ->
    (p | a*r-3*b*c^2).
Proof.
  intros p a b c r Hp Hlarge Hc Hf Hd.

  assert (Hlinear :
    (p | 3*F28_cubic
             (F28_A a c) (F28_B b c) r
          - r*F28_derivative (F28_A a c) r)).
  {
    apply F28_divide_sub.
    - replace
        (3*F28_cubic
             (F28_A a c) (F28_B b c) r)
        with
        (F28_cubic
             (F28_A a c) (F28_B b c) r*3)
        by ring.
      apply F28_divide_mul.
      exact Hf.
    - replace
        (r*F28_derivative (F28_A a c) r)
        with
        (F28_derivative (F28_A a c) r*r)
        by ring.
      apply F28_divide_mul.
      exact Hd.
  }

  rewrite F28_singular_linear_identity
    in Hlinear.

  assert (H8 : ~ (p | 8)).
  {
    exact (F28_eight_nonzero p Hp Hlarge).
  }

  assert (Hcube : ~ (p | c^3)).
  {
    exact (F28_cube_nonzero p c Hp Hc).
  }

  assert (Hfactor : ~ (p | 8*c^3)).
  {
    apply F28_prime_product_nonzero.
    - exact Hp.
    - exact H8.
    - exact Hcube.
  }

  replace
    (8*c^3*(a*r-3*b*c^2))
    with
    ((8*c^3)*(a*r-3*b*c^2))
    in Hlinear by ring.

  exact
    (F28_prime_cancel
       p (8*c^3) (a*r-3*b*c^2)
       Hp Hfactor Hlinear).
Qed.

Theorem F28_square_class_identity :
  forall a b c r : Z,
    (3*r)*(a*b) - (3*b*c)^2 =
    3*b*(a*r-3*b*c^2).
Proof.
  intros a b c r.
  ring.
Qed.

Theorem F28_singular_square_relation :
  forall p a b c r : Z,
    prime p ->
    5 <= p ->
    ~ (p | c) ->
    (p | F28_cubic
           (F28_A a c) (F28_B b c) r) ->
    (p | F28_derivative (F28_A a c) r) ->
    (p | (3*r)*(a*b)-(3*b*c)^2).
Proof.
  intros p a b c r Hp Hlarge Hc Hf Hd.

  rewrite F28_square_class_identity.

  replace
    (3*b*(a*r-3*b*c^2))
    with
    ((a*r-3*b*c^2)*(3*b))
    by ring.

  apply F28_divide_mul.

  exact
    (F28_singular_linear_relation
       p a b c r Hp Hlarge Hc Hf Hd).
Qed.

Lemma F28_square_transfer :
  forall p x y z : Z,
    prime p ->
    ~ (p | x) ->
    ~ (p | y) ->
    (p | x*y-z^2) ->
    F28_square_certificate p x ->
    F28_square_certificate p y.
Proof.
  intros p x y z Hp Hx Hy Hrelation Hsquare.
  destruct Hsquare as [u [v [Hu Heq]]].

  assert (Hxu : ~ (p | x*u)).
  {
    apply F28_prime_product_nonzero.
    - exact Hp.
    - exact Hx.
    - exact Hu.
  }

  exists (x*u), (z*v).
  split.
  - exact Hxu.
  - assert (Hfirst :
        (p | (x*y-z^2)*(x*u^2))).
    {
      apply F28_divide_mul.
      exact Hrelation.
    }

    assert (Hsecond :
        (p | (x*u^2-v^2)*z^2)).
    {
      apply F28_divide_mul.
      exact Heq.
    }

    assert (Hsum :
        (p |
          (x*y-z^2)*(x*u^2)
          + (x*u^2-v^2)*z^2)).
    {
      apply F28_divide_add.
      - exact Hfirst.
      - exact Hsecond.
    }

    replace
      (y*(x*u)^2-(z*v)^2)
      with
      ((x*y-z^2)*(x*u^2)
       + (x*u^2-v^2)*z^2)
      by ring.

    exact Hsum.
Qed.

Theorem F28_square_class_equivalence :
  forall p x y z : Z,
    prime p ->
    ~ (p | x) ->
    ~ (p | y) ->
    (p | x*y-z^2) ->
    (F28_square_certificate p x <->
     F28_square_certificate p y).
Proof.
  intros p x y z Hp Hx Hy Hrelation.

  assert (Hreverse : (p | y*x-z^2)).
  {
    replace (y*x-z^2) with (x*y-z^2)
      by ring.
    exact Hrelation.
  }

  split.
  - intro Hsquare.
    exact
      (F28_square_transfer
         p x y z Hp Hx Hy Hrelation Hsquare).
  - intro Hsquare.
    exact
      (F28_square_transfer
         p y x z Hp Hy Hx Hreverse Hsquare).
Qed.

Lemma F28_divide_opp_iff :
  forall p x : Z,
    (p | x) <-> (p | -x).
Proof.
  intros p x.
  split.
  - intro H.
    exact (F28_divide_neg p x H).
  - intro H.
    replace x with (-(-x)) by ring.
    exact (F28_divide_neg p (-x) H).
Qed.

Theorem F28_tangent_square_equivalence :
  forall p r : Z,
    F28_rational_tangent_directions p r <->
    F28_square_certificate p (3*r).
Proof.
  intros p r.
  unfold F28_rational_tangent_directions.
  unfold F28_square_certificate.

  split.
  - intros [u [v [Hu Hcone]]].
    exists u, v.
    split.
    + exact Hu.
    + apply
        (proj2
          (F28_divide_opp_iff
             p (3*r*u^2-v^2))).
      replace
        (-(3*r*u^2-v^2))
        with (F28_tangent_cone r u v)
        by (unfold F28_tangent_cone; ring).
      exact Hcone.
  - intros [u [v [Hu Hsquare]]].
    exists u, v.
    split.
    + exact Hu.
    + apply
        (proj1
          (F28_divide_opp_iff
             p (3*r*u^2-v^2))) in Hsquare.
      replace
        (F28_tangent_cone r u v)
        with (-(3*r*u^2-v^2))
        by (unfold F28_tangent_cone; ring).
      exact Hsquare.
Qed.

Theorem F28_unconditional_square_bridge :
  forall p a b c r : Z,
    prime p ->
    5 <= p ->
    ~ (p | c) ->
    ~ (p | 3*r) ->
    ~ (p | a*b) ->
    (p | F28_cubic
           (F28_A a c) (F28_B b c) r) ->
    (p | F28_derivative (F28_A a c) r) ->
    (F28_square_certificate p (3*r) <->
     F28_square_certificate p (a*b)).
Proof.
  intros p a b c r
         Hp Hlarge Hc Hthree Hab Hf Hd.

  assert (Hrelation :
    (p | (3*r)*(a*b)-(3*b*c)^2)).
  {
    exact
      (F28_singular_square_relation
         p a b c r Hp Hlarge Hc Hf Hd).
  }

  exact
    (F28_square_class_equivalence
       p (3*r) (a*b) (3*b*c)
       Hp Hthree Hab Hrelation).
Qed.

Theorem F28_unconditional_split_node :
  forall p a b c r : Z,
    prime p ->
    5 <= p ->
    ~ (p | c) ->
    ~ (p | 3*r) ->
    ~ (p | a*b) ->
    (p | F28_cubic
           (F28_A a c) (F28_B b c) r) ->
    (p | F28_derivative (F28_A a c) r) ->
    (F28_split_node_certificate p r <->
     F28_square_certificate p (a*b)).
Proof.
  intros p a b c r
         Hp Hlarge Hc Hthree Hab Hf Hd.

  pose proof
    (F28_unconditional_square_bridge
       p a b c r
       Hp Hlarge Hc Hthree Hab Hf Hd)
    as Hbridge.

  pose proof
    (F28_tangent_square_equivalence p r)
    as Htangent.

  unfold F28_split_node_certificate.

  split.
  - intros [_ Hdirections].
    apply (proj1 Hbridge).
    apply (proj1 Htangent).
    exact Hdirections.
  - intro Hsquare.
    split.
    + exact Hthree.
    + apply (proj2 Htangent).
      apply (proj2 Hbridge).
      exact Hsquare.
Qed.

(* ====================================================== *)
(* BLOCK COPIED UNCHANGED FROM THE 40TH FILE (F28_complete_arithmetic_bridge.v) *)
(* ====================================================== *)

Lemma F28_prime_inverse :
  forall p s : Z,
    prime p ->
    ~ (p | s) ->
    exists u : Z, (p | s*u-1).
Proof.
  intros p s Hp Hnotdiv.

  assert (Hgcd : Z.gcd p s = 1).
  {
    apply Zis_gcd_gcd.
    - lia.
    - apply prime_rel_prime.
      + exact Hp.
      + exact Hnotdiv.
  }

  pose proof
    (Z.gcd_bezout p s 1 Hgcd) as Hbezout.

  unfold Z.Bezout in Hbezout.
  destruct Hbezout as [k [u Hidentity]].

  exists u.
  exists (-k).
  rewrite <- Hidentity.
  ring.
Qed.

(* ====================================================== *)
(* NEW IN STAGE 8a (written in review by Claude)          *)
(* ====================================================== *)

(* ------------------------------------------------------ *)
(* 8a.1  ELEMENTARY MINIMALITY CRITERION                  *)
(* ------------------------------------------------------ *)

(* An integral change of Weierstrass coordinates with scaling
   factor u multiplies c4 by u^4: c4 = u^4 * c4'.  If p does not
   divide c4 then p cannot divide u. *)

Theorem F28_unit_scaling :
  forall p C u C' : Z,
    ~ (p | C) ->
    C = u^4*C' ->
    ~ (p | u).
Proof.
  intros p C u C' HC Heq Hu.
  apply HC.
  rewrite Heq.
  destruct Hu as [k Hk].
  exists (k^4*p^3*C').
  rewrite Hk.
  ring.
Qed.

Theorem F28_model_scaling_unit :
  forall p a c u C' : Z,
    prime p ->
    5 <= p ->
    ~ (p | a) ->
    ~ (p | c) ->
    F28_c4 (F28_A a c) = u^4*C' ->
    ~ (p | u).
Proof.
  intros p a c u C' Hp Hlarge Ha Hc Heq.
  apply (F28_unit_scaling p (F28_c4 (F28_A a c)) u C').
  - exact (F28_c4_nonzero p a c Hp Hlarge Ha Hc).
  - exact Heq.
Qed.

(* ------------------------------------------------------ *)
(* 8a.2  EXISTENCE OF A DOUBLE ROOT (GENERAL A, B)        *)
(* ------------------------------------------------------ *)

Lemma F28_double_root_general :
  forall p A B u m : Z,
    prime p ->
    5 <= p ->
    ~ (p | A) ->
    (p | 4*A^3 + 27*B^2) ->
    2*A*u - 1 = m*p ->
    (p | F28_cubic A B (-3*B*u)) /\
    (p | F28_derivative A (-3*B*u)).
Proof.
  intros p A B u m Hp Hlarge HA HD Hm.

  assert (H3 : ~ (p | 3)).
  {
    apply F28_not_divide_small; lia.
  }

  assert (H4 : ~ (p | 4)).
  {
    exact (F28_prime_4_nonzero p Hp Hlarge).
  }

  assert (HAA : ~ (p | A*A)).
  {
    exact (F28_prime_square_nonzero p A Hp HA).
  }

  assert (H4AA : ~ (p | 4*(A*A))).
  {
    exact (F28_prime_product_nonzero p 4 (A*A) Hp H4 HAA).
  }

  assert (Hu : 2*A*u = m*p+1).
  {
    rewrite <- Hm.
    ring.
  }

  assert (Hid :
    4*(A*A)*(3*(-3*B*u)^2+A) =
    (4*A^3+27*B^2) + p*(27*B^2*(2*m+m^2*p))).
  {
    replace (4*(A*A)*(3*(-3*B*u)^2+A))
      with (4*A^3+27*B^2*(2*A*u)^2) by ring.
    rewrite Hu.
    ring.
  }

  assert (Hdiv :
    (p | 4*(A*A)*(3*(-3*B*u)^2+A))).
  {
    rewrite Hid.
    apply F28_divide_add.
    - exact HD.
    - exact
        (F28_divide_mul p p
           (27*B^2*(2*m+m^2*p))
           (Z.divide_refl p)).
  }

  assert (Hder : (p | 3*(-3*B*u)^2+A)).
  {
    exact
      (F28_prime_cancel p (4*(A*A))
         (3*(-3*B*u)^2+A) Hp H4AA Hdiv).
  }

  assert (Hid2 :
    3*((-3*B*u)^3 + A*(-3*B*u) + B) =
    (3*(-3*B*u)^2+A)*(-3*B*u) + p*(-3*B*m)).
  {
    replace (3*((-3*B*u)^3 + A*(-3*B*u) + B))
      with ((3*(-3*B*u)^2+A)*(-3*B*u)
            + 3*B*(1 - 2*A*u)) by ring.
    replace (1 - 2*A*u) with (-(m*p)).
    - ring.
    - rewrite Hu.
      ring.
  }

  assert (H3f :
    (p | 3*((-3*B*u)^3 + A*(-3*B*u) + B))).
  {
    rewrite Hid2.
    apply F28_divide_add.
    - exact
        (F28_divide_mul p (3*(-3*B*u)^2+A)
           (-3*B*u) Hder).
    - exact
        (F28_divide_mul p p (-3*B*m)
           (Z.divide_refl p)).
  }

  split.
  - exact
      (F28_prime_cancel p 3
         ((-3*B*u)^3 + A*(-3*B*u) + B)
         Hp H3 H3f).
  - exact Hder.
Qed.

Lemma F28_discriminant_quartic_identity :
  forall a b c : Z,
    4*(F28_A a c)^3 + 27*(F28_B b c)^2 =
    64*c^9*F28_F a b c.
Proof.
  intros a b c.
  unfold F28_A, F28_B, F28_F.
  ring.
Qed.

Theorem F28_double_root_exists :
  forall p a b c : Z,
    prime p ->
    5 <= p ->
    ~ (p | a) ->
    ~ (p | c) ->
    (p | F28_F a b c) ->
    exists r : Z,
      (p | F28_cubic (F28_A a c) (F28_B b c) r) /\
      (p | F28_derivative (F28_A a c) r).
Proof.
  intros p a b c Hp Hlarge Ha Hc HF.

  assert (H2 : ~ (p | 2)).
  {
    apply F28_not_divide_small; lia.
  }

  assert (HA : ~ (p | F28_A a c)).
  {
    exact (F28_A_nonzero p a c Hp Hlarge Ha Hc).
  }

  assert (H2A : ~ (p | 2*F28_A a c)).
  {
    exact
      (F28_prime_product_nonzero
         p 2 (F28_A a c) Hp H2 HA).
  }

  assert (HD :
    (p | 4*(F28_A a c)^3 + 27*(F28_B b c)^2)).
  {
    rewrite F28_discriminant_quartic_identity.
    destruct HF as [k Hk].
    exists (64*c^9*k).
    rewrite Hk.
    ring.
  }

  destruct
    (F28_prime_inverse p (2*F28_A a c) Hp H2A)
    as [u [m Hm]].

  exists (-3*F28_B b c*u).

  exact
    (F28_double_root_general
       p (F28_A a c) (F28_B b c) u m
       Hp Hlarge HA HD Hm).
Qed.

(* ------------------------------------------------------ *)
(* 8a.3  THE REDUCED CURVE OVER F_p, AFFINE SINGULAR POINTS *)
(* ------------------------------------------------------ *)

(* A point (x, y) of the reduced curve y^2 = f(x) over F_p is
   singular when it lies on the curve, d/dy (y^2 - f) = 2 y
   vanishes and d/dx (y^2 - f) = - f'(x) vanishes (the sign is
   irrelevant for divisibility).  Points are integer
   representatives; everything is read mod p. *)

Definition F28_reduced_singular
  (p A B x y : Z) : Prop :=
  (p | y^2 - F28_cubic A B x) /\
  (p | 2*y) /\
  (p | F28_derivative A x).

Lemma F28_reduced_singular_split :
  forall p A B x y : Z,
    prime p ->
    5 <= p ->
    F28_reduced_singular p A B x y ->
    (p | y) /\
    (p | F28_cubic A B x) /\
    (p | F28_derivative A x).
Proof.
  intros p A B x y Hp Hlarge Hsing.
  destruct Hsing as [Hcurve [Hy2 Hder]].

  assert (H2 : ~ (p | 2)).
  {
    apply F28_not_divide_small; lia.
  }

  assert (Hy : (p | y)).
  {
    exact (F28_prime_cancel p 2 y Hp H2 Hy2).
  }

  assert (Hysq : (p | y^2)).
  {
    replace (y^2) with (y*y) by ring.
    exact (F28_divide_mul p y y Hy).
  }

  assert (Hf : (p | F28_cubic A B x)).
  {
    replace (F28_cubic A B x)
      with (y^2 - (y^2 - F28_cubic A B x))
      by ring.
    exact (F28_divide_sub p _ _ Hysq Hcurve).
  }

  split.
  - exact Hy.
  - split.
    + exact Hf.
    + exact Hder.
Qed.

Lemma F28_reduced_singular_intro :
  forall p A B x : Z,
    (p | F28_cubic A B x) ->
    (p | F28_derivative A x) ->
    F28_reduced_singular p A B x 0.
Proof.
  intros p A B x Hf Hder.
  unfold F28_reduced_singular.
  split.
  - replace (0^2 - F28_cubic A B x)
      with (-(F28_cubic A B x)) by ring.
    exact (F28_divide_neg p _ Hf).
  - split.
    + exists 0.
      ring.
    + exact Hder.
Qed.

(* ------------------------------------------------------ *)
(* 8a.4  THE SINGULAR POINT IS UNIQUE MOD p               *)
(* ------------------------------------------------------ *)

Theorem F28_reduced_singular_unique :
  forall p a b c x1 y1 x2 y2 : Z,
    prime p ->
    5 <= p ->
    ~ (p | a) ->
    ~ (p | c) ->
    F28_reduced_singular
      p (F28_A a c) (F28_B b c) x1 y1 ->
    F28_reduced_singular
      p (F28_A a c) (F28_B b c) x2 y2 ->
    (p | x1 - x2) /\ (p | y1) /\ (p | y2).
Proof.
  intros p a b c x1 y1 x2 y2
         Hp Hlarge Ha Hc S1 S2.

  destruct
    (F28_reduced_singular_split
       p (F28_A a c) (F28_B b c) x1 y1
       Hp Hlarge S1)
    as [Hy1 [Hf1 Hd1]].

  destruct
    (F28_reduced_singular_split
       p (F28_A a c) (F28_B b c) x2 y2
       Hp Hlarge S2)
    as [Hy2 [Hf2 Hd2]].

  pose proof
    (F28_singular_linear_relation
       p a b c x1 Hp Hlarge Hc Hf1 Hd1)
    as L1.

  pose proof
    (F28_singular_linear_relation
       p a b c x2 Hp Hlarge Hc Hf2 Hd2)
    as L2.

  split.
  - apply (F28_prime_cancel p a (x1-x2) Hp Ha).
    replace (a*(x1-x2))
      with ((a*x1-3*b*c^2) - (a*x2-3*b*c^2))
      by ring.
    exact (F28_divide_sub p _ _ L1 L2).
  - split.
    + exact Hy1.
    + exact Hy2.
Qed.

(* ------------------------------------------------------ *)
(* 8a.5  THE SINGULAR POINT IS A NODE (NONDEGENERATE CONE) *)
(* ------------------------------------------------------ *)

Theorem F28_reduced_singular_node :
  forall p a b c x y : Z,
    prime p ->
    5 <= p ->
    ~ (p | a) ->
    ~ (p | c) ->
    F28_reduced_singular
      p (F28_A a c) (F28_B b c) x y ->
    ~ (p | x) /\
    ~ (p | 3*x) /\
    ~ (p | F28_tangent_cone x 1 0).
Proof.
  intros p a b c x y Hp Hlarge Ha Hc Hsing.

  destruct
    (F28_reduced_singular_split
       p (F28_A a c) (F28_B b c) x y
       Hp Hlarge Hsing)
    as [Hy [Hf Hd]].

  assert (HA : ~ (p | F28_A a c)).
  {
    exact (F28_A_nonzero p a c Hp Hlarge Ha Hc).
  }

  assert (Hr : ~ (p | x)).
  {
    exact
      (F28_derivative_root_nonzero
         p (F28_A a c) x HA Hd).
  }

  assert (Hthree : ~ (p | 3*x)).
  {
    exact
      (F28_three_root_nonzero
         p (F28_A a c) x Hp Hlarge HA Hd).
  }

  split.
  - exact Hr.
  - split.
    + exact Hthree.
    + exact
        (F28_tangent_coefficient_nonzero
           p x Hthree).
Qed.

(* ------------------------------------------------------ *)
(* 8a.6  SPLIT / NONSPLIT NODE OF THE REDUCED CURVE       *)
(* ------------------------------------------------------ *)

Theorem F28_reduced_node_split_criterion :
  forall p a b c x y : Z,
    prime p ->
    5 <= p ->
    ~ (p | a) ->
    ~ (p | b) ->
    ~ (p | c) ->
    F28_reduced_singular
      p (F28_A a c) (F28_B b c) x y ->
    (F28_split_node_certificate p x <->
     F28_square_certificate p (a*b)).
Proof.
  intros p a b c x y Hp Hlarge Ha Hb Hc Hsing.

  assert (Hab : ~ (p | a*b)).
  {
    exact (F28_prime_product_nonzero p a b Hp Ha Hb).
  }

  destruct
    (F28_reduced_singular_split
       p (F28_A a c) (F28_B b c) x y
       Hp Hlarge Hsing)
    as [Hy [Hf Hd]].

  destruct
    (F28_reduced_singular_node
       p a b c x y Hp Hlarge Ha Hc Hsing)
    as [Hr [Hthree Htangent]].

  exact
    (F28_unconditional_split_node
       p a b c x
       Hp Hlarge Hc Hthree Hab Hf Hd).
Qed.

(* ------------------------------------------------------ *)
(* 8a.7  THE STAGE 8a MODEL THEOREM                       *)
(* ------------------------------------------------------ *)

Theorem F28_stage8a_reduction_model :
  forall p a b c : Z,
    prime p ->
    5 <= p ->
    ~ (p | a) ->
    ~ (p | b) ->
    ~ (p | c) ->
    (p | F28_F a b c) ->
    F28_multiplicative_invariant_criterion
      p (F28_A a c) (F28_B b c)
    /\
    (forall u C' : Z,
       F28_c4 (F28_A a c) = u^4*C' ->
       ~ (p | u))
    /\
    (exists x : Z,
       F28_reduced_singular
         p (F28_A a c) (F28_B b c) x 0)
    /\
    (forall x1 y1 x2 y2 : Z,
       F28_reduced_singular
         p (F28_A a c) (F28_B b c) x1 y1 ->
       F28_reduced_singular
         p (F28_A a c) (F28_B b c) x2 y2 ->
       (p | x1 - x2) /\ (p | y1) /\ (p | y2))
    /\
    (forall x y : Z,
       F28_reduced_singular
         p (F28_A a c) (F28_B b c) x y ->
       ~ (p | x) /\
       ~ (p | 3*x) /\
       ~ (p | F28_tangent_cone x 1 0))
    /\
    (forall x y : Z,
       F28_reduced_singular
         p (F28_A a c) (F28_B b c) x y ->
       (F28_split_node_certificate p x <->
        F28_square_certificate p (a*b))).
Proof.
  intros p a b c Hp Hlarge Ha Hb Hc HF.

  assert (H1 :
    F28_multiplicative_invariant_criterion
      p (F28_A a c) (F28_B b c)).
  {
    exact
      (F28_multiplicative_invariants
         p a b c Hp Hlarge Ha Hc HF).
  }

  assert (H2 :
    forall u C' : Z,
      F28_c4 (F28_A a c) = u^4*C' ->
      ~ (p | u)).
  {
    intros u C' Heq.
    exact
      (F28_model_scaling_unit
         p a c u C' Hp Hlarge Ha Hc Heq).
  }

  assert (H3 :
    exists x : Z,
      F28_reduced_singular
        p (F28_A a c) (F28_B b c) x 0).
  {
    destruct
      (F28_double_root_exists
         p a b c Hp Hlarge Ha Hc HF)
      as [r [Hf Hd]].
    exists r.
    exact
      (F28_reduced_singular_intro
         p (F28_A a c) (F28_B b c) r Hf Hd).
  }

  assert (H4 :
    forall x1 y1 x2 y2 : Z,
      F28_reduced_singular
        p (F28_A a c) (F28_B b c) x1 y1 ->
      F28_reduced_singular
        p (F28_A a c) (F28_B b c) x2 y2 ->
      (p | x1 - x2) /\ (p | y1) /\ (p | y2)).
  {
    intros x1 y1 x2 y2 S1 S2.
    exact
      (F28_reduced_singular_unique
         p a b c x1 y1 x2 y2
         Hp Hlarge Ha Hc S1 S2).
  }

  assert (H5 :
    forall x y : Z,
      F28_reduced_singular
        p (F28_A a c) (F28_B b c) x y ->
      ~ (p | x) /\
      ~ (p | 3*x) /\
      ~ (p | F28_tangent_cone x 1 0)).
  {
    intros x y S.
    exact
      (F28_reduced_singular_node
         p a b c x y Hp Hlarge Ha Hc S).
  }

  assert (H6 :
    forall x y : Z,
      F28_reduced_singular
        p (F28_A a c) (F28_B b c) x y ->
      (F28_split_node_certificate p x <->
       F28_square_certificate p (a*b))).
  {
    intros x y S.
    exact
      (F28_reduced_node_split_criterion
         p a b c x y
         Hp Hlarge Ha Hb Hc S).
  }

  exact (conj H1 (conj H2 (conj H3 (conj H4 (conj H5 H6))))).
Qed.


(* ====================================================== *)
(* BLOCKS COPIED UNCHANGED FROM THE 56TH FILE (F28_stage12_inverses.v): STAGES 8-12 *)
(* ====================================================== *)

Definition F28_factor (r x : Z) : Z := (x-r)^2*(x+2*r).

Theorem F28_factor_difference :
  forall A B r x : Z,
    F28_cubic A B x - F28_factor r x =
    F28_derivative A r*(x-r) + F28_cubic A B r.
Proof.
  intros A B r x.
  unfold F28_cubic, F28_derivative, F28_factor. ring.
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

Definition F28_norm_x (r t : Z) : Z := t^2 - 2*r.

Definition F28_norm_y (r t : Z) : Z := t*(t^2 - 3*r).

Definition F28_node_equation (r x y : Z) : Z :=
  y^2 - F28_factor r x.

Theorem F28_stage9_parametrization :
  forall r t : Z,
    F28_node_equation r (F28_norm_x r t) (F28_norm_y r t) = 0.
Proof.
  intros r t.
  unfold F28_node_equation, F28_norm_x, F28_norm_y, F28_factor.
  ring.
Qed.

Theorem F28_stage9_reduced_model_parametrization :
  forall p A B r t : Z,
    (p | F28_cubic A B r) ->
    (p | F28_derivative A r) ->
    (p | F28_norm_y r t ^ 2 -
         F28_cubic A B (F28_norm_x r t)).
Proof.
  intros p A B r t Hf Hd.
  pose proof
    (F28_singular_factorization
       p A B r (F28_norm_x r t) Hf Hd) as Hdiff.
  destruct Hdiff as [k Hk].
  exists (-k).
  pose proof (F28_stage9_parametrization r t) as Hparam.
  unfold F28_node_equation in Hparam.
  replace (F28_norm_y r t ^ 2 -
           F28_cubic A B (F28_norm_x r t))
    with ((F28_norm_y r t ^ 2 - F28_factor r (F28_norm_x r t))
          - (F28_cubic A B (F28_norm_x r t)
             - F28_factor r (F28_norm_x r t))) by ring.
  rewrite Hparam, Hk.
  ring.
Qed.

Definition F28_square_mod (p z : Z) : Prop :=
  exists t : Z, (p | t^2 - z).

Definition F28_split_branches (p r : Z) : Prop :=
  exists t : Z,
    (p | F28_norm_x r t - r) /\
    (p | F28_norm_y r t) /\
    ~ (p | t).

Theorem F28_stage10_node_x_identity :
  forall r t : Z,
    F28_norm_x r t - r = t^2 - 3*r.
Proof.
  intros r t. unfold F28_norm_x. ring.
Qed.

Theorem F28_stage10_node_y_identity :
  forall r t : Z,
    F28_norm_y r t = t*(t^2-3*r).
Proof.
  intros r t. unfold F28_norm_y. reflexivity.
Qed.

Theorem F28_stage10_square_gives_node :
  forall p r t : Z,
    (p | t^2 - 3*r) ->
    (p | F28_norm_x r t - r) /\
    (p | F28_norm_y r t).
Proof.
  intros p r t H.
  split.
  - rewrite F28_stage10_node_x_identity. exact H.
  - rewrite F28_stage10_node_y_identity.
    destruct H as [k Hk].
    exists (t*k). rewrite Hk. ring.
Qed.

Theorem F28_stage10_square_nonzero :
  forall p r t : Z,
    prime p ->
    ~ (p | 3*r) ->
    (p | t^2 - 3*r) ->
    ~ (p | t).
Proof.
  intros p r t Hp Hr Hsquare Ht.
  apply Hr.
  destruct Hsquare as [k Hk].
  destruct Ht as [j Hj].
  exists (p*j*j-k).
  rewrite Hj in Hk.
  nia.
Qed.

Theorem F28_stage10_split_iff_square :
  forall p r : Z,
    prime p ->
    ~ (p | 3*r) ->
    (F28_split_branches p r <-> F28_square_mod p (3*r)).
Proof.
  intros p r Hp Hr.
  split.
  - intros [t [Hx [Hy Ht]]].
    exists t.
    rewrite <- F28_stage10_node_x_identity.
    exact Hx.
  - intros [t Hsquare].
    exists t.
    destruct (F28_stage10_square_gives_node p r t Hsquare)
      as [Hx Hy].
    repeat split.
    + exact Hx.
    + exact Hy.
    + exact (F28_stage10_square_nonzero p r t Hp Hr Hsquare).
Qed.

Definition F28_congr (p x y : Z) : Prop := (p | x-y).

Lemma F28_congr_refl : forall p x, F28_congr p x x.
Proof.
  intros p x. unfold F28_congr.
  replace (x-x) with 0 by ring.
  exists 0. ring.
Qed.

Lemma F28_congr_sym : forall p x y,
  F28_congr p x y -> F28_congr p y x.
Proof.
  intros p x y H. unfold F28_congr in *.
  destruct H as [k Hk]. exists (-k).
  replace (y-x) with (-(x-y)) by ring.
  rewrite Hk. ring.
Qed.

Lemma F28_congr_trans : forall p x y z,
  F28_congr p x y -> F28_congr p y z -> F28_congr p x z.
Proof.
  intros p x y z H1 H2. unfold F28_congr in *.
  destruct H1 as [k Hk]. destruct H2 as [l Hl].
  exists (k+l).
  replace (x-z) with ((x-y)+(y-z)) by ring.
  rewrite Hk, Hl. ring.
Qed.

Lemma F28_congr_mul : forall p x x' y y',
  F28_congr p x x' -> F28_congr p y y' ->
  F28_congr p (x*y) (x'*y').
Proof.
  intros p x x' y y' H1 H2. unfold F28_congr in *.
  destruct H1 as [k Hk]. destruct H2 as [l Hl].
  exists (k*y+x'*l).
  replace (x*y-x'*y') with ((x-x')*y+x'*(y-y')) by ring.
  rewrite Hk, Hl. ring.
Qed.

Lemma F28_congr_square : forall p x y,
  F28_congr p x y -> F28_congr p (x^2) (y^2).
Proof.
  intros p x y H.
  replace (x^2) with (x*x) by ring.
  replace (y^2) with (y*y) by ring.
  apply F28_congr_mul; exact H.
Qed.

Theorem F28_stage11_product_square :
  forall p a b c r : Z,
    (p | a*r - 3*b*c^2) ->
    F28_congr p ((3*r)*(a*b)) ((3*b*c)^2).
Proof.
  intros p a b c r H.
  unfold F28_congr.
  destruct H as [k Hk].
  exists (3*b*k).
  replace ((3*r)*(a*b)-(3*b*c)^2)
    with ((3*b)*(a*r-3*b*c^2)) by ring.
  rewrite Hk. ring.
Qed.

Theorem F28_stage11_square_transfer :
  forall p z y s w : Z,
    F28_congr p (z*y) (s^2) ->
    F28_congr p (z*w) 1 ->
    F28_square_mod p z ->
    F28_square_mod p y.
Proof.
  intros p z y s w Hprod Hinv [t Ht].
  exists (s*w*t).
  unfold F28_square_mod in *.
  assert (Htz : F28_congr p (t^2) z).
  { unfold F28_congr. exact Ht. }
  assert (Hsqprod : F28_congr p (s^2) (z*y)).
  { apply F28_congr_sym. exact Hprod. }
  assert (Hleft :
    F28_congr p ((s^2)*(w^2)*(t^2)) ((z*y)*(w^2)*z)).
  {
    apply F28_congr_mul.
    - apply F28_congr_mul.
      + exact Hsqprod.
      + apply F28_congr_refl.
    - exact Htz.
  }
  assert (Hinv2 : F28_congr p ((z*w)^2) 1).
  {
    replace 1 with (1^2) by ring.
    apply F28_congr_square. exact Hinv.
  }
  assert (Hright : F28_congr p (y*((z*w)^2)) y).
  {
    replace y with (y*1) at 2 by ring.
    apply F28_congr_mul.
    - apply F28_congr_refl.
    - exact Hinv2.
  }
  assert (Hfinal : F28_congr p ((s*w*t)^2) y).
  {
    eapply F28_congr_trans.
    - replace ((s*w*t)^2) with ((s^2)*(w^2)*(t^2)) by ring.
      exact Hleft.
    - replace ((z*y)*(w^2)*z) with (y*((z*w)^2)) by ring.
      exact Hright.
  }
  unfold F28_congr in Hfinal.
  exact Hfinal.
Qed.

Theorem F28_stage11_split_to_ab :
  forall p a b c r w : Z,
    prime p ->
    ~ (p | 3*r) ->
    (p | a*r-3*b*c^2) ->
    (p | (3*r)*w-1) ->
    F28_split_branches p r ->
    F28_square_mod p (a*b).
Proof.
  intros p a b c r w Hp Hr Hbridge Hinv Hsplit.
  apply (F28_stage11_square_transfer
           p (3*r) (a*b) (3*b*c) w).
  - exact (F28_stage11_product_square p a b c r Hbridge).
  - unfold F28_congr. exact Hinv.
  - apply (proj1 (F28_stage10_split_iff_square p r Hp Hr)).
    exact Hsplit.
Qed.

Theorem F28_stage11_ab_to_split :
  forall p a b c r w : Z,
    prime p ->
    ~ (p | 3*r) ->
    (p | a*r-3*b*c^2) ->
    (p | (a*b)*w-1) ->
    F28_square_mod p (a*b) ->
    F28_split_branches p r.
Proof.
  intros p a b c r w Hp Hr Hbridge Hinv Hsquare.
  apply (proj2 (F28_stage10_split_iff_square p r Hp Hr)).
  apply (F28_stage11_square_transfer
           p (a*b) (3*r) (3*b*c) w).
  - unfold F28_congr.
    replace ((a*b)*(3*r)-(3*b*c)^2)
      with ((3*r)*(a*b)-(3*b*c)^2) by ring.
    exact (F28_stage11_product_square p a b c r Hbridge).
  - unfold F28_congr. exact Hinv.
  - exact Hsquare.
Qed.

Theorem F28_stage11_split_iff_ab :
  forall p a b c r w1 w2 : Z,
    prime p ->
    ~ (p | 3*r) ->
    (p | a*r-3*b*c^2) ->
    (p | (3*r)*w1-1) ->
    (p | (a*b)*w2-1) ->
    (F28_split_branches p r <-> F28_square_mod p (a*b)).
Proof.
  intros p a b c r w1 w2 Hp Hr Hbridge Hinv1 Hinv2.
  split.
  - apply (F28_stage11_split_to_ab p a b c r w1
             Hp Hr Hbridge Hinv1).
  - apply (F28_stage11_ab_to_split p a b c r w2
             Hp Hr Hbridge Hinv2).
Qed.

Lemma F28_stage12_inverse_from_bezout :
  forall p z : Z,
    Bezout p z 1 -> exists w : Z, (p | z*w-1).
Proof.
  intros p z Hbez.
  destruct Hbez as [u v Huv].
  exists v.
  exists (-u).
  nia.
Qed.

Lemma F28_stage12_inverse_prime :
  forall p z : Z,
    prime p -> ~ (p | z) ->
    exists w : Z, (p | z*w-1).
Proof.
  intros p z Hp Hnz.
  apply F28_stage12_inverse_from_bezout.
  apply rel_prime_bezout.
  apply prime_rel_prime; assumption.
Qed.

Theorem F28_stage12_split_iff_ab :
  forall p a b c r : Z,
    prime p ->
    ~ (p | 3*r) ->
    ~ (p | a*b) ->
    (p | a*r-3*b*c^2) ->
    (F28_split_branches p r <-> F28_square_mod p (a*b)).
Proof.
  intros p a b c r Hp Hr Hab Hbridge.
  destruct (F28_stage12_inverse_prime p (3*r) Hp Hr)
    as [w1 Hw1].
  destruct (F28_stage12_inverse_prime p (a*b) Hp Hab)
    as [w2 Hw2].
  exact (F28_stage11_split_iff_ab
           p a b c r w1 w2 Hp Hr Hbridge Hw1 Hw2).
Qed.

(* ====================================================== *)
(* NEW IN STAGE 13 (written in review by Claude)          *)
(* ====================================================== *)

(* ------------------------------------------------------ *)
(* 13.1  VALUATION FORM OF THE MINIMALITY CRITERION       *)
(* ------------------------------------------------------ *)

(* F28_ppow p k = p^k, for a natural number k. *)

Fixpoint F28_ppow (p : Z) (k : nat) : Z :=
  match k with
  | O => 1
  | S k' => p * F28_ppow p k'
  end.

Lemma F28_ppow_pos :
  forall p : Z,
    1 < p ->
    forall k : nat,
      0 < F28_ppow p k.
Proof.
  intros p Hp k.
  induction k as [|k IH].
  - simpl. lia.
  - simpl.
    apply Z.mul_pos_pos.
    + lia.
    + exact IH.
Qed.

Lemma F28_prime_divides_fourth :
  forall p x : Z,
    prime p ->
    (p | x^4) ->
    (p | x).
Proof.
  intros p x Hp H.
  replace (x^4) with (x*(x*(x*x))) in H by ring.
  destruct (prime_mult p Hp x (x*(x*x)) H) as [H1 | H2].
  - exact H1.
  - destruct (prime_mult p Hp x (x*x) H2) as [H3 | H4].
    + exact H3.
    + destruct (prime_mult p Hp x x H4) as [H5 | H6].
      * exact H5.
      * exact H6.
Qed.

(* One step of the induction: n^4 C = m^4 C', p not dividing C,
   q | n and p q | m give p q | n.  Here u = m/n is the scaling
   factor of a change of coordinates, C = c4 and C' = c4'. *)

Lemma F28_valuation_step :
  forall p C m n C' q : Z,
    prime p ->
    ~ (p | C) ->
    0 < q ->
    n^4*C = m^4*C' ->
    (q | n) ->
    (p*q | m) ->
    (p*q | n).
Proof.
  intros p C m n C' q Hp HC Hq Heq Hqn Hpqm.
  destruct Hqn as [n' Hn].
  destruct Hpqm as [m' Hm].

  assert (Hq4 : q^4 <> 0).
  {
    assert (Hpos : 0 < q^4).
    {
      apply Z.pow_pos_nonneg; lia.
    }
    lia.
  }

  assert (Hmul :
    q^4*(n'^4*C) = q^4*(p^4*m'^4*C')).
  {
    transitivity (n^4*C).
    - rewrite Hn. ring.
    - rewrite Heq. rewrite Hm. ring.
  }

  assert (Hred : n'^4*C = p^4*m'^4*C').
  {
    exact
      (proj1
        (Z.mul_cancel_l
           (n'^4*C) (p^4*m'^4*C') (q^4) Hq4)
        Hmul).
  }

  assert (Hdiv : (p | C*n'^4)).
  {
    exists (p^3*m'^4*C').
    replace (C*n'^4) with (n'^4*C) by ring.
    rewrite Hred.
    ring.
  }

  assert (Hn4 : (p | n'^4)).
  {
    exact (F28_prime_cancel p C (n'^4) Hp HC Hdiv).
  }

  destruct (F28_prime_divides_fourth p n' Hp Hn4)
    as [j Hj].
  exists j.
  rewrite Hn.
  rewrite Hj.
  ring.
Qed.

(* v_p(m) <= v_p(n): every power of p dividing m divides n. *)

Lemma F28_valuation_bound :
  forall p C m n C' : Z,
    prime p ->
    ~ (p | C) ->
    n^4*C = m^4*C' ->
    forall k : nat,
      (F28_ppow p k | m) ->
      (F28_ppow p k | n).
Proof.
  intros p C m n C' Hp HC Heq k.

  assert (Hgt : 1 < p).
  {
    destruct Hp as [Hg _].
    exact Hg.
  }

  induction k as [|k IH].
  - simpl.
    intro H.
    apply Z.divide_1_l.
  - intro Hm.
    simpl in Hm.
    assert (Hqm : (F28_ppow p k | m)).
    {
      destruct Hm as [m' Hm'].
      exists (m'*p).
      rewrite Hm'.
      ring.
    }
    exact
      (F28_valuation_step
         p C m n C' (F28_ppow p k)
         Hp HC (F28_ppow_pos p Hgt k) Heq
         (IH Hqm) Hm).
Qed.

(* ------------------------------------------------------ *)
(* 13.2  REDUCTION TYPE OF AN INTEGRAL MODEL AT p         *)
(*       (Silverman, Ch. VII, section 1, used as the      *)
(*        definition; a model, not Q_p)                   *)
(* ------------------------------------------------------ *)

(* Minimality, in valuation form: a change of coordinates with
   rational scaling u = m/n and c4 = u^4 c4' (c4' an integer)
   has v_p(u) <= 0.  Then Delta = u^12 Delta' gives
   v_p(Delta') = v_p(Delta) - 12 v_p(u) >= v_p(Delta), so no
   change of coordinates lowers the discriminant valuation.
   The last step (Delta = u^12 Delta', valuations of Delta) is
   not formalised here. *)

Definition F28_scaling_minimal (p A : Z) : Prop :=
  forall m n C' : Z,
    n^4*F28_c4 A = m^4*C' ->
    forall k : nat,
      (F28_ppow p k | m) ->
      (F28_ppow p k | n).

(* A node of the reduced curve: a singular point exists, and at
   every singular point (x, y) the tangent cone v^2 - 3 x u^2 is
   nondegenerate (p does not divide 3x). *)

Definition F28_node_reduction (p A B : Z) : Prop :=
  (exists x : Z, F28_reduced_singular p A B x 0) /\
  (forall x y : Z,
     F28_reduced_singular p A B x y ->
     ~ (p | 3*x)).

Definition F28_multiplicative_reduction (p A B : Z) : Prop :=
  F28_scaling_minimal p A /\
  F28_node_reduction p A B.

Definition F28_split_multiplicative (p A B : Z) : Prop :=
  F28_multiplicative_reduction p A B /\
  (forall x y : Z,
     F28_reduced_singular p A B x y ->
     F28_rational_tangent_directions p x).

Definition F28_nonsplit_multiplicative (p A B : Z) : Prop :=
  F28_multiplicative_reduction p A B /\
  (forall x y : Z,
     F28_reduced_singular p A B x y ->
     ~ F28_rational_tangent_directions p x).

Theorem F28_scaling_minimal_model :
  forall p a c : Z,
    prime p ->
    5 <= p ->
    ~ (p | a) ->
    ~ (p | c) ->
    F28_scaling_minimal p (F28_A a c).
Proof.
  intros p a c Hp Hlarge Ha Hc.
  unfold F28_scaling_minimal.
  intros m n C' Heq k.
  exact
    (F28_valuation_bound
       p (F28_c4 (F28_A a c)) m n C'
       Hp
       (F28_c4_nonzero p a c Hp Hlarge Ha Hc)
       Heq k).
Qed.

(* ------------------------------------------------------ *)
(* 13.3  THE DISCRIMINANT IS NONZERO                      *)
(* ------------------------------------------------------ *)

Theorem F28_discriminant_nonzero :
  forall p a b c : Z,
    prime p ->
    ~ (p | c) ->
    F28_F a b c <> 0 ->
    F28_discriminant (F28_A a c) (F28_B b c) <> 0.
Proof.
  intros p a b c Hp Hc HF Hzero.
  rewrite F28_discriminant_identity in Hzero.

  assert (Hc0 : c <> 0).
  {
    intro H0.
    apply Hc.
    rewrite H0.
    exists 0.
    ring.
  }

  assert (Hc9 : c^9 <> 0).
  {
    apply Z.pow_nonzero.
    - exact Hc0.
    - lia.
  }

  assert (H1024 : -1024*c^9 <> 0).
  {
    intro H.
    apply Z.mul_eq_0 in H.
    destruct H as [H | H].
    - lia.
    - exact (Hc9 H).
  }

  apply Z.mul_eq_0 in Hzero.
  destruct Hzero as [H | H].
  - exact (H1024 H).
  - exact (HF H).
Qed.

(* ------------------------------------------------------ *)
(* 13.4  MULTIPLICATIVE REDUCTION OF THE MODEL            *)
(* ------------------------------------------------------ *)

Theorem F28_model_multiplicative_reduction :
  forall p a b c : Z,
    prime p ->
    5 <= p ->
    ~ (p | a) ->
    ~ (p | c) ->
    (p | F28_F a b c) ->
    F28_multiplicative_reduction
      p (F28_A a c) (F28_B b c).
Proof.
  intros p a b c Hp Hlarge Ha Hc HF.
  unfold F28_multiplicative_reduction.
  split.
  - exact
      (F28_scaling_minimal_model
         p a c Hp Hlarge Ha Hc).
  - unfold F28_node_reduction.
    split.
    + destruct
        (F28_double_root_exists
           p a b c Hp Hlarge Ha Hc HF)
        as [r [Hf Hd]].
      exists r.
      exact
        (F28_reduced_singular_intro
           p (F28_A a c) (F28_B b c) r Hf Hd).
    + intros x y Hsing.
      exact
        (proj1
          (proj2
            (F28_reduced_singular_node
               p a b c x y
               Hp Hlarge Ha Hc Hsing))).
Qed.

Theorem F28_model_split_multiplicative_iff :
  forall p a b c : Z,
    prime p ->
    5 <= p ->
    ~ (p | a) ->
    ~ (p | b) ->
    ~ (p | c) ->
    (p | F28_F a b c) ->
    (F28_split_multiplicative
       p (F28_A a c) (F28_B b c) <->
     F28_square_certificate p (a*b)).
Proof.
  intros p a b c Hp Hlarge Ha Hb Hc HF.

  pose proof
    (F28_model_multiplicative_reduction
       p a b c Hp Hlarge Ha Hc HF)
    as Hmult.

  pose proof Hmult as Hmult0.
  unfold F28_multiplicative_reduction in Hmult.
  unfold F28_node_reduction in Hmult.
  destruct Hmult as [Hmin [[x Hx] Hthree]].

  unfold F28_split_multiplicative.
  split.
  - intros [_ Hdir].
    assert (Hsc : F28_split_node_certificate p x).
    {
      unfold F28_split_node_certificate.
      split.
      - exact (Hthree x 0 Hx).
      - exact (Hdir x 0 Hx).
    }
    exact
      (proj1
        (F28_reduced_node_split_criterion
           p a b c x 0
           Hp Hlarge Ha Hb Hc Hx)
        Hsc).
  - intro Hsq.
    split.
    + exact Hmult0.
    + intros x' y' Hsing.
      pose proof
        (F28_reduced_node_split_criterion
           p a b c x' y'
           Hp Hlarge Ha Hb Hc Hsing)
        as Hcrit.
      pose proof (proj2 Hcrit Hsq) as Hsc.
      unfold F28_split_node_certificate in Hsc.
      exact (proj2 Hsc).
Qed.

Theorem F28_model_nonsplit_multiplicative_iff :
  forall p a b c : Z,
    prime p ->
    5 <= p ->
    ~ (p | a) ->
    ~ (p | b) ->
    ~ (p | c) ->
    (p | F28_F a b c) ->
    (F28_nonsplit_multiplicative
       p (F28_A a c) (F28_B b c) <->
     ~ F28_square_certificate p (a*b)).
Proof.
  intros p a b c Hp Hlarge Ha Hb Hc HF.

  pose proof
    (F28_model_multiplicative_reduction
       p a b c Hp Hlarge Ha Hc HF)
    as Hmult.

  pose proof Hmult as Hmult0.
  unfold F28_multiplicative_reduction in Hmult.
  unfold F28_node_reduction in Hmult.
  destruct Hmult as [Hmin [[x Hx] Hthree]].

  unfold F28_nonsplit_multiplicative.
  split.
  - intros [_ Hnot] Hsq.
    apply (Hnot x 0 Hx).
    pose proof
      (F28_reduced_node_split_criterion
         p a b c x 0
         Hp Hlarge Ha Hb Hc Hx)
      as Hcrit.
    pose proof (proj2 Hcrit Hsq) as Hsc.
    unfold F28_split_node_certificate in Hsc.
    exact (proj2 Hsc).
  - intro Hnot.
    split.
    + exact Hmult0.
    + intros x' y' Hsing Hdir.
      apply Hnot.
      pose proof
        (F28_reduced_node_split_criterion
           p a b c x' y'
           Hp Hlarge Ha Hb Hc Hsing)
        as Hcrit.
      apply (proj1 Hcrit).
      unfold F28_split_node_certificate.
      split.
      * exact (Hthree x' y' Hsing).
      * exact Hdir.
Qed.

(* ------------------------------------------------------ *)
(* 13.5  BRANCHES OF THE NORMALIZATION = TANGENT DIRECTIONS *)
(* ------------------------------------------------------ *)

Lemma F28_square_certificate_to_mod :
  forall p z : Z,
    prime p ->
    F28_square_certificate p z ->
    F28_square_mod p z.
Proof.
  intros p z Hp Hcert.
  unfold F28_square_certificate in Hcert.
  destruct Hcert as [u [v [Hu Hc]]].
  destruct (F28_prime_inverse p u Hp Hu) as [w Hw].
  destruct Hc as [k Hk].
  destruct Hw as [l Hl].
  exists (v*w).
  exists (-w^2*k + z*(u*w+1)*l).
  assert (E :
    (-w^2*k + z*(u*w+1)*l)*p =
    -w^2*(k*p) + z*(u*w+1)*(l*p)) by ring.
  rewrite E.
  rewrite <- Hk.
  rewrite <- Hl.
  ring.
Qed.

Lemma F28_square_mod_to_certificate :
  forall p z : Z,
    5 <= p ->
    F28_square_mod p z ->
    F28_square_certificate p z.
Proof.
  intros p z Hlarge Hmod.
  destruct Hmod as [t Ht].
  unfold F28_square_certificate.
  exists 1, t.
  split.
  - apply F28_not_divide_small; lia.
  - replace (z*1^2 - t^2) with (-(t^2 - z)) by ring.
    exact (F28_divide_neg p _ Ht).
Qed.

Theorem F28_branches_iff_tangent_directions :
  forall p r : Z,
    prime p ->
    5 <= p ->
    ~ (p | 3*r) ->
    (F28_split_branches p r <->
     F28_rational_tangent_directions p r).
Proof.
  intros p r Hp Hlarge Hr.
  pose proof
    (F28_stage10_split_iff_square p r Hp Hr) as H1.
  pose proof
    (F28_tangent_square_equivalence p r) as H2.
  pose proof
    (F28_square_certificate_to_mod p (3*r) Hp) as H3.
  pose proof
    (F28_square_mod_to_certificate p (3*r) Hlarge) as H4.
  tauto.
Qed.

(* ------------------------------------------------------ *)
(* 13.6  THE STAGE 13 THEOREM                             *)
(* ------------------------------------------------------ *)

Theorem F28_stage13_multiplicative_reduction :
  forall p a b c : Z,
    prime p ->
    5 <= p ->
    ~ (p | a) ->
    ~ (p | b) ->
    ~ (p | c) ->
    (p | F28_F a b c) ->
    F28_F a b c <> 0 ->
    (p | F28_discriminant (F28_A a c) (F28_B b c))
    /\
    ~ (p | F28_c4 (F28_A a c))
    /\
    F28_discriminant (F28_A a c) (F28_B b c) <> 0
    /\
    F28_multiplicative_reduction
      p (F28_A a c) (F28_B b c)
    /\
    (forall x y : Z,
       F28_reduced_singular
         p (F28_A a c) (F28_B b c) x y ->
       F28_factorization_certificate
         p (F28_A a c) (F28_B b c) x)
    /\
    (forall x y : Z,
       F28_reduced_singular
         p (F28_A a c) (F28_B b c) x y ->
       forall t : Z,
         (p | F28_norm_y x t ^ 2 -
              F28_cubic (F28_A a c) (F28_B b c)
                (F28_norm_x x t)))
    /\
    (forall x y : Z,
       F28_reduced_singular
         p (F28_A a c) (F28_B b c) x y ->
       (F28_split_branches p x <->
        F28_rational_tangent_directions p x))
    /\
    (forall x y : Z,
       F28_reduced_singular
         p (F28_A a c) (F28_B b c) x y ->
       (F28_split_branches p x <->
        F28_square_mod p (a*b)))
    /\
    (F28_split_multiplicative
       p (F28_A a c) (F28_B b c) <->
     F28_square_certificate p (a*b))
    /\
    (F28_nonsplit_multiplicative
       p (F28_A a c) (F28_B b c) <->
     ~ F28_square_certificate p (a*b)).
Proof.
  intros p a b c Hp Hlarge Ha Hb Hc HF HF0.

  assert (Hab : ~ (p | a*b)).
  {
    exact (F28_prime_product_nonzero p a b Hp Ha Hb).
  }

  assert (H1 :
    (p | F28_discriminant (F28_A a c) (F28_B b c))).
  {
    exact (F28_discriminant_vanishes p a b c HF).
  }

  assert (H2 : ~ (p | F28_c4 (F28_A a c))).
  {
    exact (F28_c4_nonzero p a c Hp Hlarge Ha Hc).
  }

  assert (H3 :
    F28_discriminant (F28_A a c) (F28_B b c) <> 0).
  {
    exact (F28_discriminant_nonzero p a b c Hp Hc HF0).
  }

  assert (H4 :
    F28_multiplicative_reduction
      p (F28_A a c) (F28_B b c)).
  {
    exact
      (F28_model_multiplicative_reduction
         p a b c Hp Hlarge Ha Hc HF).
  }

  assert (H5 :
    forall x y : Z,
      F28_reduced_singular
        p (F28_A a c) (F28_B b c) x y ->
      F28_factorization_certificate
        p (F28_A a c) (F28_B b c) x).
  {
    intros x y Hsing.
    destruct
      (F28_reduced_singular_split
         p (F28_A a c) (F28_B b c) x y
         Hp Hlarge Hsing)
      as [Hy [Hf Hd]].
    destruct
      (F28_reduced_singular_node
         p a b c x y Hp Hlarge Ha Hc Hsing)
      as [Hx [Hthree Htan]].
    exact
      (F28_stage8_factorization
         p (F28_A a c) (F28_B b c) x
         Hp Hthree Hf Hd).
  }

  assert (H6 :
    forall x y : Z,
      F28_reduced_singular
        p (F28_A a c) (F28_B b c) x y ->
      forall t : Z,
        (p | F28_norm_y x t ^ 2 -
             F28_cubic (F28_A a c) (F28_B b c)
               (F28_norm_x x t))).
  {
    intros x y Hsing t.
    destruct
      (F28_reduced_singular_split
         p (F28_A a c) (F28_B b c) x y
         Hp Hlarge Hsing)
      as [Hy [Hf Hd]].
    exact
      (F28_stage9_reduced_model_parametrization
         p (F28_A a c) (F28_B b c) x t Hf Hd).
  }

  assert (H7 :
    forall x y : Z,
      F28_reduced_singular
        p (F28_A a c) (F28_B b c) x y ->
      (F28_split_branches p x <->
       F28_rational_tangent_directions p x)).
  {
    intros x y Hsing.
    destruct
      (F28_reduced_singular_node
         p a b c x y Hp Hlarge Ha Hc Hsing)
      as [Hx [Hthree Htan]].
    exact
      (F28_branches_iff_tangent_directions
         p x Hp Hlarge Hthree).
  }

  assert (H8 :
    forall x y : Z,
      F28_reduced_singular
        p (F28_A a c) (F28_B b c) x y ->
      (F28_split_branches p x <->
       F28_square_mod p (a*b))).
  {
    intros x y Hsing.
    destruct
      (F28_reduced_singular_split
         p (F28_A a c) (F28_B b c) x y
         Hp Hlarge Hsing)
      as [Hy [Hf Hd]].
    destruct
      (F28_reduced_singular_node
         p a b c x y Hp Hlarge Ha Hc Hsing)
      as [Hx [Hthree Htan]].
    exact
      (F28_stage12_split_iff_ab
         p a b c x Hp Hthree Hab
         (F28_singular_linear_relation
            p a b c x Hp Hlarge Hc Hf Hd)).
  }

  assert (H9 :
    F28_split_multiplicative
      p (F28_A a c) (F28_B b c) <->
    F28_square_certificate p (a*b)).
  {
    exact
      (F28_model_split_multiplicative_iff
         p a b c Hp Hlarge Ha Hb Hc HF).
  }

  assert (H10 :
    F28_nonsplit_multiplicative
      p (F28_A a c) (F28_B b c) <->
    ~ F28_square_certificate p (a*b)).
  {
    exact
      (F28_model_nonsplit_multiplicative_iff
         p a b c Hp Hlarge Ha Hb Hc HF).
  }

  exact
    (conj H1
      (conj H2
        (conj H3
          (conj H4
            (conj H5
              (conj H6
                (conj H7
                  (conj H8
                    (conj H9 H10))))))))).
Qed.

(* ====================================================== *)
(* NEW IN STAGE 14 (written in review by Claude)          *)
(* ====================================================== *)

(* ------------------------------------------------------ *)
(* 14.0  SMALL GENERAL LEMMAS                             *)
(* ------------------------------------------------------ *)

Lemma F28_cancel_nonzero :
  forall k x y : Z,
    k <> 0 ->
    k*x = k*y ->
    x = y.
Proof.
  intros k x y Hk H.
  exact (proj1 (Z.mul_cancel_l x y k Hk) H).
Qed.

Lemma F28_prime_divides_square :
  forall p x : Z,
    prime p ->
    (p | x^2) ->
    (p | x).
Proof.
  intros p x Hp H.
  replace (x^2) with (x*x) in H by ring.
  destruct (prime_mult p Hp x x H) as [H1 | H1].
  - exact H1.
  - exact H1.
Qed.

Lemma F28_prime_divides_cube :
  forall p x : Z,
    prime p ->
    (p | x^3) ->
    (p | x).
Proof.
  intros p x Hp H.
  replace (x^3) with (x*(x*x)) in H by ring.
  destruct (prime_mult p Hp x (x*x) H) as [H1 | H2].
  - exact H1.
  - destruct (prime_mult p Hp x x H2) as [H3 | H3].
    + exact H3.
    + exact H3.
Qed.

(* ------------------------------------------------------ *)
(* 14.1  THE -c6 CRITERION                                *)
(* ------------------------------------------------------ *)

(* The paper's criterion: the node is split iff -c6 is a
   square mod p.  Here c6 = -864 B (F28_c6), so -c6 = 864 B. *)

Definition F28_minus_c6 (B : Z) : Z :=
  864*B.

Lemma F28_minus_c6_is_minus_c6 :
  forall B : Z,
    F28_minus_c6 B = - F28_c6 B.
Proof.
  intro B.
  unfold F28_minus_c6, F28_c6.
  ring.
Qed.

Lemma F28_certificate_transfer :
  forall p x y : Z,
    (p | x-y) ->
    F28_square_certificate p x ->
    F28_square_certificate p y.
Proof.
  intros p x y Hxy Hcert.
  destruct Hxy as [k Hk].
  destruct Hcert as [u [v [Hu [l Hl]]]].
  exists u, v.
  split.
  - exact Hu.
  - exists (l - k*u^2).
    assert (E : y*u^2 - v^2 = (x*u^2 - v^2) - (x-y)*u^2) by ring.
    rewrite E.
    rewrite Hl.
    rewrite Hk.
    ring.
Qed.

Lemma F28_certificate_congruence :
  forall p x y : Z,
    (p | x-y) ->
    (F28_square_certificate p x <-> F28_square_certificate p y).
Proof.
  intros p x y Hxy.
  split.
  - apply F28_certificate_transfer.
    exact Hxy.
  - apply F28_certificate_transfer.
    replace (y-x) with (-(x-y)) by ring.
    exact (F28_divide_neg p (x-y) Hxy).
Qed.

Lemma F28_certificate_scaling :
  forall p x w : Z,
    prime p ->
    ~ (p | w) ->
    (F28_square_certificate p (x*w^2) <->
     F28_square_certificate p x).
Proof.
  intros p x w Hp Hw.
  split.
  - intros [u [v [Hu Hd]]].
    exists (u*w), v.
    split.
    + exact (F28_prime_product_nonzero p u w Hp Hu Hw).
    + replace (x*(u*w)^2 - v^2) with (x*w^2*u^2 - v^2) by ring.
      exact Hd.
  - intros [u [v [Hu [l Hl]]]].
    exists u, (v*w).
    split.
    + exact Hu.
    + exists (w^2*l).
      replace (x*w^2*u^2 - (v*w)^2) with (w^2*(x*u^2 - v^2)) by ring.
      rewrite Hl.
      ring.
Qed.

(* At a double root r of f mod p: B = 2 r^3, so
   864 B = 1728 r^3 = (3 r) (24 r)^2. *)

Lemma F28_minus_c6_vs_three_r :
  forall p A B r : Z,
    prime p ->
    5 <= p ->
    (p | F28_cubic A B r) ->
    (p | F28_derivative A r) ->
    ~ (p | 3*r) ->
    (F28_square_certificate p (F28_minus_c6 B) <->
     F28_square_certificate p (3*r)).
Proof.
  intros p A B r Hp Hlarge Hf Hd Hr.

  assert (HB : (p | B - 2*r^3)).
  {
    replace (B - 2*r^3)
      with (F28_cubic A B r - F28_derivative A r * r)
      by (unfold F28_cubic, F28_derivative; ring).
    apply F28_divide_sub.
    - exact Hf.
    - apply F28_divide_mul.
      exact Hd.
  }

  assert (Hcong : (p | F28_minus_c6 B - 3*r*(24*r)^2)).
  {
    replace (F28_minus_c6 B - 3*r*(24*r)^2)
      with ((B - 2*r^3)*864)
      by (unfold F28_minus_c6; ring).
    apply F28_divide_mul.
    exact HB.
  }

  assert (H24r : ~ (p | 24*r)).
  {
    replace (24*r) with (8*(3*r)) by ring.
    apply F28_prime_product_nonzero.
    - exact Hp.
    - apply F28_eight_nonzero; assumption.
    - exact Hr.
  }

  pose proof (F28_certificate_congruence p _ _ Hcong) as H1.
  pose proof (F28_certificate_scaling p (3*r) (24*r) Hp H24r) as H2.
  tauto.
Qed.

Theorem F28_model_minus_c6_criterion :
  forall p a b c : Z,
    prime p ->
    5 <= p ->
    ~ (p | a) ->
    ~ (p | b) ->
    ~ (p | c) ->
    (p | F28_F a b c) ->
    (F28_square_certificate p (F28_minus_c6 (F28_B b c)) <->
     F28_square_certificate p (a*b)).
Proof.
  intros p a b c Hp Hlarge Ha Hb Hc HF.

  pose proof
    (F28_model_multiplicative_reduction
       p a b c Hp Hlarge Ha Hc HF)
    as Hmult.
  unfold F28_multiplicative_reduction in Hmult.
  unfold F28_node_reduction in Hmult.
  destruct Hmult as [Hmin [[x Hx] Hthree]].

  destruct
    (F28_reduced_singular_split
       p (F28_A a c) (F28_B b c) x 0
       Hp Hlarge Hx)
    as [Hy [Hf Hd]].

  pose proof
    (F28_minus_c6_vs_three_r
       p (F28_A a c) (F28_B b c) x
       Hp Hlarge Hf Hd (Hthree x 0 Hx))
    as H1.

  pose proof
    (F28_reduced_node_split_criterion
       p a b c x 0
       Hp Hlarge Ha Hb Hc Hx)
    as H2.
  unfold F28_split_node_certificate in H2.

  pose proof (F28_tangent_square_equivalence p x) as H3.

  pose proof (Hthree x 0 Hx) as H4.

  tauto.
Qed.

Theorem F28_model_split_iff_minus_c6 :
  forall p a b c : Z,
    prime p ->
    5 <= p ->
    ~ (p | a) ->
    ~ (p | b) ->
    ~ (p | c) ->
    (p | F28_F a b c) ->
    (F28_split_multiplicative
       p (F28_A a c) (F28_B b c) <->
     F28_square_certificate p (F28_minus_c6 (F28_B b c)))
    /\
    (F28_nonsplit_multiplicative
       p (F28_A a c) (F28_B b c) <->
     ~ F28_square_certificate p (F28_minus_c6 (F28_B b c))).
Proof.
  intros p a b c Hp Hlarge Ha Hb Hc HF.
  pose proof
    (F28_model_minus_c6_criterion
       p a b c Hp Hlarge Ha Hb Hc HF) as H1.
  pose proof
    (F28_model_split_multiplicative_iff
       p a b c Hp Hlarge Ha Hb Hc HF) as H2.
  pose proof
    (F28_model_nonsplit_multiplicative_iff
       p a b c Hp Hlarge Ha Hb Hc HF) as H3.
  split; tauto.
Qed.

(* ------------------------------------------------------ *)
(* 14.2  THE PYTHAGOREAN FAMILY                           *)
(* ------------------------------------------------------ *)

(* The paper's polynomial (section 1, F.28):
     F_paper(U,V) = U^6 - 30 U^4 V^2 - 24 U^2 V^4 - V^6.
   (a, b, c) = ((V^2-U^2)/d, 2UV/d, (U^2+V^2)/d), d in {1, 2},
   is encoded by d*a = V^2-U^2, d*b = 2UV, d*c = U^2+V^2.
   F28_F is the polynomial of the primitive triple;
   d^3 F28_F = -4 F_paper (F28_family_normalization). *)

Definition F28_F_paper (U V : Z) : Z :=
  U^6 - 30*U^4*V^2 - 24*U^2*V^4 - V^6.

Definition F28_family (d U V a b c : Z) : Prop :=
  d*a = V^2 - U^2 /\
  d*b = 2*U*V /\
  d*c = U^2 + V^2.

Lemma F28_family_normalization :
  forall d U V a b c : Z,
    F28_family d U V a b c ->
    d^3 * F28_F a b c = -4 * F28_F_paper U V.
Proof.
  intros d U V a b c [Ha [Hb Hc]].
  unfold F28_F, F28_F_paper.
  replace (d^3 * (4*a^3 + 27*b^2*c))
    with (4*(d*a)^3 + 27*(d*b)^2*(d*c)) by ring.
  rewrite Ha, Hb, Hc.
  ring.
Qed.

Lemma F28_family_pythagorean :
  forall d U V a b c : Z,
    d <> 0 ->
    F28_family d U V a b c ->
    a^2 + b^2 = c^2.
Proof.
  intros d U V a b c Hd [Ha [Hb Hc]].
  assert (Hd2 : d^2 <> 0).
  {
    apply Z.pow_nonzero.
    - exact Hd.
    - lia.
  }
  apply (F28_cancel_nonzero (d^2) _ _ Hd2).
  replace (d^2*(a^2+b^2)) with ((d*a)^2 + (d*b)^2) by ring.
  replace (d^2*c^2) with ((d*c)^2) by ring.
  rewrite Ha, Hb, Hc.
  ring.
Qed.

(* p odd and not dividing both U and V: p does not divide
   both a and b (the triple is primitive at p). *)

Lemma F28_family_primitive_at_p :
  forall p d U V a b c : Z,
    prime p ->
    5 <= p ->
    F28_family d U V a b c ->
    ~ ((p | U) /\ (p | V)) ->
    ~ ((p | a) /\ (p | b)).
Proof.
  intros p d U V a b c Hp Hlarge [Ha [Hb Hc]] Hcop [Hpa Hpb].

  assert (H2 : ~ (p | 2)).
  {
    apply F28_not_divide_small; lia.
  }

  assert (Hdiff : (p | V^2 - U^2)).
  {
    rewrite <- Ha.
    replace (d*a) with (a*d) by ring.
    apply F28_divide_mul.
    exact Hpa.
  }

  assert (H2UV : (p | 2*(U*V))).
  {
    replace (2*(U*V)) with (2*U*V) by ring.
    rewrite <- Hb.
    replace (d*b) with (b*d) by ring.
    apply F28_divide_mul.
    exact Hpb.
  }

  pose proof (F28_prime_cancel p 2 (U*V) Hp H2 H2UV) as HUV.
  destruct (prime_mult p Hp U V HUV) as [HU | HV].
  - apply Hcop.
    split.
    + exact HU.
    + apply F28_prime_divides_square; [exact Hp |].
      replace (V^2) with ((V^2 - U^2) + U*U) by ring.
      apply F28_divide_add.
      * exact Hdiff.
      * apply F28_divide_mul.
        exact HU.
  - apply Hcop.
    split.
    + apply F28_prime_divides_square; [exact Hp |].
      replace (U^2) with (V*V - (V^2 - U^2)) by ring.
      apply F28_divide_sub.
      * apply F28_divide_mul.
        exact HV.
      * exact Hdiff.
    + exact HV.
Qed.

(* p | F, p >= 5, a^2 + b^2 = c^2, (a, b) not both divisible by p:
   then p divides none of a, b, c. *)

Lemma F28_pythagorean_large_prime :
  forall p a b c : Z,
    prime p ->
    5 <= p ->
    a^2 + b^2 = c^2 ->
    ~ ((p | a) /\ (p | b)) ->
    (p | F28_F a b c) ->
    ~ (p | a) /\ ~ (p | b) /\ ~ (p | c).
Proof.
  intros p a b c Hp Hlarge Hpyth Hprim HF.

  assert (H2 : ~ (p | 2)).
  {
    apply F28_not_divide_small; lia.
  }
  assert (H3 : ~ (p | 3)).
  {
    apply F28_not_divide_small; lia.
  }
  assert (H4 : ~ (p | 4)).
  {
    apply F28_prime_4_nonzero; assumption.
  }
  assert (H27 : ~ (p | 27)).
  {
    replace 27 with (3^3) by ring.
    apply F28_prime_cube_nonzero; assumption.
  }

  (* p | F and p | a  =>  p | 27 b^2 c *)
  assert (Hfrom_a :
    (p | a) -> (p | 27*b^2*c)).
  {
    intro Hpa.
    replace (27*b^2*c) with (F28_F a b c - a*(4*a^2))
      by (unfold F28_F; ring).
    apply F28_divide_sub.
    - exact HF.
    - apply F28_divide_mul.
      exact Hpa.
  }

  (* p | F and p | 27 b^2 c  =>  p | a *)
  assert (Hto_a :
    (p | 27*b^2*c) -> (p | a)).
  {
    intro H.
    assert (H4a : (p | 4*a^3)).
    {
      replace (4*a^3) with (F28_F a b c - 27*b^2*c)
        by (unfold F28_F; ring).
      apply F28_divide_sub.
      - exact HF.
      - exact H.
    }
    apply F28_prime_divides_cube; [exact Hp |].
    exact (F28_prime_cancel p 4 (a^3) Hp H4 H4a).
  }

  (* p | 27 b^2 c  =>  p | b or p | c *)
  assert (Hsplit :
    (p | 27*b^2*c) -> (p | b) \/ (p | c)).
  {
    intro H.
    destruct (prime_mult p Hp (27*b^2) c H) as [H1 | H1].
    - left.
      destruct (prime_mult p Hp 27 (b^2) H1) as [H5 | H5].
      + exfalso.
        exact (H27 H5).
      + exact (F28_prime_divides_square p b Hp H5).
    - right.
      exact H1.
  }

  (* p | c and p | a  =>  p | b *)
  assert (Hc_to_b :
    (p | c) -> (p | a) -> (p | b)).
  {
    intros Hpc Hpa.
    apply F28_prime_divides_square; [exact Hp |].
    replace (b^2) with (c*c - a*a) by nia.
    apply F28_divide_sub.
    - apply F28_divide_mul.
      exact Hpc.
    - apply F28_divide_mul.
      exact Hpa.
  }

  assert (Ha : ~ (p | a)).
  {
    intro Hpa.
    destruct (Hsplit (Hfrom_a Hpa)) as [Hpb | Hpc].
    - exact (Hprim (conj Hpa Hpb)).
    - exact (Hprim (conj Hpa (Hc_to_b Hpc Hpa))).
  }

  assert (Hb : ~ (p | b)).
  {
    intro Hpb.
    apply Ha.
    apply Hto_a.
    replace (27*b^2*c) with (b*(27*b*c)) by ring.
    apply F28_divide_mul.
    exact Hpb.
  }

  assert (Hc : ~ (p | c)).
  {
    intro Hpc.
    apply Ha.
    apply Hto_a.
    replace (27*b^2*c) with (c*(27*b^2)) by ring.
    apply F28_divide_mul.
    exact Hpc.
  }

  exact (conj Ha (conj Hb Hc)).
Qed.

(* p | F_paper iff p | F28_F, for p >= 5 and d in {1, 2}. *)

Lemma F28_divides_F_iff :
  forall p d U V a b c : Z,
    prime p ->
    5 <= p ->
    (d = 1 \/ d = 2) ->
    F28_family d U V a b c ->
    ((p | F28_F a b c) <-> (p | F28_F_paper U V)).
Proof.
  intros p d U V a b c Hp Hlarge Hd Hfam.
  pose proof (F28_family_normalization d U V a b c Hfam) as Hn.

  assert (H4 : ~ (p | 4)).
  {
    apply F28_prime_4_nonzero; assumption.
  }

  assert (Hnd3 : ~ (p | d^3)).
  {
    destruct Hd as [Hd1 | Hd2].
    - rewrite Hd1.
      replace (1^3) with 1 by ring.
      apply F28_not_divide_small; lia.
    - rewrite Hd2.
      replace (2^3) with 8 by ring.
      apply F28_eight_nonzero; assumption.
  }

  split.
  - intro HF.
    assert (E : 4 * F28_F_paper U V = -(d^3 * F28_F a b c)).
    {
      rewrite Hn.
      ring.
    }
    apply (F28_prime_cancel p 4 (F28_F_paper U V) Hp H4).
    rewrite E.
    apply F28_divide_neg.
    replace (d^3 * F28_F a b c) with (F28_F a b c * d^3) by ring.
    apply F28_divide_mul.
    exact HF.
  - intro HFp.
    apply (F28_prime_cancel p (d^3) (F28_F a b c) Hp Hnd3).
    rewrite Hn.
    replace (-4 * F28_F_paper U V) with (F28_F_paper U V * (-4)) by ring.
    apply F28_divide_mul.
    exact HFp.
Qed.

(* F_paper is nonzero when U, V are not both even. *)

Lemma F28_odd_form :
  forall F H : Z,
    F = 2*H + 1 ->
    F <> 0.
Proof.
  intros F H E.
  lia.
Qed.

Lemma F28_odd_form_neg :
  forall F H : Z,
    F = 2*H - 1 ->
    F <> 0.
Proof.
  intros F H E.
  lia.
Qed.

Lemma F28_two_mod_four_form :
  forall F H : Z,
    F = 4*H + 2 ->
    F <> 0.
Proof.
  intros F H E.
  lia.
Qed.

Theorem F28_F_paper_nonzero :
  forall U V : Z,
    ~ ((2 | U) /\ (2 | V)) ->
    F28_F_paper U V <> 0.
Proof.
  intros U V Hcop.
  destruct (Z.Even_or_Odd U) as [[k Hk] | [k Hk]];
  destruct (Z.Even_or_Odd V) as [[l Hl] | [l Hl]].
  - (* both even: excluded *)
    exfalso.
    apply Hcop.
    split.
    + exists k. lia.
    + exists l. lia.
  - (* U even, V odd *)
    apply (F28_odd_form_neg _
      (32*k^6 - 15*U^4*V^2 - 12*U^2*V^4
       - l*(V^5 + V^4 + V^3 + V^2 + V + 1))).
    unfold F28_F_paper.
    subst U V.
    ring.
  - (* U odd, V even *)
    apply (F28_odd_form _
      (k*(U^5 + U^4 + U^3 + U^2 + U + 1)
       - 32*l^6 - 15*U^4*V^2 - 12*U^2*V^4)).
    unfold F28_F_paper.
    subst U V.
    ring.
  - (* both odd *)
    apply (F28_two_mod_four_form _
      (-81*(k*(k+1)) - 81*(l*(l+1))
       - 108*(k*(k+1))^2 - 108*(l*(l+1))^2
       - 432*(k*(k+1))*(l*(l+1))
       + 16*(k*(k+1))^3 - 16*(l*(l+1))^3
       - 480*(k*(k+1))^2*(l*(l+1))
       - 384*(k*(k+1))*(l*(l+1))^2 - 14)).
    unfold F28_F_paper.
    subst U V.
    ring.
Qed.

Theorem F28_family_F_nonzero :
  forall d U V a b c : Z,
    F28_family d U V a b c ->
    ~ ((2 | U) /\ (2 | V)) ->
    F28_F a b c <> 0.
Proof.
  intros d U V a b c Hfam Hcop H0.
  pose proof (F28_family_normalization d U V a b c Hfam) as Hn.
  rewrite H0 in Hn.
  replace (d^3 * 0) with 0 in Hn by ring.
  apply (F28_F_paper_nonzero U V Hcop).
  lia.
Qed.

(* Everything about the family needed by the stages above. *)

Theorem F28_family_hypotheses :
  forall p d U V a b c : Z,
    prime p ->
    5 <= p ->
    (d = 1 \/ d = 2) ->
    F28_family d U V a b c ->
    ~ ((2 | U) /\ (2 | V)) ->
    ~ ((p | U) /\ (p | V)) ->
    (p | F28_F_paper U V) ->
    (p | F28_F a b c) /\
    F28_F a b c <> 0 /\
    ~ (p | a) /\ ~ (p | b) /\ ~ (p | c).
Proof.
  intros p d U V a b c Hp Hlarge Hd Hfam Hcop2 Hcopp HFp.

  assert (Hd0 : d <> 0).
  {
    destruct Hd as [H | H]; lia.
  }

  pose proof
    (proj2 (F28_divides_F_iff p d U V a b c Hp Hlarge Hd Hfam) HFp)
    as HF.

  pose proof
    (F28_pythagorean_large_prime
       p a b c Hp Hlarge
       (F28_family_pythagorean d U V a b c Hd0 Hfam)
       (F28_family_primitive_at_p
          p d U V a b c Hp Hlarge Hfam Hcopp)
       HF)
    as [Ha [Hb Hc]].

  exact
    (conj HF
      (conj (F28_family_F_nonzero d U V a b c Hfam Hcop2)
        (conj Ha (conj Hb Hc)))).
Qed.

(* ------------------------------------------------------ *)
(* 14.3  WEIERSTRASS INVARIANTS AND CHANGE OF COORDINATES *)
(* ------------------------------------------------------ *)

(* General integral Weierstrass equation
     y^2 + a1 xy + a3 y = x^3 + a2 x^2 + a4 x + a6.
   Standard invariants (Silverman, III.1). *)

Definition F28_W_b2 (a1 a2 : Z) : Z :=
  a1^2 + 4*a2.

Definition F28_W_b4 (a1 a3 a4 : Z) : Z :=
  2*a4 + a1*a3.

Definition F28_W_b6 (a3 a6 : Z) : Z :=
  a3^2 + 4*a6.

Definition F28_W_b8 (a1 a2 a3 a4 a6 : Z) : Z :=
  a1^2*a6 + 4*a2*a6 - a1*a3*a4 + a2*a3^2 - a4^2.

Definition F28_W_c4 (b2 b4 : Z) : Z :=
  b2^2 - 24*b4.

Definition F28_W_c6 (b2 b4 b6 : Z) : Z :=
  -b2^3 + 36*b2*b4 - 216*b6.

Definition F28_W_disc (b2 b4 b6 b8 : Z) : Z :=
  -b2^2*b8 - 8*b4^3 - 27*b6^2 + 9*b2*b4*b6.

(* The same, in terms of a1, ..., a6. *)

Definition F28_W_c4a (a1 a2 a3 a4 : Z) : Z :=
  F28_W_c4 (F28_W_b2 a1 a2) (F28_W_b4 a1 a3 a4).

Definition F28_W_c6a (a1 a2 a3 a4 a6 : Z) : Z :=
  F28_W_c6 (F28_W_b2 a1 a2) (F28_W_b4 a1 a3 a4) (F28_W_b6 a3 a6).

Definition F28_W_disca (a1 a2 a3 a4 a6 : Z) : Z :=
  F28_W_disc
    (F28_W_b2 a1 a2) (F28_W_b4 a1 a3 a4)
    (F28_W_b6 a3 a6) (F28_W_b8 a1 a2 a3 a4 a6).

(* For y^2 = x^3 + A x + B these are the invariants used above:
   c4 = -48 A, c6 = -864 B, Delta = -16 (4 A^3 + 27 B^2). *)

Theorem F28_W_short_model :
  forall A B : Z,
    F28_W_c4a 0 0 0 A = F28_c4 A /\
    F28_W_c6a 0 0 0 A B = F28_c6 B /\
    F28_W_disca 0 0 0 A B = F28_discriminant A B.
Proof.
  intros A B.
  unfold F28_W_c4a, F28_W_c6a, F28_W_disca.
  unfold F28_W_c4, F28_W_c6, F28_W_disc.
  unfold F28_W_b2, F28_W_b4, F28_W_b6, F28_W_b8.
  unfold F28_c4, F28_c6, F28_discriminant.
  repeat split; ring.
Qed.

Lemma F28_W_b8_relation :
  forall a1 a2 a3 a4 a6 : Z,
    4 * F28_W_b8 a1 a2 a3 a4 a6 =
    F28_W_b2 a1 a2 * F28_W_b6 a3 a6 - (F28_W_b4 a1 a3 a4)^2.
Proof.
  intros a1 a2 a3 a4 a6.
  unfold F28_W_b8, F28_W_b2, F28_W_b4, F28_W_b6.
  ring.
Qed.

(* 1728 Delta = c4^3 - c6^2, given 4 b8 = b2 b6 - b4^2. *)

Lemma F28_W_disc_identity :
  forall b2 b4 b6 b8 : Z,
    4*b8 = b2*b6 - b4^2 ->
    1728 * F28_W_disc b2 b4 b6 b8 =
    (F28_W_c4 b2 b4)^3 - (F28_W_c6 b2 b4 b6)^2.
Proof.
  intros b2 b4 b6 b8 H.
  unfold F28_W_disc, F28_W_c4, F28_W_c6.
  apply (F28_cancel_nonzero 4); [lia |].
  assert (E :
    4*(1728*(-b2^2*b8 - 8*b4^3 - 27*b6^2 + 9*b2*b4*b6)) =
    1728*(-b2^2*(4*b8) - 32*b4^3 - 108*b6^2 + 36*b2*b4*b6))
    by ring.
  rewrite E.
  rewrite H.
  ring.
Qed.

(* Scaling of the b-invariants under x = u^2 x' + r, u = m/n, r = R/n^2
   (cleared of denominators). *)

Lemma F28_W_c_scaling :
  forall b2 b4 b6 b2' b4' b6' m n R : Z,
    m^2*b2' = n^2*b2 + 12*R ->
    m^4*b4' = n^4*b4 + n^2*R*b2 + 6*R^2 ->
    m^6*b6' = n^6*b6 + 2*n^4*R*b4 + n^2*R^2*b2 + 4*R^3 ->
    m^4 * F28_W_c4 b2' b4' = n^4 * F28_W_c4 b2 b4 /\
    m^6 * F28_W_c6 b2' b4' b6' = n^6 * F28_W_c6 b2 b4 b6.
Proof.
  intros b2 b4 b6 b2' b4' b6' m n R H2 H4 H6.
  split.
  - unfold F28_W_c4.
    replace (m^4*(b2'^2 - 24*b4'))
      with ((m^2*b2')^2 - 24*(m^4*b4')) by ring.
    rewrite H2, H4.
    ring.
  - unfold F28_W_c6.
    replace (m^6*(-b2'^3 + 36*b2'*b4' - 216*b6'))
      with (-(m^2*b2')^3 + 36*(m^2*b2')*(m^4*b4') - 216*(m^6*b6'))
      by ring.
    rewrite H2, H4, H6.
    ring.
Qed.

Lemma F28_W_disc_scaling :
  forall c4 c6 D c4' c6' D' m n : Z,
    1728*D = c4^3 - c6^2 ->
    1728*D' = c4'^3 - c6'^2 ->
    m^4*c4' = n^4*c4 ->
    m^6*c6' = n^6*c6 ->
    m^12*D' = n^12*D.
Proof.
  intros c4 c6 D c4' c6' D' m n HD HD' H4 H6.
  apply (F28_cancel_nonzero 1728); [lia |].
  replace (1728*(m^12*D')) with (m^12*(1728*D')) by ring.
  rewrite HD'.
  replace (m^12*(c4'^3 - c6'^2))
    with ((m^4*c4')^3 - (m^6*c6')^2) by ring.
  rewrite H4, H6.
  replace ((n^4*c4)^3 - (n^6*c6)^2)
    with (n^12*(c4^3 - c6^2)) by ring.
  rewrite <- HD.
  ring.
Qed.

(* The change of coordinates x = u^2 x' + r, y = u^3 y' + s u^2 x' + t
   with u = m/n, r = R/n^2, s = S/n, t = T/n^3 (denominators cleared),
   between the integral Weierstrass models (a1, ..., a6) and
   (a1', ..., a6').  The hypotheses H1 ... H6 are the standard formulas
   u^i a_i' = ... multiplied by n^i.  Conclusion: u^4 c4' = c4,
   u^6 c6' = c6, u^12 Delta' = Delta (cleared of denominators). *)

Theorem F28_W_change_of_coordinates :
  forall a1 a2 a3 a4 a6 a1' a2' a3' a4' a6' m n R S T : Z,
    m*a1' = n*a1 + 2*S ->
    m^2*a2' = n^2*a2 - n*S*a1 + 3*R - S^2 ->
    m^3*a3' = n^3*a3 + n*R*a1 + 2*T ->
    m^4*a4' = n^4*a4 - n^3*S*a3 + 2*n^2*R*a2
              - n*(T + R*S)*a1 + 3*R^2 - 2*S*T ->
    m^6*a6' = n^6*a6 + n^4*R*a4 + n^2*R^2*a2 + R^3
              - n^3*T*a3 - T^2 - n*R*T*a1 ->
    m^4 * F28_W_c4a a1' a2' a3' a4' = n^4 * F28_W_c4a a1 a2 a3 a4 /\
    m^6 * F28_W_c6a a1' a2' a3' a4' a6' =
      n^6 * F28_W_c6a a1 a2 a3 a4 a6 /\
    m^12 * F28_W_disca a1' a2' a3' a4' a6' =
      n^12 * F28_W_disca a1 a2 a3 a4 a6.
Proof.
  intros a1 a2 a3 a4 a6 a1' a2' a3' a4' a6' m n R S T
    H1 H2 H3 H4 H6.

  assert (Hb2 :
    m^2 * F28_W_b2 a1' a2' = n^2 * F28_W_b2 a1 a2 + 12*R).
  {
    unfold F28_W_b2.
    replace (m^2*(a1'^2 + 4*a2'))
      with ((m*a1')^2 + 4*(m^2*a2')) by ring.
    rewrite H1, H2.
    ring.
  }

  assert (Hb4 :
    m^4 * F28_W_b4 a1' a3' a4' =
    n^4 * F28_W_b4 a1 a3 a4 + n^2*R*F28_W_b2 a1 a2 + 6*R^2).
  {
    unfold F28_W_b4, F28_W_b2.
    replace (m^4*(2*a4' + a1'*a3'))
      with (2*(m^4*a4') + (m*a1')*(m^3*a3')) by ring.
    rewrite H4, H1, H3.
    ring.
  }

  assert (Hb6 :
    m^6 * F28_W_b6 a3' a6' =
    n^6 * F28_W_b6 a3 a6 + 2*n^4*R*F28_W_b4 a1 a3 a4
    + n^2*R^2*F28_W_b2 a1 a2 + 4*R^3).
  {
    unfold F28_W_b6, F28_W_b4, F28_W_b2.
    replace (m^6*(a3'^2 + 4*a6'))
      with ((m^3*a3')^2 + 4*(m^6*a6')) by ring.
    rewrite H3, H6.
    ring.
  }

  destruct
    (F28_W_c_scaling
       (F28_W_b2 a1 a2) (F28_W_b4 a1 a3 a4) (F28_W_b6 a3 a6)
       (F28_W_b2 a1' a2') (F28_W_b4 a1' a3' a4') (F28_W_b6 a3' a6')
       m n R Hb2 Hb4 Hb6)
    as [Hc4 Hc6].

  split.
  - unfold F28_W_c4a.
    exact Hc4.
  - split.
    + unfold F28_W_c6a.
      exact Hc6.
    + unfold F28_W_disca.
      apply
        (F28_W_disc_scaling
           (F28_W_c4 (F28_W_b2 a1 a2) (F28_W_b4 a1 a3 a4))
           (F28_W_c6 (F28_W_b2 a1 a2) (F28_W_b4 a1 a3 a4)
                     (F28_W_b6 a3 a6))
           (F28_W_disc (F28_W_b2 a1 a2) (F28_W_b4 a1 a3 a4)
                       (F28_W_b6 a3 a6) (F28_W_b8 a1 a2 a3 a4 a6))
           (F28_W_c4 (F28_W_b2 a1' a2') (F28_W_b4 a1' a3' a4'))
           (F28_W_c6 (F28_W_b2 a1' a2') (F28_W_b4 a1' a3' a4')
                     (F28_W_b6 a3' a6'))
           (F28_W_disc (F28_W_b2 a1' a2') (F28_W_b4 a1' a3' a4')
                       (F28_W_b6 a3' a6') (F28_W_b8 a1' a2' a3' a4' a6'))
           m n).
      * apply F28_W_disc_identity.
        apply F28_W_b8_relation.
      * apply F28_W_disc_identity.
        apply F28_W_b8_relation.
      * exact Hc4.
      * exact Hc6.
Qed.

(* ------------------------------------------------------ *)
(* 14.4  MINIMAL DISCRIMINANT                             *)
(* ------------------------------------------------------ *)

Lemma F28_pow_cancel :
  forall (p x y : Z) (k : nat),
    prime p ->
    ~ (p | x) ->
    (F28_ppow p k | x*y) ->
    (F28_ppow p k | y).
Proof.
  intros p x y k Hp Hx.
  assert (Hp0 : p <> 0).
  {
    destruct Hp as [Hg _].
    lia.
  }
  revert y.
  induction k as [|k IH].
  - intros y H.
    simpl.
    apply Z.divide_1_l.
  - intros y H.
    simpl in H.
    simpl.
    assert (Hpd : (p | x*y)).
    {
      destruct H as [q Hq].
      exists (q*F28_ppow p k).
      rewrite Hq.
      ring.
    }
    pose proof (F28_prime_cancel p x y Hp Hx Hpd) as Hy.
    destruct Hy as [y1 Hy1].
    destruct H as [q Hq].
    assert (E : p * (x*y1) = p * (q * F28_ppow p k)).
    {
      replace (p*(x*y1)) with (x*(y1*p)) by ring.
      rewrite <- Hy1.
      rewrite Hq.
      ring.
    }
    pose proof (F28_cancel_nonzero p _ _ Hp0 E) as E2.
    assert (Hdiv : (F28_ppow p k | y1)).
    {
      apply IH.
      exists q.
      exact E2.
    }
    destruct Hdiv as [s Hs].
    exists s.
    rewrite Hy1.
    rewrite Hs.
    ring.
Qed.

(* Every nonzero integer is p^a m0 with p not dividing m0. *)

Lemma F28_decompose_bounded :
  forall p : Z,
    prime p ->
    forall N : nat,
    forall m : Z,
      m <> 0 ->
      Z.abs m <= Z.of_nat N ->
      exists (a : nat) (m0 : Z),
        m = F28_ppow p a * m0 /\ ~ (p | m0).
Proof.
  intros p Hp N.
  assert (Hgt : 1 < p).
  {
    destruct Hp as [Hg _].
    exact Hg.
  }
  induction N as [|N IH].
  - intros m Hm Hb.
    exfalso.
    change (Z.of_nat 0) with 0 in Hb.
    lia.
  - intros m Hm Hb.
    destruct (Zdivide_dec p m) as [Hdiv | Hndiv].
    + destruct Hdiv as [k Hk].
      assert (Hk0 : k <> 0).
      {
        intro H0.
        apply Hm.
        rewrite Hk, H0.
        ring.
      }
      assert (Hbk : Z.abs k <= Z.of_nat N).
      {
        rewrite Nat2Z.inj_succ in Hb.
        rewrite Hk in Hb.
        rewrite Z.abs_mul in Hb.
        rewrite (Z.abs_eq p) in Hb by lia.
        assert (Hk1 : 1 <= Z.abs k) by lia.
        assert (Hkp : 2 * Z.abs k <= Z.abs k * p) by nia.
        lia.
      }
      destruct (IH k Hk0 Hbk) as [a [m0 [Hkm Hm0]]].
      exists (S a), m0.
      split.
      * change (F28_ppow p (S a)) with (p * F28_ppow p a).
        rewrite Hk, Hkm.
        ring.
      * exact Hm0.
    + exists O, m.
      split.
      * change (F28_ppow p O) with 1.
        ring.
      * exact Hndiv.
Qed.

Lemma F28_decompose :
  forall p m : Z,
    prime p ->
    m <> 0 ->
    exists (a : nat) (m0 : Z),
      m = F28_ppow p a * m0 /\ ~ (p | m0).
Proof.
  intros p m Hp Hm.
  apply (F28_decompose_bounded p Hp (Z.to_nat (Z.abs m)) m Hm).
  rewrite Z2Nat.id.
  - lia.
  - apply Z.abs_nonneg.
Qed.

(* p not dividing C, n^4 C = m^4 C', n^12 D = m^12 D' (u = m/n):
   every power of p dividing D divides D', i.e. v_p(D') >= v_p(D). *)

Theorem F28_valuation_discriminant :
  forall p C C' D D' m n : Z,
    prime p ->
    m <> 0 ->
    ~ (p | C) ->
    n^4*C = m^4*C' ->
    n^12*D = m^12*D' ->
    forall k : nat,
      (F28_ppow p k | D) ->
      (F28_ppow p k | D').
Proof.
  intros p C C' D D' m n Hp Hm HC H4 H12 k HkD.

  assert (Hgt : 1 < p).
  {
    destruct Hp as [Hg _].
    exact Hg.
  }

  destruct (F28_decompose p m Hp Hm) as [a [m0 [Hm0 Hnd]]].

  assert (Hdm : (F28_ppow p a | m)).
  {
    exists m0.
    rewrite Hm0.
    ring.
  }

  destruct
    (F28_valuation_bound p C m n C' Hp HC H4 a Hdm)
    as [n1 Hn1].

  assert (HP : F28_ppow p a <> 0).
  {
    pose proof (F28_ppow_pos p Hgt a) as Hpos.
    lia.
  }
  assert (HP12 : (F28_ppow p a)^12 <> 0).
  {
    apply Z.pow_nonzero.
    - exact HP.
    - lia.
  }

  assert (E : (F28_ppow p a)^12 * (n1^12 * D) =
              (F28_ppow p a)^12 * (m0^12 * D')).
  {
    replace ((F28_ppow p a)^12 * (n1^12 * D))
      with ((n1 * F28_ppow p a)^12 * D) by ring.
    replace ((F28_ppow p a)^12 * (m0^12 * D'))
      with ((F28_ppow p a * m0)^12 * D') by ring.
    rewrite <- Hn1.
    rewrite <- Hm0.
    exact H12.
  }

  pose proof (F28_cancel_nonzero _ _ _ HP12 E) as Hmain.

  assert (Hnd12 : ~ (p | m0^12)).
  {
    intro H.
    apply Hnd.
    apply F28_prime_divides_cube; [exact Hp |].
    apply F28_prime_divides_fourth; [exact Hp |].
    replace ((m0^3)^4) with (m0^12) by ring.
    exact H.
  }

  apply (F28_pow_cancel p (m0^12) D' k Hp Hnd12).
  rewrite <- Hmain.
  replace (n1^12 * D) with (D * n1^12) by ring.
  apply F28_divide_mul.
  exact HkD.
Qed.

(* The minimal discriminant statement for the model
   y^2 = x^3 + A x + B with p not dividing c4 = -48 A:
   for EVERY integral Weierstrass model (a1', ..., a6') related to it
   by a change of coordinates with u = m/n, m nonzero (formulas of
   F28_W_change_of_coordinates, a1 = a2 = a3 = 0, a4 = A, a6 = B),
   every power of p dividing Delta = -16 (4A^3 + 27 B^2) divides
   Delta': v_p(Delta') >= v_p(Delta).  So the model has minimal
   discriminant at p. *)

Theorem F28_minimal_discriminant :
  forall p A B a1' a2' a3' a4' a6' m n R S T : Z,
    prime p ->
    m <> 0 ->
    ~ (p | F28_c4 A) ->
    m*a1' = n*0 + 2*S ->
    m^2*a2' = n^2*0 - n*S*0 + 3*R - S^2 ->
    m^3*a3' = n^3*0 + n*R*0 + 2*T ->
    m^4*a4' = n^4*A - n^3*S*0 + 2*n^2*R*0
              - n*(T + R*S)*0 + 3*R^2 - 2*S*T ->
    m^6*a6' = n^6*B + n^4*R*A + n^2*R^2*0 + R^3
              - n^3*T*0 - T^2 - n*R*T*0 ->
    forall k : nat,
      (F28_ppow p k | F28_discriminant A B) ->
      (F28_ppow p k | F28_W_disca a1' a2' a3' a4' a6').
Proof.
  intros p A B a1' a2' a3' a4' a6' m n R S T Hp Hm HC H1 H2 H3 H4 H6 k.

  destruct
    (F28_W_change_of_coordinates
       0 0 0 A B a1' a2' a3' a4' a6' m n R S T
       H1 H2 H3 H4 H6)
    as [Hc4 [Hc6 HD]].

  destruct (F28_W_short_model A B) as [Hs4 [Hs6 HsD]].

  rewrite Hs4 in Hc4.
  rewrite HsD in HD.

  apply
    (F28_valuation_discriminant
       p (F28_c4 A) (F28_W_c4a a1' a2' a3' a4')
       (F28_discriminant A B)
       (F28_W_disca a1' a2' a3' a4' a6')
       m n Hp Hm HC).
  - symmetry.
    exact Hc4.
  - symmetry.
    exact HD.
Qed.

(* The model attached to the family: p not dividing c4. *)

Theorem F28_model_minimal_discriminant :
  forall p a b c a1' a2' a3' a4' a6' m n R S T : Z,
    prime p ->
    5 <= p ->
    ~ (p | a) ->
    ~ (p | c) ->
    m <> 0 ->
    m*a1' = n*0 + 2*S ->
    m^2*a2' = n^2*0 - n*S*0 + 3*R - S^2 ->
    m^3*a3' = n^3*0 + n*R*0 + 2*T ->
    m^4*a4' = n^4*(F28_A a c) - n^3*S*0 + 2*n^2*R*0
              - n*(T + R*S)*0 + 3*R^2 - 2*S*T ->
    m^6*a6' = n^6*(F28_B b c) + n^4*R*(F28_A a c) + n^2*R^2*0 + R^3
              - n^3*T*0 - T^2 - n*R*T*0 ->
    forall k : nat,
      (F28_ppow p k | F28_discriminant (F28_A a c) (F28_B b c)) ->
      (F28_ppow p k | F28_W_disca a1' a2' a3' a4' a6').
Proof.
  intros p a b c a1' a2' a3' a4' a6' m n R S T
    Hp Hlarge Ha Hc Hm H1 H2 H3 H4 H6 k.
  exact
    (F28_minimal_discriminant
       p (F28_A a c) (F28_B b c) a1' a2' a3' a4' a6' m n R S T
       Hp Hm
       (F28_c4_nonzero p a c Hp Hlarge Ha Hc)
       H1 H2 H3 H4 H6 k).
Qed.

(* ------------------------------------------------------ *)
(* 14.5  THE ROOT-NUMBER THEOREM AS AN EXPLICIT HYPOTHESIS *)
(* ------------------------------------------------------ *)

(* w p A B is an ARBITRARY function: it stands for the local root
   number of y^2 = x^3 + A x + B at p.  Nothing about it is assumed
   except the two statements below, which are the content of
   Rohrlich's theorem (local root number -1 for split and +1 for
   nonsplit multiplicative reduction), read with F28_split_multiplicative
   and F28_nonsplit_multiplicative as the definition of the reduction
   type.  They are hypotheses, not theorems of this file. *)

Definition F28_rohrlich_split_hypothesis
  (w : Z -> Z -> Z -> Z) : Prop :=
  forall p A B : Z,
    prime p ->
    5 <= p ->
    F28_split_multiplicative p A B ->
    w p A B = -1.

Definition F28_rohrlich_nonsplit_hypothesis
  (w : Z -> Z -> Z -> Z) : Prop :=
  forall p A B : Z,
    prime p ->
    5 <= p ->
    F28_nonsplit_multiplicative p A B ->
    w p A B = 1.

(* The conclusions are stated as implications.  The converse
   implications (w = -1 gives a square) would need the decidability of
   F28_square_certificate, i.e. classical logic; they are not needed:
   cert -> w = -1 and not cert -> w = 1 already determine w. *)

Theorem F28_root_number_conditional :
  forall (w : Z -> Z -> Z -> Z) (p a b c : Z),
    F28_rohrlich_split_hypothesis w ->
    F28_rohrlich_nonsplit_hypothesis w ->
    prime p ->
    5 <= p ->
    ~ (p | a) ->
    ~ (p | b) ->
    ~ (p | c) ->
    (p | F28_F a b c) ->
    (F28_square_certificate p (a*b) ->
       w p (F28_A a c) (F28_B b c) = -1)
    /\
    (~ F28_square_certificate p (a*b) ->
       w p (F28_A a c) (F28_B b c) = 1)
    /\
    (F28_square_certificate p (F28_minus_c6 (F28_B b c)) ->
       w p (F28_A a c) (F28_B b c) = -1)
    /\
    (~ F28_square_certificate p (F28_minus_c6 (F28_B b c)) ->
       w p (F28_A a c) (F28_B b c) = 1)
    /\
    (w p (F28_A a c) (F28_B b c) = 1 ->
       ~ F28_square_certificate p (a*b)).
Proof.
  intros w p a b c Hsplit Hnonsplit Hp Hlarge Ha Hb Hc HF.

  pose proof
    (F28_model_split_multiplicative_iff
       p a b c Hp Hlarge Ha Hb Hc HF) as H1.
  pose proof
    (F28_model_nonsplit_multiplicative_iff
       p a b c Hp Hlarge Ha Hb Hc HF) as H2.
  pose proof
    (F28_model_minus_c6_criterion
       p a b c Hp Hlarge Ha Hb Hc HF) as H3.

  assert (Hs :
    F28_square_certificate p (a*b) ->
    w p (F28_A a c) (F28_B b c) = -1).
  {
    intro Hcert.
    apply (Hsplit p _ _ Hp Hlarge).
    exact (proj2 H1 Hcert).
  }

  assert (Hn :
    ~ F28_square_certificate p (a*b) ->
    w p (F28_A a c) (F28_B b c) = 1).
  {
    intro Hcert.
    apply (Hnonsplit p _ _ Hp Hlarge).
    exact (proj2 H2 Hcert).
  }

  split.
  - exact Hs.
  - split.
    + exact Hn.
    + split.
      * intro Hcert.
        apply Hs.
        exact (proj1 H3 Hcert).
      * split.
        -- intro Hcert.
           apply Hn.
           intro Hab.
           apply Hcert.
           exact (proj2 H3 Hab).
        -- intros Hw Hcert.
           pose proof (Hs Hcert) as Hm1.
           lia.
Qed.

(* ------------------------------------------------------ *)
(* 14.6  THE STAGE 14 THEOREM                             *)
(* ------------------------------------------------------ *)

Theorem F28_stage14_complete :
  forall (w : Z -> Z -> Z -> Z) (p d U V a b c : Z),
    F28_rohrlich_split_hypothesis w ->
    F28_rohrlich_nonsplit_hypothesis w ->
    prime p ->
    5 <= p ->
    (d = 1 \/ d = 2) ->
    F28_family d U V a b c ->
    ~ ((2 | U) /\ (2 | V)) ->
    ~ ((p | U) /\ (p | V)) ->
    (p | F28_F_paper U V) ->
    (* the family: p | F, F nonzero, p divides none of a, b, c *)
    (p | F28_F a b c) /\
    F28_F a b c <> 0 /\
    (~ (p | a) /\ ~ (p | b) /\ ~ (p | c)) /\
    (* the curve: an elliptic curve with multiplicative reduction at p *)
    (p | F28_discriminant (F28_A a c) (F28_B b c)) /\
    F28_discriminant (F28_A a c) (F28_B b c) <> 0 /\
    ~ (p | F28_c4 (F28_A a c)) /\
    F28_multiplicative_reduction p (F28_A a c) (F28_B b c) /\
    (* split iff ab is a square class iff -c6 is a square class *)
    (F28_split_multiplicative p (F28_A a c) (F28_B b c) <->
     F28_square_certificate p (a*b)) /\
    (F28_nonsplit_multiplicative p (F28_A a c) (F28_B b c) <->
     ~ F28_square_certificate p (a*b)) /\
    (F28_square_certificate p (F28_minus_c6 (F28_B b c)) <->
     F28_square_certificate p (a*b)) /\
    (* the root number, GIVEN the two hypotheses on w *)
    (F28_square_certificate p (a*b) ->
       w p (F28_A a c) (F28_B b c) = -1) /\
    (~ F28_square_certificate p (a*b) ->
       w p (F28_A a c) (F28_B b c) = 1).
Proof.
  intros w p d U V a b c Hsplit Hnonsplit Hp Hlarge Hd Hfam
    Hcop2 Hcopp HFp.

  destruct
    (F28_family_hypotheses
       p d U V a b c Hp Hlarge Hd Hfam Hcop2 Hcopp HFp)
    as [HF [HF0 [Ha [Hb Hc]]]].

  pose proof
    (F28_stage13_multiplicative_reduction
       p a b c Hp Hlarge Ha Hb Hc HF HF0)
    as S13.
  destruct S13 as [HD [Hc4 [HD0 [Hmult S13rest]]]].

  pose proof
    (F28_model_split_multiplicative_iff
       p a b c Hp Hlarge Ha Hb Hc HF) as Hsp.
  pose proof
    (F28_model_nonsplit_multiplicative_iff
       p a b c Hp Hlarge Ha Hb Hc HF) as Hns.
  pose proof
    (F28_model_minus_c6_criterion
       p a b c Hp Hlarge Ha Hb Hc HF) as Hc6.
  pose proof
    (F28_root_number_conditional
       w p a b c Hsplit Hnonsplit Hp Hlarge Ha Hb Hc HF)
    as [Hr1 [Hr2 _]].

  exact
    (conj HF
      (conj HF0
        (conj (conj Ha (conj Hb Hc))
          (conj HD
            (conj HD0
              (conj Hc4
                (conj Hmult
                  (conj Hsp
                    (conj Hns
                      (conj Hc6
                        (conj Hr1 Hr2))))))))))).
Qed.

(* ------------------------------------------------------ *)
(* COMPILER AND ASSUMPTION CHECKS                         *)
(* ------------------------------------------------------ *)

Check F28_model_minus_c6_criterion.
Check F28_model_split_iff_minus_c6.
Check F28_family_normalization.
Check F28_family_hypotheses.
Check F28_W_change_of_coordinates.
Check F28_minimal_discriminant.
Check F28_model_minimal_discriminant.
Check F28_root_number_conditional.
Check F28_stage14_complete.

Print Assumptions F28_model_minus_c6_criterion.
Print Assumptions F28_family_hypotheses.
Print Assumptions F28_model_minimal_discriminant.
Print Assumptions F28_stage14_complete.

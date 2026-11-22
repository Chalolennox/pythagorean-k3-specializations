(* code/coq/F28_stage8a_reduced_model.v

   STAGE 8a.  NOT an owner file: written in review by Claude (a language model; no human check), at the owner's request ("8a") after the owner's Stage 7 file and the Stage 8 proposal.
   Standalone.  Compiled only by CI (Coq 8.20.1); read by hand beforehand, no local Coq.
   HOW IT IS BUILT: the text of the owner's 51st file (F28_stage7_nodal_reduction.v: definitions, invariants, nodal certificate; its closing Check/Print lines dropped), followed by blocks copied UNCHANGED from the 50th file
   (F28_unconditional_bridge.v: the square-certificate / split-node definitions, F28_singular_linear_relation, the square-class bridge, F28_unconditional_split_node) and from the 40th file (F28_prime_inverse), and then a section
   "NEW IN STAGE 8a" which is mine.  The only import change against the owner's files is the added module Zgcd_alt (needed by F28_prime_inverse, exactly as in the 40th file).
   WHAT THE NEW SECTION PROVES, for prime p >= 5, p not dividing a, b, c, p | F = 4 a^3 + 27 b^2 c, integral model Y^2 = X^3 + A X + B, A = 4 a c^3, B = -8 b c^5:
     F28_unit_scaling / F28_model_scaling_unit: if c4 = u^4 c4' (an integral change of Weierstrass coordinates with scaling u multiplies c4 by u^4) and p does not divide c4, then p does not divide u.  So the model cannot be made
       smaller at p by any integral change of coordinates: this is the elementary minimality criterion (p not dividing c4 implies the model is minimal at p), proved over the integers, no p-adic valuation needed.
     F28_double_root_exists: there is r with p | f(r) and p | f'(r) (r = -3 B u, u an inverse of 2A mod p; proof written here, using 4 A^2 f'(r) = (4 A^3 + 27 B^2) + p (...) and 3 f(r) = r f'(r) + p (...)).
     F28_reduced_singular p A B x y := p | y^2 - f(x), p | 2 y, p | f'(x): (x, y) is a singular point of the reduced curve y^2 = f(x) over F_p (Silverman, Ch. VII, definition of the reduction type via the reduced curve).
       F28_reduced_singular_split: for p >= 5 it means p | y, p | f(x), p | f'(x).
     F28_reduced_singular_unique: any two singular points of the reduced curve agree mod p (p | x1 - x2, p | y1, p | y2); this uses F28_singular_linear_relation (a x = 3 b c^2 mod p at every double root).
     F28_reduced_singular_node: at a singular point p does not divide x, 3x and the tangent cone v^2 - 3 x u^2 at (1,0) is nonzero, i.e. the singularity is a node (not a cusp).
     F28_reduced_node_split_criterion: the node is split (rational tangent directions, F28_split_node_certificate) iff a b is a square class mod p (F28_square_certificate p (a b)).
     F28_stage8a_reduction_model: all of the above in one statement (invariants, minimality, existence, uniqueness, node, split criterion).
   WHAT IT DOES NOT PROVE (explicitly): there is no construction of Q_p or of a p-adic valuation here; the statements are about integer representatives read mod p.  "Minimal" is the elementary criterion c4 = u^4 c4' => p not
   dividing u, not Tate's algorithm.  That this reduction type of the reduced curve over F_p is what is called split multiplicative reduction of the elliptic curve over Q_p is Silverman's definition (Ch. VII, section 1 and Prop. VII.5.1),
   used as the definition here, not derived; the local root number w_p = -1 for split and +1 for nonsplit multiplicative reduction is Rohrlich's theorem (cited, NOT in Coq); the parametrization and "c is a perfect square on the family" are not here.
   Composition with the other standalone files is held until the owner says so. *)

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

(* ------------------------------------------------------ *)
(* COMPILER AND ASSUMPTION CHECKS                         *)
(* ------------------------------------------------------ *)

Check F28_unit_scaling.
Check F28_model_scaling_unit.
Check F28_double_root_general.
Check F28_double_root_exists.
Check F28_reduced_singular_unique.
Check F28_reduced_singular_node.
Check F28_reduced_node_split_criterion.
Check F28_stage8a_reduction_model.

Print Assumptions F28_stage8a_reduction_model.

(* code/coq/F28_stage11_bridge.v

   The owner's fifty-fifth Coq file ("Stages 8 to 11", 22 November 2026).  The text is the owner's, with ONE change: the import "From Stdlib Require Import ZArith Znumtheory Ring Lia." is written
   "From Coq Require Import ZArith Znumtheory Ring Lia." (CI compiles with Coq 8.20.1, which has no Stdlib prefix).  Plus this header.  Standalone.
   Its first 448 lines are the owner's 54th file (F28_stage10_branches.v, which contains the 52nd and 53rd) unchanged; the Stage 11 section after it is new.
   STAGE 11 DEFINITION: F28_congr p x y := p | x - y (with reflexivity, symmetry, transitivity, multiplication and squares of congruences, all by ring identities).
   WHAT STAGE 11 PROVES (read by hand), for integers and a prime p:
     F28_stage11_product_square: p | a r - 3 b c^2 implies (3 r)(a b) = (3 b c)^2 mod p  (the difference is 3 b (a r - 3 b c^2), ring);
     F28_stage11_square_transfer: z y = s^2 mod p, z w = 1 mod p and z a square mod p (t^2 = z) imply y a square mod p (witness s w t: (s w t)^2 = s^2 w^2 t^2 = (z y) w^2 z = y (z w)^2 = y mod p);
     F28_stage11_split_to_ab / F28_stage11_ab_to_split: for prime p not dividing 3 r with p | a r - 3 b c^2 and explicit inverses w of 3 r (resp. a b) mod p: F28_split_branches p r  <->  F28_square_mod p (a b), in each direction;
     F28_stage11_split_iff_ab: both directions together (inverses w1 of 3 r and w2 of a b given).
   WHY IT MATTERS: together with the earlier files it connects the two-branch normalization of Stages 9-10 to the arithmetic class ab: the branches over the node exist iff a b is a square mod p (the split case), the same conclusion as F28_unconditional_bridge.v (50th) but stated for F28_split_branches and F28_square_mod.
   The hypothesis p | a r - 3 b c^2 holds at every double root r (F28_singular_linear_relation, 50th file; p >= 5, p not dividing c); the inverses w exist when p does not divide 3 r, a b (F28_prime_inverse, 40th file); these are hypotheses here, not derived.
   WHAT IT DOES NOT PROVE: existence of r, that p does not divide 3 r, a b for the model, root counting (that t, -t are the only preimages), surjectivity of the normalization, the Q_p identification, minimality, root numbers, the paper's own parametrization by t.
   Composition with the other standalone files is held until the owner says so. *)

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

(* ===================================================== *)
(* STAGE 9: EXPLICIT NORMALIZATION OF THE NODAL CUBIC  *)
(* ===================================================== *)

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

Theorem F28_stage9_slope_identity :
  forall r t : Z,
    F28_norm_y r t = t*(F28_norm_x r t-r).
Proof.
  intros r t.
  unfold F28_norm_x, F28_norm_y.
  ring.
Qed.

Theorem F28_stage9_node_preimages :
  forall r t : Z,
    F28_norm_x r t = r <-> t^2 = 3*r.
Proof.
  intros r t.
  unfold F28_norm_x.
  lia.
Qed.

Theorem F28_stage9_node_y :
  forall r t : Z,
    t^2 = 3*r -> F28_norm_y r t = 0.
Proof.
  intros r t H.
  unfold F28_norm_y.
  rewrite H.
  ring.
Qed.

Theorem F28_stage9_inverse_slope_relation :
  forall r x y t : Z,
    y^2 = F28_factor r x ->
    y = t*(x-r) ->
    (x-r)^2*(t^2-(x+2*r)) = 0.
Proof.
  intros r x y t Hcurve Hslope.
  replace ((x-r)^2*(t^2-(x+2*r)))
    with ((t*(x-r))^2 - F28_factor r x)
    by (unfold F28_factor; ring).
  rewrite <- Hslope.
  rewrite Hcurve.
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

Theorem F28_stage9_family_parametrization :
  forall p a b c r t : Z,
    (p | F28_cubic (F28_A a c) (F28_B b c) r) ->
    (p | F28_derivative (F28_A a c) r) ->
    (p | F28_norm_y r t ^ 2 -
         F28_cubic (F28_A a c) (F28_B b c)
           (F28_norm_x r t)).
Proof.
  intros p a b c r t Hf Hd.
  exact (F28_stage9_reduced_model_parametrization
    p (F28_A a c) (F28_B b c) r t Hf Hd).
Qed.

Check F28_stage9_parametrization.
Check F28_stage9_slope_identity.
Check F28_stage9_node_preimages.
Check F28_stage9_node_y.
Check F28_stage9_inverse_slope_relation.
Check F28_stage9_reduced_model_parametrization.
Check F28_stage9_family_parametrization.
Print Assumptions F28_stage9_family_parametrization.

(* ===================================================== *)
(* STAGE 10: TWO BRANCHES ABOVE THE NODE                 *)
(* ===================================================== *)

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

Theorem F28_stage10_opposite_branch :
  forall p r t : Z,
    (p | t^2-3*r) ->
    (p | (-t)^2-3*r).
Proof.
  intros p r t H.
  replace ((-t)^2-3*r) with (t^2-3*r) by ring.
  exact H.
Qed.

Theorem F28_stage10_distinct_branches :
  forall p r t : Z,
    prime p ->
    ~ (p | 2) ->
    ~ (p | 3*r) ->
    (p | t^2-3*r) ->
    ~ (p | t-(-t)).
Proof.
  intros p r t Hp Htwo Hr Hsquare Hdiff.
  assert (Ht : ~ (p | t)).
  { exact (F28_stage10_square_nonzero p r t Hp Hr Hsquare). }
  replace (t-(-t)) with (2*t) in Hdiff by ring.
  apply prime_mult in Hdiff; [|exact Hp].
  destruct Hdiff as [H2 | Htbad].
  - exact (Htwo H2).
  - exact (Ht Htbad).
Qed.

Theorem F28_stage10_family_split_iff_square :
  forall p a b c r : Z,
    prime p ->
    ~ (p | 3*r) ->
    (F28_split_branches p r <-> F28_square_mod p (3*r)).
Proof.
  intros p a b c r Hp Hr.
  exact (F28_stage10_split_iff_square p r Hp Hr).
Qed.

Check F28_stage10_node_x_identity.
Check F28_stage10_node_y_identity.
Check F28_stage10_square_gives_node.
Check F28_stage10_square_nonzero.
Check F28_stage10_split_iff_square.
Check F28_stage10_opposite_branch.
Check F28_stage10_distinct_branches.
Print Assumptions F28_stage10_split_iff_square.
Print Assumptions F28_stage10_distinct_branches.

(* ===================================================== *)
(* STAGE 11: ARITHMETIC SQUARE-CLASS BRIDGE              *)
(* ===================================================== *)

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

Lemma F28_congr_ring : forall p x y,
  x=y -> F28_congr p x y.
Proof.
  intros p x y H. subst y. apply F28_congr_refl.
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

(* Transfer a square class through a square product, given
   an explicit modular inverse of the first factor. *)
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

Check F28_stage11_product_square.
Check F28_stage11_square_transfer.
Check F28_stage11_split_to_ab.
Check F28_stage11_ab_to_split.
Check F28_stage11_split_iff_ab.
Print Assumptions F28_stage11_split_iff_ab.

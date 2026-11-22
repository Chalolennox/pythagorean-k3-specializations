(* code/coq/F28_stage9_normalization.v

   The owner's fifty-third Coq file ("Stage 8 + Stage 9: factorization certificate and explicit normalization of the nodal cubic", 22 November 2026).  The text is the owner's, with ONE change: the import "From Stdlib Require Import ZArith Znumtheory Ring Lia."
   is written "From Coq Require Import ZArith Znumtheory Ring Lia." (CI compiles with Coq 8.20.1, which has no Stdlib prefix).  Plus this header.  Standalone.
   Its first 214 lines are the owner's 52nd file (F28_stage8_factorization.v) unchanged; the Stage 9 section after it is new.
   STAGE 9 DEFINITIONS: F28_norm_x r t := t^2 - 2 r;  F28_norm_y r t := t (t^2 - 3 r);  F28_node_equation r x y := y^2 - (x - r)^2 (x + 2r).
   WHAT STAGE 9 PROVES (read by hand), for integers r, t:
     F28_stage9_parametrization: y^2 = (x - r)^2 (x + 2r) at (x, y) = (t^2 - 2r, t (t^2 - 3r))  (x - r = t^2 - 3r and x + 2r = t^2, so both sides equal t^2 (t^2 - 3r)^2; ring);
     F28_stage9_slope_identity: y = t (x - r)  (t is the slope of the line through the node (r, 0));
     F28_stage9_node_preimages: x = r iff t^2 = 3r;  F28_stage9_node_y: t^2 = 3r gives y = 0  (the two preimages of the node are t = +- sqrt(3r));
     F28_stage9_inverse_slope_relation: if y^2 = (x - r)^2 (x + 2r) and y = t (x - r) then (x - r)^2 (t^2 - (x + 2r)) = 0  (ring);
     F28_stage9_reduced_model_parametrization: if p | f(r) and p | f'(r) then p | y^2 - f(x) at (x, y) = (norm_x r t, norm_y r t) for every integer t  (f(x) is congruent to (x - r)^2 (x + 2r) mod p by F28_singular_factorization; the difference is -(f(x) - factor_r(x)));
     F28_stage9_family_parametrization: the same for A = 4 a c^3, B = -8 b c^5.
   WHY IT MATTERS: the reduced cubic y^2 = (x - r)^2 (x + 2r) is the nodal cubic with explicit normalization t |-> (t^2 - 2r, t (t^2 - 3r)); the node has two preimages exactly when 3r is a square (the split case, matching F28_unconditional_bridge.v).
   WHAT IT DOES NOT PROVE: that every point of the reduced curve over F_p comes from some t (surjectivity of the normalization, inverse map: only the slope relation is proved), the point count, the existence of r, the Q_p identification, minimality, root numbers, the paper's own parametrization by t.
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

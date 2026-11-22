(* code/coq/F28_large_prime_tangent.v

   The owner's twenty-first Coq file (22 November 2026), unchanged except for this header.  Standalone and integrated: it repeats the constant
   exclusions (twentieth file), the singular-root nondivisibility (eighteenth and nineteenth), the tangent certificate and its cancellation
   (sixteenth and seventeenth).
   WHAT IT PROVES: F28_large_prime_tangent_character: for a prime p >= 5 and a cubic Y^2 = X^3 + A X + B with a double root r mod p
   (p | f(r), p | f'(r)) and p not dividing A,
        (-c6 = 864 B is a square certificate mod p)  <->  (3r is a square certificate mod p),
   with every nonvanishing hypothesis (p not dividing 1, 2, r, B, 3r, 864 B) discharged inside.  It states the same as
   F28_nodal_split_criterion in F28_tangent_character.v (added in review), which stays as a cross-check.  I read the proof: the six bullets
   match the six hypotheses of F28_tangent_character_equivalence in order; sound.
   WHAT IT DOES NOT PROVE: the identification of "split multiplicative reduction" with "3r is a square mod p" (Tate/Silverman); no Legendre symbol; for the integral model A = 4 a c^3, B = -8 b c^5
   one needs p not dividing a, c (F28_main_arithmetic) for p not dividing A.
   The added part removes the need to be GIVEN the double root: F28_double_root_exists (Bezout: r = -3B u with 2A u = 1 mod p, from the owner's
   twenty-third file identities) and F28_discriminant_split_criterion (p >= 5, p | Delta = -4A^3 - 27B^2, p not dividing A: some r with the
   criterion). *)

From Coq Require Import ZArith.
From Coq Require Import Znumtheory.
From Coq Require Import Lia.
From Coq Require Import Ring.

Open Scope Z_scope.

(* ======================================== *)
(* DEFINITIONS                              *)
(* ======================================== *)

Definition F28_cubic (A B r : Z) : Z :=
  r^3 + A*r + B.

Definition F28_derivative (A r : Z) : Z :=
  3*r^2 + A.

Definition F28_minus_c6 (B : Z) : Z :=
  864*B.

Definition F28_square_certificate (p x : Z) : Prop :=
  exists u v : Z,
    ~ (p | u) /\
    (p | x*u^2-v^2).

(* ======================================== *)
(* DIVISIBILITY HELPERS                     *)
(* ======================================== *)

Lemma F28_divide_product :
  forall p x y : Z,
    (p | x) -> (p | x*y).
Proof.
  intros p x y H.
  destruct H as [k Hk].
  exists (k*y).
  rewrite Hk.
  ring.
Qed.

Lemma F28_divide_sum :
  forall p x y : Z,
    (p | x) -> (p | y) -> (p | x+y).
Proof.
  intros p x y Hx Hy.
  destruct Hx as [u Hu].
  destruct Hy as [v Hv].
  exists (u+v).
  rewrite Hu, Hv.
  ring.
Qed.

Lemma F28_divide_difference :
  forall p x y : Z,
    (p | x) -> (p | y) -> (p | x-y).
Proof.
  intros p x y Hx Hy.
  destruct Hx as [u Hu].
  destruct Hy as [v Hv].
  exists (u-v).
  rewrite Hu, Hv.
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
(* SMALL PRIME EXCLUSIONS                   *)
(* ======================================== *)

Theorem F28_large_prime_not_divide_two :
  forall p : Z,
    prime p ->
    5 <= p ->
    ~ (p | 2).
Proof.
  intros p Hp Hlarge Hdiv.
  destruct Hdiv as [k Hk].
  assert (Hpositive : 0 < p) by lia.
  assert (Hbound : 0 <= k \/ k < 0) by lia.
  destruct Hbound as [Hnonneg | Hneg].
  - destruct (Z.eq_dec k 0) as [Hzero | Hnonzero].
    + subst k. lia.
    + assert (1 <= k) by lia.
      nia.
  - assert (k <= -1) by lia.
    nia.
Qed.

Theorem F28_large_prime_not_divide_three :
  forall p : Z,
    prime p ->
    5 <= p ->
    ~ (p | 3).
Proof.
  intros p Hp Hlarge Hdiv.
  destruct Hdiv as [k Hk].
  assert (Hpositive : 0 < p) by lia.
  destruct (Z_le_gt_dec 0 k) as [Hnonneg | Hneg].
  - destruct (Z.eq_dec k 0) as [Hzero | Hnonzero].
    + subst k. lia.
    + assert (1 <= k) by lia.
      nia.
  - assert (k <= -1) by lia.
    nia.
Qed.

Theorem F28_large_prime_not_divide_864 :
  forall p : Z,
    prime p ->
    5 <= p ->
    ~ (p | 864).
Proof.
  intros p Hp Hlarge Hdiv.

  assert (Hnot2 : ~ (p | 2)).
  {
    apply (F28_large_prime_not_divide_two p).
    - exact Hp.
    - exact Hlarge.
  }

  assert (Hnot3 : ~ (p | 3)).
  {
    apply (F28_large_prime_not_divide_three p).
    - exact Hp.
    - exact Hlarge.
  }

  replace 864 with (2*2*2*2*2*3*3*3) in Hdiv
    by ring.

  repeat match type of Hdiv with
  | (p | ?x * ?y) =>
      let H := fresh "Hsplit" in
      pose proof
        (F28_prime_product_split p x y Hp Hdiv)
        as H;
      clear Hdiv;
      destruct H as [Hdiv | Hdiv]
  end.

  all: first [exact (Hnot2 Hdiv) |
              exact (Hnot3 Hdiv)].
Qed.

Theorem F28_three_r_nonzero :
  forall p r : Z,
    prime p ->
    5 <= p ->
    ~ (p | r) ->
    ~ (p | 3*r).
Proof.
  intros p r Hp Hlarge Hr.
  apply (F28_nonzero_product p 3 r).
  - exact Hp.
  - apply (F28_large_prime_not_divide_three p).
    + exact Hp.
    + exact Hlarge.
  - exact Hr.
Qed.

Theorem F28_864_B_nonzero :
  forall p B : Z,
    prime p ->
    5 <= p ->
    ~ (p | B) ->
    ~ (p | 864*B).
Proof.
  intros p B Hp Hlarge HB.
  apply (F28_nonzero_product p 864 B).
  - exact Hp.
  - apply (F28_large_prime_not_divide_864 p).
    + exact Hp.
    + exact Hlarge.
  - exact HB.
Qed.

(* ======================================== *)
(* SINGULAR ROOT NONDIVISIBILITY            *)
(* ======================================== *)

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

(* ======================================== *)
(* TANGENT PRODUCT CERTIFICATE              *)
(* ======================================== *)

Theorem F28_tangent_product_certificate :
  forall p A B r : Z,
    (p | F28_cubic A B r) ->
    (p | F28_derivative A r) ->
    ~ (p | 1) ->
    F28_square_certificate
      p (F28_minus_c6 B*(3*r)).
Proof.
  intros p A B r Hcubic Hderivative Hunit.
  unfold F28_square_certificate.

  exists 1.
  exists (72*r^2).
  split.
  - exact Hunit.
  - destruct Hcubic as [k Hk].
    destruct Hderivative as [m Hm].
    exists (2592*r*k - 2592*r^2*m).

    unfold F28_minus_c6.
    unfold F28_cubic in Hk.
    unfold F28_derivative in Hm.

    assert (Hidentity :
      864*B*(3*r)*1^2 - (72*r^2)^2 =
      2592*r*(r^3+A*r+B)
      -2592*r^2*(3*r^2+A)).
    {
      ring.
    }

    rewrite Hidentity.
    rewrite Hk.
    rewrite Hm.
    ring.
Qed.

(* ======================================== *)
(* CERTIFICATE CANCELLATION                 *)
(* ======================================== *)

Theorem F28_certificate_cancel :
  forall p x y : Z,
    prime p ->
    ~ (p | x) ->
    F28_square_certificate p (x*y) ->
    F28_square_certificate p x ->
    F28_square_certificate p y.
Proof.
  intros p x y Hp Hnx Hxy Hx.

  destruct Hxy as [u [v [Hnu Hxyuv]]].
  destruct Hx as [r [s [Hnr Hxrs]]].

  unfold F28_square_certificate.

  exists (x*u*r).
  exists (v*s).

  split.

  - assert (Hnur : ~ (p | u*r)).
    {
      apply (F28_nonzero_product p u r).
      + exact Hp.
      + exact Hnu.
      + exact Hnr.
    }

    replace (x*u*r) with (x*(u*r)) by ring.
    apply (F28_nonzero_product p x (u*r)).
    + exact Hp.
    + exact Hnx.
    + exact Hnur.

  - replace
      (y*(x*u*r)^2-(v*s)^2)
      with
      ((x*y*u^2-v^2)*(x*r^2)
       +v^2*(x*r^2-s^2))
      by ring.

    apply F28_divide_sum.
    + apply F28_divide_product.
      exact Hxyuv.
    + replace
        (v^2*(x*r^2-s^2))
        with ((x*r^2-s^2)*v^2)
        by ring.
      apply F28_divide_product.
      exact Hxrs.
Qed.

Theorem F28_tangent_character_equivalence :
  forall p A B r : Z,
    prime p ->
    ~ (p | 1) ->
    (p | F28_cubic A B r) ->
    (p | F28_derivative A r) ->
    ~ (p | F28_minus_c6 B) ->
    ~ (p | 3*r) ->
    (F28_square_certificate p (F28_minus_c6 B)
     <->
     F28_square_certificate p (3*r)).
Proof.
  intros p A B r
    Hp Hunit Hcubic Hderivative Hnc6 Hnr.

  pose proof
    (F28_tangent_product_certificate
       p A B r Hcubic Hderivative Hunit)
    as Hproduct.

  split.

  - intro Hc6.
    apply
      (F28_certificate_cancel
         p (F28_minus_c6 B) (3*r)).
    + exact Hp.
    + exact Hnc6.
    + exact Hproduct.
    + exact Hc6.

  - intro Htangent.

    assert (Hreverse :
      F28_square_certificate
        p ((3*r)*F28_minus_c6 B)).
    {
      replace
        ((3*r)*F28_minus_c6 B)
        with
        (F28_minus_c6 B*(3*r))
        by ring.
      exact Hproduct.
    }

    apply
      (F28_certificate_cancel
         p (3*r) (F28_minus_c6 B)).
    + exact Hp.
    + exact Hnr.
    + exact Hreverse.
    + exact Htangent.
Qed.

(* ======================================== *)
(* MAIN THEOREM                             *)
(* ======================================== *)

Theorem F28_large_prime_tangent_character :
  forall p A B r : Z,
    prime p ->
    5 <= p ->
    (p | F28_cubic A B r) ->
    (p | F28_derivative A r) ->
    ~ (p | A) ->
    (F28_square_certificate p (F28_minus_c6 B)
     <->
     F28_square_certificate p (3*r)).
Proof.
  intros p A B r
    Hp Hlarge Hcubic Hderivative HnotA.

  assert (Hnot1 : ~ (p | 1)).
  {
    intro Hdiv.
    destruct Hdiv as [k Hk].
    destruct (Z_le_gt_dec 0 k) as [Hkpos | Hkneg].
    - destruct (Z.eq_dec k 0) as [Hzero | Hnonzero].
      + subst k. lia.
      + assert (1 <= k) by lia.
        nia.
    - assert (k <= -1) by lia.
      nia.
  }

  assert (Hnot2 : ~ (p | 2)).
  {
    apply (F28_large_prime_not_divide_two p).
    - exact Hp.
    - exact Hlarge.
  }

  assert (Hr : ~ (p | r)).
  {
    apply (F28_singular_root_nonzero p A r).
    - exact Hderivative.
    - exact HnotA.
  }

  assert (HB : ~ (p | B)).
  {
    apply (F28_singular_B_nonzero p A B r).
    - exact Hp.
    - exact Hnot2.
    - exact Hcubic.
    - exact Hderivative.
    - exact HnotA.
  }

  assert (Hthree : ~ (p | 3*r)).
  {
    apply (F28_three_r_nonzero p r).
    - exact Hp.
    - exact Hlarge.
    - exact Hr.
  }

  assert (Hc6 : ~ (p | F28_minus_c6 B)).
  {
    unfold F28_minus_c6.
    apply (F28_864_B_nonzero p B).
    - exact Hp.
    - exact Hlarge.
    - exact HB.
  }

  apply
    (F28_tangent_character_equivalence
       p A B r).
  - exact Hp.
  - exact Hnot1.
  - exact Hcubic.
  - exact Hderivative.
  - exact Hc6.
  - exact Hthree.
Qed.

(* ======================================== *)
(* FINAL VERIFICATION                       *)
(* ======================================== *)

Check F28_large_prime_tangent_character.

Print Assumptions F28_large_prime_tangent_character.

(* ======================================== *)
(* ADDED IN REVIEW (22 November 2026): from p | Delta to the split criterion *)
(* ======================================== *)

Definition F28_discriminant (A B : Z) : Z :=
  -4*A^3 - 27*B^2.

Definition F28_root_numerator (B : Z) : Z :=
  -3*B.

Definition F28_root_denominator (A : Z) : Z :=
  2*A.

(* The two identities of the owner's twenty-third file (F28_root_transport.v), repeated. *)
Theorem F28_candidate_derivative_identity :
  forall A B u : Z,
    F28_derivative A
      (F28_root_numerator B*u)
    =
    -u^2*F28_discriminant A B
    - A*
      (F28_root_denominator A*u-1)*
      (F28_root_denominator A*u+1).
Proof.
  intros A B u.
  unfold F28_derivative.
  unfold F28_root_numerator.
  unfold F28_root_denominator.
  unfold F28_discriminant.
  ring.
Qed.

Theorem F28_candidate_cubic_identity :
  forall A B u : Z,
    F28_cubic A B
      (F28_root_numerator B*u)
    =
    B*u^3*F28_discriminant A B
    -
    (F28_root_denominator A*u-1)*
    (A*(F28_root_numerator B)*u*
       (F28_root_denominator A*u+1)
     + B*
       ((F28_root_denominator A*u)^2
        + F28_root_denominator A*u+1)).
Proof.
  intros A B u.
  unfold F28_cubic.
  unfold F28_root_numerator.
  unfold F28_root_denominator.
  unfold F28_discriminant.
  ring.
Qed.

(* For a prime p not dividing 2A, p | Delta gives an INTEGER double root r = -3B u, where u inverts 2A modulo p (Bezout). *)
Theorem F28_double_root_exists :
  forall p A B : Z,
    prime p ->
    ~ (p | 2*A) ->
    (p | F28_discriminant A B) ->
    exists r : Z,
      (p | F28_cubic A B r) /\
      (p | F28_derivative A r).
Proof.
  intros p A B Hp Hn2A HD.
  destruct (rel_prime_bezout p (2*A)
              (prime_rel_prime p Hp (2*A) Hn2A))
    as [x y Hxy].
  assert (Hd : (p | F28_root_denominator A*y - 1)).
  {
    exists (-x).
    unfold F28_root_denominator.
    nia.
  }
  exists (F28_root_numerator B*y).
  split.
  - rewrite F28_candidate_cubic_identity.
    apply F28_divide_difference.
    + replace (B*y^3*F28_discriminant A B)
        with (F28_discriminant A B*(B*y^3))
        by ring.
      apply F28_divide_product.
      exact HD.
    + apply F28_divide_product.
      exact Hd.
  - rewrite F28_candidate_derivative_identity.
    apply F28_divide_difference.
    + replace (-y^2*F28_discriminant A B)
        with (F28_discriminant A B*(-y^2))
        by ring.
      apply F28_divide_product.
      exact HD.
    + replace
        (A*(F28_root_denominator A*y-1)
          *(F28_root_denominator A*y+1))
        with
        ((F28_root_denominator A*y-1)
          *(A*(F28_root_denominator A*y+1)))
        by ring.
      apply F28_divide_product.
      exact Hd.
Qed.

(* The combination: for a prime p >= 5 with p | Delta and p not dividing A, the cubic has an integer double root r mod p and
   (-c6/p) = (3r/p) in certificate form, with r = -3B/(2A) mod p. *)
Theorem F28_discriminant_split_criterion :
  forall p A B : Z,
    prime p ->
    5 <= p ->
    (p | F28_discriminant A B) ->
    ~ (p | A) ->
    exists r : Z,
      (p | F28_cubic A B r) /\
      (p | F28_derivative A r) /\
      (F28_square_certificate p (F28_minus_c6 B)
       <->
       F28_square_certificate p (3*r)).
Proof.
  intros p A B Hp Hlarge HD HnA.
  assert (Hn2A : ~ (p | 2*A)).
  {
    exact (F28_nonzero_product p 2 A Hp
             (F28_large_prime_not_divide_two p Hp Hlarge) HnA).
  }
  destruct (F28_double_root_exists p A B Hp Hn2A HD)
    as [r [Hcubic Hderivative]].
  exists r.
  split.
  - exact Hcubic.
  - split.
    + exact Hderivative.
    + exact (F28_large_prime_tangent_character
               p A B r Hp Hlarge Hcubic Hderivative HnA).
Qed.

Print Assumptions F28_discriminant_split_criterion.

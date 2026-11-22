(* code/coq/F28_bezout_inverse.v

   The owner's twenty-sixth Coq file (22 November 2026), unchanged except for this header.  Standalone (ZArith, Ring only).
   F28_bezout_to_inverse: p k + 2 A u = 1 ==> p | 2 A u - 1  (2 A u - 1 = -p k, checked by hand);
   F28_bezout_witness_gives_inverse: the existential form.
   This is the step that feeds F28_candidate_is_singular (F28_candidate_root.v): its hypothesis "p | 2 A u - 1" is exactly what this produces from a Bezout
   relation.  The Bezout relation itself (p prime, p not dividing 2A) comes from rel_prime_bezout in F28_large_prime_tangent.v (F28_double_root_exists,
   where the same computation is done inline with x, y).  WHAT IT DOES NOT PROVE: existence of the Bezout coefficients. *)

From Coq Require Import ZArith.
From Coq Require Import Ring.

Open Scope Z_scope.

Definition F28_root_denominator (A : Z) : Z :=
  2*A.

(* ======================================== *)
(* BEZOUT IDENTITY IMPLIES MODULAR INVERSE  *)
(* ======================================== *)

Theorem F28_bezout_to_inverse :
  forall p A k u : Z,
    p*k + F28_root_denominator A*u = 1 ->
    (p | F28_root_denominator A*u-1).
Proof.
  intros p A k u Hbezout.

  exists (-k).

  unfold F28_root_denominator in *.

  assert (Hidentity :
    2*A*u-1 = -p*k).
  {
    rewrite <- Hbezout.
    ring.
  }

  rewrite Hidentity.
  ring.
Qed.

(* ======================================== *)
(* EXISTENTIAL VERSION                      *)
(* ======================================== *)

Theorem F28_bezout_witness_gives_inverse :
  forall p A : Z,
    (exists k u : Z,
       p*k + F28_root_denominator A*u = 1) ->
    exists u : Z,
      (p | F28_root_denominator A*u-1).
Proof.
  intros p A Hbezout.

  destruct Hbezout as [k [u Hidentity]].

  exists u.

  apply (F28_bezout_to_inverse p A k u).
  exact Hidentity.
Qed.

(* ======================================== *)
(* VERIFICATION                             *)
(* ======================================== *)

Check F28_bezout_to_inverse.
Check F28_bezout_witness_gives_inverse.

Print Assumptions F28_bezout_witness_gives_inverse.

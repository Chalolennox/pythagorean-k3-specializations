(* code/coq/Dossier_crt_two_adic.v

   THIS FILE: (1) crt_compat: (exists n, m | n - a and l | n - b) <-> gcd(m,l) | a - b; (2) two_adic_cover: every n > 0 lies in exactly one A_k = {n = 2^(k-1) mod 2^k}, written with j = k-1.
   Written by Claude (a language model) in review, 23 November 2026.  NO HUMAN HAS CHECKED IT; the only compile check is CI (Coq 8.20.1).  Standalone (ZArith, Lia, Ring only).
   Not one of the owner's files.  Part of the elementary dossier theorems (split into several files so that CI shows which part is slow or failing):
     Dossier_crt_two_adic.v   (1) generalized CRT compatibility, (2) the 2-adic covering of the positive integers;
     Dossier_sextic_cleared.v (3a) the quotient sextic R of x -> 2/x: the cleared identity h hT = X^6 R(X + 2/X);
     Dossier_sextic_norm.v    (3b) the norm form R(z1+z2) = h(z1) h(z2) for z1 z2 = 2, with an explicit cofactor;
     Dossier_Fs_g_hom.v       (4) the F_s congruences of Lemma R (F.52), (5) the homogeneous g(tau(t)) identity.
   The statements about x(Q+T) = 2/x and the rational form of g(tau(t)) are in Dossier_elementary_rational.v (QArith).
   WHAT IT DOES NOT PROVE: anything about elliptic curves or root numbers; polynomial identity, divisibility and counting only.  Each identity was also checked in exact arithmetic with
   code/verify_dossier_elementary.py.  The statements were chosen by Claude from the dossier text, so whether they are the statements the owner wants is for a human to check. *)

From Coq Require Import ZArith Znumtheory Ring Lia.

Open Scope Z_scope.

(* ============================================================ *)
(* (1) GENERALIZED CRT COMPATIBILITY                            *)
(* ============================================================ *)

Theorem crt_compat :
  forall m l a b : Z,
    (exists n : Z, (m | n - a) /\ (l | n - b)) <->
    (Z.gcd m l | a - b).
Proof.
  intros m l a b.
  split.
  - intros [n [[k1 H1] [k2 H2]]].
    destruct (Z.gcd_divide_l m l) as [c1 Hc1].
    destruct (Z.gcd_divide_r m l) as [c2 Hc2].
    set (g := Z.gcd m l) in *.
    clearbody g.
    rewrite Hc1 in H1.
    rewrite Hc2 in H2.
    exists (c2*k2 - c1*k1).
    assert (E : a - b = (n - b) - (n - a)) by ring.
    rewrite E, H1, H2.
    ring.
  - intros [k Hk].
    assert (Hb : exists u v : Z, u*m + v*l = Z.gcd m l).
    {
      destruct (Z.gcd_bezout m l (Z.gcd m l) eq_refl) as [u [v H]].
      exists u, v.
      first [exact H | (rewrite <- H; ring) | lia].
    }
    destruct Hb as [u [v Hb]].
    rewrite <- Hb in Hk.
    exists (a - m*u*k).
    split.
    + exists (-u*k).
      ring.
    + exists (k*v).
      assert (E : a - m*u*k - b = (a - b) - m*u*k) by ring.
      rewrite E, Hk.
      ring.
Qed.

(* ============================================================ *)
(* (2) THE 2-ADIC COVERING                                      *)
(* ============================================================ *)

Fixpoint pow2 (j : nat) : Z :=
  match j with
  | O => 1
  | S j' => 2 * pow2 j'
  end.

Lemma pow2_pos : forall j : nat, 0 < pow2 j.
Proof.
  induction j as [|j IH].
  - change (pow2 0) with 1. lia.
  - change (pow2 (S j)) with (2 * pow2 j). lia.
Qed.

Lemma pow2_is_power : forall j : nat, pow2 j = 2 ^ Z.of_nat j.
Proof.
  induction j as [|j IH].
  - reflexivity.
  - change (pow2 (S j)) with (2 * pow2 j).
    rewrite Nat2Z.inj_succ.
    rewrite Z.pow_succ_r by apply Nat2Z.is_nonneg.
    rewrite IH.
    reflexivity.
Qed.

(* A_(j+1) = { n : n = 2^j mod 2^(j+1) }; j = k - 1 for the paper's A_k. *)
Definition in_A (j : nat) (n : Z) : Prop :=
  (2 ^ Z.of_nat (S j) | n - 2 ^ Z.of_nat j).

Lemma in_A_iff :
  forall (j : nat) (n : Z),
    in_A j n <-> exists q : Z, n = pow2 j * (2*q + 1).
Proof.
  intros j n.
  unfold in_A.
  rewrite <- !pow2_is_power.
  change (pow2 (S j)) with (2 * pow2 j).
  split.
  - intros [m Hm].
    exists m.
    first [lia | (ring_simplify in Hm; ring_simplify; lia)].
  - intros [q Hq].
    exists q.
    first [lia | (ring_simplify in Hq; ring_simplify; lia)].
Qed.

Lemma two_adic_exists_aux :
  forall N : nat, forall n : Z,
    0 < n -> n <= Z.of_nat N ->
    exists (j : nat) (q : Z), n = pow2 j * (2*q + 1).
Proof.
  induction N as [|N IH].
  - intros n Hn HnN. lia.
  - intros n Hn HnN.
    pose proof (Z.div_mod n 2 ltac:(discriminate)) as Hdm.
    pose proof (Z.mod_pos_bound n 2 ltac:(lia)) as Hb.
    destruct (Z.eq_dec (n mod 2) 0) as [He|Ho].
    + assert (Hm : 0 < n / 2) by lia.
      assert (Hm2 : n / 2 <= Z.of_nat N) by lia.
      destruct (IH (n / 2) Hm Hm2) as [j [q Hjq]].
      exists (S j), q.
      change (pow2 (S j)) with (2 * pow2 j).
      assert (Hn2 : n = 2 * (n / 2)) by lia.
      rewrite Hjq in Hn2.
      rewrite Hn2.
      ring.
    + exists O, (n / 2).
      change (pow2 0) with 1.
      lia.
Qed.

Lemma pow2_odd_inj :
  forall (j j' : nat) (q q' : Z),
    pow2 j * (2*q + 1) = pow2 j' * (2*q' + 1) -> j = j'.
Proof.
  intros j.
  induction j as [|j IH].
  - intros j' q q' H.
    destruct j' as [|j'].
    + reflexivity.
    + exfalso.
      change (pow2 0) with 1 in H.
      change (pow2 (S j')) with (2 * pow2 j') in H.
      assert (E : 2*q + 1 = 2 * (pow2 j' * (2*q' + 1))).
      { first [lia | (replace (2*q + 1) with (1 * (2*q + 1)) by ring; rewrite H; ring)]. }
      lia.
  - intros j' q q' H.
    destruct j' as [|j'].
    + exfalso.
      change (pow2 0) with 1 in H.
      change (pow2 (S j)) with (2 * pow2 j) in H.
      assert (E : 2*q' + 1 = 2 * (pow2 j * (2*q + 1))).
      { first [lia | (replace (2*q' + 1) with (1 * (2*q' + 1)) by ring; rewrite <- H; ring)]. }
      lia.
    + change (pow2 (S j)) with (2 * pow2 j) in H.
      change (pow2 (S j')) with (2 * pow2 j') in H.
      assert (H' : pow2 j * (2*q + 1) = pow2 j' * (2*q' + 1)).
      { first [lia | (apply (proj1 (Z.mul_cancel_l _ _ 2 ltac:(discriminate))); rewrite <- !Z.mul_assoc in H; exact H)]. }
      f_equal.
      exact (IH j' q q' H').
Qed.

Theorem two_adic_cover :
  forall n : Z, 0 < n -> exists j : nat, in_A j n /\ forall j' : nat, in_A j' n -> j' = j.
Proof.
  intros n Hn.
  assert (HN : n <= Z.of_nat (Z.to_nat n)) by (rewrite Z2Nat.id; lia).
  destruct (two_adic_exists_aux (Z.to_nat n) n Hn HN) as [j [q Hq]].
  exists j.
  split.
  - apply in_A_iff.
    exists q.
    exact Hq.
  - intros j' Hj'.
    apply in_A_iff in Hj'.
    destruct Hj' as [q' Hq'].
    symmetry.
    apply (pow2_odd_inj j j' q q').
    rewrite <- Hq.
    exact Hq'.
Qed.

(* ============================================================ *)
(* VERIFICATION                                                 *)
(* ============================================================ *)

Check crt_compat.
Check two_adic_cover.

Print Assumptions crt_compat.
Print Assumptions two_adic_cover.

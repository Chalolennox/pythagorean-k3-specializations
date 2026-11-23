(* code/coq/Dossier_elementary_theorems.v

   Written by Claude (a language model) in review, 23 November 2026.  NO HUMAN HAS CHECKED IT; the only compile check is CI (Coq 8.20.1).  Standalone (ZArith, Lia, Ring only).
   Not one of the owner's files.  Formalizes the elementary statements of the Problem-H dossier that need no elliptic-curve group law:
     (1) crt_compat: generalized CRT: (exists n, m | n - a and l | n - b)  <->  gcd(m,l) | a - b  (Z.gcd_bezout for the inverse direction; witness n = a - m u k);
     (2) two_adic_cover: every integer n > 0 lies in exactly one A_k = { n = 2^(k-1) mod 2^k }, k >= 1 (written with j = k-1: n - 2^j divisible by 2^(j+1));
     (3) the cleared identity of the quotient sextic: h(X) hT(X) = X^6 R(X + 2/X) as a polynomial identity in X (R as in paper F.26), and the norm form
         R(z1 + z2) = h(z1) h(z2) whenever z1 z2 = 2 (R(U) = Res_Z(Z^2 - U Z + 2, h(Z))), with the explicit cofactor R(z1+z2) - h(z1)h(z2) = (z1 z2 - 2) Rcof;
     (4) the congruences of F_s(U,V) = U^6 - 30U^4V^2 - 24U^2V^4 - V^6 used in Lemma R of F.52: F_s = -V^6 mod U, F_s = U^6 mod V, and
         F_s + 54 U^6 = (V - U)(V + U) K, hence F_s = -54 U^6 modulo every divisor of V - U and of V + U (modulo P' and Q');
     (5) the homogeneous form of g(tau(t)) = 4 g(t)/(1-t)^4: with g_hom(a,b) = 2ab(b^2 - a^2), g_hom(-(a+b), b-a) = 4 g_hom(a,b).
   The statements about x(Q+T) = 2/x and the rational form of g(tau(t)) are in Dossier_elementary_rational.v (QArith).
   WHAT IT DOES NOT PROVE: anything about elliptic curves or root numbers; it is polynomial identity, divisibility and counting only.  Each identity was also checked in exact arithmetic with an
   independent Python script before this file was written.  The statements were chosen by Claude from the dossier text, so whether they are the statements the owner wants is for a human to check. *)

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
    first [lia | nia | (ring_simplify in H1; ring_simplify in H2; ring_simplify; lia)].
  - intros [k Hk].
    assert (Hb : exists u v : Z, u*m + v*l = Z.gcd m l).
    {
      destruct (Z.gcd_bezout m l (Z.gcd m l) eq_refl) as [u [v H]].
      exists u, v.
      first [exact H | (rewrite <- H; ring) | lia | nia].
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
    first [lia | nia | (ring_simplify in Hm; ring_simplify; lia)].
  - intros [q Hq].
    exists q.
    first [lia | nia | (ring_simplify in Hq; ring_simplify; lia)].
Qed.

Lemma two_adic_exists_aux :
  forall N : nat, forall n : Z,
    0 < n -> n <= Z.of_nat N ->
    exists (j : nat) (q : Z), n = pow2 j * (2*q + 1).
Proof.
  induction N as [|N IH].
  - intros n Hn HnN. lia.
  - intros n Hn HnN.
    destruct (Z.eq_dec (n mod 2) 0) as [He|Ho].
    + assert (Hm : 0 < n / 2) by lia.
      assert (Hm2 : n / 2 <= Z.of_nat N) by lia.
      destruct (IH (n / 2) Hm Hm2) as [j [q Hjq]].
      exists (S j), q.
      change (pow2 (S j)) with (2 * pow2 j).
      first [lia | nia].
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
      { first [lia | nia | (ring_simplify in H; ring_simplify; lia)]. }
      lia.
  - intros j' q q' H.
    destruct j' as [|j'].
    + exfalso.
      change (pow2 0) with 1 in H.
      change (pow2 (S j)) with (2 * pow2 j) in H.
      assert (E : 2*q' + 1 = 2 * (pow2 j * (2*q + 1))).
      { first [lia | nia | (ring_simplify in H; ring_simplify; lia)]. }
      lia.
    + change (pow2 (S j)) with (2 * pow2 j) in H.
      change (pow2 (S j')) with (2 * pow2 j') in H.
      assert (H' : pow2 j * (2*q + 1) = pow2 j' * (2*q' + 1)).
      { first [lia | nia | (ring_simplify in H; ring_simplify; lia)]. }
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
(* (3) THE QUOTIENT SEXTIC OF x -> 2/x  (paper F.26)            *)
(* ============================================================ *)

(* h(x) = H(1 - x) with H(t) = t^6 - 30 t^4 - 24 t^2 - 1 *)
Definition hZ (x : Z) : Z :=
  (1 - x)^6 - 30*(1 - x)^4 - 24*(1 - x)^2 - 1.

(* hT(X) = X^6 h(2/X), cleared of denominators:  (1 - 2/X) X = X - 2 *)
Definition hT (X : Z) : Z :=
  (X - 2)^6 - 30*(X - 2)^4*X^2 - 24*(X - 2)^2*X^4 - X^6.

Definition RZ (u : Z) : Z :=
  -54*u^6 + 648*u^5 - 1242*u^4 - 11404*u^3 + 62082*u^2 - 113832*u + 73224.

(* h(X) hT(X) = X^6 R(X + 2/X), with X^6 R(X + 2/X) = sum_k r_k (X^2 + 2)^k X^(6-k) *)
Theorem sextic_cleared_identity :
  forall X : Z,
    hZ X * hT X =
      -54*(X^2 + 2)^6
      + 648*(X^2 + 2)^5*X
      - 1242*(X^2 + 2)^4*X^2
      - 11404*(X^2 + 2)^3*X^3
      + 62082*(X^2 + 2)^2*X^4
      - 113832*(X^2 + 2)*X^5
      + 73224*X^6.
Proof.
  intros X.
  unfold hZ, hT.
  ring.
Qed.

Definition Rcof (z1 z2 : Z) : Z :=
  (-35154) + (52542)*z2^1 + (-25938)*z2^2 + (3002)*z2^3 + (1026)*z2^4 + (-162)*z2^5 + (52542)*z1^1 + (-66537)*z1^1*z2^1 + (28068)*z1^1*z2^2 + (-2385)*z1^1*z2^3 + (-1334)*z1^1*z2^4 + (189)*z1^1*z2^5 + (-25938)*z1^2 + (28068)*z1^2*z2^1 + (-11682)*z1^2*z2^2 + (1344)*z1^2*z2^3 + (630)*z1^2*z2^4 + (-100)*z1^2*z2^5 + (3002)*z1^3 + (-2385)*z1^3*z2^1 + (1344)*z1^3*z2^2 + (-301)*z1^3*z2^3 + (-78)*z1^3*z2^4 + (15)*z1^3*z2^5 + (1026)*z1^4 + (-1334)*z1^4*z2^1 + (630)*z1^4*z2^2 + (-78)*z1^4*z2^3 + (-38)*z1^4*z2^4 + (6)*z1^4*z2^5 + (-162)*z1^5 + (189)*z1^5*z2^1 + (-100)*z1^5*z2^2 + (15)*z1^5*z2^3 + (6)*z1^5*z2^4 + (-1)*z1^5*z2^5.

Lemma sextic_norm_cofactor :
  forall z1 z2 : Z,
    RZ (z1 + z2) - hZ z1 * hZ z2 = (z1*z2 - 2) * Rcof z1 z2.
Proof.
  intros z1 z2.
  unfold RZ, hZ, Rcof.
  ring.
Qed.

(* R(U) = Res_Z(Z^2 - U Z + 2, h(Z)) is the quadratic norm: R(z1 + z2) = h(z1) h(z2) when z1 z2 = 2 *)
Theorem sextic_norm_identity :
  forall z1 z2 : Z,
    z1 * z2 = 2 -> RZ (z1 + z2) = hZ z1 * hZ z2.
Proof.
  intros z1 z2 Hz.
  pose proof (sextic_norm_cofactor z1 z2) as E.
  rewrite Hz in E.
  assert (E2 : (2 - 2) * Rcof z1 z2 = 0) by ring.
  rewrite E2 in E.
  lia.
Qed.

(* ============================================================ *)
(* (4) THE CONGRUENCES OF F_s (Lemma R of F.52)                 *)
(* ============================================================ *)

Definition Fs (U V : Z) : Z :=
  U^6 - 30*U^4*V^2 - 24*U^2*V^4 - V^6.

Theorem Fs_mod_U :
  forall U V : Z, (U | Fs U V + V^6).
Proof.
  intros U V.
  exists (U^5 - 30*U^3*V^2 - 24*U*V^4).
  unfold Fs.
  ring.
Qed.

Theorem Fs_mod_V :
  forall U V : Z, (V | Fs U V - U^6).
Proof.
  intros U V.
  exists (-30*U^4*V - 24*U^2*V^3 - V^5).
  unfold Fs.
  ring.
Qed.

Definition Fs_cofactor (U V : Z) : Z :=
  -30*U^4 - 24*U^2*(V^2 + U^2) - (V^4 + V^2*U^2 + U^4).

(* F_s(U,V) + 54 U^6 = (V - U)(V + U) K : F_s(U, +-U) = -54 U^6 *)
Theorem Fs_factorization :
  forall U V : Z,
    Fs U V + 54*U^6 = (V - U) * ((V + U) * Fs_cofactor U V).
Proof.
  intros U V.
  unfold Fs, Fs_cofactor.
  ring.
Qed.

Theorem Fs_mod_V_minus_U :
  forall U V W : Z, (W | V - U) -> (W | Fs U V + 54*U^6).
Proof.
  intros U V W [c Hc].
  rewrite Fs_factorization.
  rewrite Hc.
  exists (c * ((V + U) * Fs_cofactor U V)).
  ring.
Qed.

Theorem Fs_mod_V_plus_U :
  forall U V W : Z, (W | V + U) -> (W | Fs U V + 54*U^6).
Proof.
  intros U V W [c Hc].
  rewrite Fs_factorization.
  rewrite Hc.
  exists (c * ((V - U) * Fs_cofactor U V)).
  ring.
Qed.

(* ============================================================ *)
(* (5) g(tau(t)) = 4 g(t) / (1 - t)^4, homogeneous form         *)
(* ============================================================ *)

(* t = a/b, g(t) = 2 t (1 - t^2) = g_hom(a,b)/b^4; tau(t) = 1 - 2/(1 - t) = -(a + b)/(b - a). *)
Definition g_hom (a b : Z) : Z :=
  2*a*b*(b^2 - a^2).

Theorem g_hom_tau :
  forall a b : Z,
    g_hom (-(a + b)) (b - a) = 4 * g_hom a b.
Proof.
  intros a b.
  unfold g_hom.
  ring.
Qed.

(* ============================================================ *)
(* VERIFICATION                                                 *)
(* ============================================================ *)

Check crt_compat.
Check two_adic_cover.
Check sextic_cleared_identity.
Check sextic_norm_identity.
Check Fs_mod_U.
Check Fs_mod_V.
Check Fs_mod_V_minus_U.
Check Fs_mod_V_plus_U.
Check g_hom_tau.

Print Assumptions crt_compat.
Print Assumptions two_adic_cover.
Print Assumptions sextic_cleared_identity.
Print Assumptions sextic_norm_identity.
Print Assumptions Fs_mod_V_minus_U.
Print Assumptions Fs_mod_V_plus_U.
Print Assumptions g_hom_tau.

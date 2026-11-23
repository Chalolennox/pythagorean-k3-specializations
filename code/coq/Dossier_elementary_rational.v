(* code/coq/Dossier_elementary_rational.v

   Written by Claude (a language model) in review, 23 November 2026.  NO HUMAN HAS CHECKED IT; the only compile check is CI (Coq 8.20.1).  Standalone (QArith, field).
   Not one of the owner's files.  Rational-function form of two dossier identities, for the curve C: y^2 = x^3 - 2x^2 + 2x with T = (0,0), t = 1 - x:
     (1) chord_QT_x_value: for x != 0 and y^2 = x^3 - 2x^2 + 2x, the chord-and-tangent x-coordinate of Q + T, namely (y/x)^2 + 2 - x (slope y/x of the line through Q = (x,y) and T = (0,0);
         for y^2 = x^3 + a2 x^2 + a4 x + a6 the formula is x3 = slope^2 - a2 - x1 - x2, here a2 = -2), equals 2/x;
         chord_QT_y_value: the matching y-coordinate -(slope (x3 - x) + y) equals -2y/x^2; chord_QT_on_curve: the point (2/x, -2y/x^2) lies on C;
     (2) gQ_tau: g(tau(t)) = 4 g(t)/(1-t)^4, where g(t) = 2t(1 - t^2) and tau(t) = 1 - 2/(1 - t) = t(Q+T) for t = t(Q) = 1 - x(Q) (so x(Q+T) = 2/x gives 1 - 2/(1-t)), for t != 1.
   WHAT IT DOES NOT PROVE: that the chord formulas are the group law of C (they are taken as the definition, as in the textbook chord-and-tangent formulas); nothing about root numbers.
   The homogeneous integer form of (2) is g_hom_tau in Dossier_elementary_theorems.v. *)

From Coq Require Import QArith Qfield.

Open Scope Q_scope.

(* ============================================================ *)
(* (1) x(Q + T) = 2/x                                           *)
(* ============================================================ *)

Definition chord_QT_x (x y : Q) : Q :=
  (y / x) * (y / x) + 2 - x.

Definition chord_QT_y (x y : Q) : Q :=
  - ((y / x) * (chord_QT_x x y - x) + y).

Theorem chord_QT_x_value :
  forall x y : Q,
    ~ x == 0 ->
    y * y == x * x * x - 2 * x * x + 2 * x ->
    chord_QT_x x y == 2 / x.
Proof.
  intros x y Hx Hy.
  unfold chord_QT_x.
  assert (E : y / x * (y / x) + 2 - x == (y * y) / (x * x) + 2 - x).
  { field. assumption. }
  rewrite E.
  rewrite Hy.
  field.
  assumption.
Qed.

Theorem chord_QT_y_value :
  forall x y : Q,
    ~ x == 0 ->
    y * y == x * x * x - 2 * x * x + 2 * x ->
    chord_QT_y x y == - 2 * y / (x * x).
Proof.
  intros x y Hx Hy.
  unfold chord_QT_y.
  rewrite (chord_QT_x_value x y Hx Hy).
  field.
  assumption.
Qed.

Theorem chord_QT_on_curve :
  forall x y : Q,
    ~ x == 0 ->
    y * y == x * x * x - 2 * x * x + 2 * x ->
    chord_QT_y x y * chord_QT_y x y ==
      chord_QT_x x y * chord_QT_x x y * chord_QT_x x y
      - 2 * chord_QT_x x y * chord_QT_x x y
      + 2 * chord_QT_x x y.
Proof.
  intros x y Hx Hy.
  rewrite (chord_QT_x_value x y Hx Hy).
  rewrite (chord_QT_y_value x y Hx Hy).
  assert (E : (- 2 * y / (x * x)) * (- 2 * y / (x * x)) == 4 * (y * y) / (x * x * x * x)).
  { field. assumption. }
  rewrite E.
  rewrite Hy.
  field.
  assumption.
Qed.

(* ============================================================ *)
(* (2) g(tau(t)) = 4 g(t) / (1 - t)^4                           *)
(* ============================================================ *)

Definition gQ (t : Q) : Q :=
  2 * t * (1 - t * t).

Definition tauQ (t : Q) : Q :=
  1 - 2 / (1 - t).

Theorem gQ_tau :
  forall t : Q,
    ~ 1 - t == 0 ->
    gQ (tauQ t) == 4 * gQ t / ((1 - t) * (1 - t) * (1 - t) * (1 - t)).
Proof.
  intros t H.
  unfold gQ, tauQ.
  field.
  assumption.
Qed.

Check chord_QT_x_value.
Check chord_QT_y_value.
Check chord_QT_on_curve.
Check gQ_tau.

Print Assumptions chord_QT_x_value.
Print Assumptions chord_QT_y_value.
Print Assumptions chord_QT_on_curve.
Print Assumptions gQ_tau.

// Reconstructed subgroup certificate; unexecuted revision.
function h(x)
 return x^6-6*x^5-15*x^4+100*x^3-189*x^2+162*x-54;
end function;
function Y(x)
 return x^3-2*x^2+2*x;
end function;
function key(Q)
 if Q eq Parent(Q)!0 then return "O"; end if;
 return Sprint(Q[1]/Q[3]) cat ":" cat Sprint(Q[2]/Q[3]);
end function;
function member(Q,P,d,mods,tables)
 if d*Q ne Parent(P)!0 then return false,-1; end if;
 logs:=[];
 for i in [1..#mods] do
  c:=d div mods[i]; A:=tables[i];
  ok,j:=IsDefined(A,key(c*Q));
  if not ok then return false,-1; end if;
  Append(~logs,j);
 end for;
 n:=CRT(logs,mods) mod d;
 assert n*P eq Q;
 return true,n;
end function;
start:=Cputime();
orig:=[]; full:=[];
for p in [229,609613,1386618529213] do
 K:=GF(p); E:=EllipticCurve([K!0,K!(-2),K!0,K!2,K!0]);
 P:=E![1,1,1]; T:=E![0,0,1]; O:=E!0;
 assert T ne O and 2*T eq O;
 d:=Order(P); fac:=Factorization(d);
 assert d*P eq O;
 assert &*[a[1]^a[2]:a in fac] eq d;
 mods:=[]; tables:=[];
 for a in fac do
  assert IsPrime(a[1]); assert (d div a[1])*P ne O;
  m:=a[1]^a[2]; G:=(d div m)*P;
  A:=AssociativeArray(); Q:=O;
  for j in [0..m-1] do
   assert not IsDefined(A,key(Q)); A[key(Q)]:=j; Q+:=G;
  end for;
  assert Q eq O;
  Append(~mods,m); Append(~tables,A);
 end for;
 R<x>:=PolynomialRing(K); S:=[]; U:=[]; V:=[];
 for r in Roots(h(x)) do
  a:=r[1]; t:=1-a; c:=2*t*(1-t^2);
  if c ne 0 and IsSquare(c) then
   for y in Roots(x^2-Y(a)) do Append(~S,E![a,y[1],1]); end for;
  end if;
 end for;
 print "Prime, order",p,d;
 for Q in S do
  b,n:=member(Q,P,d,mods,tables);
  c,k:=member(Q-T,P,d,mods,tables);
  print Q,b,n,c,k;
  if b then Append(~U,Q); end if;
  if b or c then Append(~V,Q); end if;
 end for;
 A:=[<a,b,a+b>:a,b in U | a+b in U];
 B:=[<a,b,a+b>:a,b in V | a+b in V];
 print "Triples",A,B;
 if #A gt 0 then Append(~orig,p); end if;
 if #B gt 0 then Append(~full,p); end if;
end for;
assert orig eq [609613];
assert full eq [609613,1386618529213];
print "PASS",orig,full,Cputime(start);

\\ PARI/GP. Reconstructed from the recorded local 2-adic tests.
\\ elllocalred returns reduction data, including Kodaira code.
a=1; b=0;
for(n=0,11,
  E=ellinit([0,0,0,4*a*5^(3*n),-8*b*5^(5*n)]);
  print("n=",n," a=",a," b=",b);
  print("local reduction at 2: ",elllocalred(E,2));
  print("global root number: ",ellrootno(E));
  aa=3*a-4*b; bb=4*a+3*b; a=aa; b=bb;
);

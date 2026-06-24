function x=Q3(A,b)
%每次先存下来·=A*·，再计算A'*·，这样就避免了显式的A'*A
    n=length(b);
    x=zeros(n,1);
    r=b-A*x;
    r=A'*r;
    p=r;
    while norm(p)>e-10
        w=A*p;
        al=r'*r/(w'*w);
        x=x-p*al;
        r1=r-al*A'*w;
        be=r1'*r1/(r'*r);
        p=r1+p*be;
        r=r1;
    end
end
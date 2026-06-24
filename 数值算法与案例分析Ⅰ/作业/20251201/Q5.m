n=250;h=1/(n+1);
x=linspace(0,1,n+2);
y=linspace(0,1,n+2);
[X,Y]=meshgrid(x,y);
A=sparse(n^2,n^2);
for i=1:n
    for j=1:n
        k=(i-1)*n+j;
        A(k,k)=-4;
        if i>1,A(k,k-n)=1;end
        if i<n,A(k,k+n)=1;end
        if j>1,A(k,k-1)=1;end
        if j<n,A(k,k+1)=1;end
    end
end
A=A/h^2;
b=zeros(n^2,1);
for i=1:n
    b(i)=-sin(pi*i*h)/h^2;
end

function[x,rnorm]=CG(A,b)
    m=length(b);
    x=zeros(m,1);
    r=b-A*x;
    p=r;
    rnorm=[norm(r)];
    while rnorm(:,end)>1e-14
        Ap=A*p;
        al=r'*r/(p'*Ap);
        x=x+p*al;
        r1=r-Ap*al;
        be=r1'*r1/(r'*r);
        p=r1+p*be;
        r=r1;
        rnorm=[rnorm,norm(r)];
    end
end

[x,rnorm]=CG(A,b);
u=reshape(x,n,n);

figure;
surf(X(2:end-1,2:end-1),Y(2:end-1,2:end-1),u');
shading interp;
xlabel('x');ylabel('y');zlabel('u');
title('Solution to 2D Laplace Equation');

figure;
semilogy(rnorm,'o-');
xlabel('Iteration');ylabel('Residual norm');
title('Convergence history');
grid on;
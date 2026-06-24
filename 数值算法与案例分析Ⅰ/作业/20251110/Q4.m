function[X,k,err]=halfpower(A)
    X=eye(size(A));
    k=0;
    tol=1e-10;
    max_iter=100;
    while true
        X=(X+A/X)/2;
        k=k+1;
        err=norm(X*X-A,'fro')/norm(A,'fro');
        if err<tol || k>max_iter
            break;
        end
    end
end

n=1000;
D=randn(n)+1i*randn(n);
[Q,~]=qr(D);
eigvals=rand(n,1)*100+0.1;
Lambda=diag(eigvals);
A=Q*Lambda*Q';

[X,k,err]=halfpower(A);

disp(err);
disp(k);
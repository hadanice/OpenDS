function B = my_expm(A)
    m=30;
    normA = norm(A, 1);

    if normA==0
        B=eye(size(A));
        return;
    end

    s=max(0,ceil(log2(normA))); 
    A_scaled = A/2^s;
    T=eye(size(A));
    term=eye(size(A));

    for k = 1:m
        term=term*A_scaled/k;
        T=T+term;
    end

    for k=1:s
        T=T*T;
    end

    B=T;
end

n=1000;
lambda=linspace(-100, 100, n);
[Q,~]=qr(randn(n));                
A=Q*diag(lambda)*Q';  
expA_my=my_expm(A);
expA_true=Q*diag(exp(lambda))*Q';
err=norm(expA_my-expA_true,'fro')/norm(expA_true,'fro');
disp(err);
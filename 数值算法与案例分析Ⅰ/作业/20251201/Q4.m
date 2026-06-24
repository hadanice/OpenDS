function[x,R,P,rnorm]=CG_vis(A,b)
    n=length(b);
    x=zeros(n,1);
    r=b-A*x;
    p=r;
    R=r;
    P=p;
    rnorm=[norm(r)];
    while rnorm(:,end)>1e-15
        Ap=A*p;
        al=r'*r/(p'*Ap);
        x=x+p*al;
        r=r-Ap*al;
        be=r'*r/(R(:,end)'*R(:,end));
        p=r+p*be;
        R=[R,r];
        P=[P,p];
        rnorm=[rnorm,norm(r)];
    end

    for j=1:size(R,2)
        nrm=norm(R(:,j));
        if nrm>eps
            R(:,j)=R(:,j)/nrm;
        end
    end

    for j = 1:size(P,2)
        pj=P(:,j);
        scale=sqrt(pj'*A*pj);
        if scale>eps
            P(:,j)=pj/scale;
        end
    end

    R1=R'*R;
    P1=P'*A*P;
    vis1=log(abs(R1-eye(size(R1))));
    vis2=log(abs(P1-eye(size(P1))));

    figure;
    subplot(2,2,1);
    semilogy(rnorm, 'o-');
    xlabel('Iteration');
    ylabel('Residual norm');
    title('Convergence history');
    grid on;
    
    subplot(2,2,2);
    imagesc(vis1);
    colorbar;
    title('|R*R-I|(log)');
    xlabel('Column index');
    ylabel('Row index');
    
    subplot(2,2,3);
    imagesc(vis2);
    colorbar;
    title('|P*AP-I|(log)');
    xlabel('Column index');
    ylabel('Row index');
    
    subplot(2,2,4);
    plot(diag(R1),'ro'); hold on;
    plot(diag(P1),'b*');
    legend('diag(R^*R)','diag(P^*AP)');
    title('Diagonal entries');

    if nargout == 0
        clear x;
    end
end


n=1000;
A=randn(n);
A=A'*A+eye(n);
b=randn(n,1);

[x,R,P,rnorm]=CG_vis(A,b);
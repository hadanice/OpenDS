P=zeros(600);
T=zeros(600);
for k=1:600
    L=randn(k,k);
    b=randn(k,1);
    [A,d,t]=gauss(k,L,b);
    T(k)=[log(t)];
    P(k)=[log(k)];
end
scatter(P,T);
saveas(gcf, 'log–log scale plo.png');
function [A,d,t] = gauss(n,L,b)
%Gauss消元，两重循环
tic;%开始计时
U=[L,b];
for i = 1:n-1
    for j = i+1:n
        factor = U(j,i)/U(i,i);
        U(j,i:n+1)= U(j,i:n+1)-factor*U(i,i:n+1);
    end
end
A = U(1:n,1:n);
d = U(1:n,n+1);
t = toc;%结束计时
end
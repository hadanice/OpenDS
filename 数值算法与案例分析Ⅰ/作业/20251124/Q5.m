function[history]=SD(A,x,b,maxit)
    r=b-A*x;
    history=x';
    for iter=1:maxit
        p=A*r;
        alpha=r'*r/(r'*p);
        x=x+r*alpha;
        history=[history;x'];
        r=r-p*alpha;
    end
end

A=[20,0;0,1];
x=[1;5];
b=[0;0];
history=SD(A,x,b,10);

figure;
for i = 1:size(history, 2)
    plot(0:size(history, 1)-1, history(:, i), '-o', 'LineWidth', 1.5, 'MarkerSize', 6);
    hold on;
end
xlabel('Iteration k (0 ≤ k ≤ 10)');
ylabel('Approximation value');
title('Intermediate Approximations x_k for 0 ≤ k ≤ 10');
legend(arrayfun(@(i) ['x_' num2str(i)], 1:size(history, 2), 'UniformOutput', false));
grid on;
box on;
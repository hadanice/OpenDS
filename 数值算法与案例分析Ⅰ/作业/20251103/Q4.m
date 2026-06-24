n = 6;

d = sort(rand(n, 1)); 
z = randn(n, 1); 
z = z ./ max(abs(z)); 
z = z + 0.1*sign(z); 

A = diag(d) + z*z';
eigenvalues = eig(A);
f = @(lambda) 1 - sum(z.^2 ./ (lambda - d));

lambda_range = linspace(min(eigenvalues)-1, max(eigenvalues)+1, 1000);

f_values = arrayfun(f, lambda_range);

figure;
plot(lambda_range, f_values, 'b-', 'LineWidth', 2);
hold on;

plot(eigenvalues, zeros(size(eigenvalues)), 'ro', 'MarkerSize', 8, 'LineWidth', 2);
xlabel('λ');
ylabel('f(λ)');
grid on;

yline(0, 'k--', 'f(λ) = 0');
legend('f(λ)', '特征值', 'Location', 'best');
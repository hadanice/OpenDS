n=500;
h=1/(n+1);
max_iter=5000; 
tol=1e-10; 

U=zeros(n+2,n+2);

x_vals=0:h:1;
U(1,:)=sin(pi*x_vals); 
U(end,:)=0;              
U(:,1)=0;                
U(:,end)=0;              

res_history = [];

tic;
for iter=1:max_iter
    U_old=U;
    
    U(2:end-1,2:end-1) = 0.25 * ( ...
        U(1:end-2,2:end-1)+ ...   
        U(3:end,2:end-1)+ ...   
        U(2:end-1,1:end-2)+ ...   
        U(2:end-1,3:end));      

    U(1,:)=sin(pi*x_vals);
    U(end,:)=0;
    U(:,1)=0;
    U(:,end)=0;
    
    diff=max(max(abs(U-U_old)));
    res_history(end+1) = diff; 
    
    if diff<tol
        fprintf('Gauss-Seidel 在 %d 次迭代后收敛，残差 = %.2e\n', iter, diff);
        break;
    end
end
elapsed = toc;
fprintf('运行时间: %.4f 秒\n', elapsed);

U_interior=U(2:end-1, 2:end-1);
x_plot=linspace(h, 1 - h, n);
y_plot=x_plot;
[X,Y]=meshgrid(x_plot,y_plot);

figure;
surf(X,Y,U_interior);
shading interp;
xlabel('x'); ylabel('y'); zlabel('u(x,y)');
title(sprintf('2D Laplace Equation Solution (n=%d, GS)', n));
colorbar;

figure;
semilogy(1:length(res_history),res_history,'b-', 'LineWidth',1.5);
xlabel('Iteration');
ylabel('Max |U^{k+1}-U^k|');
title('Gauss-Seidel Convergence History');
grid on;
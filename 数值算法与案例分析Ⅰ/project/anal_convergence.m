%收敛行为分析
rng(21);
% 全局看对角线以下Frobenius范数，局部看每次处理块的最右下角的元素
fprintf('\n--- (b)全局与局部收敛行为 (400阶)---\n');
n=400;
A_b=randn(n,n);
n=size(A_b,1);
[H_b,Q_b]=reduce_to_hessenberg(A_b,n);
H_b=clean_subdiagonal(H_b,1,n);
[l,r]=locate_active_block(H_b,n);
iteration_time=0;
history=struct();
history.global_err=[];
history.local_err=[];
while r>1
    global_norm=norm(tril(H_b,-1),'fro');
    history.global_err(end+1)=global_norm;
    if r>l
        local_val=abs(H_b(r,r-1));
    else
        local_val=0; 
    end
    history.local_err(end+1)=local_val;
    
    if r-l==1
        [Q_b,H_b]=update_2x2_block(H_b,Q_b,l,n);
    else
        [Q_b,H_b]=francis_double_shift(H_b,Q_b,l,r,n);
    end
    H_b=clean_subdiagonal(H_b,l,r);
    [l, r]=locate_active_block(H_b,r);
    iteration_time=iteration_time+1;
end
fprintf('经过%d次迭代后收敛\n',iteration_time);
% 绘制图像
figure('Color','w','Position',[100,100,800,500]);
yyaxis left
semilogy(1:iteration_time,history.global_err,'-b','LineWidth',1.5);
ylabel('严格下三角部分的Frobenius范数','FontSize', 12);
ax=gca; 
ax.YColor='b';
yyaxis right
semilogy(1:iteration_time,history.local_err+1e-18,'-r','LineWidth',1.0); 
ylabel('实时处理的分块右下角次对角元的绝对值','FontSize',12);
ax.YColor='r';
xlabel('迭代次数','FontSize',12);
title('收敛行为分析','FontSize',14,'FontWeight','bold');
grid on;
legend({'严格下三角部分的Frobenius范数','分块右下角次对角元的绝对值'},'Location','southwest','FontSize',10)

saveas(gcf, ['convergence_plot.png']);
%% 稳定性验证：条件数对Francis QR算法性能的影响
clear; clc; close all;

%% 参数设置
n = 100;  % 固定矩阵维度
cond_numbers = logspace(1,12,12);  % 条件数从10^1到10^12
n_tests = length(cond_numbers);
rng(98);

% 预分配结果数组
forward_errors = zeros(n_tests, 1);
backward_errors = zeros(n_tests, 1);
orth_losses = zeros(n_tests, 1);
iter_counts = zeros(n_tests, 1);

fprintf('=== 稳定性验证 ===\n');
fprintf('测试矩阵维度: %d\n', n);
fprintf('条件数范围: 10^%.1f 到 10^%.1f\n', log10(cond_numbers(1)), log10(cond_numbers(end)));

%% 生成给定条件数的矩阵并测试
for k = 1:n_tests
    cond_num = cond_numbers(k);
    fprintf('\n测试%d/%d:条件数=%.1e', k, n_tests, cond_num);
    
    % 生成给定条件数的矩阵
    % 方法：创建对角矩阵，然后应用随机正交变换
    [U, ~] = qr(randn(n, n));  % 随机正交矩阵
    [V, ~] = qr(randn(n, n));  % 随机正交矩阵
    
    % 创建奇异值矩阵，条件数为cond_num
    if cond_num == 1
        S = eye(n);
    else
        % 对数间隔的奇异值
        singular_values = logspace(0, log10(cond_num), n);
        % 随机排列
        singular_values = singular_values(randperm(n));
        S = diag(singular_values);
    end
    
    % 构造矩阵 A = U * S * V'
    A = U * S * V';
    
    % 运行Francis QR算法
    tic;
    [U_qr, T_qr, iter] = my_frqr(A);
    time_elapsed = toc;
    
    % 存储迭代次数
    iter_counts(k) = iter;
    
    % 计算正交性损失
    orth_loss = norm(U_qr'*U_qr - eye(n), 'fro');
    orth_losses(k) = orth_loss;
    
    % 计算向后误差
    backward_error = norm(U_qr'*A*U_qr - T_qr, 'fro');
    rel_backward_error = backward_error / norm(A, 'fro');
    backward_errors(k) = rel_backward_error;
    
    % 计算特征值（向前误差）
    % 从T_qr提取特征值
    eig_qr = zeros(n, 1);
    idx = 1;
    while idx <= n
        if idx < n && abs(T_qr(idx+1, idx)) > 1e-12 * norm(T_qr, 'fro')
            % 2x2块
            sub_block = T_qr(idx:idx+1, idx:idx+1);
            e = eig(sub_block);
            eig_qr(idx) = e(1);
            eig_qr(idx+1) = e(2);
            idx = idx + 2;
        else
            % 1x1块
            eig_qr(idx) = T_qr(idx, idx);
            idx = idx + 1;
        end
    end
    
    % 使用MATLAB内置函数计算特征值
    eig_matlab = eig(A);
    
    % 排序特征值
    eig_qr_sorted = sort(eig_qr);
    eig_matlab_sorted = sort(eig_matlab);
    
    % 计算最大相对向前误差
    abs_errors = abs(eig_qr_sorted - eig_matlab_sorted);
    rel_errors = abs_errors ./ max(1, abs(eig_matlab_sorted));
    max_rel_error = max(rel_errors);
    forward_errors(k) = max_rel_error;
    
    fprintf('-迭代:%d,向前误差:%.2e,向后误差:%.2e', ...
        iter, max_rel_error, rel_backward_error);
end

%% 绘制结果
figure();

% 子图1: 向前误差（单独）
subplot(1,3,1);
loglog(cond_numbers, forward_errors, 'b-o', 'LineWidth', 2, 'MarkerSize', 8, 'MarkerFaceColor', 'b');
hold on;

% 添加参考线（线性依赖）
x_ref = [min(cond_numbers), max(cond_numbers)];
y_ref = 1e-15 * x_ref;  % 线性参考
loglog(x_ref, y_ref, 'r--', 'LineWidth', 1.5, 'DisplayName', 'O(κ)');

xlabel('条件数 κ');
ylabel('最大相对特征值误差');
title('向前误差 vs 条件数');
grid on;
legend('测试结果', 'O(κ) 参考线', 'Location', 'northwest');
set(gca, 'XScale', 'log', 'YScale', 'log');

% 子图2: 向后误差和正交性损失（合并）
subplot(1,3,2);
yyaxis left;
loglog(cond_numbers, backward_errors, 'g-s', 'LineWidth', 2, 'MarkerSize', 8, 'MarkerFaceColor', 'b');
ylabel('相对向后误差');
ylim([1e-15, 0.8e-14]);

yyaxis right;
loglog(cond_numbers, orth_losses, 'm-^', 'LineWidth', 2, 'MarkerSize', 8, 'MarkerFaceColor', 'm');
ylabel('正交性损失 ‖U^TU-I‖_F');

xlabel('条件数 κ');
title('向后误差和正交性损失 vs 条件数');
grid on;
legend('向后误差', '正交性损失', 'Location', 'northwest');
set(gca, 'XScale', 'log', 'YScale', 'log');

% 子图3: 迭代次数
subplot(1,3,3);
semilogx(cond_numbers, iter_counts, 'k-d', 'LineWidth', 2, 'MarkerSize', 8, 'MarkerFaceColor', 'k');
xlabel('条件数 κ');
ylabel('迭代次数');
title('迭代次数 vs 条件数');
grid on;

saveas(gcf, 'stability_plot.png');

% 添加条件数与精度的关系表格
fprintf('\n\n=== 稳定性测试汇总 ===\n');
fprintf('条件数(κ)\t向前误差\t向后误差\t正交损失\t迭代次数\n');
fprintf('----------\t----------\t----------\t----------\t----------\n');
for k = 1:n_tests
    fprintf('%.1e\t  %.2e\t  %.2e\t  %.2e\t  %d\n', ...
        cond_numbers(k), forward_errors(k), backward_errors(k), orth_losses(k), iter_counts(k));
end

%% 分析稳定性
fprintf('\n=== 稳定性分析 ===\n');

% 计算斜率（对数尺度）
log_cond = log10(cond_numbers(:));
log_forward = log10(forward_errors(:));

% 移除inf值
valid_idx = isfinite(log_forward);
if sum(valid_idx) > 2
    p = polyfit(log_cond(valid_idx), log_forward(valid_idx), 1);
    slope = p(1);
    fprintf('向前误差 vs 条件数的对数斜率: %.3f\n', slope);
    
    if abs(slope - 1) < 0.2
        fprintf('   结论: 向前误差与条件数近似线性相关 (O(κ))\n');
    elseif abs(slope) < 0.5
        fprintf('   结论: 向前误差对条件数不敏感\n');
    else
        fprintf('   结论: 向前误差与条件数呈幂律关系，指数 ≈ %.2f\n', slope);
    end
end

% 向后误差分析
log_backward = log10(backward_errors(:));
valid_idx = isfinite(log_backward);
if sum(valid_idx) > 2
    p = polyfit(log_cond(valid_idx), log_backward(valid_idx), 1);
    slope = p(1);
    fprintf('向后误差 vs 条件数的对数斜率: %.3f\n', slope);
    
    if abs(slope) < 0.5
        fprintf('   结论: 向后误差对条件数不敏感，算法向后稳定\n');
    else
        fprintf('   结论: 向后误差随条件数增长\n');
    end
end

fprintf('\n 稳定性验证完成。\n');
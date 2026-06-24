function test_complexity()
% TEST_COMPLEXITY - 验证Francis QR算法的时间复杂度
%   测量不同规模矩阵的运行时间，验证O(n^3)复杂度

    fprintf('=== 时间复杂度测试 ===\n\n');
    
    n_list = [100, 150, 200, 250, 300, 350, 400, 450, 500,600,750,1000];  % 矩阵规模
    n_tests = length(n_list);
    rng(98)
    
    time_ours = zeros(n_tests, 1);
    time_matlab = zeros(n_tests, 1);
    iterations = zeros(n_tests, 1);
    
    fprintf('%-10s %-12s %-12s %-10s\n', ...
            '规模n', '时间(秒)', 'MATLAB(秒)', '迭代次数');
    fprintf('%s\n', repmat('-', 1, 50));
    
    for i = 1:n_tests
        n = n_list(i);
        
        % 生成随机矩阵
        A = randn(n);
        
        % 测试我们的算法
        tic;
        [~, ~, iters] = my_frqr(A);
        time_ours(i) = toc;
        iterations(i) = iters;
        
        % 测试MATLAB内置函数
        tic;
        [~, ~] = schur(A);
        time_matlab(i) = toc;
        
        fprintf('%-10d %-12.4f %-12.4f %-10d\n', ...
                n, time_ours(i), time_matlab(i), iters);
    end
    
    % 理论复杂度参考
    n3_ref = n_list.^3;
    scale_factor = time_ours(end) / n3_ref(end);
    time_theory = n3_ref * scale_factor;
    
    % 可视化结果
    figure();
    
    % 子图1：运行时间对比
    subplot(1,2,1);
    loglog(n_list, time_ours, 'bo-', 'LineWidth', 2, 'MarkerSize', 10);
    hold on;
    loglog(n_list, time_matlab, 'ro-', 'LineWidth', 2, 'MarkerSize', 10);
    loglog(n_list, time_theory, 'k--', 'LineWidth', 2);
    
    xlabel('矩阵规模 n');
    ylabel('运行时间 (秒)');
    title('运行时间 vs 矩阵规模');
    legend('my frqr', 'MATLAB schur', 'O(n^3)参考线', 'Location', 'best');
    grid on;
    
    % 添加复杂度拟合
    p = polyfit(log(n_list), log(time_ours), 1);
    exponent = p(1);
    annotation('textbox', [0.15, 0.7, 0.2, 0.1], ...
               'String', sprintf('拟合指数: %.2f', exponent), ...
               'FitBoxToText', 'on', 'BackgroundColor', 'white');
    
    % 子图2：迭代次数
    subplot(1,2,2);
    plot(n_list, iterations, 'gs-', 'LineWidth', 2, 'MarkerSize', 10);
    xlabel('矩阵规模 n');
    ylabel('迭代次数');
    title('迭代次数 vs 矩阵规模');
    grid on;
    
    % 多项式拟合迭代次数
    p_iter = polyfit(n_list, iterations, 1);
    annotation('textbox', [0.65, 0.75, 0.2, 0.1], ...
               'String', sprintf('迭代次数 ≈ %.1fn + %.1f', p_iter(1), p_iter(2)), ...
               'FitBoxToText', 'on', 'BackgroundColor', 'white');
    
    % 保存图像
    saveas(gcf, 'complexity_plot.png');
    
    % 复杂度分析表格
    fprintf('\n=== 复杂度分析 ===\n');
    fprintf('矩阵规模范围: %d - %d\n', min(n_list), max(n_list));
    fprintf('时间拟合指数: %.3f (理论值: 3.000)\n', exponent);
    fprintf('迭代次数线性拟合斜率: %.3f\n', p_iter(1));
    
    % 计算加速比
    speedup = time_matlab ./ time_ours;
    fprintf('\n%-10s %-12s\n', '规模n', '加速比(ours/MATLAB)');
    fprintf('%s\n', repmat('-', 1, 35));
    for i = 1:n_tests
        fprintf('%-10d %-12.2f\n', n_list(i), speedup(i));
    end
end
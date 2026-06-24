function test_correctness()
% TEST_CORRECTNESS - 验证Francis QR算法的正确性
%   测试指标：
%   1. 正交性损失: norm(U'*U - I, 'fro')
%   2. 向后误差: norm(U'*A*U - T, 'fro')/norm(A, 'fro')
%   3. Schur形结构: 检查T是否为拟上三角矩阵

    fprintf('=== 正确性验证测试 ===\n\n');
    
    n_list = [10, 20, 50, 100, 150, 200, 300, 400, 500];  % 测试不同规模的矩阵
    n_tests = length(n_list);
    
    orth_error = zeros(n_tests, 1);
    backward_error = zeros(n_tests, 1);
    schur_valid = true(n_tests, 1);

    rng(21);
    
    for i = 1:n_tests
        n = n_list(i);
        fprintf('测试 %d×%d 矩阵...\n', n, n);
        
        % 生成随机矩阵
        A = randn(n);
        
        % 使用算法
        [U, T, ~] = my_frqr(A);
        
        % 计算误差
        orth_error(i) = norm(U'*U - eye(n), 'fro');
        backward_error(i) = norm(U'*A*U - T, 'fro') / norm(A, 'fro');
        
        % 验证Schur形结构
        schur_valid(i) = check_schur_form(T, n);
        
        
        fprintf('  正交性损失: %e\n', orth_error(i));
        fprintf('  向后误差: %e\n', backward_error(i));
        fprintf('  Schur形验证: %s\n\n', string(schur_valid(i)));
    end
    
    % 可视化结果
    figure();

    subplot(1,2,1);
    semilogy(n_list, orth_error, 'bo-', 'LineWidth', 2, 'MarkerSize', 8);
    hold on;
    xlabel('矩阵规模 n');
    ylabel('‖U^TU-I‖_F');
    title('正交性损失 vs 矩阵规模');
    grid on;

    subplot(1,2,2);
    semilogy(n_list, backward_error, 'ro-', 'LineWidth', 2, 'MarkerSize', 8);
    hold on;

    xlabel('矩阵规模 n');
    ylabel('‖U^TAU-T‖_F');
    title('向后误差 vs 矩阵规模');
    grid on;

    % 保存图像
    saveas(gcf, 'correctness_plot.png');
    
    fprintf('测试完成。\n');
end

function valid = check_schur_form(T, n)
% CHECK_SCHUR_FORM - 验证矩阵是否为拟上三角Schur形
%   对角块为1x1或2x2，且2x2块的特征值为复数

    valid = true;
    i = 1;
    
    while i <= n
        if i == n
            % 1x1块
            i = i + 1;
        elseif abs(T(i+1, i)) < eps * norm(T, 'fro')
            % 1x1块
            i = i + 1;
        else
            % 检查是否为2x2块
            if i+1 > n || (i+2 <= n && abs(T(i+2, i+1)) > eps * norm(T, 'fro'))
                valid = false;
                return;
            end
            
            % 检查2x2块的特征值是否为复数
            subblock = T(i:i+1, i:i+1);
            trace_h = subblock(1,1) + subblock(2,2);
            det_h = subblock(1,1)*subblock(2,2) - subblock(1,2)*subblock(2,1);
            disc = trace_h^2 - 4*det_h;
            
            if disc >= -eps * norm(T, 'fro')
                % 实特征值应为1x1块
                valid = false;
                return;
            end
            
            i = i + 2;
        end
    end
end
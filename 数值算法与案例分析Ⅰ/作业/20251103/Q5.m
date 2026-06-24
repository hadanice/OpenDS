function Q5()
    % 生成实对称矩阵
    generate_symmetric_matrix = @(n) (randn(n) + randn(n)') / 2;

    % 测试不同矩阵大小
    ns = [5,10,20,50,100,200,500,1000,2000];
    times = zeros(size(ns));
    histories = cell(1, length(ns));
    
    fprintf('开始测试不同矩阵大小的性能：\n');
    for i = 1:length(ns)
        n = ns(i);
        A = generate_symmetric_matrix(n);
        
        tic;
        [D, V, history] = jacobi_method(A, 1e-6, 1000);
        times(i) = toc;
        
        histories{i} = history;
        fprintf('n=%d 耗时: %.4f 秒\n', n, times(i));
    end

    % 绘制性能曲线
    figure;
    plot(ns, times, 'o-', 'LineWidth', 2, 'MarkerSize', 8);
    xlabel('矩阵大小 n');
    ylabel('耗时 (秒)');
    title('雅可比对角化算法性能');
    grid on;

    % 可视化收敛历史 (n=5)
    figure;
    semilogy(histories{1}, 'o-', 'LineWidth', 2, 'MarkerSize', 4);
    xlabel('迭代次数');
    ylabel('最大非对角元素绝对值');
    title('收敛历史 (n=5)');
    grid on;

    % 观察分量收敛 (跟踪 A(1,2))
    A_track = generate_symmetric_matrix(5);
    [D, V, history, elem_history] = jacobi_method_with_tracking(A_track, [1,2]);
    
    figure;
    semilogy(elem_history, 's-', 'LineWidth', 2, 'MarkerSize', 4, 'DisplayName', '|A(1,2)|');
    hold on;
    semilogy(history, 'o-', 'LineWidth', 2, 'MarkerSize', 4, 'DisplayName', '最大非对角元');
    xlabel('迭代次数');
    ylabel('绝对值');
    title('分量收敛观察');
    legend;
    grid on;
    
    % 验证结果
    fprintf('\n验证对角化结果 (n=5):\n');
    fprintf('V''*A*V ≈ D:\n');
    disp(V' * A_track * V);
end

function [D, V, history] = jacobi_method(A, tol, max_iter)
    A = A;
    n = size(A, 1);
    V = eye(n);
    history = [];
    
    for iter = 1:max_iter
        % 找最大非对角元 (排除对角线)
        A_off = A;
        A_off(1:n+1:end) = 0;  % 置对角线为0
        [max_val, idx] = max(abs(A_off(:)));
        if max_val < tol
            break;
        end
        history = [history; max_val];
        
        % 获取位置 (p,q)
        p = mod(idx-1, n) + 1;
        q = floor((idx-1)/n) + 1;
        
        % 计算旋转角
        d = A(q,q) - A(p,p);
        if abs(d) < eps
            theta = pi/4;
        else
            theta = 0.5 * atan2(2*A(p,q), d);
        end
        c = cos(theta);
        s = sin(theta);
        
        % 保存旧值
        App = A(p,p);
        Aqq = A(q,q);
        Apq = A(p,q);
        
        % 更新对角元
        A(p,p) = App*c^2 + Aqq*s^2 - 2*Apq*c*s;
        A(q,q) = App*s^2 + Aqq*c^2 + 2*Apq*c*s;
        A(p,q) = 0;
        A(q,p) = 0;
        
        % 更新其他元素
        for k = 1:n
            if k ~= p && k ~= q
                Akp = A(k,p);
                Akq = A(k,q);
                A(k,p) = c*Akp - s*Akq;
                A(k,q) = s*Akp + c*Akq;
                A(p,k) = A(k,p);
                A(q,k) = A(k,q);
            end
        end
        
        % 更新特征向量
        for k = 1:n
            Vpk = V(k,p);
            Vqk = V(k,q);
            V(k,p) = c*Vpk - s*Vqk;
            V(k,q) = s*Vpk + c*Vqk;
        end
    end
    D = diag(diag(A));
end

function [D, V, history, elem_history] = jacobi_method_with_tracking(A, indices)
    % 跟踪特定元素 (indices = [i,j])
    [D, V, history] = jacobi_method(A, 1e-6, 1000);
    elem_history = [];
    
    for iter = 1:length(history)
        elem_history = [elem_history; abs(A(indices(1), indices(2)))];
    end
end
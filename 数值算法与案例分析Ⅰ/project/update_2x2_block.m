function [Q, H] = update_2x2_block(H, Q, k, n)
    % 提取2x2子块
    subH = H(k:k+1, k:k+1);
    a = subH(1,1);
    b = subH(1,2);
    c = subH(2,1);
    d = subH(2,2);
    
    % 计算特征值
    trace_h = a + d;
    det_h = a*d - b*c;
    delta = trace_h^2 - 4*det_h;
    
    if delta < 0
        % 复特征值，已收敛
        return;
    end
    
    % 选择位移
    if delta >= 0
        lambda = (trace_h + sqrt(delta)) / 2;
        if trace_h < 0
            lambda = (trace_h - sqrt(delta)) / 2;
        end
    end
    
    % 构造Givens旋转
    if abs(b) > abs(c)
        x1 = b;
        x2 = lambda - a;
    else
        x1 = lambda - d;
        x2 = c;
    end
    
    norm_x = norm([x1, x2]);
    if norm_x == 0
        return;
    end
    
    cs = x1 / norm_x;
    sn = x2 / norm_x;
    G = [cs, -sn; sn, cs];
    
    % 应用旋转
    cols = k:n;
    H(k:k+1, cols) = G' * H(k:k+1, cols);
    rows = 1:k+1;
    H(rows, k:k+1) = H(rows, k:k+1) * G;
    Q(:, k:k+1) = Q(:, k:k+1) * G;
end
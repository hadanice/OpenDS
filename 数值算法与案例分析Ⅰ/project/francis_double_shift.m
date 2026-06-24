function [Q, H] = francis_double_shift(H, Q, l, r, n)
    % 从右下角2x2块计算位移
    m = r - 1;
    a = H(m, m);
    b = H(m, r);
    c = H(r, m);
    d = H(r, r);
    
    trace_h = a + d;
    det_h = a*d - b*c;
    
    % 构造初始向量
    x = zeros(3, 1);
    h11 = H(l, l);
    h12 = H(l, l+1);
    h21 = H(l+1, l);
    h22 = H(l+1, l+1);
    h32 = H(l+2, l+1);
    
    x(1) = h11*h11 + h12*h21 - trace_h*h11 + det_h;
    x(2) = h21*(h11 + h22 - trace_h);
    x(3) = h21*h32;
    
    % 第一个Householder变换
    norm_x = norm(x);
    if norm_x == 0
        return;
    end
    
    if x(1) >= 0
        norm_x = -norm_x;
    end
    
    x(1) = x(1) - norm_x;
    x = x / norm(x);
    
    % 应用第一个变换
    rows = l:min(l+2, r);
    cols = l:n;
    P = eye(3) - 2*(x*x');
    H(rows, cols) = P * H(rows, cols);
    
    cols2 = l:min(l+2, r);
    rows2 = 1:min(l+3, r);
    H(rows2, cols2) = H(rows2, cols2) * P';
    Q(:, cols2) = Q(:, cols2) * P';
    
    % 追赶凸起
    for k = l:r-3
        % 提取向量
        v = H(k+1:k+3, k);
        norm_v = norm(v);
        if norm_v == 0
            continue;
        end
        
        if v(1) >= 0
            norm_v = -norm_v;
        end
        
        v(1) = v(1) - norm_v;
        v = v / norm(v);
        
        % 应用变换
        P = eye(3) - 2*(v*v');
        rows = k+1:min(k+3, r);
        cols = k:n;
        H(rows, cols) = P * H(rows, cols);
        
        cols2 = k+1:min(k+3, r);
        rows2 = 1:min(k+4, r);
        H(rows2, cols2) = H(rows2, cols2) * P';
        Q(:, cols2) = Q(:, cols2) * P';
    end
    
    % 最后2x2处理
    if r-l >= 2
        v = H(r-1:r, r-2);
        norm_v = norm(v);
        if norm_v > 0
            if v(1) >= 0
                norm_v = -norm_v;
            end
            
            v(1) = v(1) - norm_v;
            v = v / norm(v);
            
            P = eye(2) - 2*(v*v');
            rows = r-1:r;
            cols = r-2:n;
            H(rows, cols) = P * H(rows, cols);
            
            cols2 = r-1:r;
            rows2 = 1:r;
            H(rows2, cols2) = H(rows2, cols2) * P';
            Q(:, cols2) = Q(:, cols2) * P';
        end
    end
end
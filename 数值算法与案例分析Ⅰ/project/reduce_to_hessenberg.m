function [H, Q] = reduce_to_hessenberg(A, n)
    H = A;
    Q = eye(n);
    
    for j = 1:n-2
        % 计算Householder向量
        v = H(j+1:n, j);
        beta = norm(v);
        if beta == 0
            continue;
        end
        
        % 符号选择避免相消
        if v(1) >= 0
            beta = -beta;
        end
        
        v(1) = v(1) - beta;
        v = v / norm(v);
        
        % 应用变换到H
        H(j+1:n, j:n) = H(j+1:n, j:n) - 2*v*(v'*H(j+1:n, j:n));
        H(1:n, j+1:n) = H(1:n, j+1:n) - 2*(H(1:n, j+1:n)*v)*v';
        
        % 累积正交变换
        Q(1:n, j+1:n) = Q(1:n, j+1:n) - 2*(Q(1:n, j+1:n)*v)*v';
    end
end
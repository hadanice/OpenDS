function [U, T, iters] = my_frqr(A)
% MY_FRQR - 实Schur分解的Francis QR算法实现
%   输入: A - n×n实矩阵
%   输出: U - 正交矩阵，T - 拟上三角矩阵，iters - 迭代次数

    n = size(A, 1);
    
    % 步骤1: 上Hessenberg化（精简实现）
    [T, U] = reduce_to_hessenberg(A, n);
    
    % 步骤2: Francis QR迭代
    iters = 0;
    
    while true
        % 寻找右下角的未收敛块
        [l, r, done] = locate_active_block(T, n);
        if done
            break;
        end
        
        % 根据块大小选择迭代策略
        if r - l == 1
            % 2x2块处理
            [U, T] = update_2x2_block(T, U, l, n);
        else
            % 大块隐式双位移迭代
            [U, T] = francis_double_shift(T, U, l, r, n);
        end
        
        % 清除微小次对角元素
        T = clean_subdiagonal(T, l, r);
        iters = iters + 1;
    end
end
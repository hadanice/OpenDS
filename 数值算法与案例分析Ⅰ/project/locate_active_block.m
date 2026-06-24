function [l, r, done] = locate_active_block(H, n)
    r = n;
    done = false;
    
    % 从右下角开始检查
    while r > 1
        if r == 2 || H(r-1, r-2) == 0
            % 检查2x2块
            if r == 1
                l = 1;
                return;
            end
            
            a = H(r-1, r-1);
            b = H(r-1, r);
            c = H(r, r-1);
            d = H(r, r);
            disc = (a+d)^2 - 4*(a*d - b*c);
            
            if disc < 0
                r = r - 2;  % 复特征值块，跳过
                continue;
            end
        end
        
        if H(r, r-1) == 0
            r = r - 1;  % 实特征值，跳过
            continue;
        end
        
        break;
    end
    
    if r <= 1
        done = true;
        l = 1;
        return;
    end
    
    % 寻找左边界
    l = r - 1;
    while l > 1 && H(l, l-1) ~= 0
        l = l - 1;
    end
end
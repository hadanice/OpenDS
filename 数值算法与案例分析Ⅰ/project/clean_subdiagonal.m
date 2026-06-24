function H = clean_subdiagonal(H, l, r)
    tol = eps * norm(H, 'fro');
    for i = l+1:r
        if abs(H(i, i-1)) < tol
            H(i, i-1) = 0;
        end
    end
end

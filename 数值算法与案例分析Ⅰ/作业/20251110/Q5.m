function[]=draw_polygon(x,y)
    x=x(:)';
    y=y(:)';
    xc=[x,x(1)];
    yc=[y,y(1)];
    plot(xc,yc,'-o');
    axis equal;
end

function M=generate_M(n)
    I=eye(n);
    S=circshift(I,-1);
    M=(I+S)/2;
end

function[x,y]=alg_1(x,y,n)
    sgtitle('Algorithm 1: No Normalization (Converges to Point)');
    M=generate_M(n);

    % 绘制 k=0
    subplot(2,2,1);
    draw_polygon(x,y);
    title('Initial Polygon (k=0)');

    % 迭代
    iters_to_plot = [5,20,100];
    subplot_indices = [2,3,4];
    plot_idx = 1;

    for k=1:max(iters_to_plot)
        x=M*x;
        y=M*y;
        if k==iters_to_plot(plot_idx)
            subplot(2,2,subplot_indices(plot_idx));
            draw_polygon(x, y);
            title(['k = ', num2str(k)]);
            plot_idx=plot_idx + 1;
            if plot_idx>length(iters_to_plot)
                break;
            end
        end
    end
end    

function[x,y]=alg_2(x,y,n)
    sgtitle('Algorithm 2: Unit 2-norm Normalization (Converges to Ellipse)');
    M=generate_M(n);

    % 绘制 k=0
    subplot(2, 2, 1);
    draw_polygon(x, y);
    title('Initial Polygon (k=0)');

    % 迭代
    iters_to_plot=[18,50,200]; 
    subplot_indices=[2,3,4];
    plot_idx=1;

    for k=1:max(iters_to_plot)
        x=M*x/norm(M*x);
        y=M*y/norm(M*y);
        if k==iters_to_plot(plot_idx)
            subplot(2,2,subplot_indices(plot_idx));
            draw_polygon(x,y);
            title(['k = ', num2str(k)]);
            plot_idx=plot_idx + 1;
            if plot_idx>length(iters_to_plot)
                break;
            end
        end
    end
end

function[u,v]=alg_3(n)
    tau=(0:n-1)'*(2*pi/n);

    c=sqrt(2/n)*cos(tau);
    s=sqrt(2/n)*sin(tau);

    theta_u=pi/4; 
    theta_v=pi/6;

    u=cos(theta_u)*c+sin(theta_v)*s;
    v=cos(theta_v)*c+cos(theta_u)*s;

    M=generate_M(n);

    % k=0 (P_even)
    subplot(2,2,1);
    draw_polygon(u,v);
    title('k=0 (P_even)');
    
    % k=1 (P_odd)
    u_k1=M*u/norm(M*u);
    v_k1=M*v/norm(M*v);
    subplot(2,2,2);
    draw_polygon(u_k1,v_k1);
    title('k=1(P_odd)');
    
    % k=2 (P_even)
    u_k2=M*u_k1/norm(M*u_k1);
    v_k2=M*v_k1/norm(M*v_k1);
    subplot(2,2,3);
    draw_polygon(u_k2,v_k2);
    title('k=2(P_even)');
    
    % k=3(P_odd)
    u_k3=M*u_k2/norm(M*u_k2);
    v_k3=M*v_k2/norm(M*v_k2);
    subplot(2,2,4);
    draw_polygon(u_k3,v_k3);
    title('k=3(P_odd)');
end

function[]=alg_4(x,y,n)
    sgtitle('Algorithm 4: 1-norm Normalization');
    M=generate_M(n);

    % 绘制 k=0
    subplot(2,3,1);
    draw_polygon(x,y);
    title('Initial Polygon (k=0)');

    % 迭代
    iters_to_plot=[5,20,50,100,200]; 
    subplot_indices=[2,3,4,5,6];
    plot_idx=1;

    for k = 1:max(iters_to_plot)
        x=M*x;
        x=x/norm(x,1);
        y=M*y;
        y=y/norm(y,1);
        if k==iters_to_plot(plot_idx)
            subplot(2,3,subplot_indices(plot_idx));
            draw_polygon(x,y);
            title(['k = ', num2str(k)]);
            plot_idx=plot_idx + 1;
            if plot_idx>length(iters_to_plot)
                break;
            end
        end
    end
end


% 复现论文中的实验

n=20; 

% 生成随机初始顶点（质心为0，单位2范数）
x0=randn(n, 1);
y0=randn(n, 1);
% 使质心为0
x0=x0-mean(x0);
y0=y0-mean(y0);
% 归一化为单位2范数
x0=x0/norm(x0);
y0=y0/norm(y0);

% 实验1: Algorithm 1 (不归一化)
figure;
alg_1(x0,y0,n);

% 实验2: Algorithm 2 (单位2范数归一化)
figure;
alg_2(x0,y0,n);

% 实验3: Algorithm 3 (特定初始条件)
figure;
alg_3(n);


% 实验4: Algorithm 4 (不同归一化方法)
figure;
alg_4(x0,y0,n);

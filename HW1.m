h = .005;
Z = GS(h, 10000);
[X,Y] = meshgrid(0:h:1,0:h:1);
surf(X, Y, Z)

function u = GS(h, maxiter)
    m = int32(1/h);
    u = zeros(m+1);
    for l = 1:(m+1)
        u(l,1) = cos(2*pi*single(m-l+1)*h);
    end
    u(:,m+1) = 0;
    for iter = 0:maxiter
        for j = 2:(m)
            for i = 2:(m)
                u(i,j) = 0.25 * (u(i-1,j) + u(i+1,j) + u(i,j-1) + u(i,j+1));
            end
        end
        for n = 2:m+1
            u(1,n) = u(2,n);
            u(m+1,n) = u(m,n);
        end
    end
end
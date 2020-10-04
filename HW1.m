h=.01;
[X,Y] = meshgrid(0:h:1,0:h:1);
surf(X,Y, GS(h, 10000,1))
CalcError(1)

%Calculate the analytical solution for step size h
%in both the x and y directions
function soltn = Analytical(h)
    m = int32(1/h);
    soltn = zeros(m+1);
    xcount = 0;
    for i = 0:h:1
        xcount = xcount+1;
        ycount = 0;
        for j = 0:h:1
            ycount = ycount+1;
            soltn(ycount, xcount) = cos(2*pi*j)*(cosh(2*pi*i)-(cosh(2*pi)/sinh(2*pi))*sinh(2*pi*i));
        end
    end
end


%use maxiter iterations of Gauss-Seidel with step size h
%to approximate the solution
%if fun is not equal to 1, we have our cos(2pi*y) boundary condition
%if fun = 1 we have our sign function boundary condition
function u = GS(h, maxiter, fun)
    m = int32(1/h);
    %initialize a guess that fits the boundary conditions
    %and is all zeros elsewhere
    u = zeros(m+1);
    for l = 1:(m+1)
        u(l,1) = cos(2*pi*double(m-l+1)*h);
        if fun == 1
            u(l,1) = sign(u(l,1));
        end
    end
    u(:,m+1) = 0;
    %use the Gauss-Seidel algorithm
    for iter = 0:maxiter
        for n = 2:m
            u(1,n) = 1/4*(2*u(2,n)+u(1,n-1)+u(1,n+1));
        end
        for j = 2:m
            for i = 2:m
                u(i,j) = 0.25 * (u(i-1,j) + u(i+1,j) + u(i,j-1) + u(i,j+1));
            end
        end
        for n = 2:m
            u(m+1,n) = 1/4*(2*u(m,n)+u(m+1, n-1)+u(m+1,n+1));
        end
    end
    size(u)
end


%compare the error in the infinity norm 
function error = CalcError(fun)
    hval = [1/25, 1/100, 1/200, 1/250];%, 1/400, 1/500, 1/625];
    mvec = [25, 100, 200, 250];%, 400, 500, 625];
    evec = zeros(size(hval));
    if fun == 1
        analytical = GS(1/500, 100000, 1);
        size(analytical)
        for counter = 1:4
            split = int(500/mvec(counter))
            NewAnalytical = analytical(1:split:501, 1:split:501);
            errorMtx = abs(GS(hval(counter),(mvec(counter))^2, fun)-NewAnalytical(hval(counter)));
            evec(counter) = max(max(errorMtx))
        end
    else
        for counter = 1:4
            errorMtx = abs(GS(hval(counter),(mvec(counter))^2, fun)-Analytical(hval(counter)));
            evec(counter) = max(max(errorMtx))
        end
    end
    hval = log(hval)
    evec = log(evec)
    plot(hval,evec)
end
h = .01;
Z = GS(h, 10000);
[X,Y] = meshgrid(0:h:1,0:h:1);
solution = Analytical(h);
subplot(1,3, 1)
surf(X, Y, solution)
subplot(1,3,2)
surf(X,Y,Z)
subplot(1,3,3)
error = abs(Z-solution);
surf(X,Y,error)
max(max(error))
CalcError(1000000)

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

function error = CalcError(maxiter)
    evec = zeros(1, 8);
    hvec = zeros(1, 8);
    hval = [.05, .025, .02, .01, .005, .004, .0025, .002];
    for counter = 1:8
        hvec(counter) = hval(counter);
        errorMtx = abs(GS(hval(counter),maxiter)-Analytical(hval(counter)));
        evec(counter) = max(max(errorMtx))
    end
    hvec = log(hvec)
    evec = log(evec)
    plot(hvec,evec)
end
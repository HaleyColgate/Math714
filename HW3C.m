%framework from Trefethen
%p20.m - 2nd-order wave eq. in 2D via FFT
error()


%%%CALCULATES THE ERROR USING N=128 AS THE 'TRUE SOLUTION' AND PLOTS IT
%%%USING A LOG-LOG PLOT OF THE SPACIAL DIFFERENCE AND THE ERROR
function errs = error()
    T = 1;
    N = 128;
    dt = 1/N*.1;
    fineGrid = solve(N);
    fineGrid = fineGrid(:,:,end);
    Nvals = [16, 32, 64];
    errs = zeros(size(Nvals));
    hs = zeros(size(Nvals));
    for i = 1:size(Nvals,2)
        h = 1/Nvals(i);
        hs(i) = log(h)
        nApprox = solve(Nvals(i));
        nApprox = nApprox(:,:,end);
        skip = int32(N/Nvals(i));
        compareMtx = fineGrid(1:skip:N+1, 1:skip:N+1);
        err = max(max(abs(compareMtx - nApprox)));
        errs(i) = log(err);
    end
    plot(hs, errs)
    title('Log-Log Plot of x and y Spacing and Error in Max Norm')
    xlabel('Log(x spacing)')
    ylabel('Log(Error in Max Norm)')    
end

function solution = solve(N)
    %grid and initial data:
    dt = 6/N^2;
    x = cos(pi*(0:N)/N);
    y=x';
    plotgap = round((1/3)/dt); dt = (1/3)/plotgap;
    vv = zeros(N+1,N+1);
    vvold = vv;
    f = @(x) exp(-100*(x).^2);
    vel = @(x,y) f(x).*f(y);
    v0 = vel(x,y);
    
    %the first step
    vvnew = vvold + dt*v0 + .5*dt^2*laplacian(vvold, N, x, y) + (1/6)*dt^3*laplacian(v0, N, x, y);
    vv = vvnew;
    %surf(x,y,vvnew)
    %pause(0.01)
    
    %time-stepping:
    for n=1:3*plotgap
        lap = laplacian(vv, N, x, y);
        lap2 = laplacian(lap, N, x, y);
        vvnew = 2*vv - vvold + dt^2*lap+dt^4*(1/12)*lap2;
        vvold = vv;
        vv = vvnew;
        %surf(x,y,vvnew)
        %zlim([-.05,.05])
        %pause(0.01)
    end
    solution = vvnew;
end


function lap = laplacian(vv, N, x, y)
    uxx = zeros(N+1,N+1);
    uyy = zeros(N+1,N+1);
    ii = 2:N;
    for i = 2:N %2nd derivs wrt x in each row
        v = vv(i,:);
        V = [v fliplr(v(ii))];
        U = real(fft(V));
        W1 = real(ifft(1i*[0:N-1 0 1-N:-1].*U)); %diff wrt theta
        W2 = real(ifft(-[0:N 1-N:-1].^2.*U)); %diff^2 wrt theta
        uxx(i,ii) = W2(ii)./(1-x(ii).^2)-x(ii).*W1(ii)./(1-x(ii).^2).^(3/2);
    end
    for j = 2:N %2nd derivs wrt y in each column
        v = vv(:,j);
        V = [v; flipud(v(ii))];
        U = real(fft(V));
        W1 = real(ifft(1i*[0:N-1 0 1-N:-1]'.*U)); %diff wrt theta
        W2 = real(ifft(-[0:N 1-N:-1]'.^2.*U)); %diff^2 wrt theta
        uyy(ii,j) = W2(ii)./(1-y(ii).^2)-y(ii).*W1(ii)./(1-y(ii).^2).^(3/2);
    end
    lap = uxx+uyy;
end
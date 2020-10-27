function plot = HW2C()
    T=1;
    dt=.001;
    N=100;
    visual(T, dt, N)
    error()
end

function Uvals = FullApprox(T, dt, N)
    h = 1/N;
    Tsteps = int32(T/dt);
    Uvals = zeros(N+1,N+1,Tsteps);
    r = (dt^2)/(h^2);
    %step 1 for u_t condition
    %boundaries stay zero for homogeneous dirichlet condition
    for i = 1:N-1
        for j = 1:N-1
            Uvals(i+1,j+1,2) = dt*f(i*h)*f(j*h);
        end
    end
    %now time step using 3 point time and 5 point laplacian in space
    for k = 3:Tsteps
        for i = 2:N
            for j = 2:N
                Uvals(i,j,k) = 2*Uvals(i,j,k-1)-Uvals(i,j,k-2)+r*(Uvals(i+1,j,k-1)+Uvals(i-1,j,k-1)+Uvals(i,j-1,k-1)+Uvals(i,j+1,k-1)-4*Uvals(i,j,k-1));
            end
        end
    end
end

function Uvals = FastApprox(T, dt, N)
    h = 1/N;
    Tsteps = int32(T/dt);
    Uvals = zeros(N+1,N+1,2);
    r = (dt^2)/(h^2);
    %step 1 for u_t condition
    %boundaries stay zero for homogeneous dirichlet condition
    for i = 1:N-1
        for j = 1:N-1
            Uvals(i+1,j+1,2) = dt*f(i*h)*f(j*h);
        end
    end
    %now time step using 3 point time and 5 point laplacian in space
    newUvals = zeros(N+1,N+1);
    for k = 3:Tsteps
        for i = 2:N
            for j = 2:N
                newUvals(i,j) = 2*Uvals(i,j,2)-Uvals(i,j,1)+r*(Uvals(i+1,j,2)+Uvals(i-1,j,2)+Uvals(i,j-1,2)+Uvals(i,j+1,2)-4*Uvals(i,j,2)); 
            end
        end
        Uvals(:,:,1) = Uvals(:,:,2);
        Uvals(:,:,2) = newUvals;
    end
end

function y = f(x)
    y = exp(-400*(x-0.5)^2);
end

function u = visual(T, dt, N)
    Tvals = int64(T/dt);
    h = 1/N;
    Xvals = 0:h:1;
    Yvals = 0:h:1;
    [X,Y] = meshgrid(Xvals, Yvals);
    mtx = FullApprox(T, dt, N);
    maxZ = max(max(abs(mtx(:,:))))
    for i = 1:Tvals
        surf(X,Y,mtx(:,:,i))
        zlim([-maxZ,maxZ])
        pause(0.01)
    end
end

function errs = error()
    T = 1;
    N = 500;
    dt = 1/N*.1;
    fineGrid = FastApprox(T, dt, N);
    fineGrid = fineGrid(:,:,end)
    'realDone'
    Nvals = [250, 125, 100];
    errs = zeros(size(Nvals));
    hs = zeros(size(Nvals));
    for i = 1:3
        h = 1/Nvals(i);
        hs(i) = log(h);
        nApprox = FastApprox(1,h*.1, Nvals(i));
        nApprox = nApprox(:,:,end);
        skip = int32(N/Nvals(i));
        compareMtx = fineGrid(1:skip:N+1, 1:skip:N+1);
        err = max(max(abs(compareMtx - nApprox)))
        errs(i) = log(err);
    end
    plot(hs, errs)
end

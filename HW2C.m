dt = .005;
T = 5;
N = 100;

visual(int32(T/dt), 0:1/N:1, 0:1/N:1, main(T, dt, N))

function Uvals = main(T, dt, N)
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

function y = f(x)
    y = exp(-400*(x-0.5)^2);
end

function u = visual(Tvals, Xvals, Yvals, mtx)
    [X,Y] = meshgrid(Xvals, Yvals);
    maxZ = max(max(abs(mtx(:,:))));
    for i = 1:Tvals
        surf(X,Y,mtx(:,:,i))
        zlim([-maxZ,maxZ])
        pause(0.1)
    end
end
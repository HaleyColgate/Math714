%%%RUN THE FILE
%%%IT WILL SHOW A SERIES OF 1000 GRAPHS QUICKLY WITH N=100 TO SHOW THE 
%%%SIMULATION OF THE 1ST HALF SECOND OF THE FUNCTION
%%%THEN IT WILL SHOW A LOG-LOG PLOT OF THE SPATIAL SPACING AND THE ERROR

function plot = HW2C()
    T=.5;
    dt=.001;
    N=100;
    visual(T, dt, N)
    error()
end

%%%COMPUTES THE APPROXIMATION SAVING EVERY TIME STEP
%%%EATS UP MEMORY REAL FAST
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
                Uvals(i,j,k) = 2*Uvals(i,j,k-1)-Uvals(i,j,k-2)+...
                    r*(Uvals(i+1,j,k-1)+Uvals(i-1,j,k-1)+...
                    Uvals(i,j-1,k-1)+Uvals(i,j+1,k-1)-4*Uvals(i,j,k-1));
            end
        end
    end
end

%%%SAME APPROXIMATION METHOD AS ABOVE BUT ONLY SAVES 3 STEPS AT ANY GIVEN
%%%TIME, MUCH BETTER FOR LARGE N
function Uvals = memoryFriendlyApprox(T, dt, N)
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
                newUvals(i,j) = 2*Uvals(i,j,2)-Uvals(i,j,1)+...
                    r*(Uvals(i+1,j,2)+Uvals(i-1,j,2)+Uvals(i,j-1,2)+...
                    Uvals(i,j+1,2)-4*Uvals(i,j,2)); 
            end
        end
        Uvals(:,:,1) = Uvals(:,:,2);
        Uvals(:,:,2) = newUvals;
    end
end


%%%THE FUNCTION CONTROLLING THE VELOCITY
function y = f(x)
    y = exp(-400*(x-0.5)^2);
end

%%%CREATES THE VISUALIZATION OF THE FUNCTION
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


%%%CALCULATES THE ERROR USING N=1000 AS THE 'TRUE SOLUTION' AND PLOTS IT
%%%USING A LOG-LOG PLOT OF THE SPACIAL DIFFERENCE AND THE ERROR
function errs = error()
    T = 1;
    N = 1000;
    dt = 1/N*.1;
    fineGrid = memoryFriendlyApprox(T, dt, N);
    fineGrid = fineGrid(:,:,end);
    Nvals = [500, 250, 200, 125, 100];
    errs = zeros(size(Nvals));
    hs = zeros(size(Nvals));
    for i = 1:size(Nvals,2)
        h = 1/Nvals(i);
        hs(i) = log(h);
        nApprox = memoryFriendlyApprox(1,h*.1, Nvals(i));
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

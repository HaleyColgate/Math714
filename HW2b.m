main(10^(-2))

%tests increasing N values until the error is within the specified
%tolerance, returns the first N value with error smaller than the
%tolerance
%due to the behavior around .5, even N values perform better than odd N
%values, so we focus on odd values
function minN = main(tolerance)
    nvals = 1:2:201;
    for n = 1:size(nvals, 2)
        err = MaxNorm(nvals(n));
        if err <= tolerance
            minN = nvals(n);
            break
        end
    end
end

%calculates the max norm of the error for a linear interpolant using N+1
%samples
function error = MaxNorm(N)
    %calculating the sample points
    h = 1/N;
    xvals = 0:h:1;
    yvals = zeros(size(xvals));
    for i = 1:(N+1)
        yvals(i) = f(xvals(i));
    end
    %finds the slope of the linear interpolant between points (i-1)h and
    %ih, then finds the critical points of the difference between the
    %function and the linear interpolant on each segment
    errors = zeros(1,N);
    for i = 1:(N+1)
        slope = (f(i*h)-f(((i-1)*h)))/h;
        %differenceFunction is the derivative of the difference between the
        %function and the linear interpolant
        differenceFunction = @(x) g(x, slope);
        critical = fzero(differenceFunction, h*(i-.5));
        if (critical > i*h )||(critical < (i-1)*h)
            errors(i) = 0;
        else
            errors(i) = abs(f(critical)-slope*critical+slope*i*h-f(i*h));
        end
    end
    error = max(errors);
end

%the function we're approximating
function y = f(x)
    y = exp(-400*(x-.5)^2);
end

%the derivative of the difference between the function we're approximating
%and the linear interpolant
function y = g(x, s)
    y = -800*(x-.5)*f(x)- s*x;
end
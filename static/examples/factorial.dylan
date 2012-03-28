define method factorial (n == 0) 1 end;
define method factorial (n == 1) 1 end;

define method factorial (n :: limited(<integer>, min: 2))
  n * factorial(n - 1)
end;

format-out("%d", factorial(10));
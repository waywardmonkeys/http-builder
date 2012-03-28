define function make-fibonacci()
  let n = 0;
  let m = 1;
  method ()
    let result = n + m;
    n := m;
    m := result  // return value
  end
end;

define constant fib = make-fibonacci();

for (i from 1 to 15)
  format-out("%d ", fib())
end;
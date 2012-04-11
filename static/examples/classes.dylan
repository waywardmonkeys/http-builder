define class <person> (<object>)
  constant slot person-name :: <string>, required-init-keyword: name:;
  slot person-age :: <integer> = 0, init-keyword: age:;
end;

let p1 = make(<person>, name: "Dylan");
format-out("Name: %s\nAge: %d\n", p1.person-name, p1.person-age);

let p2 = make(<person>, name: "Thomas", age: 23);
format-out("Name: %s\nAge: %d\n", p2.person-name, p2.person-age);

p2.person-age := 24;
format-out("Name: %s\nAge: %d\n", p2.person-name, p2.person-age);

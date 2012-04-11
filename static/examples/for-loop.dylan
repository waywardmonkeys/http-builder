for (i from 1,
     c in "abcdef",
     until: c = 'e')
  format-out("%d: %s\n", i, c);
end;
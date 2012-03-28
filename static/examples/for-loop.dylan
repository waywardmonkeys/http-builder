// Whichever iteration clause terminates first ends the loop.
for (i from 1,
     c in "abcdef")
  format-out("%d: %s\n", i, c);
end;
# Static Site Notes

I wrote a function for the split nodes delimiter, but this wasn't correct. I
assumed only one pair of delimiters per node, but you should check for multiple.

The course solution uses a nested loop, so for each node in old nodes, split the
line based on a delimiter. If the length of the array produced is not equal, the
markdown is not valid. Now start an inner loop using a range. If i is odd, you
know the new node should be of a given type. 

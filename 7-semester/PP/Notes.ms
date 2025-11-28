# Notes for haskell

## General stuff

## Algorithms

### Quicksort
```hs
qs [] = []
qs [x] = [x] #Not needed
qs (x:xs) = qs sm ++ [x] qs bg
	  where
	  sm = [a| a <- xs, a<= x]
          bg = [b| b <- xs. b > x]
```

 

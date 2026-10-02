# Notes for haskell

## General stuff

- Function application 
	Function application in Haskell is much like math but instead of () we use spaces.
	It has the highest priority.

Haskell is a static typed language meaning it checks types at compile time.

## Algorithms

### Quicksort
```haskell
qs [] = []
qs [x] = [x] #Not needed
qs (x:xs) = qs sm ++ [x] qs bg
	  where
	      sm = [a| a <- xs, a<= x]
          bg = [b| b <- xs. b > x]
```


## Cheat sheet

| Math        | Haskell   |
| ----------- | --------- |
| $f(x)$      | f x       |
| $f(x,y)$    | f x y     |
| $f(g(x))$   | f (g x)   |
| $f(x,g(y))$ | f x (g y) |
| $f(x)g(y)$  | f x * g y |

| Command | Meaning |
| :--- | :--- |
| `:load` *name* | load script *name* |
| `:reload` | reload current script |
| `:set editor` *name* | set editor to *name* |
| `:edit` *name* | edit script *name* |
| `:edit` | edit current script |
| `:type` *expr* | show type of *expr* |
| `:?` | show all commands |
| `:quit` | quit GHCi |


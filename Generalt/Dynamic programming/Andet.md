# Opgaver

## Fib
![[Pasted image 20240705153800.png]]

Her gentager et pattern sig et såkaldt subproblem og dette problem kan fixes ved ligesom at gæmme de values vi allerede har beregnet også kigge tilbage og se om vi har dem

![[Pasted image 20240705160327.png]]

Husk også at evaluate den anden græn når du når et basecase :) 
![[Pasted image 20240705160921.png]]
## Grid traveler
![[Pasted image 20240705182512.png]]
![[Pasted image 20240705182630.png]]

## Can sum

![[Pasted image 20240705190709.png]]
![[Pasted image 20240705191435.png]]
## howSum

## bestSum

![[Pasted image 20240707203140.png]]



# Gode tips 

Tegn din algorithme for bedre at forstå den eller hvordan den fungerere og hvis den includerer recurrsion så prøv at reducerer tegningen til et recursive tree.
eksempel, også start med et lille input 
![[Pasted image 20240705153800.png]]

Analyser nu hvordan dens big O er så du kan se hvad du kan forbedre. led efter subproblems der er duplicates som f.eks. her skal der regnes fib(5) ud 2 gange det kan forbedres ved kun at regne det ud 1 gang. 
Husk hvis der er flere parameter så skal de også tages højde for eksempel
![[Pasted image 20240705185721.png]]

# Alvins recipie 
![[Pasted image 20240705190126.png]]


# Řešení problému vážené splnitelnosti booleovské formule pokročilou iterativní metodou

## Testovací instance 

Ve složce `instCtV` byly vygenerovány pomocí stránky https://toughsat.appspot.com/
Ve složce `instNV` byly využity testovací instance ze stránky https://www.cs.ubc.ca/~hoos/SATLIB/benchm.html
Všechny testovací instance byli přejmenovány, kde se v názvu nachází počet proměných a klausulí a také poměr clausulí ku počtu proměným.
Dále byly pro všechny testovací instance dogenerovány náhodně váhy k proměným v rozsahu od 1 do 50. Tyto váhy byly přídány jako řádek komentáře `c weights 20 ...`, tak aby byl zachován formát souboru DIMACS.

## Problém

Je dána booleovská formule F proměnnných X=(x1, x2, ... , xn) v konjunktivní normální formě (tj. součin součtů). Dále jsou dány celočíselné kladné váhy W=(w1, w2, ... , wn). Najděte ohodnocení Y=(y1, y2, ... , yn) proměnných x1, x2, ... , xn tak, aby F(Y)=1 a součet vah proměnných, které jsou ohodnoceny jedničkou, byl maximální.

## Spuštění

* Je potřeba Python 3.6 a vyšší
* Nutné nainstalovat `python -m pip install -r requirements`
* Sestavit Cython pomocí `python setup.py develop`
* Vytvořit configurační soubor podle ukázky `config.yaml`
* Lze pustit aplikaci klasicky `python WCNFSolver.py [args]`
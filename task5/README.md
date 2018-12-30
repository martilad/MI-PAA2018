# Řešení problému vážené splnitelnosti booleovské formule pokročilou iterativní metodou

## Problém

Je dána booleovská formule F proměnnných X=(x1, x2, ... , xn) v konjunktivní normální formě (tj. součin součtů). Dále jsou dány celočíselné kladné váhy W=(w1, w2, ... , wn). Najděte ohodnocení Y=(y1, y2, ... , yn) proměnných x1, x2, ... , xn tak, aby F(Y)=1 a součet vah proměnných, které jsou ohodnoceny jedničkou, byl maximální.

## Spuštění

* Je potřeba Python 3.6 a vyšší
* Nutné nainstalovat `python -m pip install -r requirements`
* Sestavit Cython pomocí `python setup.py develop`
* Lze pustit aplikaci klasicky `python task4.py [args]`
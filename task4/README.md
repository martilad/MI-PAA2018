# Seznámenı́ se se zvolenou pokročilou iterativnı́ metodou na problému batohu

## Zadánı́ úlohy
* Zvolte si heuristiku, kterou budete řešit problém vážené splnitelnosti booleovské formule (si-
mulované ochlazovánı́, simulovaná evoluce, tabu prohledávánı́)
* Tuto heuristiku použijte pro řešenı́ problému batohu. Můžete použı́t dostupné instance, anebo
si vygenerujte své instance pomocı́ generátoru. Použı́vejte instance s většı́m počtem věcı́ (>30).
* Hlavnı́m cı́lem domácı́ práce je seznámit se s danou heuristikou, zejména se způsobem, jakým
se nastavujı́ jejı́ parametry (rozvrh ochlazovánı́, selekčnı́ tlak, tabu lhůta...) a modifikace
(zjištěnı́ počátečnı́ teploty, mechanismus slekce, tabu atributy...). Nenı́-li Vám cokoli jasné,
prosı́me ptejte se na cvičenı́ch.
* Problém batohu nenı́ přı́liš obtı́žný, většinou budete mı́t k dispozici globálnı́ maxima (exaktnı́
řešenı́) z předchozı́ch pracı́, napřı́klad z dynamického programovánı́. Při správném nastavenı́
parametrů byste měli vždy dosáhnout těchto optim, přı́padně pouze velice malých chyb. Doba
výpočtu může ovšem být relativně většı́. Závěrečná úloha je co do nastavenı́ a požadovaného
výkonu heuristiky podstatně náročnějšı́a může vyžadovat zcela jiné nastavenı́ parametrů.

## Spustění

* Je potřeba Python 3.6 a vyšší
* Nutné nainstalovat `python -m pip install -r requirements`
* Sestavit Cython pomocí `python setup.py develop`
* Lze pustit aplikaci klasicky `python task4.py [args]`
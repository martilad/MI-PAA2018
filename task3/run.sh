#!/bin/sh


python3 task3.py stats --outfile='S_G05M.csv' -p'inst/_G05.inst.dat' -h -bb -dc -dw  > log.log 2> elog.log 
echo '19/25' > log.log

python3 task3.py stats --outfile='S_G10M.csv' -p'inst/_G10.inst.dat' -h -bb -dc -dw  > log.log 2> elog.log 
echo '20/25' > log.log

python3 task3.py stats --outfile='S_G15M.csv' -p'inst/_G15.inst.dat' -h -bb -dc -dw  > log.log 2> elog.log 
echo '21/25' > log.log

python3 task3.py stats --outfile='S_G20M.csv' -p'inst/_G20.inst.dat' -h -bb -dc -dw  > log.log 2> elog.log 
echo '22/25' > log.log

python3 task3.py stats --outfile='S_G25M.csv' -p'inst/_G25.inst.dat' -h -bb -dc -dw  > log.log 2> elog.log 
echo '23/25' > log.log

python3 task3.py stats --outfile='S_G30M.csv' -p'inst/_G30.inst.dat' -h -bb -dc -dw  > log.log 2> elog.log 
echo '24/25' > log.log


python3 task3.py stats --outfile='S_G05V.csv' -p'inst/_G05V.inst.dat' -h -bb -dc -dw  > log.log 2> elog.log 
echo '19/25' > log.log

python3 task3.py stats --outfile='S_G10V.csv' -p'inst/_G10V.inst.dat' -h -bb -dc -dw  > log.log 2> elog.log 
echo '20/25' > log.log

python3 task3.py stats --outfile='S_G15V.csv' -p'inst/_G15V.inst.dat' -h -bb -dc -dw  > log.log 2> elog.log 
echo '21/25' > log.log

python3 task3.py stats --outfile='S_G20V.csv' -p'inst/_G20V.inst.dat' -h -bb -dc -dw  > log.log 2> elog.log 
echo '22/25' > log.log

python3 task3.py stats --outfile='S_G25V.csv' -p'inst/_G25V.inst.dat' -h -bb -dc -dw  > log.log 2> elog.log 
echo '23/25' > log.log

python3 task3.py stats --outfile='S_G30V.csv' -p'inst/_G30V.inst.dat' -h -bb -dc -dw  > log.log 2> elog.log 
echo '24/25' > log.log



#!/bin/sh

python3 task2.py stats --outfile="stats.txt" -ptestInst/ -b -h -bb -dc -dw -fptas .01,.05,.1,.2,.3,.4,.5,.6,.7,.8,.9,.95,.99 > log.log 2>elog.log &
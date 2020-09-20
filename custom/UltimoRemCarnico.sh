#!/bin/bash

#--------------------------------------------------------------------
# $01 argumento enviado por el sistema: Punto Emision
#--------------------------------------------------------------------

cd /master/intercambio/WSERVICE/$emp/REMCARNICO/
echo "PYFELIX REMITOS CARNICOS VERSION 1.00 de 01-04-2019" > ./Logs/UltimoRemCarnico.log
./UltimoRemCarnico.py $@ >> ./Logs/UltimoRemCarnico.log
chmod -v 777 ./Logs/UltimoRemCarnico.log >> ./Logs/UltimoRemCarnico.log

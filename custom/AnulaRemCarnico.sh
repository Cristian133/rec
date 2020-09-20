#!/bin/bash

#--------------------------------------------------------------------
# $01 argumento enviado por el sistema: CodRemito
# $02 argumento enviado por el sistema: TipoContingencia
#--------------------------------------------------------------------

cd /master/intercambio/WSERVICE/$emp/REMCARNICO/
echo "PYFELIX REMITOS CARNICOS VERSION 1.00 de 01-04-2019" > ./Logs/AnulaRemCarnico.log
./AnulaRemCarnico.py $@ >> ./Logs/AnulaRemCarnico.log
chmod -v 777 ./Logs/AnulaRemCarnico.log >> ./Logs/AnulaRemCarnico.log

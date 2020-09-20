#!/bin/bash

#--------------------------------------------------------------------
# $01 argumento enviado por el sistema: CodRemito
# $02 argumento enviado por el sistema: IdReq
# $03 argumento enviado por el sistema: Punto Emision
# $04 argumento enviado por el sistema: Nro Cbte
#--------------------------------------------------------------------

cd /master/intercambio/WSERVICE/$emp/REMCARNICO/
echo "PYFELIX REMITOS CARNICOS VERSION 1.00 de 01-04-2019" > ./Logs/ConsultaRemCarnico.log
./ConsultaRemCarnico.py $@ >> ./Logs/ConsultaRemCarnico.log
chmod -v 777 ./Logs/ConsultaRemCarnico.log >> ./Logs/ConsultaRemCarnico.log

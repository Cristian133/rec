#!/bin/bash

#--------------------------------------------------------------------
# $01 argumento enviado por el sistema: cuit trasporte
# $02 argumento enviado por el sistema: cuit chofer
# $03 argumento enviado por el sistema: patente chasis camion
# $04 argumento enviado por el sistema: kilometros de viaje
# $05 argumento enviado por el sistema: codigo emision
# $06 argumento enviado por el sistema: tipo cbte, unico 995
# $07 argumento enviado por el sistema: cuit emisor/titular mercad/depositario
# $08 argumento enviado por el sistema: cuit receptor
# $09 argumento enviado por el sistema: fecha inicio viaje
# $10 argumento enviado por el sistema: tipo movimiento
# $11 argumento enviado por el sistema: categoria emisor
# $12 argumento enviado por el sistema: categoria receptor
# $13 argumento enviado por el sistema: codigo dominio origen
# $14 argumento enviado por el sistema: numero comprobante
#--------------------------------------------------------------------

cd /master/intercambio/WSERVICE/$emp/REMCARNICO/
echo "PYFELIX REMITOS CARNICOS VERSION 1.00 de 01-04-2019" > ./Logs/EmiteRemCarnico.log
./EmiteRemCarnico.py $@ >> ./Logs/EmiteRemCarnico.log
chmod -v 777 ./Logs/EmiteRemCarnico.log >> ./Logs/EmiteRemCarnico.log

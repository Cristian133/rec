#!/usr/bin/env python3
#
# Copyright (C) 2019  Cristian Andrione <cristian.andrione@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version# # .
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


import os

from datetime import date

emp = os.environ['emp']
path = '/master/intercambio/WSERVICE/'+emp+'/REMCARNICO/Mercaderias.txt'

def GeneraRemitoLog(a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12, a13, a14):
    print('IdReq = ',a14)
    print('---------------------------')
    print('CUIT TRASPORTE = ',a1)
    print('CUIT CHOFER    = ',a2)
    print('PATENTE CAMION = ',a3)
    print('KILOMETROS     = ',a4)
    print('PUNTO EMISION  = ',a5)
    print('TIPO CBTE      = ',a6)
    print('CUIT EMISOR    = ',a7)
    print('CUIT RECEPTOR  = ',a8)
    print('FECHA VIAJE    = ',a9)
    print('TIPO MOVIMIENTO= ',a10)
    print('CATEG. EMISOR  = ',a11)
    print('CATEG. RECEPTOR= ',a12)
    print('COD. DOM. ORI. = ',a13)
    print('---------------------------')
    print('Comienzo de Array Mercaderia')
    z = 0
    with open(path, 'r') as arch:
        i = 1
        for line in arch:
            if i == 1:
                print('---------------------------')
                print('Orden = '+line)
            elif i == 2:
                print('CodPro = '+line)
            elif i == 3:
                print('Tropa = '+line)
            elif i == 4:
                print('Kilos = '+line)
            elif i == 5:
                print('unidades = '+line)
            elif i==6 :
                print('kilosRec = '+line)
            elif i==7 :
                print('unidadesRec = '+line)
                i = 0
            i += 1
            z += 1
        print('Fin de Array Mercaderia')
        if z%7 == 0:
            print('Array Mercaderias OK')
        else:
            print('Array Mercaderias -> Cantidad incorrecta de items')

def esCUITValida(cuit):
    cuit = str(cuit)
    cuit = cuit.replace("-", "")
    cuit = cuit.replace(" ", "")
    cuit = cuit.replace(".", "")
    if len(cuit) != 11:
        return False
    if not cuit.isdigit():
        return False
    base = [5, 4, 3, 2, 7, 6, 5, 4, 3, 2]
    aux = 0
    for i in xrange(10):
        aux += int(cuit[i]) * base[i]
    aux = 11 - (aux % 11)
    if aux == 11:
        aux = 0
    if int(cuit[10]) == aux:
        return True
    else:
        return False

def limpiaCUIT(cuit):
    cuit = str(cuit)
    cuit = cuit.replace("-", "")
    cuit = cuit.replace("/", "")
    cuit = cuit.replace(" ", "")
    cuit.replace(".", "")
    return int(cuit)

def limpiaFECHA(fecha):
    fecha = str(fecha)
    fecha = fecha.replace("-", "")
    fecha = fecha.replace("/", "")
    fecha = fecha.replace(" ", "")
    return fecha.replace(".", "")

def convierteFECHA(fecha):
    fecha = str(fecha)
    return fecha[4:]+'-'+fecha[2:4]+'-'+fecha[0:2]

def comaAPunto(arg):
    return arg.replace(",",".")

def respuesta(remito_emitido):
   remito_emitido['codRemito']
   remito_emitido['tipoComprobante']
   remito_emitido['punto_emision']
   remito_emitido['datosEmision']['nroRemito']
   remito_emitido['datosEmision']['fechaEmision']
   remito_emitido['datosEmision']['fechaVencimiento']
   remito_emitido['estado']
   remito_emitido['qr']
   remito_emitido['resultado']
   remito_emitido['evento']
   remito_emitido['arrayObservaciones']
   remito_emitido['arrayErrores']
   remito_emitido['arrayErroresFormato']

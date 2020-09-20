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


# IMPORT
import os, sys, base64, datetime

from zeep import Client
from lxml import etree as T
from datetime import datetime
from zeep.cache import SqliteCache
from zeep.transports import Transport

import mod_wsaa as wsaa
import mod_wsre as wsre
import mod_cbte as cbte
import mod_tool as tool

# ENVIROMENT
emp = os.environ['emp']
user = os.environ['USER']
CUIT = os.environ['cuitemp']
# Piso => Homologacion
CUIT = 11111111111

# SERVICE
service = 'wsremcarne'
WSDL_HOMO = 'https://fwshomo.afip.gov.ar/wsremcarne/RemCarneService?wsdl'
WSDL_PROD = 'https://serviciosjava.afip.gob.ar/wsremcarne/RemCarneService?wsdl'
WSDL = WSDL_HOMO

# CACHE WSDL
PATHDB = '/master/intercambio/WSERVICE/'+emp+'/REMCARNICO/cache.db'
cache = SqliteCache(path=PATHDB, timeout=480)
transport = Transport(cache=cache)
client = Client(wsdl=WSDL, transport=transport)

# LOG
print('user '+user)
print('emp '+emp)
print('CUIT '+str(CUIT))
print('service '+service)

# WEB SERVICE AUTORIZACION
if wsaa.wsaa(service, user) == 0:
    x = wsaa.ta(service)

# LOG
tool.GeneraRemitoLog(sys.argv[1],  sys.argv[2],  sys.argv[3],  sys.argv[4],
                     sys.argv[5],  sys.argv[6],  sys.argv[7],  sys.argv[8],
                     sys.argv[9],  sys.argv[10], sys.argv[11], sys.argv[12],
                     sys.argv[13], sys.argv[14])

# GENERO COMPROBANTE
r = cbte.RemitoCarnico(CodigoRemito = None, TipoCbte = int(sys.argv[6]),
                       TipoMovimiento = sys.argv[10], CategoriaEmisor = sys.argv[11],
                       PuntoEmision = int(sys.argv[5]),
                       CuitTitularMercaderia = int(sys.argv[7]),
                       CuitDepositario =  None,  #int(sys.argv[7]),
                       TipoReceptor = 'MI', CategoriaReceptor = int(sys.argv[12]),
                       CuitReceptor = int(sys.argv[8]),
                       CodigoDominioOrigen = int(sys.argv[13]),
                       CodigoDominioDestino = 1,
                       CuitTransportista = int(sys.argv[1]),
                       CuitConductor = int(sys.argv[2]),
                       FechaInicioViaje = tool.convierteFECHA(sys.argv[9]),
                       DistanciaKm = float(tool.comaAPunto(sys.argv[4])), DominioVehiculo = sys.argv[3],
                       DominioAcoplado = None, Estado = None, NumeroRemito = None,
                       CodigoAutorizacion = None, FechaEmision = None,
                       FechaVencimiento = None, CodigoRemitoRedestinado = None)


# PATH GENERAL
path = '/master/intercambio/WSERVICE/'+emp+'/REMCARNICO/'
path_m = path+'Mercaderias.txt'

# MERCADERIAS
r.LeeMercaderia(path_m)
print(str(r.remito))

# /Logs REQUEST
path_req = path+'/Logs/cbte_req_'+sys.argv[6]+'_'+sys.argv[5]+'_'+sys.argv[14]+'.log'
with open(path_req, 'w') as f_out:
    f_out.write(str(r.remito))

# ENVIO A AFIP
remito_raw = wsre.GenerarRemito(x, int(sys.argv[14]), r.remito)

# /Logs RESPONSE
path_res = path+'/Logs/cbte_res_'+sys.argv[6]+'_'+sys.argv[5]+'_'+sys.argv[14]+'.log'
remito_emitido = str(remito_raw)
with open(path_res, 'w') as f_res:
    f_res.write(remito_emitido)

# PROCESO RESPUESTA METODO GenerarRemito(x, IdReq, remito)
if remito_raw['resultado'] == 'A':  #APROBADO

    # Escribimos el codigo qr en un archivo PNG
    qr_path = path+'/Logs/qr_'+sys.argv[6]+'_'+sys.argv[5]+'_'+sys.argv[14]+'.png'
    qr_raw = remito_raw['qr']
    qr = base64.b64decode(qr_raw)
    f = open(qr_path, "wb")
    f.write(qr)
    f.close()
    print("Archivo qr.png OK")

    fecha_emi = '{0:%d/%m/%Y}'.format(remito_raw['datosEmision']['fechaEmision'])
    fecha_venc = '{0:%d/%m/%Y}'.format(remito_raw['datosEmision']['fechaVencimiento'])
    linea = (
            str(remito_raw['resultado'])+'\n'+
            fecha_emi+'\n'+
            fecha_venc+'\n'+
            str(remito_raw['codRemito'])+'\n'+
            str(remito_raw['datosEmision']['nroRemito'])+'\n'+
            str(remito_raw['datosEmision']['codAutorizacion'])+'\n'+
            str(remito_raw['estado'])
            #str(remito_raw['tipoComprobante'])+'\n'+
            #str(remito_raw['punto_emision'])+'\n'+
            #str(remito_raw['qr'])+'\n'+
            #str(remito_raw['evento'])+'\n'+\
            #str(remito_raw['arrayObservaciones'])+'\n'+\
            #str(remito_raw['arrayErrores'])+'\n'+\
            #str(remito_raw['arrayErroresFormato'])
            )

if remito_raw['resultado'] == 'R':  #RECHAZADO

    linea = (
            remito_raw['resultado']
            #for key_ext, value_ext in remito_raw['arrayErroresFormato']['codigoDescripcionString']:
            #    for value_int remito_raw['arrayErroresFormato']['codigoDescripcionString'][value_ext]
            #        remito_raw['arrayErroresFormato']['codigoDescripcionString'][value_ext][value_int]+'\n'+
            #remito_raw['arrayErroresFormato']['codigoDescripcionString'][0]['codigo']+'\n'+
            #remito_raw['arrayErroresFormato']['codigoDescripcionString'][0]['descripcion']+'\n'

            #str(remito_raw['evento'])+'\n'+\
            #str(remito_raw['arrayObservaciones'])+'\n'+\
            #str(remito_raw['arrayErrores'])+'\n'+\
            #str(remito_raw['arrayErroresFormato'])
            )

# ESCRIBE TXT PARA LECTURA
path_emi =  path+'EmiteRemCarnico.txt'
with open(path_emi, 'w') as f_arch:
    f_arch.write(linea)


#parametros = {'Auth': {'Token': x.token,
#                'Sign': x.sign,
#                'Cuit': CUIT
#            },
#            'FeCAEReq': cbte.cbte
#        }
#
#node = client.create_message(client.service, 'FECAESolicitar', **parametros)
#
#req = './'+diruser+'/Logs/req_'+str()+'_'+str()+'_'+str()+'.xml'
#tree = T.ElementTree(node)
#tree.write(req)
#print(node)
#r.AgregarContingencia(TipoContingencia = 2, Observacion = 'Nada para observar')

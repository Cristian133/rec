#!/usr/bin/env python3

import os
import sys

from zeep import Client
from lxml import etree
from datetime import datetime
from zeep.cache import SqliteCache
from zeep.transports import Transport

import mod_wsaa as wsaa
import mod_wsre as wsre
import mod_cbte as cbte

user = os.environ['USER']
# Produccion
CUIT = os.environ['cuitemp']
# Homologacion
CUIT = 11111111111
emp = os.environ['emp']
service = 'wsremcarne'

WSDL_PROD = 'https://serviciosjava.afip.gob.ar/wsremcarne/RemCarneService?wsdl'
WSDL_HOMO = 'https://fwshomo.afip.gov.ar/wsremcarne/RemCarneService?wsdl'
WSDL = WSDL_HOMO

PATHDB = '/home/cristian/fuentes/wservices/python/wsfe/cache.db'
#PATHDB = '/master/intercambio/WSERVICE/'+emp+'/REMCARNE/cache.db'

cache = SqliteCache(path=PATHDB, timeout=480)
transport = Transport(cache=cache)

if wsaa.wsaa(service, user) == 0:
    x = wsaa.ta(service)

client = Client(wsdl=WSDL, transport=transport)

#consultarUltimoRemitoEmitido(authRequest: ns0:AuthRequestType,
#                             tipoComprobante: xsd:short,
#                             puntoEmision: ns0:PuntoEmisionSimpleType) ->
#   consultarUltimoRemitoReturn: ns0:ConsultarRemitoReturnType

# Tipo "int": 1 <= PuntoEmision <= 99999

PuntoEmision = int(sys.argv[1])
ure = str(wsre.ConsultarUltimoRemitoEmitido(x, PuntoEmision))

filename='./'+user+'/ultiRC_'+sys.argv[1]+'.txt'

print('path: '+filename)
with open(filename, 'w') as f_out:
    f_out.write(ure)


parametros = {'authRequest': {'token': x.token,
                              'sign': x.sign,
                              'cuitRepresentada': CUIT
                              },
              'tipoComprobante': '995',
              'puntoEmision': PuntoEmision
              }

node = client.create_message(client.service,
                             'consultarUltimoRemitoEmitido',
                             **parametros)

raw = './'+user+'/ultiRC_'+sys.argv[1]+'.xml'
tree = etree.ElementTree(node)
tree.write(raw)
print(node)

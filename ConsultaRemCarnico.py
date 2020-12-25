#!/usr/bin/env python3

# Standard library imports
import os
import sys

from datetime import datetime

# Related third party imports
from zeep import Client
from lxml import etree
from zeep.cache import SqliteCache
from zeep.transports import Transport

# Local library specific imports
import mod_wsaa as wsaa
import mod_wsre as wsre
import mod_cbte as cbte

# Environ variables
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

PATHDB = '/master/intercambio/WSERVICE/'+emp+'/REMCARNE/cache.db'

cache = SqliteCache(path=PATHDB, timeout=480)
transport = Transport(cache=cache)

if wsaa.wsaa(service, user) == 0:
    x = wsaa.ta(service)

client = Client(wsdl=WSDL, transport=transport)

# consultarRemito(authRequest: ns0:AuthRequestType,
#                 codRemito: xsd:long,
#                 idReq: ns0:IdReqSimpleType,
#                 cuitEmisor: ns0:CuitSimpleType,
#                 tipoComprobante: xsd:short,
#                 puntoEmision: ns0:PuntoEmisionSimpleType,
#                 nroComprobante: ns0:NumeroRemitoSimpleType) ->
#   consultarRemitoReturn: ns0:ConsultarRemitoReturnType

# Tipo "long": 1 <= idReq <= 999999999999999
# Tipo "int" : 1 <= PuntoEmision <= 99999
# Tipo "long": 1 <= NroCbte <= 99999999

CodigoRemito = int(sys.argv[1])
IdReq  = int(sys.argv[2])
PuntoEmision = int(sys.argv[3])
NroCbte = int(sys.argv[4])

cr = str(wsre.ConsultarRemito(x, CodigoRemito, IdReq, PuntoEmision, NroCbte))

filename='./'+user+'/cr_'+sys.argv[1]+'_'+sys.argv[2]+'_'+sys.argv[3]+'_'+sys.argv[4]+'.txt'
print('path: '+filename)
with open(filename, 'w') as f_out:
    f_out.write(cr)

parametros = {'authRequest': {'token': x.token,
                              'sign': x.sign,
                              'cuitRepresentada': CUIT
                              },
              'codRemito': CodigoRemito,
              'idReq': IdReq,
              'cuitEmisor': CUIT,
              'tipoComprobante': '995',
              'puntoEmision': PuntoEmision,
              'nroComprobante': NroCbte
              }

node = client.create_message(client.service, 'consultarRemito', **parametros)

raw = './'+user+'/cr_'+str()+'_'+str()+'_'+str()+'.xml'
tree = etree.ElementTree(node)
tree.write(raw)
print(node)

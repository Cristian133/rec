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

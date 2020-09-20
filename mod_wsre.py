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
#
#
# Modulo para generar Remito Electrónico Cárnico AFIP v3.0
# Remito de Carnes y subproductos derivados de la faena de bovinos y porcinos
# Resolución General 4256/18 y Resolución General 4303/18.


import os, base64
from zeep import Client
from zeep.cache import SqliteCache
from zeep.transports import Transport

# Produccion
CUIT = os.environ['cuitemp']
# Homologacion
CUIT = 11111111111

WSDL_HOMO = 'https://fwshomo.afip.gov.ar/wsremcarne/RemCarneService?wsdl'
WSDL_PROD = 'https://serviciosjava.afip.gob.ar/wsremcarne/RemCarneService?wsdl'
WSDL = WSDL_HOMO
clienteRemCarne = Client(wsdl=WSDL)


def dummy():
    print(clienteRemCarne.service.dummy())

def TiposCarne(x, codigoGrupoCarne):
    print(clienteRemCarne.service.consultarTiposCarne(
            authRequest = {'token': x.token,
                           'sign': x.sign,
                           'cuitRepresentada': CUIT },
            codGrupoCarne = codigoGrupoCarne
          )
    )

def GruposCarne(x):
    print(clienteRemCarne.service.consultarGruposCarne(
            authRequest = {'token': x.token,
                           'sign': x.sign,
                           'cuitRepresentada': CUIT },
          )
    )

def CategoriasReceptor(x):
    print(clienteRemCarne.service.consultarTiposCategoriaReceptor(
            authRequest = {'token': x.token,
                           'sign': x.sign,
                           'cuitRepresentada': CUIT }
          )
    )

def CategoriasEmisor(x):
    print(clienteRemCarne.service.consultarTiposCategoriaEmisor(
            authRequest = {'token': x.token,
                           'sign': x.sign,
                           'cuitRepresentada': CUIT }
          )
    )

def TiposContingencia(x):
    print(clienteRemCarne.service.consultarTiposContingencia(
            authRequest = {'token': x.token,
                           'sign': x.sign,
                           'cuitRepresentada': CUIT }
          )
    )

def TiposEstado(x):
    print(clienteRemCarne.service.consultarTiposEstado(
            authRequest = {'token': x.token,
                           'sign': x.sign,
                           'cuitRepresentada': CUIT }
          )
    )

def TiposCbte(x):
    print(clienteRemCarne.service.consultarTiposComprobante(
            authRequest = {'token': x.token,
                           'sign': x.sign,
                           'cuitRepresentada': CUIT }
          )
    )

def PuntosEmision(x):
    print(clienteRemCarne.service.consultarPuntosEmision(
            authRequest = {'token': x.token,
                           'sign': x.sign,
                           'cuitRepresentada': CUIT }
          )
    )

def TiposEstado(x):
    print(clienteRemCarne.service.consultarTiposEstado(
            authRequest = {'token': x.token,
                           'sign': x.sign,
                           'cuitRepresentada': CUIT }
          )
    )

def CodigosDomicilio(x, cuitTitular):
    print(clienteRemCarne.service.consultarCodigosDomicilio(
            authRequest = {'token': x.token,
                           'sign': x.sign,
                           'cuitRepresentada': CUIT },
            cuitTitularDomicilio = cuitTitular
          )
    )

def ConsultarRemito(x, CodigoRemito, IdReq, PuntoEmision, NroCbte):
    return clienteRemCarne.service.consultarRemito(
            authRequest = {'token': x.token,
                           'sign': x.sign,
                           'cuitRepresentada': CUIT },
            codRemito = CodigoRemito,
            idReq = IdReq,
            cuitEmisor = CUIT,
            tipoComprobante = '995',
            puntoEmision = PuntoEmision,
            nroComprobante = NroCbte
          )

def ConsultarUltimoRemitoEmitido(x, PuntoEmision):
    return clienteRemCarne.service.consultarUltimoRemitoEmitido(
            authRequest = {'token': x.token,
                           'sign': x.sign,
                           'cuitRepresentada': CUIT },
            tipoComprobante = '995',
            puntoEmision = PuntoEmision
          )

# METODOS DE MODIFICACION

def ModificarViaje(x, CodigoRemito, CuitTransportista, CuitConductor,
                   DominioVehiculo, DominioAcoplado):
    return clienteRemCarne.service.modificarViaje(
            authRequest = {'token': x.token,
                           'sign': x.sign,
                           'cuitRepresentada': CUIT },
            codRemito = CodigoRemito,
            cuitTransportista = CuitTranspostista,
            cuitConductor = CuitConductor,
            vehiculo = {'dominioVehiculo': DominioVehiculo,
                        'dominioAcoplado': DominioAcoplado }
          )

def InformarContingencia(x, CodigoRemito, TipoContingencia, Observacion):
    return clienteRemCarne.service.informarContingencia(
            authRequest = {'token': x.token,
                           'sign': x.sign,
                           'cuitRepresentada': CUIT },
            codRemito = CodigoRemito,
            contingencia = {'tipoContingencia': TipoContingencia,
                            'observacion': Observacion }
          )

def RegistrarRecepcionMercaderia(x, CodigoRemito, Estado ):
    return clienteRemCarne.service.registrarRecepcion(
            authRequest = {'token': x.token,
                           'sign': x.sign,
                           'cuitRepresentada': CUIT },
            codRemito = CodigoRemito,
            estado = Estado,
            arrayRecepcionMercaderia = []
          )

def EmitirRemito(x, CodigoRemito, CuitTransportista, CuitConductor,
                 FechaInicioViaje, DistanciaKm, DominioVehiculo,
                 DominioAcoplado):
    return clienteRemCarne.service.emitirRemito(
            authRequest = {'token': x.token,
                           'sign': x.sign,
                           'cuitRepresentada': CUIT },
            codRemito = CodigoRemito,
            viaje = {'cuitTransportista': CuitTransportista,
                     'cuitConductor': CuitConductor,
                     'fechaInicioViaje': FechaInicioViaje,
                     'distanciaKm': DistanciaKm },
            vehiculo = {'dominioVehiculo': DominioVehiculo,
                        'dominioAcoplado': DominioAcoplado }
          )

def AnularRemitoNoEmitido(x, CodigoRemito):
    return clienteRemCarne.service.anularRemito(
            authRequest = {'token': x.token,
                           'sign': x.sign,
                           'cuitRepresentada': CUIT },
            codRemito = CodigoRemito
          )

def AutorizarRemito(x, CodigoRemito, Estado):
    return clienteRemCarne.service.autorizarRemito(
            authRequest = {'token': x.token,
                           'sign': x.sign,
                           'cuitRepresentada': CUIT },
            codRemito = CodigoRemito,
            estado = Estado
          )

def GenerarRemito(x, IdReq, Remito):
    return clienteRemCarne.service.generarRemito(
            authRequest = {'token': x.token,
                           'sign': x.sign,
                           'cuitRepresentada': CUIT },
            idReq = IdReq,
            remito = Remito
          )

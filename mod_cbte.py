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


import mod_tool as tool

class RemitoCarnico:

    remito = None
    def __init__(self,
                 CodigoRemito, TipoCbte, TipoMovimiento, CategoriaEmisor, PuntoEmision,
                 CuitTitularMercaderia, CuitDepositario, TipoReceptor, CategoriaReceptor,
                 CuitReceptor, CodigoDominioOrigen, CodigoDominioDestino,
                 CuitTransportista, CuitConductor, FechaInicioViaje,
                 DistanciaKm, DominioVehiculo, DominioAcoplado, Estado,
                 #NumeroRemito, CodigoAutorizacion, FechaEmision,
                 #FechaVencimiento, CodigoRemitoRedestinado,
                 **kwargs):

        remito =  {'codRemito': CodigoRemito,
                   'tipoComprobante': TipoCbte,
                   'tipoMovimiento': TipoMovimiento,
                   'categoriaEmisor': CategoriaEmisor,
                   'puntoEmision': PuntoEmision,
                   'cuitTitularMercaderia': CuitTitularMercaderia,
                   'cuitDepositario': CuitDepositario,
                   'tipoReceptor': TipoReceptor,
                   'categoriaReceptor': CategoriaReceptor,
                   'cuitReceptor': CuitReceptor,
                   'codDomOrigen': CodigoDominioOrigen,
                   'codDomDestino': CodigoDominioDestino,
                   'viaje': {'cuitTransportista': CuitTransportista,
                             'cuitConductor': CuitConductor,
                             'fechaInicioViaje': FechaInicioViaje,
                             'distanciaKm': DistanciaKm,
                             'vehiculo': {
                                 'dominioVehiculo': DominioVehiculo,
                                 'dominioAcoplado': DominioAcoplado,
                                 }
                             },
                   'arrayMercaderias': {'mercaderia':[]},
                   #'estado': Estado,
                   #'datosEmision': {'nroRemito': NumeroRemito,
                   #                 'codAutorizacion': CodigoAutorizacion,
                   #                 'fechaEmision': FechaEmision,
                   #                 'fechaVencimiento': FechaVencimiento
                   #                 },
                   #'codRemRedestinado': CodigoRemitoRedestinado,
                   'arrayContingencias':None
                   }

        self.remito = remito

    def AgregarMercaderia(self,
                          Orden, CodigoTipoProducto, Tropa,
                          Cantidad, Unidades,
                          CantidadRecibida, UnidadesRecibidas):
        '''
        Agrego mercaderia a un remito
        ns0:MercaderiaType(orden: ns0:OrdenSimpleType,
                           codTipoProd: xsd:string,
                           tropa: ns0:TropaSimpleType,
                           kilos: ns0:CantidadSimpleType,
                           unidades: ns0:CantidadSimpleType,
                           kilosRec: ns0:CantidadSimpleType,
                           unidadesRec: ns0:CantidadSimpleType)

        <xsd:simpleType name="CantidadSimpleType">
            <xsd:restriction base="xsd:decimal">
            <xsd:minInclusive value="0"/>
            <xsd:maxInclusive value="999999.99"/>
        '''
        mercaderia = {'orden': int(Orden),
                      'codTipoProd': CodigoTipoProducto,
                      'tropa': int(Tropa),
                      'kilos': float(tool.comaAPunto(Cantidad)),
                      'unidades': float(tool.comaAPunto(Unidades)),
                      'kilosRec': float(tool.comaAPunto(CantidadRecibida)),
                      'unidadesRec': float(tool.comaAPunto(UnidadesRecibidas)),
                      }
        self.remito['arrayMercaderias']['mercaderia'].append(mercaderia)
        print('Agrego item array Mercaderia')
        return True


    def AgregarContingencia(self, TipoContingencia, Observacion):
        '''Agrego contingencia a un remito'''
        if self.remito['arrayContingencias'] == None:
            self.remito['arrayContingencias'] = {'contingencias': []}
        contingencia = {'tipoContingencia': TipoContingencia,
                        'observacion': Observacion,
                        }
        self.remito['arrayContingencias']['contingencia'].append(contingencia)
        return True


    def LeeMercaderia(self, arch):
        n = 0
        lista_args = []
        with open(arch) as arch_ent:
            for line in arch_ent:
                if n < 7:
                    lista_args.append(line.strip('\n'))
                    n = n + 1
                elif n == 7:
                    if self.AgregarMercaderia(*lista_args):
                        n = 0
                        lista_args.clear()
                        lista_args.append(line.strip('\n'))
                        n = n + 1
                else:
                    pass
        if self.AgregarMercaderia(*lista_args):
            lista_args.clear()
            lista_args.append(line.strip('\n'))

        return True

    def AnalizaErrores(self, ret):
        '''
        Comprueba y extrae errores si existen en la respuesta
        '''
        self.Errores = [err['codigoDescripcion'] for err in ret.get('arrayErrores', [])]
        self.ErroresFormato = [err['codigoDescripcionString'] for err in ret.get('arrayErroresFormato', [])]
        errores = self.Errores + self.ErroresFormato
        self.ErrCode = ' '.join(["%(codigo)s" % err for err in errores])
        self.ErrMsg = '\n'.join(["%(codigo)s: %(descripcion)s" % err for err in errores])

    def AnalizaObservaciones(self, ret):
        '''
        Comprueba y extrae observaciones si existen en la respuesta
        '''
        self.Observaciones = [obs["codigoDescripcion"] for obs in ret.get('arrayObservaciones', [])]
        self.Obs = '\n'.join(["%(codigo)s: %(descripcion)s" % obs for obs in self.Observaciones])

    def AnalizaEvento(self, ret):
        '''
        Comprueba y extrae evento informativo si existen en la respuesta
        '''
        evt = ret.get('evento')
        if evt:
            self.Eventos = [evt]
            self.Evento = "%(codigo)s: %(descripcion)s" % evt

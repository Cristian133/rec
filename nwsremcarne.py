#!/usr/bin/env python3

import os, sys, time, base64
from utils import date
import traceback
from pysimplesoap.client import SoapFault
import utils

# importo funciones compartidas:
from utils import json, BaseWS, inicializar_y_capturar_excepciones, get_install_dir


# constantes de configuración (producción/homologación):
WSDL = ["https://serviciosjava.afip.gob.ar/wsremcarne/RemCarneService?wsdl",
        "https://fwshomo.afip.gov.ar/wsremcarne/RemCarneService?wsdl"]

DEBUG = False
XML = False
CONFIG_FILE = "wsremcarne.ini"
HOMO = False
ENCABEZADO = []


class WSRemCarne(BaseWS):
    "Interfaz para el WebService de Remito Electronico Carnico (Version 3)"
    _public_methods_ = ['Conectar', 'Dummy', 'SetTicketAcceso', 'DebugLog',
                        'GenerarRemito', 'EmitirRemito', 'AutorizarRemito', 'AnularRemito', 'ConsultarRemito',
                        'InformarContingencia', 'ModificarViaje', 'RegistrarRecepcion',  'ConsultarUltimoRemitoEmitido',
                        'CrearRemito', 'AgregarViaje', 'AgregarVehiculo', 'AgregarMercaderia',
                        'AgregarDatosAutorizacion', 'AgregarContingencia',
                        'ConsultarTiposCarne', 'ConsultarTiposCategoriaEmisor', 'ConsultarTiposCategoriaReceptor',
                        'ConsultarTiposComprobante', 'ConsultarTiposContingencia', 'ConsultarTiposEstado',
                        'ConsultarCodigosDomicilio', 'ConsultarGruposCarne, ConsultarPuntosEmision',
                        'SetParametros', 'SetParametro', 'GetParametro', 'AnalizarXml', 'ObtenerTagXml', 'LoadTestXML',
                        ]
    _public_attrs_ = ['XmlRequest', 'XmlResponse', 'Version', 'Traceback', 'Excepcion', 'LanzarExcepciones',
                      'Token', 'Sign', 'Cuit', 'AppServerStatus', 'DbServerStatus', 'AuthServerStatus',
                      'CodRemito', 'TipoComprobante', 'PuntoEmision',
                      'NroRemito', 'CodAutorizacion', 'FechaVencimiento', 'FechaEmision', 'Estado', 'Resultado', 'QR',
                      'ErrCode', 'ErrMsg', 'Errores', 'ErroresFormato', 'Observaciones', 'Obs', 'Evento', 'Eventos',
                     ]
    _reg_progid_ = "WSRemCarne"
    _reg_clsid_ = "{71DB0CB9-2ED7-4226-A1E6-C3FA7FB18F41}"

    # Variables globales para BaseWS:
    HOMO = HOMO
    WSDL = WSDL[HOMO]
    LanzarExcepciones = False
    Version = "%s %s" % (__version__, HOMO and 'Homologación' or '')

    def Conectar(self, *args, **kwargs):
        ret = BaseWS.Conectar(self, *args, **kwargs)
        return ret

    def inicializar(self):
        self.AppServerStatus = self.DbServerStatus = self.AuthServerStatus = None
        self.CodRemito = self.TipoComprobante = self.PuntoEmision = None
        self.NroRemito = self.CodAutorizacion = self.FechaVencimiento = self.FechaEmision = None
        self.Estado = self.Resultado = self.QR = None
        self.Errores = []
        self.ErroresFormato = []
        self.Observaciones = []
        self.Eventos = []
        self.Evento = self.ErrCode = self.ErrMsg = self.Obs = ""

    def __analizar_errores(self, ret):
        "Comprueba y extrae errores si existen en la respuesta"
        self.Errores = [err['codigoDescripcion'] for err in ret.get('arrayErrores', [])]
        self.ErroresFormato = [err['codigoDescripcionString'] for err in ret.get('arrayErroresFormato', [])]
        errores = self.Errores + self.ErroresFormato
        self.ErrCode = ' '.join(["%(codigo)s" % err for err in errores])
        self.ErrMsg = '\n'.join(["%(codigo)s: %(descripcion)s" % err for err in errores])

    def __analizar_observaciones(self, ret):
        "Comprueba y extrae observaciones si existen en la respuesta"
        self.Observaciones = [obs["codigoDescripcion"] for obs in ret.get('arrayObservaciones', [])]
        self.Obs = '\n'.join(["%(codigo)s: %(descripcion)s" % obs for obs in self.Observaciones])

    def __analizar_evento(self, ret):
        "Comprueba y extrae el wvento informativo si existen en la respuesta"
        evt = ret.get('evento')
        if evt:
            self.Eventos = [evt]
            self.Evento = "%(codigo)s: %(descripcion)s" % evt


    def CrearRemito(self, tipo_comprobante, punto_emision, tipo_movimiento, categoria_emisor, cuit_titular_mercaderia, cod_dom_origen,
                    tipo_receptor, categoria_receptor=None, cuit_receptor=None, cuit_depositario=None,
                    cod_dom_destino=None, cod_rem_redestinar=None, cod_remito=None, estado=None,
                    **kwargs):
        "Inicializa internamente los datos de un remito para autorizar"
        self.remito = {'tipoComprobante': tipo_comprobante, 'puntoEmision': punto_emision, 'categoriaEmisor': categoria_emisor,
                       'cuitTitularMercaderia': cuit_titular_mercaderia, 'cuitDepositario': cuit_depositario,
                       'tipoReceptor': tipo_receptor, 'categoriaReceptor': categoria_receptor, 'cuitReceptor': cuit_receptor,
                       'codDomOrigen': cod_dom_origen, 'codDomDestino': cod_dom_destino, 'tipoMovimiento': tipo_movimiento,
                       'estado': estado, 'codRemito': cod_remito,
                       'codRemRedestinado': cod_rem_redestinar,
                       'arrayMercaderias': [], 'arrayContingencias': [],
                      }
        return True


    def AgregarViaje(self, cuit_transportista=None, cuit_conductor=None, fecha_inicio_viaje=None, distancia_km=None, **kwargs):
        "Agrega la información referente al viaje del remito electrónico cárnico"
        self.remito['viaje'] = {'cuitTransportista': cuit_transportista,
                                'cuitConductor': cuit_conductor,
                                'fechaInicioViaje': fecha_inicio_viaje ,
                                'distanciaKm': distancia_km,
                                'vehiculo': {}
                               }
        return True


    def AgregarVehiculo(self, dominio_vehiculo=None, dominio_acoplado=None, **kwargs):
        "Agrega la información referente al vehiculo usado en el viaje del remito electrónico cárnico"
        self.remito['viaje']['vehiculo'] = {'dominioVehiculo': dominio_vehiculo, 'dominioAcoplado': dominio_acoplado}
        return True


    def AgregarMercaderia(self, orden=None, cod_tipo_prod=None, kilos=None, unidades=None, tropa=None, kilos_rec=None, unidades_rec=None, **kwargs):
        "Agrega la información referente a la mercadería del remito electrónico cárnico"
        mercaderia = dict(orden=orden, tropa=tropa, codTipoProd=cod_tipo_prod, kilos=kilos, unidades=unidades,
                          kilosRec=kilos_rec, unidadesRec=unidades_rec)
        self.remito['arrayMercaderias'].append(dict(mercaderia=mercaderia))
        return True


    def AgregarDatosAutorizacion(self, nro_remito=None, cod_autorizacion=None, fecha_emision=None, fecha_vencimiento=None, **kwargs):
        "Agrega la información referente a los datos de autorización del remito electrónico cárnico"
        self.remito['datosEmision'] = dict(nroRemito=nro_remito, codAutorizacion=cod_autorizacion,
                                                fechaEmision=fecha_emision, fechaVencimiento=fecha_vencimiento,
                                               )
        return True


    def AgregarContingencias(self, tipo=None, observacion=None, **kwargs):
        "Agrega la información referente a los opcionales de la liq. seq."
        contingencia = dict(tipoContingencia=tipo, observacion=observacion)
        self.remito['arrayContingencias'].append(dict(contingencia=contingencia))
        return True


    def GenerarRemito(self, id_req, archivo="qr.png"):
        "Informar los datos necesarios para la generación de un remito nuevo"
        if not self.remito['arrayContingencias']:
            del self.remito['arrayContingencias']
        response = self.client.generarRemito(
                                authRequest={'token': self.Token, 'sign': self.Sign, 'cuitRepresentada': self.Cuit},
                                idReq=id_req, remito=self.remito)
        ret = response.get("generarRemitoReturn")
        if ret:
            self.__analizar_errores(ret)
            self.__analizar_observaciones(ret)
            self.__analizar_evento(ret)
            self.AnalizarRemito(ret, archivo)
        return bool(self.CodRemito)

    def AnalizarRemito(self, ret, archivo=None):
        "Extrae el resultado del remito, si existen en la respuesta"
        if ret:
            self.CodRemito = ret.get("codRemito")
            self.TipoComprobante = ret.get("tipoComprobante")
            self.PuntoEmision = ret.get("puntoEmision")
            datos_aut = ret.get('datosAutorizacion')
            if datos_aut:
                self.NroRemito = datos_aut.get('nroRemito')
                self.CodAutorizacion = datos_aut.get('codAutorizacion')
                self.FechaEmision = datos_aut.get('fechaEmision')
                self.FechaVencimiento = datos_aut.get('fechaVencimiento')
            self.Estado = ret.get('estado')
            self.Resultado = ret.get('resultado')
            self.QR = ret.get('qr') or ""
            if archivo:
                qr = base64.b64decode(self.QR)
                f = open(archivo, "wb")
                f.write(qr)
                f.close()


    def EmitirRemito(self, archivo="qr.png"):
        "Emitir Remitos que se encuentren en estado Pendiente de Emitir."
        response = self.client.emitirRemito(
                                authRequest={'token': self.Token, 'sign': self.Sign, 'cuitRepresentada': self.Cuit},
                                codRemito=self.remito['codRemito'],
                                viaje=self.remito.get('viaje'))
        ret = response.get("emitirRemitoReturn")
        if ret:
            self.__analizar_errores(ret)
            self.__analizar_observaciones(ret)
            self.__analizar_evento(ret)
            self.AnalizarRemito(ret, archivo)
        return bool(self.CodRemito)


    def AutorizarRemito(self, archivo="qr.png"):
        "Autorizar o denegar un remito (cuando corresponde autorizacion) por parte del titular/depositario"
        response = self.client.autorizarRemito(
                                authRequest={'token': self.Token, 'sign': self.Sign, 'cuitRepresentada': self.Cuit},
                                codRemito=self.remito['codRemito'],
                                estado=self.remito['estado'])
        ret = response.get("autorizarRemitoReturn")
        if ret:
            self.__analizar_errores(ret)
            self.__analizar_observaciones(ret)
            self.__analizar_evento(ret)
            self.AnalizarRemito(ret, archivo)
        return bool(self.CodRemito)


    def AnularRemito(self):
        "Anular un remito generado que aún no haya sido emitido"
        response = self.client.anularRemito(
                                authRequest={'token': self.Token, 'sign': self.Sign, 'cuitRepresentada': self.Cuit},
                                codRemito=self.remito['codRemito'])
        ret = response.get("anularRemitoReturn")
        if ret:
            self.__analizar_errores(ret)
            self.__analizar_observaciones(ret)
            self.__analizar_evento(ret)
            self.AnalizarRemito(ret)
        return bool(self.CodRemito)


    def ConsultarUltimoRemitoEmitido(self, tipo_comprobante=995, punto_emision=1):
        "Obtener el último número de remito que se emitió por tipo de comprobante y punto de emisión"
        response = self.client.consultarUltimoRemitoEmitido(
                                authRequest={'token': self.Token, 'sign': self.Sign, 'cuitRepresentada': self.Cuit},
                                tipoComprobante=tipo_comprobante,
                                puntoEmision=punto_emision)
        ret = response.get("consultarUltimoRemitoReturn", {})
        id_req = ret.get("idReq", 0)
        rec = ret.get("remito", {})
        self.__analizar_errores(ret)
        self.__analizar_observaciones(ret)
        self.__analizar_evento(ret)
        self.AnalizarRemito(rec)
        return id_req


    def ConsultarRemito(self, cod_remito=None, id_req=None,
                        tipo_comprobante=None, punto_emision=None, nro_comprobante=None):
        "Obtener los datos de un remito generado"
        print(self.client.help("consultarRemito"))
        response = self.client.consultarRemito(
                                authRequest={'token': self.Token, 'sign': self.Sign, 'cuitRepresentada': self.Cuit},
                                codRemito=cod_remito,
                                idReq=id_req,
                                tipoComprobante=tipo_comprobante,
                                puntoEmision=punto_emision,
                                nroComprobante=nro_comprobante)
        ret = response.get("consultarRemitoReturn", {})
        id_req = ret.get("idReq", 0)
        self.remito = rec = ret.get("remito", {})
        self.__analizar_errores(ret)
        self.__analizar_observaciones(ret)
        self.__analizar_evento(ret)
        self.AnalizarRemito(rec)
        return id_req


    def Dummy(self):
        "Obtener el estado de los servidores de la AFIP"
        results = self.client.dummy()['dummyReturn']
        self.AppServerStatus = str(results['appserver'])
        self.DbServerStatus = str(results['dbserver'])
        self.AuthServerStatus = str(results['authserver'])


    def ConsultarTiposComprobante(self, sep="||"):
        "Obtener el código y descripción para tipo de comprobante"
        ret = self.client.consultarTiposComprobante(
                            authRequest={
                                'token': self.Token, 'sign': self.Sign,
                                'cuitRepresentada': self.Cuit, },
                                )['consultarTiposComprobanteReturn']
        self.__analizar_errores(ret)
        array = ret.get('arrayTiposComprobante', [])
        lista = [it['codigoDescripcion'] for it in array]
        return [(u"%s {codigo} %s {descripcion} %s" % (sep, sep, sep)).format(**it) if sep else it for it in lista]


    def ConsultarTiposContingencia(self, sep="||"):
        "Obtener el código y descripción para cada tipo de contingencia que puede reportar"
        ret = self.client.consultarTiposContingencia(
                            authRequest={
                                'token': self.Token, 'sign': self.Sign,
                                'cuitRepresentada': self.Cuit, },
                                )['consultarTiposContingenciaReturn']
        self.__analizar_errores(ret)
        array = ret.get('arrayTiposContingencia', [])
        lista = [it['codigoDescripcion'] for it in array]
        return [(u"%s {codigo} %s {descripcion} %s" % (sep, sep, sep)).format(**it) if sep else it for it in lista]


    def ConsultarTiposCategoriaEmisor(self, sep="||"):
        "Obtener el código y descripción para tipos de categorías de emisor"
        ret = self.client.consultarTiposCategoriaEmisor(
                            authRequest={
                                'token': self.Token, 'sign': self.Sign,
                                'cuitRepresentada': self.Cuit, },
                                )['consultarCategoriasEmisorReturn']
        self.__analizar_errores(ret)
        array = ret.get('arrayCategoriasEmisor', [])
        lista = [it['codigoDescripcionString'] for it in array]
        return [(u"%s {codigo} %s {descripcion} %s" % (sep, sep, sep)).format(**it) if sep else it for it in lista]


    def ConsultarTiposCategoriaReceptor(self, sep="||"):
        "Obtener el código y descripción para cada tipos de categorías de receptor"
        ret = self.client.consultarTiposCategoriaReceptor(
                            authRequest={
                                'token': self.Token, 'sign': self.Sign,
                                'cuitRepresentada': self.Cuit, },
                                )['consultarCategoriasReceptorReturn']
        self.__analizar_errores(ret)
        array = ret.get('arrayCategoriasReceptor', [])
        lista = [it['codigoDescripcionString'] for it in array]
        return [(u"%s {codigo} %s {descripcion} %s" % (sep, sep, sep)).format(**it) if sep else it for it in lista]


    def ConsultarTiposEstado(self, sep="||"):
        "Obtener el código y descripción para cada estado posibles en los que puede estar un remito cárnico"
        ret = self.client.consultarTiposEstado(
                            authRequest={
                                'token': self.Token, 'sign': self.Sign,
                                'cuitRepresentada': self.Cuit, },
                                )['consultarTiposEstadoReturn']
        self.__analizar_errores(ret)
        array = ret.get('arrayTiposEstado', [])
        lista = [it['codigoDescripcionString'] for it in array]
        return [(u"%s {codigo} %s {descripcion} %s" % (sep, sep, sep)).format(**it) if sep else it for it in lista]


    def ConsultarGruposCarne(self, sep="||"):
        "Obtener el código y descripción para los grupos de los distintos tipos de cortes de carne"
        ret = self.client.consultarGruposCarne(
                            authRequest={
                                'token': self.Token, 'sign': self.Sign,
                                'cuitRepresentada': self.Cuit, },
                                )['consultarGruposCarneReturn']
        self.__analizar_errores(ret)
        array = ret.get('arrayGruposCarne', [])
        lista = [it['codigoDescripcionString'] for it in array]
        return [(u"%s {codigo} %s {descripcion} %s" % (sep, sep, sep)).format(**it) if sep else it for it in lista]


    def ConsultarTiposCarne(self, cod_grupo_carne=1, sep="||"):
        "Obtener el código y descripción para tipos de corte de carne"
        ret = self.client.consultarTiposCarne(
                            authRequest={
                                'token': self.Token, 'sign': self.Sign,
                                'cuitRepresentada': self.Cuit, },
                            codGrupoCarne=cod_grupo_carne,
                            )['consultarTiposCarneReturn']
        self.__analizar_errores(ret)
        array = ret.get('arrayTiposCarne', [])
        lista = [it['codigoDescripcionString'] for it in array]
        return [(u"%s {codigo} %s {descripcion} %s" % (sep, sep, sep)).format(**it) if sep else it for it in lista]


    def ConsultarCodigosDomicilio(self, cuit_titular=1, sep="||"):
        "Obtener el código de depositos que tiene habilitados para operar el cuit informado"
        ret = self.client.consultarCodigosDomicilio(
                            authRequest={
                                'token': self.Token, 'sign': self.Sign,
                                'cuitRepresentada': self.Cuit, },
                            cuitTitularDomicilio=cuit_titular,
                            )['consultarCodigosDomicilioReturn']
        self.__analizar_errores(ret)
        array = ret.get('arrayDomicilios', [])
        lista = [it['codigoDescripcion'] for it in array]
        return [(u"%s {codigo} %s {descripcion} %s" % (sep, sep, sep)).format(**it) if sep else it for it in lista]

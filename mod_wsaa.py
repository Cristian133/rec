#!/usr/bin/env python3

import xml.etree.ElementTree as ET
from zeep import Client
import datetime as DT
import subprocess
import os.path
import sys


WSDL_HOMO = 'https://wsaahomo.afip.gov.ar/ws/services/LoginCms?wsdl'
WSDL_PROD = 'https://wsaa.afip.gov.ar/ws/services/LoginCms?wsdl'
WSDL = WSDL_HOMO

class ta:
    '''
    Extrae datos del Ticket de Acceso enviado por AFIP
    según WSN (Web servicio de Negocio)
    '''
    def __init__(self, servicio):
        self.ta_name = 'ta.' + servicio + '.xml'
        self.tree = ET.parse(self.ta_name)
        self.root = self.tree.getroot()
        self.header = self.root.find('header')
        self.credentials = self.root.find('credentials')
        self.source = self.header.find('source').text
        self.destination = self.header.find('destination').text
        self.uniqueId = self.header.find('uniqueId').text
        self.generationTime = self.header.find('generationTime').text
        self.expirationTime = self.header.find('expirationTime').text
        self.date_gen = DT.datetime.strptime(self.generationTime,\
                '%Y-%m-%dT%H:%M:%S.%f-03:00')
        self.date_exp = DT.datetime.strptime(self.expirationTime,\
                '%Y-%m-%dT%H:%M:%S.%f-03:00')
        self.token = self.credentials.find('token').text
        self.sign = self.credentials.find('sign').text

    def __str__(self):
        return  'SOURCE:          '  + '\t'  + self.source +         '\n' + \
                'DESTINATION:     '  + '\t'  + self.destination +    '\n' + \
                'UNIQUE ID:       '  + '\t'  + self.uniqueId +       '\n' + \
                'GENERATION TIME: '  + '\t'  + self.generationTime + '\n' + \
                'EXPIRATION TIME: '  + '\t'  + self.expirationTime + '\n' + \
                'TOKEN:           '  + '\t'  + self.token +          '\n' + \
                'SIGN:            '  + '\t'  + self.sign +           '\n'

    def es_valido(self):
        try:
            date_exp_ta = self.date_exp
        except:
            return False
        if date_exp_ta > DT.datetime.now():
            return True
        else:
            return False

    def delta_T(self):
        return self.date_exp - DT.datetime.now()

    def delta_T_str(self):
        if self.date_exp > DT.datetime.now():
            print(self.date_exp - DT.datetime.now())
            return
        return


def _genera_tra(servicio, diruser):
    '''
    Genera tra.servicio.xml
    '''
    gen = DT.datetime.now()
    exp = DT.datetime.now() + DT.timedelta(minutes=20)
    uniqueId = str(int(gen.timestamp()))

    date_gen = gen.strftime("%Y-%m-%dT%H:%M:%S-03:00")
    date_exp = exp.strftime("%Y-%m-%dT%H:%M:%S-03:00")

    root = ET.Element("loginTicketRequest", version='1.0')
    head = ET.SubElement(root, "header")
    service = ET.SubElement(root, "service").text = servicio

    ET.SubElement(head, "uniqueId").text = uniqueId
    ET.SubElement(head, "generationTime").text = date_gen
    ET.SubElement(head, "expirationTime").text = date_exp

    tree = ET.ElementTree(root)
    pathtra = diruser + '/' + 'tra.' + servicio + '.xml'
    tree.write(pathtra, encoding='utf-8', xml_declaration=True)
    print('Se escribe ' + pathtra)


def _env_openssl(servicio, diruser):
    '''
    A partir del certificado y su clave privada genera Ticket de Requerimiento
    de Acceso para el servicio en cuestión: tra.service.xml.cms.base64
    '''
    try:
        print('servicio = ' + servicio + ', diruser = ' + diruser)
        subprocess.call('./openssl.sh %s %s' %(servicio, diruser), shell=True)
        return
    except Exception as e:
        print('Error: No se procesa' + diruser + '/' \
                + 'tra.' + servicio + '.xml')
        print(e.message)
        return


def _pide_ta(servicio, diruser):
    '''
    Lee tra.service.xml.cms.base64 y gestiona pedido de ta.xml a AFIP
    '''
    er=False
    _genera_tra(servicio, diruser)
    _env_openssl(servicio, diruser)
    cliente=Client(wsdl=WSDL)
    f_path = diruser + '/' + 'tra.' + servicio + '.xml.cms.base64'
    try:
        with open(f_path, 'r') as f_input:
            print('Se abre el archivo ' + f_path)
            in0 = f_input.read()
    except FileNotFoundError:
        print('No se encuentra el archivo ' + f_path)
        return -1
    except PermissionError:
        print('No tenemos permisos para abrir el archivo ' + f_path)
        return -1

    try:
        ta=cliente.service.loginCms(in0)
    except Exception as e:
        print('No se obtiene Ticket de Acceso ta.' + servicio + '.xml')
        print(e.message)
        er = True

    if  er == False:
        '''
        si no hubo exception entra en este bloque
        '''
        f = 'ta.' + servicio + '.xml'
        with open(f, 'w') as f_out:
            f_out.write(ta)
            print('Se obtiene ta.' + servicio + '.xml')
            return 0

def wsaa(servicio, diruser):
    '''
    Verifica validez de ta.service.xml y si no es válido lo pide.
    '''
    if os.path.exists('ta.' + servicio + '.xml'):
        print('ta.' + servicio + '.xml existe')
        try:
            x = ta(servicio)
        except:
            print('pero esta corrupto, se pide_ta')
            if _pide_ta(servicio, diruser) == 0:
                return 0
            else:
                return -1
        if x.es_valido():
            print('El ta actual es válido')
            print('Salimos sin pedir ta')
            return 0
        else:
            print('el ta actual esta vencido, se pide_ta')
            if _pide_ta(servicio, diruser)== 0:
                return 0
            else:
                return -1
    else:
        print('ta.' + servicio + '.xml no existe')
        print('se pide_ta')
        if _pide_ta(servicio, diruser) == 0:
            return 0
        else:
            return -1

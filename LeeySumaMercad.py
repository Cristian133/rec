#!/usr/bin/env python3

arrayMercaderias = {'mercaderia':[]}

def LeeMercaderia(arch):
    n = 0
    j = 0
    z = 0
    repetido = False
    lista_args = []
    with open(arch) as arch_ent:
        for line in arch_ent:
            if j == 0:
                if n < 7:
                    lista_args.append(line.strip('\n'))
                    n = n + 1
                else:
                    if AgregarMercaderia(*lista_args):
                        print('AgregaMercaderia: ' + str(lista_args))
                        n = 0
                        lista_args.clear()
                        j = j +1

            if j > 0:
                if n < 7:
                    lista_args.append(line.strip('\n'))
                    n = n + 1
                else:
                    for mercaderia in arrayMercaderias['mercaderia']:
                        print('for')
                        if mercaderia['codTipoProd'] == lista_args[1] and mercaderia['tropa'] == lista_args[2]:
                            print('ENCONTRO RENGLON REPETIDO\ncodTipoProd: ' + mercaderia['codTipoProd'] +
                                    ' orden: ' + mercaderia['orden'] + ' tropa: ' + mercaderia['tropa'] +
                                    ' kilos: ' + mercaderia['kilos'])
                            kilos = float(mercaderia['kilos'].replace(",",".")) + float(lista_args[3].replace(",","."))
                            mercaderia['kilos'] = str(kilos)
                            unit = float(mercaderia['unidades'].replace(",",".")) + 1
                            mercaderia['unidades'] = str(unit)
                            repetido = True
                            n=0
                            break
                    if repetido == False: #Si es repetido no se agrega.
                        if AgregarMercaderia(*lista_args):
                            print('AgregaMercaderia: ' + str(lista_args))
                            n = 0
                            lista_args.clear()
                            lista_args.append(line.strip('\n'))
                            n = n + 1
                            j = j +1

    return (j, n)


def AgregarMercaderia(Orden, CodigoTipoProducto, Tropa,
                      Cantidad, Unidades,
                      CantidadRecibida, UnidadesRecibidas):

    mercaderia = {'orden': Orden,
                  'codTipoProd': CodigoTipoProducto,
                  'tropa': Tropa,
                  'kilos': Cantidad,
                  'unidades': Unidades,
                  'kilosRec': CantidadRecibida,
                  'unidadesRec': UnidadesRecibidas,
                  }

    arrayMercaderias['mercaderia'].append(mercaderia)
    print('Agrego item array Mercaderia')
    return True


if __name__=='__main__':
    t = LeeMercaderia('Mercaderias.txt')
    for mercaderia in arrayMercaderias['mercaderia']:
        print(mercaderia)
    print(t)

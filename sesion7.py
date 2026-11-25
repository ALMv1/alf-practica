import sys

from sesion7 import (
    validar_entrada,
    obtener_cadena_tiempo,
    obtener_cadena_coordenada,
    validar_telefono,
    validar_nif,
    validar_tiempo
)


def tiempo_a_tupla(t_dict):
    """
    Convierte el diccionario de tiempo de la Sesión 7 en una tupla
    para permitir comparaciones directas de fechas (<, <=, >, >=).
    """
    return (t_dict['anyo'], t_dict['mes'], t_dict['dia'], t_dict['hora'], t_dict['minutos'], t_dict['segundos'])


def opcion_normaliza(fichero, f1=2, f2=3):
    """
    Opción -normaliza:
    Muestra los registros normalizados formateando fecha (f1) y coordenadas (f2).
    """
    try:
        f = open(fichero, 'r', encoding='utf-8')
    except Exception:
        sys.exit(1)

    for linea in f:
        datos = validar_entrada(linea)
        if datos is None:
            continue  # Se ignoran las entradas con errores de formato

        t_str = obtener_cadena_tiempo(datos['tiempo'], f1)
        c_str = obtener_cadena_coordenada(datos['coordenadas'], f2)

        print(f"{datos['telefono']} ; {datos['nif']} ; {t_str} ; {c_str} ; {datos['producto']} ; {datos['precio']}")

    f.close()


def opcion_telefono(fichero, telefono_buscado):
    """
    Opción -telefono:
    Muestra únicamente las entradas originales cuyo teléfono coincida con el argumento.
    """
    tel_norm = validar_telefono(telefono_buscado)
    if tel_norm is None:
        tel_norm = telefono_buscado

    try:
        f = open(fichero, 'r', encoding='utf-8')
    except Exception:
        sys.exit(1)

    for linea in f:
        datos = validar_entrada(linea)
        if datos is None:
            continue

        if datos['telefono'] == tel_norm or datos['telefono'] == telefono_buscado:
            print(datos['linea_original'])

    f.close()


def opcion_nif(fichero, nif_buscado):
    """
    Opción -nif:
    Muestra únicamente las entradas originales cuyo NIF coincida con el argumento.
    """
    nif_norm = validar_nif(nif_buscado)
    if nif_norm is None:
        nif_norm = nif_buscado

    try:
        f = open(fichero, 'r', encoding='utf-8')
    except Exception:
        sys.exit(1)

    for linea in f:
        datos = validar_entrada(linea)
        if datos is None:
            continue

        if datos['nif'] == nif_norm or datos['nif'] == nif_buscado:
            print(datos['linea_original'])

    f.close()


def opcion_intervalo(fichero, desde_raw, hasta_raw):
    """
    Opción -intervalo:
    Muestra únicamente las entradas originales cuya fecha esté dentro del intervalo [desde, hasta].
    """
    d_dict = validar_tiempo(desde_raw)
    h_dict = validar_tiempo(hasta_raw)

    if d_dict is None or h_dict is None:
        sys.exit(1)

    t_desde = tiempo_a_tupla(d_dict)
    t_hasta = tiempo_a_tupla(h_dict)

    if t_desde > t_hasta:
        sys.exit(1)

    try:
        f = open(fichero, 'r', encoding='utf-8')
    except Exception:
        sys.exit(1)

    for linea in f:
        datos = validar_entrada(linea)
        if datos is None:
            continue

        t_ev = tiempo_a_tupla(datos['tiempo'])
        if t_desde <= t_ev <= t_hasta:
            print(datos['linea_original'])

    f.close()


# ==============================================================================
# GESTIÓN DE ARGUMENTOS DE LÍNEA DE COMANDOS (sys.argv)
# ==============================================================================
def main():
    if len(sys.argv) < 3:
        sys.exit(1)

    modo = sys.argv[1]
    fichero = sys.argv[2]

    if modo == "-normaliza":
        if len(sys.argv) == 3:
            opcion_normaliza(fichero, 2, 3)
        elif len(sys.argv) == 5:
            try:
                f1 = int(sys.argv[3])
                f2 = int(sys.argv[4])
                if 1 <= f1 <= 3 and 1 <= f2 <= 3:
                    opcion_normaliza(fichero, f1, f2)
                else:
                    sys.exit(1)
            except ValueError:
                sys.exit(1)
        else:
            sys.exit(1)

    elif modo == "-telefono":
        if len(sys.argv) == 4:
            opcion_telefono(fichero, sys.argv[3])
        else:
            sys.exit(1)

    elif modo == "-nif":
        if len(sys.argv) == 4:
            opcion_nif(fichero, sys.argv[3])
        else:
            sys.exit(1)

    elif modo == "-intervalo":
        if len(sys.argv) == 5:
            opcion_intervalo(fichero, sys.argv[3], sys.argv[4])
        else:
            sys.exit(1)

    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
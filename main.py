import sys
import regex as re
from sesion7 import (
    validar_entrada,
    obtener_cadena_tiempo,
    obtener_cadena_coordenada,
    validar_telefono,
    validar_nif,
    validar_tiempo
)

PATRON_TEL_NORMALIZADO = re.compile(r"\+34\d{9}")


def tiempo_a_lista(t_dict):
    """
    Precondición: t_dict es un diccionario de tiempo válido.
    Efecto: Convierte el diccionario en una lista ordenable cronológicamente.
    Resultado: Lista [anyo, mes, dia, hora, minutos, segundos].
    """
    return [
        t_dict['anyo'], t_dict['mes'], t_dict['dia'],
        t_dict['hora'], t_dict['minutos'], t_dict['segundos']
    ]


def opcion_normaliza(fichero, f1=2, f2=3):
    """
    Precondición: fichero es una ruta válida; f1 y f2 son enteros entre 1 y 3.
    Efecto: Imprime los registros válidos normalizados separados por ' ; '.
    Resultado: None.
    """
    try:
        f = open(fichero, 'r', encoding='utf-8')
    except Exception:
        exit(1)

    for linea in f:
        datos = validar_entrada(linea)
        if datos is None:
            continue

        t_str = obtener_cadena_tiempo(datos['tiempo'], f1)
        c_str = obtener_cadena_coordenada(datos['coordenadas'], f2)
        print(f"{datos['telefono']} ; {datos['nif']} ; {t_str} ; {c_str} ; {datos['producto']} ; {datos['precio']}")

    f.close()


def opcion_telefono(fichero, telefono_buscado):
    """
    Precondición: fichero es una ruta válida y telefono_buscado tiene formato válido.
    Efecto: Muestra las líneas originales cuyo teléfono coincide con el buscado.
    Resultado: None.
    """
    tel_norm = validar_telefono(telefono_buscado)
    if tel_norm is None:
        if PATRON_TEL_NORMALIZADO.fullmatch(telefono_buscado):
            tel_norm = telefono_buscado
        else:
            exit(1)

    try:
        f = open(fichero, 'r', encoding='utf-8')
    except Exception:
        exit(1)

    for linea in f:
        datos = validar_entrada(linea)
        if datos is None:
            continue

        if datos['telefono'] == tel_norm:
            print(datos['linea_original'])

    f.close()


def opcion_nif(fichero, nif_buscado):
    """
    Precondición: fichero es una ruta válida y nif_buscado es un NIF/NIE válido.
    Efecto: Muestra las líneas originales cuyo NIF coincide con el buscado.
    Resultado: None.
    """
    nif_norm = validar_nif(nif_buscado)
    if nif_norm is None:
        exit(1)

    try:
        f = open(fichero, 'r', encoding='utf-8')
    except Exception:
        exit(1)

    for linea in f:
        datos = validar_entrada(linea)
        if datos is None:
            continue

        if datos['nif'] == nif_norm:
            print(datos['linea_original'])

    f.close()


def opcion_intervalo(fichero, desde_raw, hasta_raw):
    """
    Precondición: fichero es válido; desde_raw y hasta_raw son fechas válidas (desde <= hasta).
    Efecto: Muestra las líneas originales ocurridas dentro del intervalo cerrado.
    Resultado: None.
    """
    d_dict = validar_tiempo(desde_raw)
    h_dict = validar_tiempo(hasta_raw)

    if d_dict is None or h_dict is None:
        exit(1)

    t_desde = tiempo_a_lista(d_dict)
    t_hasta = tiempo_a_lista(h_dict)

    if t_desde > t_hasta:
        exit(1)

    try:
        f = open(fichero, 'r', encoding='utf-8')
    except Exception:
        exit(1)

    for linea in f:
        datos = validar_entrada(linea)
        if datos is None:
            continue

        t_ev = tiempo_a_lista(datos['tiempo'])
        if t_desde <= t_ev <= t_hasta:
            print(datos['linea_original'])

    f.close()


def main():
    """
    Precondición: Argumentos recibidos en sys.argv.
    Efecto: Valida la sintaxis de invocación y ejecuta la opción seleccionada.
    Resultado: None (termina con exit(1) ante cualquier error de argumentos).
    """
    if len(sys.argv) < 3:
        exit(1)

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
                    exit(1)
            except ValueError:
                exit(1)
        else:
            exit(1)

    elif modo == "-telefono":
        if len(sys.argv) == 4:
            opcion_telefono(fichero, sys.argv[3])
        else:
            exit(1)

    elif modo == "-nif":
        if len(sys.argv) == 4:
            opcion_nif(fichero, sys.argv[3])
        else:
            exit(1)

    elif modo == "-intervalo":
        if len(sys.argv) == 5:
            opcion_intervalo(fichero, sys.argv[3], sys.argv[4])
        else:
            exit(1)

    else:
        exit(1)


if __name__ == "__main__":
    main()
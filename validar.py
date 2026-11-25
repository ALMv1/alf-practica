import re

LETRAS_DNI = 'TRWAGMYFPDXBNJZSQVHLCKE'

MONTHS = [
    'january', 'february', 'march', 'april', 'may', 'june',
    'july', 'august', 'september', 'october', 'november', 'december'
]

NOMBRES_MESES = [
    "", "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

PATRON_TELEFONO = re.compile(r"(\d{3})-(\d{3})-(\d{3})")
PATRON_NIF = re.compile(r"(\d{8}|[XYZ]\d{7})-([A-Z])")

PATRON_TIEMPO_1 = re.compile(r"(\d{4})-(\d{2})-(\d{2})\s+(\d{2}):(\d{2})")
PATRON_TIEMPO_2 = re.compile(r"(?i)([a-zA-Z]+)\s+([1-9]\d?),\s+([1-9]\d{0,3})\s+([1-9]\d?):(\d{2})\s+(AM|PM)")
PATRON_TIEMPO_3 = re.compile(r"(\d{2}):(\d{2}):(\d{2})\s+(\d{2})/(\d{2})/(\d{4})")

PATRON_GEOGRAFICO_1 = re.compile(r"([+-]?(?:0|[1-9]\d*)\.\d+)\s*,\s*([+-]?(?:0|[1-9]\d*)\.\d+)")
PATRON_GEOGRAFICO_2 = re.compile(r"""((?:0|[1-9]\d*))°\s*((?:0|[1-9]\d*))'\s*((?:0|[1-9]\d*)\.\d{4})"\s*([NS])\s*,\s*((?:0|[1-9]\d*))°\s*((?:0|[1-9]\d*))'\s*((?:0|[1-9]\d*)\.\d{4})"\s*([EW])""")
PATRON_GEOGRAFICO_3 = re.compile(r"(\d{3})(\d{2})(\d{2}\.\d{4})([NS])(\d{3})(\d{2})(\d{2}\.\d{4})([EW])")

PATRON_PRECIO = re.compile(r"((?:0|[1-9]\d*)(?:\.\d+)?)([€$])")


def esBisiesto(anyo):
    """
    Precondición: anyo es un entero positivo.
    Efecto: Comprueba si el año cumple las reglas del calendario gregoriano para ser bisiesto.
    Resultado: True si es bisiesto, False en caso contrario.
    """
    return (anyo % 4 == 0 and anyo % 100 != 0) or (anyo % 400 == 0)


def esFechaCorrecta(anyo, mes, dia):
    """
    Precondición: anyo, mes y dia son números enteros.
    Efecto: Verifica que el año esté en [1, 9999] y que el mes y el día existan en el calendario.
    Resultado: True si la fecha es válida, False en caso contrario.
    """
    if not (1 <= anyo <= 9999):
        return False

    if 1 <= mes <= 12:
        if mes in [1, 3, 5, 7, 8, 10, 12]:
            return 1 <= dia <= 31
        elif mes == 2:
            if esBisiesto(anyo):
                return 1 <= dia <= 29
            return 1 <= dia <= 28
        else:
            return 1 <= dia <= 30
    return False


def esHoraCorrecta(hora, minuto, segundo):
    """
    Precondición: hora, minuto y segundo son números enteros.
    Efecto: Comprueba que los valores estén dentro de un reloj de 24 horas.
    Resultado: True si la hora es válida, False en caso contrario.
    """
    return 0 <= hora < 24 and 0 <= minuto < 60 and 0 <= segundo < 60


def letraDNI(dni):
    """
    Precondición: dni es un número entero no negativo de 8 cifras.
    Efecto: Calcula el resto módulo 23 para obtener la letra de control oficial.
    Resultado: Carácter correspondiente en LETRAS_DNI.
    """
    mod = dni % 23
    return LETRAS_DNI[mod]


def mesNum(month):
    """
    Precondición: month es una cadena de texto.
    Efecto: Busca el nombre del mes en inglés sin distinguir mayúsculas o minúsculas.
    Resultado: Entero del 1 al 12 si coincide, o 0 si no es un mes válido.
    """
    try:
        return MONTHS.index(month.lower()) + 1
    except ValueError:
        return 0


def validar_telefono(tel):
    """
    Precondición: tel es una cadena de texto.
    Efecto: Valida el formato XXX-XXX-XXX y lo normaliza eliminando guiones y añadiendo +34.
    Resultado: Cadena con formato '+34XXXXXXXXX' si es válido, o None si no lo es.
    """
    res = PATRON_TELEFONO.fullmatch(tel)
    if not res:
        return None

    sin_guiones = PATRON_TELEFONO.sub(r'\1\2\3', tel)
    if len(sin_guiones) == 9:
        return f"+34{sin_guiones}"
    return None


def validar_nif(nif):
    """
    Precondición: nif es una cadena de texto.
    Efecto: Comprueba el formato de DNI/NIE y verifica que la letra coincida con el número.
    Resultado: La cadena original si es válida, o None en caso contrario.
    """
    res = PATRON_NIF.fullmatch(nif)
    if not res:
        return None

    cuerpo = res.group(1)
    letra_dada = res.group(2)

    if cuerpo[0] == "X":
        cuerpo = '0' + cuerpo[1:]
    elif cuerpo[0] == "Y":
        cuerpo = '1' + cuerpo[1:]
    elif cuerpo[0] == "Z":
        cuerpo = '2' + cuerpo[1:]

    letra_correcta = letraDNI(int(cuerpo))

    if letra_dada == letra_correcta:
        return nif
    return None


def validar_tiempo(tiempo):
    """
    Precondición: tiempo es una cadena de texto.
    Efecto: Valida la sintaxis en cualquiera de los 3 formatos del Anexo 1 y comprueba su validez semántica.
    Resultado: Diccionario {'anyo', 'mes', 'dia', 'hora', 'minutos', 'segundos'} o None.
    """
    res = PATRON_TIEMPO_1.fullmatch(tiempo)
    if res:
        anyo, mes, dia = int(res.group(1)), int(res.group(2)), int(res.group(3))
        hora, minuto, segundo = int(res.group(4)), int(res.group(5)), 0
    else:
        res = PATRON_TIEMPO_2.fullmatch(tiempo)
        if res:
            mes = mesNum(res.group(1))
            if mes == 0:
                return None

            dia, anyo = int(res.group(2)), int(res.group(3))
            h12, minuto = int(res.group(4)), int(res.group(5))
            ampm = res.group(6).upper()

            if not (1 <= h12 <= 12):
                return None

            if ampm == "AM":
                if h12 == 12:
                    hora = 0
                else:
                    hora = h12
            else:
                if h12 == 12:
                    hora = 12
                else:
                    hora = h12 + 12
            segundo = 0
        else:
            res = PATRON_TIEMPO_3.fullmatch(tiempo)
            if res:
                hora, minuto, segundo = int(res.group(1)), int(res.group(2)), int(res.group(3))
                dia, mes, anyo = int(res.group(4)), int(res.group(5)), int(res.group(6))
            else:
                return None

    if esFechaCorrecta(anyo, mes, dia) and esHoraCorrecta(hora, minuto, segundo):
        return {
            'anyo': anyo,
            'mes': mes,
            'dia': dia,
            'hora': hora,
            'minutos': minuto,
            'segundos': segundo
        }

    return None


def sexagesimal_a_decimal(grados, minutos, segundos, orientacion):
    """
    Precondición: grados y minutos son enteros >= 0; segundos es float >= 0; orientacion es 'N', 'S', 'E' o 'W'.
    Efecto: Comprueba que minutos y segundos estén en [0, 60) y convierte la coordenada a grados decimales.
    Resultado: Valor float con signo según la orientación, o None si los minutos/segundos son inválidos.
    """
    if grados > 180 or minutos >= 60 or segundos >= 60:
        return None

    valor = grados + (minutos / 60.0) + (segundos / 3600.0)
    if orientacion == "S" or orientacion == "W":
        valor = -valor
    return valor


def validar_coordenada(coordenada):
    """
    Precondición: coordenada es una cadena de texto.
    Efecto: Valida la sintaxis en los 3 formatos del Anexo 2 y verifica los rangos de latitud y longitud.
    Resultado: Diccionario {'latitud', 'longitud'} en formato decimal o None si es inválida.
    """
    res = PATRON_GEOGRAFICO_1.fullmatch(coordenada)
    if res:
        lat, lon = float(res.group(1)), float(res.group(2))
    else:
        res = PATRON_GEOGRAFICO_2.fullmatch(coordenada)
        if not res:
            res = PATRON_GEOGRAFICO_3.fullmatch(coordenada)

        if res:
            lat = sexagesimal_a_decimal(int(res.group(1)), int(res.group(2)), float(res.group(3)), res.group(4))
            lon = sexagesimal_a_decimal(int(res.group(5)), int(res.group(6)), float(res.group(7)), res.group(8))
            if lat is None or lon is None:
                return None
        else:
            return None

    if -90.0 <= lat <= 90.0 and -180.0 <= lon <= 180.0:
        return {'latitud': lat, 'longitud': lon}
    return None


def obtener_cadena_tiempo(t, formato):
    """
    Precondición: t es un diccionario de tiempo válido; formato es un entero entre 1 y 3.
    Efecto: Formatea el instante temporal según el estándar del Anexo 1 indicado.
    Resultado: Cadena formateada o cadena vacía si el formato no es válido.
    """
    anyo, mes, dia = t['anyo'], t['mes'], t['dia']
    hora, minutos, segundos = t['hora'], t['minutos'], t['segundos']

    if formato == 1:
        return f"{anyo:04d}-{mes:02d}-{dia:02d} {hora:02d}:{minutos:02d}"

    elif formato == 2:
        nombre_mes = NOMBRES_MESES[mes]
        if hora == 0:
            h12, ampm = 12, "AM"
        elif 1 <= hora <= 11:
            h12, ampm = hora, "AM"
        elif hora == 12:
            h12, ampm = 12, "PM"
        else:
            h12, ampm = hora - 12, "PM"

        return f"{nombre_mes} {dia}, {anyo} {h12}:{minutos:02d} {ampm}"

    elif formato == 3:
        return f"{hora:02d}:{minutos:02d}:{segundos:02d} {dia:02d}/{mes:02d}/{anyo:04d}"

    return ""


def decimal_a_sexagesimal(val_decimal):
    """
    Precondición: val_decimal es un número real en grados decimales.
    Efecto: Descompone el valor absoluto en grados, minutos y segundos redondeados a 4 decimales con acarreo.
    Resultado: Lista [grados, minutos, segundos].
    """
    val_abs = abs(val_decimal)
    grados = int(val_abs)
    resto_minutos = (val_abs - grados) * 60.0
    minutos = int(resto_minutos)
    segundos = round((resto_minutos - minutos) * 60.0, 4)

    if segundos >= 60.0:
        segundos = 0.0
        minutos += 1
    if minutos >= 60:
        minutos = 0
        grados += 1

    return [grados, minutos, segundos]


def obtener_cadena_coordenada(c, formato):
    """
    Precondición: c es un diccionario de coordenadas válido; formato es un entero entre 1 y 3.
    Efecto: Formatea las coordenadas según el estándar del Anexo 2 indicado.
    Resultado: Cadena formateada o cadena vacía si el formato no es válido.
    """
    lat, lon = c['latitud'], c['longitud']

    if formato == 1:
        return f"{lat}, {lon}"

    elif formato == 2:
        g_lat, m_lat, s_lat = decimal_a_sexagesimal(lat)
        if lat >= 0:
            o_lat = 'N'
        else:
            o_lat = 'S'

        g_lon, m_lon, s_lon = decimal_a_sexagesimal(lon)
        if lon >= 0:
            o_lon = 'E'
        else:
            o_lon = 'W'

        return f'{g_lat}° {m_lat}\' {s_lat:.4f}" {o_lat}, {g_lon}° {m_lon}\' {s_lon:.4f}" {o_lon}'

    elif formato == 3:
        g_lat, m_lat, s_lat = decimal_a_sexagesimal(lat)
        if lat >= 0:
            o_lat = 'N'
        else:
            o_lat = 'S'

        g_lon, m_lon, s_lon = decimal_a_sexagesimal(lon)
        if lon >= 0:
            o_lon = 'E'
        else:
            o_lon = 'W'

        return f"{g_lat:03d}{m_lat:02d}{s_lat:07.4f}{o_lat}{g_lon:03d}{m_lon:02d}{s_lon:07.4f}{o_lon}"

    return ""


def validar_precio(precio):
    """
    Precondición: precio es una cadena de texto.
    Efecto: Comprueba que sea un entero o decimal sin ceros superfluos a la izquierda seguido de € o $.
    Resultado: La cadena original si es válida, o None en caso contrario.
    """
    res = PATRON_PRECIO.fullmatch(precio)
    if res:
        return precio
    return None


def validar_entrada(linea):
    """
    Precondición: linea es una cadena correspondiente a una fila del fichero de registro.
    Efecto: Separa los 6 campos por ';' y valida tanto el formato como la semántica de cada uno.
    Resultado: Diccionario con los datos normalizados y la línea original, o None si algún campo falla.
    """
    linea_sin_salto = linea.strip('\r\n')
    if not linea_sin_salto.strip():
        return None

    campos = linea_sin_salto.split(';')
    if len(campos) != 6:
        return None

    tel_raw = campos[0].strip()
    nif_raw = campos[1].strip()
    tiempo_raw = campos[2].strip()
    coord_raw = campos[3].strip()
    prod_raw = campos[4].strip()
    precio_raw = campos[5].strip()

    tel = validar_telefono(tel_raw)
    nif = validar_nif(nif_raw)
    tiempo = validar_tiempo(tiempo_raw)
    coord = validar_coordenada(coord_raw)
    precio = validar_precio(precio_raw)

    if not prod_raw:
        return None

    if tel is None or nif is None or tiempo is None or coord is None or precio is None:
        return None

    return {
        'telefono': tel,
        'nif': nif,
        'tiempo': tiempo,
        'coordenadas': coord,
        'producto': prod_raw,
        'precio': precio,
        'linea_original': linea_sin_salto
    }
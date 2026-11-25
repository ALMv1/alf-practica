import sys

def mostrar_errores_exit():
    print("Error de sintaxis al invocar.", file=sys.stderr)
    print("Formato esperado:", file=sys.stderr)

    print("  python main.py -normaliza <fichero> [<f1> <f2>]", file=sys.stderr)
    print("  python main.py -telefono <fichero> <telefono>", file=sys.stderr)
    print("  python main.py -nif <fichero> <NIF>", file=sys.stderr)
    print("  python main.py -intervalo <fichero> <desde> <hasta>", file=sys.stderr)
    sys.exit(1)
    
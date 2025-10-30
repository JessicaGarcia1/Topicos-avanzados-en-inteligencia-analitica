

def leer_pbm(ruta):
    with open(ruta, "r", encoding="utf-8") as f:
        lineas = f.readlines()

    limpias = []
    for ln in lineas:
        ln = ln.strip()
        if len(ln) > 0 and not ln.startswith("#"):
            limpias.append(ln)

    header = limpias[0]
    if header.startswith("\ufeff"):
        header = header[1:]
    if not header.startswith("P1"):
        raise Exception("No es PBM tipo P1: " + ruta)

    dims = limpias[1].split()
    ancho = int(dims[0]); alto = int(dims[1])

    tokens = []
    for linea in limpias[2:]:
        tokens += linea.split()

    vals = []
    total = ancho * alto
    for k in range(total):
        t = tokens[k] if k < len(tokens) else "0"
        vals.append(1 if t == "1" else -1)

    return vals, alto, ancho


def signo(x):
    if x > 0: return 1
    if x < 0: return -1
    return 0

def outer(v):
    n = len(v)
    M = []
    for i in range(n):
        fila = []
        for j in range(n):
            fila.append(v[i] * v[j])
        M.append(fila)
    return M

def suma_matrices(A, B):
    n = len(A)
    C = []
    for i in range(n):
        fila = []
        for j in range(n):
            fila.append(A[i][j] + B[i][j])
        C.append(fila)
    return C

def diagonal_cero(W):
    for i in range(len(W)):
        W[i][i] = 0
    return W

def vec_por_mat(v, W):
    n = len(v)
    r = []
    for j in range(n):
        s = 0
        for i in range(n):
            s += v[i] * W[i][j]
        r.append(s)
    return r

def actualizar_sincrono(U, W):
    campo = vec_por_mat(U, W)
    return [signo(z) for z in campo]

def iguales(a, b):
    if len(a) != len(b): return False
    for i in range(len(a)):
        if a[i] != b[i]: return False
    return True

def similitud(a, b):
    s = 0
    for i in range(len(a)):
        if a[i] == b[i]:
            s += 1
    return s

def imprimir_figura(vec, M, N):
    k = 0
    for i in range(M):
        linea = ""
        for j in range(N):
            if vec[k] == 1:
                linea += "■"  # cuadrado negro
            else:
                linea += "□"  # cuadrado blanco
            k += 1
        print(linea)


def leer_manual_8x8():
    print("\nEscribe tu figura 8x8 (usa #/. o 1/0, ambos funcionan)")
    filas = []
    for i in range(8):
        fila = input(f"Línea {i+1}: ").strip()
        for j in range(8):
            if j < len(fila):
                c = fila[j]
                if c in ['#', '1']:
                    filas.append(1)
                else:
                    filas.append(-1)
            else:
                filas.append(-1)
    return filas


# -------- PROGRAMA PRINCIPAL --------
print("=== Hopfield: figura manual 8x8 (visual con cuadros negros/blancos) ===")

rutas   = ["cuadro.pbm", "triangulo.pbm", "cruz.pbm", "circulo.pbm", "rombo.pbm"]
nombres = ["cuadro", "triangulo", "cruz", "circulo", "rombo"]

x0, M, N = leer_pbm(rutas[0])
Ntot = len(x0)

W = outer(x0)
patrones = [x0]
for p in range(1, len(rutas)):
    xp, Mp, Np = leer_pbm(rutas[p])
    if Mp != M or Np != N:
        raise Exception("Tamaño distinto en " + rutas[p])
    W = suma_matrices(W, outer(xp))
    patrones.append(xp)
W = diagonal_cero(W)

print("\nFiguras entrenadas:", nombres)

U = leer_manual_8x8()
print("\nFigura ingresada:")
imprimir_figura(U, M, N)

max_iter = 10
for t in range(max_iter):
    print("\n--- Iteración", t, "---")
    imprimir_figura(U, M, N)
    print("Similitud con patrones:")
    for i in range(len(patrones)):
        print(f" {nombres[i]}: {similitud(U, patrones[i])} / {Ntot}")
    input("\nPresiona ENTER para continuar...")
    U_next = actualizar_sincrono(U, W)
    if iguales(U_next, U):
        print("\nLa red se estabilizó (punto fijo).")
        break
    U = U_next

print("\nFigura recordada:")
imprimir_figura(U, M, N)

mejor = 0
mejor_val = similitud(U, patrones[0])
for i in range(1, len(patrones)):
    s = similitud(U, patrones[i])
    if s > mejor_val:
        mejor_val = s
        mejor = i

print("\nResultado final:")
print("Figura reconocida como:", nombres[mejor])
print(f"Coincidencia: {mejor_val}/{Ntot}")

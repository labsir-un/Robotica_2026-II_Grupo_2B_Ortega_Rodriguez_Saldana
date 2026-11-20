
from robodk.robolink import *
from robodk.robomath import *

import math
import numpy as np

from matplotlib.textpath import TextPath
from matplotlib.font_manager import FontProperties


#================================================
# 1) Conexión a RoboDK e inicialización
#================================================

RDK = Robolink()

robot = RDK.ItemUserPick(
    "Selecciona un robot",
    ITEM_TYPE_ROBOT
)

if not robot.Valid():
    raise Exception("No se ha seleccionado un robot válido.")

# Conectar al robot físico
#if not robot.Connect():
#    raise Exception("No se pudo conectar al robot.")

# Confirmar conexión
#if not robot.ConnectedState():
#    raise Exception("El robot no está conectado correctamente.")

#print("Robot conectado correctamente.")


#================================================
# 2. CARGAR FRAME Y TARGETS
#================================================

frame_name = "Frame_from_Target1"

frame = RDK.Item(frame_name, ITEM_TYPE_FRAME)

T_H = RDK.Item("Target_Home", ITEM_TYPE_TARGET)
T_A = RDK.Item("Target_Aprox", ITEM_TYPE_TARGET)

if not frame.Valid():
    raise Exception("No se encontro el Frame.")

if not T_H.Valid():
    raise Exception("No se encontro Target_Home.")

if not T_A.Valid():
    raise Exception("No se encontro Target_Aprox.")


robot.setPoseFrame(frame)
robot.setPoseTool(robot.PoseTool())

orientacion = T_A.PoseWrt(frame)
orientacion.setPos([0, 0, 0])


def pose_dibujo(x, y, z):

    return transl(x, y, z) * orientacion


robot.setSpeed(300)
robot.setRounding(0)


#================================================
# 3. PARAMETROS DE LA MARIPOSA
#================================================

num_points = 2160

A = 250

angulo_rotacion = -90

z_surface = 0
z_safe = 50

z_retiro = z_surface - z_safe

desplazamiento_mariposa = 50


#================================================
# 4. FUNCION DE LA MARIPOSA
#================================================

def butterfly(t):

    r = (
        math.exp(math.cos(t))
        - 2 * math.cos(4 * t)
        - math.sin(t / 12) ** 5
    )

    x = r * math.sin(t)
    y = r * math.cos(t)

    alfa = math.radians(angulo_rotacion)

    x_rot = x * math.cos(alfa) - y * math.sin(alfa)
    y_rot = x * math.sin(alfa) + y * math.cos(alfa)

    return x_rot, y_rot


#================================================
# 5. GENERAR TRAYECTORIA DE LA MARIPOSA
#================================================

t_inicio = 0
t_final = 12 * math.pi

puntos = []

for i in range(num_points + 1):

    t = t_inicio + (
        (t_final - t_inicio) * i / num_points
    )

    x, y = butterfly(t)

    puntos.append((x, y))


# Escalado
radio_max = max(
    math.hypot(x, y)
    for x, y in puntos
)

escala = A / radio_max

puntos_escalados = [

    (
        x * escala,
        y * escala + desplazamiento_mariposa
    )

    for x, y in puntos
]


# Punto inicial y final
x_inicio, y_inicio = puntos_escalados[0]

x_final = x_inicio
y_final = y_inicio


# Limites de la mariposa
x_min_mariposa = min(
    x for x, y in puntos_escalados
)

x_max_mariposa = max(
    x for x, y in puntos_escalados
)

y_min_mariposa = min(
    y for x, y in puntos_escalados
)

y_max_mariposa = max(
    y for x, y in puntos_escalados
)


# Centro de la mariposa
centro_y_mariposa = (
    y_min_mariposa + y_max_mariposa
) / 2


#================================================
# 6. CONFIGURACION DEL TEXTO
#================================================

nombres = ["JUAN", "YEISON", "DANIEL"]

fuente = FontProperties(
    family="DejaVu Sans",
    weight="bold"
)

# Dimensiones del texto
ancho_max = 160
alto_max = 25

# Separacion entre nombres
separacion_nombres = 15

# Separacion respecto a la mariposa
margen_mariposa = 25

# Centro de las palabras
x_centro = 0


#================================================
# 7. ORIENTACION DEL TEXTO
#================================================

INVERTIR_X = True

ROTACION_TEXTO = -90

theta = math.radians(ROTACION_TEXTO)

cos_t = math.cos(theta)
sin_t = math.sin(theta)


#================================================
# 8. POSICIONAMIENTO DE LOS NOMBRES
#================================================

trayectorias_texto = []

# IMPORTANTE:
#
# Con ROTACION_TEXTO = -90,
# el ancho de las palabras queda orientado
# principalmente sobre el eje Y.
#
# Por eso ahora las separamos sobre X.

# +1: avanzar hacia X positivo
# -1: avanzar hacia X negativo
#
# Si los nombres aparecen en el lado contrario
# al que quieres, cambia este valor.

DIRECCION_DEBAJO = 1


# Primera posicion respecto a la mariposa
if DIRECCION_DEBAJO == 1:

    x_cursor = x_max_mariposa + margen_mariposa

else:

    x_cursor = x_min_mariposa - margen_mariposa


for indice, nombre in enumerate(nombres):

    #--------------------------------------------
    # Crear texto con Matplotlib
    #--------------------------------------------

    texto = TextPath(
        (0, 0),
        nombre,
        size=100,
        prop=fuente
    )

    poligonos = texto.to_polygons()

    if len(poligonos) == 0:
        continue


    #--------------------------------------------
    # Dimensiones originales
    #--------------------------------------------

    todos_puntos = np.vstack(poligonos)

    x_min = np.min(todos_puntos[:, 0])
    x_max = np.max(todos_puntos[:, 0])

    y_min = np.min(todos_puntos[:, 1])
    y_max = np.max(todos_puntos[:, 1])

    ancho_original = x_max - x_min
    alto_original = y_max - y_min


    #--------------------------------------------
    # Escalado
    #--------------------------------------------

    factor_escala = min(
        ancho_max / ancho_original,
        alto_max / alto_original
    )


    # Centro original
    centro_x = (x_min + x_max) / 2
    centro_y = (y_min + y_max) / 2


    #--------------------------------------------
    # Aplicar transformaciones
    #--------------------------------------------

    poligonos_transformados = []

    for poligono in poligonos:

        puntos_transformados = []

        for punto in poligono:

            px = punto[0]
            py = punto[1]

            # Centrar y escalar
            x_local = (
                px - centro_x
            ) * factor_escala

            y_local = (
                py - centro_y
            ) * factor_escala


            # Corregir espejo
            if INVERTIR_X:

                x_local = -x_local


            # Rotacion
            x_rotado = (
                x_local * cos_t
                - y_local * sin_t
            )

            y_rotado = (
                x_local * sin_t
                + y_local * cos_t
            )


            puntos_transformados.append(
                (x_rotado, y_rotado)
            )


        poligonos_transformados.append(
            puntos_transformados
        )


    #--------------------------------------------
    # Obtener dimensiones despues de rotar
    #--------------------------------------------

    puntos_palabra = np.vstack(
        poligonos_transformados
    )

    x_min_rot = np.min(puntos_palabra[:, 0])
    x_max_rot = np.max(puntos_palabra[:, 0])

    y_min_rot = np.min(puntos_palabra[:, 1])
    y_max_rot = np.max(puntos_palabra[:, 1])


    #--------------------------------------------
    # CENTRAR LA PALABRA EN Y
    #--------------------------------------------

    # Todas las palabras quedan centradas
    # respecto al centro de la mariposa.

    desplazamiento_y = (
        centro_y_mariposa
        - (y_min_rot + y_max_rot) / 2
    )


    #--------------------------------------------
    # UBICAR CADA NOMBRE EN X
    #--------------------------------------------

    if DIRECCION_DEBAJO == 1:

        desplazamiento_x = (
            x_cursor - x_min_rot
        )

    else:

        desplazamiento_x = (
            x_cursor - x_max_rot
        )


    #--------------------------------------------
    # GUARDAR TRAYECTORIAS FINALES
    #--------------------------------------------

    for poligono in poligonos_transformados:

        puntos_finales = []

        for x, y in poligono:

            x_robot = x + desplazamiento_x

            y_robot = y + desplazamiento_y

            puntos_finales.append(
                (x_robot, y_robot)
            )


        # Cerrar contorno
        if puntos_finales:

            if not np.allclose(
                puntos_finales[0],
                puntos_finales[-1]
            ):

                puntos_finales.append(
                    puntos_finales[0]
                )


            trayectorias_texto.append(
                puntos_finales
            )


    #--------------------------------------------
    # ACTUALIZAR POSICION DEL SIGUIENTE NOMBRE
    #--------------------------------------------

    if DIRECCION_DEBAJO == 1:

        x_cursor = (
            x_cursor
            + (x_max_rot - x_min_rot)
            + separacion_nombres
        )

    else:

        x_cursor = (
            x_cursor
            - (x_max_rot - x_min_rot)
            - separacion_nombres
        )


    print(
        "Nombre:",
        nombre,
        "| Ancho:",
        round(x_max_rot - x_min_rot, 2),
        "mm"
    )


#================================================
# 9. FUNCION PARA DIBUJAR LOS NOMBRES
#================================================

def dibujar_nombres(trayectorias):

    for poligono in trayectorias:

        if len(poligono) < 2:
            continue

        # Primer punto
        x, y = poligono[0]

        # Aproximacion
        robot.MoveL(
            pose_dibujo(x, y, z_retiro)
        )

        # Descenso
        robot.MoveL(
            pose_dibujo(x, y, z_surface)
        )

        # Recorrer contorno
        for x, y in poligono[1:]:

            robot.MoveL(
                pose_dibujo(x, y, z_surface)
            )

        # Retirada
        x, y = poligono[-1]

        robot.MoveL(
            pose_dibujo(x, y, z_retiro)
        )


#================================================
# 10. APROXIMACION A LA MARIPOSA
#================================================

robot.MoveJ(T_H)

robot.MoveJ(T_A)

robot.setSpeed(50)
robot.setRounding(0)

robot.MoveJ(
    pose_dibujo(
        x_inicio,
        y_inicio,
        z_retiro
    )
)

robot.MoveL(
    pose_dibujo(
        x_inicio,
        y_inicio,
        z_surface
    )
)


#================================================
# 11. DIBUJAR MARIPOSA
#================================================

robot.setSpeed(30)
robot.setRounding(0)

for x, y in puntos_escalados[1:]:

    robot.MoveL(
        pose_dibujo(
            x,
            y,
            z_surface
        )
    )


# Retirada
robot.MoveL(
    pose_dibujo(
        x_final,
        y_final,
        z_retiro
    )
)


#================================================
# 12. ESCRIBIR LOS NOMBRES
#================================================

robot.setSpeed(30)
robot.setRounding(0)

dibujar_nombres(trayectorias_texto)


#================================================
# 13. REGRESAR A HOME
#================================================

robot.setSpeed(50)

robot.MoveJ(T_A)

robot.setSpeed(300)

robot.MoveJ(T_H)


#================================================
# 14. INFORMACION FINAL
#================================================

print("--------------------------------")
print("TRABAJO COMPLETADO")
print("--------------------------------")

print("Frame:", frame_name)

print("Mariposa:", A, "mm")

print("Segmentos:", num_points)

print("Nombres:", nombres)

print("Contornos:", len(trayectorias_texto))

print("Espejo X:", INVERTIR_X)

print("Rotacion texto:", ROTACION_TEXTO)

print("Direccion:", DIRECCION_DEBAJO)

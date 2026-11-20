
## Generación de trayectorias mediante funciones polares y texto

Se desarrolló un programa en **Python**, utilizando la API de **RoboDK**, para generar una trayectoria basada en una función polar con forma de mariposa, complementada con el trazado de los nombres de los integrantes.

El procedimiento permite transformar expresiones matemáticas y contornos vectoriales de texto en movimientos cartesianos ejecutables por el robot.

### 1. Configuración inicial del robot

El programa establece la comunicación con RoboDK mediante `Robolink()` y permite seleccionar el robot encargado de ejecutar la trayectoria.

Se utilizan tres elementos previamente definidos en la estación:

- **`Frame_from_Target1`:** sistema de referencia utilizado para el dibujo.
- **`Target_Home`:** posición inicial y final del robot.
- **`Target_Aprox`:** posición de aproximación y referencia para la orientación del efector final.

Adicionalmente, la función `pose_dibujo(x, y, z)` permite construir las poses cartesianas manteniendo una orientación constante del efector final durante el trazado.

### 2. Generación de la mariposa mediante una función polar

Para generar la figura se empleó la siguiente función polar:

$$
r(t)=e^{\cos(t)}-2\cos(4t)-\sin^5\left(\frac{t}{12}\right)
$$

Esta expresión combina funciones exponenciales y trigonométricas para producir los lóbulos y las variaciones características de la figura.

Posteriormente, se transforma la representación polar en coordenadas cartesianas mediante:

$$
x(t)=r(t)\sin(t)
$$

$$
y(t)=r(t)\cos(t)
$$

La función se implementó en Python de la siguiente manera:

```python
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
```

Para construir la trayectoria se evaluó la función en el intervalo:

$$
0\leq t\leq12\pi
$$

El intervalo se dividió en **2160 segmentos**, obteniendo una secuencia de puntos que permite reproducir la figura mediante movimientos lineales consecutivos. Vale la pena mencionar que esto en el manipulador real hubiera tomado demasiado tiempo en ejecutarse, por lo que al momento de implementarse se redujeron los puntos a 50. En la simulación si se aprecia el resultado con la cantidad correcta.

Finalmente, se aplicaron tres transformaciones geométricas:

- **Rotación de −90°:** para ajustar la orientación de la mariposa respecto al sistema de referencia.
- **Escalado:** se calculó un factor de escala para establecer una distancia radial máxima de 250 mm.
- **Desplazamiento:** se realizó una traslación de 50 mm sobre el eje Y para posicionar la figura dentro del área de trabajo.

Los puntos transformados se almacenaron en `puntos_escalados`, que posteriormente se utiliza para ejecutar el trazado.

### 3. Generación de los nombres mediante contornos vectoriales

Para incorporar los nombres **JUAN, YEISON y DANIEL**, se utilizó la biblioteca `matplotlib`, específicamente las herramientas `TextPath` y `FontProperties`.

A diferencia de la mariposa, cuya trayectoria se obtiene evaluando una ecuación matemática, los nombres se generan a partir de la geometría de sus caracteres.

El procedimiento se divide en las siguientes etapas:

**1. Conversión del texto en polígonos**

Cada palabra se genera utilizando la fuente `DejaVu Sans` en negrita. Mediante el método `to_polygons()`, las letras se transforman en conjuntos de coordenadas que representan sus contornos.

```python
texto = TextPath(
    (0, 0),
    nombre,
    size=100,
    prop=fuente
)

poligonos = texto.to_polygons()
```

De esta manera, no es necesario definir manualmente los puntos que conforman cada letra.

**2. Escalado de los caracteres**

Se calculan las dimensiones originales de cada palabra y se establece un factor de escala uniforme para conservar sus proporciones.

Las dimensiones máximas establecidas antes de la rotación son:

- Ancho máximo: **160 mm**.
- Alto máximo: **25 mm**.

**3. Orientación del texto**

Para ajustar la orientación de los nombres respecto al sistema de referencia del robot, se aplican dos transformaciones:

- Inversión sobre el eje X mediante `INVERTIR_X = True`.
- Rotación de −90° mediante `ROTACION_TEXTO = -90`.

Estas transformaciones permiten corregir la orientación visual de los caracteres sobre la superficie de dibujo.

**4. Posicionamiento automático**

Cada palabra se posiciona con respecto a los límites geométricos de la mariposa.

Se establece un margen inicial de **25 mm** respecto a la figura y una separación de **15 mm** entre nombres.

Debido a la rotación aplicada, las palabras quedan orientadas principalmente sobre el eje Y, por lo que su distribución consecutiva se realiza sobre el eje X.

Además, cada palabra se centra sobre el eje Y tomando como referencia el centro de la mariposa.

**5. Construcción de las trayectorias**

Los puntos transformados de cada contorno se almacenan en `trayectorias_texto`.

Se verifica que cada polígono se encuentre cerrado, agregando su punto inicial al final cuando sea necesario.

Así, cada letra se representa mediante una o varias trayectorias cartesianas independientes, que pueden ser recorridas por el manipulador.

### 4. Ejecución de las trayectorias

La ejecución se organiza en una secuencia que combina movimientos articulares y cartesianos:

1. **Aproximación:** el robot parte de `Target_Home`, pasa por `Target_Aprox` y se aproxima al punto inicial de la mariposa.
2. **Dibujo de la mariposa:** se recorren los puntos generados mediante movimientos lineales `MoveL`.
3. **Escritura de los nombres:** la función `dibujar_nombres()` ejecuta cada contorno, realizando una aproximación, un descenso a la superficie, el trazado y una retirada.
4. **Transición entre contornos:** el robot se retira de la superficie antes de iniciar un nuevo contorno, evitando dibujar conexiones entre letras.
5. **Retorno:** después de completar las trayectorias, el robot regresa a `Target_Aprox` y posteriormente a `Target_Home`.

Durante el trazado se utiliza una velocidad de **30 mm/s** y se configura `setRounding(0)` para mantener el seguimiento de los puntos programados sin redondeo de trayectoria.




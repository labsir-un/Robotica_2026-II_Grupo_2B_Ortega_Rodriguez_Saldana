### Laboratorio 2.

## 1. Cuadro Comparativo

Los robots industriales **Motoman MH6**, fabricado por Yaskawa, y **IRB 140**, fabricado por ABB, son manipuladores seriales antropomórficos de seis grados de libertad. Ambos están diseñados para aplicaciones de automatización industrial, aunque presentan diferencias importantes en alcance, velocidad, precisión y dimensiones.

### Características técnicas generales

| Característica | Yaskawa Motoman MH6 | ABB IRB 140 |
|---|---|---|
| Fabricante | Yaskawa Motoman | ABB Robotics |
| Modelo | MH6 | IRB 140-6/0.8 |
| Tipo de robot | Manipulador industrial articulado | Manipulador industrial articulado |
| Configuración mecánica | Antropomórfica, 6 ejes rotacionales | Antropomórfica, 6 ejes rotacionales |
| Grados de libertad (GDL) | 6 | 6 |
| Carga útil máxima | 6 kg | 6 kg |
| Alcance horizontal máximo | 1422 mm | 810 mm |
| Alcance vertical máximo | 2486 mm | Depende de la configuración articular |
| Repetibilidad de posicionamiento | ±0.08 mm | ±0.03 mm |
| Peso aproximado del manipulador | 130 kg | 98 kg|
| Sistema de accionamiento | Servomotores eléctricos de CA | Servomotores eléctricos de CA |
| Tipo de articulaciones | 6 articulaciones rotacionales, más 2 ejes externos | 6 articulaciones rotacionales |
| Controlador | Motoman DX100 | ABB IRC5 |
| Lenguaje de programación | INFORM | RAPID |
| Interfaz de programación | Teach Pendant Motoman | FlexPendant ABB |
| Simulador asociado | MotoSim EG-VRC | RobotStudio |
| Montaje | Suelo, invertido e inclinado | Suelo, pared e invertido |
| Aplicaciones típicas | Manipulación, soldadura, ensamblaje, empaquetado, alimentación de máquinas y dosificación | Manipulación, ensamblaje, soldadura, aplicación de adhesivos y operaciones de precisión |

### Velocidades articulares máximas

Las velocidades se expresan en grados por segundo (°/s). Cada valor corresponde a la velocidad máxima de una articulación individual.

| Articulación | Motoman MH6 | ABB IRB 140 |
|---|---|---|
| Eje 1: Rotación de base | 220 °/s | 200 °/s |
| Eje 2: Hombro | 200 °/s | 200 °/s |
| Eje 3: Codo | 220 °/s | 260 °/s |
| Eje 4: Rotación de muñeca | 410 °/s | 360 °/s |
| Eje 5: Inclinación de muñeca | 410 °/s | 360 °/s |
| Eje 6: Rotación final | 610 °/s | 450 °/s |

**Nota:** Las velocidades articulares máximas no equivalen a la velocidad cartesiana del TCP. La velocidad real del efector final depende de la configuración cinemática, las articulaciones involucradas y las restricciones del controlador.

### Rangos de movimiento articular

| Articulación | Motoman MH6 | ABB IRB 140 |
|---|---|---|
| Eje 1 | -170° a +170° | Recorrido total de 360° |
| Eje 2 | -90° a +155° | Recorrido total de 200° |
| Eje 3 | -175° a +250° | Recorrido total de 280° |
| Eje 4 | -180° a +180° | Rotación continua; límite configurable |
| Eje 5 | -45° a +225° | Recorrido total de 230° |
| Eje 6 | -360° a +360° | Rotación continua; límite configurable |

**Nota:** Los rangos del ABB se presentan como recorridos angulares totales cuando corresponde, no como límites simétricos respecto a cero. Los límites efectivos dependen de la versión y configuración del robot.

### Sistemas de control y programación

| Característica | Motoman MH6 | ABB IRB 140 |
|---|---|---|
| Controlador considerado | DX100 | IRC5 |
| Lenguaje nativo | INFORM | RAPID |
| Programación manual | Teach Pendant | FlexPendant |
| Movimiento articular | MOVJ | MoveAbsJ / MoveJ |
| Movimiento lineal | MOVL | MoveL |
| Movimiento circular | MOVC | MoveC |
| Gestión de entradas y salidas | Instrucciones INFORM y configuración de I/O | Instrucciones RAPID y configuración de I/O |
| Integración con sensores | Mediante interfaces y módulos compatibles | Mediante interfaces y módulos compatibles |
| Simulación y programación offline | MotoSim, RoboDK | RobotStudio, RoboDK |

## 2. Configuraciones Home
## 3. Tipos de Movimiento
## 4. Niveles de Velocidad 


## Selección de velocidad para movimientos manuales

El robot **Motoman MH6**, mediante su controlador **DX100**, permite ajustar la velocidad de desplazamiento durante la operación manual desde el *Teach Pendant*. 

El controlador dispone de **cuatro niveles de velocidad manual**, que permiten adaptar el movimiento del robot según la precisión y rapidez requeridas.

### 1. Niveles de velocidad manual

Los niveles disponibles son los siguientes:

| Nivel | Identificador | Descripción | Aplicación |
|---|:---:|---|---|
| **Inching** | `I` | Movimiento incremental de muy corta distancia por accionamiento de la tecla. | Ajustes finos y posicionamiento de alta precisión. |
| **Low Speed** | `L` | Movimiento continuo a baja velocidad mientras se mantiene presionada la tecla correspondiente. | Aproximación cuidadosa a piezas, herramientas u obstáculos. |
| **Medium Speed** | `M` | Movimiento continuo a velocidad intermedia. | Posicionamiento general y desplazamientos dentro del espacio de trabajo. |
| **High Speed** | `H` | Movimiento continuo a la velocidad manual más alta disponible. | Desplazamientos amplios en zonas libres de obstáculos. |

![Selección de velocidad manual](ruta/de/la/imagen_velocidad_manual.png)

**Figura 1.** Niveles de velocidad manual y teclas de selección `FAST` y `SLOW` del controlador DX100.

#### Consideraciones importantes

- **Inching (I):** a diferencia de los otros niveles, está orientado a realizar pequeños incrementos de posición, lo que facilita el ajuste fino del manipulador.
- **Low (L):** permite realizar movimientos lentos y controlados, especialmente útiles cuando el robot se encuentra cerca de objetos.
- **Medium (M):** ofrece una velocidad intermedia para desplazamientos habituales durante la programación manual.
- **High (H):** permite efectuar desplazamientos manuales más rápidos, siempre respetando las restricciones de seguridad del controlador.

### 2. Procedimiento para cambiar el nivel de velocidad

La selección de velocidad manual se realiza directamente mediante las teclas **MANUAL SPEED**, ubicadas en el *Teach Pendant*.

Estas teclas están identificadas como:

- **FAST (▲):** aumenta el nivel de velocidad manual.
- **SLOW (▼):** disminuye el nivel de velocidad manual.

El procedimiento consiste en:

1. Colocar el controlador en modo **TEACH** para habilitar la operación manual.
2. Verificar el nivel de velocidad actualmente seleccionado en el área de estado de la pantalla.
3. Presionar la tecla `FAST` para aumentar la velocidad o `SLOW` para disminuirla.
4. Observar cómo cambia el indicador de velocidad en la interfaz.
5. Seleccionar el nivel apropiado antes de ejecutar cualquier movimiento manual mediante las teclas de desplazamiento de los ejes.

Durante la selección, el robot no necesita estar en movimiento; el cambio se refleja directamente en el indicador de velocidad del controlador.

### 3. Identificación de la velocidad en la interfaz

El controlador DX100 dispone de un **área de estado** ubicada en la parte superior de la pantalla del *Teach Pendant*. Esta sección muestra diferentes indicadores relacionados con el funcionamiento del robot.

Entre ellos se encuentra el indicador de **velocidad manual**, identificado con la letra `C` en el esquema de la Figura 2.

![Área de estado del controlador DX100](ruta/de/la/imagen_area_estado.png)

**Figura 2.** Área de estado del controlador DX100. El elemento `C` corresponde al indicador de velocidad manual.

El indicador muestra el nivel seleccionado mediante una letra.

De esta manera, el operador puede comprobar visualmente la velocidad configurada antes y durante la ejecución de movimientos manuales.

### 4. Relación entre la velocidad y el tipo de movimiento

La velocidad manual seleccionada se utiliza durante el desplazamiento del robot mediante las teclas de operación del *Teach Pendant*.

Su efecto depende del sistema de coordenadas seleccionado:

| Sistema de movimiento | Comportamiento |
|---|---|
| **Joint** | Permite mover individualmente las articulaciones del robot. |
| **Robot / Cartesian** | Permite desplazar el TCP respecto al sistema de referencia del robot. |
| **Tool** | Permite desplazar el TCP respecto al sistema de coordenadas de la herramienta. |
| **User** | Permite desplazar el TCP respecto a un sistema de coordenadas definido por el usuario. |

En todos los casos, el nivel seleccionado determina la rapidez del desplazamiento manual, sujeto a las limitaciones del sistema.


## 5. Funciones ROBOTDK
## 6. ROBOTDK vs RobotStudio
## 7. Diagrama de Flujo
## 8. Plano de Planta
## 9. Rutina
### Referencias

1. Yaskawa Motoman. *MOTOMAN-MH6 Instructions*. Manual de especificaciones y operación del manipulador.
2. Yaskawa Motoman. *MH6/MH6S Technical Specifications*.
3. ABB Robotics. *Product Manual - IRB 140*. Documento 3HAC027400-001, revisión AA, 2024.
4. ABB Robotics. *Product Specification - IRB 140*. Documento 3HAC041346-001.
5. Yaskawa Motoman. *DX100 - Manual de instrucciones y programación básica*.

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
| Tipo de articulaciones | 6 articulaciones rotacionales | 6 articulaciones rotacionales |
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
| Simulación y programación offline | MotoSim | RobotStudio |

### Análisis comparativo

**Capacidad de carga:** Ambos manipuladores presentan una carga útil nominal de 6 kg, lo cual permite desarrollar aplicaciones de manipulación de piezas pequeñas, ensamblaje y automatización ligera.

**Alcance:** El Motoman MH6 ofrece un alcance horizontal considerablemente mayor (1422 mm frente a 810 mm), por lo que resulta más adecuado para tareas que necesitan cubrir un espacio de trabajo amplio.

**Precisión:** El ABB IRB 140 presenta una mejor repetibilidad nominal (±0.03 mm frente a ±0.08 mm), característica favorable para tareas que requieren posicionamientos repetitivos de alta precisión.

**Velocidad:** El Motoman MH6 alcanza mayores velocidades en los ejes 1, 4, 5 y 6, mientras que el ABB IRB 140 presenta una mayor velocidad máxima en el eje 3. No obstante, estos valores no permiten determinar directamente cuál robot completa una tarea más rápido.

**Dimensiones:** El ABB IRB 140 presenta una estructura más compacta y menor masa, lo que facilita su instalación en celdas robotizadas con restricciones de espacio.

**Programación:** Los dos robots permiten implementar trayectorias articulares, lineales y circulares. Sin embargo, utilizan entornos diferentes: INFORM en el Motoman MH6 y RAPID en el ABB IRB 140.

### Referencias

1. Yaskawa Motoman. *MOTOMAN-MH6 Instructions*. Manual de especificaciones y operación del manipulador.
2. Yaskawa Motoman. *MH6/MH6S Technical Specifications*.
3. ABB Robotics. *Product Manual - IRB 140*. Documento 3HAC027400-001, revisión AA, 2024.
4. ABB Robotics. *Product Specification - IRB 140*. Documento 3HAC041346-001.
5. Yaskawa Motoman. *DX100 - Manual de instrucciones y programación básica*.


## 2. Configuraciones Home
## 3. Tipos de Movimiento
## 4. Niveles de Velocidad 
## 5. Funciones ROBOTDK
## 6. ROBOTDK vs RobotStudio
## 7. Diagrama de Flujo
## 8. Plano de Planta
## 9. Rutina

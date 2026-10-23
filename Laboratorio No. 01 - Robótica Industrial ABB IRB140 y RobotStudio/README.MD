# Análisis del Código. Laboratorio 1.

A continuación se abordará con más detalle el código **RAPID** desarrollado por nuestro equipo. 

## 1. Arquitectura general del programa

La programación se encuentra contenida en el módulo RAPID `Module1`, que agrupa las declaraciones de datos, las posiciones objetivo y los procedimientos utilizados durante la ejecución.

El programa está organizado en cuatro componentes principales:

| Componente | Descripción |
|---|---|
| Declaración de datos | Definición de herramienta, objeto de trabajo y posiciones objetivo. |
| `main()` | Procedimiento principal que supervisa las entradas digitales y selecciona la rutina correspondiente. |
| Procedimientos de trayectoria | Rutinas que ejecutan los movimientos necesarios para escribir caracteres y dibujar la figura decorativa. |
| Procedimientos auxiliares | Rutinas de mantenimiento, movimiento de demostración y posicionamiento del robot. |

El sistema utiliza un ciclo de ejecución continuo mediante la estructura `WHILE TRUE`, que permite evaluar repetidamente las señales de entrada y seleccionar el modo de operación solicitado.

La lógica de selección está implementada mediante instrucciones condicionales `IF` y `ELSEIF`, estableciendo un orden de evaluación entre las diferentes entradas digitales.

---

## 3. Configuración de la herramienta y sistema de referencia

### 3.1. Herramienta de trabajo — `Tool_Cuy`

El programa utiliza una herramienta definida mediante la variable persistente `Tool_Cuy`, de tipo `tooldata`.

Esta estructura contiene información relativa a la geometría y las propiedades de la herramienta utilizada para realizar el proceso de decoración.

Entre sus parámetros se encuentran:

- La posición y orientación del TCP (*Tool Center Point*) respecto al sistema de montaje de la herramienta.
- La masa de la herramienta.
- La posición de su centro de gravedad.
- Los parámetros de inercia utilizados en su definición.

El TCP establece el punto de referencia que RobotStudio utiliza para calcular la posición y orientación del extremo de la herramienta durante los movimientos programados.

### 3.2. Objeto de trabajo — `Workobject_1`

El sistema de coordenadas `Workobject_1`, definido mediante una variable persistente de tipo `wobjdata`, representa la referencia espacial utilizada para ejecutar las trayectorias de decoración.

Este sistema permite expresar las posiciones de los caracteres y de la figura decorativa respecto a una referencia asociada a la superficie de trabajo, en lugar de definir todos los movimientos directamente respecto a la base del robot.

La configuración del objeto de trabajo facilita la organización geométrica de las trayectorias y permite ajustar su ubicación mediante la modificación de la referencia correspondiente.

Durante el posicionamiento general se utiliza también `wobj0`, correspondiente al sistema de referencia global del controlador.

---

## 4. Sistema de entradas y salidas digitales

La lógica de control se fundamenta en señales digitales que permiten seleccionar los modos de operación y gestionar determinadas acciones de la celda.

### 4.1. Entradas digitales

| Señal | Modo de operación | Función |
|---|---|---|
| `DI_01` | Ciclo automático | Inicia la secuencia de transporte y decoración del pastel. |
| `DI_02` | Mantenimiento | Ejecuta una rutina para posicionar el robot en una configuración de mantenimiento. |
| `DI_03` | Farmear Aura | Ejecuta una secuencia predefinida de movimientos articulares. |

Las señales son evaluadas desde el procedimiento principal. Cuando una entrada cumple la condición correspondiente, se invoca el procedimiento asociado.

**Prioridad de las señales:** debido al orden de las condiciones, `DI_01` tiene prioridad sobre las demás entradas. Si `DI_01` está activa, el programa ejecuta el ciclo automático, independientemente del estado de `DI_02` o `DI_03`.

Cuando `DI_01` está desactivada, se evalúa `DI_03` antes de `DI_02`.

### 4.2. Salidas digitales

| Señal | Función |
|---|---|
| FWD_Conveyor | Orden que determina el sentido de giro de la banda. |
| BWD_Conveyor | Orden inicia o detiene l movimiento de la banda. |
| `DO_01` | Indicador digital asociado a la ejecución de la rutina de decoración. |

Las salidas se controlan mediante las instrucciones RAPID `SET` y `RESET`, que establecen sus estados lógicos en 1 y 0, respectivamente.

La salida `DO_01` se activa antes de ejecutar `EscribirNombres()` y se desactiva una vez finalizado dicho procedimiento.

---

## 5. Procedimiento principal — `main()`

El procedimiento `main()` constituye el núcleo de supervisión del sistema robotizado.

Al iniciar su ejecución, el programa activa la salida `FWD_Conveyor`. Posteriormente, ingresa en un ciclo infinito que supervisa continuamente las entradas digitales y determina qué rutina debe ejecutarse.

La lógica del programa se organiza de acuerdo con las siguientes condiciones:

| Condición | Acción ejecutada |
|---|---|
| `DI_01 = 1` | Ejecutar el ciclo automático de transporte y decoración. |
| `DI_01 = 1 AND DI_02 = 1` | Bloque programado para un accionamiento adicional de la banda. |
| `DI_03 = 1` | Ejecutar `FarmearAura()` y esperar la desactivación de `DI_03`. |
| `DI_02 = 1` | Ejecutar `Mantenimiento()` y esperar la desactivación de `DI_02`. |
| Ninguna condición activa | Esperar 0,05 segundos antes de volver a evaluar las entradas. |

La utilización de un ciclo `WHILE TRUE` permite mantener el programa activo durante la operación de la celda, sin necesidad de reiniciarlo para seleccionar una rutina diferente.

Las rutinas se ejecutan de forma secuencial. Por lo tanto, una vez iniciado un procedimiento de movimiento, el programa principal no vuelve a evaluar las condiciones hasta que este termina o alcanza una instrucción de espera.

---

## 6. Modo de operación 1 — Ciclo automático de transporte y decoración

**Entrada de activación:** `DI_01`

**Procedimiento principal de movimiento:** `EscribirNombres()`

Este modo integra el funcionamiento de la banda transportadora con las trayectorias de decoración ejecutadas por el robot ABB IRB 140.

La secuencia implementada se divide en tres etapas: transporte inicial, decoración y transporte de salida.

### 6.1. Transporte inicial del pastel

Cuando se detecta `DI_01 = 1`, el controlador activa la salida `BWD_Conveyor`, que permanece activa durante 3 segundos.

Transcurrido este intervalo, el programa desactiva dicha salida y ejecuta una pausa adicional de 0,5 segundos antes de comenzar la decoración.

Este intervalo representa la etapa de transporte y posicionamiento temporal del producto dentro de la celda.

En la implementación analizada, el avance de la banda se controla mediante tiempos predefinidos, sin que el código incluya una condición de detección del pastel mediante sensores de posición.

### 6.2. Activación de la decoración

Después de la pausa, el controlador activa la salida `DO_01`, utilizada como indicador del estado de decoración.

Posteriormente, se invoca el procedimiento `EscribirNombres()`, encargado de ejecutar las trayectorias que forman los caracteres y la figura decorativa.

Durante esta etapa, el robot realiza una secuencia de movimientos programados que combinan posicionamientos articulares, desplazamientos lineales y trayectorias circulares.

Al finalizar la rutina, se desactiva `DO_01`.

### 6.3. Transporte de salida

Una vez completada la decoración, el programa activa nuevamente `BWD_Conveyor` durante 2 segundos, con el objetivo de transportar el pastel decorado hacia la etapa posterior del proceso.

Al finalizar el tiempo programado, la señal se desactiva.

El ciclo automático concluye y el programa retorna a la evaluación de las entradas digitales dentro de `main()`.

### 6.4. Resumen de la secuencia

| Etapa | Acción | Señal o procedimiento | Duración |
|---|---|---|---|
| 1 | Recepción de la orden | `DI_01 = 1` | Según activación |
| 2 | Transporte inicial | `SET BWD_Conveyor` | 3 s |
| 3 | Detención de la orden de transporte | `RESET BWD_Conveyor` | — |
| 4 | Pausa previa | `WaitTime` | 0,5 s |
| 5 | Activación del indicador | `SET DO_01` | — |
| 6 | Ejecución de la decoración | `EscribirNombres()` | Según trayectorias |
| 7 | Desactivación del indicador | `RESET DO_01` | — |
| 8 | Transporte de salida | `SET BWD_Conveyor` | 2 s |
| 9 | Finalización del transporte | `RESET BWD_Conveyor` | — |

El tiempo total de espera y transporte programado es de **5,5 segundos**, sin incluir la duración de las trayectorias de decoración.

---

## 7. Procedimiento de decoración — `EscribirNombres()`

El procedimiento `EscribirNombres()` organiza la secuencia completa de escritura y dibujo del robot.

Su implementación utiliza una arquitectura modular, en la que cada letra o elemento gráfico se desarrolla mediante un procedimiento RAPID independiente.

Esta organización permite modificar una trayectoria específica sin necesidad de reestructurar el procedimiento principal.

### 7.1. Posicionamiento inicial

La rutina comienza ejecutando dos procedimientos:

- **`Path_Home()`**: desplaza el robot hacia una posición de referencia definida mediante `Target_Home`.
- **`Path_Aprox()`**: ejecuta los movimientos de aproximación mediante `Target_Aprox` y `Target_Aprox_2`, preparando el robot para iniciar la decoración.

Estos movimientos permiten establecer una secuencia de acceso a la superficie de trabajo antes de comenzar la escritura.

### 7.2. Escritura de los nombres

El programa desarrolla las letras que conforman los nombres de los integrantes mediante procedimientos individuales.

La secuencia de escritura está organizada de la siguiente manera:

| Secuencia | Procedimientos | Resultado |
|---|---|---|
| Primer nombre | `Path_J`, `Path_U`, `Path_A`, `Path_N` | JUAN |
| Separación | `Path_S`, `Path_Doth_1` | Espacio o separación programada |
| Segundo nombre | `Path_Y`, `Path_E`, `Path_I`, `Path_S_2`, `Path_O`, `Path_N_2` | YEISON |
| Separación | `Path_O_2`, `Path_Doth_2` | Transición entre grupos de caracteres |
| Tercer nombre | `Path_D`, `Path_A_2`, `Path_N_3`, `Path_I_2`, `Path_E_2`, `Path_L`, `Path_R` | DANIEL y procedimiento adicional `Path_R` |
| Transición final | `Path_Doth_3` | Posicionamiento previo a la figura |

Cada procedimiento contiene una secuencia de posiciones objetivo que define la geometría del trazo correspondiente.

Los nombres de los procedimientos y su orden de ejecución se encuentran establecidos directamente en `EscribirNombres()`.

### 7.3. Figura decorativa del cuy

Una vez finalizada la secuencia de escritura, el robot ejecuta cuatro procedimientos adicionales destinados a generar una figura decorativa.

| Procedimiento | Función |
|---|---|
| `Path_Cuy_Externo()` | Generación del contorno exterior de la figura. |
| `Path_Cuy_Interno()` | Generación de elementos interiores de la figura. |
| `Path_Oreja()` | Trazado del detalle correspondiente a la oreja. |
| `Path_Ojo()` | Trazado del ojo mediante segmentos circulares. |

Estas rutinas utilizan principalmente interpolaciones lineales y circulares, permitiendo representar contornos y curvas mediante movimientos continuos del extremo de la herramienta.

### 7.4. Retorno a HOME

Al completar la decoración, el procedimiento ejecuta nuevamente `Path_Home()`.

De esta manera, la rutina de escritura comienza y termina con un movimiento hacia la posición de referencia establecida.

---

## 8. Tipos de movimiento utilizados

Las trayectorias del proyecto utilizan diferentes instrucciones de movimiento RAPID según las necesidades geométricas y funcionales de cada operación.

| Instrucción | Tipo de movimiento | Aplicación |
|---|---|---|
| `MoveJ` | Movimiento articular hacia una posición cartesiana | Aproximación, posicionamiento y transiciones entre trayectorias. |
| `MoveL` | Movimiento lineal del TCP | Escritura de segmentos rectos. |
| `MoveC` | Movimiento circular del TCP | Generación de curvas, contornos y detalles decorativos. |
| `MoveAbsJ` | Movimiento a una configuración articular absoluta | Rutinas de mantenimiento y Farmear Aura. |

### 8.1. Parámetros de movimiento

Las trayectorias de decoración emplean frecuentemente parámetros como:

- `v200`: velocidad programada de movimiento.
- `z10`: zona de aproximación que permite suavizar las transiciones entre posiciones.
- `Tool_Cuy`: herramienta utilizada para ejecutar los movimientos.
- `Workobject_1`: referencia espacial asociada a la superficie de decoración.

Algunas rutinas auxiliares utilizan velocidades diferentes, incluyendo `v400`, `v800` y `v1000`.

Asimismo, el parámetro `fine` se utiliza en posiciones específicas para exigir una llegada precisa al objetivo, sin utilizar una zona de paso suavizada.

### 8.2. Definición de posiciones

El programa emplea dos estructuras principales para definir los objetivos del robot.

**`robtarget`:** contiene la posición y orientación cartesianas del extremo de la herramienta, junto con la configuración del robot y la información de ejes externos.

**`jointtarget`:** contiene los valores articulares que definen directamente una configuración del robot.

La utilización de ambas estructuras permite combinar movimientos cartesianos para la decoración y movimientos articulares para las operaciones auxiliares.

---

## 9. Modo de operación 2 — Posición de mantenimiento

**Entrada de activación:** `DI_02`

**Procedimiento asociado:** `Mantenimiento()`

Este modo permite trasladar el robot hacia una configuración articular previamente definida para operaciones de mantenimiento o inspección.

La secuencia comienza mediante una llamada a `Path_Home()`, que posiciona el robot en la referencia inicial.

Posteriormente, se ejecuta un movimiento `MoveAbsJ` hacia la configuración `Mant_Aprox`, utilizando una velocidad programada de `v400` y el parámetro de precisión `fine`.

El objetivo es situar el manipulador en una configuración específica y reproducible, diferente de las posiciones utilizadas durante la decoración.

Una vez finalizada la rutina, el procedimiento principal espera hasta que `DI_02` se desactive, mediante `WaitDI DI_02,0`.

Esto evita que el modo se ejecute repetidamente mientras la entrada permanece activa.

**Consideración:** la rutina finaliza en `Mant_Aprox`; no incluye un retorno automático a HOME después de alcanzar la posición de mantenimiento.

---

## 10. Modo de operación 3 — Farmear Aura

**Entrada de activación:** `DI_03`

**Procedimiento asociado:** `FarmearAura()`

Esta rutina implementa una secuencia demostrativa de movimientos articulares del manipulador ABB IRB 140.

Su propósito es explorar el comportamiento cinemático del robot mediante diferentes configuraciones y velocidades de movimiento.

La secuencia se encuentra estructurada en cinco etapas principales.

### 10.1. Posicionamiento inicial

El robot ejecuta `Path_Home()` y posteriormente se desplaza hacia la configuración `Aura_Vertical`, definida mediante un objetivo articular absoluto.

### 10.2. Apertura y giro

Se realizan movimientos hacia las posiciones `Aura_Abre_Der` y `Aura_Giro_Der`, seguidos de movimientos hacia `Aura_Abre_Izq` y `Aura_Giro_Izq`.

Estas configuraciones generan una secuencia alternada de apertura y rotación del manipulador.

### 10.3. Repetición de giros

El robot repite desplazamientos entre las posiciones de giro derecha e izquierda, utilizando velocidades programadas de movimiento.

### 10.4. Cierre y saludo

La secuencia continúa hacia `Aura_Abre_Der` y `Aura_Vertical`, para luego ejecutar una serie de movimientos de saludo mediante las posiciones:

`Aura_Saludo_1`, `Aura_Saludo_2`, `Aura_Saludo_3`, `Aura_Saludo_4`, `Aura_Saludo_5`, `Aura_Saludo_6` y `Aura_Saludo_Fin`.

### 10.5. Retorno a HOME

La rutina concluye mediante una llamada a `Path_Home()`.

Posteriormente, el procedimiento principal espera la desactivación de `DI_03`, evitando repetir automáticamente la secuencia mientras la entrada permanezca activa.

---

## 11. Consideraciones técnicas de la implementación

La programación desarrollada permite integrar movimientos industriales, trayectorias complejas y selección de modos mediante señales digitales. Sin embargo, es importante distinguir las funciones implementadas de aquellas que podrían incorporarse en versiones posteriores.

### 11.1. Control temporal de la banda

La secuencia automática utiliza tiempos fijos para controlar las etapas de transporte.

Los intervalos empleados son:

- Transporte inicial: 3 segundos.
- Pausa previa a la decoración: 0,5 segundos.
- Transporte de salida: 2 segundos.

La implementación no verifica mediante sensores la llegada del pastel a la zona de trabajo ni su salida de la banda.

### 11.2. Control de señales de transporte

La salida `FWD_Conveyor` se activa al iniciar `main()`, mientras que el ciclo de decoración activa y desactiva `BWD_Conveyor`.

En la implementación actual, no se desactiva explícitamente `FWD_Conveyor` antes de accionar `BWD_Conveyor` durante la rutina normal.

Es necesario revisar el comportamiento de ambas señales dentro de la lógica de la estación, especialmente si controlan direcciones opuestas de un mismo transportador.

### 11.3. Condición combinada de entradas

El programa incluye una condición destinada a evaluar simultáneamente `DI_01 = 1` y `DI_02 = 1`.

Dicho bloque contiene una orden de desactivación de `FWD_Conveyor`, seguida de la activación de `BWD_Conveyor` durante 5,5 segundos.

Sin embargo, debido al orden de las condiciones `IF` y `ELSEIF`, este bloque no resulta alcanzable durante la ejecución normal: cualquier activación de `DI_01` es atendida primero por el ciclo automático de decoración.

### 11.4. Repetición del ciclo automático

A diferencia de las rutinas de mantenimiento y Farmear Aura, el modo de decoración no contiene una instrucción `WaitDI` para esperar la desactivación de `DI_01`.

Por tanto, si dicha entrada permanece activa al finalizar el ciclo, el programa puede comenzar nuevamente la secuencia de transporte y decoración.

### 11.5. Posibles desarrollos futuros

Como ampliaciones del proyecto, se consideran:

- Implementación de sensores para detectar la presencia y posición del pastel.
- Incorporación de condiciones de enclavamiento para las señales de movimiento de la banda.
- Implementación de indicadores de estado independientes para cada modo de operación.
- Incorporación de una condición de rearme para el ciclo automático.
- Definición de estados de fallo y recuperación ante interrupciones.
- Implementación de una interfaz de supervisión para seleccionar y visualizar los modos de operación.

Estas funciones corresponden a oportunidades de mejora y no deben interpretarse como características ya implementadas en el código actual.

---

## 12. Conclusiones

El programa RAPID desarrollado permite simular una celda robotizada capaz de ejecutar trayectorias de decoración, controlar señales digitales asociadas al transporte y seleccionar distintas rutinas de operación.

La división en procedimientos independientes favorece la organización del código, su mantenimiento y la reutilización de trayectorias, mientras que el uso de referencias `tooldata` y `wobjdata` permite relacionar los movimientos programados con la configuración geométrica de la celda.

La implementación de `MoveJ`, `MoveL`, `MoveC` y `MoveAbsJ` permite abordar diferentes tipos de movimiento y comprender su aplicación dentro de una tarea de automatización industrial.

Finalmente, el proyecto constituye una base para desarrollar estrategias de integración más avanzadas entre robots industriales, sistemas transportadores y dispositivos de control, incorporando posteriormente sensores, enclavamientos y mecanismos de supervisión.

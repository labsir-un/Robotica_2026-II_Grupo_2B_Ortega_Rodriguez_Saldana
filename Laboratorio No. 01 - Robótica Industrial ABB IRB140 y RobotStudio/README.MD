Laboratorio 1.

A continuación se abordará con más detalle el código **RAPID** desarrollado por nuestro equipo. Para observar el resultado final del laboratorio y su implementación en el robot real, lo invitamos a visitar el siguiente link: [LabSIR UNAL](https://www.youtube.com/watch?v=dCyNcPcHMXA)

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

## 2. Configuración de la herramienta y sistema de referencia

### 2.1. Herramienta de trabajo — `Tool_Cuy`

El programa utiliza una herramienta definida mediante la variable persistente `Tool_Cuy`, de tipo `tooldata`.

Esta estructura contiene información relativa a la geometría y las propiedades de la herramienta utilizada para realizar el proceso de decoración.

Entre sus parámetros se encuentran:

- La posición y orientación del TCP (*Tool Center Point*) respecto al sistema de montaje de la herramienta.
- La masa de la herramienta.
- La posición de su centro de gravedad.
- Los parámetros de inercia utilizados en su definición.

El TCP establece el punto de referencia que RobotStudio utiliza para calcular la posición y orientación del extremo de la herramienta durante los movimientos programados.

### 2.2 Calibración de la Herramienta
# Calibración de la herramienta

Para definir el sistema de coordenadas de la herramienta (*Tool Center Point*, TCP) del manipulador ABB IRB 140, se realizaron dos procedimientos: una definición geométrica ideal mediante RobotStudio y una calibración experimental utilizando el robot físico.

En RobotStudio, el sistema de referencia se ubicó directamente en la punta del marcador, considerando su geometría nominal. Por otra parte, en el robot físico se empleó el **método de calibración de cuatro puntos**, que consiste en posicionar la punta de la herramienta sobre un punto fijo de referencia, modificando la orientación del manipulador durante cada medición.

A continuación, se presentan los sistemas de referencia obtenidos mediante ambos procedimientos.

**Figura 1. Sistema de referencia de la herramienta.**

![Sistema de referencia de la herramienta](https://github.com/user-attachments/assets/7bdb2436-1d77-4fa4-aee6-1487374a00e8)

**Figura 2. Comparación de los sistemas de referencia.**

![Comparación de los marcos de referencia](https://github.com/user-attachments/assets/e71ad511-9fef-41e4-be3a-5883f83ad8f0)

Como se observa en las imágenes, existe un desfase entre los sistemas de referencia definidos. Esta diferencia puede asociarse a las condiciones reales de montaje de la herramienta, las aproximaciones realizadas durante la calibración física y las simplificaciones geométricas consideradas en el modelo virtual.

## Comparación de los parámetros de calibración

Los parámetros de posición y orientación de cada TCP se encuentran definidos mediante estructuras `tooldata` en el lenguaje RAPID.

**TCP ideal — RobotStudio**

```rapid
PERS tooldata Tool_Cuy:=
[TRUE, [[59.512,0,113],[0.866025404,0,0.5,0]],[1,[0,0,1],[1,0,0,0],0,0,0]];
```

**TCP experimental — Robot físico**
```rapid
TASK PERS tooldata tool_acer:=
[TRUE,[[63.9211,0.528303,120.581],[1,0,0,0]],[1,[0,0,0],[1,0,0,0],0,0,0]];
```

A partir de estos parámetros es posible establecer una comparación de la posición de ambos TCP respecto a la brida del manipulador.

| Componente | TCP ideal (mm) | TCP físico (mm) | Diferencia (mm) |
|:---:|---:|---:|---:|
| X | 59.512 | 63.9211 | 4.4091 |
| Y | 0.000 | 0.5283 | 0.5283 |
| Z | 113.000 | 120.581 | 7.5810 |

La diferencia de posición entre los dos sistemas de referencia se calcula mediante la distancia euclidiana:

$$
e_p=\sqrt{(x_f-x_i)^2+(y_f-y_i)^2+(z_f-z_i)^2}
$$

Sustituyendo los valores registrados:

$$
e_p=\sqrt{4.4091^2+0.528303^2+7.581^2}
$$

$$
\boxed{e_p=8.7858\ \text{mm}}
$$

La diferencia de posición entre los dos sistemas de referencia **es de aproximadamente 8.79 mm**, cuya mayor contribución corresponde al eje Z.

Adicionalmente, se identifica una diferencia en las orientaciones definidas mediante los cuaterniones. El TCP ideal incorpora una rotación de 60° alrededor del eje Y, debido a que la geometría de la herramienta, importada desde el modelo CAD hacia RobotStudio, se posicionó inicialmente con respecto al sistema de referencia de origen del robot. Por esta razón, fue necesario aplicar una rotación que compensara la inclinación original de la herramienta en el modelo CAD, con el propósito de alinear los sistemas de referencia y conseguir que sus respectivos ejes Z fueran colineales. De esta manera, la orientación definida en el modelo virtual corresponde a un ajuste geométrico necesario para representar adecuadamente la disposición de la herramienta, y no necesariamente a un error de orientación asociado al procedimiento de calibración física.

En consecuencia, la comparación permite identificar las diferencias entre la configuración nominal y la experimental de la herramienta. Sin embargo, para determinar la precisión absoluta del TCP sería necesario realizar mediciones adicionales con una referencia metrológica independiente.

### 2.3. Objeto de trabajo — `Workobject_1`

El sistema de coordenadas `Workobject_1`, definido mediante una variable persistente de tipo `wobjdata`, representa la referencia espacial utilizada para ejecutar las trayectorias de decoración.

Este sistema permite expresar las posiciones de los caracteres y de la figura decorativa respecto a una referencia asociada a la superficie de trabajo, en lugar de definir todos los movimientos directamente respecto a la base del robot.

La configuración del objeto de trabajo facilita la organización geométrica de las trayectorias y permite ajustar su ubicación mediante la modificación de la referencia correspondiente.

Durante el posicionamiento general se utiliza también `wobj0`, correspondiente al objeto de trabajo predeterminado del controlador.

#### Ajuste del sistema de referencia a las condiciones físicas

Durante las pruebas experimentales con el manipulador físico, se identificó que la banda transportadora presentaba una inclinación aproximada de **4° respecto al plano de referencia inicialmente considerado**. Esta condición generaba una diferencia entre la superficie real de trabajo y el plano utilizado para definir las trayectorias de decoración.

Como consecuencia, al ejecutar las trayectorias sin compensar esta inclinación, el marcador no mantenía un contacto adecuado con la superficie, llegando a desplazarse por encima de ella sin realizar correctamente el trazado.

Para corregir este comportamiento, fue necesario ajustar la orientación del sistema `Workobject_1`, incorporando una rotación aproximada de **4° alrededor del eje Y**. Esta modificación permitió adaptar el plano de ejecución de las trayectorias a la inclinación física de la banda transportadora, favoreciendo que el TCP del marcador siguiera la superficie de trabajo durante la decoración.

De esta manera, la compensación se realizó directamente sobre el sistema de referencia de trabajo, sin necesidad de modificar individualmente los puntos que conforman las letras y figuras programadas.

Este ajuste evidencia la importancia de definir correctamente los sistemas de referencia durante la implementación física, ya que pequeñas diferencias de orientación pueden producir desviaciones significativas en aplicaciones que requieren contacto entre la herramienta y la superficie de trabajo.


### 2.4. Corrección de trayectoria

Durante las pruebas experimentales, después de corregir la inclinación del sistema de referencia `Workobject_1`, se identificó un problema adicional relacionado con los desplazamientos del manipulador entre las trayectorias de escritura.

Inicialmente, el robot ejecutaba correctamente la escritura del nombre **JUAN**. Sin embargo, al finalizar la última letra y desplazarse hacia el primer punto del nombre **YEISON**, se presentaba una interferencia entre el marcador y la superficie de trabajo (Esto pasaba en el cambio de línea de trabajo).  Debido a la separación existente entre ambos puntos, la trayectoria de desplazamiento permitía que la herramienta entrara en contacto con el tablero antes de alcanzar la posición inicial del siguiente nombre, generando una línea no deseada sobre la superficie.

Para solucionar este inconveniente, se incorporó un **punto intermedio de aproximación**, ubicado a una altura de seguridad respecto al plano de escritura. Su propósito era garantizar que el manipulador realizara el desplazamiento entre ambos nombres manteniendo el marcador separado de la superficie, antes de iniciar el descenso hacia el siguiente punto de escritura.

No obstante, durante la implementación de esta modificación se presentó un segundo inconveniente relacionado con la configuración articular del manipulador. Al definir el nuevo punto de aproximación, se utilizó inicialmente un vector de configuración diferente al establecido en los puntos originales de la trayectoria.

Esta inconsistencia provocó un movimiento brusco e inesperado durante la transición hacia el nuevo objetivo, ocasionando una presión excesiva sobre la herramienta y, finalmente, su fractura.

Tras identificar el problema, se corrigió el vector de configuración del nuevo punto para hacerlo consistente con el utilizado en las posiciones previamente programadas. La definición final del punto de aproximación fue:

```rapid
CONST robtarget Target_1020_3:=[[71.588911511,180.412,-49.878202511],[1,0,0,0],[-1,0,-1,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
```

En esta declaración, el vector `[-1,0,-1,1]` corresponde al parámetro `confdata` de RAPID, utilizado para identificar la configuración cinemática del manipulador asociada al objetivo. Su correcta definición resulta importante para conservar la coherencia entre las configuraciones articulares previstas durante la ejecución de las trayectorias.

Una vez corregida la configuración y verificada la trayectoria, se recuperó el funcionamiento esperado del desplazamiento entre ambos nombres. Debido al daño ocasionado, fue necesario fabricar nuevamente la herramienta mediante impresión 3D.

Esta experiencia permitió identificar dos aspectos fundamentales para la programación de trayectorias robóticas: **la importancia de establecer puntos de aproximación seguros para evitar contactos no deseados y la necesidad de verificar la coherencia de las configuraciones articulares entre los objetivos programados**.

Asimismo, se evidenció la importancia de validar las modificaciones de trayectoria en simulación y mediante pruebas controladas antes de ejecutar el programa a su velocidad normal, especialmente cuando se utilizan herramientas susceptibles a daños mecánicos.

### 2.5. Simulación de la banda transportadora mediante Smart Components

Con el propósito de representar el funcionamiento de la banda transportadora dentro del entorno virtual, se implementó un sistema de movimiento utilizando la herramienta **Smart Components** de RobotStudio. Esta funcionalidad permite integrar componentes de simulación, operaciones lógicas y señales digitales para reproducir el comportamiento de dispositivos externos al manipulador.

Para este proyecto, se desarrolló un componente encargado de simular el desplazamiento lineal del tablero sobre la banda transportadora, estableciendo una comunicación con las señales digitales del controlador virtual IRC5. De esta manera, el movimiento del tablero se encuentra sincronizado con la rutina de decoración programada en RAPID.

#### Integración del Smart Component con el controlador IRC5

Inicialmente, se creó el componente `SmartComponent_1` y se definieron dos entradas digitales asociadas al funcionamiento de la banda transportadora:

| Señal digital | Función |
|---|---|
| `BWD_Conveyor` | Habilita o deshabilita el movimiento de la banda transportadora. |
| `FWD_Conveyor` | Determina el sentido de desplazamiento: adelante cuando es 1 y atrás cuando es 0. |

Aunque la nomenclatura `BWD_Conveyor` hace referencia a *Backward*, en la implementación realizada esta señal se utiliza exclusivamente como habilitación del movimiento, mientras que `FWD_Conveyor` controla su dirección.

Para establecer la comunicación entre RAPID y el componente, se realizaron las conexiones de entrada y salida mediante la herramienta **Station Logic** de RobotStudio, vinculando las salidas digitales del controlador virtual `IRB140_6_81` con las entradas correspondientes de `SmartComponent_1`.

**Figura 3. Conexión de las señales digitales entre el controlador IRC5 y el Smart Component.**
<img width="613" height="174" alt="image" src="https://github.com/user-attachments/assets/13a48ae3-ec8e-4a1f-b1d0-cda2500ed9f8" />

Esta conexión permite que las instrucciones `Set` y `Reset` ejecutadas desde RAPID modifiquen directamente las entradas digitales del Smart Component y, en consecuencia, controlen el desplazamiento del tablero durante la simulación.

#### Implementación de la lógica de movimiento

Para representar el movimiento bidireccional de la banda transportadora, se incorporaron dos componentes `LinearMover`, encargados de desplazar el objeto `Tablero_cuy` en sentidos opuestos.

Los parámetros de configuración utilizados fueron:

| Parámetro | Movimiento hacia adelante | Movimiento hacia atrás |
|---|---|---|
| Componente | `Adelante` | `Atras` |
| Objeto | `Tablero_cuy` | `Tablero_cuy` |
| Dirección | `[1000, 0, 0]` | `[-1000, 0, 0]` |
| Velocidad | 300 mm/s | 300 mm/s |
| Referencia | Global | Global |

Adicionalmente, se implementó una estructura lógica compuesta por dos compuertas **AND** y una compuerta **NOT**. Su función es interpretar las señales digitales recibidas y activar exclusivamente el componente de movimiento correspondiente al sentido seleccionado.

**Figura 4. Configuración interna de los componentes de movimiento y las compuertas lógicas.**
<img width="1079" height="403" alt="image" src="https://github.com/user-attachments/assets/7f2188c1-5869-4062-a155-086a750d8b97" />

La lógica implementada responde a las siguientes expresiones booleanas:

**Movimiento hacia adelante:**

$$
M_A=BWD\_Conveyor\land FWD\_Conveyor
$$

**Movimiento hacia atrás:**

$$
M_R=BWD\_Conveyor\land\neg FWD\_Conveyor
$$

Donde \(M_A\) y \(M_R\) representan las señales de ejecución de los componentes `LinearMover` correspondientes.

A partir de estas condiciones, se obtiene la siguiente tabla de funcionamiento:

| BWD_Conveyor | FWD_Conveyor | Estado de la banda |
|:---:|:---:|---|
| 0 | 0 | Detenida |
| 0 | 1 | Detenida |
| 1 | 0 | Movimiento hacia atrás |
| 1 | 1 | Movimiento hacia adelante |

Esta configuración permite controlar el desplazamiento bidireccional utilizando únicamente dos señales digitales, evitando que ambos componentes de movimiento se ejecuten simultáneamente.

#### Sincronización con la rutina de decoración

Una vez configurada la lógica de movimiento, se integró su funcionamiento con el procedimiento `main()` del programa RAPID.

El ciclo automático de decoración, activado mediante la entrada digital `DI_01`, ejecuta una secuencia de transporte, posicionamiento, escritura y retirada del tablero.

La estructura principal implementada es la siguiente:

```rapid
! Establecer sentido hacia adelante
SET FWD_Conveyor;

! Activar transporte del tablero
SET BWD_Conveyor;
WaitTime 3;
RESET BWD_Conveyor;

! Estabilizacion del tablero
WaitTime 0.5;

! Activar indicador de decoracion
SET DO_01;

! Ejecutar trayectorias del manipulador
EscribirNombres;

! Desactivar indicador de decoracion
RESET DO_01;

! Retirar el tablero
SET BWD_Conveyor;
WaitTime 2;
RESET BWD_Conveyor;
```

En esta secuencia, la banda transportadora permanece activada durante **3 segundos**, permitiendo que el tablero alcance la zona de trabajo del manipulador. Posteriormente, el movimiento se detiene y se establece una espera de 0.5 segundos antes de iniciar la decoración.

Durante la ejecución de `EscribirNombres`, la banda permanece detenida para garantizar que las trayectorias del TCP se realicen sobre una superficie estacionaria.

Al finalizar la decoración, la señal `BWD_Conveyor` se activa nuevamente durante **2 segundos**, desplazando el tablero fuera de la zona de trabajo.

La señal `DO_01` se utiliza como indicador del estado de ejecución de la rutina de decoración.

De esta manera, se consigue una sincronización entre el movimiento del objeto transportado y las trayectorias programadas del manipulador, reproduciendo la secuencia de funcionamiento prevista para la estación.

#### Ajuste de la geometría de la banda transportadora

Como parte de la configuración final, se modificó la inclinación del tablero en el entorno virtual para reproducir la disposición de la superficie física, que presentaba una inclinación aproximada de **4°**.

Este ajuste permitió mejorar la correspondencia visual y geométrica entre el modelo de simulación y la estación real, complementando la corrección realizada previamente sobre el sistema de referencia `Workobject_1`.

De esta manera, la disposición del tablero y el plano de trabajo utilizado para las trayectorias de decoración mantienen una configuración coherente con las condiciones consideradas durante las pruebas experimentales.

#### Configuración de la posición inicial de simulación

Finalmente, se implementó un mecanismo para restablecer la posición inicial del tablero al reiniciar la simulación.

Debido a que los componentes `LinearMover` modifican la posición del objeto durante su ejecución, inicialmente era necesario reposicionar manualmente el tablero después de cada prueba.

Para corregir esta situación, se utilizó la funcionalidad de **estados guardados (*Saved States*)** de RobotStudio, registrando la posición y orientación iniciales del tablero y estableciendo dicho estado como referencia de inicio de la simulación.

Esta configuración permite recuperar la disposición inicial de la estación al restablecer la simulación, facilitando la repetición de las pruebas sin necesidad de intervenir manualmente sobre la geometría del tablero.

En conjunto, la implementación de Smart Components permitió integrar el movimiento de la banda transportadora con el controlador virtual, comprobar el funcionamiento de las señales digitales y reproducir de forma coordinada las etapas de transporte y decoración dentro del entorno de simulación.
## 3. Sistema de entradas y salidas digitales

La lógica de control se fundamenta en señales digitales que permiten seleccionar los modos de operación y gestionar determinadas acciones de la celda.

### 3.1. Entradas digitales

| Señal | Modo de operación | Función |
|---|---|---|
| `DI_01` | Ciclo automático | Inicia la secuencia de transporte y decoración del pastel. |
| `DI_02` | Mantenimiento | Ejecuta una rutina para posicionar el robot en una configuración de mantenimiento. |
| `DI_03` | Farmear Aura | Ejecuta una secuencia predefinida de movimientos articulares. |

Las señales son evaluadas desde el procedimiento principal. Cuando una entrada cumple la condición correspondiente, se invoca el procedimiento asociado.

**Prioridad de las señales:** debido al orden de las condiciones, `DI_01` tiene prioridad sobre las demás entradas. Si `DI_01` está activa, el programa ejecuta el ciclo automático, independientemente del estado de `DI_02` o `DI_03`.

Cuando `DI_01` está desactivada, se evalúa `DI_03` antes de `DI_02`.

### 3.2. Salidas digitales

| Señal | Función |
|---|---|
| FWD_Conveyor | Orden que determina el sentido de giro de la banda. |
| BWD_Conveyor | Orden inicia o detiene l movimiento de la banda. |
| `DO_01` | Indicador digital asociado a la ejecución de la rutina de decoración. |

Las salidas se controlan mediante las instrucciones RAPID `SET` y `RESET`, que establecen sus estados lógicos en 1 y 0, respectivamente.

La salida `DO_01` se activa antes de ejecutar `EscribirNombres()` y se desactiva una vez finalizado dicho procedimiento.

---

## 4. Procedimiento principal — `main()`

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

## 5. Modo de operación 1 — Ciclo automático de transporte y decoración

**Entrada de activación:** `DI_01`

**Procedimiento principal de movimiento:** `EscribirNombres()`

Este modo integra el funcionamiento de la banda transportadora con las trayectorias de decoración ejecutadas por el robot ABB IRB 140.

La secuencia implementada se divide en tres etapas: transporte inicial, decoración y transporte de salida.

### 5.1. Transporte inicial del pastel

Cuando se detecta `DI_01 = 1`, el controlador activa la salida `BWD_Conveyor`, que permanece activa durante 3 segundos.

Transcurrido este intervalo, el programa desactiva dicha salida y ejecuta una pausa adicional de 0,5 segundos antes de comenzar la decoración.

Este intervalo representa la etapa de transporte y posicionamiento temporal del producto dentro de la celda.

En la implementación analizada, el avance de la banda se controla mediante tiempos predefinidos, sin que el código incluya una condición de detección del pastel mediante sensores de posición.

### 5.2. Activación de la decoración

Después de la pausa, el controlador activa la salida `DO_01`, utilizada como indicador del estado de decoración.

Posteriormente, se invoca el procedimiento `EscribirNombres()`, encargado de ejecutar las trayectorias que forman los caracteres y la figura decorativa.

Durante esta etapa, el robot realiza una secuencia de movimientos programados que combinan posicionamientos articulares, desplazamientos lineales y trayectorias circulares.

Al finalizar la rutina, se desactiva `DO_01`.

### 5.3. Transporte de salida

Una vez completada la decoración, el programa activa nuevamente `BWD_Conveyor` durante 2 segundos, con el objetivo de transportar el pastel decorado hacia la etapa posterior del proceso.

Al finalizar el tiempo programado, la señal se desactiva.

El ciclo automático concluye y el programa retorna a la evaluación de las entradas digitales dentro de `main()`.

### 5.4. Resumen de la secuencia

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

## 6. Procedimiento de decoración — `EscribirNombres()`

El procedimiento `EscribirNombres()` organiza la secuencia completa de escritura y dibujo del robot.

Su implementación utiliza una arquitectura modular, en la que cada letra o elemento gráfico se desarrolla mediante un procedimiento RAPID independiente.

Esta organización permite modificar una trayectoria específica sin necesidad de reestructurar el procedimiento principal.

### 6.1. Posicionamiento inicial

La rutina comienza ejecutando dos procedimientos:

- **`Path_Home()`**: desplaza el robot hacia una posición de referencia definida mediante `Target_Home`.
- **`Path_Aprox()`**: ejecuta los movimientos de aproximación mediante `Target_Aprox` y `Target_Aprox_2`, preparando el robot para iniciar la decoración.

Estos movimientos permiten establecer una secuencia de acceso a la superficie de trabajo antes de comenzar la escritura.

### 6.2. Escritura de los nombres

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

### 6.3. Figura decorativa del cuy

Una vez finalizada la secuencia de escritura, el robot ejecuta cuatro procedimientos adicionales destinados a generar una figura decorativa.

| Procedimiento | Función |
|---|---|
| `Path_Cuy_Externo()` | Generación del contorno exterior de la figura. |
| `Path_Cuy_Interno()` | Generación de elementos interiores de la figura. |
| `Path_Oreja()` | Trazado del detalle correspondiente a la oreja. |
| `Path_Ojo()` | Trazado del ojo mediante segmentos circulares. |

Estas rutinas utilizan principalmente interpolaciones lineales y circulares, permitiendo representar contornos y curvas mediante movimientos continuos del extremo de la herramienta.

### 6.4. Retorno a HOME

Al completar la decoración, el procedimiento ejecuta nuevamente `Path_Home()`.

De esta manera, la rutina de escritura comienza y termina con un movimiento hacia la posición de referencia establecida.

---

## 7. Tipos de movimiento utilizados

Las trayectorias del proyecto utilizan diferentes instrucciones de movimiento RAPID según las necesidades geométricas y funcionales de cada operación.

| Instrucción | Tipo de movimiento | Aplicación |
|---|---|---|
| `MoveJ` | Movimiento articular hacia una posición cartesiana | Aproximación, posicionamiento y transiciones entre trayectorias. |
| `MoveL` | Movimiento lineal del TCP | Escritura de segmentos rectos. |
| `MoveC` | Movimiento circular del TCP | Generación de curvas, contornos y detalles decorativos. |
| `MoveAbsJ` | Movimiento a una configuración articular absoluta | Rutinas de mantenimiento y Farmear Aura. |

### 7.1. Parámetros de movimiento

Las trayectorias de decoración emplean frecuentemente parámetros como:

- `v200`: velocidad programada de movimiento.
- `z10`: zona de aproximación que permite suavizar las transiciones entre posiciones.
- `Tool_Cuy`: herramienta utilizada para ejecutar los movimientos.
- `Workobject_1`: referencia espacial asociada a la superficie de decoración.

Algunas rutinas auxiliares utilizan velocidades diferentes, incluyendo `v400`, `v800` y `v1000`.

Asimismo, el parámetro `fine` se utiliza en posiciones específicas para exigir una llegada precisa al objetivo, sin utilizar una zona de paso suavizada.

### 7.2. Definición de posiciones

El programa emplea dos estructuras principales para definir los objetivos del robot.

**`robtarget`:** contiene la posición y orientación cartesianas del extremo de la herramienta, junto con la configuración del robot y la información de ejes externos.

**`jointtarget`:** contiene los valores articulares que definen directamente una configuración del robot.

La utilización de ambas estructuras permite combinar movimientos cartesianos para la decoración y movimientos articulares para las operaciones auxiliares.

---

## 8. Modo de operación 2 — Posición de mantenimiento

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

## 9. Modo de operación 3 — Farmear Aura

**Entrada de activación:** `DI_03`

**Procedimiento asociado:** `FarmearAura()`

Esta rutina implementa una secuencia demostrativa de movimientos articulares del manipulador ABB IRB 140.

Su propósito es explorar el comportamiento cinemático del robot mediante diferentes configuraciones y velocidades de movimiento.

La secuencia se encuentra estructurada en cinco etapas principales.

### 9.1. Posicionamiento inicial

El robot ejecuta `Path_Home()` y posteriormente se desplaza hacia la configuración `Aura_Vertical`, definida mediante un objetivo articular absoluto.

### 9.2. Apertura y giro

Se realizan movimientos hacia las posiciones `Aura_Abre_Der` y `Aura_Giro_Der`, seguidos de movimientos hacia `Aura_Abre_Izq` y `Aura_Giro_Izq`.

Estas configuraciones generan una secuencia alternada de apertura y rotación del manipulador.

### 9.3. Repetición de giros

El robot repite desplazamientos entre las posiciones de giro derecha e izquierda, utilizando velocidades programadas de movimiento.

### 9.4. Cierre y saludo

La secuencia continúa hacia `Aura_Abre_Der` y `Aura_Vertical`, para luego ejecutar una serie de movimientos de saludo mediante las posiciones:

`Aura_Saludo_1`, `Aura_Saludo_2`, `Aura_Saludo_3`, `Aura_Saludo_4`, `Aura_Saludo_5`, `Aura_Saludo_6` y `Aura_Saludo_Fin`.

### 9.5. Retorno a HOME

La rutina concluye mediante una llamada a `Path_Home()`.

Posteriormente, el procedimiento principal espera la desactivación de `DI_03`, evitando repetir automáticamente la secuencia mientras la entrada permanezca activa.

---

## 10. Consideraciones técnicas de la implementación

La programación desarrollada permite integrar movimientos industriales, trayectorias complejas y selección de modos mediante señales digitales. Sin embargo, es importante distinguir las funciones implementadas de aquellas que podrían incorporarse en versiones posteriores.

### 10.1. Control temporal de la banda

La secuencia automática utiliza tiempos fijos para controlar las etapas de transporte.

Los intervalos empleados son:

- Transporte inicial: 3 segundos.
- Pausa previa a la decoración: 0,5 segundos.
- Transporte de salida: 2 segundos.

La implementación no verifica mediante sensores la llegada del pastel a la zona de trabajo ni su salida de la banda, por lo que fue necesario tomar tiempos experimentalmente. Adicionalmente, es importante mencionar que tras ejecutar los primeros intentos en el robot real, y observar diferencias entre el resultado obtenido y la simulación, nos dimos cuenta que además del ángulo de inclinación, la banda transportadora no estaba completamente paralela al robot, sino que tenía cierta inclinación a la izquierda, lo que hacía que el "pastel" se fuera acercando al robot y alterando la decoración. Como recomendación para otros grupos que en un futuro estén desarrollando este laboratorio, primero aseguranse de que la banda esté correctamente posicionada.



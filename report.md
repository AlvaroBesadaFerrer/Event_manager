# Planificador de Eventos - Taller Mecánico


## Qué hace este programa

El programa es un planificador de eventos para un taller mecánico. Permite crear, listar y eliminar eventos que consumen recursos limitados (áreas de trabajo, trabajadores y herramientas). Antes de guardar un evento, valida conflictos de horario y restricciones del dominio (co-requisitos y exclusiones mutuas). Los datos se guardan en un archivo JSON para que el calendario persista entre ejecuciones.

Funcionalidades principales:
- Agregar eventos manualmente con selección de área, tipo de evento, trabajadores, herramientas, color y horario.
- Agregar eventos automáticamente: busca el próximo intervalo libre en los próximos 7 días con pasos de 5 minutos.
- Agregar eventos con IA (Gemini) a partir de lenguaje natural, con edición iterativa del mismo evento.
- Validación completa de conflictos (área, trabajadores, herramientas) y de restricciones configuradas.
- Ver calendario en una línea de tiempo con colores personalizados y texto legible según el color.
- Ver detalles de un evento seleccionado.
- Eliminar eventos y liberar recursos.
- Ver agenda por recurso (qué eventos usa cada trabajador, herramienta o área).
- Mensajes de error claros cuando hay conflictos, horarios inválidos o restricciones incumplidas.

## Dominio

Se implementó un sistema de gestión de eventos para un **taller mecánico**. El taller realiza trabajos en vehículos (eventos) que requieren espacios físicos (áreas de trabajo), trabajadores especializados y herramientas específicas. 

### ¿Por qué elegí un taller mecánico?

Combina múltiples tipos de recursos (espacios, personas, herramientas) que deben coordinarse
Cada tipo de trabajo tiene requisitos específicos (ej: soldadura requiere trabajadores y herramientas especializadas)
Los recursos son limitados y compartidos, generando conflictos realistas
Es un dominio que existe en el mundo real y puede beneficiarse de esta solución

## Cómo lo diseñé y por qué tomé esas decisiones

Modelé el dominio como un taller mecánico porque combina varios tipos de recursos y restricciones realistas. Separé la lógica en capas:

- domain/: define eventos, recursos y restricciones para mantener el modelo claro y reusable.
- schedule_events/: concentra validaciones y planificación automática para desacoplar la interfaz.
- pages/ y main.py: interfaz Streamlit para interacción visual.
- json_storage/ y utils/: persistencia y utilidades de formato, fechas y colores.

Esta separación facilita probar la lógica del programa sin depender de la interfaz, y permite agregar nuevas páginas o reglas sin romper el resto.

### Objetivo

Evitar conflictos de recursos (dos eventos no pueden usar el mismo recurso al mismo tiempo) y cumplir restricciones configuradas que reflejan las reglas operacionales del taller.

## Recursos

Existen 4 tipos de recursos:

1. **Tipo de evento** (9 tipos): Reparaciones eléctricas, Soldadura en la carrocería, Arreglo de mecánica, Aspirar interior, Pintar exterior, Cambio de aceite, Arreglar dirección, Revisar transmisión, Soldadura en tubo de escape.

2. **Áreas de trabajo** (4 áreas): Espacio con rampa, Espacio para pintura, Espacio de trabajo A, Espacio de trabajo B.

3. **Trabajadores** (6 personas): Juan, Pedro, José, Luisa, Sofía, Frank.

4. **Herramientas** (7 herramientas): Compresor, Caja de herramientas, Planta de soldar, Gato hidráulico, Guantes de trabajo, Careta para soldar, Lentes de seguridad.

## Tipos de Restricciones Implementadas

El sistema implementa dos tipos principales de restricciones, como se requiere en el proyecto:

### 1. **Restricción de Co-requisito (Inclusión)**
Un recurso requiere que otro recurso específico esté presente en el mismo evento.

**Ejemplos en el taller:**
- Evento "Soldadura en la carrocería" requiere trabajador José + herramientas (Careta, Planta de soldar, Guantes)
- Evento "Pintar exterior" requiere área "Espacio para pintura" + Compresor + Lentes de seguridad
- Trabajadora Luisa requiere Guantes de trabajo si participa en cualquier evento

**Implementación:** Clase `CoRequisite` en `domain/restrictions.py`

### 2. **Restricción de Exclusión Mutua**
Dos recursos no pueden estar presentes en el mismo evento.

**Ejemplos en el taller:**
- Evento "Reparaciones eléctricas" no puede realizarse en "Espacio para pintura"
- Trabajadora Sofía no puede trabajar junto a Juan
- Trabajadora Sofía no puede usar el Compresor

**Implementación:** Clase `MutualExclusion` en `domain/restrictions.py`

## Restricciones Detalladas por Recurso

- Evento "Reparaciones eléctricas": Requiere que el trabajador Juan esté asignado. No puede realizarse en el área Espacio para pintura.

- Evento "Soldadura en la carrocería": Requiere al trabajador José. Requiere las herramientas Careta para soldar, Planta de soldar y Guantes de trabajo. No puede realizarse en el área Espacio para pintura.

- Evento "Arreglo de Mecánica": Requiere al trabajador Pedro. Requiere la Caja de herramientas. No puede realizarse en el área Espacio con rampa. No puede realizarse en el área Espacio para pintura.

- Evento "Aspirar interior del auto": Requiere el Compresor. No puede realizarse en el área Espacio con rampa. No puede realizarse en el área Espacio para pintura.

- Evento "Pintar exterior del auto": Requiere el área Espacio para pintura. Requiere el Compresor. Requiere los Lentes de seguridad. No puede ser realizado por el trabajador Pedro.

- Evento "Cambio de aceite del motor": Requiere el Gato hidráulico. No puede realizarse en el área Espacio para pintura.

- Evento "Arreglar dirección": Requiere el área Espacio con rampa. Requiere la Caja de herramientas. Requiere el Gato hidráulico. No puede ser realizado por el trabajador Juan.

- Evento "Revisar transmisión": Requiere el área Espacio con rampa. Requiere la Caja de herramientas. No tiene restricciones de recursos prohibidos.

- Evento "Soldadura en el tubo de escape": Requiere el área Espacio con rampa. Requiere al trabajador José. Requiere la Planta de soldar, la Careta para soldar y los Guantes de trabajo. No tiene restricciones de recursos prohibidos.

- Trabajadora Luisa: Requiere el uso de Guantes de trabajo. No puede participar en el evento Arreglo de Mecánica. No puede participar en el evento Pintar exterior del auto.

- Trabajadora Sofía: No puede trabajar junto a Juan. No puede participar en el evento Arreglar dirección. No puede utilizar el Compresor.

### Configuración de Restricciones

La configuración completa está en `domain/restrictions_config.py` y `domain/restrictions_data.py`.

**Cómo modificar restricciones:**
1. Abre `domain/restrictions_config.py`
2. Cada clave es el ID de un recurso (trabajadores, áreas, herramientas, tipos de evento)
3. Cada recurso tiene dos listas:
   - `"required"`: recursos que deben estar presentes (Co-requisito)
   - `"forbidden"`: recursos que no pueden estar presentes (Exclusión Mutua)

**Ejemplo:**
```python
"event_5": {
    "required": ["area_2", "tool_1", "tool_7"],  # Requiere área 2, compresor y lentes
    "forbidden": ["worker_2"],                    # No puede ser realizado por worker_2
}
```

Todas las restricciones posibles se pueden configurar entre áreas de trabajo, trabajadores, tipos de evento y herramientas. No tiene que ser necesariamente restricciones por cada tipo de evento o cada trabajador, puede ser entre cualquiera de estos objetos.

## Validaciones Implementadas

1. **Conflicto de recursos por tiempo**: Si un recurso ya está asignado en ese horario, el evento se rechaza.
2. **Conflicto de trabajadores**: Si un trabajador ya tiene evento en ese horario, se rechaza.
3. **Conflicto de herramientas**: Si una herramienta ya está en uso, se rechaza.
4. **Conflicto de área de trabajo**: Si un área ya está ocupada, se rechaza.
5. **Violación de restricciones**: Se valida cada restricción configurada (las restricciones que listamos arriba).
6. **Horario laboral**: Los eventos solo pueden entre 08:00 y 17:00, del mismo día (horario de trabajo).
7. **Requerimiento de trabajador**: Cada evento requiere al menos un trabajador.
8. **Orden de horarios**: Hora de fin debe ser posterior a hora de inicio.

## Funcionalidades

1. **Agregar evento manual**: Usuario especifica el área, tipo de evento, trabajadores, herramientas, color y horario. El sistema valida y rechaza si hay conflictos.

2. **Agregar evento automático**: Usuario especifica el área, tipo de evento, trabajadores, herramientas y color. El sistema busca automáticamente el próximo horario disponible en los próximos 7 días, verificando en intervalos de 5 minutos. Si encuentra un intervalo de tiempo válido, lo asigna.

3. **Agregar evento con IA**: Permite crear eventos desde lenguaje natural con Gemini. Para usar esta funcionalidad se requiere configurar la variable de entorno `GEMINI_API_KEY`.

4. **Problemas con las validaciones al crear eventos**: Cuando el usuario intenta crear un evento y no cumple algunas de las validaciones, que fueron listadas anteriormente, se muestran mensajes de error en la interfaz gráfica de todas las validaciones que están fallando.

5. **Ver calendario**: Línea de tiempo visual con todos los eventos programados, representados con distintos colores. También, el color del texto de cada evento se ajusta automáticamente según qué tan oscuro o claro sea el color del evento. 

6. **Ver detalles de evento**: Muestra todos los atributos del evento seleccionado (área, tipo de evento, trabajadores, herramientas, color y horario)

7. **Eliminar evento**: Libera todos los recursos del evento, elimina el evento del JSON y refresca la página.

8. **Ver detalles por recurso**: Muestra la agenda de cada recurso (tipo de evento en el que se usa, hora de inicio y hora de fin del evento)

9. **Persistencia en JSON**: Todos los eventos se guardan en `event_data.json`.

## Guía de Uso

### Página Principal (main.py)
1. **Ver calendario**: Al abrir la aplicación, se muestra una línea de tiempo con todos los eventos programados
2. **Seleccionar evento**: Al hacer clic en cualquier evento puede ver sus detalles
3. **Eliminar evento**: Después de seleccionar un evento, puede eliminarlo con el botón "Eliminar evento"

### Agregar Evento (1_Agregar_evento.py)
1. **Selecciona el lugar**: Elija una de las 4 áreas de trabajo disponibles
2. **Selecciona el tipo de evento**: Elija uno de los 9 tipos de trabajos
3. **Selecciona trabajadores**: Puede seleccionar uno o más trabajadores
4. **Selecciona herramientas**: Marque las herramientas necesarias
5. **Elige color**: Personalice el color del evento en la línea de tiempo
6. **Elige horario**:
   - **Opción manual**: Especifique la fecha, hora de inicio y hora de fin
   - **Opción automática**: El sistema busca automáticamente el próximo horario disponible en los próximos 7 días
7. **Envía el formulario**: El sistema valida automáticamente todas las restricciones y conflictos

**Ejemplo de flujo manual:**
- Área: "Espacio con rampa"
- Tipo: "Arreglar dirección"
- Trabajadores: "Pedro"
- Herramientas: "Caja de herramientas", "Gato hidráulico"
- Fecha: 2026-02-05
- Hora inicio: 09:00
- Hora fin: 11:30
- El sistema valida que Pedro esté disponible, que el área esté libre, y que todas las restricciones se cumplan

**Ejemplo de flujo automático:**
- Área: "Espacio para pintura"
- Tipo: "Pintar exterior del auto"
- Trabajadores: "Luisa"
- Herramientas: "Compresor", "Lentes de seguridad"
- Duración: 120 minutos
- El sistema busca automáticamente el próximo intervalo de tiempo disponible en los próximos 7 días

### Agregar Evento con IA (3_Agregar_evento_con_AI.py)

Crea eventos usando lenguaje natural. La IA Gemini extrae automáticamente los detalles del evento desde tu descripción y permite hacer cambios iterativos.

**Flujo de uso:**

1. **Descripción inicial**: Escribe una descripción en lenguaje natural
   - Ejemplo: "Reparación de motor con Juan mañana a las 10 am por 2 horas en el Espacio con Rampa"

2. **Procesamiento**: Gemini extrae automáticamente:
   - Área de trabajo
   - Tipo de evento
   - Trabajadores asignados
   - Herramientas necesarias
   - Horario (inicio, fin, duración)

3. **Cambios iterativos**: Refina el evento escribiendo nuevas descripciones sin repetir todo:
   - "Agrega a Pedro también"
   - "Cambia la hora a las 2 pm"
   - "Quita el compresor"
   
   La IA mantiene los datos previos y aplica solo los cambios mencionados.

4. **Programación automática**: Si solo especificas duración (sin horario), el sistema usa el planificador automático que creamos anteriormente que:
   - Busca el próximo intervalo disponible en los próximos 7 días
   - Verifica cada 5 minutos disponibilidad de recursos
   - Asigna automáticamente el evento sin requerir hora específica
   - Ejemplo: "Reparación de motor con Juan por 2 horas" → Sistema busca el próximo slot de 2 horas libre

5. **Validación**: El sistema valida automáticamente:
   - Existencia de recursos (ID válidos en el dominio)
   - Coherencia de horarios
   - Conflictos de tiempo con otros eventos
   - Cumplimiento de restricciones configuradas

6. **Creación**: Si todo es válido, se agrega el evento al calendario. Si hay errores, Gemini explica qué está mal y sugiere correcciones.

**Interfaz:**
- Campo de entrada: "¿Qué evento necesitas agendar?"
- Selector de color para personalizar el evento
- Botón: "Procesar con IA"

**Resultado en pantalla:**
- Resumen visual del evento (área, tipo, trabajadores, duración, color)
- JSON completo del evento en expander desplegable
- Mensajes de error con explicación de IA si hay problemas
- Opción de continuar editando o crear nuevo evento

**Ejemplo en acción:**
```
Usuario: "Reparación eléctrica con Juan en Rampa mañana a las 3 pm por 1 hora"

Resultado: ✓ Área: Espacio con rampa
          ✓ Tipo: Reparaciones eléctricas
          ✓ Trabajadores: Juan
          ✓ Inicio: 2026-02-14 15:00:00
          ✓ Duración: 60 minutos

Usuario: "Agrega a José también"

Resultado: (Mantiene todo igual, agrega José a trabajadores)
```

### Ver Detalles por Recurso (2_Ver_detalles_por_recurso.py)
1. Accede a esta página para ver la agenda completa de cada recurso
2. Visualiza qué eventos están usando cada trabajador, herramienta o área
3. Útil para planificar y evitar conflictos


Ejemplo manual (página Agregar evento):
- Área: Espacio con rampa
- Tipo: Arreglar dirección
- Trabajadores: Pedro
- Herramientas: Caja de herramientas, Gato hidráulico
- Inicio: 2026-06-09 09:00
- Fin: 2026-06-09 11:30

Ejemplo automático:
- Área: Espacio para pintura
- Tipo: Pintar exterior del auto
- Trabajadores: Luisa
- Herramientas: Compresor, Lentes de seguridad
- Duración: 120 minutos
El sistema busca el próximo horario disponible y crea el evento si no hay conflictos.

Ejemplo con IA (página Agregar evento con IA):
"Reparación eléctrica con Juan mañana a las 3 pm por 1 hora en el Espacio con rampa"

Ejemplo con IA (solo duración):
"Soldadura en tubo de escape con José por 90 minutos"
El sistema usa el planificador automático para buscar el primer hueco libre.

Ejemplo con IA (edición iterativa):
1) "Pintar exterior mañana a las 10 am por 2 horas en el Espacio para pintura"
2) "Agrega a Luisa"
3) "Cambia la hora a las 2 pm"

Ejemplo de ver detalles por recurso:
- Entrar a la página "Ver detalles por recurso"
- Seleccionar "Herramienta: Compresor"
- Se muestra la lista de eventos donde se usa, con fechas y horas

Ejemplo de eliminación:
- Seleccionar un evento en la línea de tiempo
- Presionar "Eliminar evento"
- El evento se elimina del JSON y desaparece del calendario


## Manejo de Errores

La aplicación muestra mensajes de error claros cuando:
- **Conflicto de horario**: "Un evento de [tipo] está usando el mismo espacio [área] a esa hora"
- **Trabajador ocupado**: "[Trabajador] ya estará trabajando en evento de [tipo] a esa hora"
- **Herramienta en uso**: "[Herramienta] ya se estará usando en evento de [tipo] a esa hora"
- **Restricción violada**: "[Recurso A] no puede estar en un evento con [Recurso B]" o "[Recurso A] necesita estar con [Recurso B] en el evento"
- **Horario fuera de rango**: "Hora de inicio o de fin fuera del horario de trabajo (de 8:00 am a 5:00 pm)"
- **Sin trabajadores**: "Debe seleccionar al menos un trabajador"
- **Horario inválido**: "La hora de fin debe ser posterior a la hora de inicio"
- **Sin disponibilidad**: "No se pudo encontrar un horario adecuado dentro de los próximos 7 días"

## Estructura de Carpetas

```
domain/
  event.py              - Clase Event con validación de intersección de horarios
  resource.py           - Clase Resource y tipos de recurso
  resources_data.py     - Lista de todos los recursos del dominio
  restrictions.py       - Clases Restriction, MutualExclusion, CoRequisite
  restrictions_config.py - Configuración de restricciones
  restrictions_data.py  - Generador de restricciones desde restrictions_config.py

schedule_events/
  schedule.py           - Funciones add_event, auto_schedule_event, validate_event
  validators.py         - Validadores: check_time_conflicts, check_restrictions, check_work_hours, etc.

gemini_scheduler/
  prompt.py             - Instrucción del sistema para Gemini con contexto de eventos previos
  ai_validators.py      - Validación de respuestas de Gemini y cálculo de tiempos
  ai_helpers.py         - Funciones auxiliares: manejo de JSON, explicación de errores, actualización de estado

pages/
  1_Agregar_evento.py   - Interfaz Streamlit para agregar eventos manualmente
  2_Ver_detalles_por_recurso.py - Interfaz para listar recursos y su agenda
  3_Agregar_evento_con_AI.py - Interfaz Streamlit para agregar eventos con Gemini

json_storage/
  save_load_data.py     - Funciones load_data(), save_data() para cargar y guardar los datos de los eventos

utils/
  time_utils.py         - Funciones para convertir fechas y horas de string a objetos datetime
  filter_utils.py       - Filtrado de recursos y eventos, por tipo de evento, id, etc.
  format_utils.py       - Funciones que ayudan a organizar los datos para mostrar detalles de eventos y de recursos
  save_load_utils.py    - Funciones que ayudan a convertir los datos para ser guardados en el JSON o para poder usarlos como objetos después de ser cargados como un diccionario.
  color_utils.py        - Cálculo de color de texto según el color de fondo de cada evento

main.py                 - Página principal con línea de tiempo, con la vista de detalles de un evento y la opción de eliminar eventos
event_data.json       - Almacenamiento de eventos (JSON)
```

## Instalación y Ejecución

### Requisitos
- Python 3.10+
- Dependencias en `requirements.txt`
- Clave API de Google Gemini (para usar la funcionalidad de agregar eventos con IA)

### Obtener Clave API de Gemini

Para usar la funcionalidad "Agregar Evento con IA", necesitas una clave API de Google Gemini:

1. Ve a [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Haz clic en "Create API Key"
3. Selecciona "Create new secret key in new project"
4. Copia la clave API generada

### Configurar Variables de Entorno

1. **Crear archivo `.env`** en la raíz del proyecto:
   ```bash
   touch .env
   ```

2. **Agregar la clave API** al archivo `.env`:
   ```
   GEMINI_API_KEY=tu_clave_api_aqui
   ```


**Nota:** La aplicación cargará la clave automáticamente al iniciar. Si la clave no está configurada, la página "Agregar evento con IA" mostrará un error.

### Instalación

**Instalar dependencias**
```bash
pip install -r requirements.txt
```

**Alternativa con pyproject.toml (Poetry)**
```bash
pip install poetry
poetry install
```

### Ejecutar la aplicación
```bash
streamlit run main.py
```

Si usas Poetry:
```bash
poetry run streamlit run main.py
```


### Estructura de un Evento (JSON)
```json
{
  "id": "uuid-del-evento",
  "spot": "area_1",
  "event_type": "event_7",
  "workers": ["worker_1", "worker_2"],
  "resources": ["tool_1", "tool_3"],
  "start_time": "2026-02-02 09:00:00",
  "end_time": "2026-02-02 12:30:00",
  "color": "#3498db"
}
```

## Archivos de Ejemplo

`event_data.json` contiene eventos de ejemplo con diferentes tipos de trabajos, áreas, trabajadores y herramientas para demostrar el funcionamiento del sistema. 

## Notas Técnicas

- **Zona horaria**: America/Havana
- **Intervalo de búsqueda automática**: 5 minutos
- **Rango de búsqueda automática**: 7 días desde ahora
- **Almacenamiento**: JSON
- **Interfaz**: Streamlit con componente de línea de tiempo (streamlit-vis-timeline)
- **IA**: Google Gemini con respuestas estructuradas en JSON
- **Lenguaje**: Python 3.10+
- **Librerías principales**: 
  - `streamlit`: Framework para la interfaz gráfica
  - `streamlit-vis-timeline`: Componente de línea de tiempo
  - `google-genai`: SDK de Google Gemini para procesamiento de lenguaje natural
  - `datetime`: Gestión de fechas y horas
  - `json`: Persistencia de datos y manejo de respuestas de IA
  - `uuid`: Generación de IDs únicos para eventos
  - `python-dotenv`: Carga de variables de entorno (GEMINI_API_KEY)



## Qué aprendí durante el desarrollo

- A modelar recursos y restricciones de un dominio real en estructuras de datos simples.
- A manejar intervalos de tiempo y validaciones consistentes.
- A diseñar una interfaz con Streamlit que muestre resultados de forma clara.
- A integrar una API de IA (Gemini) para interpretar texto natural y convertirlo en eventos.
- A implementar un planificador automático que busca el próximo intervalo libre con pasos de tiempo pequeños.
- A construir mensajes de error útiles a partir de reglas de negocio y restricciones configurables.
- A trabajar con persistencia en JSON y a mantener sincronizada la interfaz con el estado guardado.
- A manejar el flujo completo con IA (prompt, JSON, validación, explicación de errores) y el uso de historial para mantener contexto.
- A normalizar fechas y horas con zona horaria (America/Havana) y formatos consistentes.
- A diseñar prompts estrictos que obligan a devolver JSON válido y a no inventar recursos.
- A separar validaciones por capas: requerimientos básicos, coherencia de tiempos y restricciones del dominio.
- A reutilizar la lógica de auto-agendado tanto en la creación manual como en la asistida por IA.


## Dificultades que encontré y cómo las resolví

- Validar conflictos de horarios entre múltiples recursos: resolví usando comparación de intervalos y validadores dedicados.
- Aplicar restricciones configurables: creé un archivo de configuración (restrictions_config.py) y generadores de reglas (restrictions_data.py) para poder cambiarlas fácilmente cada vez que sea necesario.
- Mantener la interfaz sincronizada con el JSON: centralice la carga y guardado en funciones de json_storage.
- Lograr que la línea de tiempo se mostrara bien y fuera interactiva para seleccionar eventos y ver detalles. Tuve que buscar entre varias librerías para ver cómo hacerlo.
- Ajustar visualmente la línea de tiempo: usé un cálculo automático de color de texto según el color del evento, para que no hubiera un fondo oscuro con un texto oscuro o texto claro con fondo claro.
- Integrar Gemini: primero probé modelos más avanzados, incluso de OpenAI, pero siempre había limitaciones (por ejemplo, eran de pago), así que ajusté la solución a un modelo que fuera gratis y fuera lo suficientemente inteligente como para esta tarea (aunque a veces comete errores).
- Interacción con Gemini: fue complejo coordinar el flujo completo. El usuario escribe, se llama a Gemini para devolver un JSON, se valida ese JSON, se determinan errores según las restricciones, y luego se le envía a Gemini para que explique los errores, dé ejemplos y muestre por qué está mal.
- Manejo de duración con IA: fue un reto decidir que, si la IA no recibe fecha de inicio y fin sino una duración, en vez de crear el evento en un horario específico se llama al planificador automático, igual que cuando se crean eventos a mano.
- Memoria del modelo: estas IA no tienen memoria, por tanto tuve que incluir el historial de mensajes en cada prompt antes de enviarlo.



# Planificador de Eventos - Taller Mecánico

## Dominio

Se implementó un sistema de gestión de eventos para un taller mecánico. El taller realiza trabajos en vehículos (eventos) que requieren espacios físicos (áreas de trabajo), trabajadores especializados y herramientas específicas. El objetivo es evitar conflictos de recursos (dos eventos no pueden usar el mismo recurso al mismo tiempo) y cumplir restricciones configuradas.

## Recursos

Existen 4 tipos de recursos:

1. **Tipo de evento** (9 tipos): Reparaciones eléctricas, Soldadura en la carrocería, Arreglo de mecánica, Aspirar interior, Pintar exterior, Cambio de aceite, Arreglar dirección, Revisar transmisión, Soldadura en tubo de escape.

2. **Áreas de trabajo** (4 áreas): Espacio con rampa, Espacio para pintura, Espacio de trabajo 1, Espacio de trabajo 2.

3. **Trabajadores** (6 personas): Juan, Pedro, José, Luisa, Sofía, Frank.

4. **Herramientas** (7 herramientas): Compresor, Caja de herramientas, Planta de soldar, Gato hidráulico, Guantes de trabajo, Careta para soldar, Lentes de seguridad.

## Restricciones

- Evento “Reparaciones eléctricas”: Requiere que el trabajador Juan esté asignado. No puede realizarse en el área Espacio para pintura.

- Evento “Soldadura en la carrocería”: Requiere al trabajador José. Requiere las herramientas Careta para soldar, Planta de soldar y Guantes de trabajo. No puede realizarse en el área Espacio para pintura.

- Evento “Arreglo de Mecánica”: Requiere al trabajador Pedro. Requiere la Caja de herramientas. No puede realizarse en el área Espacio con rampa. No puede realizarse en el área Espacio para pintura.

- Evento “Aspirar interior del auto”: Requiere el Compresor. No puede realizarse en el área Espacio con rampa. No puede realizarse en el área Espacio para pintura.

- Evento “Pintar exterior del auto”: Requiere el área Espacio para pintura. Requiere el Compresor. Requiere los Lentes de seguridad. No puede ser realizado por el trabajador Pedro.

- Evento “Cambio de aceite del motor”: Requiere el Gato hidráulico. No puede realizarse en el área Espacio para pintura.

- Evento “Arreglar dirección”: Requiere el área Espacio con rampa. Requiere la Caja de herramientas. Requiere el Gato hidráulico. No puede ser realizado por el trabajador Juan.

- Evento “Revisar transmisión”: Requiere el área Espacio con rampa. Requiere la Caja de herramientas. No tiene restricciones de recursos prohibidos.

- Evento “Soldadura en el tubo de escape”: Requiere el área Espacio con rampa. Requiere al trabajador José. Requiere la Planta de soldar, la Careta para soldar y los Guantes de trabajo. No tiene restricciones de recursos prohibidos.

- Trabajadora Luisa: Requiere el uso de Guantes de trabajo. No puede participar en el evento Arreglo de Mecánica. No puede participar en el evento Pintar exterior del auto.

- Trabajadora Sofía: No puede trabajar junto a Juan. No puede participar en el evento Arreglar dirección. No puede utilizar el Compresor.

La configuración completa está en `domain/restrictions_config.py` y `domain/restrictions_data.py`.
Todas las restricciones posibles se pueden configurar entre áreas de trabajo, trabajadores, tipos de evento y herramientas en `domain/restrictions_config.py`. No tiene que ser neccesariamente restricciones por cada tipo de evento o cada trabajador, puede ser entre cualquiera de estos objetos.

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

3. **Problemas con las validaciones al crear eventos**: Cuando el usuario intenta crear un evento y no cumple algunas de las validaciones, que fueron listadas anteriormente, se muestran mensajes de error en la interfaz gráfica de todas las validaciones que están fallando.

4. **Ver calendario**: Línea de tiempo visual con todos los eventos programados, representados con distintos colores. También, el color del texto de cada evento se ajusta automáticamente según qué tan oscuro o claro sea el color del evento. 

5. **Ver detalles de evento**: Muestra todos los atributos del evento seleccionado (área, tipo de evento, trabajadores, herramientas, color y horario)

6. **Eliminar evento**: Libera todos los recursos del evento, elimina el evento del JSON y refresca la página.

7. **Ver detalles por recurso**: Muestra la agenda de cada recurso (tipo de evento en el que se usa, hora de inicio y hora de fin del evento)

8. **Persistencia en JSON**: Todos los eventos se guardan en `event_data.json`.

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

pages/
  1_Agregar_evento.py   - Interfaz Streamlit para agregar eventos
  2_Ver_detalles_por_recurso.py - Interfaz para listar recursos y su agenda

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

### Instalación
```bash
pip install -r requirements.txt
```

### Ejecutar la aplicación
```bash
streamlit run main.py
```

Se abre automáticamente en http://localhost:8501

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

- Zona horaria: America/Havana
- Intervalo de búsqueda automática: 5 minutos
- Rango de búsqueda automática: 7 días desde ahora
- Almacenamiento: JSON
- Interfaz: Streamlit con componente de línea de tiempo (streamlit-vis-timeline)

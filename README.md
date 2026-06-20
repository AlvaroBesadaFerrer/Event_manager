Planificador de eventos para un taller mecánico. Permite crear, listar y eliminar eventos que consumen recursos limitados (áreas de trabajo, trabajadores y herramientas). Antes de guardar un evento, valida conflictos de horario y restricciones del dominio (co-requisitos y exclusiones mutuas). Los datos se guardan en un archivo JSON para que el calendario persista entre ejecuciones.

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

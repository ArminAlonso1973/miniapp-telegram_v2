Decisiones de Arquitectura

📊 Contexto General

El proyecto tiene como objetivo desarrollar una miniaplicación modular y escalable, utilizando contenedores Docker. La aplicación incluye un backend basado en Quart y soporte para integración con bases de datos, sistemas de caché y servicios externos de OpenAI. A continuación, se documentan las decisiones clave que facilitan el mantenimiento y la extensibilidad del proyecto.

🛠️ Principales Componentes

Backend

Lenguaje: Python.

Framework: Quart por su soporte asíncrono.

Características Principales:

Registro de Blueprints para organizar las rutas.

Inicialización centralizada de servicios.

Manejo eficiente de errores y logs.

Frontend

Manejado en un contenedor separado.

Independiente del backend.

Bases de Datos

Redis: Almacenamiento en caché para respuestas frecuentes.

PostgreSQL: Base de datos relacional utilizada para datos persistentes.

Asistente OpenAI

Modelo: Integrado con GPT-4.

Funcionalidades:

Recepción de mensajes y ejecución de tool calls.

Ejecución de requires actions con respuestas automáticas.

Búsqueda optimizada en Redis y posteriormente en PostgreSQL.

Generación de prompts y respuestas finales basadas en contexto.

📏 Nuevas Decisiones Clave

1. Agrupación de Funciones Complejas de OpenAI

Se ha unificado toda la lógica de comunicación con el asistente de OpenAI en una única clase: AssistantService.

Motivos:

Facilitar la reutilización en otros proyectos.

Mejorar la mantenibilidad del código.

Centralizar operaciones complejas en un solo punto.

Funciones Agrupadas:

Recepción de una pregunta.

Ejecución de tool calls y manejo de requires actions.

Búsqueda optimizada:

Redis: Primero se verifica la caché para respuestas frecuentes.

PostgreSQL: Si no existe en Redis, se realiza una consulta en la base de datos relacional.

Generación de prompts y respuesta final a través de OpenAI.

Beneficios:

La clase AssistantService es autónoma y puede ser fácilmente integrada en nuevos proyectos.

La lógica completa está encapsulada y se puede probar de manera individual con Pytest.

2. Refactorización del Uso de Redis

Problemas Detectados:

Inicialización redundante de Redis.

Duplicación de lógica en varias partes del código.

Solución:

Redis se inicializa globalmente al iniciar la aplicación (únicamente en app.py).

Las funciones guardar_cache y obtener_cache en redis_service.py asumen que la conexión global está activa.

Estrategia de Búsqueda Optimizada:

Se verifica la existencia de datos en Redis.

Si no se encuentran, se consultan en PostgreSQL y se almacenan en Redis con una expiración de 1 hora.

3. Modularización del Código

Se ha eliminado la redundancia de endpoints y servicios:

Redis: Los endpoints relacionados con Redis se mantienen exclusivamente en redis_routes.py.

PostgreSQL: Operaciones centralizadas en postgres_service.py.

AssistantService: Maneja de manera integral la interacción con OpenAI.

Nuevos Archivos y Refactorización:

services/assistant_service.py: Clase que encapsula toda la lógica del asistente.

services/redis_service.py: Manejo centralizado de Redis.

services/postgres_service.py: Manejo centralizado de PostgreSQL.

🔢 Pruebas Automatizadas

Problemas Detectados:

Las pruebas existentes eran limitadas y no validaban la integración completa con Redis y PostgreSQL.

Solución:

Se amplió el archivo test_redis.py para probar:

Almacenamiento en Redis.

Recuperación desde Redis.

Validación de expiración de claves.

Nuevas pruebas para PostgreSQL en test_postgres.py:

Validar la conexión.

Insertar y recuperar datos.

Pruebas de integración para AssistantService:

Flujo completo de interacción con OpenAI.

Verificación de búsqueda en Redis y PostgreSQL.

💡 Beneficios de las Decisiones

Reutilización:

La clase AssistantService puede ser implementada fácilmente en otros proyectos.

Mantenimiento:

Lógica compleja centralizada facilita la detección y corrección de errores.

Rendimiento:

La búsqueda optimizada en Redis y PostgreSQL mejora la velocidad de respuesta.

Pruebas Robustas:

Las nuevas pruebas aseguran la estabilidad y el funcionamiento correcto del sistema.

📝 Próximos Pasos

Integrar pruebas continuas (CI/CD) con herramientas como GitHub Actions.

Documentar completamente la clase AssistantService con ejemplos de uso.

Monitorear el rendimiento de Redis y PostgreSQL en producción.

Preparar el sistema para escalar horizontalmente en caso de incremento de usuarios.

Esta estructura modular y optimizada asegura que el sistema sea escalable, eficiente y fácil de mantener, además de proporcionar una base sólida para futuros desarrollos. 🌟🚀


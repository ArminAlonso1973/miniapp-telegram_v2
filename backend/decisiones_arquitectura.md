Decisiones de Arquitectura 📚🚀

Contexto General 🌟

El proyecto actual tiene como objetivo desarrollar una miniaplicación utilizando contenedores Docker para gestionar un backend basado en Quart, con soporte para operaciones asincrónicas, integración con bases de datos y pruebas automatizadas. A continuación, se documentan las decisiones arquitectónicas tomadas hasta la fecha.

Contenedores Docker 🐳

Situación Actual ⚙️

Backend:

Lenguaje: Python con Quart.

Define la lógica de la aplicación y las rutas para los servicios.

Frontend:

Se utiliza un contenedor separado para manejar la interfaz.

PostgreSQL:

Base de datos relacional, utilizada como reemplazo de ArangoDB.

Configurado con variables de entorno para credenciales.

Integrado con soporte nativo en Render.

Redis:

Base de datos en memoria, utilizada para manejar operaciones rápidas y colas de mensajes.

Configurado también con soporte en Render.

Problemas y Cambios 🔄

Inicialmente, se implementó ArangoDB como base de datos principal, pero debido a incompatibilidades con operaciones asincrónicas en Quart, se decidió migrar a PostgreSQL.

Desarrollo del Backend 🛠️

Framework Seleccionado:

Quart: Elegido por su soporte para asincronía, permitiendo operaciones eficientes con Redis y PostgreSQL.

Decisiones sobre Lógica de Inicio:

Centralizar la inicialización de servicios (p. ej., Redis) en el archivo services/__init__.py.

Uso de “fábrica de pruebas” para permitir la configuración flexible del backend, especialmente durante las pruebas automatizadas.

Problemas Encontrados:

Se detectaron problemas de repetición de código al trasladar los “blueprints” a __init__.py. Aunque esta estructura mejora la modularidad, es necesario refactorizar para evitar duplicación de código.

Bases de Datos 🗄️

PostgreSQL

Base de datos principal para almacenamiento persistente.

Utiliza conexión nativa en Render.

Configurado en un contenedor separado, manejado por Docker Compose.

Redis

Base de datos en memoria para operaciones rápidas.

Utilizada también para colas de mensajes.

Pruebas Automatizadas ✅

Framework: Pytest.

Ubicación: Las pruebas se encuentran en el directorio ./backend/test/test.

Cobertura:

Pruebas unitarias de los servicios.

Pruebas de integración para verificar el funcionamiento de rutas y servicios externos.

Cambios Implementados 📝

Migración de ArangoDB a PostgreSQL debido a problemas de compatibilidad asincrónica.

Uso de Redis para almacenamiento rápido.

Inclusión de un esquema de pruebas automatizadas basado en Pytest.

Implementación de una fábrica de pruebas para flexibilizar el desarrollo y permitir una mejor configuración de pruebas.

Configuración de contenedores Docker separados para cada componente (backend, frontend, PostgreSQL y Redis).

Planes Futuros 🌱

Refactorizar la lógica de inicialización de blueprints para evitar duplicación de código.

Consolidar un sistema de documentación interna que facilite la colaboración en el equipo.

Ampliar las pruebas automatizadas para incluir casos de error complejos.

Notas Finales 🖋️

Este archivo debe actualizarse de forma regular para reflejar cualquier cambio importante en la arquitectura del proyecto. La consistencia en las decisiones arquitectónicas es clave para mantener un sistema robusto y fácil de escalar. ✨
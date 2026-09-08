# SIREMA

**Sistema de Revisiones y Mantenciones**

Aplicación web para el control de las mantenciones y revisiones periódicas del material menor de la Octava Compañía del Cuerpo de Bomberos de Talcahuano.

Proyecto APT desarrollado en la asignatura Capstone, Ingeniería en Informática, Duoc UC Sede San Andrés.

---

## Descripción

La Octava Compañía opera equipos delicados y críticos, como motores de combustión, equipos de medición de gases y herramientas hidráulicas de rescate. Por norma y por seguridad, esos equipos deben revisarse periódicamente: encenderlos, medir su estado, verificar niveles y dejar constancia del resultado.

Hoy esas revisiones se realizan de memoria o en papel. No existe un calendario, no queda registro de quién revisó ni con qué resultado, y una falla puede descubrirse recién durante la emergencia.

SIREMA convierte esa práctica informal en un proceso controlado. Define para cada equipo un plan de revisión con su frecuencia, lo asigna a un bombero responsable y lo ejecuta como una lista de verificación con resultado, valores medidos y observaciones. El sistema conserva el historial completo, avisa lo pendiente o vencido y entrega a la jefatura un panel con el estado real del material.

El aporte de valor es que la jefatura pueda conocer el estado real de cada equipo antes de que ocurra la emergencia, y que cada revisión quede asociada a un equipo identificable y a un responsable.

---

## A quién va dirigido

| Usuario | Qué hace en el sistema |
|---|---|
| Bombero | Ejecuta las revisiones asignadas y registra sus resultados desde el celular, junto al carro. |
| Encargado de material | Administra el inventario, define los planes de revisión y asigna responsables. |
| Jefatura | Consulta el panel de cumplimiento, el historial por equipo y los reportes exportables. |
| Administrador | Gestiona usuarios, roles y respaldos del sistema. |

---

## Alcance

**Incluye**

- Gestión de usuarios con rol asignado y restricción de funciones según ese rol.
- Inventario del material menor, con código institucional único por elemento.
- Registro de la ubicación en carro y cajonera, y de los movimientos entre ellas.
- Búsqueda y filtros por nombre, código, ubicación, categoría y estado.
- Definición de planes de revisión por frecuencia y su asignación a bomberos.
- Ejecución de la revisión como lista de verificación con resultado, valores medidos y observaciones.
- Notificaciones de revisiones pendientes o vencidas.
- Panel de indicadores de cumplimiento, historial por equipo y reportes exportables.
- Bitácora de auditoría de toda acción relevante.

**No incluye**

- Material mayor y vehículos.
- Integración con sistemas externos.
- Aplicación móvil nativa.

---

## Arquitectura de la solución

El sistema se despliega en un servidor local dentro del cuartel y opera sobre la red interna, sin requerir conexión permanente a internet. Los usuarios acceden desde el navegador de sus celulares o computadores conectados a esa misma red.

La solución se ejecuta en contenedores, separando el servidor web, la aplicación y la base de datos. Los datos residen en un volumen persistente, de modo que sobreviven a la recreación de los contenedores y a los reinicios del equipo. El servidor está configurado para levantar los servicios de forma automática al arrancar, y se contemplan respaldos periódicos de la base de datos con procedimiento de restauración verificado.

La aplicación se organiza en cuatro módulos de dominio construidos sobre un modelo de datos común:

| Módulo | Responsabilidad |
|---|---|
| Accesos | Usuarios, roles, autenticación y control de permisos. |
| Inventario | Material menor, código institucional único, ubicaciones y movimientos. |
| Revisiones | Planes de revisión, asignación de responsables y ejecución con registro de resultados. |
| Reportes | Panel de cumplimiento, notificaciones, exportaciones y bitácora de auditoría. |

Cada revisión queda enlazada a un equipo registrado en el inventario y a un responsable, lo que sostiene la trazabilidad completa del material.

---

## Ejecución del proyecto

El sistema se levanta mediante contenedores, por lo que la instalación no requiere configurar manualmente el entorno en el equipo servidor.

**Requisitos previos**

- Docker instalado en el equipo servidor.
- Acceso a la red local del cuartel.
- Archivo de variables de entorno con las credenciales de la base de datos.

**Puesta en marcha**

1. Clonar el repositorio en el equipo servidor.
2. Crear el archivo de variables de entorno a partir del archivo de ejemplo incluido y completar las credenciales.
3. Construir y levantar los contenedores.
4. Aplicar las migraciones de la base de datos.
5. Crear el usuario administrador inicial.
6. Cargar el inventario del material menor.

Una vez levantado, el sistema queda disponible para todos los dispositivos conectados a la red del cuartel a través de la dirección del servidor.

El detalle técnico de cada paso, junto con el procedimiento de respaldo y restauración, se documenta en el manual técnico de despliegue incluido en la carpeta de documentación.

---

## Equipo

| Integrante | Rol | Responsabilidades |
|---|---|---|
| **Renato Pomeri Navarrete** | Jefe de proyecto y analista de requisitos | Planificación y control del avance, relación con la contraparte, levantamiento y especificación de requerimientos, coordinación de la implantación y capacitación en el cuartel. |
| **Fernando Molina Figueroa** | Arquitecto de datos y desarrollador back end | Diseño e implementación del modelo de datos, lógica de negocio de los módulos de inventario y revisiones, seguridad de acceso, respaldos y su restauración. |
| **Fabián Fica Villagra** | Desarrollador front end y encargado de calidad | Diseño de interfaces y del prototipo, construcción de las vistas responsivas y del panel de indicadores, elaboración y ejecución del plan de pruebas y seguimiento de los hallazgos. |

---

## Metodología de trabajo

El proyecto se desarrolla con una **metodología tradicional en cascada**, en la que cada etapa se cierra con un producto documentado y validado antes de iniciar la siguiente.

La elección responde a las características del encargo: los requerimientos derivan de normas y prácticas de revisión estables en el tiempo, la contraparte tiene disponibilidad acotada y necesita validar documentos concretos en instancias puntuales, y el plazo de la asignatura es fijo.

| Etapa | Producto que la cierra |
|---|---|
| 1. Levantamiento de requerimientos | Acta de levantamiento con el proceso actual documentado |
| 2. Análisis y especificación | Documento de requerimientos validado por la contraparte |
| 3. Diseño | Documento de diseño con arquitectura, modelo de datos y diagramas UML |
| 4. Construcción | Sistema funcional con el código versionado en este repositorio |
| 5. Pruebas | Plan de pruebas con sus evidencias de ejecución |
| 6. Implantación y cierre | Sistema en operación, manual técnico y acta de entrega |

El trabajo se coordina mediante ramas por funcionalidad y revisión cruzada antes de integrar a la rama principal.

---

## Planificación

| Fase | Semanas | Contenido |
|---|---|---|
| Fase 1 | 1 a 4 | Definición del proyecto, levantamiento y especificación de requisitos |
| Fase 2 | 5 a 15 | Diseño, construcción de los módulos, pruebas, despliegue y documentación |
| Fase 3 | 16 a 18 | Presentación del proyecto ante la comisión evaluadora |

Hitos de entrega: definición del proyecto en la semana 4, informe de avance en la semana 10 e informe final en la semana 15.

---

## Estructura del repositorio

- **Fase 1**: documentación de la definición del proyecto y evidencias individuales.
- **Fase 2**: documentación de requerimientos, diseño, pruebas y manual técnico.
- **src**: código fuente de la aplicación, organizado por módulos de dominio.
- **docs**: diagramas, modelo de datos y material de apoyo.

---

## Tecnologías utilizadas

- **Python**
- **Bootstrap**
- **HTML**
- **PostgreSQL**
- **Docker**

---

## Estado del proyecto

En desarrollo. Fase 1 completada.

---

## Contexto académico

Este repositorio corresponde a un proyecto de titulación de Duoc UC y su uso es académico. El sistema se desarrolla para la Octava Compañía del Cuerpo de Bomberos de Talcahuano, que participa como contraparte del proyecto.

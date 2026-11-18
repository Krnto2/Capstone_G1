--
-- PostgreSQL database dump
--

\restrict pyj6LKREbJh5DTFN72xx0ZxM1tHBQmTXuGKHandBNTd6nnWEz3HhqX6OhUY3TyN

-- Dumped from database version 16.15 (Debian 16.15-1.pgdg13+2)
-- Dumped by pg_dump version 16.15 (Debian 16.15-1.pgdg13+2)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: unidad; Type: TABLE DATA; Schema: public; Owner: -
--

SET SESSION AUTHORIZATION DEFAULT;

ALTER TABLE public.unidad DISABLE TRIGGER ALL;

INSERT INTO public.unidad (id_unidad, codigo, nombre, tipo, activo) VALUES (1, 'B-8', 'Carro de incendios', 'carro', true);
INSERT INTO public.unidad (id_unidad, codigo, nombre, tipo, activo) VALUES (2, 'H-8', 'Unidad HazMat', 'carro', true);
INSERT INTO public.unidad (id_unidad, codigo, nombre, tipo, activo) VALUES (3, 'F-8', 'Carro de rescate', 'carro', true);
INSERT INTO public.unidad (id_unidad, codigo, nombre, tipo, activo) VALUES (4, 'BOD', 'Bodega del cuartel', 'bodega', true);


ALTER TABLE public.unidad ENABLE TRIGGER ALL;

--
-- Data for Name: cajonera; Type: TABLE DATA; Schema: public; Owner: -
--

ALTER TABLE public.cajonera DISABLE TRIGGER ALL;

INSERT INTO public.cajonera (id_cajonera, nombre, descripcion, orden, id_unidad) VALUES (1, 'Cabina trasera', NULL, 1, 1);
INSERT INTO public.cajonera (id_cajonera, nombre, descripcion, orden, id_unidad) VALUES (2, 'Cajonera 1', NULL, 2, 1);
INSERT INTO public.cajonera (id_cajonera, nombre, descripcion, orden, id_unidad) VALUES (3, 'Cajonera 2', NULL, 3, 1);
INSERT INTO public.cajonera (id_cajonera, nombre, descripcion, orden, id_unidad) VALUES (4, 'Cajonera 3', NULL, 4, 1);
INSERT INTO public.cajonera (id_cajonera, nombre, descripcion, orden, id_unidad) VALUES (5, 'Cajonera 4', NULL, 5, 1);
INSERT INTO public.cajonera (id_cajonera, nombre, descripcion, orden, id_unidad) VALUES (6, 'Cabina', NULL, 1, 2);
INSERT INTO public.cajonera (id_cajonera, nombre, descripcion, orden, id_unidad) VALUES (7, 'Cajonera 1', NULL, 2, 2);
INSERT INTO public.cajonera (id_cajonera, nombre, descripcion, orden, id_unidad) VALUES (8, 'Cajonera 2', NULL, 3, 2);
INSERT INTO public.cajonera (id_cajonera, nombre, descripcion, orden, id_unidad) VALUES (9, 'Cajonera 3', NULL, 4, 2);
INSERT INTO public.cajonera (id_cajonera, nombre, descripcion, orden, id_unidad) VALUES (10, 'Cajonera 1', NULL, 1, 3);
INSERT INTO public.cajonera (id_cajonera, nombre, descripcion, orden, id_unidad) VALUES (11, 'Cajonera 2', NULL, 2, 3);
INSERT INTO public.cajonera (id_cajonera, nombre, descripcion, orden, id_unidad) VALUES (12, 'Techo', NULL, 3, 3);
INSERT INTO public.cajonera (id_cajonera, nombre, descripcion, orden, id_unidad) VALUES (13, 'Estante A', NULL, 1, 4);
INSERT INTO public.cajonera (id_cajonera, nombre, descripcion, orden, id_unidad) VALUES (14, 'Estante B', NULL, 2, 4);


ALTER TABLE public.cajonera ENABLE TRIGGER ALL;

--
-- Data for Name: categoria; Type: TABLE DATA; Schema: public; Owner: -
--

ALTER TABLE public.categoria DISABLE TRIGGER ALL;

INSERT INTO public.categoria (id_categoria, nombre, descripcion) VALUES (1, 'AGUA', 'Material de agua y bombeo');
INSERT INTO public.categoria (id_categoria, nombre, descripcion) VALUES (2, 'ERA', 'Equipos de respiración autónoma');
INSERT INTO public.categoria (id_categoria, nombre, descripcion) VALUES (3, 'HAZMAT', 'Materiales peligrosos y medición de gases');
INSERT INTO public.categoria (id_categoria, nombre, descripcion) VALUES (4, 'MOTORES', 'Equipos con motor de combustión');
INSERT INTO public.categoria (id_categoria, nombre, descripcion) VALUES (5, 'RESCATE', 'Herramientas hidráulicas y de rescate');
INSERT INTO public.categoria (id_categoria, nombre, descripcion) VALUES (6, 'ELECTRICIDAD', 'Generación e iluminación');
INSERT INTO public.categoria (id_categoria, nombre, descripcion) VALUES (7, 'PROTECCIÓN', 'Elementos de protección personal');


ALTER TABLE public.categoria ENABLE TRIGGER ALL;

--
-- Data for Name: material; Type: TABLE DATA; Schema: public; Owner: -
--

ALTER TABLE public.material DISABLE TRIGGER ALL;

INSERT INTO public.material (id_material, codigo_institucional, nombre, tipo, cantidad, marca, modelo, numero_serie, estado, observaciones, fecha_alta, fecha_actualizacion, id_cajonera, id_categoria) VALUES (1, '8C-0112', 'Motobomba portátil', 'unitario', 1, 'Honda', 'WX15', NULL, 'activo', NULL, '2026-11-17 22:05:10.793728-03', '2026-11-17 22:05:10.793888-03', 1, 4);
INSERT INTO public.material (id_material, codigo_institucional, nombre, tipo, cantidad, marca, modelo, numero_serie, estado, observaciones, fecha_alta, fecha_actualizacion, id_cajonera, id_categoria) VALUES (2, '8C-0457', 'Detector multigas', 'unitario', 1, 'MSA', 'Altair 4XR', NULL, 'activo', NULL, '2026-11-17 22:05:10.797377-03', '2026-11-17 22:05:10.79747-03', 9, 3);
INSERT INTO public.material (id_material, codigo_institucional, nombre, tipo, cantidad, marca, modelo, numero_serie, estado, observaciones, fecha_alta, fecha_actualizacion, id_cajonera, id_categoria) VALUES (3, '8C-0233', 'Motosierra de rescate', 'unitario', 1, 'Stihl', 'MS 462 R', NULL, 'activo', NULL, '2026-11-17 22:05:10.80061-03', '2026-11-17 22:05:10.800695-03', 3, 5);
INSERT INTO public.material (id_material, codigo_institucional, nombre, tipo, cantidad, marca, modelo, numero_serie, estado, observaciones, fecha_alta, fecha_actualizacion, id_cajonera, id_categoria) VALUES (4, '8C-0390', 'Generador eléctrico', 'unitario', 1, 'Honda', 'EU22i', NULL, 'activo', NULL, '2026-11-17 22:05:10.803537-03', '2026-11-17 22:05:10.803618-03', 10, 6);
INSERT INTO public.material (id_material, codigo_institucional, nombre, tipo, cantidad, marca, modelo, numero_serie, estado, observaciones, fecha_alta, fecha_actualizacion, id_cajonera, id_categoria) VALUES (5, '8C-0101', 'Ventilador de presión positiva', 'unitario', 1, 'Tempest', 'GX200', NULL, 'activo', NULL, '2026-11-17 22:05:10.806563-03', '2026-11-17 22:05:10.806644-03', 5, 4);
INSERT INTO public.material (id_material, codigo_institucional, nombre, tipo, cantidad, marca, modelo, numero_serie, estado, observaciones, fecha_alta, fecha_actualizacion, id_cajonera, id_categoria) VALUES (6, '8C-0305', 'Equipo de corte hidráulico', 'unitario', 1, 'Holmatro', 'CU 4050', NULL, 'activo', NULL, '2026-11-17 22:05:10.809214-03', '2026-11-17 22:05:10.809296-03', 11, 5);
INSERT INTO public.material (id_material, codigo_institucional, nombre, tipo, cantidad, marca, modelo, numero_serie, estado, observaciones, fecha_alta, fecha_actualizacion, id_cajonera, id_categoria) VALUES (7, '8C-0458', 'Detector monogas H2S', 'unitario', 1, 'Dräger', 'Pac 6500', NULL, 'activo', NULL, '2026-11-17 22:05:10.812008-03', '2026-11-17 22:05:10.812087-03', 9, 3);
INSERT INTO public.material (id_material, codigo_institucional, nombre, tipo, cantidad, marca, modelo, numero_serie, estado, observaciones, fecha_alta, fecha_actualizacion, id_cajonera, id_categoria) VALUES (8, '8C-0120', 'Motobomba de achique', 'unitario', 1, 'Koshin', 'SEV-50X', NULL, 'activo', NULL, '2026-11-17 22:05:10.81471-03', '2026-11-17 22:05:10.814793-03', 13, 1);
INSERT INTO public.material (id_material, codigo_institucional, nombre, tipo, cantidad, marca, modelo, numero_serie, estado, observaciones, fecha_alta, fecha_actualizacion, id_cajonera, id_categoria) VALUES (9, '8C-0510', 'Equipo de respiración autónoma', 'unitario', 1, 'MSA', 'G1', NULL, 'activo', NULL, '2026-11-17 22:05:10.817368-03', '2026-11-17 22:05:10.817448-03', 1, 2);
INSERT INTO public.material (id_material, codigo_institucional, nombre, tipo, cantidad, marca, modelo, numero_serie, estado, observaciones, fecha_alta, fecha_actualizacion, id_cajonera, id_categoria) VALUES (10, '8C-0511', 'Equipo de respiración autónoma', 'unitario', 1, 'MSA', 'G1', NULL, 'activo', NULL, '2026-11-17 22:05:10.820023-03', '2026-11-17 22:05:10.820103-03', 1, 2);
INSERT INTO public.material (id_material, codigo_institucional, nombre, tipo, cantidad, marca, modelo, numero_serie, estado, observaciones, fecha_alta, fecha_actualizacion, id_cajonera, id_categoria) VALUES (11, '8C-0612', 'Separador hidráulico', 'unitario', 1, 'Holmatro', 'SP 4240', NULL, 'activo', NULL, '2026-11-17 22:05:10.8227-03', '2026-11-17 22:05:10.822778-03', 11, 5);
INSERT INTO public.material (id_material, codigo_institucional, nombre, tipo, cantidad, marca, modelo, numero_serie, estado, observaciones, fecha_alta, fecha_actualizacion, id_cajonera, id_categoria) VALUES (12, '8C-0701', 'Torre de iluminación portátil', 'unitario', 1, 'Peli', '9500', NULL, 'activo', NULL, '2026-11-17 22:05:10.825215-03', '2026-11-17 22:05:10.825293-03', 12, 6);
INSERT INTO public.material (id_material, codigo_institucional, nombre, tipo, cantidad, marca, modelo, numero_serie, estado, observaciones, fecha_alta, fecha_actualizacion, id_cajonera, id_categoria) VALUES (13, '8C-0215', 'Pitón regulable 50 mm', 'unitario', 1, 'Akron', 'Turbojet', NULL, 'activo', NULL, '2026-11-17 22:05:10.8283-03', '2026-11-17 22:05:10.828381-03', 2, 1);
INSERT INTO public.material (id_material, codigo_institucional, nombre, tipo, cantidad, marca, modelo, numero_serie, estado, observaciones, fecha_alta, fecha_actualizacion, id_cajonera, id_categoria) VALUES (14, '8C-0216', 'Pitón regulable 70 mm', 'unitario', 1, 'Akron', 'Turbojet', NULL, 'activo', NULL, '2026-11-17 22:05:10.831199-03', '2026-11-17 22:05:10.831281-03', 2, 1);
INSERT INTO public.material (id_material, codigo_institucional, nombre, tipo, cantidad, marca, modelo, numero_serie, estado, observaciones, fecha_alta, fecha_actualizacion, id_cajonera, id_categoria) VALUES (15, NULL, 'Guantes de nitrilo (caja)', 'granel', 12, NULL, NULL, NULL, 'activo', 'Material a granel: sin código institucional.', '2026-11-17 22:05:10.833829-03', '2026-11-17 22:05:10.833915-03', 14, 7);


ALTER TABLE public.material ENABLE TRIGGER ALL;

--
-- Data for Name: plan_revision; Type: TABLE DATA; Schema: public; Owner: -
--

ALTER TABLE public.plan_revision DISABLE TRIGGER ALL;

INSERT INTO public.plan_revision (id_plan, nombre, version, descripcion, frecuencia_valor, frecuencia_unidad, dias_tolerancia, exige_fotografia, activo, fecha_creacion) VALUES (1, 'Motobomba', 1, 'Encender en zona ventilada. Usar protección auditiva. Revisar según manual Honda WX15.', 1, 'semana', 1, true, true, '2026-11-17 22:05:10.835295-03');
INSERT INTO public.plan_revision (id_plan, nombre, version, descripcion, frecuencia_valor, frecuencia_unidad, dias_tolerancia, exige_fotografia, activo, fecha_creacion) VALUES (2, 'Detector de gases', 1, 'Realizar la prueba en aire limpio, fuera del cuartel. Registrar la lectura estable tras 60 segundos.', 1, 'mes', 2, true, true, '2026-11-17 22:05:10.837502-03');
INSERT INTO public.plan_revision (id_plan, nombre, version, descripcion, frecuencia_valor, frecuencia_unidad, dias_tolerancia, exige_fotografia, activo, fecha_creacion) VALUES (3, 'Motosierra', 1, 'Verificar con el freno de cadena activado.', 1, 'semana', 1, false, true, '2026-11-17 22:05:10.839687-03');
INSERT INTO public.plan_revision (id_plan, nombre, version, descripcion, frecuencia_valor, frecuencia_unidad, dias_tolerancia, exige_fotografia, activo, fecha_creacion) VALUES (4, 'Generador', 1, 'Conectar la carga de prueba (foco de 500 W) durante 5 minutos.', 2, 'semana', 2, false, true, '2026-11-17 22:05:10.840848-03');
INSERT INTO public.plan_revision (id_plan, nombre, version, descripcion, frecuencia_valor, frecuencia_unidad, dias_tolerancia, exige_fotografia, activo, fecha_creacion) VALUES (5, 'Herramienta hidráulica', 1, 'Revisar acoples y mangueras antes de operar la herramienta.', 1, 'mes', 3, false, true, '2026-11-17 22:05:10.842164-03');


ALTER TABLE public.plan_revision ENABLE TRIGGER ALL;

--
-- Data for Name: asignacion_plan; Type: TABLE DATA; Schema: public; Owner: -
--

ALTER TABLE public.asignacion_plan DISABLE TRIGGER ALL;

INSERT INTO public.asignacion_plan (id_asignacion, fecha_inicio, fecha_termino, activa, id_material, id_plan) VALUES (1, '2026-09-22', NULL, true, 1, 1);
INSERT INTO public.asignacion_plan (id_asignacion, fecha_inicio, fecha_termino, activa, id_material, id_plan) VALUES (2, '2026-08-25', NULL, true, 2, 2);
INSERT INTO public.asignacion_plan (id_asignacion, fecha_inicio, fecha_termino, activa, id_material, id_plan) VALUES (3, '2026-09-22', NULL, true, 3, 3);
INSERT INTO public.asignacion_plan (id_asignacion, fecha_inicio, fecha_termino, activa, id_material, id_plan) VALUES (4, '2026-09-22', NULL, true, 4, 4);
INSERT INTO public.asignacion_plan (id_asignacion, fecha_inicio, fecha_termino, activa, id_material, id_plan) VALUES (5, '2026-09-22', NULL, true, 5, 1);
INSERT INTO public.asignacion_plan (id_asignacion, fecha_inicio, fecha_termino, activa, id_material, id_plan) VALUES (6, '2026-08-25', NULL, true, 6, 5);
INSERT INTO public.asignacion_plan (id_asignacion, fecha_inicio, fecha_termino, activa, id_material, id_plan) VALUES (7, '2026-08-25', NULL, true, 7, 2);
INSERT INTO public.asignacion_plan (id_asignacion, fecha_inicio, fecha_termino, activa, id_material, id_plan) VALUES (8, '2026-10-06', NULL, true, 8, 1);
INSERT INTO public.asignacion_plan (id_asignacion, fecha_inicio, fecha_termino, activa, id_material, id_plan) VALUES (9, '2026-08-25', NULL, true, 11, 5);


ALTER TABLE public.asignacion_plan ENABLE TRIGGER ALL;

--
-- Data for Name: rol; Type: TABLE DATA; Schema: public; Owner: -
--

ALTER TABLE public.rol DISABLE TRIGGER ALL;

INSERT INTO public.rol (id_rol, nombre, descripcion, activo) VALUES (1, 'bombero', 'Voluntario: consulta el inventario, registra traslados y ejecuta sus revisiones.', true);
INSERT INTO public.rol (id_rol, nombre, descripcion, activo) VALUES (2, 'jefatura', 'Oficiales: gestionan material, planes, asignaciones, hallazgos y reportes.', true);
INSERT INTO public.rol (id_rol, nombre, descripcion, activo) VALUES (3, 'administrador', 'Bombero designado: administra usuarios, permisos, catálogos y bitácora.', true);


ALTER TABLE public.rol ENABLE TRIGGER ALL;

--
-- Data for Name: usuario; Type: TABLE DATA; Schema: public; Owner: -
--

ALTER TABLE public.usuario DISABLE TRIGGER ALL;

INSERT INTO public.usuario (id_usuario, rut, nombre, apellidos, correo, hash_contrasena, telefono, activo, fecha_creacion, ultimo_acceso, id_rol, foto_version) VALUES (1, 'SISTEMA', 'Sistema', 'SIREMA', 'sistema@sirema.local', '!UwwBk3555x5YpzooAy5L87d95FqQlKj0bgM9pSJx', NULL, false, '2026-11-17 22:03:55.403969-03', NULL, 1, NULL);
INSERT INTO public.usuario (id_usuario, rut, nombre, apellidos, correo, hash_contrasena, telefono, activo, fecha_creacion, ultimo_acceso, id_rol, foto_version) VALUES (2, '11.111.111-1', 'Ana', 'Torres Vidal', 'admin@sirema.local', 'argon2$argon2id$v=19$m=102400,t=2,p=8$MUZnMVpUU0VmSnJzYkQycTAxeVZSTg$KirNV3gk4tIt2/cVYKUO62gZpkK+9lVbjXWHjnkSDWo', '+56 9 5555 0000', true, '2026-11-17 22:05:10.58666-03', NULL, 3, NULL);
INSERT INTO public.usuario (id_usuario, rut, nombre, apellidos, correo, hash_contrasena, telefono, activo, fecha_creacion, ultimo_acceso, id_rol, foto_version) VALUES (3, '12.345.678-5', 'Carlos', 'Muñoz Reyes', 'jefatura@sirema.local', 'argon2$argon2id$v=19$m=102400,t=2,p=8$eXRiVG9xN2VxTk9mUm5OcFdIQ1Rleg$VKG1ba/mq32lP/N7WKZdtzB1lusxQY+dBRuTiJvxK1A', '+56 9 5555 0000', true, '2026-11-17 22:05:10.631603-03', NULL, 2, NULL);
INSERT INTO public.usuario (id_usuario, rut, nombre, apellidos, correo, hash_contrasena, telefono, activo, fecha_creacion, ultimo_acceso, id_rol, foto_version) VALUES (4, '15.555.555-6', 'Juan', 'Soto Pérez', 'j.soto@sirema.local', 'argon2$argon2id$v=19$m=102400,t=2,p=8$SGVqaG9vcUhQT2xTSUVsekR5TmNONw$U58nbwTv6MsihOwq9apXqXUt+o7tXpp9bqzfkpH6bnY', '+56 9 5555 0000', true, '2026-11-17 22:05:10.672334-03', NULL, 1, NULL);
INSERT INTO public.usuario (id_usuario, rut, nombre, apellidos, correo, hash_contrasena, telefono, activo, fecha_creacion, ultimo_acceso, id_rol, foto_version) VALUES (5, '16.666.666-K', 'María', 'Rivas Fuentes', 'm.rivas@sirema.local', 'argon2$argon2id$v=19$m=102400,t=2,p=8$cUt1cUFrc3NqUUFhNTZQOG43dlZ2Zw$9/npgZH4C3uhAmREECTTNAUNr6egfv5HlUnjBg72RXo', '+56 9 5555 0000', true, '2026-11-17 22:05:10.711242-03', NULL, 1, NULL);
INSERT INTO public.usuario (id_usuario, rut, nombre, apellidos, correo, hash_contrasena, telefono, activo, fecha_creacion, ultimo_acceso, id_rol, foto_version) VALUES (6, '17.777.777-3', 'Pedro', 'Lagos Herrera', 'p.lagos@sirema.local', 'argon2$argon2id$v=19$m=102400,t=2,p=8$bHVpbTVNak93SFVKZmp6aHI0OFFCWg$MRNWcDIO17NVihh9pCtmXpRwz0lnWryCJ0ipPpUlCR8', '+56 9 5555 0000', true, '2026-11-17 22:05:10.748682-03', NULL, 1, NULL);


ALTER TABLE public.usuario ENABLE TRIGGER ALL;

--
-- Data for Name: asignacion_responsable; Type: TABLE DATA; Schema: public; Owner: -
--

ALTER TABLE public.asignacion_responsable DISABLE TRIGGER ALL;

INSERT INTO public.asignacion_responsable (id_asignacion, id_usuario) VALUES (1, 4);
INSERT INTO public.asignacion_responsable (id_asignacion, id_usuario) VALUES (2, 4);
INSERT INTO public.asignacion_responsable (id_asignacion, id_usuario) VALUES (3, 4);
INSERT INTO public.asignacion_responsable (id_asignacion, id_usuario) VALUES (4, 4);
INSERT INTO public.asignacion_responsable (id_asignacion, id_usuario) VALUES (5, 5);
INSERT INTO public.asignacion_responsable (id_asignacion, id_usuario) VALUES (6, 6);
INSERT INTO public.asignacion_responsable (id_asignacion, id_usuario) VALUES (7, 5);
INSERT INTO public.asignacion_responsable (id_asignacion, id_usuario) VALUES (8, 4);
INSERT INTO public.asignacion_responsable (id_asignacion, id_usuario) VALUES (8, 6);
INSERT INTO public.asignacion_responsable (id_asignacion, id_usuario) VALUES (9, 6);


ALTER TABLE public.asignacion_responsable ENABLE TRIGGER ALL;

--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: -
--

ALTER TABLE public.auth_group DISABLE TRIGGER ALL;



ALTER TABLE public.auth_group ENABLE TRIGGER ALL;

--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: -
--

ALTER TABLE public.django_content_type DISABLE TRIGGER ALL;

INSERT INTO public.django_content_type (id, app_label, model) VALUES (1, 'auth', 'permission');
INSERT INTO public.django_content_type (id, app_label, model) VALUES (2, 'auth', 'group');
INSERT INTO public.django_content_type (id, app_label, model) VALUES (3, 'contenttypes', 'contenttype');
INSERT INTO public.django_content_type (id, app_label, model) VALUES (4, 'sessions', 'session');
INSERT INTO public.django_content_type (id, app_label, model) VALUES (5, 'axes', 'accessattempt');
INSERT INTO public.django_content_type (id, app_label, model) VALUES (6, 'axes', 'accesslog');
INSERT INTO public.django_content_type (id, app_label, model) VALUES (7, 'axes', 'accessfailurelog');
INSERT INTO public.django_content_type (id, app_label, model) VALUES (8, 'axes', 'accessattemptexpiration');
INSERT INTO public.django_content_type (id, app_label, model) VALUES (9, 'revisiones', 'planrevision');
INSERT INTO public.django_content_type (id, app_label, model) VALUES (10, 'revisiones', 'asignacionplan');
INSERT INTO public.django_content_type (id, app_label, model) VALUES (11, 'revisiones', 'puntocontrol');
INSERT INTO public.django_content_type (id, app_label, model) VALUES (12, 'revisiones', 'revision');
INSERT INTO public.django_content_type (id, app_label, model) VALUES (13, 'revisiones', 'resultadopunto');
INSERT INTO public.django_content_type (id, app_label, model) VALUES (14, 'revisiones', 'notificacion');
INSERT INTO public.django_content_type (id, app_label, model) VALUES (15, 'revisiones', 'hallazgo');
INSERT INTO public.django_content_type (id, app_label, model) VALUES (16, 'revisiones', 'fotografia');
INSERT INTO public.django_content_type (id, app_label, model) VALUES (17, 'revisiones', 'asignacionresponsable');
INSERT INTO public.django_content_type (id, app_label, model) VALUES (18, 'revisiones', 'revisionresponsable');
INSERT INTO public.django_content_type (id, app_label, model) VALUES (19, 'inventario', 'cajonera');
INSERT INTO public.django_content_type (id, app_label, model) VALUES (20, 'inventario', 'categoria');
INSERT INTO public.django_content_type (id, app_label, model) VALUES (21, 'inventario', 'material');
INSERT INTO public.django_content_type (id, app_label, model) VALUES (22, 'inventario', 'baja');
INSERT INTO public.django_content_type (id, app_label, model) VALUES (23, 'inventario', 'movimiento');
INSERT INTO public.django_content_type (id, app_label, model) VALUES (24, 'inventario', 'unidad');
INSERT INTO public.django_content_type (id, app_label, model) VALUES (25, 'accesos', 'permiso');
INSERT INTO public.django_content_type (id, app_label, model) VALUES (26, 'accesos', 'rol');
INSERT INTO public.django_content_type (id, app_label, model) VALUES (27, 'accesos', 'usuario');
INSERT INTO public.django_content_type (id, app_label, model) VALUES (28, 'accesos', 'rolpermiso');
INSERT INTO public.django_content_type (id, app_label, model) VALUES (29, 'accesos', 'eventoauditoria');
INSERT INTO public.django_content_type (id, app_label, model) VALUES (30, 'accesos', 'fotoperfil');


ALTER TABLE public.django_content_type ENABLE TRIGGER ALL;

--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: -
--

ALTER TABLE public.auth_permission DISABLE TRIGGER ALL;

INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (1, 'Can add permission', 1, 'add_permission');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (2, 'Can change permission', 1, 'change_permission');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (3, 'Can delete permission', 1, 'delete_permission');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (4, 'Can view permission', 1, 'view_permission');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (5, 'Can add group', 2, 'add_group');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (6, 'Can change group', 2, 'change_group');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (7, 'Can delete group', 2, 'delete_group');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (8, 'Can view group', 2, 'view_group');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (9, 'Can add content type', 3, 'add_contenttype');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (10, 'Can change content type', 3, 'change_contenttype');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (11, 'Can delete content type', 3, 'delete_contenttype');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (12, 'Can view content type', 3, 'view_contenttype');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (13, 'Can add session', 4, 'add_session');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (14, 'Can change session', 4, 'change_session');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (15, 'Can delete session', 4, 'delete_session');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (16, 'Can view session', 4, 'view_session');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (17, 'Can add access attempt', 5, 'add_accessattempt');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (18, 'Can change access attempt', 5, 'change_accessattempt');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (19, 'Can delete access attempt', 5, 'delete_accessattempt');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (20, 'Can view access attempt', 5, 'view_accessattempt');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (21, 'Can add access log', 6, 'add_accesslog');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (22, 'Can change access log', 6, 'change_accesslog');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (23, 'Can delete access log', 6, 'delete_accesslog');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (24, 'Can view access log', 6, 'view_accesslog');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (25, 'Can add access failure', 7, 'add_accessfailurelog');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (26, 'Can change access failure', 7, 'change_accessfailurelog');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (27, 'Can delete access failure', 7, 'delete_accessfailurelog');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (28, 'Can view access failure', 7, 'view_accessfailurelog');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (29, 'Can add access attempt expiration', 8, 'add_accessattemptexpiration');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (30, 'Can change access attempt expiration', 8, 'change_accessattemptexpiration');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (31, 'Can delete access attempt expiration', 8, 'delete_accessattemptexpiration');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (32, 'Can view access attempt expiration', 8, 'view_accessattemptexpiration');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (33, 'Can add plan de revisión', 9, 'add_planrevision');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (34, 'Can change plan de revisión', 9, 'change_planrevision');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (35, 'Can delete plan de revisión', 9, 'delete_planrevision');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (36, 'Can view plan de revisión', 9, 'view_planrevision');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (37, 'Can add asignacion plan', 10, 'add_asignacionplan');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (38, 'Can change asignacion plan', 10, 'change_asignacionplan');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (39, 'Can delete asignacion plan', 10, 'delete_asignacionplan');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (40, 'Can view asignacion plan', 10, 'view_asignacionplan');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (41, 'Can add punto control', 11, 'add_puntocontrol');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (42, 'Can change punto control', 11, 'change_puntocontrol');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (43, 'Can delete punto control', 11, 'delete_puntocontrol');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (44, 'Can view punto control', 11, 'view_puntocontrol');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (45, 'Can add revisión', 12, 'add_revision');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (46, 'Can change revisión', 12, 'change_revision');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (47, 'Can delete revisión', 12, 'delete_revision');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (48, 'Can view revisión', 12, 'view_revision');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (49, 'Can add resultado punto', 13, 'add_resultadopunto');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (50, 'Can change resultado punto', 13, 'change_resultadopunto');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (51, 'Can delete resultado punto', 13, 'delete_resultadopunto');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (52, 'Can view resultado punto', 13, 'view_resultadopunto');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (53, 'Can add notificación', 14, 'add_notificacion');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (54, 'Can change notificación', 14, 'change_notificacion');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (55, 'Can delete notificación', 14, 'delete_notificacion');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (56, 'Can view notificación', 14, 'view_notificacion');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (57, 'Can add hallazgo', 15, 'add_hallazgo');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (58, 'Can change hallazgo', 15, 'change_hallazgo');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (59, 'Can delete hallazgo', 15, 'delete_hallazgo');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (60, 'Can view hallazgo', 15, 'view_hallazgo');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (61, 'Can add fotografía', 16, 'add_fotografia');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (62, 'Can change fotografía', 16, 'change_fotografia');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (63, 'Can delete fotografía', 16, 'delete_fotografia');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (64, 'Can view fotografía', 16, 'view_fotografia');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (65, 'Can add asignacion responsable', 17, 'add_asignacionresponsable');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (66, 'Can change asignacion responsable', 17, 'change_asignacionresponsable');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (67, 'Can delete asignacion responsable', 17, 'delete_asignacionresponsable');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (68, 'Can view asignacion responsable', 17, 'view_asignacionresponsable');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (69, 'Can add revision responsable', 18, 'add_revisionresponsable');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (70, 'Can change revision responsable', 18, 'change_revisionresponsable');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (71, 'Can delete revision responsable', 18, 'delete_revisionresponsable');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (72, 'Can view revision responsable', 18, 'view_revisionresponsable');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (73, 'Can add cajonera', 19, 'add_cajonera');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (74, 'Can change cajonera', 19, 'change_cajonera');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (75, 'Can delete cajonera', 19, 'delete_cajonera');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (76, 'Can view cajonera', 19, 'view_cajonera');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (77, 'Can add categoría', 20, 'add_categoria');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (78, 'Can change categoría', 20, 'change_categoria');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (79, 'Can delete categoría', 20, 'delete_categoria');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (80, 'Can view categoría', 20, 'view_categoria');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (81, 'Can add material', 21, 'add_material');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (82, 'Can change material', 21, 'change_material');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (83, 'Can delete material', 21, 'delete_material');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (84, 'Can view material', 21, 'view_material');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (85, 'Can add baja', 22, 'add_baja');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (86, 'Can change baja', 22, 'change_baja');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (87, 'Can delete baja', 22, 'delete_baja');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (88, 'Can view baja', 22, 'view_baja');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (89, 'Can add movimiento', 23, 'add_movimiento');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (90, 'Can change movimiento', 23, 'change_movimiento');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (91, 'Can delete movimiento', 23, 'delete_movimiento');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (92, 'Can view movimiento', 23, 'view_movimiento');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (93, 'Can add unidad', 24, 'add_unidad');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (94, 'Can change unidad', 24, 'change_unidad');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (95, 'Can delete unidad', 24, 'delete_unidad');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (96, 'Can view unidad', 24, 'view_unidad');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (97, 'Can add permiso', 25, 'add_permiso');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (98, 'Can change permiso', 25, 'change_permiso');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (99, 'Can delete permiso', 25, 'delete_permiso');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (100, 'Can view permiso', 25, 'view_permiso');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (101, 'Can add rol', 26, 'add_rol');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (102, 'Can change rol', 26, 'change_rol');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (103, 'Can delete rol', 26, 'delete_rol');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (104, 'Can view rol', 26, 'view_rol');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (105, 'Can add usuario', 27, 'add_usuario');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (106, 'Can change usuario', 27, 'change_usuario');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (107, 'Can delete usuario', 27, 'delete_usuario');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (108, 'Can view usuario', 27, 'view_usuario');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (109, 'Can add rol permiso', 28, 'add_rolpermiso');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (110, 'Can change rol permiso', 28, 'change_rolpermiso');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (111, 'Can delete rol permiso', 28, 'delete_rolpermiso');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (112, 'Can view rol permiso', 28, 'view_rolpermiso');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (113, 'Can add evento auditoria', 29, 'add_eventoauditoria');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (114, 'Can change evento auditoria', 29, 'change_eventoauditoria');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (115, 'Can delete evento auditoria', 29, 'delete_eventoauditoria');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (116, 'Can view evento auditoria', 29, 'view_eventoauditoria');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (117, 'Can add foto perfil', 30, 'add_fotoperfil');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (118, 'Can change foto perfil', 30, 'change_fotoperfil');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (119, 'Can delete foto perfil', 30, 'delete_fotoperfil');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (120, 'Can view foto perfil', 30, 'view_fotoperfil');


ALTER TABLE public.auth_permission ENABLE TRIGGER ALL;

--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: -
--

ALTER TABLE public.auth_group_permissions DISABLE TRIGGER ALL;



ALTER TABLE public.auth_group_permissions ENABLE TRIGGER ALL;

--
-- Data for Name: baja; Type: TABLE DATA; Schema: public; Owner: -
--

ALTER TABLE public.baja DISABLE TRIGGER ALL;



ALTER TABLE public.baja ENABLE TRIGGER ALL;

--
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: -
--

ALTER TABLE public.django_migrations DISABLE TRIGGER ALL;

INSERT INTO public.django_migrations (id, app, name, applied) VALUES (1, 'accesos', '0001_initial', '2026-11-17 22:03:55.38256-03');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (2, 'accesos', '0002_datos_iniciales', '2026-11-17 22:03:55.404526-03');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (3, 'accesos', '0003_bitacora_inmutable', '2026-11-17 22:03:55.407205-03');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (4, 'accesos', '0004_usuario_foto_perfil', '2026-11-17 22:03:55.410298-03');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (5, 'accesos', '0005_usuario_sesion_activa', '2026-11-17 22:03:55.413507-03');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (6, 'accesos', '0006_quitar_sesion_activa', '2026-11-17 22:03:55.416879-03');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (7, 'accesos', '0007_foto_perfil_en_base', '2026-11-17 22:03:55.431828-03');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (8, 'accesos', '0008_permiso_respaldos', '2026-11-17 22:03:55.437484-03');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (9, 'contenttypes', '0001_initial', '2026-11-17 22:03:55.443077-03');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (10, 'contenttypes', '0002_remove_content_type_name', '2026-11-17 22:03:55.448242-03');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (11, 'auth', '0001_initial', '2026-11-17 22:03:55.471715-03');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (12, 'auth', '0002_alter_permission_name_max_length', '2026-11-17 22:03:55.474655-03');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (13, 'auth', '0003_alter_user_email_max_length', '2026-11-17 22:03:55.478262-03');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (14, 'auth', '0004_alter_user_username_opts', '2026-11-17 22:03:55.481405-03');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (15, 'auth', '0005_alter_user_last_login_null', '2026-11-17 22:03:55.484625-03');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (16, 'auth', '0006_require_contenttypes_0002', '2026-11-17 22:03:55.485738-03');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (17, 'auth', '0007_alter_validators_add_error_messages', '2026-11-17 22:03:55.488415-03');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (18, 'auth', '0008_alter_user_username_max_length', '2026-11-17 22:03:55.491319-03');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (19, 'auth', '0009_alter_user_last_name_max_length', '2026-11-17 22:03:55.494418-03');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (20, 'auth', '0010_alter_group_name_max_length', '2026-11-17 22:03:55.497954-03');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (21, 'auth', '0011_update_proxy_permissions', '2026-11-17 22:03:55.502502-03');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (22, 'auth', '0012_alter_user_first_name_max_length', '2026-11-17 22:03:55.505812-03');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (23, 'axes', '0001_initial', '2026-11-17 22:03:55.515251-03');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (24, 'axes', '0002_auto_20151217_2044', '2026-11-17 22:03:55.541153-03');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (25, 'axes', '0003_auto_20160322_0929', '2026-11-17 22:03:55.547619-03');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (26, 'axes', '0004_auto_20181024_1538', '2026-11-17 22:03:55.555176-03');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (27, 'axes', '0005_remove_accessattempt_trusted', '2026-11-17 22:03:55.558151-03');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (28, 'axes', '0006_remove_accesslog_trusted', '2026-11-17 22:03:55.561072-03');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (29, 'axes', '0007_alter_accessattempt_unique_together', '2026-11-17 22:03:55.571396-03');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (30, 'axes', '0008_accessfailurelog', '2026-11-17 22:03:55.585378-03');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (31, 'axes', '0009_add_session_hash', '2026-11-17 22:03:55.588129-03');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (32, 'axes', '0010_accessattemptexpiration', '2026-11-17 22:03:55.593638-03');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (33, 'inventario', '0001_initial', '2026-11-17 22:03:55.679508-03');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (34, 'revisiones', '0001_initial', '2026-11-17 22:03:55.949963-03');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (35, 'revisiones', '0002_fk_foto_resultado', '2026-11-17 22:03:55.961634-03');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (36, 'revisiones', '0003_varios_responsables', '2026-11-17 22:03:56.066153-03');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (37, 'sessions', '0001_initial', '2026-11-17 22:03:56.07475-03');


ALTER TABLE public.django_migrations ENABLE TRIGGER ALL;

--
-- Data for Name: evento_auditoria; Type: TABLE DATA; Schema: public; Owner: -
--

ALTER TABLE public.evento_auditoria DISABLE TRIGGER ALL;

INSERT INTO public.evento_auditoria (id_evento, fecha_hora, accion, entidad_afectada, id_registro, datos_anteriores, datos_nuevos, direccion_ip, id_usuario) VALUES (1, '2026-11-17 22:05:10.794957-03', 'alta', 'material', '1', NULL, '{"tipo": "unitario", "marca": "Honda", "estado": "activo", "modelo": "WX15", "nombre": "Motobomba portátil", "cantidad": 1, "fecha_alta": "2026-11-18T01:05:10.793728+00:00", "id_cajonera": 1, "id_material": 1, "id_categoria": 4, "numero_serie": null, "observaciones": null, "fecha_actualizacion": "2026-11-18T01:05:10.793888+00:00", "codigo_institucional": "8C-0112"}', NULL, 3);
INSERT INTO public.evento_auditoria (id_evento, fecha_hora, accion, entidad_afectada, id_registro, datos_anteriores, datos_nuevos, direccion_ip, id_usuario) VALUES (2, '2026-11-17 22:05:10.798253-03', 'alta', 'material', '2', NULL, '{"tipo": "unitario", "marca": "MSA", "estado": "activo", "modelo": "Altair 4XR", "nombre": "Detector multigas", "cantidad": 1, "fecha_alta": "2026-11-18T01:05:10.797377+00:00", "id_cajonera": 9, "id_material": 2, "id_categoria": 3, "numero_serie": null, "observaciones": null, "fecha_actualizacion": "2026-11-18T01:05:10.797470+00:00", "codigo_institucional": "8C-0457"}', NULL, 3);
INSERT INTO public.evento_auditoria (id_evento, fecha_hora, accion, entidad_afectada, id_registro, datos_anteriores, datos_nuevos, direccion_ip, id_usuario) VALUES (3, '2026-11-17 22:05:10.801472-03', 'alta', 'material', '3', NULL, '{"tipo": "unitario", "marca": "Stihl", "estado": "activo", "modelo": "MS 462 R", "nombre": "Motosierra de rescate", "cantidad": 1, "fecha_alta": "2026-11-18T01:05:10.800610+00:00", "id_cajonera": 3, "id_material": 3, "id_categoria": 5, "numero_serie": null, "observaciones": null, "fecha_actualizacion": "2026-11-18T01:05:10.800695+00:00", "codigo_institucional": "8C-0233"}', NULL, 3);
INSERT INTO public.evento_auditoria (id_evento, fecha_hora, accion, entidad_afectada, id_registro, datos_anteriores, datos_nuevos, direccion_ip, id_usuario) VALUES (4, '2026-11-17 22:05:10.804202-03', 'alta', 'material', '4', NULL, '{"tipo": "unitario", "marca": "Honda", "estado": "activo", "modelo": "EU22i", "nombre": "Generador eléctrico", "cantidad": 1, "fecha_alta": "2026-11-18T01:05:10.803537+00:00", "id_cajonera": 10, "id_material": 4, "id_categoria": 6, "numero_serie": null, "observaciones": null, "fecha_actualizacion": "2026-11-18T01:05:10.803618+00:00", "codigo_institucional": "8C-0390"}', NULL, 3);
INSERT INTO public.evento_auditoria (id_evento, fecha_hora, accion, entidad_afectada, id_registro, datos_anteriores, datos_nuevos, direccion_ip, id_usuario) VALUES (5, '2026-11-17 22:05:10.807305-03', 'alta', 'material', '5', NULL, '{"tipo": "unitario", "marca": "Tempest", "estado": "activo", "modelo": "GX200", "nombre": "Ventilador de presión positiva", "cantidad": 1, "fecha_alta": "2026-11-18T01:05:10.806563+00:00", "id_cajonera": 5, "id_material": 5, "id_categoria": 4, "numero_serie": null, "observaciones": null, "fecha_actualizacion": "2026-11-18T01:05:10.806644+00:00", "codigo_institucional": "8C-0101"}', NULL, 3);
INSERT INTO public.evento_auditoria (id_evento, fecha_hora, accion, entidad_afectada, id_registro, datos_anteriores, datos_nuevos, direccion_ip, id_usuario) VALUES (6, '2026-11-17 22:05:10.8099-03', 'alta', 'material', '6', NULL, '{"tipo": "unitario", "marca": "Holmatro", "estado": "activo", "modelo": "CU 4050", "nombre": "Equipo de corte hidráulico", "cantidad": 1, "fecha_alta": "2026-11-18T01:05:10.809214+00:00", "id_cajonera": 11, "id_material": 6, "id_categoria": 5, "numero_serie": null, "observaciones": null, "fecha_actualizacion": "2026-11-18T01:05:10.809296+00:00", "codigo_institucional": "8C-0305"}', NULL, 3);
INSERT INTO public.evento_auditoria (id_evento, fecha_hora, accion, entidad_afectada, id_registro, datos_anteriores, datos_nuevos, direccion_ip, id_usuario) VALUES (7, '2026-11-17 22:05:10.812667-03', 'alta', 'material', '7', NULL, '{"tipo": "unitario", "marca": "Dräger", "estado": "activo", "modelo": "Pac 6500", "nombre": "Detector monogas H2S", "cantidad": 1, "fecha_alta": "2026-11-18T01:05:10.812008+00:00", "id_cajonera": 9, "id_material": 7, "id_categoria": 3, "numero_serie": null, "observaciones": null, "fecha_actualizacion": "2026-11-18T01:05:10.812087+00:00", "codigo_institucional": "8C-0458"}', NULL, 3);
INSERT INTO public.evento_auditoria (id_evento, fecha_hora, accion, entidad_afectada, id_registro, datos_anteriores, datos_nuevos, direccion_ip, id_usuario) VALUES (8, '2026-11-17 22:05:10.815371-03', 'alta', 'material', '8', NULL, '{"tipo": "unitario", "marca": "Koshin", "estado": "activo", "modelo": "SEV-50X", "nombre": "Motobomba de achique", "cantidad": 1, "fecha_alta": "2026-11-18T01:05:10.814710+00:00", "id_cajonera": 13, "id_material": 8, "id_categoria": 1, "numero_serie": null, "observaciones": null, "fecha_actualizacion": "2026-11-18T01:05:10.814793+00:00", "codigo_institucional": "8C-0120"}', NULL, 3);
INSERT INTO public.evento_auditoria (id_evento, fecha_hora, accion, entidad_afectada, id_registro, datos_anteriores, datos_nuevos, direccion_ip, id_usuario) VALUES (9, '2026-11-17 22:05:10.818114-03', 'alta', 'material', '9', NULL, '{"tipo": "unitario", "marca": "MSA", "estado": "activo", "modelo": "G1", "nombre": "Equipo de respiración autónoma", "cantidad": 1, "fecha_alta": "2026-11-18T01:05:10.817368+00:00", "id_cajonera": 1, "id_material": 9, "id_categoria": 2, "numero_serie": null, "observaciones": null, "fecha_actualizacion": "2026-11-18T01:05:10.817448+00:00", "codigo_institucional": "8C-0510"}', NULL, 3);
INSERT INTO public.evento_auditoria (id_evento, fecha_hora, accion, entidad_afectada, id_registro, datos_anteriores, datos_nuevos, direccion_ip, id_usuario) VALUES (10, '2026-11-17 22:05:10.820674-03', 'alta', 'material', '10', NULL, '{"tipo": "unitario", "marca": "MSA", "estado": "activo", "modelo": "G1", "nombre": "Equipo de respiración autónoma", "cantidad": 1, "fecha_alta": "2026-11-18T01:05:10.820023+00:00", "id_cajonera": 1, "id_material": 10, "id_categoria": 2, "numero_serie": null, "observaciones": null, "fecha_actualizacion": "2026-11-18T01:05:10.820103+00:00", "codigo_institucional": "8C-0511"}', NULL, 3);
INSERT INTO public.evento_auditoria (id_evento, fecha_hora, accion, entidad_afectada, id_registro, datos_anteriores, datos_nuevos, direccion_ip, id_usuario) VALUES (11, '2026-11-17 22:05:10.823354-03', 'alta', 'material', '11', NULL, '{"tipo": "unitario", "marca": "Holmatro", "estado": "activo", "modelo": "SP 4240", "nombre": "Separador hidráulico", "cantidad": 1, "fecha_alta": "2026-11-18T01:05:10.822700+00:00", "id_cajonera": 11, "id_material": 11, "id_categoria": 5, "numero_serie": null, "observaciones": null, "fecha_actualizacion": "2026-11-18T01:05:10.822778+00:00", "codigo_institucional": "8C-0612"}', NULL, 3);
INSERT INTO public.evento_auditoria (id_evento, fecha_hora, accion, entidad_afectada, id_registro, datos_anteriores, datos_nuevos, direccion_ip, id_usuario) VALUES (12, '2026-11-17 22:05:10.8259-03', 'alta', 'material', '12', NULL, '{"tipo": "unitario", "marca": "Peli", "estado": "activo", "modelo": "9500", "nombre": "Torre de iluminación portátil", "cantidad": 1, "fecha_alta": "2026-11-18T01:05:10.825215+00:00", "id_cajonera": 12, "id_material": 12, "id_categoria": 6, "numero_serie": null, "observaciones": null, "fecha_actualizacion": "2026-11-18T01:05:10.825293+00:00", "codigo_institucional": "8C-0701"}', NULL, 3);
INSERT INTO public.evento_auditoria (id_evento, fecha_hora, accion, entidad_afectada, id_registro, datos_anteriores, datos_nuevos, direccion_ip, id_usuario) VALUES (13, '2026-11-17 22:05:10.828971-03', 'alta', 'material', '13', NULL, '{"tipo": "unitario", "marca": "Akron", "estado": "activo", "modelo": "Turbojet", "nombre": "Pitón regulable 50 mm", "cantidad": 1, "fecha_alta": "2026-11-18T01:05:10.828300+00:00", "id_cajonera": 2, "id_material": 13, "id_categoria": 1, "numero_serie": null, "observaciones": null, "fecha_actualizacion": "2026-11-18T01:05:10.828381+00:00", "codigo_institucional": "8C-0215"}', NULL, 3);
INSERT INTO public.evento_auditoria (id_evento, fecha_hora, accion, entidad_afectada, id_registro, datos_anteriores, datos_nuevos, direccion_ip, id_usuario) VALUES (14, '2026-11-17 22:05:10.831983-03', 'alta', 'material', '14', NULL, '{"tipo": "unitario", "marca": "Akron", "estado": "activo", "modelo": "Turbojet", "nombre": "Pitón regulable 70 mm", "cantidad": 1, "fecha_alta": "2026-11-18T01:05:10.831199+00:00", "id_cajonera": 2, "id_material": 14, "id_categoria": 1, "numero_serie": null, "observaciones": null, "fecha_actualizacion": "2026-11-18T01:05:10.831281+00:00", "codigo_institucional": "8C-0216"}', NULL, 3);
INSERT INTO public.evento_auditoria (id_evento, fecha_hora, accion, entidad_afectada, id_registro, datos_anteriores, datos_nuevos, direccion_ip, id_usuario) VALUES (15, '2026-11-17 22:05:10.834789-03', 'alta', 'material', '15', NULL, '{"tipo": "granel", "marca": null, "estado": "activo", "modelo": null, "nombre": "Guantes de nitrilo (caja)", "cantidad": 12, "fecha_alta": "2026-11-18T01:05:10.833829+00:00", "id_cajonera": 14, "id_material": 15, "id_categoria": 7, "numero_serie": null, "observaciones": "Material a granel: sin código institucional.", "fecha_actualizacion": "2026-11-18T01:05:10.833915+00:00", "codigo_institucional": null}', NULL, 3);
INSERT INTO public.evento_auditoria (id_evento, fecha_hora, accion, entidad_afectada, id_registro, datos_anteriores, datos_nuevos, direccion_ip, id_usuario) VALUES (16, '2026-11-17 22:05:10.869302-03', 'alta', 'revision', '1', NULL, '{"fecha_limite": "2026-09-23", "id_asignacion": 1, "fecha_programada": "2026-09-22", "id_usuarios_responsables": [4]}', NULL, 1);
INSERT INTO public.evento_auditoria (id_evento, fecha_hora, accion, entidad_afectada, id_registro, datos_anteriores, datos_nuevos, direccion_ip, id_usuario) VALUES (17, '2026-11-17 22:05:10.874242-03', 'alta', 'revision', '2', NULL, '{"fecha_limite": "2026-09-30", "id_asignacion": 1, "fecha_programada": "2026-09-29", "id_usuarios_responsables": [4]}', NULL, 1);
INSERT INTO public.evento_auditoria (id_evento, fecha_hora, accion, entidad_afectada, id_registro, datos_anteriores, datos_nuevos, direccion_ip, id_usuario) VALUES (18, '2026-11-17 22:05:10.87783-03', 'alta', 'revision', '3', NULL, '{"fecha_limite": "2026-10-07", "id_asignacion": 1, "fecha_programada": "2026-10-06", "id_usuarios_responsables": [4]}', NULL, 1);
INSERT INTO public.evento_auditoria (id_evento, fecha_hora, accion, entidad_afectada, id_registro, datos_anteriores, datos_nuevos, direccion_ip, id_usuario) VALUES (19, '2026-11-17 22:05:10.882081-03', 'alta', 'revision', '4', NULL, '{"fecha_limite": "2026-10-14", "id_asignacion": 1, "fecha_programada": "2026-10-13", "id_usuarios_responsables": [4]}', NULL, 1);
INSERT INTO public.evento_auditoria (id_evento, fecha_hora, accion, entidad_afectada, id_registro, datos_anteriores, datos_nuevos, direccion_ip, id_usuario) VALUES (20, '2026-11-17 22:05:10.885679-03', 'alta', 'revision', '5', NULL, '{"fecha_limite": "2026-10-21", "id_asignacion": 1, "fecha_programada": "2026-10-20", "id_usuarios_responsables": [4]}', NULL, 1);
INSERT INTO public.evento_auditoria (id_evento, fecha_hora, accion, entidad_afectada, id_registro, datos_anteriores, datos_nuevos, direccion_ip, id_usuario) VALUES (21, '2026-11-17 22:05:10.889508-03', 'alta', 'revision', '6', NULL, '{"fecha_limite": "2026-10-28", "id_asignacion": 1, "fecha_programada": "2026-10-27", "id_usuarios_responsables": [4]}', NULL, 1);
INSERT INTO public.evento_auditoria (id_evento, fecha_hora, accion, entidad_afectada, id_registro, datos_anteriores, datos_nuevos, direccion_ip, id_usuario) VALUES (22, '2026-11-17 22:05:10.892878-03', 'alta', 'revision', '7', NULL, '{"fecha_limite": "2026-11-04", "id_asignacion": 1, "fecha_programada": "2026-11-03", "id_usuarios_responsables": [4]}', NULL, 1);
INSERT INTO public.evento_auditoria (id_evento, fecha_hora, accion, entidad_afectada, id_registro, datos_anteriores, datos_nuevos, direccion_ip, id_usuario) VALUES (23, '2026-11-17 22:05:10.896744-03', 'alta', 'revision', '8', NULL, '{"fecha_limite": "2026-11-11", "id_asignacion": 1, "fecha_programada": "2026-11-10", "id_usuarios_responsables": [4]}', NULL, 1);
INSERT INTO public.evento_auditoria (id_evento, fecha_hora, accion, entidad_afectada, id_registro, datos_anteriores, datos_nuevos, direccion_ip, id_usuario) VALUES (24, '2026-11-17 22:05:10.901636-03', 'alta', 'revision', '9', NULL, '{"fecha_limite": "2026-11-18", "id_asignacion": 1, "fecha_programada": "2026-11-17", "id_usuarios_responsables": [4]}', NULL, 1);
INSERT INTO public.evento_auditoria (id_evento, fecha_hora, accion, entidad_afectada, id_registro, datos_anteriores, datos_nuevos, direccion_ip, id_usuario) VALUES (25, '2026-11-17 22:05:10.905689-03', 'alta', 'revision', '10', NULL, '{"fecha_limite": "2026-11-25", "id_asignacion": 1, "fecha_programada": "2026-11-24", "id_usuarios_responsables": [4]}', NULL, 1);
INSERT INTO public.evento_auditoria (id_evento, fecha_hora, accion, entidad_afectada, id_registro, datos_anteriores, datos_nuevos, direccion_ip, id_usuario) VALUES (26, '2026-11-17 22:05:10.911545-03', 'alta', 'revision', '11', NULL, '{"fecha_limite": "2026-08-27", "id_asignacion": 2, "fecha_programada": "2026-08-25", "id_usuarios_responsables": [4]}', NULL, 1);
INSERT INTO public.evento_auditoria (id_evento, fecha_hora, accion, entidad_afectada, id_registro, datos_anteriores, datos_nuevos, direccion_ip, id_usuario) VALUES (27, '2026-11-17 22:05:10.91613-03', 'alta', 'revision', '12', NULL, '{"fecha_limite": "2026-09-27", "id_asignacion": 2, "fecha_programada": "2026-09-25", "id_usuarios_responsables": [4]}', NULL, 1);
INSERT INTO public.evento_auditoria (id_evento, fecha_hora, accion, entidad_afectada, id_registro, datos_anteriores, datos_nuevos, direccion_ip, id_usuario) VALUES (28, '2026-11-17 22:05:10.919918-03', 'alta', 'revision', '13', NULL, '{"fecha_limite": "2026-10-27", "id_asignacion": 2, "fecha_programada": "2026-10-25", "id_usuarios_responsables": [4]}', NULL, 1);
INSERT INTO public.evento_auditoria (id_evento, fecha_hora, accion, entidad_afectada, id_registro, datos_anteriores, datos_nuevos, direccion_ip, id_usuario) VALUES (29, '2026-11-17 22:05:10.924741-03', 'alta', 'revision', '14', NULL, '{"fecha_limite": "2026-09-23", "id_asignacion": 3, "fecha_programada": "2026-09-22", "id_usuarios_responsables": [4]}', NULL, 1);
INSERT INTO public.evento_auditoria (id_evento, fecha_hora, accion, entidad_afectada, id_registro, datos_anteriores, datos_nuevos, direccion_ip, id_usuario) VALUES (30, '2026-11-17 22:05:10.929588-03', 'alta', 'revision', '15', NULL, '{"fecha_limite": "2026-09-30", "id_asignacion": 3, "fecha_programada": "2026-09-29", "id_usuarios_responsables": [4]}', NULL, 1);
INSERT INTO public.evento_auditoria (id_evento, fecha_hora, accion, entidad_afectada, id_registro, datos_anteriores, datos_nuevos, direccion_ip, id_usuario) VALUES (31, '2026-11-17 22:05:10.933354-03', 'alta', 'revision', '16', NULL, '{"fecha_limite": "2026-10-07", "id_asignacion": 3, "fecha_programada": "2026-10-06", "id_usuarios_responsables": [4]}', NULL, 1);
INSERT INTO public.evento_auditoria (id_evento, fecha_hora, accion, entidad_afectada, id_registro, datos_anteriores, datos_nuevos, direccion_ip, id_usuario) VALUES (32, '2026-11-17 22:05:10.937835-03', 'alta', 'revision', '17', NULL, '{"fecha_limite": "2026-10-14", "id_asignacion": 3, "fecha_programada": "2026-10-13", "id_usuarios_responsables": [4]}', NULL, 1);
INSERT INTO public.evento_auditoria (id_evento, fecha_hora, accion, entidad_afectada, id_registro, datos_anteriores, datos_nuevos, direccion_ip, id_usuario) VALUES (33, '2026-11-17 22:05:10.942384-03', 'alta', 'revision', '18', NULL, '{"fecha_limite": "2026-10-21", "id_asignacion": 3, "fecha_programada": "2026-10-20", "id_usuarios_responsables": [4]}', NULL, 1);
INSERT INTO public.evento_auditoria (id_evento, fecha_hora, accion, entidad_afectada, id_registro, datos_anteriores, datos_nuevos, direccion_ip, id_usuario) VALUES (34, '2026-11-17 22:05:10.946174-03', 'alta', 'revision', '19', NULL, '{"fecha_limite": "2026-10-28", "id_asignacion": 3, "fecha_programada": "2026-10-27", "id_usuarios_responsables": [4]}', NULL, 1);
INSERT INTO public.evento_auditoria (id_evento, fecha_hora, accion, entidad_afectada, id_registro, datos_anteriores, datos_nuevos, direccion_ip, id_usuario) VALUES (35, '2026-11-17 22:05:10.950141-03', 'alta', 'revision', '20', NULL, '{"fecha_limite": "2026-11-04", "id_asignacion": 3, "fecha_programada": "2026-11-03", "id_usuarios_responsables": [4]}', NULL, 1);
INSERT INTO public.evento_auditoria (id_evento, fecha_hora, accion, entidad_afectada, id_registro, datos_anteriores, datos_nuevos, direccion_ip, id_usuario) VALUES (36, '2026-11-17 22:05:10.95343-03', 'alta', 'revision', '21', NULL, '{"fecha_limite": "2026-11-11", "id_asignacion": 3, "fecha_programada": "2026-11-10", "id_usuarios_responsables": [4]}', NULL, 1);
INSERT INTO public.evento_auditoria (id_evento, fecha_hora, accion, entidad_afectada, id_registro, datos_anteriores, datos_nuevos, direccion_ip, id_usuario) VALUES (37, '2026-11-17 22:05:10.961268-03', 'alta', 'revision', '22', NULL, '{"fecha_limite": "2026-11-18", "id_asignacion": 3, "fecha_programada": "2026-11-17", "id_usuarios_responsables": [4]}', NULL, 1);
INSERT INTO public.evento_auditoria (id_evento, fecha_hora, accion, entidad_afectada, id_registro, datos_anteriores, datos_nuevos, direccion_ip, id_usuario) VALUES (38, '2026-11-17 22:05:10.966638-03', 'alta', 'revision', '23', NULL, '{"fecha_limite": "2026-11-25", "id_asignacion": 3, "fecha_programada": "2026-11-24", "id_usuarios_responsables": [4]}', NULL, 1);
INSERT INTO public.evento_auditoria (id_evento, fecha_hora, accion, entidad_afectada, id_registro, datos_anteriores, datos_nuevos, direccion_ip, id_usuario) VALUES (39, '2026-11-17 22:05:10.973364-03', 'alta', 'revision', '24', NULL, '{"fecha_limite": "2026-09-24", "id_asignacion": 4, "fecha_programada": "2026-09-22", "id_usuarios_responsables": [4]}', NULL, 1);
INSERT INTO public.evento_auditoria (id_evento, fecha_hora, accion, entidad_afectada, id_registro, datos_anteriores, datos_nuevos, direccion_ip, id_usuario) VALUES (40, '2026-11-17 22:05:10.9781-03', 'alta', 'revision', '25', NULL, '{"fecha_limite": "2026-10-08", "id_asignacion": 4, "fecha_programada": "2026-10-06", "id_usuarios_responsables": [4]}', NULL, 1);
INSERT INTO public.evento_auditoria (id_evento, fecha_hora, accion, entidad_afectada, id_registro, datos_anteriores, datos_nuevos, direccion_ip, id_usuario) VALUES (41, '2026-11-17 22:05:10.981448-03', 'alta', 'revision', '26', NULL, '{"fecha_limite": "2026-10-22", "id_asignacion": 4, "fecha_programada": "2026-10-20", "id_usuarios_responsables": [4]}', NULL, 1);
INSERT INTO public.evento_auditoria (id_evento, fecha_hora, accion, entidad_afectada, id_registro, datos_anteriores, datos_nuevos, direccion_ip, id_usuario) VALUES (42, '2026-11-17 22:05:10.984802-03', 'alta', 'revision', '27', NULL, '{"fecha_limite": "2026-11-05", "id_asignacion": 4, "fecha_programada": "2026-11-03", "id_usuarios_responsables": [4]}', NULL, 1);
INSERT INTO public.evento_auditoria (id_evento, fecha_hora, accion, entidad_afectada, id_registro, datos_anteriores, datos_nuevos, direccion_ip, id_usuario) VALUES (43, '2026-11-17 22:05:10.988908-03', 'alta', 'revision', '28', NULL, '{"fecha_limite": "2026-11-19", "id_asignacion": 4, "fecha_programada": "2026-11-17", "id_usuarios_responsables": [4]}', NULL, 1);
INSERT INTO public.evento_auditoria (id_evento, fecha_hora, accion, entidad_afectada, id_registro, datos_anteriores, datos_nuevos, direccion_ip, id_usuario) VALUES (44, '2026-11-17 22:05:10.993486-03', 'alta', 'revision', '29', NULL, '{"fecha_limite": "2026-09-23", "id_asignacion": 5, "fecha_programada": "2026-09-22", "id_usuarios_responsables": [5]}', NULL, 1);
INSERT INTO public.evento_auditoria (id_evento, fecha_hora, accion, entidad_afectada, id_registro, datos_anteriores, datos_nuevos, direccion_ip, id_usuario) VALUES (45, '2026-11-17 22:05:10.997688-03', 'alta', 'revision', '30', NULL, '{"fecha_limite": "2026-09-30", "id_asignacion": 5, "fecha_programada": "2026-09-29", "id_usuarios_responsables": [5]}', NULL, 1);
INSERT INTO public.evento_auditoria (id_evento, fecha_hora, accion, entidad_afectada, id_registro, datos_anteriores, datos_nuevos, direccion_ip, id_usuario) VALUES (46, '2026-11-17 22:05:11.001365-03', 'alta', 'revision', '31', NULL, '{"fecha_limite": "2026-10-07", "id_asignacion": 5, "fecha_programada": "2026-10-06", "id_usuarios_responsables": [5]}', NULL, 1);
INSERT INTO public.evento_auditoria (id_evento, fecha_hora, accion, entidad_afectada, id_registro, datos_anteriores, datos_nuevos, direccion_ip, id_usuario) VALUES (47, '2026-11-17 22:05:11.005095-03', 'alta', 'revision', '32', NULL, '{"fecha_limite": "2026-10-14", "id_asignacion": 5, "fecha_programada": "2026-10-13", "id_usuarios_responsables": [5]}', NULL, 1);
INSERT INTO public.evento_auditoria (id_evento, fecha_hora, accion, entidad_afectada, id_registro, datos_anteriores, datos_nuevos, direccion_ip, id_usuario) VALUES (48, '2026-11-17 22:05:11.008757-03', 'alta', 'revision', '33', NULL, '{"fecha_limite": "2026-10-21", "id_asignacion": 5, "fecha_programada": "2026-10-20", "id_usuarios_responsables": [5]}', NULL, 1);
INSERT INTO public.evento_auditoria (id_evento, fecha_hora, accion, entidad_afectada, id_registro, datos_anteriores, datos_nuevos, direccion_ip, id_usuario) VALUES (49, '2026-11-17 22:05:11.012128-03', 'alta', 'revision', '34', NULL, '{"fecha_limite": "2026-10-28", "id_asignacion": 5, "fecha_programada": "2026-10-27", "id_usuarios_responsables": [5]}', NULL, 1);
INSERT INTO public.evento_auditoria (id_evento, fecha_hora, accion, entidad_afectada, id_registro, datos_anteriores, datos_nuevos, direccion_ip, id_usuario) VALUES (50, '2026-11-17 22:05:11.015409-03', 'alta', 'revision', '35', NULL, '{"fecha_limite": "2026-11-04", "id_asignacion": 5, "fecha_programada": "2026-11-03", "id_usuarios_responsables": [5]}', NULL, 1);
INSERT INTO public.evento_auditoria (id_evento, fecha_hora, accion, entidad_afectada, id_registro, datos_anteriores, datos_nuevos, direccion_ip, id_usuario) VALUES (51, '2026-11-17 22:05:11.019088-03', 'alta', 'revision', '36', NULL, '{"fecha_limite": "2026-11-11", "id_asignacion": 5, "fecha_programada": "2026-11-10", "id_usuarios_responsables": [5]}', NULL, 1);
INSERT INTO public.evento_auditoria (id_evento, fecha_hora, accion, entidad_afectada, id_registro, datos_anteriores, datos_nuevos, direccion_ip, id_usuario) VALUES (52, '2026-11-17 22:05:11.022445-03', 'alta', 'revision', '37', NULL, '{"fecha_limite": "2026-11-18", "id_asignacion": 5, "fecha_programada": "2026-11-17", "id_usuarios_responsables": [5]}', NULL, 1);
INSERT INTO public.evento_auditoria (id_evento, fecha_hora, accion, entidad_afectada, id_registro, datos_anteriores, datos_nuevos, direccion_ip, id_usuario) VALUES (53, '2026-11-17 22:05:11.025764-03', 'alta', 'revision', '38', NULL, '{"fecha_limite": "2026-11-25", "id_asignacion": 5, "fecha_programada": "2026-11-24", "id_usuarios_responsables": [5]}', NULL, 1);
INSERT INTO public.evento_auditoria (id_evento, fecha_hora, accion, entidad_afectada, id_registro, datos_anteriores, datos_nuevos, direccion_ip, id_usuario) VALUES (54, '2026-11-17 22:05:11.030435-03', 'alta', 'revision', '39', NULL, '{"fecha_limite": "2026-08-28", "id_asignacion": 6, "fecha_programada": "2026-08-25", "id_usuarios_responsables": [6]}', NULL, 1);
INSERT INTO public.evento_auditoria (id_evento, fecha_hora, accion, entidad_afectada, id_registro, datos_anteriores, datos_nuevos, direccion_ip, id_usuario) VALUES (55, '2026-11-17 22:05:11.037454-03', 'alta', 'revision', '40', NULL, '{"fecha_limite": "2026-09-28", "id_asignacion": 6, "fecha_programada": "2026-09-25", "id_usuarios_responsables": [6]}', NULL, 1);
INSERT INTO public.evento_auditoria (id_evento, fecha_hora, accion, entidad_afectada, id_registro, datos_anteriores, datos_nuevos, direccion_ip, id_usuario) VALUES (56, '2026-11-17 22:05:11.041795-03', 'alta', 'revision', '41', NULL, '{"fecha_limite": "2026-10-28", "id_asignacion": 6, "fecha_programada": "2026-10-25", "id_usuarios_responsables": [6]}', NULL, 1);
INSERT INTO public.evento_auditoria (id_evento, fecha_hora, accion, entidad_afectada, id_registro, datos_anteriores, datos_nuevos, direccion_ip, id_usuario) VALUES (57, '2026-11-17 22:05:11.046821-03', 'alta', 'revision', '42', NULL, '{"fecha_limite": "2026-08-27", "id_asignacion": 7, "fecha_programada": "2026-08-25", "id_usuarios_responsables": [5]}', NULL, 1);
INSERT INTO public.evento_auditoria (id_evento, fecha_hora, accion, entidad_afectada, id_registro, datos_anteriores, datos_nuevos, direccion_ip, id_usuario) VALUES (58, '2026-11-17 22:05:11.051381-03', 'alta', 'revision', '43', NULL, '{"fecha_limite": "2026-09-27", "id_asignacion": 7, "fecha_programada": "2026-09-25", "id_usuarios_responsables": [5]}', NULL, 1);
INSERT INTO public.evento_auditoria (id_evento, fecha_hora, accion, entidad_afectada, id_registro, datos_anteriores, datos_nuevos, direccion_ip, id_usuario) VALUES (59, '2026-11-17 22:05:11.05475-03', 'alta', 'revision', '44', NULL, '{"fecha_limite": "2026-10-27", "id_asignacion": 7, "fecha_programada": "2026-10-25", "id_usuarios_responsables": [5]}', NULL, 1);
INSERT INTO public.evento_auditoria (id_evento, fecha_hora, accion, entidad_afectada, id_registro, datos_anteriores, datos_nuevos, direccion_ip, id_usuario) VALUES (60, '2026-11-17 22:05:11.059572-03', 'alta', 'revision', '45', NULL, '{"fecha_limite": "2026-10-07", "id_asignacion": 8, "fecha_programada": "2026-10-06", "id_usuarios_responsables": [4, 6]}', NULL, 1);
INSERT INTO public.evento_auditoria (id_evento, fecha_hora, accion, entidad_afectada, id_registro, datos_anteriores, datos_nuevos, direccion_ip, id_usuario) VALUES (61, '2026-11-17 22:05:11.065075-03', 'alta', 'revision', '46', NULL, '{"fecha_limite": "2026-10-14", "id_asignacion": 8, "fecha_programada": "2026-10-13", "id_usuarios_responsables": [4, 6]}', NULL, 1);
INSERT INTO public.evento_auditoria (id_evento, fecha_hora, accion, entidad_afectada, id_registro, datos_anteriores, datos_nuevos, direccion_ip, id_usuario) VALUES (62, '2026-11-17 22:05:11.072329-03', 'alta', 'revision', '47', NULL, '{"fecha_limite": "2026-10-21", "id_asignacion": 8, "fecha_programada": "2026-10-20", "id_usuarios_responsables": [4, 6]}', NULL, 1);
INSERT INTO public.evento_auditoria (id_evento, fecha_hora, accion, entidad_afectada, id_registro, datos_anteriores, datos_nuevos, direccion_ip, id_usuario) VALUES (63, '2026-11-17 22:05:11.076673-03', 'alta', 'revision', '48', NULL, '{"fecha_limite": "2026-10-28", "id_asignacion": 8, "fecha_programada": "2026-10-27", "id_usuarios_responsables": [4, 6]}', NULL, 1);
INSERT INTO public.evento_auditoria (id_evento, fecha_hora, accion, entidad_afectada, id_registro, datos_anteriores, datos_nuevos, direccion_ip, id_usuario) VALUES (64, '2026-11-17 22:05:11.08135-03', 'alta', 'revision', '49', NULL, '{"fecha_limite": "2026-11-04", "id_asignacion": 8, "fecha_programada": "2026-11-03", "id_usuarios_responsables": [4, 6]}', NULL, 1);
INSERT INTO public.evento_auditoria (id_evento, fecha_hora, accion, entidad_afectada, id_registro, datos_anteriores, datos_nuevos, direccion_ip, id_usuario) VALUES (65, '2026-11-17 22:05:11.086171-03', 'alta', 'revision', '50', NULL, '{"fecha_limite": "2026-11-11", "id_asignacion": 8, "fecha_programada": "2026-11-10", "id_usuarios_responsables": [4, 6]}', NULL, 1);
INSERT INTO public.evento_auditoria (id_evento, fecha_hora, accion, entidad_afectada, id_registro, datos_anteriores, datos_nuevos, direccion_ip, id_usuario) VALUES (66, '2026-11-17 22:05:11.090797-03', 'alta', 'revision', '51', NULL, '{"fecha_limite": "2026-11-18", "id_asignacion": 8, "fecha_programada": "2026-11-17", "id_usuarios_responsables": [4, 6]}', NULL, 1);
INSERT INTO public.evento_auditoria (id_evento, fecha_hora, accion, entidad_afectada, id_registro, datos_anteriores, datos_nuevos, direccion_ip, id_usuario) VALUES (67, '2026-11-17 22:05:11.095126-03', 'alta', 'revision', '52', NULL, '{"fecha_limite": "2026-11-25", "id_asignacion": 8, "fecha_programada": "2026-11-24", "id_usuarios_responsables": [4, 6]}', NULL, 1);
INSERT INTO public.evento_auditoria (id_evento, fecha_hora, accion, entidad_afectada, id_registro, datos_anteriores, datos_nuevos, direccion_ip, id_usuario) VALUES (68, '2026-11-17 22:05:11.101226-03', 'alta', 'revision', '53', NULL, '{"fecha_limite": "2026-08-28", "id_asignacion": 9, "fecha_programada": "2026-08-25", "id_usuarios_responsables": [6]}', NULL, 1);
INSERT INTO public.evento_auditoria (id_evento, fecha_hora, accion, entidad_afectada, id_registro, datos_anteriores, datos_nuevos, direccion_ip, id_usuario) VALUES (69, '2026-11-17 22:05:11.105518-03', 'alta', 'revision', '54', NULL, '{"fecha_limite": "2026-09-28", "id_asignacion": 9, "fecha_programada": "2026-09-25", "id_usuarios_responsables": [6]}', NULL, 1);
INSERT INTO public.evento_auditoria (id_evento, fecha_hora, accion, entidad_afectada, id_registro, datos_anteriores, datos_nuevos, direccion_ip, id_usuario) VALUES (70, '2026-11-17 22:05:11.109137-03', 'alta', 'revision', '55', NULL, '{"fecha_limite": "2026-10-28", "id_asignacion": 9, "fecha_programada": "2026-10-25", "id_usuarios_responsables": [6]}', NULL, 1);
INSERT INTO public.evento_auditoria (id_evento, fecha_hora, accion, entidad_afectada, id_registro, datos_anteriores, datos_nuevos, direccion_ip, id_usuario) VALUES (71, '2026-11-17 22:05:11.604516-03', 'modificacion', 'revision', '50', '{"estado": "pendiente"}', '{"estado": "vencida"}', NULL, 1);
INSERT INTO public.evento_auditoria (id_evento, fecha_hora, accion, entidad_afectada, id_registro, datos_anteriores, datos_nuevos, direccion_ip, id_usuario) VALUES (72, '2026-11-17 22:05:11.606889-03', 'modificacion', 'revision', '35', '{"estado": "pendiente"}', '{"estado": "vencida"}', NULL, 1);
INSERT INTO public.evento_auditoria (id_evento, fecha_hora, accion, entidad_afectada, id_registro, datos_anteriores, datos_nuevos, direccion_ip, id_usuario) VALUES (73, '2026-11-17 22:05:11.608872-03', 'modificacion', 'revision', '16', '{"estado": "pendiente"}', '{"estado": "vencida"}', NULL, 1);
INSERT INTO public.evento_auditoria (id_evento, fecha_hora, accion, entidad_afectada, id_registro, datos_anteriores, datos_nuevos, direccion_ip, id_usuario) VALUES (74, '2026-11-17 22:05:11.610742-03', 'modificacion', 'revision', '15', '{"estado": "pendiente"}', '{"estado": "vencida"}', NULL, 1);


ALTER TABLE public.evento_auditoria ENABLE TRIGGER ALL;

--
-- Data for Name: foto_perfil; Type: TABLE DATA; Schema: public; Owner: -
--

ALTER TABLE public.foto_perfil DISABLE TRIGGER ALL;



ALTER TABLE public.foto_perfil ENABLE TRIGGER ALL;

--
-- Data for Name: punto_control; Type: TABLE DATA; Schema: public; Owner: -
--

ALTER TABLE public.punto_control DISABLE TRIGGER ALL;

INSERT INTO public.punto_control (id_punto, numero_orden, descripcion, tipo_dato, unidad_medida, valor_minimo, valor_maximo, obligatorio, exige_fotografia, id_plan) VALUES (1, 1, '¿Nivel de combustible sobre la mitad?', 'booleano', NULL, NULL, NULL, true, false, 1);
INSERT INTO public.punto_control (id_punto, numero_orden, descripcion, tipo_dato, unidad_medida, valor_minimo, valor_maximo, obligatorio, exige_fotografia, id_plan) VALUES (2, 2, '¿Enciende en menos de tres intentos?', 'booleano', NULL, NULL, NULL, true, false, 1);
INSERT INTO public.punto_control (id_punto, numero_orden, descripcion, tipo_dato, unidad_medida, valor_minimo, valor_maximo, obligatorio, exige_fotografia, id_plan) VALUES (3, 3, 'Presión de descarga', 'numerico', 'bar', 6.00, 10.00, true, false, 1);
INSERT INTO public.punto_control (id_punto, numero_orden, descripcion, tipo_dato, unidad_medida, valor_minimo, valor_maximo, obligatorio, exige_fotografia, id_plan) VALUES (4, 4, 'Estado de mangueras de succión', 'seleccion', NULL, NULL, NULL, true, false, 1);
INSERT INTO public.punto_control (id_punto, numero_orden, descripcion, tipo_dato, unidad_medida, valor_minimo, valor_maximo, obligatorio, exige_fotografia, id_plan) VALUES (5, 5, '¿Sin fugas de aceite?', 'booleano', NULL, NULL, NULL, true, false, 1);
INSERT INTO public.punto_control (id_punto, numero_orden, descripcion, tipo_dato, unidad_medida, valor_minimo, valor_maximo, obligatorio, exige_fotografia, id_plan) VALUES (6, 1, 'Carga de batería', 'numerico', '%', 50.00, 100.00, true, false, 2);
INSERT INTO public.punto_control (id_punto, numero_orden, descripcion, tipo_dato, unidad_medida, valor_minimo, valor_maximo, obligatorio, exige_fotografia, id_plan) VALUES (7, 2, 'Prueba de alarma sonora y visual', 'booleano', NULL, NULL, NULL, true, false, 2);
INSERT INTO public.punto_control (id_punto, numero_orden, descripcion, tipo_dato, unidad_medida, valor_minimo, valor_maximo, obligatorio, exige_fotografia, id_plan) VALUES (8, 3, 'Lectura de O₂ en aire limpio', 'numerico', '% vol', 20.50, 21.00, true, false, 2);
INSERT INTO public.punto_control (id_punto, numero_orden, descripcion, tipo_dato, unidad_medida, valor_minimo, valor_maximo, obligatorio, exige_fotografia, id_plan) VALUES (9, 4, 'Lectura de CO en aire limpio', 'numerico', 'ppm', 0.00, 5.00, true, true, 2);
INSERT INTO public.punto_control (id_punto, numero_orden, descripcion, tipo_dato, unidad_medida, valor_minimo, valor_maximo, obligatorio, exige_fotografia, id_plan) VALUES (10, 5, 'Lectura de H₂S en aire limpio', 'numerico', 'ppm', 0.00, 1.00, true, false, 2);
INSERT INTO public.punto_control (id_punto, numero_orden, descripcion, tipo_dato, unidad_medida, valor_minimo, valor_maximo, obligatorio, exige_fotografia, id_plan) VALUES (11, 6, 'Lectura de LEL en aire limpio', 'numerico', '%', 0.00, 1.00, true, false, 2);
INSERT INTO public.punto_control (id_punto, numero_orden, descripcion, tipo_dato, unidad_medida, valor_minimo, valor_maximo, obligatorio, exige_fotografia, id_plan) VALUES (12, 1, '¿Nivel de mezcla y aceite de cadena correctos?', 'booleano', NULL, NULL, NULL, true, false, 3);
INSERT INTO public.punto_control (id_punto, numero_orden, descripcion, tipo_dato, unidad_medida, valor_minimo, valor_maximo, obligatorio, exige_fotografia, id_plan) VALUES (13, 2, 'Tensión de la cadena', 'seleccion', NULL, NULL, NULL, true, false, 3);
INSERT INTO public.punto_control (id_punto, numero_orden, descripcion, tipo_dato, unidad_medida, valor_minimo, valor_maximo, obligatorio, exige_fotografia, id_plan) VALUES (14, 3, 'Afilado y estado de eslabones', 'seleccion', NULL, NULL, NULL, true, true, 3);
INSERT INTO public.punto_control (id_punto, numero_orden, descripcion, tipo_dato, unidad_medida, valor_minimo, valor_maximo, obligatorio, exige_fotografia, id_plan) VALUES (15, 4, '¿Enciende y acelera sin fallas?', 'booleano', NULL, NULL, NULL, true, false, 3);
INSERT INTO public.punto_control (id_punto, numero_orden, descripcion, tipo_dato, unidad_medida, valor_minimo, valor_maximo, obligatorio, exige_fotografia, id_plan) VALUES (16, 1, '¿Nivel de aceite correcto?', 'booleano', NULL, NULL, NULL, true, false, 4);
INSERT INTO public.punto_control (id_punto, numero_orden, descripcion, tipo_dato, unidad_medida, valor_minimo, valor_maximo, obligatorio, exige_fotografia, id_plan) VALUES (17, 2, '¿Enciende sin fallas?', 'booleano', NULL, NULL, NULL, true, false, 4);
INSERT INTO public.punto_control (id_punto, numero_orden, descripcion, tipo_dato, unidad_medida, valor_minimo, valor_maximo, obligatorio, exige_fotografia, id_plan) VALUES (18, 3, 'Voltaje de salida', 'numerico', 'V', 210.00, 230.00, true, false, 4);
INSERT INTO public.punto_control (id_punto, numero_orden, descripcion, tipo_dato, unidad_medida, valor_minimo, valor_maximo, obligatorio, exige_fotografia, id_plan) VALUES (19, 4, 'Horómetro', 'texto', NULL, NULL, NULL, false, false, 4);
INSERT INTO public.punto_control (id_punto, numero_orden, descripcion, tipo_dato, unidad_medida, valor_minimo, valor_maximo, obligatorio, exige_fotografia, id_plan) VALUES (20, 1, '¿Acoples sin fugas?', 'booleano', NULL, NULL, NULL, true, false, 5);
INSERT INTO public.punto_control (id_punto, numero_orden, descripcion, tipo_dato, unidad_medida, valor_minimo, valor_maximo, obligatorio, exige_fotografia, id_plan) VALUES (21, 2, 'Estado de cuchillas o puntas', 'seleccion', NULL, NULL, NULL, true, false, 5);
INSERT INTO public.punto_control (id_punto, numero_orden, descripcion, tipo_dato, unidad_medida, valor_minimo, valor_maximo, obligatorio, exige_fotografia, id_plan) VALUES (22, 3, 'Presión de trabajo de la central', 'numerico', 'bar', 600.00, 720.00, true, false, 5);


ALTER TABLE public.punto_control ENABLE TRIGGER ALL;

--
-- Data for Name: revision; Type: TABLE DATA; Schema: public; Owner: -
--

ALTER TABLE public.revision DISABLE TRIGGER ALL;

INSERT INTO public.revision (id_revision, fecha_programada, fecha_limite, estado, fecha_hora_inicio, fecha_hora_termino, resultado_global, observaciones, id_asignacion, id_usuario_ejecutor) VALUES (9, '2026-11-17', '2026-11-18', 'pendiente', NULL, NULL, NULL, NULL, 1, NULL);
INSERT INTO public.revision (id_revision, fecha_programada, fecha_limite, estado, fecha_hora_inicio, fecha_hora_termino, resultado_global, observaciones, id_asignacion, id_usuario_ejecutor) VALUES (10, '2026-11-24', '2026-11-25', 'pendiente', NULL, NULL, NULL, NULL, 1, NULL);
INSERT INTO public.revision (id_revision, fecha_programada, fecha_limite, estado, fecha_hora_inicio, fecha_hora_termino, resultado_global, observaciones, id_asignacion, id_usuario_ejecutor) VALUES (22, '2026-11-17', '2026-11-18', 'pendiente', NULL, NULL, NULL, NULL, 3, NULL);
INSERT INTO public.revision (id_revision, fecha_programada, fecha_limite, estado, fecha_hora_inicio, fecha_hora_termino, resultado_global, observaciones, id_asignacion, id_usuario_ejecutor) VALUES (23, '2026-11-24', '2026-11-25', 'pendiente', NULL, NULL, NULL, NULL, 3, NULL);
INSERT INTO public.revision (id_revision, fecha_programada, fecha_limite, estado, fecha_hora_inicio, fecha_hora_termino, resultado_global, observaciones, id_asignacion, id_usuario_ejecutor) VALUES (28, '2026-11-17', '2026-11-19', 'pendiente', NULL, NULL, NULL, NULL, 4, NULL);
INSERT INTO public.revision (id_revision, fecha_programada, fecha_limite, estado, fecha_hora_inicio, fecha_hora_termino, resultado_global, observaciones, id_asignacion, id_usuario_ejecutor) VALUES (37, '2026-11-17', '2026-11-18', 'pendiente', NULL, NULL, NULL, NULL, 5, NULL);
INSERT INTO public.revision (id_revision, fecha_programada, fecha_limite, estado, fecha_hora_inicio, fecha_hora_termino, resultado_global, observaciones, id_asignacion, id_usuario_ejecutor) VALUES (38, '2026-11-24', '2026-11-25', 'pendiente', NULL, NULL, NULL, NULL, 5, NULL);
INSERT INTO public.revision (id_revision, fecha_programada, fecha_limite, estado, fecha_hora_inicio, fecha_hora_termino, resultado_global, observaciones, id_asignacion, id_usuario_ejecutor) VALUES (51, '2026-11-17', '2026-11-18', 'pendiente', NULL, NULL, NULL, NULL, 8, NULL);
INSERT INTO public.revision (id_revision, fecha_programada, fecha_limite, estado, fecha_hora_inicio, fecha_hora_termino, resultado_global, observaciones, id_asignacion, id_usuario_ejecutor) VALUES (52, '2026-11-24', '2026-11-25', 'pendiente', NULL, NULL, NULL, NULL, 8, NULL);
INSERT INTO public.revision (id_revision, fecha_programada, fecha_limite, estado, fecha_hora_inicio, fecha_hora_termino, resultado_global, observaciones, id_asignacion, id_usuario_ejecutor) VALUES (1, '2026-09-22', '2026-09-23', 'realizada', '2026-09-23 11:12:00-03', '2026-09-23 11:25:00-03', 'conforme', NULL, 1, 4);
INSERT INTO public.revision (id_revision, fecha_programada, fecha_limite, estado, fecha_hora_inicio, fecha_hora_termino, resultado_global, observaciones, id_asignacion, id_usuario_ejecutor) VALUES (2, '2026-09-29', '2026-09-30', 'realizada', '2026-09-30 10:35:00-03', '2026-09-30 10:48:00-03', 'conforme', NULL, 1, 4);
INSERT INTO public.revision (id_revision, fecha_programada, fecha_limite, estado, fecha_hora_inicio, fecha_hora_termino, resultado_global, observaciones, id_asignacion, id_usuario_ejecutor) VALUES (3, '2026-10-06', '2026-10-07', 'realizada', '2026-10-09 14:06:00-03', '2026-10-09 14:19:00-03', 'conforme', NULL, 1, 4);
INSERT INTO public.revision (id_revision, fecha_programada, fecha_limite, estado, fecha_hora_inicio, fecha_hora_termino, resultado_global, observaciones, id_asignacion, id_usuario_ejecutor) VALUES (4, '2026-10-13', '2026-10-14', 'realizada', '2026-10-13 12:40:00-03', '2026-10-13 12:53:00-03', 'conforme', NULL, 1, 4);
INSERT INTO public.revision (id_revision, fecha_programada, fecha_limite, estado, fecha_hora_inicio, fecha_hora_termino, resultado_global, observaciones, id_asignacion, id_usuario_ejecutor) VALUES (5, '2026-10-20', '2026-10-21', 'realizada', '2026-10-21 12:03:00-03', '2026-10-21 12:16:00-03', 'conforme', NULL, 1, 4);
INSERT INTO public.revision (id_revision, fecha_programada, fecha_limite, estado, fecha_hora_inicio, fecha_hora_termino, resultado_global, observaciones, id_asignacion, id_usuario_ejecutor) VALUES (6, '2026-10-27', '2026-10-28', 'realizada', '2026-10-28 16:55:00-03', '2026-10-28 17:08:00-03', 'conforme', NULL, 1, 4);
INSERT INTO public.revision (id_revision, fecha_programada, fecha_limite, estado, fecha_hora_inicio, fecha_hora_termino, resultado_global, observaciones, id_asignacion, id_usuario_ejecutor) VALUES (7, '2026-11-03', '2026-11-04', 'realizada', '2026-11-04 17:51:00-03', '2026-11-04 18:04:00-03', 'conforme', NULL, 1, 4);
INSERT INTO public.revision (id_revision, fecha_programada, fecha_limite, estado, fecha_hora_inicio, fecha_hora_termino, resultado_global, observaciones, id_asignacion, id_usuario_ejecutor) VALUES (8, '2026-11-10', '2026-11-11', 'realizada', '2026-11-11 10:51:00-03', '2026-11-11 11:04:00-03', 'conforme', NULL, 1, 4);
INSERT INTO public.revision (id_revision, fecha_programada, fecha_limite, estado, fecha_hora_inicio, fecha_hora_termino, resultado_global, observaciones, id_asignacion, id_usuario_ejecutor) VALUES (11, '2026-08-25', '2026-08-27', 'realizada', '2026-08-27 09:54:00-04', '2026-08-27 10:09:00-04', 'conforme', NULL, 2, 4);
INSERT INTO public.revision (id_revision, fecha_programada, fecha_limite, estado, fecha_hora_inicio, fecha_hora_termino, resultado_global, observaciones, id_asignacion, id_usuario_ejecutor) VALUES (12, '2026-09-25', '2026-09-27', 'realizada', '2026-09-27 13:56:00-03', '2026-09-27 14:11:00-03', 'conforme', NULL, 2, 4);
INSERT INTO public.revision (id_revision, fecha_programada, fecha_limite, estado, fecha_hora_inicio, fecha_hora_termino, resultado_global, observaciones, id_asignacion, id_usuario_ejecutor) VALUES (14, '2026-09-22', '2026-09-23', 'realizada', '2026-09-22 16:41:00-03', '2026-09-22 16:52:00-03', 'conforme', NULL, 3, 4);
INSERT INTO public.revision (id_revision, fecha_programada, fecha_limite, estado, fecha_hora_inicio, fecha_hora_termino, resultado_global, observaciones, id_asignacion, id_usuario_ejecutor) VALUES (17, '2026-10-13', '2026-10-14', 'realizada', '2026-10-15 19:39:00-03', '2026-10-15 19:50:00-03', 'observacion', NULL, 3, 4);
INSERT INTO public.revision (id_revision, fecha_programada, fecha_limite, estado, fecha_hora_inicio, fecha_hora_termino, resultado_global, observaciones, id_asignacion, id_usuario_ejecutor) VALUES (18, '2026-10-20', '2026-10-21', 'realizada', '2026-10-21 13:32:00-03', '2026-10-21 13:43:00-03', 'conforme', NULL, 3, 4);
INSERT INTO public.revision (id_revision, fecha_programada, fecha_limite, estado, fecha_hora_inicio, fecha_hora_termino, resultado_global, observaciones, id_asignacion, id_usuario_ejecutor) VALUES (19, '2026-10-27', '2026-10-28', 'realizada', '2026-10-28 16:11:00-03', '2026-10-28 16:22:00-03', 'conforme', NULL, 3, 4);
INSERT INTO public.revision (id_revision, fecha_programada, fecha_limite, estado, fecha_hora_inicio, fecha_hora_termino, resultado_global, observaciones, id_asignacion, id_usuario_ejecutor) VALUES (20, '2026-11-03', '2026-11-04', 'realizada', '2026-11-04 14:13:00-03', '2026-11-04 14:24:00-03', 'conforme', NULL, 3, 4);
INSERT INTO public.revision (id_revision, fecha_programada, fecha_limite, estado, fecha_hora_inicio, fecha_hora_termino, resultado_global, observaciones, id_asignacion, id_usuario_ejecutor) VALUES (24, '2026-09-22', '2026-09-24', 'realizada', '2026-09-24 12:35:00-03', '2026-09-24 12:46:00-03', 'conforme', NULL, 4, 4);
INSERT INTO public.revision (id_revision, fecha_programada, fecha_limite, estado, fecha_hora_inicio, fecha_hora_termino, resultado_global, observaciones, id_asignacion, id_usuario_ejecutor) VALUES (25, '2026-10-06', '2026-10-08', 'realizada', '2026-10-07 14:19:00-03', '2026-10-07 14:30:00-03', 'observacion', NULL, 4, 4);
INSERT INTO public.revision (id_revision, fecha_programada, fecha_limite, estado, fecha_hora_inicio, fecha_hora_termino, resultado_global, observaciones, id_asignacion, id_usuario_ejecutor) VALUES (26, '2026-10-20', '2026-10-22', 'realizada', '2026-10-20 13:53:00-03', '2026-10-20 14:04:00-03', 'conforme', NULL, 4, 4);
INSERT INTO public.revision (id_revision, fecha_programada, fecha_limite, estado, fecha_hora_inicio, fecha_hora_termino, resultado_global, observaciones, id_asignacion, id_usuario_ejecutor) VALUES (27, '2026-11-03', '2026-11-05', 'realizada', '2026-11-05 09:28:00-03', '2026-11-05 09:39:00-03', 'conforme', NULL, 4, 4);
INSERT INTO public.revision (id_revision, fecha_programada, fecha_limite, estado, fecha_hora_inicio, fecha_hora_termino, resultado_global, observaciones, id_asignacion, id_usuario_ejecutor) VALUES (29, '2026-09-22', '2026-09-23', 'realizada', '2026-09-22 10:08:00-03', '2026-09-22 10:21:00-03', 'conforme', NULL, 5, 5);
INSERT INTO public.revision (id_revision, fecha_programada, fecha_limite, estado, fecha_hora_inicio, fecha_hora_termino, resultado_global, observaciones, id_asignacion, id_usuario_ejecutor) VALUES (30, '2026-09-29', '2026-09-30', 'realizada', '2026-09-30 14:26:00-03', '2026-09-30 14:39:00-03', 'observacion', NULL, 5, 5);
INSERT INTO public.revision (id_revision, fecha_programada, fecha_limite, estado, fecha_hora_inicio, fecha_hora_termino, resultado_global, observaciones, id_asignacion, id_usuario_ejecutor) VALUES (31, '2026-10-06', '2026-10-07', 'realizada', '2026-10-06 12:49:00-03', '2026-10-06 13:02:00-03', 'conforme', NULL, 5, 5);
INSERT INTO public.revision (id_revision, fecha_programada, fecha_limite, estado, fecha_hora_inicio, fecha_hora_termino, resultado_global, observaciones, id_asignacion, id_usuario_ejecutor) VALUES (32, '2026-10-13', '2026-10-14', 'realizada', '2026-10-13 17:08:00-03', '2026-10-13 17:21:00-03', 'conforme', NULL, 5, 5);
INSERT INTO public.revision (id_revision, fecha_programada, fecha_limite, estado, fecha_hora_inicio, fecha_hora_termino, resultado_global, observaciones, id_asignacion, id_usuario_ejecutor) VALUES (33, '2026-10-20', '2026-10-21', 'realizada', '2026-10-21 12:08:00-03', '2026-10-21 12:21:00-03', 'conforme', NULL, 5, 5);
INSERT INTO public.revision (id_revision, fecha_programada, fecha_limite, estado, fecha_hora_inicio, fecha_hora_termino, resultado_global, observaciones, id_asignacion, id_usuario_ejecutor) VALUES (34, '2026-10-27', '2026-10-28', 'realizada', '2026-10-28 19:14:00-03', '2026-10-28 19:27:00-03', 'conforme', NULL, 5, 5);
INSERT INTO public.revision (id_revision, fecha_programada, fecha_limite, estado, fecha_hora_inicio, fecha_hora_termino, resultado_global, observaciones, id_asignacion, id_usuario_ejecutor) VALUES (36, '2026-11-10', '2026-11-11', 'realizada', '2026-11-10 10:19:00-03', '2026-11-10 10:32:00-03', 'observacion', NULL, 5, 5);
INSERT INTO public.revision (id_revision, fecha_programada, fecha_limite, estado, fecha_hora_inicio, fecha_hora_termino, resultado_global, observaciones, id_asignacion, id_usuario_ejecutor) VALUES (39, '2026-08-25', '2026-08-28', 'realizada', '2026-08-30 18:30:00-04', '2026-08-30 18:39:00-04', 'observacion', NULL, 6, 6);
INSERT INTO public.revision (id_revision, fecha_programada, fecha_limite, estado, fecha_hora_inicio, fecha_hora_termino, resultado_global, observaciones, id_asignacion, id_usuario_ejecutor) VALUES (40, '2026-09-25', '2026-09-28', 'realizada', '2026-09-26 14:20:00-03', '2026-09-26 14:29:00-03', 'conforme', NULL, 6, 6);
INSERT INTO public.revision (id_revision, fecha_programada, fecha_limite, estado, fecha_hora_inicio, fecha_hora_termino, resultado_global, observaciones, id_asignacion, id_usuario_ejecutor) VALUES (42, '2026-08-25', '2026-08-27', 'realizada', '2026-08-27 17:38:00-04', '2026-08-27 17:53:00-04', 'observacion', NULL, 7, 5);
INSERT INTO public.revision (id_revision, fecha_programada, fecha_limite, estado, fecha_hora_inicio, fecha_hora_termino, resultado_global, observaciones, id_asignacion, id_usuario_ejecutor) VALUES (43, '2026-09-25', '2026-09-27', 'realizada', '2026-09-26 11:49:00-03', '2026-09-26 12:04:00-03', 'conforme', NULL, 7, 5);
INSERT INTO public.revision (id_revision, fecha_programada, fecha_limite, estado, fecha_hora_inicio, fecha_hora_termino, resultado_global, observaciones, id_asignacion, id_usuario_ejecutor) VALUES (44, '2026-10-25', '2026-10-27', 'realizada', '2026-10-26 17:40:00-03', '2026-10-26 17:55:00-03', 'conforme', NULL, 7, 5);
INSERT INTO public.revision (id_revision, fecha_programada, fecha_limite, estado, fecha_hora_inicio, fecha_hora_termino, resultado_global, observaciones, id_asignacion, id_usuario_ejecutor) VALUES (45, '2026-10-06', '2026-10-07', 'realizada', '2026-10-07 17:39:00-03', '2026-10-07 17:52:00-03', 'conforme', NULL, 8, 6);
INSERT INTO public.revision (id_revision, fecha_programada, fecha_limite, estado, fecha_hora_inicio, fecha_hora_termino, resultado_global, observaciones, id_asignacion, id_usuario_ejecutor) VALUES (46, '2026-10-13', '2026-10-14', 'realizada', '2026-10-13 18:23:00-03', '2026-10-13 18:36:00-03', 'conforme', NULL, 8, 6);
INSERT INTO public.revision (id_revision, fecha_programada, fecha_limite, estado, fecha_hora_inicio, fecha_hora_termino, resultado_global, observaciones, id_asignacion, id_usuario_ejecutor) VALUES (47, '2026-10-20', '2026-10-21', 'realizada', '2026-10-20 17:42:00-03', '2026-10-20 17:55:00-03', 'conforme', NULL, 8, 6);
INSERT INTO public.revision (id_revision, fecha_programada, fecha_limite, estado, fecha_hora_inicio, fecha_hora_termino, resultado_global, observaciones, id_asignacion, id_usuario_ejecutor) VALUES (48, '2026-10-27', '2026-10-28', 'realizada', '2026-10-27 13:14:00-03', '2026-10-27 13:27:00-03', 'conforme', NULL, 8, 6);
INSERT INTO public.revision (id_revision, fecha_programada, fecha_limite, estado, fecha_hora_inicio, fecha_hora_termino, resultado_global, observaciones, id_asignacion, id_usuario_ejecutor) VALUES (49, '2026-11-03', '2026-11-04', 'realizada', '2026-11-03 12:14:00-03', '2026-11-03 12:27:00-03', 'conforme', NULL, 8, 6);
INSERT INTO public.revision (id_revision, fecha_programada, fecha_limite, estado, fecha_hora_inicio, fecha_hora_termino, resultado_global, observaciones, id_asignacion, id_usuario_ejecutor) VALUES (53, '2026-08-25', '2026-08-28', 'realizada', '2026-08-28 14:02:00-04', '2026-08-28 14:11:00-04', 'conforme', NULL, 9, 6);
INSERT INTO public.revision (id_revision, fecha_programada, fecha_limite, estado, fecha_hora_inicio, fecha_hora_termino, resultado_global, observaciones, id_asignacion, id_usuario_ejecutor) VALUES (54, '2026-09-25', '2026-09-28', 'realizada', '2026-09-26 16:03:00-03', '2026-09-26 16:12:00-03', 'conforme', NULL, 9, 6);
INSERT INTO public.revision (id_revision, fecha_programada, fecha_limite, estado, fecha_hora_inicio, fecha_hora_termino, resultado_global, observaciones, id_asignacion, id_usuario_ejecutor) VALUES (55, '2026-10-25', '2026-10-28', 'realizada', '2026-10-27 18:32:00-03', '2026-10-27 18:41:00-03', 'conforme', NULL, 9, 6);
INSERT INTO public.revision (id_revision, fecha_programada, fecha_limite, estado, fecha_hora_inicio, fecha_hora_termino, resultado_global, observaciones, id_asignacion, id_usuario_ejecutor) VALUES (13, '2026-10-25', '2026-10-27', 'realizada', '2026-10-27 10:30:00-03', '2026-10-27 10:45:00-03', 'falla', NULL, 2, 4);
INSERT INTO public.revision (id_revision, fecha_programada, fecha_limite, estado, fecha_hora_inicio, fecha_hora_termino, resultado_global, observaciones, id_asignacion, id_usuario_ejecutor) VALUES (21, '2026-11-10', '2026-11-11', 'realizada', '2026-11-11 10:30:00-03', '2026-11-11 10:41:00-03', 'falla', NULL, 3, 4);
INSERT INTO public.revision (id_revision, fecha_programada, fecha_limite, estado, fecha_hora_inicio, fecha_hora_termino, resultado_global, observaciones, id_asignacion, id_usuario_ejecutor) VALUES (50, '2026-11-10', '2026-11-11', 'vencida', NULL, NULL, NULL, NULL, 8, NULL);
INSERT INTO public.revision (id_revision, fecha_programada, fecha_limite, estado, fecha_hora_inicio, fecha_hora_termino, resultado_global, observaciones, id_asignacion, id_usuario_ejecutor) VALUES (35, '2026-11-03', '2026-11-04', 'vencida', NULL, NULL, NULL, NULL, 5, NULL);
INSERT INTO public.revision (id_revision, fecha_programada, fecha_limite, estado, fecha_hora_inicio, fecha_hora_termino, resultado_global, observaciones, id_asignacion, id_usuario_ejecutor) VALUES (16, '2026-10-06', '2026-10-07', 'vencida', NULL, NULL, NULL, NULL, 3, NULL);
INSERT INTO public.revision (id_revision, fecha_programada, fecha_limite, estado, fecha_hora_inicio, fecha_hora_termino, resultado_global, observaciones, id_asignacion, id_usuario_ejecutor) VALUES (15, '2026-09-29', '2026-09-30', 'vencida', NULL, NULL, NULL, NULL, 3, NULL);
INSERT INTO public.revision (id_revision, fecha_programada, fecha_limite, estado, fecha_hora_inicio, fecha_hora_termino, resultado_global, observaciones, id_asignacion, id_usuario_ejecutor) VALUES (41, '2026-10-25', '2026-10-28', 'realizada', '2026-10-28 10:30:00-03', '2026-10-28 10:39:00-03', 'falla', NULL, 6, 6);


ALTER TABLE public.revision ENABLE TRIGGER ALL;

--
-- Data for Name: resultado_punto; Type: TABLE DATA; Schema: public; Owner: -
--

ALTER TABLE public.resultado_punto DISABLE TRIGGER ALL;

INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('Sí', 'conforme', NULL, '2026-09-23 11:13:00-03', 1, 1);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('Sí', 'conforme', NULL, '2026-09-23 11:15:00-03', 2, 1);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('6.5', 'conforme', NULL, '2026-09-23 11:17:00-03', 3, 1);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES (NULL, 'conforme', NULL, '2026-09-23 11:19:00-03', 4, 1);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('Sí', 'conforme', NULL, '2026-09-23 11:21:00-03', 5, 1);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('Sí', 'conforme', NULL, '2026-09-30 10:36:00-03', 1, 2);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('Sí', 'conforme', NULL, '2026-09-30 10:38:00-03', 2, 2);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('9.2', 'conforme', NULL, '2026-09-30 10:40:00-03', 3, 2);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES (NULL, 'conforme', NULL, '2026-09-30 10:42:00-03', 4, 2);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('Sí', 'conforme', NULL, '2026-09-30 10:44:00-03', 5, 2);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('Sí', 'conforme', NULL, '2026-10-09 14:07:00-03', 1, 3);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('Sí', 'conforme', NULL, '2026-10-09 14:09:00-03', 2, 3);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('7.9', 'conforme', NULL, '2026-10-09 14:11:00-03', 3, 3);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES (NULL, 'conforme', NULL, '2026-10-09 14:13:00-03', 4, 3);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('Sí', 'conforme', NULL, '2026-10-09 14:15:00-03', 5, 3);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('Sí', 'conforme', NULL, '2026-10-13 12:41:00-03', 1, 4);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('Sí', 'conforme', NULL, '2026-10-13 12:43:00-03', 2, 4);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('7.3', 'conforme', NULL, '2026-10-13 12:45:00-03', 3, 4);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES (NULL, 'conforme', NULL, '2026-10-13 12:47:00-03', 4, 4);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('Sí', 'conforme', NULL, '2026-10-13 12:49:00-03', 5, 4);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('Sí', 'conforme', NULL, '2026-10-21 12:04:00-03', 1, 5);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('Sí', 'conforme', NULL, '2026-10-21 12:06:00-03', 2, 5);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('8', 'conforme', NULL, '2026-10-21 12:08:00-03', 3, 5);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES (NULL, 'conforme', NULL, '2026-10-21 12:10:00-03', 4, 5);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('Sí', 'conforme', NULL, '2026-10-21 12:12:00-03', 5, 5);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('Sí', 'conforme', NULL, '2026-10-28 16:56:00-03', 1, 6);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('Sí', 'conforme', NULL, '2026-10-28 16:58:00-03', 2, 6);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('9.2', 'conforme', NULL, '2026-10-28 17:00:00-03', 3, 6);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES (NULL, 'conforme', NULL, '2026-10-28 17:02:00-03', 4, 6);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('Sí', 'conforme', NULL, '2026-10-28 17:04:00-03', 5, 6);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('Sí', 'conforme', NULL, '2026-11-04 17:52:00-03', 1, 7);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('Sí', 'conforme', NULL, '2026-11-04 17:54:00-03', 2, 7);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('6.9', 'conforme', NULL, '2026-11-04 17:56:00-03', 3, 7);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES (NULL, 'conforme', NULL, '2026-11-04 17:58:00-03', 4, 7);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('Sí', 'conforme', NULL, '2026-11-04 18:00:00-03', 5, 7);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('Sí', 'conforme', NULL, '2026-11-11 10:52:00-03', 1, 8);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('Sí', 'conforme', NULL, '2026-11-11 10:54:00-03', 2, 8);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('8.2', 'conforme', NULL, '2026-11-11 10:56:00-03', 3, 8);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES (NULL, 'conforme', NULL, '2026-11-11 10:58:00-03', 4, 8);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('Sí', 'conforme', NULL, '2026-11-11 11:00:00-03', 5, 8);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('82.5', 'conforme', NULL, '2026-08-27 09:55:00-04', 6, 11);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('Sí', 'conforme', NULL, '2026-08-27 09:57:00-04', 7, 11);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('20.8', 'conforme', NULL, '2026-08-27 09:59:00-04', 8, 11);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('0.2', 'conforme', NULL, '2026-08-27 10:01:00-04', 9, 11);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('0.7', 'conforme', NULL, '2026-08-27 10:03:00-04', 10, 11);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('0.7', 'conforme', NULL, '2026-08-27 10:05:00-04', 11, 11);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('69.8', 'conforme', NULL, '2026-09-27 13:57:00-03', 6, 12);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('Sí', 'conforme', NULL, '2026-09-27 13:59:00-03', 7, 12);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('20.7', 'conforme', NULL, '2026-09-27 14:01:00-03', 8, 12);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('4.6', 'conforme', NULL, '2026-09-27 14:03:00-03', 9, 12);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('0.7', 'conforme', NULL, '2026-09-27 14:05:00-03', 10, 12);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('0.5', 'conforme', NULL, '2026-09-27 14:07:00-03', 11, 12);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('Sí', 'conforme', NULL, '2026-09-22 16:42:00-03', 12, 14);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES (NULL, 'conforme', NULL, '2026-09-22 16:44:00-03', 13, 14);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES (NULL, 'conforme', NULL, '2026-09-22 16:46:00-03', 14, 14);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('Sí', 'conforme', NULL, '2026-09-22 16:48:00-03', 15, 14);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('Sí', 'conforme', NULL, '2026-10-15 19:40:00-03', 12, 17);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES (NULL, 'observacion', 'Leve suciedad; se limpió en el lugar.', '2026-10-15 19:42:00-03', 13, 17);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES (NULL, 'conforme', NULL, '2026-10-15 19:44:00-03', 14, 17);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('Sí', 'conforme', NULL, '2026-10-15 19:46:00-03', 15, 17);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('Sí', 'conforme', NULL, '2026-10-21 13:33:00-03', 12, 18);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES (NULL, 'conforme', NULL, '2026-10-21 13:35:00-03', 13, 18);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES (NULL, 'conforme', NULL, '2026-10-21 13:37:00-03', 14, 18);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('Sí', 'conforme', NULL, '2026-10-21 13:39:00-03', 15, 18);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('Sí', 'conforme', NULL, '2026-10-28 16:12:00-03', 12, 19);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES (NULL, 'conforme', NULL, '2026-10-28 16:14:00-03', 13, 19);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES (NULL, 'conforme', NULL, '2026-10-28 16:16:00-03', 14, 19);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('Sí', 'conforme', NULL, '2026-10-28 16:18:00-03', 15, 19);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('Sí', 'conforme', NULL, '2026-11-04 14:14:00-03', 12, 20);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES (NULL, 'conforme', NULL, '2026-11-04 14:16:00-03', 13, 20);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES (NULL, 'conforme', NULL, '2026-11-04 14:18:00-03', 14, 20);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('Sí', 'conforme', NULL, '2026-11-04 14:20:00-03', 15, 20);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('Sí', 'conforme', NULL, '2026-09-24 12:36:00-03', 16, 24);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('Sí', 'conforme', NULL, '2026-09-24 12:38:00-03', 17, 24);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('218.6', 'conforme', NULL, '2026-09-24 12:40:00-03', 18, 24);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('127 h', 'conforme', NULL, '2026-09-24 12:42:00-03', 19, 24);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('Sí', 'observacion', 'Leve suciedad; se limpió en el lugar.', '2026-10-07 14:20:00-03', 16, 25);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('Sí', 'conforme', NULL, '2026-10-07 14:22:00-03', 17, 25);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('216.4', 'conforme', NULL, '2026-10-07 14:24:00-03', 18, 25);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('310 h', 'conforme', NULL, '2026-10-07 14:26:00-03', 19, 25);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('Sí', 'conforme', NULL, '2026-10-20 13:54:00-03', 16, 26);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('Sí', 'conforme', NULL, '2026-10-20 13:56:00-03', 17, 26);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('218.5', 'conforme', NULL, '2026-10-20 13:58:00-03', 18, 26);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('431 h', 'conforme', NULL, '2026-10-20 14:00:00-03', 19, 26);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('Sí', 'conforme', NULL, '2026-11-05 09:29:00-03', 16, 27);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('Sí', 'conforme', NULL, '2026-11-05 09:31:00-03', 17, 27);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('225.2', 'conforme', NULL, '2026-11-05 09:33:00-03', 18, 27);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('440 h', 'conforme', NULL, '2026-11-05 09:35:00-03', 19, 27);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('Sí', 'conforme', NULL, '2026-09-22 10:09:00-03', 1, 29);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('Sí', 'conforme', NULL, '2026-09-22 10:11:00-03', 2, 29);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('9.2', 'conforme', NULL, '2026-09-22 10:13:00-03', 3, 29);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES (NULL, 'conforme', NULL, '2026-09-22 10:15:00-03', 4, 29);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('Sí', 'conforme', NULL, '2026-09-22 10:17:00-03', 5, 29);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('Sí', 'conforme', NULL, '2026-09-30 14:27:00-03', 1, 30);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('Sí', 'observacion', 'Leve suciedad; se limpió en el lugar.', '2026-09-30 14:29:00-03', 2, 30);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('9.5', 'conforme', NULL, '2026-09-30 14:31:00-03', 3, 30);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES (NULL, 'conforme', NULL, '2026-09-30 14:33:00-03', 4, 30);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('Sí', 'conforme', NULL, '2026-09-30 14:35:00-03', 5, 30);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('Sí', 'conforme', NULL, '2026-10-06 12:50:00-03', 1, 31);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('Sí', 'conforme', NULL, '2026-10-06 12:52:00-03', 2, 31);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('9.8', 'conforme', NULL, '2026-10-06 12:54:00-03', 3, 31);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES (NULL, 'conforme', NULL, '2026-10-06 12:56:00-03', 4, 31);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('Sí', 'conforme', NULL, '2026-10-06 12:58:00-03', 5, 31);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('Sí', 'conforme', NULL, '2026-10-13 17:09:00-03', 1, 32);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('Sí', 'conforme', NULL, '2026-10-13 17:11:00-03', 2, 32);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('8.3', 'conforme', NULL, '2026-10-13 17:13:00-03', 3, 32);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES (NULL, 'conforme', NULL, '2026-10-13 17:15:00-03', 4, 32);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('Sí', 'conforme', NULL, '2026-10-13 17:17:00-03', 5, 32);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('Sí', 'conforme', NULL, '2026-10-21 12:09:00-03', 1, 33);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('Sí', 'conforme', NULL, '2026-10-21 12:11:00-03', 2, 33);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('6.4', 'conforme', NULL, '2026-10-21 12:13:00-03', 3, 33);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES (NULL, 'conforme', NULL, '2026-10-21 12:15:00-03', 4, 33);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('Sí', 'conforme', NULL, '2026-10-21 12:17:00-03', 5, 33);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('Sí', 'conforme', NULL, '2026-10-28 19:15:00-03', 1, 34);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('Sí', 'conforme', NULL, '2026-10-28 19:17:00-03', 2, 34);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('9.5', 'conforme', NULL, '2026-10-28 19:19:00-03', 3, 34);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES (NULL, 'conforme', NULL, '2026-10-28 19:21:00-03', 4, 34);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('Sí', 'conforme', NULL, '2026-10-28 19:23:00-03', 5, 34);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('Sí', 'conforme', NULL, '2026-11-10 10:20:00-03', 1, 36);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('Sí', 'conforme', NULL, '2026-11-10 10:22:00-03', 2, 36);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('8.3', 'conforme', NULL, '2026-11-10 10:24:00-03', 3, 36);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES (NULL, 'conforme', NULL, '2026-11-10 10:26:00-03', 4, 36);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('Sí', 'observacion', 'Leve suciedad; se limpió en el lugar.', '2026-11-10 10:28:00-03', 5, 36);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('Sí', 'observacion', 'Leve suciedad; se limpió en el lugar.', '2026-08-30 18:31:00-04', 20, 39);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES (NULL, 'conforme', NULL, '2026-08-30 18:33:00-04', 21, 39);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('715.6', 'conforme', NULL, '2026-08-30 18:35:00-04', 22, 39);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('Sí', 'conforme', NULL, '2026-09-26 14:21:00-03', 20, 40);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES (NULL, 'conforme', NULL, '2026-09-26 14:23:00-03', 21, 40);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('657', 'conforme', NULL, '2026-09-26 14:25:00-03', 22, 40);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('51.4', 'conforme', NULL, '2026-08-27 17:39:00-04', 6, 42);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('Sí', 'conforme', NULL, '2026-08-27 17:41:00-04', 7, 42);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('20.6', 'observacion', 'Leve suciedad; se limpió en el lugar.', '2026-08-27 17:43:00-04', 8, 42);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('1.6', 'conforme', NULL, '2026-08-27 17:45:00-04', 9, 42);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('0.8', 'conforme', NULL, '2026-08-27 17:47:00-04', 10, 42);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('1', 'conforme', NULL, '2026-08-27 17:49:00-04', 11, 42);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('79', 'conforme', NULL, '2026-09-26 11:50:00-03', 6, 43);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('Sí', 'conforme', NULL, '2026-09-26 11:52:00-03', 7, 43);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('20.6', 'conforme', NULL, '2026-09-26 11:54:00-03', 8, 43);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('0.5', 'conforme', NULL, '2026-09-26 11:56:00-03', 9, 43);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('0.1', 'conforme', NULL, '2026-09-26 11:58:00-03', 10, 43);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('0.6', 'conforme', NULL, '2026-09-26 12:00:00-03', 11, 43);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('89.3', 'conforme', NULL, '2026-10-26 17:41:00-03', 6, 44);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('Sí', 'conforme', NULL, '2026-10-26 17:43:00-03', 7, 44);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('20.9', 'conforme', NULL, '2026-10-26 17:45:00-03', 8, 44);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('4.4', 'conforme', NULL, '2026-10-26 17:47:00-03', 9, 44);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('0.1', 'conforme', NULL, '2026-10-26 17:49:00-03', 10, 44);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('0.4', 'conforme', NULL, '2026-10-26 17:51:00-03', 11, 44);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('Sí', 'conforme', NULL, '2026-10-07 17:40:00-03', 1, 45);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('Sí', 'conforme', NULL, '2026-10-07 17:42:00-03', 2, 45);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('9.5', 'conforme', NULL, '2026-10-07 17:44:00-03', 3, 45);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES (NULL, 'conforme', NULL, '2026-10-07 17:46:00-03', 4, 45);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('Sí', 'conforme', NULL, '2026-10-07 17:48:00-03', 5, 45);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('Sí', 'conforme', NULL, '2026-10-13 18:24:00-03', 1, 46);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('Sí', 'conforme', NULL, '2026-10-13 18:26:00-03', 2, 46);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('9.5', 'conforme', NULL, '2026-10-13 18:28:00-03', 3, 46);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES (NULL, 'conforme', NULL, '2026-10-13 18:30:00-03', 4, 46);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('Sí', 'conforme', NULL, '2026-10-13 18:32:00-03', 5, 46);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('Sí', 'conforme', NULL, '2026-10-20 17:43:00-03', 1, 47);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('Sí', 'conforme', NULL, '2026-10-20 17:45:00-03', 2, 47);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('6.6', 'conforme', NULL, '2026-10-20 17:47:00-03', 3, 47);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES (NULL, 'conforme', NULL, '2026-10-20 17:49:00-03', 4, 47);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('Sí', 'conforme', NULL, '2026-10-20 17:51:00-03', 5, 47);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('Sí', 'conforme', NULL, '2026-10-27 13:15:00-03', 1, 48);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('Sí', 'conforme', NULL, '2026-10-27 13:17:00-03', 2, 48);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('8.5', 'conforme', NULL, '2026-10-27 13:19:00-03', 3, 48);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES (NULL, 'conforme', NULL, '2026-10-27 13:21:00-03', 4, 48);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('Sí', 'conforme', NULL, '2026-10-27 13:23:00-03', 5, 48);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('Sí', 'conforme', NULL, '2026-11-03 12:15:00-03', 1, 49);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('Sí', 'conforme', NULL, '2026-11-03 12:17:00-03', 2, 49);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('8.7', 'conforme', NULL, '2026-11-03 12:19:00-03', 3, 49);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES (NULL, 'conforme', NULL, '2026-11-03 12:21:00-03', 4, 49);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('Sí', 'conforme', NULL, '2026-11-03 12:23:00-03', 5, 49);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('Sí', 'conforme', NULL, '2026-08-28 14:03:00-04', 20, 53);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES (NULL, 'conforme', NULL, '2026-08-28 14:05:00-04', 21, 53);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('639.6', 'conforme', NULL, '2026-08-28 14:07:00-04', 22, 53);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('Sí', 'conforme', NULL, '2026-09-26 16:04:00-03', 20, 54);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES (NULL, 'conforme', NULL, '2026-09-26 16:06:00-03', 21, 54);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('706.3', 'conforme', NULL, '2026-09-26 16:08:00-03', 22, 54);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('Sí', 'conforme', NULL, '2026-10-27 18:33:00-03', 20, 55);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES (NULL, 'conforme', NULL, '2026-10-27 18:35:00-03', 21, 55);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('692.1', 'conforme', NULL, '2026-10-27 18:37:00-03', 22, 55);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('61.9', 'conforme', NULL, '2026-10-27 10:31:00-03', 6, 13);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('Sí', 'conforme', NULL, '2026-10-27 10:33:00-03', 7, 13);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('20.8', 'conforme', NULL, '2026-10-27 10:35:00-03', 8, 13);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('9', 'falla', 'El sensor de CO no vuelve a cero tras la calibración.', '2026-10-27 10:37:00-03', 9, 13);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('0.2', 'conforme', NULL, '2026-10-27 10:39:00-03', 10, 13);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('1', 'conforme', NULL, '2026-10-27 10:41:00-03', 11, 13);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('No', 'falla', 'Cadena con desgaste en eslabones.', '2026-11-11 10:31:00-03', 12, 21);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES (NULL, 'conforme', NULL, '2026-11-11 10:33:00-03', 13, 21);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES (NULL, 'conforme', NULL, '2026-11-11 10:35:00-03', 14, 21);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('Sí', 'conforme', NULL, '2026-11-11 10:37:00-03', 15, 21);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('Sí', 'conforme', NULL, '2026-10-28 10:31:00-03', 20, 41);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES (NULL, 'conforme', NULL, '2026-10-28 10:33:00-03', 21, 41);
INSERT INTO public.resultado_punto (valor_registrado, resultado, observacion, fecha_hora_registro, id_punto, id_revision) VALUES ('793', 'falla', 'Cadena con desgaste en eslabones.', '2026-10-28 10:35:00-03', 22, 41);


ALTER TABLE public.resultado_punto ENABLE TRIGGER ALL;

--
-- Data for Name: fotografia; Type: TABLE DATA; Schema: public; Owner: -
--

ALTER TABLE public.fotografia DISABLE TRIGGER ALL;

INSERT INTO public.fotografia (id_fotografia, nombre_archivo, ruta_almacenamiento, tipo_mime, tamano_bytes, hash_sha256, fecha_hora_captura, fecha_hora_carga, latitud, longitud, descripcion, anulada, id_usuario, id_punto, id_revision) VALUES ('1057958d-705b-45a1-a7d8-7ec937f0f4fe', 'IMG_0001.jpg', 'fotografias/2026/11/1057958d-705b-45a1-a7d8-7ec937f0f4fe.jpg', 'image/jpeg', 17664, '91054aeb3d407d26dcd9a77e71acdf794f9a22ac803cddecd9b5f4b9e2a77f39', '2026-09-23 11:23:00-03', '2026-09-23 11:23:00-03', NULL, NULL, NULL, false, 4, NULL, 1);
INSERT INTO public.fotografia (id_fotografia, nombre_archivo, ruta_almacenamiento, tipo_mime, tamano_bytes, hash_sha256, fecha_hora_captura, fecha_hora_carga, latitud, longitud, descripcion, anulada, id_usuario, id_punto, id_revision) VALUES ('d525236a-4e59-48dd-a274-a0b35a8c5871', 'IMG_0002.jpg', 'fotografias/2026/11/d525236a-4e59-48dd-a274-a0b35a8c5871.jpg', 'image/jpeg', 16852, '7068dd40d8f7a05e87f5452ec2dcef7e8b0da167b64d7bcc0b36dc228cbc455a', '2026-09-30 10:46:00-03', '2026-09-30 10:46:00-03', NULL, NULL, NULL, false, 4, NULL, 2);
INSERT INTO public.fotografia (id_fotografia, nombre_archivo, ruta_almacenamiento, tipo_mime, tamano_bytes, hash_sha256, fecha_hora_captura, fecha_hora_carga, latitud, longitud, descripcion, anulada, id_usuario, id_punto, id_revision) VALUES ('8a6764fb-316c-4c51-a1d9-5cf54a74d8ad', 'IMG_0003.jpg', 'fotografias/2026/11/8a6764fb-316c-4c51-a1d9-5cf54a74d8ad.jpg', 'image/jpeg', 16492, '8d57fd7ef4c702b6269a84dcfc8ff0446ba9592cde50c6af414aafd730b6b77e', '2026-10-09 14:17:00-03', '2026-10-09 14:17:00-03', NULL, NULL, NULL, false, 4, NULL, 3);
INSERT INTO public.fotografia (id_fotografia, nombre_archivo, ruta_almacenamiento, tipo_mime, tamano_bytes, hash_sha256, fecha_hora_captura, fecha_hora_carga, latitud, longitud, descripcion, anulada, id_usuario, id_punto, id_revision) VALUES ('e2554a4a-9b8f-4d6b-868e-aebea708bca4', 'IMG_0004.jpg', 'fotografias/2026/11/e2554a4a-9b8f-4d6b-868e-aebea708bca4.jpg', 'image/jpeg', 16328, '9c5bd2a58dd64727e89d22ffc633434dfe921f2148f6d073a74bd9eddca9285c', '2026-10-13 12:51:00-03', '2026-10-13 12:51:00-03', NULL, NULL, NULL, false, 4, NULL, 4);
INSERT INTO public.fotografia (id_fotografia, nombre_archivo, ruta_almacenamiento, tipo_mime, tamano_bytes, hash_sha256, fecha_hora_captura, fecha_hora_carga, latitud, longitud, descripcion, anulada, id_usuario, id_punto, id_revision) VALUES ('a4e26200-47a4-474a-b00a-310e993fdf64', 'IMG_0005.jpg', 'fotografias/2026/11/a4e26200-47a4-474a-b00a-310e993fdf64.jpg', 'image/jpeg', 16295, '5f1d66510e44a4dcfc132716f375309091cc33d5a092e061e41ba1739abba9f8', '2026-10-21 12:14:00-03', '2026-10-21 12:14:00-03', NULL, NULL, NULL, false, 4, NULL, 5);
INSERT INTO public.fotografia (id_fotografia, nombre_archivo, ruta_almacenamiento, tipo_mime, tamano_bytes, hash_sha256, fecha_hora_captura, fecha_hora_carga, latitud, longitud, descripcion, anulada, id_usuario, id_punto, id_revision) VALUES ('156e8886-385a-4992-a33a-9c449074447c', 'IMG_0006.jpg', 'fotografias/2026/11/156e8886-385a-4992-a33a-9c449074447c.jpg', 'image/jpeg', 17207, '31d29f6f5d91ae183bcef604f3f2ae669ea0fff92d591af01c0b6d14da223114', '2026-10-28 17:06:00-03', '2026-10-28 17:06:00-03', NULL, NULL, NULL, false, 4, NULL, 6);
INSERT INTO public.fotografia (id_fotografia, nombre_archivo, ruta_almacenamiento, tipo_mime, tamano_bytes, hash_sha256, fecha_hora_captura, fecha_hora_carga, latitud, longitud, descripcion, anulada, id_usuario, id_punto, id_revision) VALUES ('a43fa662-9b0d-4e88-84b5-e7d0e58b0c78', 'IMG_0007.jpg', 'fotografias/2026/11/a43fa662-9b0d-4e88-84b5-e7d0e58b0c78.jpg', 'image/jpeg', 16792, '639d325b34391dadfef60d503f51c5d3c5b5a6b620d1c9853eb872a8c991ad90', '2026-11-04 18:02:00-03', '2026-11-04 18:02:00-03', NULL, NULL, NULL, false, 4, NULL, 7);
INSERT INTO public.fotografia (id_fotografia, nombre_archivo, ruta_almacenamiento, tipo_mime, tamano_bytes, hash_sha256, fecha_hora_captura, fecha_hora_carga, latitud, longitud, descripcion, anulada, id_usuario, id_punto, id_revision) VALUES ('5f593ff9-e710-4573-b280-9b9551cfd267', 'IMG_0008.jpg', 'fotografias/2026/11/5f593ff9-e710-4573-b280-9b9551cfd267.jpg', 'image/jpeg', 17074, '8a5aec5405e4b32749fb03168424d93003e0508f28da498df0bd21ae6cc13139', '2026-11-11 11:02:00-03', '2026-11-11 11:02:00-03', NULL, NULL, NULL, false, 4, NULL, 8);
INSERT INTO public.fotografia (id_fotografia, nombre_archivo, ruta_almacenamiento, tipo_mime, tamano_bytes, hash_sha256, fecha_hora_captura, fecha_hora_carga, latitud, longitud, descripcion, anulada, id_usuario, id_punto, id_revision) VALUES ('9f2bae58-4d2e-48c5-87ef-f22563bea1d9', 'IMG_0009.jpg', 'fotografias/2026/11/9f2bae58-4d2e-48c5-87ef-f22563bea1d9.jpg', 'image/jpeg', 17593, 'fe4e9daac430dc3e8b0c183e5eeb98eea8eb4e648b44e5d3fa0f4dfc9436bdb0', '2026-08-27 10:01:00-04', '2026-08-27 10:01:00-04', NULL, NULL, NULL, false, 4, 9, 11);
INSERT INTO public.fotografia (id_fotografia, nombre_archivo, ruta_almacenamiento, tipo_mime, tamano_bytes, hash_sha256, fecha_hora_captura, fecha_hora_carga, latitud, longitud, descripcion, anulada, id_usuario, id_punto, id_revision) VALUES ('a4ccc4e0-7604-4af3-9143-1553f7af6325', 'IMG_0010.jpg', 'fotografias/2026/11/a4ccc4e0-7604-4af3-9143-1553f7af6325.jpg', 'image/jpeg', 16831, '005058d4b8991bf01c400f21d2472cf0b964f64c9c810c4268eb8318fc7f86d6', '2026-08-27 10:07:00-04', '2026-08-27 10:07:00-04', NULL, NULL, NULL, false, 4, NULL, 11);
INSERT INTO public.fotografia (id_fotografia, nombre_archivo, ruta_almacenamiento, tipo_mime, tamano_bytes, hash_sha256, fecha_hora_captura, fecha_hora_carga, latitud, longitud, descripcion, anulada, id_usuario, id_punto, id_revision) VALUES ('6c4573b3-0951-4742-a29c-d89d7ad2bc2c', 'IMG_0011.jpg', 'fotografias/2026/11/6c4573b3-0951-4742-a29c-d89d7ad2bc2c.jpg', 'image/jpeg', 16361, 'a6a7a4aa72c2f9a2d5af6552217c77db2a487f692a86082884808665cb580194', '2026-09-27 14:03:00-03', '2026-09-27 14:03:00-03', NULL, NULL, NULL, false, 4, 9, 12);
INSERT INTO public.fotografia (id_fotografia, nombre_archivo, ruta_almacenamiento, tipo_mime, tamano_bytes, hash_sha256, fecha_hora_captura, fecha_hora_carga, latitud, longitud, descripcion, anulada, id_usuario, id_punto, id_revision) VALUES ('7ceaa29b-5158-41a5-ad20-b2259477c68a', 'IMG_0012.jpg', 'fotografias/2026/11/7ceaa29b-5158-41a5-ad20-b2259477c68a.jpg', 'image/jpeg', 17510, 'bd7728f8f755fa1252d20a90ea38fb8dd396ffd2183319df06ddc555bdeb85a2', '2026-09-27 14:09:00-03', '2026-09-27 14:09:00-03', NULL, NULL, NULL, false, 4, NULL, 12);
INSERT INTO public.fotografia (id_fotografia, nombre_archivo, ruta_almacenamiento, tipo_mime, tamano_bytes, hash_sha256, fecha_hora_captura, fecha_hora_carga, latitud, longitud, descripcion, anulada, id_usuario, id_punto, id_revision) VALUES ('d80ebaca-3693-4c34-8d2b-f603e2bdfc5e', 'IMG_0015.jpg', 'fotografias/2026/11/d80ebaca-3693-4c34-8d2b-f603e2bdfc5e.jpg', 'image/jpeg', 16009, '4c06eac276dfe7c8d856d50cf3ea3e213259b43616619f8f067742c009f72606', '2026-09-22 16:46:00-03', '2026-09-22 16:46:00-03', NULL, NULL, NULL, false, 4, 14, 14);
INSERT INTO public.fotografia (id_fotografia, nombre_archivo, ruta_almacenamiento, tipo_mime, tamano_bytes, hash_sha256, fecha_hora_captura, fecha_hora_carga, latitud, longitud, descripcion, anulada, id_usuario, id_punto, id_revision) VALUES ('580c85be-4f7d-4405-a6ec-a173249d6d6f', 'IMG_0016.jpg', 'fotografias/2026/11/580c85be-4f7d-4405-a6ec-a173249d6d6f.jpg', 'image/jpeg', 17779, 'd4ef616bf251784966ee18c9d60501c73b9e2ca944b63eb002a6f552e94d218a', '2026-10-15 19:44:00-03', '2026-10-15 19:44:00-03', NULL, NULL, NULL, false, 4, 14, 17);
INSERT INTO public.fotografia (id_fotografia, nombre_archivo, ruta_almacenamiento, tipo_mime, tamano_bytes, hash_sha256, fecha_hora_captura, fecha_hora_carga, latitud, longitud, descripcion, anulada, id_usuario, id_punto, id_revision) VALUES ('a1da29ee-121f-4261-9c7d-c933520f905d', 'IMG_0017.jpg', 'fotografias/2026/11/a1da29ee-121f-4261-9c7d-c933520f905d.jpg', 'image/jpeg', 17305, '6e54b6a1d7b315513da5235248e88a750cbb1f9136c6351827c61dd23173f389', '2026-10-21 13:37:00-03', '2026-10-21 13:37:00-03', NULL, NULL, NULL, false, 4, 14, 18);
INSERT INTO public.fotografia (id_fotografia, nombre_archivo, ruta_almacenamiento, tipo_mime, tamano_bytes, hash_sha256, fecha_hora_captura, fecha_hora_carga, latitud, longitud, descripcion, anulada, id_usuario, id_punto, id_revision) VALUES ('c4ab8a79-27f8-4ada-bb68-10517735f3fd', 'IMG_0018.jpg', 'fotografias/2026/11/c4ab8a79-27f8-4ada-bb68-10517735f3fd.jpg', 'image/jpeg', 17251, '57d8aedf765308b95b19e8ad04b9b422338e4eb067fe9158eb2363a9d1045b71', '2026-10-28 16:16:00-03', '2026-10-28 16:16:00-03', NULL, NULL, NULL, false, 4, 14, 19);
INSERT INTO public.fotografia (id_fotografia, nombre_archivo, ruta_almacenamiento, tipo_mime, tamano_bytes, hash_sha256, fecha_hora_captura, fecha_hora_carga, latitud, longitud, descripcion, anulada, id_usuario, id_punto, id_revision) VALUES ('7b5da09b-6281-4dce-9e17-a4b4f26fdf44', 'IMG_0019.jpg', 'fotografias/2026/11/7b5da09b-6281-4dce-9e17-a4b4f26fdf44.jpg', 'image/jpeg', 17045, '74f439c8a283b4c8d05c1ec13b65d5d41985297d48f825c7794c2f9cf5171864', '2026-11-04 14:18:00-03', '2026-11-04 14:18:00-03', NULL, NULL, NULL, false, 4, 14, 20);
INSERT INTO public.fotografia (id_fotografia, nombre_archivo, ruta_almacenamiento, tipo_mime, tamano_bytes, hash_sha256, fecha_hora_captura, fecha_hora_carga, latitud, longitud, descripcion, anulada, id_usuario, id_punto, id_revision) VALUES ('46f624d1-439c-4cd8-81af-56e1f0c19b7f', 'IMG_0021.jpg', 'fotografias/2026/11/46f624d1-439c-4cd8-81af-56e1f0c19b7f.jpg', 'image/jpeg', 16716, '98cfaa4c846ed8c8e13c7828af6bf580733cc48de68228f371a7885b6bdd3e49', '2026-09-22 10:19:00-03', '2026-09-22 10:19:00-03', NULL, NULL, NULL, false, 5, NULL, 29);
INSERT INTO public.fotografia (id_fotografia, nombre_archivo, ruta_almacenamiento, tipo_mime, tamano_bytes, hash_sha256, fecha_hora_captura, fecha_hora_carga, latitud, longitud, descripcion, anulada, id_usuario, id_punto, id_revision) VALUES ('aad242c9-f936-499d-bd65-e982ef0919e7', 'IMG_0022.jpg', 'fotografias/2026/11/aad242c9-f936-499d-bd65-e982ef0919e7.jpg', 'image/jpeg', 17799, '380687d0acaa1e595ec6ef5eb7260d69a4f9d80468f98ddf0d1f4d4e0991221e', '2026-09-30 14:37:00-03', '2026-09-30 14:37:00-03', NULL, NULL, NULL, false, 5, NULL, 30);
INSERT INTO public.fotografia (id_fotografia, nombre_archivo, ruta_almacenamiento, tipo_mime, tamano_bytes, hash_sha256, fecha_hora_captura, fecha_hora_carga, latitud, longitud, descripcion, anulada, id_usuario, id_punto, id_revision) VALUES ('b5ab64eb-b16a-4f3c-b133-15919d6838eb', 'IMG_0023.jpg', 'fotografias/2026/11/b5ab64eb-b16a-4f3c-b133-15919d6838eb.jpg', 'image/jpeg', 18005, 'dcf58fda37d4e4f4a9c1325631f6e2c5fd5c1c518256ba5cc046682f6d1d396e', '2026-10-06 13:00:00-03', '2026-10-06 13:00:00-03', NULL, NULL, NULL, false, 5, NULL, 31);
INSERT INTO public.fotografia (id_fotografia, nombre_archivo, ruta_almacenamiento, tipo_mime, tamano_bytes, hash_sha256, fecha_hora_captura, fecha_hora_carga, latitud, longitud, descripcion, anulada, id_usuario, id_punto, id_revision) VALUES ('7290a589-27c8-4f65-a3f6-9568362c6ca1', 'IMG_0024.jpg', 'fotografias/2026/11/7290a589-27c8-4f65-a3f6-9568362c6ca1.jpg', 'image/jpeg', 17624, '6a7719724db38b578847dd5ca34c0c3133aa36fb1c7f933ebec110abb708d6ed', '2026-10-13 17:19:00-03', '2026-10-13 17:19:00-03', NULL, NULL, NULL, false, 5, NULL, 32);
INSERT INTO public.fotografia (id_fotografia, nombre_archivo, ruta_almacenamiento, tipo_mime, tamano_bytes, hash_sha256, fecha_hora_captura, fecha_hora_carga, latitud, longitud, descripcion, anulada, id_usuario, id_punto, id_revision) VALUES ('cd6c9bb7-6ad0-40e1-b072-334fb7dea772', 'IMG_0025.jpg', 'fotografias/2026/11/cd6c9bb7-6ad0-40e1-b072-334fb7dea772.jpg', 'image/jpeg', 16650, '1896f7b98463662cceddf5920e22a9899434d144516f50a975463a5bfe2c84e3', '2026-10-21 12:19:00-03', '2026-10-21 12:19:00-03', NULL, NULL, NULL, false, 5, NULL, 33);
INSERT INTO public.fotografia (id_fotografia, nombre_archivo, ruta_almacenamiento, tipo_mime, tamano_bytes, hash_sha256, fecha_hora_captura, fecha_hora_carga, latitud, longitud, descripcion, anulada, id_usuario, id_punto, id_revision) VALUES ('eb143f85-c9a3-4365-a2fa-7fe7616878e4', 'IMG_0026.jpg', 'fotografias/2026/11/eb143f85-c9a3-4365-a2fa-7fe7616878e4.jpg', 'image/jpeg', 17116, '0d67dc49d291c9a57aedfcbfa422bcd7a577b93d7cd77113795c1f32d5cb0594', '2026-10-28 19:25:00-03', '2026-10-28 19:25:00-03', NULL, NULL, NULL, false, 5, NULL, 34);
INSERT INTO public.fotografia (id_fotografia, nombre_archivo, ruta_almacenamiento, tipo_mime, tamano_bytes, hash_sha256, fecha_hora_captura, fecha_hora_carga, latitud, longitud, descripcion, anulada, id_usuario, id_punto, id_revision) VALUES ('e9bfadfe-00d7-420d-abdc-54b8c356198d', 'IMG_0027.jpg', 'fotografias/2026/11/e9bfadfe-00d7-420d-abdc-54b8c356198d.jpg', 'image/jpeg', 18315, 'be11dd8cfc5709bff8406ef4931ffc25a527db53dbe6aeb3282fb517b6cf3202', '2026-11-10 10:30:00-03', '2026-11-10 10:30:00-03', NULL, NULL, NULL, false, 5, NULL, 36);
INSERT INTO public.fotografia (id_fotografia, nombre_archivo, ruta_almacenamiento, tipo_mime, tamano_bytes, hash_sha256, fecha_hora_captura, fecha_hora_carga, latitud, longitud, descripcion, anulada, id_usuario, id_punto, id_revision) VALUES ('4f4c3415-e8d4-47a7-81d6-ec7c671b653d', 'IMG_0028.jpg', 'fotografias/2026/11/4f4c3415-e8d4-47a7-81d6-ec7c671b653d.jpg', 'image/jpeg', 17588, '5554b3f2be28a36373632a9b099f7b1f871701fed680b551d0f3492240c3653f', '2026-08-27 17:45:00-04', '2026-08-27 17:45:00-04', NULL, NULL, NULL, false, 5, 9, 42);
INSERT INTO public.fotografia (id_fotografia, nombre_archivo, ruta_almacenamiento, tipo_mime, tamano_bytes, hash_sha256, fecha_hora_captura, fecha_hora_carga, latitud, longitud, descripcion, anulada, id_usuario, id_punto, id_revision) VALUES ('86536901-5a47-4f10-b77c-e20fc9bd1a82', 'IMG_0029.jpg', 'fotografias/2026/11/86536901-5a47-4f10-b77c-e20fc9bd1a82.jpg', 'image/jpeg', 16044, '163aa55e687d360ff7737570ead7204a777270bc3355697129d47f4d17f9173f', '2026-08-27 17:51:00-04', '2026-08-27 17:51:00-04', NULL, NULL, NULL, false, 5, NULL, 42);
INSERT INTO public.fotografia (id_fotografia, nombre_archivo, ruta_almacenamiento, tipo_mime, tamano_bytes, hash_sha256, fecha_hora_captura, fecha_hora_carga, latitud, longitud, descripcion, anulada, id_usuario, id_punto, id_revision) VALUES ('5d01c872-ec81-4aaa-9956-fa39613cf04f', 'IMG_0030.jpg', 'fotografias/2026/11/5d01c872-ec81-4aaa-9956-fa39613cf04f.jpg', 'image/jpeg', 17655, '70bc209cf774b8e7acc62fe6b3f195aaed41cde6577974bc5f78b7014ad8dba0', '2026-09-26 11:56:00-03', '2026-09-26 11:56:00-03', NULL, NULL, NULL, false, 5, 9, 43);
INSERT INTO public.fotografia (id_fotografia, nombre_archivo, ruta_almacenamiento, tipo_mime, tamano_bytes, hash_sha256, fecha_hora_captura, fecha_hora_carga, latitud, longitud, descripcion, anulada, id_usuario, id_punto, id_revision) VALUES ('54f0480e-7434-4e99-969f-559164a04447', 'IMG_0031.jpg', 'fotografias/2026/11/54f0480e-7434-4e99-969f-559164a04447.jpg', 'image/jpeg', 16245, 'fca70a2865a7875024088eb26a4efb1be244ff8626ad054e3b260fb1685d8da5', '2026-09-26 12:02:00-03', '2026-09-26 12:02:00-03', NULL, NULL, NULL, false, 5, NULL, 43);
INSERT INTO public.fotografia (id_fotografia, nombre_archivo, ruta_almacenamiento, tipo_mime, tamano_bytes, hash_sha256, fecha_hora_captura, fecha_hora_carga, latitud, longitud, descripcion, anulada, id_usuario, id_punto, id_revision) VALUES ('d6bf8297-47cb-4f14-8d18-3c0dd175ca5c', 'IMG_0032.jpg', 'fotografias/2026/11/d6bf8297-47cb-4f14-8d18-3c0dd175ca5c.jpg', 'image/jpeg', 17015, 'd634da2ab054cf6d9031d381180c7c0854cee53e215ccc953813e3bb3c2f4cb0', '2026-10-26 17:47:00-03', '2026-10-26 17:47:00-03', NULL, NULL, NULL, false, 5, 9, 44);
INSERT INTO public.fotografia (id_fotografia, nombre_archivo, ruta_almacenamiento, tipo_mime, tamano_bytes, hash_sha256, fecha_hora_captura, fecha_hora_carga, latitud, longitud, descripcion, anulada, id_usuario, id_punto, id_revision) VALUES ('4e04fbd7-aad0-44a3-b582-b60654c5bcf0', 'IMG_0033.jpg', 'fotografias/2026/11/4e04fbd7-aad0-44a3-b582-b60654c5bcf0.jpg', 'image/jpeg', 16247, 'c4f88e50458221fb994172aa1ac7fd61dbcbf3e2638bddcfb9c598394765e36c', '2026-10-26 17:53:00-03', '2026-10-26 17:53:00-03', NULL, NULL, NULL, false, 5, NULL, 44);
INSERT INTO public.fotografia (id_fotografia, nombre_archivo, ruta_almacenamiento, tipo_mime, tamano_bytes, hash_sha256, fecha_hora_captura, fecha_hora_carga, latitud, longitud, descripcion, anulada, id_usuario, id_punto, id_revision) VALUES ('2c529cf8-8103-4c5d-bfb8-cc41c425ebf0', 'IMG_0034.jpg', 'fotografias/2026/11/2c529cf8-8103-4c5d-bfb8-cc41c425ebf0.jpg', 'image/jpeg', 16654, '926c89453dbbbe967b0d660b79d6b64803bc25703d8936fa512c9d3c9893bc8e', '2026-10-07 17:50:00-03', '2026-10-07 17:50:00-03', NULL, NULL, NULL, false, 6, NULL, 45);
INSERT INTO public.fotografia (id_fotografia, nombre_archivo, ruta_almacenamiento, tipo_mime, tamano_bytes, hash_sha256, fecha_hora_captura, fecha_hora_carga, latitud, longitud, descripcion, anulada, id_usuario, id_punto, id_revision) VALUES ('3949d63c-c565-4b94-b870-0c305ede6158', 'IMG_0035.jpg', 'fotografias/2026/11/3949d63c-c565-4b94-b870-0c305ede6158.jpg', 'image/jpeg', 16830, '90387235883c18c2e93eb8279dcd6b1564d3d2339d22dd697f0225bef98050d7', '2026-10-13 18:34:00-03', '2026-10-13 18:34:00-03', NULL, NULL, NULL, false, 6, NULL, 46);
INSERT INTO public.fotografia (id_fotografia, nombre_archivo, ruta_almacenamiento, tipo_mime, tamano_bytes, hash_sha256, fecha_hora_captura, fecha_hora_carga, latitud, longitud, descripcion, anulada, id_usuario, id_punto, id_revision) VALUES ('30d101bc-8e61-4ed9-8bed-cf3c1f2b22a5', 'IMG_0036.jpg', 'fotografias/2026/11/30d101bc-8e61-4ed9-8bed-cf3c1f2b22a5.jpg', 'image/jpeg', 16871, 'f25d2afdfba3cbede6761eafd9cc4df48ff7b28af72d8ebb708606b4185acacd', '2026-10-20 17:53:00-03', '2026-10-20 17:53:00-03', NULL, NULL, NULL, false, 6, NULL, 47);
INSERT INTO public.fotografia (id_fotografia, nombre_archivo, ruta_almacenamiento, tipo_mime, tamano_bytes, hash_sha256, fecha_hora_captura, fecha_hora_carga, latitud, longitud, descripcion, anulada, id_usuario, id_punto, id_revision) VALUES ('c9d95811-4bf7-49ce-88e3-0b6adc199bf7', 'IMG_0037.jpg', 'fotografias/2026/11/c9d95811-4bf7-49ce-88e3-0b6adc199bf7.jpg', 'image/jpeg', 16679, '8ad45643e15b2927615c38637cd52e8f42662064ea4b70cbc9a9079d7d712a79', '2026-10-27 13:25:00-03', '2026-10-27 13:25:00-03', NULL, NULL, NULL, false, 6, NULL, 48);
INSERT INTO public.fotografia (id_fotografia, nombre_archivo, ruta_almacenamiento, tipo_mime, tamano_bytes, hash_sha256, fecha_hora_captura, fecha_hora_carga, latitud, longitud, descripcion, anulada, id_usuario, id_punto, id_revision) VALUES ('a74d76f5-0f86-4ce6-a1dc-169b58cbb3af', 'IMG_0038.jpg', 'fotografias/2026/11/a74d76f5-0f86-4ce6-a1dc-169b58cbb3af.jpg', 'image/jpeg', 17607, 'dc8b233c9816fae749ac429646e6ac9c345937e3c5928085685ec71e6b414253', '2026-11-03 12:25:00-03', '2026-11-03 12:25:00-03', NULL, NULL, NULL, false, 6, NULL, 49);
INSERT INTO public.fotografia (id_fotografia, nombre_archivo, ruta_almacenamiento, tipo_mime, tamano_bytes, hash_sha256, fecha_hora_captura, fecha_hora_carga, latitud, longitud, descripcion, anulada, id_usuario, id_punto, id_revision) VALUES ('cb57fe1d-d908-4ccd-9aac-4de9922eed9f', 'IMG_0039.jpg', 'fotografias/2026/11/cb57fe1d-d908-4ccd-9aac-4de9922eed9f.jpg', 'image/jpeg', 16646, 'd904c07d786dda1a775c952b6ebae8711a446257bde805133881a1f7c4b14a6a', '2026-10-27 10:37:00-03', '2026-10-27 10:37:00-03', NULL, NULL, NULL, false, 4, 9, 13);
INSERT INTO public.fotografia (id_fotografia, nombre_archivo, ruta_almacenamiento, tipo_mime, tamano_bytes, hash_sha256, fecha_hora_captura, fecha_hora_carga, latitud, longitud, descripcion, anulada, id_usuario, id_punto, id_revision) VALUES ('2bd03346-70e8-4e20-8607-e42459c3397e', 'IMG_0040.jpg', 'fotografias/2026/11/2bd03346-70e8-4e20-8607-e42459c3397e.jpg', 'image/jpeg', 16656, 'a6c739329c301179d2cd4c263a5b528b6e8cb37a96d148c79145501b7f58805b', '2026-10-27 10:43:00-03', '2026-10-27 10:43:00-03', NULL, NULL, NULL, false, 4, NULL, 13);
INSERT INTO public.fotografia (id_fotografia, nombre_archivo, ruta_almacenamiento, tipo_mime, tamano_bytes, hash_sha256, fecha_hora_captura, fecha_hora_carga, latitud, longitud, descripcion, anulada, id_usuario, id_punto, id_revision) VALUES ('d0fdbb9b-ba7e-4602-b38f-a599e2b10c42', 'IMG_0041.jpg', 'fotografias/2026/11/d0fdbb9b-ba7e-4602-b38f-a599e2b10c42.jpg', 'image/jpeg', 16777, '8b200753df61cb1afafde50b9beb3981539b3d02eb45f57467028da9db6857ae', '2026-11-11 10:35:00-03', '2026-11-11 10:35:00-03', NULL, NULL, NULL, false, 4, 14, 21);


ALTER TABLE public.fotografia ENABLE TRIGGER ALL;

--
-- Data for Name: hallazgo; Type: TABLE DATA; Schema: public; Owner: -
--

ALTER TABLE public.hallazgo DISABLE TRIGGER ALL;

INSERT INTO public.hallazgo (id_hallazgo, descripcion, criticidad, estado, fecha_apertura, fecha_cierre, acciones, id_usuario_cierre, id_revision) VALUES (1, 'Sensor de CO marca 8 ppm en aire limpio y no vuelve a cero. Se retira el equipo de la unidad H-8 hasta su calibración.', 'alta', 'abierto', '2026-10-27 10:45:00-03', NULL, NULL, NULL, 13);
INSERT INTO public.hallazgo (id_hallazgo, descripcion, criticidad, estado, fecha_apertura, fecha_cierre, acciones, id_usuario_cierre, id_revision) VALUES (2, 'Cadena con desgaste en eslabones; requiere reemplazo.', 'media', 'abierto', '2026-11-11 10:41:00-03', NULL, NULL, NULL, 21);
INSERT INTO public.hallazgo (id_hallazgo, descripcion, criticidad, estado, fecha_apertura, fecha_cierre, acciones, id_usuario_cierre, id_revision) VALUES (3, 'Fuga leve en acople de la manguera de presión.', 'baja', 'cerrado', '2026-10-28 10:39:00-03', '2026-11-17 22:05:11.589332-03', 'Se reemplazó la junta tórica del acople y se probó sin fugas.', 3, 41);


ALTER TABLE public.hallazgo ENABLE TRIGGER ALL;

--
-- Data for Name: movimiento; Type: TABLE DATA; Schema: public; Owner: -
--

ALTER TABLE public.movimiento DISABLE TRIGGER ALL;

INSERT INTO public.movimiento (id_movimiento, fecha_hora, motivo, id_cajonera_destino, id_cajonera_origen, id_material, id_usuario) VALUES (1, '2026-11-17 22:05:10.794385-03', 'Alta inicial', 1, NULL, 1, 3);
INSERT INTO public.movimiento (id_movimiento, fecha_hora, motivo, id_cajonera_destino, id_cajonera_origen, id_material, id_usuario) VALUES (2, '2026-11-17 22:05:10.797832-03', 'Alta inicial', 9, NULL, 2, 3);
INSERT INTO public.movimiento (id_movimiento, fecha_hora, motivo, id_cajonera_destino, id_cajonera_origen, id_material, id_usuario) VALUES (3, '2026-11-17 22:05:10.801137-03', 'Alta inicial', 3, NULL, 3, 3);
INSERT INTO public.movimiento (id_movimiento, fecha_hora, motivo, id_cajonera_destino, id_cajonera_origen, id_material, id_usuario) VALUES (4, '2026-11-17 22:05:10.803909-03', 'Alta inicial', 10, NULL, 4, 3);
INSERT INTO public.movimiento (id_movimiento, fecha_hora, motivo, id_cajonera_destino, id_cajonera_origen, id_material, id_usuario) VALUES (5, '2026-11-17 22:05:10.806929-03', 'Alta inicial', 5, NULL, 5, 3);
INSERT INTO public.movimiento (id_movimiento, fecha_hora, motivo, id_cajonera_destino, id_cajonera_origen, id_material, id_usuario) VALUES (6, '2026-11-17 22:05:10.809566-03', 'Alta inicial', 11, NULL, 6, 3);
INSERT INTO public.movimiento (id_movimiento, fecha_hora, motivo, id_cajonera_destino, id_cajonera_origen, id_material, id_usuario) VALUES (7, '2026-11-17 22:05:10.812373-03', 'Alta inicial', 9, NULL, 7, 3);
INSERT INTO public.movimiento (id_movimiento, fecha_hora, motivo, id_cajonera_destino, id_cajonera_origen, id_material, id_usuario) VALUES (8, '2026-11-17 22:05:10.81508-03', 'Alta inicial', 13, NULL, 8, 3);
INSERT INTO public.movimiento (id_movimiento, fecha_hora, motivo, id_cajonera_destino, id_cajonera_origen, id_material, id_usuario) VALUES (9, '2026-11-17 22:05:10.817795-03', 'Alta inicial', 1, NULL, 9, 3);
INSERT INTO public.movimiento (id_movimiento, fecha_hora, motivo, id_cajonera_destino, id_cajonera_origen, id_material, id_usuario) VALUES (10, '2026-11-17 22:05:10.820379-03', 'Alta inicial', 1, NULL, 10, 3);
INSERT INTO public.movimiento (id_movimiento, fecha_hora, motivo, id_cajonera_destino, id_cajonera_origen, id_material, id_usuario) VALUES (11, '2026-11-17 22:05:10.823066-03', 'Alta inicial', 11, NULL, 11, 3);
INSERT INTO public.movimiento (id_movimiento, fecha_hora, motivo, id_cajonera_destino, id_cajonera_origen, id_material, id_usuario) VALUES (12, '2026-11-17 22:05:10.82556-03', 'Alta inicial', 12, NULL, 12, 3);
INSERT INTO public.movimiento (id_movimiento, fecha_hora, motivo, id_cajonera_destino, id_cajonera_origen, id_material, id_usuario) VALUES (13, '2026-11-17 22:05:10.828672-03', 'Alta inicial', 2, NULL, 13, 3);
INSERT INTO public.movimiento (id_movimiento, fecha_hora, motivo, id_cajonera_destino, id_cajonera_origen, id_material, id_usuario) VALUES (14, '2026-11-17 22:05:10.831617-03', 'Alta inicial', 2, NULL, 14, 3);
INSERT INTO public.movimiento (id_movimiento, fecha_hora, motivo, id_cajonera_destino, id_cajonera_origen, id_material, id_usuario) VALUES (15, '2026-11-17 22:05:10.834413-03', 'Alta inicial', 14, NULL, 15, 3);


ALTER TABLE public.movimiento ENABLE TRIGGER ALL;

--
-- Data for Name: notificacion; Type: TABLE DATA; Schema: public; Owner: -
--

ALTER TABLE public.notificacion DISABLE TRIGGER ALL;

INSERT INTO public.notificacion (id_notificacion, tipo, mensaje, fecha_generacion, fecha_lectura, leida, id_usuario, id_revision) VALUES (9, 'asignacion', 'Nueva revisión asignada: Motobomba portátil (8C-0112 · B-8 / Cabina trasera), fecha límite 18-11-2026.', '2026-11-17 22:05:10.90269-03', NULL, false, 4, 9);
INSERT INTO public.notificacion (id_notificacion, tipo, mensaje, fecha_generacion, fecha_lectura, leida, id_usuario, id_revision) VALUES (10, 'asignacion', 'Nueva revisión asignada: Motobomba portátil (8C-0112 · B-8 / Cabina trasera), fecha límite 25-11-2026.', '2026-11-17 22:05:10.906915-03', NULL, false, 4, 10);
INSERT INTO public.notificacion (id_notificacion, tipo, mensaje, fecha_generacion, fecha_lectura, leida, id_usuario, id_revision) VALUES (22, 'asignacion', 'Nueva revisión asignada: Motosierra de rescate (8C-0233 · B-8 / Cajonera 2), fecha límite 18-11-2026.', '2026-11-17 22:05:10.962876-03', NULL, false, 4, 22);
INSERT INTO public.notificacion (id_notificacion, tipo, mensaje, fecha_generacion, fecha_lectura, leida, id_usuario, id_revision) VALUES (23, 'asignacion', 'Nueva revisión asignada: Motosierra de rescate (8C-0233 · B-8 / Cajonera 2), fecha límite 25-11-2026.', '2026-11-17 22:05:10.96834-03', NULL, false, 4, 23);
INSERT INTO public.notificacion (id_notificacion, tipo, mensaje, fecha_generacion, fecha_lectura, leida, id_usuario, id_revision) VALUES (28, 'asignacion', 'Nueva revisión asignada: Generador eléctrico (8C-0390 · F-8 / Cajonera 1), fecha límite 19-11-2026.', '2026-11-17 22:05:10.989895-03', NULL, false, 4, 28);
INSERT INTO public.notificacion (id_notificacion, tipo, mensaje, fecha_generacion, fecha_lectura, leida, id_usuario, id_revision) VALUES (37, 'asignacion', 'Nueva revisión asignada: Ventilador de presión positiva (8C-0101 · B-8 / Cajonera 4), fecha límite 18-11-2026.', '2026-11-17 22:05:11.023377-03', NULL, false, 5, 37);
INSERT INTO public.notificacion (id_notificacion, tipo, mensaje, fecha_generacion, fecha_lectura, leida, id_usuario, id_revision) VALUES (38, 'asignacion', 'Nueva revisión asignada: Ventilador de presión positiva (8C-0101 · B-8 / Cajonera 4), fecha límite 25-11-2026.', '2026-11-17 22:05:11.026709-03', NULL, false, 5, 38);
INSERT INTO public.notificacion (id_notificacion, tipo, mensaje, fecha_generacion, fecha_lectura, leida, id_usuario, id_revision) VALUES (57, 'asignacion', 'Nueva revisión asignada: Motobomba de achique (8C-0120 · BOD / Estante A), fecha límite 18-11-2026.', '2026-11-17 22:05:11.09179-03', NULL, false, 6, 51);
INSERT INTO public.notificacion (id_notificacion, tipo, mensaje, fecha_generacion, fecha_lectura, leida, id_usuario, id_revision) VALUES (58, 'asignacion', 'Nueva revisión asignada: Motobomba de achique (8C-0120 · BOD / Estante A), fecha límite 18-11-2026.', '2026-11-17 22:05:11.092552-03', NULL, false, 4, 51);
INSERT INTO public.notificacion (id_notificacion, tipo, mensaje, fecha_generacion, fecha_lectura, leida, id_usuario, id_revision) VALUES (59, 'asignacion', 'Nueva revisión asignada: Motobomba de achique (8C-0120 · BOD / Estante A), fecha límite 25-11-2026.', '2026-11-17 22:05:11.096156-03', NULL, false, 6, 52);
INSERT INTO public.notificacion (id_notificacion, tipo, mensaje, fecha_generacion, fecha_lectura, leida, id_usuario, id_revision) VALUES (60, 'asignacion', 'Nueva revisión asignada: Motobomba de achique (8C-0120 · BOD / Estante A), fecha límite 25-11-2026.', '2026-11-17 22:05:11.097021-03', NULL, false, 4, 52);
INSERT INTO public.notificacion (id_notificacion, tipo, mensaje, fecha_generacion, fecha_lectura, leida, id_usuario, id_revision) VALUES (64, 'recordatorio', 'Recordatorio: la revisión de Motobomba de achique (8C-0120 · BOD / Estante A) vence mañana (18-11-2026).', '2026-11-17 22:05:11.616036-03', NULL, false, 6, 51);
INSERT INTO public.notificacion (id_notificacion, tipo, mensaje, fecha_generacion, fecha_lectura, leida, id_usuario, id_revision) VALUES (65, 'recordatorio', 'Recordatorio: la revisión de Motobomba de achique (8C-0120 · BOD / Estante A) vence mañana (18-11-2026).', '2026-11-17 22:05:11.617636-03', NULL, false, 4, 51);
INSERT INTO public.notificacion (id_notificacion, tipo, mensaje, fecha_generacion, fecha_lectura, leida, id_usuario, id_revision) VALUES (66, 'recordatorio', 'Recordatorio: la revisión de Motobomba de achique (8C-0120 · BOD / Estante A) vence mañana (18-11-2026). Responsables: P. Lagos, J. Soto.', '2026-11-17 22:05:11.620521-03', NULL, false, 3, 51);
INSERT INTO public.notificacion (id_notificacion, tipo, mensaje, fecha_generacion, fecha_lectura, leida, id_usuario, id_revision) VALUES (67, 'recordatorio', 'Recordatorio: la revisión de Ventilador de presión positiva (8C-0101 · B-8 / Cajonera 4) vence mañana (18-11-2026).', '2026-11-17 22:05:11.622155-03', NULL, false, 5, 37);
INSERT INTO public.notificacion (id_notificacion, tipo, mensaje, fecha_generacion, fecha_lectura, leida, id_usuario, id_revision) VALUES (68, 'recordatorio', 'Recordatorio: la revisión de Ventilador de presión positiva (8C-0101 · B-8 / Cajonera 4) vence mañana (18-11-2026). Responsable: M. Rivas.', '2026-11-17 22:05:11.62459-03', NULL, false, 3, 37);
INSERT INTO public.notificacion (id_notificacion, tipo, mensaje, fecha_generacion, fecha_lectura, leida, id_usuario, id_revision) VALUES (69, 'recordatorio', 'Recordatorio: la revisión de Motosierra de rescate (8C-0233 · B-8 / Cajonera 2) vence mañana (18-11-2026).', '2026-11-17 22:05:11.626029-03', NULL, false, 4, 22);
INSERT INTO public.notificacion (id_notificacion, tipo, mensaje, fecha_generacion, fecha_lectura, leida, id_usuario, id_revision) VALUES (70, 'recordatorio', 'Recordatorio: la revisión de Motosierra de rescate (8C-0233 · B-8 / Cajonera 2) vence mañana (18-11-2026). Responsable: J. Soto.', '2026-11-17 22:05:11.628827-03', NULL, false, 3, 22);
INSERT INTO public.notificacion (id_notificacion, tipo, mensaje, fecha_generacion, fecha_lectura, leida, id_usuario, id_revision) VALUES (71, 'recordatorio', 'Recordatorio: la revisión de Motobomba portátil (8C-0112 · B-8 / Cabina trasera) vence mañana (18-11-2026).', '2026-11-17 22:05:11.630318-03', NULL, false, 4, 9);
INSERT INTO public.notificacion (id_notificacion, tipo, mensaje, fecha_generacion, fecha_lectura, leida, id_usuario, id_revision) VALUES (72, 'recordatorio', 'Recordatorio: la revisión de Motobomba portátil (8C-0112 · B-8 / Cabina trasera) vence mañana (18-11-2026). Responsable: J. Soto.', '2026-11-17 22:05:11.632815-03', NULL, false, 3, 9);
INSERT INTO public.notificacion (id_notificacion, tipo, mensaje, fecha_generacion, fecha_lectura, leida, id_usuario, id_revision) VALUES (1, 'asignacion', 'Nueva revisión asignada: Motobomba portátil (8C-0112 · B-8 / Cabina trasera), fecha límite 23-09-2026.', '2026-11-17 22:05:10.871396-03', '2026-11-15 22:05:11.657101-03', true, 4, 1);
INSERT INTO public.notificacion (id_notificacion, tipo, mensaje, fecha_generacion, fecha_lectura, leida, id_usuario, id_revision) VALUES (2, 'asignacion', 'Nueva revisión asignada: Motobomba portátil (8C-0112 · B-8 / Cabina trasera), fecha límite 30-09-2026.', '2026-11-17 22:05:10.875167-03', '2026-11-15 22:05:11.657101-03', true, 4, 2);
INSERT INTO public.notificacion (id_notificacion, tipo, mensaje, fecha_generacion, fecha_lectura, leida, id_usuario, id_revision) VALUES (3, 'asignacion', 'Nueva revisión asignada: Motobomba portátil (8C-0112 · B-8 / Cabina trasera), fecha límite 07-10-2026.', '2026-11-17 22:05:10.879526-03', '2026-11-15 22:05:11.657101-03', true, 4, 3);
INSERT INTO public.notificacion (id_notificacion, tipo, mensaje, fecha_generacion, fecha_lectura, leida, id_usuario, id_revision) VALUES (4, 'asignacion', 'Nueva revisión asignada: Motobomba portátil (8C-0112 · B-8 / Cabina trasera), fecha límite 14-10-2026.', '2026-11-17 22:05:10.883181-03', '2026-11-15 22:05:11.657101-03', true, 4, 4);
INSERT INTO public.notificacion (id_notificacion, tipo, mensaje, fecha_generacion, fecha_lectura, leida, id_usuario, id_revision) VALUES (5, 'asignacion', 'Nueva revisión asignada: Motobomba portátil (8C-0112 · B-8 / Cabina trasera), fecha límite 21-10-2026.', '2026-11-17 22:05:10.886678-03', '2026-11-15 22:05:11.657101-03', true, 4, 5);
INSERT INTO public.notificacion (id_notificacion, tipo, mensaje, fecha_generacion, fecha_lectura, leida, id_usuario, id_revision) VALUES (6, 'asignacion', 'Nueva revisión asignada: Motobomba portátil (8C-0112 · B-8 / Cabina trasera), fecha límite 28-10-2026.', '2026-11-17 22:05:10.890475-03', '2026-11-15 22:05:11.657101-03', true, 4, 6);
INSERT INTO public.notificacion (id_notificacion, tipo, mensaje, fecha_generacion, fecha_lectura, leida, id_usuario, id_revision) VALUES (7, 'asignacion', 'Nueva revisión asignada: Motobomba portátil (8C-0112 · B-8 / Cabina trasera), fecha límite 04-11-2026.', '2026-11-17 22:05:10.894018-03', '2026-11-15 22:05:11.657101-03', true, 4, 7);
INSERT INTO public.notificacion (id_notificacion, tipo, mensaje, fecha_generacion, fecha_lectura, leida, id_usuario, id_revision) VALUES (8, 'asignacion', 'Nueva revisión asignada: Motobomba portátil (8C-0112 · B-8 / Cabina trasera), fecha límite 11-11-2026.', '2026-11-17 22:05:10.897723-03', '2026-11-15 22:05:11.657101-03', true, 4, 8);
INSERT INTO public.notificacion (id_notificacion, tipo, mensaje, fecha_generacion, fecha_lectura, leida, id_usuario, id_revision) VALUES (11, 'asignacion', 'Nueva revisión asignada: Detector multigas (8C-0457 · H-8 / Cajonera 3), fecha límite 27-08-2026.', '2026-11-17 22:05:10.913183-03', '2026-11-15 22:05:11.657101-03', true, 4, 11);
INSERT INTO public.notificacion (id_notificacion, tipo, mensaje, fecha_generacion, fecha_lectura, leida, id_usuario, id_revision) VALUES (12, 'asignacion', 'Nueva revisión asignada: Detector multigas (8C-0457 · H-8 / Cajonera 3), fecha límite 27-09-2026.', '2026-11-17 22:05:10.917119-03', '2026-11-15 22:05:11.657101-03', true, 4, 12);
INSERT INTO public.notificacion (id_notificacion, tipo, mensaje, fecha_generacion, fecha_lectura, leida, id_usuario, id_revision) VALUES (13, 'asignacion', 'Nueva revisión asignada: Detector multigas (8C-0457 · H-8 / Cajonera 3), fecha límite 27-10-2026.', '2026-11-17 22:05:10.920852-03', '2026-11-15 22:05:11.657101-03', true, 4, 13);
INSERT INTO public.notificacion (id_notificacion, tipo, mensaje, fecha_generacion, fecha_lectura, leida, id_usuario, id_revision) VALUES (14, 'asignacion', 'Nueva revisión asignada: Motosierra de rescate (8C-0233 · B-8 / Cajonera 2), fecha límite 23-09-2026.', '2026-11-17 22:05:10.926588-03', '2026-11-15 22:05:11.657101-03', true, 4, 14);
INSERT INTO public.notificacion (id_notificacion, tipo, mensaje, fecha_generacion, fecha_lectura, leida, id_usuario, id_revision) VALUES (15, 'asignacion', 'Nueva revisión asignada: Motosierra de rescate (8C-0233 · B-8 / Cajonera 2), fecha límite 30-09-2026.', '2026-11-17 22:05:10.930598-03', '2026-11-15 22:05:11.657101-03', true, 4, 15);
INSERT INTO public.notificacion (id_notificacion, tipo, mensaje, fecha_generacion, fecha_lectura, leida, id_usuario, id_revision) VALUES (16, 'asignacion', 'Nueva revisión asignada: Motosierra de rescate (8C-0233 · B-8 / Cajonera 2), fecha límite 07-10-2026.', '2026-11-17 22:05:10.93454-03', '2026-11-15 22:05:11.657101-03', true, 4, 16);
INSERT INTO public.notificacion (id_notificacion, tipo, mensaje, fecha_generacion, fecha_lectura, leida, id_usuario, id_revision) VALUES (17, 'asignacion', 'Nueva revisión asignada: Motosierra de rescate (8C-0233 · B-8 / Cajonera 2), fecha límite 14-10-2026.', '2026-11-17 22:05:10.93921-03', '2026-11-15 22:05:11.657101-03', true, 4, 17);
INSERT INTO public.notificacion (id_notificacion, tipo, mensaje, fecha_generacion, fecha_lectura, leida, id_usuario, id_revision) VALUES (18, 'asignacion', 'Nueva revisión asignada: Motosierra de rescate (8C-0233 · B-8 / Cajonera 2), fecha límite 21-10-2026.', '2026-11-17 22:05:10.943339-03', '2026-11-15 22:05:11.657101-03', true, 4, 18);
INSERT INTO public.notificacion (id_notificacion, tipo, mensaje, fecha_generacion, fecha_lectura, leida, id_usuario, id_revision) VALUES (19, 'asignacion', 'Nueva revisión asignada: Motosierra de rescate (8C-0233 · B-8 / Cajonera 2), fecha límite 28-10-2026.', '2026-11-17 22:05:10.947089-03', '2026-11-15 22:05:11.657101-03', true, 4, 19);
INSERT INTO public.notificacion (id_notificacion, tipo, mensaje, fecha_generacion, fecha_lectura, leida, id_usuario, id_revision) VALUES (20, 'asignacion', 'Nueva revisión asignada: Motosierra de rescate (8C-0233 · B-8 / Cajonera 2), fecha límite 04-11-2026.', '2026-11-17 22:05:10.951068-03', '2026-11-15 22:05:11.657101-03', true, 4, 20);
INSERT INTO public.notificacion (id_notificacion, tipo, mensaje, fecha_generacion, fecha_lectura, leida, id_usuario, id_revision) VALUES (21, 'asignacion', 'Nueva revisión asignada: Motosierra de rescate (8C-0233 · B-8 / Cajonera 2), fecha límite 11-11-2026.', '2026-11-17 22:05:10.954445-03', '2026-11-15 22:05:11.657101-03', true, 4, 21);
INSERT INTO public.notificacion (id_notificacion, tipo, mensaje, fecha_generacion, fecha_lectura, leida, id_usuario, id_revision) VALUES (24, 'asignacion', 'Nueva revisión asignada: Generador eléctrico (8C-0390 · F-8 / Cajonera 1), fecha límite 24-09-2026.', '2026-11-17 22:05:10.975143-03', '2026-11-15 22:05:11.657101-03', true, 4, 24);
INSERT INTO public.notificacion (id_notificacion, tipo, mensaje, fecha_generacion, fecha_lectura, leida, id_usuario, id_revision) VALUES (25, 'asignacion', 'Nueva revisión asignada: Generador eléctrico (8C-0390 · F-8 / Cajonera 1), fecha límite 08-10-2026.', '2026-11-17 22:05:10.979037-03', '2026-11-15 22:05:11.657101-03', true, 4, 25);
INSERT INTO public.notificacion (id_notificacion, tipo, mensaje, fecha_generacion, fecha_lectura, leida, id_usuario, id_revision) VALUES (26, 'asignacion', 'Nueva revisión asignada: Generador eléctrico (8C-0390 · F-8 / Cajonera 1), fecha límite 22-10-2026.', '2026-11-17 22:05:10.982402-03', '2026-11-15 22:05:11.657101-03', true, 4, 26);
INSERT INTO public.notificacion (id_notificacion, tipo, mensaje, fecha_generacion, fecha_lectura, leida, id_usuario, id_revision) VALUES (27, 'asignacion', 'Nueva revisión asignada: Generador eléctrico (8C-0390 · F-8 / Cajonera 1), fecha límite 05-11-2026.', '2026-11-17 22:05:10.985718-03', '2026-11-15 22:05:11.657101-03', true, 4, 27);
INSERT INTO public.notificacion (id_notificacion, tipo, mensaje, fecha_generacion, fecha_lectura, leida, id_usuario, id_revision) VALUES (29, 'asignacion', 'Nueva revisión asignada: Ventilador de presión positiva (8C-0101 · B-8 / Cajonera 4), fecha límite 23-09-2026.', '2026-11-17 22:05:10.995151-03', '2026-11-15 22:05:11.657101-03', true, 5, 29);
INSERT INTO public.notificacion (id_notificacion, tipo, mensaje, fecha_generacion, fecha_lectura, leida, id_usuario, id_revision) VALUES (30, 'asignacion', 'Nueva revisión asignada: Ventilador de presión positiva (8C-0101 · B-8 / Cajonera 4), fecha límite 30-09-2026.', '2026-11-17 22:05:10.998686-03', '2026-11-15 22:05:11.657101-03', true, 5, 30);
INSERT INTO public.notificacion (id_notificacion, tipo, mensaje, fecha_generacion, fecha_lectura, leida, id_usuario, id_revision) VALUES (31, 'asignacion', 'Nueva revisión asignada: Ventilador de presión positiva (8C-0101 · B-8 / Cajonera 4), fecha límite 07-10-2026.', '2026-11-17 22:05:11.002375-03', '2026-11-15 22:05:11.657101-03', true, 5, 31);
INSERT INTO public.notificacion (id_notificacion, tipo, mensaje, fecha_generacion, fecha_lectura, leida, id_usuario, id_revision) VALUES (32, 'asignacion', 'Nueva revisión asignada: Ventilador de presión positiva (8C-0101 · B-8 / Cajonera 4), fecha límite 14-10-2026.', '2026-11-17 22:05:11.006128-03', '2026-11-15 22:05:11.657101-03', true, 5, 32);
INSERT INTO public.notificacion (id_notificacion, tipo, mensaje, fecha_generacion, fecha_lectura, leida, id_usuario, id_revision) VALUES (33, 'asignacion', 'Nueva revisión asignada: Ventilador de presión positiva (8C-0101 · B-8 / Cajonera 4), fecha límite 21-10-2026.', '2026-11-17 22:05:11.009672-03', '2026-11-15 22:05:11.657101-03', true, 5, 33);
INSERT INTO public.notificacion (id_notificacion, tipo, mensaje, fecha_generacion, fecha_lectura, leida, id_usuario, id_revision) VALUES (34, 'asignacion', 'Nueva revisión asignada: Ventilador de presión positiva (8C-0101 · B-8 / Cajonera 4), fecha límite 28-10-2026.', '2026-11-17 22:05:11.01303-03', '2026-11-15 22:05:11.657101-03', true, 5, 34);
INSERT INTO public.notificacion (id_notificacion, tipo, mensaje, fecha_generacion, fecha_lectura, leida, id_usuario, id_revision) VALUES (35, 'asignacion', 'Nueva revisión asignada: Ventilador de presión positiva (8C-0101 · B-8 / Cajonera 4), fecha límite 04-11-2026.', '2026-11-17 22:05:11.01635-03', '2026-11-15 22:05:11.657101-03', true, 5, 35);
INSERT INTO public.notificacion (id_notificacion, tipo, mensaje, fecha_generacion, fecha_lectura, leida, id_usuario, id_revision) VALUES (36, 'asignacion', 'Nueva revisión asignada: Ventilador de presión positiva (8C-0101 · B-8 / Cajonera 4), fecha límite 11-11-2026.', '2026-11-17 22:05:11.020014-03', '2026-11-15 22:05:11.657101-03', true, 5, 36);
INSERT INTO public.notificacion (id_notificacion, tipo, mensaje, fecha_generacion, fecha_lectura, leida, id_usuario, id_revision) VALUES (39, 'asignacion', 'Nueva revisión asignada: Equipo de corte hidráulico (8C-0305 · F-8 / Cajonera 2), fecha límite 28-08-2026.', '2026-11-17 22:05:11.032138-03', '2026-11-15 22:05:11.657101-03', true, 6, 39);
INSERT INTO public.notificacion (id_notificacion, tipo, mensaje, fecha_generacion, fecha_lectura, leida, id_usuario, id_revision) VALUES (40, 'asignacion', 'Nueva revisión asignada: Equipo de corte hidráulico (8C-0305 · F-8 / Cajonera 2), fecha límite 28-09-2026.', '2026-11-17 22:05:11.03896-03', '2026-11-15 22:05:11.657101-03', true, 6, 40);
INSERT INTO public.notificacion (id_notificacion, tipo, mensaje, fecha_generacion, fecha_lectura, leida, id_usuario, id_revision) VALUES (41, 'asignacion', 'Nueva revisión asignada: Equipo de corte hidráulico (8C-0305 · F-8 / Cajonera 2), fecha límite 28-10-2026.', '2026-11-17 22:05:11.042842-03', '2026-11-15 22:05:11.657101-03', true, 6, 41);
INSERT INTO public.notificacion (id_notificacion, tipo, mensaje, fecha_generacion, fecha_lectura, leida, id_usuario, id_revision) VALUES (42, 'asignacion', 'Nueva revisión asignada: Detector monogas H2S (8C-0458 · H-8 / Cajonera 3), fecha límite 27-08-2026.', '2026-11-17 22:05:11.048622-03', '2026-11-15 22:05:11.657101-03', true, 5, 42);
INSERT INTO public.notificacion (id_notificacion, tipo, mensaje, fecha_generacion, fecha_lectura, leida, id_usuario, id_revision) VALUES (43, 'asignacion', 'Nueva revisión asignada: Detector monogas H2S (8C-0458 · H-8 / Cajonera 3), fecha límite 27-09-2026.', '2026-11-17 22:05:11.052321-03', '2026-11-15 22:05:11.657101-03', true, 5, 43);
INSERT INTO public.notificacion (id_notificacion, tipo, mensaje, fecha_generacion, fecha_lectura, leida, id_usuario, id_revision) VALUES (44, 'asignacion', 'Nueva revisión asignada: Detector monogas H2S (8C-0458 · H-8 / Cajonera 3), fecha límite 27-10-2026.', '2026-11-17 22:05:11.055675-03', '2026-11-15 22:05:11.657101-03', true, 5, 44);
INSERT INTO public.notificacion (id_notificacion, tipo, mensaje, fecha_generacion, fecha_lectura, leida, id_usuario, id_revision) VALUES (45, 'asignacion', 'Nueva revisión asignada: Motobomba de achique (8C-0120 · BOD / Estante A), fecha límite 07-10-2026.', '2026-11-17 22:05:11.061328-03', '2026-11-15 22:05:11.657101-03', true, 6, 45);
INSERT INTO public.notificacion (id_notificacion, tipo, mensaje, fecha_generacion, fecha_lectura, leida, id_usuario, id_revision) VALUES (46, 'asignacion', 'Nueva revisión asignada: Motobomba de achique (8C-0120 · BOD / Estante A), fecha límite 07-10-2026.', '2026-11-17 22:05:11.062212-03', '2026-11-15 22:05:11.657101-03', true, 4, 45);
INSERT INTO public.notificacion (id_notificacion, tipo, mensaje, fecha_generacion, fecha_lectura, leida, id_usuario, id_revision) VALUES (47, 'asignacion', 'Nueva revisión asignada: Motobomba de achique (8C-0120 · BOD / Estante A), fecha límite 14-10-2026.', '2026-11-17 22:05:11.067804-03', '2026-11-15 22:05:11.657101-03', true, 6, 46);
INSERT INTO public.notificacion (id_notificacion, tipo, mensaje, fecha_generacion, fecha_lectura, leida, id_usuario, id_revision) VALUES (48, 'asignacion', 'Nueva revisión asignada: Motobomba de achique (8C-0120 · BOD / Estante A), fecha límite 14-10-2026.', '2026-11-17 22:05:11.06911-03', '2026-11-15 22:05:11.657101-03', true, 4, 46);
INSERT INTO public.notificacion (id_notificacion, tipo, mensaje, fecha_generacion, fecha_lectura, leida, id_usuario, id_revision) VALUES (49, 'asignacion', 'Nueva revisión asignada: Motobomba de achique (8C-0120 · BOD / Estante A), fecha límite 21-10-2026.', '2026-11-17 22:05:11.073293-03', '2026-11-15 22:05:11.657101-03', true, 6, 47);
INSERT INTO public.notificacion (id_notificacion, tipo, mensaje, fecha_generacion, fecha_lectura, leida, id_usuario, id_revision) VALUES (50, 'asignacion', 'Nueva revisión asignada: Motobomba de achique (8C-0120 · BOD / Estante A), fecha límite 21-10-2026.', '2026-11-17 22:05:11.074089-03', '2026-11-15 22:05:11.657101-03', true, 4, 47);
INSERT INTO public.notificacion (id_notificacion, tipo, mensaje, fecha_generacion, fecha_lectura, leida, id_usuario, id_revision) VALUES (51, 'asignacion', 'Nueva revisión asignada: Motobomba de achique (8C-0120 · BOD / Estante A), fecha límite 28-10-2026.', '2026-11-17 22:05:11.077715-03', '2026-11-15 22:05:11.657101-03', true, 6, 48);
INSERT INTO public.notificacion (id_notificacion, tipo, mensaje, fecha_generacion, fecha_lectura, leida, id_usuario, id_revision) VALUES (52, 'asignacion', 'Nueva revisión asignada: Motobomba de achique (8C-0120 · BOD / Estante A), fecha límite 28-10-2026.', '2026-11-17 22:05:11.078548-03', '2026-11-15 22:05:11.657101-03', true, 4, 48);
INSERT INTO public.notificacion (id_notificacion, tipo, mensaje, fecha_generacion, fecha_lectura, leida, id_usuario, id_revision) VALUES (53, 'asignacion', 'Nueva revisión asignada: Motobomba de achique (8C-0120 · BOD / Estante A), fecha límite 04-11-2026.', '2026-11-17 22:05:11.082606-03', '2026-11-15 22:05:11.657101-03', true, 6, 49);
INSERT INTO public.notificacion (id_notificacion, tipo, mensaje, fecha_generacion, fecha_lectura, leida, id_usuario, id_revision) VALUES (54, 'asignacion', 'Nueva revisión asignada: Motobomba de achique (8C-0120 · BOD / Estante A), fecha límite 04-11-2026.', '2026-11-17 22:05:11.083542-03', '2026-11-15 22:05:11.657101-03', true, 4, 49);
INSERT INTO public.notificacion (id_notificacion, tipo, mensaje, fecha_generacion, fecha_lectura, leida, id_usuario, id_revision) VALUES (55, 'asignacion', 'Nueva revisión asignada: Motobomba de achique (8C-0120 · BOD / Estante A), fecha límite 11-11-2026.', '2026-11-17 22:05:11.087103-03', '2026-11-15 22:05:11.657101-03', true, 6, 50);
INSERT INTO public.notificacion (id_notificacion, tipo, mensaje, fecha_generacion, fecha_lectura, leida, id_usuario, id_revision) VALUES (56, 'asignacion', 'Nueva revisión asignada: Motobomba de achique (8C-0120 · BOD / Estante A), fecha límite 11-11-2026.', '2026-11-17 22:05:11.088102-03', '2026-11-15 22:05:11.657101-03', true, 4, 50);
INSERT INTO public.notificacion (id_notificacion, tipo, mensaje, fecha_generacion, fecha_lectura, leida, id_usuario, id_revision) VALUES (61, 'asignacion', 'Nueva revisión asignada: Separador hidráulico (8C-0612 · F-8 / Cajonera 2), fecha límite 28-08-2026.', '2026-11-17 22:05:11.102968-03', '2026-11-15 22:05:11.657101-03', true, 6, 53);
INSERT INTO public.notificacion (id_notificacion, tipo, mensaje, fecha_generacion, fecha_lectura, leida, id_usuario, id_revision) VALUES (62, 'asignacion', 'Nueva revisión asignada: Separador hidráulico (8C-0612 · F-8 / Cajonera 2), fecha límite 28-09-2026.', '2026-11-17 22:05:11.106612-03', '2026-11-15 22:05:11.657101-03', true, 6, 54);
INSERT INTO public.notificacion (id_notificacion, tipo, mensaje, fecha_generacion, fecha_lectura, leida, id_usuario, id_revision) VALUES (63, 'asignacion', 'Nueva revisión asignada: Separador hidráulico (8C-0612 · F-8 / Cajonera 2), fecha límite 28-10-2026.', '2026-11-17 22:05:11.110104-03', '2026-11-15 22:05:11.657101-03', true, 6, 55);
INSERT INTO public.notificacion (id_notificacion, tipo, mensaje, fecha_generacion, fecha_lectura, leida, id_usuario, id_revision) VALUES (73, 'vencimiento', 'La revisión de Motobomba de achique (8C-0120 · BOD / Estante A) venció el 11-11-2026.', '2026-11-17 22:05:11.638545-03', '2026-11-15 22:05:11.657101-03', true, 6, 50);
INSERT INTO public.notificacion (id_notificacion, tipo, mensaje, fecha_generacion, fecha_lectura, leida, id_usuario, id_revision) VALUES (74, 'vencimiento', 'La revisión de Motobomba de achique (8C-0120 · BOD / Estante A) venció el 11-11-2026.', '2026-11-17 22:05:11.640034-03', '2026-11-15 22:05:11.657101-03', true, 4, 50);
INSERT INTO public.notificacion (id_notificacion, tipo, mensaje, fecha_generacion, fecha_lectura, leida, id_usuario, id_revision) VALUES (75, 'vencimiento', 'La revisión de Motobomba de achique (8C-0120 · BOD / Estante A) venció el 11-11-2026. Responsables: P. Lagos, J. Soto.', '2026-11-17 22:05:11.642519-03', '2026-11-15 22:05:11.657101-03', true, 3, 50);
INSERT INTO public.notificacion (id_notificacion, tipo, mensaje, fecha_generacion, fecha_lectura, leida, id_usuario, id_revision) VALUES (76, 'vencimiento', 'La revisión de Ventilador de presión positiva (8C-0101 · B-8 / Cajonera 4) venció el 04-11-2026.', '2026-11-17 22:05:11.64397-03', '2026-11-15 22:05:11.657101-03', true, 5, 35);
INSERT INTO public.notificacion (id_notificacion, tipo, mensaje, fecha_generacion, fecha_lectura, leida, id_usuario, id_revision) VALUES (77, 'vencimiento', 'La revisión de Ventilador de presión positiva (8C-0101 · B-8 / Cajonera 4) venció el 04-11-2026. Responsable: M. Rivas.', '2026-11-17 22:05:11.646649-03', '2026-11-15 22:05:11.657101-03', true, 3, 35);
INSERT INTO public.notificacion (id_notificacion, tipo, mensaje, fecha_generacion, fecha_lectura, leida, id_usuario, id_revision) VALUES (78, 'vencimiento', 'La revisión de Motosierra de rescate (8C-0233 · B-8 / Cajonera 2) venció el 07-10-2026.', '2026-11-17 22:05:11.648155-03', '2026-11-15 22:05:11.657101-03', true, 4, 16);
INSERT INTO public.notificacion (id_notificacion, tipo, mensaje, fecha_generacion, fecha_lectura, leida, id_usuario, id_revision) VALUES (79, 'vencimiento', 'La revisión de Motosierra de rescate (8C-0233 · B-8 / Cajonera 2) venció el 07-10-2026. Responsable: J. Soto.', '2026-11-17 22:05:11.651197-03', '2026-11-15 22:05:11.657101-03', true, 3, 16);
INSERT INTO public.notificacion (id_notificacion, tipo, mensaje, fecha_generacion, fecha_lectura, leida, id_usuario, id_revision) VALUES (80, 'vencimiento', 'La revisión de Motosierra de rescate (8C-0233 · B-8 / Cajonera 2) venció el 30-09-2026.', '2026-11-17 22:05:11.653316-03', '2026-11-15 22:05:11.657101-03', true, 4, 15);
INSERT INTO public.notificacion (id_notificacion, tipo, mensaje, fecha_generacion, fecha_lectura, leida, id_usuario, id_revision) VALUES (81, 'vencimiento', 'La revisión de Motosierra de rescate (8C-0233 · B-8 / Cajonera 2) venció el 30-09-2026. Responsable: J. Soto.', '2026-11-17 22:05:11.656025-03', '2026-11-15 22:05:11.657101-03', true, 3, 15);


ALTER TABLE public.notificacion ENABLE TRIGGER ALL;

--
-- Data for Name: permiso; Type: TABLE DATA; Schema: public; Owner: -
--

ALTER TABLE public.permiso DISABLE TRIGGER ALL;

INSERT INTO public.permiso (id_permiso, codigo, nombre, modulo) VALUES (1, 'usuario.administrar', 'Administrar usuarios y asignar roles', 'accesos');
INSERT INTO public.permiso (id_permiso, codigo, nombre, modulo) VALUES (2, 'permiso.administrar', 'Administrar permisos por rol', 'accesos');
INSERT INTO public.permiso (id_permiso, codigo, nombre, modulo) VALUES (3, 'auditoria.consultar', 'Consultar bitácora de auditoría', 'accesos');
INSERT INTO public.permiso (id_permiso, codigo, nombre, modulo) VALUES (4, 'material.consultar', 'Buscar material y consultar su historial', 'inventario');
INSERT INTO public.permiso (id_permiso, codigo, nombre, modulo) VALUES (5, 'material.registrar', 'Registrar material y cargar planillas', 'inventario');
INSERT INTO public.permiso (id_permiso, codigo, nombre, modulo) VALUES (6, 'material.modificar', 'Modificar ficha de material', 'inventario');
INSERT INTO public.permiso (id_permiso, codigo, nombre, modulo) VALUES (7, 'material.dar_de_baja', 'Dar de baja material', 'inventario');
INSERT INTO public.permiso (id_permiso, codigo, nombre, modulo) VALUES (8, 'movimiento.registrar', 'Registrar movimiento de material', 'inventario');
INSERT INTO public.permiso (id_permiso, codigo, nombre, modulo) VALUES (9, 'catalogo.administrar', 'Administrar unidades, cajoneras y categorías', 'inventario');
INSERT INTO public.permiso (id_permiso, codigo, nombre, modulo) VALUES (10, 'revision.ejecutar', 'Ejecutar sus revisiones asignadas', 'revisiones');
INSERT INTO public.permiso (id_permiso, codigo, nombre, modulo) VALUES (11, 'revision.supervisar', 'Consultar y reasignar todas las revisiones', 'revisiones');
INSERT INTO public.permiso (id_permiso, codigo, nombre, modulo) VALUES (12, 'plan.administrar', 'Definir planes y puntos de control', 'revisiones');
INSERT INTO public.permiso (id_permiso, codigo, nombre, modulo) VALUES (13, 'asignacion.administrar', 'Asignar planes a material', 'revisiones');
INSERT INTO public.permiso (id_permiso, codigo, nombre, modulo) VALUES (14, 'fotografia.anular', 'Anular fotografías de evidencia', 'revisiones');
INSERT INTO public.permiso (id_permiso, codigo, nombre, modulo) VALUES (15, 'hallazgo.gestionar', 'Dar seguimiento y cerrar hallazgos', 'revisiones');
INSERT INTO public.permiso (id_permiso, codigo, nombre, modulo) VALUES (16, 'panel.consultar', 'Consultar panel de cumplimiento', 'revisiones');
INSERT INTO public.permiso (id_permiso, codigo, nombre, modulo) VALUES (17, 'reporte.exportar', 'Exportar reportes de cumplimiento', 'revisiones');
INSERT INTO public.permiso (id_permiso, codigo, nombre, modulo) VALUES (18, 'respaldo.administrar', 'Generar, descargar y restaurar respaldos', 'accesos');


ALTER TABLE public.permiso ENABLE TRIGGER ALL;

--
-- Data for Name: revision_responsable; Type: TABLE DATA; Schema: public; Owner: -
--

ALTER TABLE public.revision_responsable DISABLE TRIGGER ALL;

INSERT INTO public.revision_responsable (id_revision, id_usuario) VALUES (1, 4);
INSERT INTO public.revision_responsable (id_revision, id_usuario) VALUES (2, 4);
INSERT INTO public.revision_responsable (id_revision, id_usuario) VALUES (3, 4);
INSERT INTO public.revision_responsable (id_revision, id_usuario) VALUES (4, 4);
INSERT INTO public.revision_responsable (id_revision, id_usuario) VALUES (5, 4);
INSERT INTO public.revision_responsable (id_revision, id_usuario) VALUES (6, 4);
INSERT INTO public.revision_responsable (id_revision, id_usuario) VALUES (7, 4);
INSERT INTO public.revision_responsable (id_revision, id_usuario) VALUES (8, 4);
INSERT INTO public.revision_responsable (id_revision, id_usuario) VALUES (9, 4);
INSERT INTO public.revision_responsable (id_revision, id_usuario) VALUES (10, 4);
INSERT INTO public.revision_responsable (id_revision, id_usuario) VALUES (11, 4);
INSERT INTO public.revision_responsable (id_revision, id_usuario) VALUES (12, 4);
INSERT INTO public.revision_responsable (id_revision, id_usuario) VALUES (13, 4);
INSERT INTO public.revision_responsable (id_revision, id_usuario) VALUES (14, 4);
INSERT INTO public.revision_responsable (id_revision, id_usuario) VALUES (15, 4);
INSERT INTO public.revision_responsable (id_revision, id_usuario) VALUES (16, 4);
INSERT INTO public.revision_responsable (id_revision, id_usuario) VALUES (17, 4);
INSERT INTO public.revision_responsable (id_revision, id_usuario) VALUES (18, 4);
INSERT INTO public.revision_responsable (id_revision, id_usuario) VALUES (19, 4);
INSERT INTO public.revision_responsable (id_revision, id_usuario) VALUES (20, 4);
INSERT INTO public.revision_responsable (id_revision, id_usuario) VALUES (21, 4);
INSERT INTO public.revision_responsable (id_revision, id_usuario) VALUES (22, 4);
INSERT INTO public.revision_responsable (id_revision, id_usuario) VALUES (23, 4);
INSERT INTO public.revision_responsable (id_revision, id_usuario) VALUES (24, 4);
INSERT INTO public.revision_responsable (id_revision, id_usuario) VALUES (25, 4);
INSERT INTO public.revision_responsable (id_revision, id_usuario) VALUES (26, 4);
INSERT INTO public.revision_responsable (id_revision, id_usuario) VALUES (27, 4);
INSERT INTO public.revision_responsable (id_revision, id_usuario) VALUES (28, 4);
INSERT INTO public.revision_responsable (id_revision, id_usuario) VALUES (29, 5);
INSERT INTO public.revision_responsable (id_revision, id_usuario) VALUES (30, 5);
INSERT INTO public.revision_responsable (id_revision, id_usuario) VALUES (31, 5);
INSERT INTO public.revision_responsable (id_revision, id_usuario) VALUES (32, 5);
INSERT INTO public.revision_responsable (id_revision, id_usuario) VALUES (33, 5);
INSERT INTO public.revision_responsable (id_revision, id_usuario) VALUES (34, 5);
INSERT INTO public.revision_responsable (id_revision, id_usuario) VALUES (35, 5);
INSERT INTO public.revision_responsable (id_revision, id_usuario) VALUES (36, 5);
INSERT INTO public.revision_responsable (id_revision, id_usuario) VALUES (37, 5);
INSERT INTO public.revision_responsable (id_revision, id_usuario) VALUES (38, 5);
INSERT INTO public.revision_responsable (id_revision, id_usuario) VALUES (39, 6);
INSERT INTO public.revision_responsable (id_revision, id_usuario) VALUES (40, 6);
INSERT INTO public.revision_responsable (id_revision, id_usuario) VALUES (41, 6);
INSERT INTO public.revision_responsable (id_revision, id_usuario) VALUES (42, 5);
INSERT INTO public.revision_responsable (id_revision, id_usuario) VALUES (43, 5);
INSERT INTO public.revision_responsable (id_revision, id_usuario) VALUES (44, 5);
INSERT INTO public.revision_responsable (id_revision, id_usuario) VALUES (45, 4);
INSERT INTO public.revision_responsable (id_revision, id_usuario) VALUES (45, 6);
INSERT INTO public.revision_responsable (id_revision, id_usuario) VALUES (46, 4);
INSERT INTO public.revision_responsable (id_revision, id_usuario) VALUES (46, 6);
INSERT INTO public.revision_responsable (id_revision, id_usuario) VALUES (47, 4);
INSERT INTO public.revision_responsable (id_revision, id_usuario) VALUES (47, 6);
INSERT INTO public.revision_responsable (id_revision, id_usuario) VALUES (48, 4);
INSERT INTO public.revision_responsable (id_revision, id_usuario) VALUES (48, 6);
INSERT INTO public.revision_responsable (id_revision, id_usuario) VALUES (49, 4);
INSERT INTO public.revision_responsable (id_revision, id_usuario) VALUES (49, 6);
INSERT INTO public.revision_responsable (id_revision, id_usuario) VALUES (50, 4);
INSERT INTO public.revision_responsable (id_revision, id_usuario) VALUES (50, 6);
INSERT INTO public.revision_responsable (id_revision, id_usuario) VALUES (51, 4);
INSERT INTO public.revision_responsable (id_revision, id_usuario) VALUES (51, 6);
INSERT INTO public.revision_responsable (id_revision, id_usuario) VALUES (52, 4);
INSERT INTO public.revision_responsable (id_revision, id_usuario) VALUES (52, 6);
INSERT INTO public.revision_responsable (id_revision, id_usuario) VALUES (53, 6);
INSERT INTO public.revision_responsable (id_revision, id_usuario) VALUES (54, 6);
INSERT INTO public.revision_responsable (id_revision, id_usuario) VALUES (55, 6);


ALTER TABLE public.revision_responsable ENABLE TRIGGER ALL;

--
-- Data for Name: rol_permiso; Type: TABLE DATA; Schema: public; Owner: -
--

ALTER TABLE public.rol_permiso DISABLE TRIGGER ALL;

INSERT INTO public.rol_permiso (id_permiso, id_rol) VALUES (4, 1);
INSERT INTO public.rol_permiso (id_permiso, id_rol) VALUES (8, 1);
INSERT INTO public.rol_permiso (id_permiso, id_rol) VALUES (10, 1);
INSERT INTO public.rol_permiso (id_permiso, id_rol) VALUES (4, 2);
INSERT INTO public.rol_permiso (id_permiso, id_rol) VALUES (8, 2);
INSERT INTO public.rol_permiso (id_permiso, id_rol) VALUES (10, 2);
INSERT INTO public.rol_permiso (id_permiso, id_rol) VALUES (5, 2);
INSERT INTO public.rol_permiso (id_permiso, id_rol) VALUES (6, 2);
INSERT INTO public.rol_permiso (id_permiso, id_rol) VALUES (7, 2);
INSERT INTO public.rol_permiso (id_permiso, id_rol) VALUES (11, 2);
INSERT INTO public.rol_permiso (id_permiso, id_rol) VALUES (12, 2);
INSERT INTO public.rol_permiso (id_permiso, id_rol) VALUES (13, 2);
INSERT INTO public.rol_permiso (id_permiso, id_rol) VALUES (14, 2);
INSERT INTO public.rol_permiso (id_permiso, id_rol) VALUES (15, 2);
INSERT INTO public.rol_permiso (id_permiso, id_rol) VALUES (16, 2);
INSERT INTO public.rol_permiso (id_permiso, id_rol) VALUES (17, 2);
INSERT INTO public.rol_permiso (id_permiso, id_rol) VALUES (4, 3);
INSERT INTO public.rol_permiso (id_permiso, id_rol) VALUES (8, 3);
INSERT INTO public.rol_permiso (id_permiso, id_rol) VALUES (10, 3);
INSERT INTO public.rol_permiso (id_permiso, id_rol) VALUES (1, 3);
INSERT INTO public.rol_permiso (id_permiso, id_rol) VALUES (2, 3);
INSERT INTO public.rol_permiso (id_permiso, id_rol) VALUES (3, 3);
INSERT INTO public.rol_permiso (id_permiso, id_rol) VALUES (9, 3);
INSERT INTO public.rol_permiso (id_permiso, id_rol) VALUES (18, 3);


ALTER TABLE public.rol_permiso ENABLE TRIGGER ALL;

--
-- Name: asignacion_plan_id_asignacion_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.asignacion_plan_id_asignacion_seq', 9, true);


--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.auth_group_id_seq', 1, false);


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.auth_group_permissions_id_seq', 1, false);


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.auth_permission_id_seq', 120, true);


--
-- Name: baja_id_baja_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.baja_id_baja_seq', 1, false);


--
-- Name: cajonera_id_cajonera_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.cajonera_id_cajonera_seq', 14, true);


--
-- Name: categoria_id_categoria_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.categoria_id_categoria_seq', 7, true);


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.django_content_type_id_seq', 30, true);


--
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.django_migrations_id_seq', 37, true);


--
-- Name: evento_auditoria_id_evento_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.evento_auditoria_id_evento_seq', 74, true);


--
-- Name: hallazgo_id_hallazgo_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.hallazgo_id_hallazgo_seq', 3, true);


--
-- Name: material_id_material_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.material_id_material_seq', 15, true);


--
-- Name: movimiento_id_movimiento_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.movimiento_id_movimiento_seq', 15, true);


--
-- Name: notificacion_id_notificacion_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.notificacion_id_notificacion_seq', 81, true);


--
-- Name: permiso_id_permiso_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.permiso_id_permiso_seq', 18, true);


--
-- Name: plan_revision_id_plan_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.plan_revision_id_plan_seq', 5, true);


--
-- Name: punto_control_id_punto_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.punto_control_id_punto_seq', 22, true);


--
-- Name: revision_id_revision_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.revision_id_revision_seq', 55, true);


--
-- Name: rol_id_rol_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.rol_id_rol_seq', 3, true);


--
-- Name: unidad_id_unidad_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.unidad_id_unidad_seq', 4, true);


--
-- Name: usuario_id_usuario_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.usuario_id_usuario_seq', 6, true);


--
-- PostgreSQL database dump complete
--

\unrestrict pyj6LKREbJh5DTFN72xx0ZxM1tHBQmTXuGKHandBNTd6nnWEz3HhqX6OhUY3TyN


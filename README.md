# Django Data Monitor (SSR + Auth + Railway)

Backend en **Django** que implementa un **Dashboard con Server Side Rendering (SSR)**, control de acceso mediante **autenticación y autorización** (permisos), panel de **Django Admin** para gestión de usuarios/permisos, consumo de una **API externa** y despliegue en **Railway** con soporte para **MySQL**, **WhiteNoise** y **Gunicorn**.

---

## Objetivo del proyecto

Desarrollar una aplicación backend robusta y escalable utilizando Django que integre:

- Interfaz de administración (Django Admin) para gestión eficiente de datos y usuarios.
- Renderizado del lado del servidor (SSR) para mejorar la carga inicial y UX.
- Autenticación y autorización para controlar el acceso a las vistas.
- Despliegue en Railway con base de datos MySQL y archivos estáticos servidos en producción.

---

## Funcionalidades implementadas

### 1) Dashboard con Server Side Rendering (SSR)
- Estructura de plantillas con herencia:
  - `templates/dashboard/base.html` define el layout base y el bloque `{% block content %}`.
  - `templates/dashboard/index.html` extiende `base.html` e incluye fragmentos.
- Fragmentos de plantilla:
  - `templates/dashboard/partials/header.html`
  - `templates/dashboard/content/data.html`
- Soporte para archivos estáticos (CSS/JS/IMG) usando `{% load static %}`.

### 2) Consumo de API externa
- Configuración de `API_URL` en variables de entorno (con fallback por defecto).
- Consumo desde servidor (SSR) usando `requests` para obtener datos.
- Renderización de indicadores en la UI mediante variables en el contexto.

### 3) Autenticación (Login/Logout)
- Acceso restringido al dashboard con `@login_required`.
- Vistas predefinidas:
  - `LoginView` en `/login/` usando `templates/security/login.html`
  - `LogoutView` en `/logout/`
- Configuración:
  - `LOGIN_URL`, `LOGIN_REDIRECT_URL`, `LOGOUT_REDIRECT_URL`
- Formulario con `POST` + `CSRF token`.

### 4) Autorización (Permisos)
- Control de acceso por permisos con:
  - `@permission_required('dashboard.index_viewer', raise_exception=True)`
- Permiso personalizado en `dashboard/models.py`:
  - `index_viewer` (Can show to index view)
- Flujo esperado:
  - `usuario01` con permiso puede acceder al dashboard.
  - `usuario02` sin permiso recibe **403**.

### 5) Manejo de error 403 personalizado
- Plantilla dedicada: `templates/403.html`
- Vista personalizada para 403: `custom_permission_denied`

### 6) Deploy en Railway (Producción)
- `Gunicorn` como servidor WSGI.
- `WhiteNoise` para servir archivos estáticos en producción.
- Base de datos MySQL en Railway usando `PyMySQL` y variables de entorno.
- Archivos clave:
  - `Procfile`
  - `runtime.txt` 
  - `requirements.txt`

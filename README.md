# Supplier & Parts MVC Flask Project (Dockerized)

## Overview
Proyecto simple en **Flask (MVC)** que implementa ABM (CRUD) para **Proveedores** y **Piezas**, y la asociación entre ellos (qué piezas suministra cada proveedor). La asociación contiene `precio`, `cantidad`, `color` y `categoria` para la relación proveedor-pieza.

## Estructura
- `app/` - paquete principal (models, controllers/views, templates)
- `run.py` - arranque de la aplicación
- `Dockerfile` & `docker-compose.yml` - para levantar con Docker
- `requirements.txt` - dependencias

## Correr con Docker (recomendado)
1. Construir y levantar:
   ```bash
   docker-compose up --build
   ```
2. Abrir en el navegador: `http://localhost:5000`

## Correr localmente sin Docker
1. Crear y activar un virtualenv con Python 3.11+
2. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Inicializar la base de datos (SQLite usado por defecto):
   ```bash
   export FLASK_APP=run.py
   flask run
   ```
   La aplicación crea la base de datos automáticamente al primer acceso.
4. Abrir `http://127.0.0.1:5000`

## Endpoints importantes (UI)
- `/providers` - listado de proveedores
- `/providers/new` - crear proveedor
- `/providers/<id>/edit` - editar proveedor
- `/providers/<id>/delete` - borrar proveedor
- `/pieces` - listado de piezas
- `/pieces/new` - crear pieza
- `/pieces/<id>/edit` - editar pieza
- `/pieces/<id>/delete` - borrar pieza
- Desde la vista de proveedor puede asociar piezas y ver la cantidad/precio/color/categoría provistos por ese proveedor.

## Notas
- Proyecto minimal, pensado como punto de partida. Está preparado para SQLite en desarrollo; puede cambiarse a PostgreSQL fácilmente modificando `SQLALCHEMY_DATABASE_URI` en `app/__init__.py`.\n
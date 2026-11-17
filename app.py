"""Punto de entrada. Aquí se ensamblan las capas.  Ejecutar con: streamlit run app.py"""
from probabilidad.aplicacion.servicios import ServicioProbabilidad
from probabilidad.infraestructura.generador import GeneradorSintetico
from probabilidad.infraestructura.lector_csv import LectorCSVPandas
from probabilidad.infraestructura.lector_texto import LectorTextoPlano
from probabilidad.presentacion import interfaz

servicio = ServicioProbabilidad(LectorTextoPlano(), LectorCSVPandas(), GeneradorSintetico())
interfaz.mostrar(servicio)

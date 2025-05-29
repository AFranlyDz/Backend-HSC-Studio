import pandas as pd
import numpy as np
import math

from apps.exportar_csv.services.make_dataframe import make_dataframe
from apps.codificadores.models import Codificadores
from apps.hc.models.rasgos_clinicos_globales import Rasgos_Clinicos_Globales


def make_knowledge_base(campos_seleccionados, tipo=1):
    base_datos_plana = make_dataframe(campos_seleccionados, tipo=2)

    base_conocimiento = base_datos_plana.drop_duplicates(
        subset="id_historia", keep="first"
    )
    if tipo == 1:
        # crear columnas para grupos de variables continuas
        columnas_agrupar = [
            "edad",
            "volumen_tada",
            "diametro_capa",
            "desviacion_linea_media",
            "diametro_mayor_transverso",
        ]
        lista_intervalos = [
            [(0, 60), (61, 70), (71, 80), (81, 90), (91, 120)],
            [(0, 50), (51, 100), (101, 150), (150, 400)],
            [(0, 0.99), (1, 1.99), (2, 5)],
            [(0, 4.99), (5, 9.99), (10, 15), (15.1, 30)],
            [(0, 9.99), (10, 20), (21, 30), (30, 60)],
        ]

        def agrupar_variables_continuas(nombre_col, lista_intervalos):
            posicion_original = base_conocimiento.columns.get_loc(nombre_col)
            for i, (inicio, fin) in enumerate(lista_intervalos, 1):
                nueva_columna = (
                    nombre_col + " " + str(round(inicio)) + "-" + str(round(fin))
                )
                base_conocimiento.loc[:, nueva_columna] = base_conocimiento[
                    nombre_col
                ].between(inicio, fin)
                columna = base_conocimiento.pop(nueva_columna)
                base_conocimiento.insert(posicion_original + i, nueva_columna, columna)

        for i in range(len(columnas_agrupar)):
            agrupar_variables_continuas(
                columnas_agrupar[i],
                lista_intervalos[i],
            )

        # crear columnas segun las escalas
        def descomponer_escalas(base_conocimiento, nombre_escala, rango_escala):
            valores_escala = range(rango_escala[0], rango_escala[1])
            for i in valores_escala:
                nueva_columna = nombre_escala + "-" + str(i)
                base_conocimiento.loc[:, nueva_columna] = (
                    base_conocimiento[nombre_escala] == i
                )
            base_conocimiento = base_conocimiento.drop(nombre_escala, axis=1)
            return base_conocimiento

        nombres_escalas = [
            "escala_glasgow_ingreso",
            "escala_mcwalder",
            "escala_gordon_firing",
            "escala_nomura",
            "escala_nakagushi",
            "escala_evaluacion_resultados_glasgow",
        ]
        rangos_escalas = [(3, 16), (0, 5), (1, 5), (1, 6), (1, 5), (1, 6)]

        for i in range(len(nombres_escalas)):
            print("valor en iteracion", i)
            base_conocimiento = descomponer_escalas(
                base_conocimiento, nombres_escalas[i], rangos_escalas[i]
            )

    # crear columnas para los rasgos clinicos, del episodio y operatorios
    lista_clasificacion_codifcadores = list(
        Codificadores.objects.values_list("clasificacion", flat=True).distinct()
    )

    def hacer_lista_codificadores(codif):
        lista_codificadores = []
        for j in base_conocimiento["id_historia"].unique():
            if any(
                (base_datos_plana["id_historia"] == j)
                & (base_datos_plana["nombre_codificadores_globales"] == codif.nombre)
            ):
                lista_codificadores.append(True)
            else:
                lista_codificadores.append(False)
        return lista_codificadores

    for clasificacion in lista_clasificacion_codifcadores:

        codificadores = Codificadores.objects.filter(clasificacion=clasificacion)

        for i, codificador in enumerate(codificadores):
            base_conocimiento[
                codificador.clasificacion + "-" + str(i + 1) + " " + codificador.nombre
            ] = hacer_lista_codificadores(codificador)
    # fin de creacion de columnas de codificadores

    # eliminar columnas redundantes
    base_conocimiento = base_conocimiento.drop(
        columns=[
            "nombre_codificadores_globales",
            "nombre_codificador_episodio",
            "nombre_codificador_operatorio",
        ]
    )

    return base_conocimiento

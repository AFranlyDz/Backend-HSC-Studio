import pandas as pd
import numpy as np
from IPython.display import display
from django.core.management.base import BaseCommand


def import_csv():
    help = "Este comando permite agregar las entradas de un csv a la base de datos"

    pd.set_option("display.max_rows", None)
    pd.set_option("display.max_columns", None)

    hsc_kb = pd.read_csv(r"management/commands/hematoma.csv", delimiter=";")

    columnas_eliminar = [
        " ",
        " ≤ 60",
        " 60 - 70",
        " 71 - 80",
        " 81 - 90",
        " >90",
        " ≤ 50",
        " 51 - 100",
        " 100 - 150",
        " > 150",
        " < 1",
        " 1 - 2",
        " >  2",
        " < 5",
        " 5 - 10",
        " 11 - 15",
        " > 15",
        " < 10",
        " 10 - 20",
        " 21 -30",
        " >  30",
    ]

    for e in columnas_eliminar:
        hsc_kb = hsc_kb.drop(e, axis=1)

    # para transformar la escala de glasgow al ingreso
    columnas_glasgow_ingreso = [
        " ESCALA DE GLASGOW AL INGRESO 3",
        " ESCALA DE GLASGOW AL INGRESO4",
        " ESCALA DE GLASGOW AL INGRESO5",
        " ESCALA DE GLASGOW AL INGRESO6",
        " ESCALA DE GLASGOW AL INGRESO7",
        " ESCALA DE GLASGOW AL INGRESO8",
        " ESCALA DE GLASGOW AL INGRESO9",
        " ESCALA DE GLASGOW AL INGRESO 10",
        " ESCALA DE GLASGOW AL INGRESO 11",
        " ESCALA DE GLASGOW AL INGRESO 12",
        " ESCALA DE GLASGOW AL INGRESO 13",
        " ESCALA DE GLASGOW AL INGRESO 14",
        " ESCALA DE GLASGOW AL INGRESO 15",
    ]
    columnas_bender = [
        " ESCALA DE BENDER 1",
        " ESCALA DE BENDER 2",
        " ESCALA DE BENDER 3",
        " ESCALA DE BENDER 4",
    ]
    columnas_mcwalder = [
        " ESCALA DE MCKWALDER 0",
        " ESCALA DE MCKWALDER 1",
        " ESCALA DE MCKWALDER 2",
        " ESCALA DE MCKWALDER 3",
        " ESCALA DE MCKWALDER 4",
    ]
    columnas_gordon_firing = [
        " ESCALA GORDON FAIRING 1",
        " ESCALA GORDON FAIRING 2",
        " ESCALA GORDON FAIRING 3",
        " ESCALA GORDON FAIRING 4",
    ]
    columnas_nomura = [
        " ESCALA DE NOMURA 1 Hiperdensidad:",
        " ESCALA DE NOMURA 2  Isodensidad",
        " ESCALA DE NOMURA 3  Hipodensidad:",
        " ESCALA DE NOMURA 4  Densidad mixta",
        " ESCALA DE NOMURA 5 Tipo capa o estrato",
    ]
    columnas_nakagushi = [
        " ESCALA DE NAKAGUCHI 1  Densidad homogénea",
        " ESCALA DE NAKAGUCHI 2  Tipo laminar",
        " ESCALA DE NAKAGUCHI 3  Tipo separado o en capa",
        " ESCALA DE NAKAGUCHI 4  Densidad trabeculado",
    ]
    columnas_resultado_glasgow = [
        " ESCALA DE EVALUACIÓN DE RESULTADOS DE GLASGOW 1",
        " ESCALA DE EVALUACIÓN DE RESULTADOS DE GLASGOW 2",
        " ESCALA DE EVALUACIÓN DE RESULTADOS DE GLASGOW 3",
        " ESCALA DE EVALUACIÓN DE RESULTADOS DE GLASGOW 4",
        " ESCALA DE EVALUACIÓN DE RESULTADOS DE GLASGOW 5",
    ]

    lista_grupos_columnas = [
        [columnas_glasgow_ingreso, "escala_glasgow_ingreso", 3],
        [columnas_bender, "escala_bender", 1],
        [columnas_mcwalder, "escala_mcwalder", 0],
        [columnas_gordon_firing, "escala_gordon_firing", 1],
        [columnas_nomura, "escala_nomura", 1],
        [columnas_nakagushi, "escala_nakagushi", 1],
        [columnas_resultado_glasgow, "escala_resultados_glasgow", 1],
    ]

    def determinar_ocurrencia_str(string, valor):
        if type(string) == str:
            if string.find(valor) != -1:
                return True
            else:
                return False
        else:
            return False

    def agrupar_columnas_en_una_sola(
        df, lista_columnas_agrupar, nombre_columna_agrupada, valor_inicial_contador=1
    ):
        campos_columna_agrupada = []
        for index, fila in df[lista_columnas_agrupar].iterrows():
            contador = valor_inicial_contador
            for columnas in lista_columnas_agrupar:
                if fila[columnas] == 1 or determinar_ocurrencia_str(
                    fila[columnas], "1"
                ):
                    campos_columna_agrupada.append(contador)
                    break
                contador += 1

            if contador == len(lista_columnas_agrupar) + valor_inicial_contador:
                campos_columna_agrupada.append(np.nan)

        df[nombre_columna_agrupada] = campos_columna_agrupada
        df = df.drop(lista_columnas_agrupar, axis=1)
        return df

    for grupo_columnas in lista_grupos_columnas:
        hsc_kb = agrupar_columnas_en_una_sola(
            hsc_kb,
            grupo_columnas[0],
            grupo_columnas[1],
            valor_inicial_contador=grupo_columnas[2],
        )

    # convertir strings vacias y solo con espacios en blanco a Nan
    # Reemplazar espacios en blanco por NaN
    hsc_kb.replace("None", np.nan, inplace=True)
    hsc_kb.replace("", np.nan, inplace=True)
    hsc_kb.replace(r"^\s*$", np.nan, regex=True, inplace=True)

    # remplazar los valores que sean string a numero, aunque tengan espacios en blanco de sobra y cambiar comas por puntos para los valores de punto flotante
    hsc_kb = hsc_kb.apply(
        lambda col: pd.to_numeric(
            col.astype(str).str.replace(",", ".").str.strip(), errors="coerce"
        )
    )

    # ahora vamos a llenar los campos Nan
    # codigo para variables categoricas
    # Antes de llamar a la función, revisa las columnas categóricas
    def corregir_faltantes_categoricos(df, lista_columnas):
        for columna in lista_columnas:
            distribucion_categorica = df[columna].value_counts(normalize=True)
            valores_aleatorios = np.random.choice(
                distribucion_categorica.index,
                size=hsc_kb[columna].isnull().sum(),
                p=distribucion_categorica.values,
            )
            df.loc[df[columna].isnull(), columna] = valores_aleatorios
        return df

    # codigo para variables continuas
    def corregir_faltantes_continuos(df, lista_columnas):
        for columna in lista_columnas:
            media = df[columna].mean()
            desviacion_estandar = df[columna].std()
            cant_nan = df[columna].isna().sum()

            valores_aleatorios = np.random.normal(
                loc=media, scale=desviacion_estandar, size=cant_nan
            )
            valores_aleatorios = np.round(valores_aleatorios).clip(0)

            df.loc[df[columna].isna(), columna] = valores_aleatorios
        return df

    lista_columnas_continuas = [
        " EDAD",
        " VOLUMEN DEL HEMATOMA",
        " DIÁMETRO DE LA CAPA",
        " DESVIACIÓN DE LÍNEA MEDIA",
        " DIÁMETRO MAYOR TRANSVERSO",
    ]
    lista_columnas_categoricas = hsc_kb.columns.difference(
        lista_columnas_continuas
        + ["NOMBRE                                ", " HISTORIA CLÍNICA"]
    )
    hsc_kb = corregir_faltantes_categoricos(hsc_kb, lista_columnas_categoricas)
    hsc_kb = corregir_faltantes_continuos(hsc_kb, lista_columnas_continuas)

    display(hsc_kb.columns)
    return hsc_kb


import_csv()

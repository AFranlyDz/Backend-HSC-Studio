import pandas as pd

from apps.hc.models.historia_clinica import historia_clinica
from apps.episodio.models.episodio import Episodio
from apps.codificadores.models import Codificadores
from apps.hc.models.rasgos_clinicos_globales import Rasgos_Clinicos_Globales
from apps.episodio.models.rasgos_clinicos_episodio import Rasgos_Clinicos_Episodio
from apps.registro_operatorio.models.Registro_Operatorio import Registro_Operatorio
from apps.registro_operatorio.models.Rasgos_Clinicos_Operatorios import (
    Rasgos_Clinicos_Operatorios,
)
from apps.registro_operatorio.models.Registro_Posoperatorio import (
    Registro_Posoperatorio,
)
from apps.hematoma.models import hematoma_subdural


def make_dataframe(campos_seleccionados):
    pd.set_option("display.max_rows", None)
    pd.set_option("display.max_columns", None)

    # establecer lista de valores para cada modelo segun campos seleccionados
    campos_historia = ["id"]
    campos_episodio = ["id", "historia_clinica_id"]
    campos_codificador = ["id"]
    campos_rasgo_clinico_global = ["id", "codificador_id", "historia_clinica_id"]
    campos_rasgo_clinico_episodio = ["id", "codificador_id", "episodio_id"]
    campos_registro_operatorio = ["id", "episodio_id"]
    campos_rasgo_clinico_operatorio = ["id", "registro_operatorio_id", "codificador_id"]
    campos_registro_posoperatorio = ["id", "registro_operatorio_id"]
    campos_hematoma = ["id", "episodio_id"]

    for campo in campos_seleccionados:
        if campo.split(".")[0] == "historia_clinica":
            campos_historia.append(campo.split(".")[1])
        elif campo.split(".")[0] == "episodio":
            campos_episodio.append(campo.split(".")[1])
        elif campo.split(".")[0] == "codificador":
            campos_codificador.append(campo.split(".")[1])
        elif campo.split(".")[0] == "rasgo_clinico_global":
            campos_rasgo_clinico_global.append(campo.split(".")[1])
        elif campo.split(".")[0] == "rasgo_clinico_episodio":
            campos_rasgo_clinico_episodio.append(campo.split(".")[1])
        elif campo.split(".")[0] == "registro_operatorio":
            campos_registro_operatorio.append(campo.split(".")[1])
        elif campo.split(".")[0] == "rasgo_clinico_operatorio":
            campos_rasgo_clinico_operatorio.append(campo.split(".")[1])
        elif campo.split(".")[0] == "registro_posoperatorio":
            campos_registro_posoperatorio.append(campo.split(".")[1])
        elif campo.split(".")[0] == "hematoma":
            campos_hematoma.append(campo.split(".")[1])

    # Tomar los modelos de la bd en dataframes
    historia_df = pd.DataFrame(
        list(historia_clinica.objects.all().values(*campos_historia))
    )
    episodio_df = pd.DataFrame(list(Episodio.objects.all().values(*campos_episodio)))
    codificador_df = pd.DataFrame(
        list(Codificadores.objects.all().values(*campos_codificador))
    )
    rasgo_clinico_global_df = pd.DataFrame(
        list(
            Rasgos_Clinicos_Globales.objects.all().values(*campos_rasgo_clinico_global)
        )
    )
    rasgo_clinico_episodio_df = pd.DataFrame(
        list(
            Rasgos_Clinicos_Episodio.objects.all().values(
                *campos_rasgo_clinico_episodio
            )
        )
    )
    registro_operatorio_df = pd.DataFrame(
        list(Registro_Operatorio.objects.all().values(*campos_registro_operatorio))
    )
    rasgo_clinico_operatorio_df = pd.DataFrame(
        list(
            Rasgos_Clinicos_Operatorios.objects.all().values(
                *campos_rasgo_clinico_operatorio
            )
        )
    )
    registro_posoperatorio_df = pd.DataFrame(
        list(
            Registro_Posoperatorio.objects.all().values(*campos_registro_posoperatorio)
        )
    )
    hematoma_df = pd.DataFrame(
        list(hematoma_subdural.objects.all().values(*campos_hematoma))
    )

    # Hacer join de los dataframes
    total_df = (
        pd.merge(
            historia_df,
            episodio_df,
            how="inner",
            left_on="id",
            right_on="historia_clinica_id",
            suffixes=("_historia", "_episodio"),
        )
        .merge(
            rasgo_clinico_global_df,
            how="inner",
            left_on="id_historia",
            right_on="historia_clinica_id",
            suffixes=(None, "_rasgo_clinico_global"),
        )
        .merge(
            rasgo_clinico_episodio_df,
            how="inner",
            left_on="id_episodio",
            right_on="episodio_id",
            suffixes=(None, "_rasgos_clinicos_episodio"),
        )
        .merge(
            registro_operatorio_df,
            how="inner",
            left_on="id_episodio",
            right_on="episodio_id",
            suffixes=(None, "_registro_operatorio"),
        )
        .merge(
            rasgo_clinico_operatorio_df,
            how="inner",
            left_on="id_registro_operatorio",
            right_on="registro_operatorio_id",
            suffixes=(None, "_rasgo_clinico_operatorio"),
        )
        .merge(
            registro_posoperatorio_df,
            how="inner",
            left_on="id_registro_operatorio",
            right_on="registro_operatorio_id",
            suffixes=(None, "_registro_posoperatorio"),
        )
        .merge(
            hematoma_df,
            how="inner",
            left_on="id_episodio",
            right_on="episodio_id",
            suffixes=(None, "_hematoma"),
        )
    )

    claves_unidas = pd.concat(
        [
            total_df["codificador_id"],
            total_df["codificador_id_rasgos_clinicos_episodio"],
            total_df["codificador_id_rasgo_clinico_operatorio"],
        ]
    ).drop_duplicates()

    merge_codificadores = pd.merge(
        pd.DataFrame({"claves_unidas": claves_unidas}),
        codificador_df,
        how="left",
        left_on="claves_unidas",
        right_on="id",
    ).drop("id", axis=1)

    total_df = (
        total_df.merge(
            merge_codificadores,
            how="left",
            left_on="codificador_id",
            right_on="claves_unidas",
            suffixes=(None, "_codificadores_globales"),
        )
        .merge(
            merge_codificadores,
            how="left",
            left_on="codificador_id_rasgos_clinicos_episodio",
            right_on="claves_unidas",
            suffixes=(None, "_codificador_episodio"),
        )
        .merge(
            merge_codificadores,
            how="left",
            left_on="codificador_id_rasgo_clinico_operatorio",
            right_on="claves_unidas",
            suffixes=(None, "_codificador_operatorio"),
        )
    )

    total_df = total_df.drop(
        [
            "historia_clinica_id",
            "historia_clinica_id_rasgo_clinico_global",
            "episodio_id",
            "id",
            "episodio_id_registro_operatorio",
            "registro_operatorio_id",
            "registro_operatorio_id_registro_posoperatorio",
            "episodio_id_hematoma",
            "codificador_id",
            "codificador_id_rasgos_clinicos_episodio",
            "codificador_id_rasgo_clinico_operatorio",
            "claves_unidas",
            "claves_unidas_codificador_episodio",
            "claves_unidas_codificador_operatorio",
        ],
        axis=1,
    )
    total_df = total_df.drop(
        [
            "id_historia",
            "id_episodio",
            # "id_rasgos_clinicos_globales",
            "id_rasgos_clinicos_episodio",
            "id_registro_operatorio",
            "id_rasgo_clinico_operatorio",
            "id_registro_posoperatorio",
            "id_hematoma",
        ],
        axis=1,
    )
    total_df = total_df.drop_duplicates()

    return total_df

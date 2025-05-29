# from apps.exportar_csv.services.make_dataframe import make_dataframe
import joblib
from sklearn.ensemble import RandomForestClassifier
from .make_kb import make_kb


def train_recurrency_random_forest():
    hsc_kb = make_kb()
    columnas_eliminar = [
        "id_historia",
        "numero",
        "nombre",
        "apellidos",
        "escala_evaluacion_resultados_glasgow",
        "estado_egreso",
    ]

    for e in columnas_eliminar:
        hsc_kb = hsc_kb.drop(e, axis=1)

    x = hsc_kb.drop("es_reintervencion", axis=1)
    y = hsc_kb["es_reintervencion"]

    modelo = RandomForestClassifier(
        n_estimators=2,
        max_depth=5,
        random_state=42,
        n_jobs=-1,
        class_weight="balanced",
    )

    modelo.fit(x, y)

    joblib.dump(modelo, "apps/ia/models/random_forest_recurrency_model.joblib")

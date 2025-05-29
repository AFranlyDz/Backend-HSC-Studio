# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import joblib

from apps.exportar_csv.services.make_dataframe import make_dataframe
from ..services.train_recurrency_random_forest import train_recurrency_random_forest
from ..services.make_kb import make_kb


class prob_recurrencia(APIView):
    def post(self, request):
        train_recurrency_random_forest()

        modelo = joblib.load("apps/ia/models/random_forest_recurrency_model.joblib")
        data = request.data

        fila_predictiva = make_kb().query(f"id_historia =={data}")
        fila_predictiva = fila_predictiva.drop(
            [
                "id_historia",
                "numero",
                "nombre",
                "apellidos",
                "escala_evaluacion_resultados_glasgow",
                "estado_egreso",
                "es_reintervencion",
            ],
            axis=1,
        )
        print(fila_predictiva)
        try:
            prediction = modelo.predict(fila_predictiva.values.tolist())
            return Response(
                {"prediction": prediction.tolist()}, status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"error": f"Error en la predicción: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

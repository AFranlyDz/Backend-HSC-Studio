# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import joblib

from ..services.train_egreso_random_forest import train_egreso_random_forest
from ..services.make_kb import make_kb


class prob_estado_egreso(APIView):
    def post(self, request):
        train_egreso_random_forest()

        modelo = joblib.load("apps/ia/models/random_forest_egreso_model.joblib")
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
            ],
            axis=1,
        )
        lista_tratamientos = [
            "Tratamiento Quírurgico-1 Trépanos parietal únicos",
            "Tratamiento Quírurgico-2 Trépanos parietal frontal",
            "Tratamiento Quírurgico-3 Trépanos parietales bilaterales",
            "Tratamiento Quírurgico-4 Trepanos parietal y frontal bilateral",
            "Tratamiento Quírurgico-5 Craniectomía y membranectomía",
            "Tratamiento Quírurgico-6 Ampliación del agujero de trépano",
        ]
        lista_respuesta = []
        for i in lista_tratamientos:
            for j in lista_tratamientos:
                fila_predictiva[j] = False

            fila_predictiva[i] = True
            lista_respuesta.append(modelo.predict(fila_predictiva.values.tolist()))
        try:
            return Response({"prediction": lista_respuesta}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": f"Error en la predicción: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

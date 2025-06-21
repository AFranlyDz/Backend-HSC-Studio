from django.test import TestCase, RequestFactory
from rest_framework import status
from apps.ia.views.prob_estado_egreso import prob_estado_egreso
import joblib
import pandas as pd
from unittest.mock import patch, MagicMock


# Create your tests here.
class Test_Prob_Estado_Egreso(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Datos iniciales para todos los tests de esta clase
        cls.factory = RequestFactory()

    def test_prediccion_exitosa(self):
        # Configurar request mock
        request = self.factory.post(
            "api/probabilidad_egreso/", {"id": 1}, content_type="application/json"
        )

        # Mockear las dependencias
        with patch("apps.ia.services.make_kb") as mock_make_kb, patch(
            "joblib.load"
        ) as mock_joblib:

            # Configurar mocks
            mock_df = pd.DataFrame(
                {
                    # Campos de historia_clinica
                    "id": [1],
                    "numero": ["HC-2023-001"],
                    "nombre": ["Juan"],
                    "apellidos": ["Pérez García"],
                    "edad": [45],
                    "sexo": ["Masculino"],
                    "historial_trauma_craneal": [True],
                    # Campos de codificador
                    "nombre_codificador": ["Trauma Craneal Severo"],
                    # Campos de hematoma
                    "escala_glasgow_ingreso": [8],
                    "escala_mcwalder": [3],
                    "escala_gordon_firing": [2],
                    "escala_nomura": [1],
                    "escala_nakagushi": [4],
                    "volumen_tada": [35.2],
                    "diametro_capa": [3.5],
                    "desviacion_linea_media": [5.1],
                    "diametro_mayor_transverso": [4.8],
                    "presencia_membrana": [True],
                    "localización": ["Parietal derecho"],
                    # Campos de registro_operatorio
                    "escala_evaluacion_resultados_glasgow": [12],
                    "es_reintervencion": [False],
                    "estado_egreso": ["Alta médica"],
                }
            )
            mock_make_kb.return_value = mock_df
            mock_model = MagicMock()
            mock_model.predict.return_value = [0.85]  # Valor de prueba
            mock_joblib.return_value = mock_model

            # Llamar a la vista
            response = prob_estado_egreso().post(request)

            # Aserciones
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertIn("prediction", response.data)

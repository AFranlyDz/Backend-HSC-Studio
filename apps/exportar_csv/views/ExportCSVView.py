from io import StringIO
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ..services.make_dataframe import make_dataframe
from ..services.prepare_headers import prepare_headers


class ExportCSVView(APIView):
    def post(self, request):
        selected_fields = request.data.get("fields", [])
        if not selected_fields:
            return Response(
                {"error": "No se han seleccionado campos para exportar"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # construir un dataframe para manejar las tablas
        base_datos_denormalizada = make_dataframe(selected_fields)
        headers = prepare_headers(base_datos_denormalizada.columns.tolist())

        if len(base_datos_denormalizada.columns) == len(headers):
            base_datos_denormalizada.columns = headers
        else:
            print("¡Error! El número de columnas no coincide")

        buffer = StringIO()
        base_datos_denormalizada.to_csv(
            buffer, sep=";", index=False, encoding="utf-8-sig"
        )
        buffer.seek(0)
        response = HttpResponse(
            buffer.getvalue(), content_type="text/csv; charset=utf-8-sig"
        )
        response["Content-Disposition"] = (
            'attachment; filename="exportacion_completa.csv"'
        )
        response["Cache-Control"] = "no-cache"
        return response

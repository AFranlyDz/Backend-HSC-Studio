# views.py
import csv
from io import StringIO
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.hc.models.historia_clinica import historia_clinica
from apps.hc.models.rasgos_clinicos_globales import (
    Rasgos_Clinicos_Globales,
)
from apps.episodio.models.episodio import Episodio
from apps.episodio.models.rasgos_clinicos_episodio import Rasgos_Clinicos_Episodio
from apps.registro_operatorio.models.Registro_Operatorio import Registro_Operatorio
from apps.registro_operatorio.models.Registro_Posoperatorio import (
    Registro_Posoperatorio,
)
from apps.registro_operatorio.models.Rasgos_Clinicos_Operatorios import (
    Rasgos_Clinicos_Operatorios,
)
from apps.hematoma.models import hematoma_subdural


class ExportCSVView(APIView):
    def post(self, request):
        # Obtener la lista de campos seleccionados del frontend
        selected_fields = request.data.get("fields", [])
        if not selected_fields:
            return Response(
                {"error": "No se han seleccionado campos para exportar"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Preparar el buffer para el CSV
        buffer = StringIO()
        writer = csv.writer(buffer, delimiter=";")

        # Escribir encabezados
        headers = self._prepare_headers(selected_fields)
        writer.writerow(headers)

        # Obtener todos los datos necesarios
        historias = historia_clinica.objects.all().prefetch_related(
            "historia_clinica",  # Rasgos_Clinicos_Globales
            "historia_clinica_episodio",  # Episodios
            "historia_clinica_episodio__episodio_rce",  # Rasgos Clinicos Episodio
            "historia_clinica_episodio__episodio_registro_operatorio",  # Registro Operatorio
            "historia_clinica_episodio__episodio_registro_operatorio__registro_operatorio_posoperatorio",  # Registro Posoperatorio
            "historia_clinica_episodio__hematoma_episodio",  # Hematoma Subdural
            "historia_clinica_episodio__episodio_registro_operatorio__rasgos_clinicos_operatorios",  # Rasgos Clinicos Operatorios
        )

        # Procesar cada historia clínica
        for hc in historias:
            row = self._build_row(hc, selected_fields)
            writer.writerow(row)

        # Preparar la respuesta
        buffer.seek(0)
        response = HttpResponse(buffer, content_type="text/csv; charset=utf-8")
        response["Content-Type"] = "text/csv; charset=utf-8"
        response["Content-Disposition"] = 'attachment; filename="exportacion.csv"'
        return response

    def _prepare_headers(self, selected_fields):
        """Traduce los nombres de campos internos a nombres legibles para el CSV"""
        field_names = {
            # Historia Clínica
            "numero": "Número HC",
            "seudonimo": "Seudónimo",
            "nombre": "Nombre",
            "apellidos": "Apellidos",
            "edad": "Edad",
            "sexo": "Sexo",
            "historial_trauma_craneal": "Historial Trauma Craneal",
            "manualidad": "Manualidad",
            "antecedentes_familiares": "Antecedentes Familiares",
            # Rasgos Clínicos Globales
            "codificador.nombre": "RCG - Codificador",
            "codificador.nombre_corto": "RCG - Codificador (Abrev)",
            "codificador.descripcion": "RCG - Descripción",
            "codificador.clasificacion": "RCG - Clasificación",
            "notas": "RCG - Notas",
            # Episodio
            "inicio": "Episodio - Inicio",
            "fecha_alta": "Episodio - Fecha Alta",
            "tiempo_estadia": "Episodio - Tiempo Estadia",
            "estado_al_egreso": "Episodio - Estado Egreso",
            "tiempo_antecedente": "Episodio - Tiempo Antecedente",
            "descripcion_antecedente": "Episodio - Descripción Antecedente",
            "edad_paciente": "Episodio - Edad Paciente",
            "observaciones": "Episodio - Observaciones",
            # Rasgos Clínicos Episodio
            "codificador.nombre": "RCE - Codificador",
            "codificador.nombre_corto": "RCE - Codificador (Abrev)",
            "codificador.descripcion": "RCE - Descripción",
            "codificador.clasificacion": "RCE - Clasificación",
            "tiempo": "RCE - Tiempo",
            "notas": "RCE - Notas",
            # Registro Operatorio
            "fecha_operacion": "Registro Op. - Fecha",
            "es_reintervencion": "Registro Op. - Reintervención",
            "escala_evaluacion_resultados_glasgow": "Registro Op. - Escala Glasgow",
            "estado_egreso": "Registro Op. - Estado Egreso",
            "observaciones": "Registro Op. - Observaciones",
            # Registro Posoperatorio
            "fecha": "Posoperatorio - Fecha",
            "tiempo_transcurrido": "Posoperatorio - Tiempo Transcurrido",
            "escala_pronostica_oslo_posoperatoria": "Posoperatorio - Escala Oslo",
            "recurrencia_hematoma": "Posoperatorio - Recurrencia Hematoma",
            "gradacion_pronostica_para_recurrencia_hsc_unilateral": "Posoperatorio - Gradación Recurrencia",
            # Hematoma Subdural
            "escala_glasgow_ingreso": "Hematoma - Escala Glasgow Ingreso",
            "escala_mcwalder": "Hematoma - Escala McWalder",
            "escala_gordon_firing": "Hematoma - Escala Gordon Firing",
            "escala_pronostica_oslo_preoperatoria": "Hematoma - Escala Oslo Preop",
            "escala_nomura": "Hematoma - Escala Nomura",
            "escala_nakagushi": "Hematoma - Escala Nakagushi",
            "valor_longitud": "Hematoma - Longitud",
            "valor_diametro": "Hematoma - Diámetro",
            "valor_altura": "Hematoma - Altura",
            "volumen_tada": "Hematoma - Volumen TADA",
            "volumen": "Hematoma - Volumen",
            "grupo_volumen": "Hematoma - Grupo Volumen",
            "grupo_volumen_residual_posoperatorio": "Hematoma - Grupo Volumen Residual",
            "diametro_capa": "Hematoma - Diámetro Capa",
            "diametro_mayor_transverso": "Hematoma - Diámetro Mayor Transverso",
            "grupo_diametro": "Hematoma - Grupo Diámetro",
            "presencia_membrana": "Hematoma - Presencia Membrana",
            "tipo_membrana": "Hematoma - Tipo Membrana",
            "localización": "Hematoma - Localización",
            "topografia": "Hematoma - Topografía",
            "desviacion_linea_media": "Hematoma - Desviación Línea Media",
            "metodo_lectura": "Hematoma - Método Lectura",
            "observaciones": "Hematoma - Observaciones",
            # Rasgos Clínicos Operatorios
            "codificador.nombre": "Rasgo Op. - Codificador",
            "codificador.nombre_corto": "Rasgo Op. - Codificador (Abrev)",
            "codificador.descripcion": "Rasgo Op. - Descripción",
            "codificador.clasificacion": "Rasgo Op. - Clasificación",
        }

        return [field_names.get(field, field) for field in selected_fields]

    def _build_row(self, hc, selected_fields):
        """Construye una fila del CSV con los datos de una historia clínica"""
        row = []

        for field in selected_fields:
            value = self._get_field_value(hc, field)
            row.append(str(value) if value is not None else "")

        return row

    def _get_field_value(self, hc, field_path):
        """Obtiene el valor de un campo, manejando relaciones"""
        parts = field_path.split(".")
        current_obj = hc

        try:
            for part in parts:
                if part == "codificador" and hasattr(current_obj, "codificador"):
                    current_obj = current_obj.codificador
                elif hasattr(current_obj, part):
                    current_obj = getattr(current_obj, part)
                elif hasattr(current_obj, f"get_{part}_display"):
                    # Para campos con choices
                    current_obj = getattr(current_obj, f"get_{part}_display")()
                else:
                    # Manejar relaciones inversas (1 a muchos)
                    related_manager = getattr(current_obj, part)
                    if related_manager.count() > 0:
                        if part in [
                            "historia_clinica",
                            "episodio_rce",
                            "registros_posoperatorios",
                            "rasgos_clinicos_operatorios",
                            "hematoma_episodio",
                        ]:
                            # Tomamos el primer elemento para el CSV (podría mejorarse)
                            current_obj = related_manager.first()
                        else:
                            return "Múltiples valores"
                    else:
                        return None

            # Manejar tipos especiales
            if isinstance(current_obj, bool):
                return "Sí" if current_obj else "No"
            return current_obj
        except AttributeError:
            return None

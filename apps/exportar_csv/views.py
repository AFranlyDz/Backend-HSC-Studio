import csv
from io import StringIO
from django.http import HttpResponse
from django.db import models
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.hc.models.historia_clinica import historia_clinica
from apps.hc.models.rasgos_clinicos_globales import Rasgos_Clinicos_Globales
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
from apps.codificadores.models import Codificadores


class ExportCSVView(APIView):
    def post(self, request):
        selected_fields = request.data.get("fields", [])
        print(f"Campos seleccionados: {selected_fields}")
        if not selected_fields:
            return Response(
                {"error": "No se han seleccionado campos para exportar"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        buffer = StringIO()
        writer = csv.writer(
            buffer, delimiter=";", quoting=csv.QUOTE_ALL, escapechar="\\"
        )

        headers = self._prepare_headers(selected_fields)
        writer.writerow(headers)

        # Consulta optimizada con prefetch_related para todas las relaciones
        historias = historia_clinica.objects.prefetch_related(
            "historia_clinica",
            "historia_clinica_episodio",
            "historia_clinica_episodio__episodio_rce",
            "historia_clinica_episodio__episodio_rce__codificador",
            "historia_clinica_episodio__episodio_registro_operatorio",
            "historia_clinica_episodio__episodio_registro_operatorio__registro_operatorio_posoperatorio",
            "historia_clinica_episodio__episodio_registro_operatorio__rasgos_clinicos_operatorios",
            "historia_clinica_episodio__episodio_registro_operatorio__rasgos_clinicos_operatorios__codificador",
            "historia_clinica_episodio__hematoma_episodio",
            "historia_clinica__codificador",
        ).all()

        for hc in historias:
            # Exportar datos básicos de historia clínica
            self._export_historia_clinica(hc, writer, selected_fields)

            # Exportar rasgos clínicos globales
            self._export_rasgos_globales(hc, writer, selected_fields)

            # Exportar episodios y sus relaciones
            self._export_episodios(hc, writer, selected_fields)

        buffer.seek(0)
        response = HttpResponse(buffer, content_type="text/csv; charset=utf-8-sig")
        response["Content-Disposition"] = (
            'attachment; filename="exportacion_completa.csv"'
        )
        return response

    def _prepare_headers(self, selected_fields):
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
            "historia_clinica.codificador.nombre": "RCG - Nombre Codificador",
            "historia_clinica.codificador.nombre_corto": "RCG - Nombre Corto",
            "historia_clinica.codificador.descripcion": "RCG - Descripción",
            "historia_clinica.codificador.clasificacion": "RCG - Clasificación",
            "historia_clinica.notas": "RCG - Notas",
            # Episodio
            "episodio.inicio": "Episodio - Inicio",
            "episodio.fecha_alta": "Episodio - Fecha Alta",
            "episodio.tiempo_estadia": "Episodio - Tiempo Estadia",
            "episodio.estado_al_egreso": "Episodio - Estado Egreso",
            "episodio.tiempo_antecedente": "Episodio - Tiempo Antecedente",
            "episodio.descripcion_antecedente": "Episodio - Descripción Antecedente",
            "episodio.edad_paciente": "Episodio - Edad Paciente",
            "episodio.observaciones": "Episodio - Observaciones",
            # Rasgos Clínicos del Episodio
            "episodio.episodio_rce.codificador.nombre": "RCE - Nombre Codificador",
            "episodio.episodio_rce.codificador.nombre_corto": "RCE - Nombre Corto",
            "episodio.episodio_rce.codificador.descripcion": "RCE - Descripción",
            "episodio.episodio_rce.codificador.clasificacion": "RCE - Clasificación",
            "episodio.episodio_rce.tiempo": "RCE - Tiempo",
            "episodio.episodio_rce.notas": "RCE - Notas",
            # Registro Operatorio
            "episodio.episodio_registro_operatorio.fecha_operacion": "Registro Op. - Fecha Operación",
            "episodio.episodio_registro_operatorio.es_reintervencion": "Registro Op. - Reintervención",
            "episodio.episodio_registro_operatorio.escala_evaluacion_resultados_glasgow": "Registro Op. - Escala Glasgow",
            "episodio.episodio_registro_operatorio.estado_egreso": "Registro Op. - Estado Egreso",
            "episodio.episodio_registro_operatorio.observaciones": "Registro Op. - Observaciones",
            # Registro Posoperatorio
            "episodio.episodio_registro_operatorio.registro_operatorio_posoperatorio.fecha": "Posoperatorio - Fecha",
            "episodio.episodio_registro_operatorio.registro_operatorio_posoperatorio.tiempo_transcurrido": "Posoperatorio - Tiempo Transcurrido",
            "episodio.episodio_registro_operatorio.registro_operatorio_posoperatorio.escala_pronostica_oslo_posoperatoria": "Posoperatorio - Escala Oslo",
            "episodio.episodio_registro_operatorio.registro_operatorio_posoperatorio.recurrencia_hematoma": "Posoperatorio - Recurrencia Hematoma",
            "episodio.episodio_registro_operatorio.registro_operatorio_posoperatorio.gradacion_pronostica_para_recurrencia_hsc_unilateral": "Posoperatorio - Gradación Recurrencia",
            # Hematoma Subdural
            "episodio.hematoma_episodio.escala_glasgow_ingreso": "Hematoma - Escala Glasgow Ingreso",
            "episodio.hematoma_episodio.escala_mcwalder": "Hematoma - Escala McWalder",
            "episodio.hematoma_episodio.escala_gordon_firing": "Hematoma - Escala Gordon Firing",
            "episodio.hematoma_episodio.escala_pronostica_oslo_preoperatoria": "Hematoma - Escala Oslo Preop",
            "episodio.hematoma_episodio.escala_nomura": "Hematoma - Escala Nomura",
            "episodio.hematoma_episodio.escala_nakagushi": "Hematoma - Escala Nakagushi",
            "episodio.hematoma_episodio.valor_longitud": "Hematoma - Longitud",
            "episodio.hematoma_episodio.valor_diametro": "Hematoma - Diámetro",
            "episodio.hematoma_episodio.valor_altura": "Hematoma - Altura",
            "episodio.hematoma_episodio.volumen_tada": "Hematoma - Volumen TADA",
            "episodio.hematoma_episodio.volumen": "Hematoma - Volumen",
            "episodio.hematoma_episodio.grupo_volumen": "Hematoma - Grupo Volumen",
            "episodio.hematoma_episodio.grupo_volumen_residual_posoperatorio": "Hematoma - Grupo Volumen Residual",
            "episodio.hematoma_episodio.diametro_capa": "Hematoma - Diámetro Capa",
            "episodio.hematoma_episodio.diametro_mayor_transverso": "Hematoma - Diámetro Mayor Transverso",
            "episodio.hematoma_episodio.grupo_diametro": "Hematoma - Grupo Diámetro",
            "episodio.hematoma_episodio.presencia_membrana": "Hematoma - Presencia Membrana",
            "episodio.hematoma_episodio.tipo_membrana": "Hematoma - Tipo Membrana",
            "episodio.hematoma_episodio.localización": "Hematoma - Localización",
            "episodio.hematoma_episodio.topografia": "Hematoma - Topografía",
            "episodio.hematoma_episodio.desviacion_linea_media": "Hematoma - Desviación Línea Media",
            "episodio.hematoma_episodio.metodo_lectura": "Hematoma - Método Lectura",
            "episodio.hematoma_episodio.observaciones": "Hematoma - Observaciones",
            # Rasgos Clínicos Operatorios
            "episodio.episodio_registro_operatorio.rasgos_clinicos_operatorios.codificador.nombre": "Rasgo Op. - Nombre Codificador",
            "episodio.episodio_registro_operatorio.rasgos_clinicos_operatorios.codificador.nombre_corto": "Rasgo Op. - Nombre Corto",
            "episodio.episodio_registro_operatorio.rasgos_clinicos_operatorios.codificador.descripcion": "Rasgo Op. - Descripción",
            "episodio.episodio_registro_operatorio.rasgos_clinicos_operatorios.codificador.clasificacion": "Rasgo Op. - Clasificación",
        }
        return [field_names.get(field, field) for field in selected_fields]

    def _export_historia_clinica(self, hc, writer, selected_fields):
        """Exporta datos básicos de la historia clínica"""
        hc_fields = [
            f
            for f in selected_fields
            if not any(x in f for x in ["historia_clinica", "episodio"])
        ]
        if hc_fields:
            row = [self._get_simple_field(hc, f) for f in hc_fields]
            writer.writerow(row)

    def _export_rasgos_globales(self, hc, writer, selected_fields):
        """Exporta rasgos clínicos globales"""
        rcg_fields = [
            f
            for f in selected_fields
            if f.startswith("historia_clinica.") and "episodio" not in f
        ]
        for rasgo in hc.historia_clinica.all():
            row = [self._get_nested_field(hc, None, f, rasgo) for f in rcg_fields]
            if any(row):  # Solo escribir si hay datos
                writer.writerow(row)

    def _export_episodios(self, hc, writer, selected_fields):
        """Exporta todos los episodios con sus relaciones"""
        print(f"\nExportando episodios para HC {hc.id}")
        print(f"Campos seleccionados: {selected_fields}")
        episodio_fields = [f for f in selected_fields if "episodio" in f]
        print(f"Campos de episodio a exportar: {episodio_fields}")
        for episodio in hc.historia_clinica_episodio.all():
            # Datos básicos del episodio
            epi_row = [
                self._get_nested_field(hc, episodio, f)
                for f in episodio_fields
                if not any(
                    x in f
                    for x in [
                        "episodio_rce",
                        "episodio_registro_operatorio",
                        "hematoma_episodio",
                    ]
                )
            ]

            # Exportar rasgos clínicos del episodio (RCE)
            rce_fields = [f for f in episodio_fields if "episodio_rce" in f]
            if rce_fields:
                for rce in episodio.episodio_rce.all():
                    rce_row = epi_row.copy()
                    rce_row.extend([self._get_rce_field(rce, f) for f in rce_fields])
                    writer.writerow(rce_row)

            # Exportar registros operatorios y posoperatorios
            regop_fields = [
                f
                for f in episodio_fields
                if "episodio_registro_operatorio" in f
                and "registro_operatorio_posoperatorio" not in f
                and "rasgos_clinicos_operatorios" not in f
            ]

            posop_fields = [
                f for f in episodio_fields if "registro_operatorio_posoperatorio" in f
            ]
            rasgo_fields = [
                f for f in episodio_fields if "rasgos_clinicos_operatorios" in f
            ]

            # Solo procesar si hay campos de registro operatorio, posoperatorio o rasgos operatorios seleccionados
            if any([regop_fields, posop_fields, rasgo_fields]):
                for registro in episodio.episodio_registro_operatorio.all():
                    print(f"\nProcesando registro operatorio {registro.id}")
                    print(
                        f"Tiene {registro.rasgos_clinicos_operatorios.count()} rasgos operatorios"
                    )
                    # Preparar fila base con datos de registro operatorio si existen
                    reg_row = epi_row.copy()
                    if regop_fields:
                        reg_row.extend(
                            [
                                self._get_direct_field(registro, f.split(".")[-1])
                                for f in regop_fields
                            ]
                        )
                    # else:
                    #     reg_row = epi_row.copy()

                    # Manejar posoperatorios
                    if posop_fields:
                        posoperatorios = (
                            registro.registro_operatorio_posoperatorio.all()
                        )

                        if posoperatorios:
                            for posop in posoperatorios:
                                posop_row = reg_row.copy()
                                posop_row.extend(
                                    [
                                        self._get_posop_field(posop, f)
                                        for f in posop_fields
                                    ]
                                )
                                writer.writerow(posop_row)
                            # if not posoperatorios:
                            #     # Si no hay posoperatorios, escribir fila vacía
                            #     posop_row = reg_row.copy()
                            #     posop_row.extend(["" for _ in posop_fields])
                            #     writer.writerow(posop_row)
                            # else:
                            # for posop in posoperatorios:
                            #     posop_row = reg_row.copy()
                            #     posop_row.extend(
                            #         [
                            #             self._get_posop_field(posop, f)
                            #             for f in posop_fields
                            #         ]
                            #     )
                            #     writer.writerow(posop_row)
                    # else:
                    #     # Si no hay campos posoperatorios seleccionados, escribir fila de registro
                    #     writer.writerow(reg_row)

                    # Exportar rasgos operatorios si existen
                    if rasgo_fields:
                        for rasgo_op in registro.rasgos_clinicos_operatorios.all():
                            rasgo_row = reg_row.copy()
                            rasgo_row.extend(
                                [
                                    self._get_rasgo_op_field(rasgo_op, f)
                                    for f in rasgo_fields
                                ]
                            )
                            writer.writerow(rasgo_row)

                    if not posop_fields and not rasgo_fields:
                        writer.writerow(reg_row)

            # Exportar hematomas (mantenemos la lógica original)
            hem_fields = [f for f in episodio_fields if "hematoma_episodio" in f]
            if hem_fields:
                for hematoma in episodio.hematoma_episodio.all():
                    hem_row = epi_row.copy()
                    hem_row.extend(
                        [
                            self._get_direct_field(hematoma, f.split(".")[-1])
                            for f in hem_fields
                        ]
                    )
                    writer.writerow(hem_row)

            if not any(
                [rce_fields, regop_fields, posop_fields, rasgo_fields, hem_fields]
            ):
                writer.writerow(epi_row)

    def _get_rce_field(self, rce, field_path):
        """Método especializado para campos RCE"""
        if not field_path.startswith("episodio.episodio_rce."):
            return ""

        field_parts = field_path.split(".")[2:]  # Eliminar "episodio.episodio_rce"
        field_name = ".".join(field_parts)

        if field_name.startswith("codificador."):
            if not rce.codificador:
                return ""
            codificador_field = field_name.split(".")[1]
            return getattr(rce.codificador, codificador_field, "")
        else:
            return self._get_direct_field(rce, field_name)

    def _get_simple_field(self, obj, field_name):
        """Obtiene campos simples sin relaciones"""
        try:
            value = getattr(obj, field_name)
            return self._format_value(value)
        except AttributeError:
            return ""

    def _get_direct_field(self, obj, field_name):
        """Obtiene campos directos de un objeto"""
        try:
            if hasattr(obj, f"get_{field_name}_display"):
                return getattr(obj, f"get_{field_name}_display")()
            value = getattr(obj, field_name)
            return self._format_value(value)
        except AttributeError:
            return ""

    def _get_posop_field(self, posop, field_path):
        """Método especializado para campos de posoperatorio"""
        if not field_path.startswith(
            "episodio.episodio_registro_operatorio.registro_operatorio_posoperatorio."
        ):
            return ""

        # Extraer el nombre del campo específico (última parte del path)
        field_name = field_path.split(".")[-1]

        try:
            value = getattr(posop, field_name, "")
            return self._format_value(value)
        except Exception as e:
            return ""

    def _get_rasgo_op_field(self, rasgo_op, field_path):
        """Método especializado para campos de rasgos operatorios"""
        if not field_path.startswith(
            "episodio.episodio_registro_operatorio.rasgos_clinicos_operatorios."
        ):
            return ""

        relevant_part = field_path.split("rasgos_clinicos_operatorios.")[
            1
        ]  # Eliminar las partes anteriores

        # Manejar campos del codificador
        if relevant_part.startswith("codificador."):
            if not rasgo_op.codificador:
                return ""
            codifier_field = relevant_part.split("codificador.")[1]
            return getattr(rasgo_op.codificador, codifier_field, "")

        # Manejar campos directos del rasgo operatorio (si los hubiera)
        return self._get_direct_field(rasgo_op, relevant_part)

    def _get_nested_field(self, hc, episodio, field_path, related_obj=None):
        """Versión mejorada para manejar múltiples niveles de relaciones"""
        if not field_path:
            return ""

        parts = field_path.split(".")
        current_obj = hc

        try:
            for part in parts:
                if current_obj is None:
                    return ""

                # Manejar objetos relacionados pasados como parámetro
                if related_obj and part in str(related_obj.__class__.__name__).lower():
                    current_obj = related_obj
                    continue

                # Manejar switch a episodio
                if part == "episodio":
                    current_obj = episodio
                    continue

                # Manejar campos de elección (choices)
                if hasattr(current_obj, f"get_{part}_display"):
                    return getattr(current_obj, f"get_{part}_display")()

                # Obtener el valor
                attr = getattr(current_obj, part, None)

                if attr is None:
                    return ""

                # Manejar relaciones
                if hasattr(attr, "all"):
                    items = list(attr.all())
                    if not items:
                        return ""
                    # Para relaciones 1-N, tomamos el primer elemento
                    current_obj = items[0]
                else:
                    current_obj = attr

            # Manejar el caso especial de codificador
            if isinstance(current_obj, Codificadores):
                if "nombre" in field_path:
                    return current_obj.nombre
                elif "nombre_corto" in field_path:
                    return current_obj.nombre_corto
                elif "descripcion" in field_path:
                    return current_obj.descripcion
                elif "clasificacion" in field_path:
                    return current_obj.clasificacion

            return self._format_value(current_obj)
        except Exception as e:
            return ""

    def _format_value(self, value):
        if value is None:
            return ""
        if isinstance(value, bool):
            return "Sí" if value else "No"
        if isinstance(value, (list, dict)):
            return str(value)
        if hasattr(value, "all"):
            items = list(value.all())
            if not items:
                return ""
            return self._format_value(items[0])
        return str(value)

import numpy as np
from django.core.management.base import BaseCommand

from apps.exportar_csv.services.import_csv import import_csv
from apps.hc.models.historia_clinica import historia_clinica
from apps.episodio.models.episodio import Episodio
from apps.registro_operatorio.models.Registro_Operatorio import Registro_Operatorio
from apps.registro_operatorio.models.Registro_Posoperatorio import (
    Registro_Posoperatorio,
)
from apps.hematoma.models import hematoma_subdural
from apps.codificadores.models import Codificadores
from apps.hc.models.rasgos_clinicos_globales import Rasgos_Clinicos_Globales
from apps.episodio.models.rasgos_clinicos_episodio import Rasgos_Clinicos_Episodio
from apps.registro_operatorio.models.Rasgos_Clinicos_Operatorios import (
    Rasgos_Clinicos_Operatorios,
)


class Command(BaseCommand):
    help = "Este comando permite guardar el csv de base de conocimiento dentro de la base de datos"

    def handle(self, *args, **options):
        hsc_kb = import_csv()

        for index, row in hsc_kb.iterrows():
            hc = historia_clinica.objects.create(
                numero=row[" HISTORIA CLÍNICA"],
                nombre=row["NOMBRE                                "].split()[0],
                apellidos=row["NOMBRE                                "].split()[1]
                + row["NOMBRE                                "].split()[2],
                seudonimo=row["NOMBRE                                "].split()[0][:2]
                + row["NOMBRE                                "].split()[1][:2]
                + str(row[" HISTORIA CLÍNICA"])[-4:],
                edad=row[" EDAD"],
                sexo=row[" SEXO"],
                historial_trauma_craneal=row[" ANTECEDENTES DE TRAUMA CRANEAL"],
                manualidad=None,
                antecedentes_familiares=None,
            )

            episodio = Episodio.objects.create(
                historia_clinica=hc,
                inicio=None,
                fecha_alta=None,
                tiempo_estadia=None,
                estado_al_egreso=row[" ESTADO AL EGRESO"],
                tiempo_antecedente=None,
                descripcion_antecedente=None,
                edad_paciente=row[" EDAD"],
                observaciones=None,
            )

            registro_operatorio = Registro_Operatorio.objects.create(
                episodio=episodio,
                fecha_operacion=None,
                es_reintervencion=row[" REINTERVENCIÓ0N"],
                escala_evaluacion_resultados_glasgow=row["escala_resultados_glasgow"],
                estado_egreso=row[" ESTADO AL EGRESO"],
                observaciones="",
            )

            registro_posoperatorio = Registro_Posoperatorio.objects.create(
                registro_operatorio=registro_operatorio,
                fecha=None,
                tiempo_transcurrido=None,
                escala_pronostica_oslo_posoperatoria=None,
                recurrencia_hematoma=None,
                gradacion_pronostica_para_recurrencia_hsc_unilateral=None,
            )

            hematoma = hematoma_subdural.objects.create(
                episodio=episodio,
                escala_glasgow_ingreso=row["escala_glasgow_ingreso"],
                escala_mcwalder=row["escala_mcwalder"],
                escala_gordon_firing=row["escala_gordon_firing"],
                escala_pronostica_oslo_preoperatoria=None,
                escala_nomura=row["escala_nomura"],
                escala_nakagushi=row["escala_nakagushi"],
                valor_longitud=None,
                valor_diametro=None,
                valor_altura=None,
                volumen_tada=row[" VOLUMEN DEL HEMATOMA"],
                volumen=row[" VOLUMEN DEL HEMATOMA"],
                grupo_volumen=None,
                grupo_volumen_residual_posoperatorio=None,
                diametro_capa=row[" DIÁMETRO DE LA CAPA"],
                diametro_mayor_transverso=row[" DIÁMETRO MAYOR TRANSVERSO"],
                grupo_diametro=None,
                presencia_membrana=row[" PRESENCIA DE MEMBRANA"],
                tipo_membrana=None,
                localización="DER" if row[" LOCALIZACIÓN DERECHO"] == 1 else "IZQ",
                topografia=None,
                desviacion_linea_media=row[" DESVIACIÓN DE LÍNEA MEDIA"],
                metodo_lectura=None,
                observaciones="",
            )

            columnas_rcg = [
                ' "FACTOR DE RIESGO 1 1,\tAlcoholismo"',
                ' "FACTOR DE RIESGO 2 2,\tInsuficiencia renal crónica" ',
                " FACTOR DE RIESGO 3 Inmunosupresión",
                " FACTOR DE RIESGO 4 Neoplasia terminal",
                " FACTOR DE RIESGO 5 Ingestión de antiagregante plaquetario",
                ' "FACTOR DE RIESGO 6 \tIngestión de anticoagulante" ',
                " ANTECEDENTES  NEUROLÓGICOS 1  Demencia",
                ' "ANTECEDENTES  NEUROLÓGICOS 2,\tParkinson" ',
                " ANTECEDENTES  NEUROLÓGICOS, 3,Enfermedad cerebrovascular isquémica",
                ' "ANTECEDENTES  NEUROLÓGICOS4 4\t Enfermedad cerebrovascularhemorrágica" ',
                ' "ANTECEDENTES  NEUROLÓGICOS 5,\tEpilepsia" ',
                ' "ANTECEDENTES  NEUROLÓGICOS 6,\tNeoplasia" ',
                ' "ANTECEDENTES PATOLÓGICOS PERSONALES 1,\tCardiovasculares" ',
                ' "ANTECEDENTES PATOLÓGICOS PERSONALES 2,\tHTA  " ',
                ' "ANTECEDENTES PATOLÓGICOS PERSONALES  3,\tDiabetes mellitus   " ',
                ' "ANTECEDENTES PATOLÓGICOS PERSONALES 4,\tDigestivas  " ',
            ]
            valores_rcg = [
                "Alcoholismo",
                "Insuficiencia Renal Crónica",
                "Inmunosupresión",
                "Neoplasia Terminal",
                "Ingestión de anticoagulante plaquetario",
                "Ingestión de anticoagulante",
                "Demencia",
                "Parkinson",
                "Enfermedad Cerebrovascular Isquémica",
                "Enfermedad cerebrovascular hemorrágica",
                "Epilepsia",
                "Neoplasia",
                "Cardiovasculares",
                "HTA",
                "Diabetes Mellitus",
                "Digestivas",
            ]

            columnas_rce = [
                " SÍNTOMA 1 Cefalea",
                " SÍNTOMA 2  Vómitos",
                " SÍNTOMA 3 Trastornos neuropsiquiatricos",
                " SÍNTOMA 4 Cambios de carácter",
                " SÍNTOMA 5 Crisis comiciales",
                " SÍNTOMA 6 Perdida de la memoria",
                " SÍNTOMA 7 Alteraciones de la conciencia",
                " SÍNTOMA 8 Trastornos de la esfera psíquica superior",
                " SÍNTOMA 9 Hemiparesia o hemiplejia",
                " SÍNTOMA 10 Paresia o plejía",
                " SÍNTOMA 11 Cuadriparesia o plejía",
                " SÍNTOMA 12 Rigidez de descerebración",
                " SÍNTOMA 13 Rigidez de descorticacion",
                " SÍNTOMA 14 Trastorno sensitivo",
                " SÍNTOMA 15 Trastorno del lenguaje",
                " SÍNTOMA 16 Alteraciones pupilares",
                " SÍNTOMA 17  Papiledema",
            ]
            valores_rce = [
                "Cefalea",
                "Vómitos",
                "Trastornos Neurosiquiatricos",
                "Cambios de carácter",
                "Crisis Comiciales",
                "Pérdida de memoria",
                "Alteraciones de la conciencia",
                "Trastornos de la esfera psiquica superior",
                "Hemiparesia o Hemiplejía",
                "Paresia o Plejía",
                "Cuadriparesia o Cuadriplejía",
                "Rigidez de Descerebración",
                "Rigidez de Descorticación",
                "Trastorno Sensitivo",
                "Trastorno del Lenguaje",
                "Alteraciones Pupilares",
                "Papiledema",
            ]
            columnas_rco = [
                " TRATAMIENTO QUIRÚRGICO 1 Trépanos parietal único",
                " TRATAMIENTO QUIRÚRGICO 2  2  Trépanos parietal frontal",
                " TRATAMIENTO QUIRÚRGICO 3 Trépanos parietales bilaterales",
                " TRATAMIENTO QUIRÚRGICO 4 Trépanos par y frontal bilateral",
                " TRATAMIENTO QUIRÚRGICO 5 Craniectomía y membranectomia",
                " TRATAMIENTO QUIRÚRGICO 6 Ampliación del agujero de trepano hasta 3 cm",
                " COMPLICACIONES DE LA CIRUGÍA 1 Re acumulación",
                " COMPLICACIONES DE LA CIRUGÍA 2  Pneumoencéfalo",
                " COMPLICACIONES DE LA CIRUGÍA 3 Empiema subdural",
                " COMPLICACIONES DE LA CIRUGÍA 4  Absceso cerebral",
                " COMPLICACIONES DE LA CIRUGÍA 5 Infección de la herida",
                " COMPLICACIONES DE LA CIRUGÍA 6 Fístula de LCR",
                " COMPLICACIONES DE LA CIRUGÍA 7  HIP",
                " COMPLICACIONES DE LA CIRUGÍA 8 Fallo de la reexpanción",
                " COMPLICACIONES DE LA CIRUGÍA 9 Epilepsia",
                " HEMATOMA EPIDURAL",
                " COMPLICACIONES MÉDICAS 1 Infecciones respiratorias",
                " COMPLICACIONES MÉDICAS 2 Shock séptico",
                " COMPLICACIONES MÉDICAS 3 Meningoencefalitis",
                " COMPLICACIONES MÉDICAS 4 Enfermedades cardiovasculares",
                " COMPLICACIONES MÉDICAS 5 Enfermedad cerebrovascular isquémica",
            ]
            valores_rco = [
                "Trépanos parietal únicos",
                "Trépanos parietal frontal",
                "Trépanos parietales bilaterales",
                "Trepanos parietal y frontal bilateral",
                "Craniectomía y membranectomía",
                "Ampliación del agujero de trépano",
                "Reacumulación",
                "Pneumoencéfalo",
                "Empiema subdural",
                "Abceso Cerebral",
                "Infección de la herida",
                "Fístula de LCR",
                "HIP",
                "Fallo de la Reexpansion",
                "Epilepsia",
                "Hematoma Epidural",
                "Infecciones Respiratorias",
                "Shock séptico",
                "Meningoencefalitis",
                "Enfermedades Cardiovasculares",
                "Enfermedad Cerebrovascular Isquémica",
            ]

            for i in range(len(columnas_rcg)):
                if row[columnas_rcg[i - 1]] == 1:
                    rcg = Rasgos_Clinicos_Globales.objects.create(
                        codificador=Codificadores.objects.filter(
                            nombre=valores_rcg[i]
                        ).first(),
                        historia_clinica=hc,
                        notas="",
                    )
            for i in range(len(columnas_rce)):
                if row[columnas_rce[i - 1]] == 1:
                    rcg = Rasgos_Clinicos_Episodio.objects.create(
                        codificador=Codificadores.objects.filter(
                            nombre=valores_rce[i]
                        ).first(),
                        episodio=episodio,
                        tiempo=None,
                        notas="",
                    )
            for i in range(len(columnas_rco)):
                if row[columnas_rco[i - 1]] == 1:
                    rcg = Rasgos_Clinicos_Operatorios.objects.create(
                        registro_operatorio=registro_operatorio,
                        codificador=Codificadores.objects.filter(
                            nombre=valores_rco[i]
                        ).first(),
                    )
        self.stdout.write(
            self.style.SUCCESS("!Migración a base de datos ejecutada con éxito!")
        )

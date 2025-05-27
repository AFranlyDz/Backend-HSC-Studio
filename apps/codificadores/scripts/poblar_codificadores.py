from apps.codificadores.models import Codificadores


def poblar_codificadores():
    tipos_codificadores = {
        "Factor de Riesgo": [
            "Alcoholismo",
            "Insuficiencia Renal Crónica",
            "Inmunosupresión",
            "Neoplasia Terminal",
            "Ingestión de anticoagulante plaquetario",
            "Ingestión de anticoagulante",
        ],
        "Antecedente Neurológico": [
            "Demencia",
            "Parkinson",
            "Enfermedad Cerebrovascular Isquémica",
            "Enfermedad cerebrovascular hemorrágica",
            "Epilepsia",
            "Neoplasia",
        ],
        "Antecedente Patológico": [
            "Cardiovasculares",
            "HTA",
            "Diabetes Mellitus",
            "Digestivas",
        ],
        "Lesión Isquémica": [],
        "Factor Predisponente": [],
        "Síntoma": [
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
        ],
        "Forma Clínica de Presentación": [],
        "Tratamiento Quírurgico": [
            "Trépanos parietal únicos",
            "Trépanos parietal frontal",
            "Trépanos parietales bilaterales",
            "Trepanos parietal y frontal bilateral",
            "Craniectomía y membranectomía",
            "Ampliación del agujero de trépano",
        ],
        "Complicaciones Médicas": [
            "Infecciones Respiratorias",
            "Shock séptico",
            "Meningoencefalitis",
            "Enfermedades Cardiovasculares",
            "Enfermedad Cerebrovascular Isquémica",
        ],
        "Complicaciones Cirugía": [
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
        ],
    }
    for tipo, lista in tipos_codificadores.items():
        for elemento in lista:
            codificadores = Codificadores.objects.create(
                nombre=elemento, nombre_corto="", descripcion="", clasificacion=tipo
            )

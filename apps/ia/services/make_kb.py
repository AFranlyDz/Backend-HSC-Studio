from apps.exportar_csv.services.make_knowledge_base import make_knowledge_base


def make_kb():
    lista_campos = [
        "historia_clinica.id",
        "historia_clinica.numero",
        "historia_clinica.nombre",
        "historia_clinica.apellidos",
        "historia_clinica.edad",
        "historia_clinica.sexo",
        "historia_clinica.historial_trauma_craneal",
        "codificador.nombre",
        "hematoma.escala_glasgow_ingreso",
        "hematoma.escala_mcwalder",
        "hematoma.escala_gordon_firing",
        "hematoma.escala_nomura",
        "hematoma.escala_nakagushi",
        "hematoma.volumen_tada",
        "hematoma.diametro_capa",
        "hematoma.desviacion_linea_media",
        "hematoma.diametro_mayor_transverso",
        "hematoma.presencia_membrana",
        "registro_operatorio.escala_evaluacion_resultados_glasgow",
        "registro_operatorio.es_reintervencion",
        "registro_operatorio.estado_egreso",
        "hematoma.localización",
    ]
    return make_knowledge_base(lista_campos, tipo=2)

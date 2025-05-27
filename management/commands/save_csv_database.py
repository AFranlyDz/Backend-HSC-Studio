import numpy as np
from import_csv import import_csv
from apps.hc.models.historia_clinica import historia_clinica
from apps.episodio.models.episodio import Episodio


def save_csv_database():
    hsc_kb = import_csv()

    for _, row in hsc_kb:
        if row[" HISTORIA CLÍNICA"] == np.nan:
            row[" HISTORIA CLÍNICA"] = np.random.randint(10000000, 99999999)
        hc = historia_clinica.objects.create(
            numero=row[" HISTORIA CLÍNICA"],
            nombre=row["NOMBRE                                "].split()[0],
            apellidos=row["NOMBRE                                "].split()[1]
            + row["NOMBRE                                "].split()[2],
            seudonimo=row["NOMBRE                                "].split()[0].str[:2]
            + row["NOMBRE                                "].split()[1].str[:2]
            + row[" HISTORIA CLÍNICA"].astype(str).str[-4:],
            edad=row[" EDAD"],
            sexo=[" SEXO"],
            historial_trauma_craneal=[" ANTECEDENTES DE TRAUMA CRANEAL"],
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

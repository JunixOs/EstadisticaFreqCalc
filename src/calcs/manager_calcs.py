import pandas as pd
from calcs import cuantitative_no_grouped_data as nq
from calcs import cuantitative_grouped_data as g

from python_calamine import CalamineWorkbook

def gestionar_datos(path_excel, column_name, tipo_variable, precision , sheet_idx):
    # Leer Excel
    Excel = CalamineWorkbook.from_path(path_excel).get_sheet_by_index(sheet_idx - 1).to_python(skip_empty_area=False)
    df = pd.DataFrame(data=Excel[1:] , columns=Excel[0])
    if column_name not in df.columns:
        raise ValueError("La columna no existe en el archivo Excel.")

    data = df[column_name].dropna().tolist()
    try:
        data = list(map(float, data))  # Intenta convertir todos los valores a float
    except:
        raise ValueError("La columna contiene valores no numéricos.")

    n = len(data)

    if tipo_variable == "Discreta":
        xi, fi = nq.Calc_fi_and_xi(data)
        hi = nq.Calc_hi(fi, n)
        Hi = nq.Calc_Hi(hi)
        pi = nq.Calc_pi_percent(hi)
        Pi = nq.Calc_Pi_percent(hi)
        media = nq.Calc_Atihmetic_Average(data)
        mediana = nq.Calc_Median(data)
        moda = nq.Calc_Mode_Mo(xi, fi)
        varianza = nq.Calc_Variance(data, media)
        desviacion = nq.Calc_Standart_Variation(varianza)
        coef_variacion = nq.Calc_Coefficient_Variation(desviacion, media)

        return {
            "tipo": "Discreta",
            "xi": xi, "fi": fi, "hi": hi, "Hi": Hi, "pi": pi, "Pi": Pi,
            "media": media, "mediana": mediana, "moda": moda,
            "varianza": varianza, "desviacion": desviacion, "coef_variacion": coef_variacion
        }

    elif tipo_variable == "Continua":
        vmin = g.Find_Min(data)
        vmax = g.Find_Max(data)
        rango = g.Calc_Range(data)
        k = g.Calc_Intervals_Number(n)
        k_redondeado = g.Calc_Rounded_Intervals_Number(k)
        amplitud, decimales = g.Calc_Amplitude(rango, k_redondeado, precision)
        intervalos = g.Calc_Intervals(vmin, amplitud, k_redondeado, decimales)
        xi = g.Calc_xi(intervalos)
        fi = g.Calc_fi(data, intervalos)
        hi = g.Calc_hi(fi, n)
        Hi = g.Calc_Hi(hi)
        pi = g.Calc_pi(hi)
        Pi = g.Calc_Pi(pi)
        media = g.Calc_Aithmetic_Average(xi, fi, n)
        mediana = g.Calc_Median(intervalos, g.Calc_Fi(fi), n, amplitud, fi)
        moda = g.Calc_Mode(intervalos, amplitud, fi)
        varianza = g.Calc_Variance(xi, fi, media, n)
        desviacion = g.Calc_Standart_Variation(varianza)
        coef_variacion = g.Calc_Coefficient_Variation(desviacion, media)

        return {
            "data" : data,
            "tipo": "Continua",
            "intervalos": intervalos, "xi": xi, "fi": fi, "hi": hi, "Hi": Hi, "pi": pi, "Pi": Pi,
            "media": media, "mediana": mediana, "moda": moda,
            "varianza": varianza, "desviacion": desviacion, "coef_variacion": coef_variacion
        }

    else:
        raise ValueError("Tipo de variable no reconocido.")

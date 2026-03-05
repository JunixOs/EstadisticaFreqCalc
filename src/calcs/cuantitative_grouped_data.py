import numpy as np

from decimal import Decimal

# ========================================================= Calculo de Frecuencias =========================================================


def Find_Max_Decimals_In_Data(Data):
    N_Decimals = [len(str(data).split(".")[1]) for data in Data if "." in str(data)]

    return np.max(N_Decimals)


def Find_Min(data):
    return np.min(data)


def Find_Max(data):
    return np.max(data)


def Calc_Range(data):
    return np.max(data) - np.min(data)


def Calc_Intervals_Number(n):
    return 1 + (3.322 * np.log10(n))


def Calc_Rounded_Intervals_Number(m):
    return round(m)


def Calc_Amplitude(rango, m_redondeado, max_n_decimals_in_data):
    """
    ==============================================================================================
    Esta funcion se encarga de redondear la amplitud, recibe un valor y le añade una decima de mas
    para que el ultimo intervalo se pase un poco del valor maximo del dataset.
    Ejemplos de uso:
        Input: 1.3456 , N_Decimals = 2
        Output: 1.346

        Input: 0.02 , N_Decimals = 2
        Output: 0.021
    ==============================================================================================
    """
    Number = rango / m_redondeado
    print(f"{Number=}")

    N_Decimals = max_n_decimals_in_data
    if Number - round(Number) != 0:
        """print(f"{Number=}")"""
        Integer_Part = str(Number).split(".")[0]
        Decimal_Part = str(Number).split(".")[1]

        N_Decimals = N_Decimals if N_Decimals < len(Decimal_Part) else len(Decimal_Part)
        if N_Decimals > len(Decimal_Part) - 1:
            Decimal_Part += "0"

        if int(Decimal_Part[N_Decimals]) >= 5:
            Decimal_Part = "".join(
                [val for i, val in enumerate(Decimal_Part, start=1) if i <= N_Decimals]
            )
            Value_To_Add = float("0." + "0" * (N_Decimals - 1) + "1")
        else:
            Decimal_Part = "".join(
                [
                    val
                    for i, val in enumerate(Decimal_Part, start=1)
                    if i <= N_Decimals + 1
                ]
            )
            Value_To_Add = "0." + "0" * N_Decimals + "1"
            N_Decimals += 1

        Number = float(Integer_Part + "." + Decimal_Part)

        """ print("Numero cortado: " , Number) """

        Decimals_To_Round = "1." + "0" * (N_Decimals) if N_Decimals > 0 else "1"

        Number = float(Decimal(str(Number)).quantize(Decimal(Decimals_To_Round)))

        Number += float(Value_To_Add)
        """ print(f"{Number=}") """

        return round(Number, N_Decimals), N_Decimals
    else:
        return Number + 0.1 , N_Decimals + 1


def Calc_Intervals(vmin, amplitud, m, N_Decimals_C):
    intervals = []
    lower = round(vmin, N_Decimals_C)
    for _ in range(m):
        upper = lower + amplitud
        upper = round(upper, N_Decimals_C)
        intervals.append([lower, upper])
        lower = upper
    return intervals


def Calc_xi(intervals):
    return [(l + u) / 2 for l, u in intervals]


def Calc_fi(data, intervals):
    fi = []
    for lower, upper in intervals:
        count = sum(1 for x in data if lower <= x < upper)
        fi.append(count)
    return fi


def Calc_Fi(fi):
    return np.cumsum(fi)


def Calc_hi(fi, n):
    return [f / n for f in fi]


def Calc_Hi(hi):
    return np.cumsum(hi)


def Calc_pi(hi):
    return [h * 100 for h in hi]


def Calc_Pi(pi):
    return np.cumsum(pi)


# ========================================================= Medidas de Tendencia Central =========================================================
def Calc_Aithmetic_Average(Arr_xi, Arr_fi, n):
    return sum([fi * xi for fi, xi in zip(Arr_fi, Arr_xi)]) / n


def Calc_Median(Arr_Intervals, Arr_Fi, n, C, Arr_fi):
    Aprox_Position_Median_Class = n / 2
    Position_Median_Class = 0
    F_i_before = 0

    for i in range(0, len(Arr_Fi)):
        F_i_before, Fi = 0, 0  # F(i-1) y Fi
        if i == 0:
            F_i_before = 0
        else:
            F_i_before = Arr_Fi[i - 1]

        Fi = Arr_Fi[i]

        if F_i_before <= Aprox_Position_Median_Class < Fi:
            Position_Median_Class = i
            break
    return Arr_Intervals[Position_Median_Class][0] + (
        (((n / 2) - F_i_before) / (Arr_fi[Position_Median_Class])) * C
    )


def Calc_Mode(Arr_Intervals, C, Arr_fi):
    Arr_Mo = []

    Max_fi = np.max(Arr_fi)

    Idx_Max_fi = [i for i, fi in enumerate(Arr_fi) if fi == Max_fi]

    for idx in Idx_Max_fi:
        f_mo = Arr_fi[idx]
        if idx == 0:
            fi_before = 0
        else:
            fi_before = Arr_fi[idx - 1]

        if idx == len(Arr_fi) - 1:
            fi_after = 0
        else:
            fi_after = Arr_fi[idx + 1]

        d1 = f_mo - fi_before
        d2 = f_mo - fi_after

        Arr_Mo.append(Arr_Intervals[idx][0] + (d1 / (d1 + d2)) * C)
    if len(Arr_Mo) == len(Arr_fi) or len(Arr_Mo) == 0:
        return ["Amodal"]
    else:
        return Arr_Mo


# ========================================================= Medidas de Posicion =========================================================
def Calc_Quantile(Arr_Intervals, Arr_Fi, n, C, Arr_fi, Type_Quantile):
    match (Type_Quantile):
        case "Cuartil":
            i = 4
        case "Decil":
            i = 10
        case "Percentil":
            i = 100

    Arr_Cuantile = []

    for k in range(1, i):
        Aprox_Position_Cuantile_Class = (k * n) / i
        Position_Cuantile_Class = 0

        for idx in range(0, len(Arr_Fi)):
            F_i_before, Fi = 0, 0  # F(i-1) y Fi
            if idx == 0:
                F_i_before = 0
            else:
                F_i_before = Arr_Fi[idx - 1]

                Fi = Arr_Fi[idx]

            if F_i_before <= Aprox_Position_Cuantile_Class < Fi:
                Position_Cuantile_Class = idx
                break

        Arr_Cuantile.append(
            Arr_Intervals[Position_Cuantile_Class][0]
            + (
                (((k * n) / i) - Arr_Fi[Position_Cuantile_Class - 1])
                / Arr_fi[Position_Cuantile_Class]
            )
        )

    return Arr_Cuantile


# ========================================================= Medidas de Dispercion =========================================================
def Calc_Variance(Arr_xi, Arr_fi, Arithmetic_Average, n):
    return np.sum(
        ((xi - Arithmetic_Average) ** 2) * fi for xi, fi in zip(Arr_xi, Arr_fi)
    ) / (n - 1)


def Calc_Standart_Variation(S_2):
    return np.sqrt(S_2)


def Calc_Coefficient_Variation(S, Arithmetic_Average):
    return (S / Arithmetic_Average) * 100

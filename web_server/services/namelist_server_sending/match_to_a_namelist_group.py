from types import MappingProxyType


def match_to_a_namelist_group(nml_data: MappingProxyType[str, float | int | str]):
    data = dict(nml_data)

    group = ""

    if data["fuel"] == "Gasolina" and data["subcategory"] == "B":
        group = "veic1"

    elif data["fuel"] == "Álcool" and data["subcategory"] == "B":
        group = "veic2"

    elif data["fuel"] == "Flex" and data["subcategory"] == "B":
        group = "veic3"

    elif data["fuel"] == "Diesel" and data["subcategory"] == "C":
        group = "veic4a"

    elif data["fuel"] == "Diesel" and data["subcategory"] == "D":
        group = "veic4b"

    elif (
        data["fuel"] == "Diesel" and data["subcategory"] == "D"
        # and data["note"].lower() == "rodoviario"
    ):
        group = "veic4b"

    elif data["subcategory"] == "B":
        # and data["note"].lower() == "taxi"

        group = "veic5"

    elif data["subcategory"] == "A":
        group = "veic6"

    else:
        group = "veic1"

    data["frac_" + group] = 0.8
    data["fuel"] = 0
    data["subcategory"] = 0

    data["use_" + group] = data.pop("autonomy")

    return data

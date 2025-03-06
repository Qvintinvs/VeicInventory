def parse_namelist(data: dict) -> dict:
    group = ""
        

    if (data['fuel'] == 'Gasolina' and data['subcategory'] == 'B'):
            group = 'veic1'

    if (data['fuel'] == 'Álcool' and data['subcategory'] == 'B'):
            group = 'veic2'

    if (data['fuel'] == 'Flex' and data['subcategory'] == 'B'):
            group = 'veic3'

    if (data['fuel'] == 'Diesel' and data['subcategory'] == 'C'):
            group = 'veic4a'

    if (data['fuel'] == 'Diesel' and data['subcategory'] == 'D'):
            group = 'veic4b'

    if (data['fuel'] == 'Diesel' and data['subcategory'] == 'D' and data['note'].lower() == "rodoviario"):
            group = 'veic4b'

    if (data['subcategory'] == 'B' and data['note'].lower() == "taxi"):
            group = 'veic5'

    if (data['subcategory'] == 'A'):
            group = 'veic6'

    data['frac_' + group] = data.pop('fraction')
    data.pop('note')
    data.pop('fuel')
    data.pop('subcategory')

    #temp
    data['use_' + group] = data.pop('autonomy')

    return data
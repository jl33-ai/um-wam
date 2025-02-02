def calculate_wam(grades):
    total_credit = sum(g['credit_points'] for g in grades)
    all_credit = sum(g['credit_points'] for g in grades if g['grade'] > 0)
    calculated_wam = sum([g['grade'] * (g['credit_points'] / all_credit) for g in grades]) if grades else 0
    return calculated_wam, total_credit


def get_letter_grade_freq(grades):
    freq_dict = {'H1': 0, 'H2A': 0, 'H2B': 0, 'H3': 0, 'P': 0, 'N': 0, '*': 0}
    maximum_g = 0
    minimum_g = 100

    for g in grades:
        freq_dict[get_letter_grade(g['grade'])] += 1
        if g['grade'] > maximum_g:
            maximum_g = g['grade']
        if g['grade'] < minimum_g:
            minimum_g = g['grade']

    return freq_dict, maximum_g, minimum_g


def get_letter_grade(g):
    if g >= 80:
        return 'H1'
    elif g >= 75:
        return 'H2A'
    elif g >= 70:
        return 'H2B'
    elif g >= 65:
        return 'H3'
    elif g >= 50:
        return 'P'
    elif g == 0:
        return '*'
    else:
        return 'N'

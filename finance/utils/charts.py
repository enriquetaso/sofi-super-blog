months = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]
colorPalette = [
    "#55efc4",
    "#81ecec",
    "#a29bfe",
    "#ffeaa7",
    "#fab1a0",
    "#ff7675",
    "#fd79a8",
]
colorPrimary, colorSuccess, colorDanger = "#79aec8", colorPalette[0], colorPalette[5]


def get_year_dict():
    """Creates a dictionary of months and values,
    which we'll use to add the monthly data to."""
    year_dict = dict()

    for month in months:
        year_dict[month] = 0

    return year_dict


def generate_color_palette(amount):
    """Generates a color palette based on the amount of colors needed."""
    palette = []

    i = 0
    while i < len(colorPalette) and len(palette) < amount:
        palette.append(colorPalette[i])
        i += 1
        if i == len(colorPalette) and len(palette) < amount:
            i = 0

    return palette

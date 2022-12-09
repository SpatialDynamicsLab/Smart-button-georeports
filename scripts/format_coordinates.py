
def dd_formating(dd_lat, dd_long):
    lat = ''
    long = ''
    if dd_lat:
        north_dir = dd_lat.find('N')
        print(north_dir)
        if north_dir != -1:
            get_lat = float(dd_lat.split('N')[0]) / 100
        else:
            get_lat = -float(dd_lat.split('S')[0]) / 100
        lat = get_lat
    if dd_long:
        east_dir = dd_long.find('E')
        if east_dir != -1:
            get_long = float(dd_long.split('E')[0]) / 100
        else:
            get_long = -float(dd_long.split('W')[0]) / 100
        long = get_long
    return lat, long

coords = dd_formating('4024.58146N', '00342.72859W')
print(coords[0])
print(coords[1])

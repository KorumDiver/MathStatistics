def rf_task_1(url_file: str):
    with open(url_file, 'r') as file:
        lines = file.readlines()
        ret = []
        for line in lines:
            dX, dY = line.split(';')
            dX = float(dX)
            dY = float(dY)
            if dX > dY:
                ret.append(1)
            else:
                ret.append(0)

    return ret


def rf_task_2(url_file: str):
    with open(url_file) as file:
        lines = file.readlines()
        value=[]
        for i in lines:
            value.append(float(i))

        return value

def _plotline_low(x0, y0, x1, y1):
    xreturn = []
    yreturn = []
    dx = x1 - x0
    dy = y1 - y0
    yi = 1
    if dy < 0:
        yi = -1
        dy = -dy

    D = 2 * dy - dx
    y = y0

    for x in range(x0, x1):
        xreturn.append(x)
        yreturn.append(y)
        if D > 0:
            y = y + yi
            D = D - 2 * dx

        D = D + 2*dy

    return zip(xreturn, yreturn)


def _plotline_high(x0, y0, x1, y1):
    xreturn = []
    yreturn = []
    dx = x1 - x0
    dy = y1 - y0
    xi = 1
    if dx < 0:
        xi = -1
        dx = -dx

    D = 2 * dx - dy
    x = x0
    for y in range(y0, y1):
        xreturn.append(x)
        yreturn.append(y)
        if D > 0:
            x = x + xi
            D = D - 2 * dy

        D = D + 2 * dx

    return zip(xreturn, yreturn)

def plotline(x0, y0, x1, y1):
    result = None
    if abs(y1 - y0) < abs(x1 - x0):
        if x0 > x1:
            result = _plotline_low(x1, y1, x0, y0)
        else:
            result = _plotline_low(x0, y0, x1, y1)

    else:
        if y0 > y1:
            result = _plotline_high(x1, y1, x0, y0)
        else:
            result = _plotline_high(x0, y0, x1, y1)

    return result
        

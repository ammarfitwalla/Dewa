import math

cords = [(1443, 930), (395, 565), (810, 1261), (1445, 911), (1222, 497), (1224, 338), (464, 567), (1433, 1025),
         (836, 1175), (838, 1234), (383, 449), (548, 293), (628, 293), (711, 293), (516, 294), (880, 294)]

while len(cords) != 0:
    for e, i in enumerate(cords):
        # print(e)
        Px = cords[0][0]
        Py = cords[0][1]

        if e != 0:
            Qx = i[0]
            Qy = i[1]

            # Calculate the Euclidean distance  
            # between points P and Q

            # euclidean_distance = math.sqrt((Px - Qx) ** 2 + (Py - Qy) ** 2)
            eDistance = math.dist([Px, Py], [Qx, Qy])
            print(int(eDistance))

        else:
            pass

    cords.pop(0)



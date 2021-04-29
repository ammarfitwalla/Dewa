import csv
import cv2
import math
import random
import sys

# INPUT_CSV = "sld_25_consolidated.csv"
INPUT_CSV = r"E:\dewa\pdfs\GCNN\ClusterGCN\NOC_OUTPUT\CSV\with_textvalues\trial_trench_details_sheet_2.csv"
# POLYLINE_CSV = "final_updated_sld_25_output.csv"
INPUT_IMAGE = r"E:\dewa\pdfs\GCNN\ClusterGCN\NOC_OUTPUT\CSV\with_textvalues\trial trench details sheet 2.png"


# INPUT_IMAGE = "sld_26.jpg"


def read_csv(ifil):
    csv_data = []
    with open(ifil, "r") as input_csv:
        reader = csv.reader(input_csv)
        for data in reader:
            if data:
                csv_data.append(data)
    csv_data.remove(csv_data[0])
    return csv_data


def sort_polyline(data):
    rectl = []
    frst_t = True
    lstv = data[len(data) - 1]
    for i in data:
        if int(i[0]) == 1 and frst_t:
            rectl.append(i)
            frst_t = False
        elif int(i[0]) == 1 and not frst_t:
            rectl.append(pre)
            rectl.append(i)
        pre = i
    rectl.append(lstv)
    frctl = []
    for _ in range(len(rectl) // 2):
        frctl.append([rectl[0][1], rectl[0][2], rectl[1][1], rectl[1][2]])
        rectl.remove(rectl[0])
        rectl.remove(rectl[0])
    return frctl


def drarect(data, image):
    clrs = [(0, 0, 255), (0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 0, 255), (255, 255, 0)]
    # clr = random.choice(clrs)
    clr = (0, 255, 0)
    for i in data:
        cv2.rectangle(image, (int(i[0]), int(i[1])), (int(i[2]), int(i[3])), clr, 2)
    return image


def drapnt(data, image):
    fpl = []
    for i in data:
        xmin, ymin, xmax, ymax = int(i[0]), int(i[1]), int(i[2]), int(i[3])
        # cv2.circle(image, (xmin, ymin), 1, (0, 177, 0), 2)
        # cv2.circle(image, (xmax, ymin), 1, (0, 177, 0), 2)
        # cv2.circle(image, (xmin, ymax), 1, (0, 177, 0), 2)
        # cv2.circle(image, (xmax, ymax), 1, (0, 177, 0), 2)

        x1_midpoint = ((xmin + xmax) // 2, (ymin + ymin) // 2)
        x2_midpoint = ((xmin + xmax) // 2, (ymax + ymax) // 2)
        y1_midpoint = ((xmin + xmin) // 2, (ymin + ymax) // 2)
        y2_midpoint = ((xmax + xmax) // 2, (ymin + ymax) // 2)

        # image = cv2.circle(image, x1_midpoint, 1, (0, 255, 0), 2)
        # image = cv2.circle(image, x2_midpoint, 1, (0, 255, 0), 2)
        # image = cv2.circle(image, y1_midpoint, 1, (0, 255, 0), 2)
        # image = cv2.circle(image, y2_midpoint, 1, (0, 255, 0), 2)

        center_coord = int((xmin + xmax) / 2), int((ymin + ymax) / 2)
        # image = cv2.circle(image, center_coord, 1, (0, 255, 0), 2)

        templ = [(xmin, ymin), (xmax, ymin), (xmin, ymax), (xmax, ymax), x1_midpoint, x2_midpoint, y1_midpoint,
                 y2_midpoint, center_coord]
        fpl.append(templ)

    return image, fpl


def srup(rl, sl):
    for i in rl:
        xmin, ymin, xmax, ymax = int(i[0]), int(i[1]), int(i[2]), int(i[3])
        center_coord = int((xmin + xmax) / 2), int((ymin + ymax) / 2)
        for j in sl:
            xmin, ymin, xmax, ymax = int(j[0]), int(j[1]), int(j[2]), int(j[3])
            if xmin < center_coord[0] < xmax and ymin < center_coord[1] < ymax:
                rl.remove(i)
                break
    return rl


def rup(wpl, vil, txtl):
    twpl = srup(wpl, vil)
    twpl = srup(twpl, txtl)
    return twpl


def get_spnt(fndlst):
    tl = []
    for i in fndlst:
        tl.append(i[0])
    stmp_elmnt = min(tl)
    for i in fndlst:
        if stmp_elmnt == i[0]:
            frstv, scndv = i[1], i[2]
    return frstv, scndv


def get_pnts(flist, slist):
    sml_ed_pnts = []
    for i in flist:
        x1 = i[0]
        x2 = i[1]
        tl = []
        for j in slist:
            y1 = j[0]
            y2 = j[1]
            e_dist = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
            tl.append([e_dist, i, j])

        first_val, second_val = get_spnt(tl)
    return first_val, second_val


vt_data = read_csv(INPUT_CSV)
# p_data = read_csv(POLYLINE_CSV)

vi = False
txt = False
pllin = True

vil = []
txtl = []
pllinl = []

for d in vt_data:
    if vi:
        if d[1] == "Shape":
            vi = False
            txt = True
            continue
        elif d[0] != '':
            vil.append([d[1], d[2], d[3], d[4], d[5]])

    elif txt:
        if d[0] == "xmin":
            txt = False
            pllin = True
            continue
        elif d[0] != '':
            txtl.append([d[0], d[1], d[2], d[3], d[4]])

    elif pllin:
        if d[0] == 'Polyline':
            continue
        elif d[0] != '' and d[0] != 'xmin':
            pllinl.append([d[0], d[1], d[2]])
        elif d[0] == 'xmin':
            txt = True
            pllin = False

# pllinl = read_csv(POLYLINE_CSV)
print(pllinl)
print(txtl)
fpl = sort_polyline(pllinl)
print(fpl)

# fwpl = rup(fpl, vil, txtl)

image = cv2.imread(INPUT_IMAGE)
image = drarect(vil, image)
image = drarect(txtl, image)
image = drarect(fpl, image)

image, point_vil = drapnt(vil, image)
image, point_txtl = drapnt(txtl, image)
image, point_fwpl = drapnt(fpl, image)

cv2.imwrite("noc_sheet_2.jpg", image)

# sys.exit()

coordinates = point_vil + point_txtl + point_fwpl


def Sort_Tuple(tup):
    tup.sort(key=lambda x: x[0])
    return tup


semi_final = []
final_value, min_1, min_2, min_3 = [], [], [], []
for i in range(len(coordinates)):
    mat = []
    first = []
    x1 = None
    y1 = None
    for num, coordinate in enumerate(coordinates):
        for n, c in enumerate(coordinates):
            if i != n:
                mat.append(c)
            else:
                first.append(c)

        for m in mat:
            m_n_list = []
            for n in first:
                n_l_list = []
                for l in n:
                    l_b_list = []
                    for b in m:
                        # print(l, b)
                        x1 = l[0], y1 = l[1], x2 = b[0], y2 = b[1]

                        e_dist = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
                        l_b_list.append([int(e_dist), l, b])
                    # print(l_b_list)
                    min_1 = Sort_Tuple(l_b_list)[0]  # 1st element to 2nd list
                    l_b_list.clear()
                    n_l_list.append(min_1)

                min_2 = Sort_Tuple(n_l_list)[0]
                n_l_list.clear()
                m_n_list.append(min_2)
            min_3 = Sort_Tuple(m_n_list)[0]
            semi_final.append(min_3)
            m_n_list.clear()
        final = Sort_Tuple(semi_final)[0]
        print(final)
        semi_final.clear()
        cv2.line(image, final[1], final[2], (255, 0, 0), 2)
        cv2.imwrite("output_whole_ammar.jpg", image)
        break

# fvi_txt_pl_list = []
# for i in vi_txt_pl_list:
#     for j in vi_txt_pl_list:
#         if i == j:
#             continue
#         frst_pnt, scnd_pnt = get_pnts(i, j)
#         print(frst_pnt, scnd_pnt)
#         i.append(frst_pnt)
#         i.append(scnd_pnt)
#         fvi_txt_pl_list.append(i)
#
# print(fvi_txt_pl_list[0])

cv2.imwrite("output_whole_ammar.jpg", image)

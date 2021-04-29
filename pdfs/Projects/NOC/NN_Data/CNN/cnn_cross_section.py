import csv, cv2
import math
import re
import sys
from prettytable import PrettyTable
import numpy as np
import silence_tensorflow

silence_tensorflow.silence_tensorflow()
import tensorflow as tf

from find_red_section import get_red_strings


def read_csv(file):
    data = []
    with open(file, "r") as fo:
        reader = csv.reader(fo)
        for i in reader:
            if i: data.append(i)
    data.remove(data[0])
    return data


def segregate_whl_dta(data):
    vi, txt, pllin = False, True, False
    # vi, txt, pllin = False, False, True
    vil, txtl, pllinl = [], [], []

    for d in data:
        if vi:
            if d[1] == "Shape":
                vi = False
                txt = True
                continue
            vil.append([d[1], d[2], d[3], d[4], d[5]])

        elif txt:
            if d[0] == "Polyline":
                txt = False
                pllin = True
                continue
            txtl.append([d[0], d[1], d[2], d[3], d[4]])
            # txtl.append([d[3], d[4], d[5], d[6], d[7]])

        elif pllin:
            if d[0] == 'xmin':
                pllin = False
                txt = True
            if d[0] != 'Line':
                pllinl.append([d[0], d[1], d[2]])
    return vil, txtl, pllinl


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


def get_pnt_lst(data):
    fpl = []
    for i in data:
        # print(len(i))
        xmin, ymin, xmax, ymax = int(i[0]), int(i[1]), int(i[2]), int(i[3])

        x1_midpoint = ((xmin + xmax) // 2, (ymin + ymin) // 2)
        x2_midpoint = ((xmin + xmax) // 2, (ymax + ymax) // 2)
        y1_midpoint = ((xmax + xmax) // 2, (ymin + ymax) // 2)
        y2_midpoint = ((xmin + xmin) // 2, (ymin + ymax) // 2)

        center_coord = int((xmin + xmax) // 2), int((ymin + ymax) // 2)

        if len(i) == 5:
            templ = [(xmin, ymin), x1_midpoint, (xmax, ymin), y1_midpoint, (xmax, ymax), x2_midpoint, (xmin, ymax),
                     y2_midpoint, center_coord, i[len(i) - 1]]
        else:
            templ = [(xmin, ymin), x1_midpoint, (xmax, ymin), y1_midpoint, (xmax, ymax), x2_midpoint, (xmin, ymax),
                     y2_midpoint, center_coord]

        fpl.append(templ)

    return fpl


def sort_polyline_ammar(data):
    all_4_polyline_coords = []
    rect_x = []
    rect_y = []
    frst_t = True
    for i in data:
        if int(i[0]) == 1 and frst_t:
            rect_x.append(int(i[1]))
            rect_y.append(int(i[2]))
            frst_t = False
        elif int(i[0]) != 1:
            rect_x.append(int(i[1]))
            rect_y.append(int(i[2]))
        elif int(i[0]) == 1 and not frst_t:
            xmin, ymin, xmax, ymax = min(rect_x) - 2, min(rect_y) - 2, max(rect_x) + 2, max(rect_y) + 2
            # print(xmin, ymin, xmax, ymax)
            all_4_polyline_coords.append([xmin, ymin, xmax, ymax])
            rect_x.clear()
            rect_y.clear()
            rect_x.append(int(i[1]))
            rect_y.append(int(i[2]))

    if rect_x and rect_y:
        xmin, ymin, xmax, ymax = min(rect_x) - 2, min(rect_y) - 2, max(rect_x) + 2, max(rect_y) + 2

        all_4_polyline_coords.append([xmin, ymin, xmax, ymax])

    return all_4_polyline_coords


def get_spnt(fndlst):
    tl = []
    for i in fndlst: tl.append(i[0])
    stmp_elmnt = min(tl)
    for i in fndlst:
        if stmp_elmnt == i[0]:
            frstv, scndv, ed = i[1], i[2], i[0]
    return frstv, scndv, ed


def get_pnts(flist, slist):
    sml_ed_pnts = []

    if len(flist) == 10:
        flist = flist[:-1]

    if len(slist) == 10:
        slist = slist[:-1]

    # if flist[4][1] < slist[4][1]:
    # print(flist[4], slist[4])

    for i in flist:
        x1 = i[0]
        y1 = i[1]
        tl = []
        for j in slist:
            x2 = j[0]
            y2 = j[1]
            e_dist = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
            tl.append([e_dist, i, j])

        first_val, second_val, ed = get_spnt(tl)
        sml_ed_pnts.append([ed, first_val, second_val])
    # print(sml_ed_pnts)
    fval, sval, ed1 = get_spnt(sml_ed_pnts)
    return fval, sval, ed1


def fnd_text(ply_lst, whole_text_list):
    text = ""
    xmin, ymin, xmax, ymax = ply_lst[0][0], ply_lst[0][1], ply_lst[4][0], ply_lst[4][1]
    for i in whole_text_list:
        txmin, tymax, txmax, tymin = i[0][0], i[0][1], i[4][0], i[4][1]
        if xmin < txmin < xmax and ymin < tymin:
            text = i[9]
            return text
    return text


def Sort_Tuple(tup):
    tup.sort(key=lambda x: x[2])
    return tup


def fnd_rct_re(lst, txt):
    tl = []
    for i in lst:
        if re.findall(".*" + txt + ".*", i[9]):
            if i[9] != 'PROPOSED 3&quot IRRIGATION LINE':
                tl.append(i)
    if len(tl) > 0:
        return tl
    else:
        return None


def section_a_to_z(csv_name, model_path):
    model = tf.keras.models.load_model(model_path)
    image_name = r'E:\dewa\pdfs\GCNN\ClusterGCN\OUTPUT_HOUSE_IRRIGATION\COMPLEX\RTA_ROW_CROSS_SECTION_LAYOUT_SECTION_B_B.png'
    # image_name = 'CROSS_SECTIONS_1B_1B.png'
    image = cv2.imread(image_name)
    # print(image)
    h, w = image.shape[:2]
    data = read_csv(csv_name)
    vsl_insght_lst, txt_lst_, plylin_lst = segregate_whl_dta(data)

    txt_lst = []
    for txts in txt_lst_:
        var = (txts[4].split(";"))
        if len(var) == 3:
            var = (txts[4].split(";")[1:])
            var = "".join(var)
        if len(var) == 2:
            var = (txts[4].split(";")[-1])
        txts[4] = var
        if len(txts[4]) > 2:
            if int(txts[1]) > int(txts[3]):
                txts[1], txts[3] = txts[3], txts[1]
            txt_lst.append(txts)
    # sys.exit()
    txt_pnt_lst = get_pnt_lst(txt_lst)

    # print(image_name)
    proposed_list = fnd_rct_re(txt_pnt_lst, "PROPOSED 3")
    # print(proposed_list)

    irrigation_line_list = fnd_rct_re(txt_pnt_lst, "IRRIGATION LINE")
    # print(irrigation_line_list)

    # sys.exit()
    polyline_4_coords = sort_polyline_ammar(plylin_lst)
    polyline_9_coords = get_pnt_lst(polyline_4_coords)
    # print(polyline_4_coords)

    horizontal_line = []
    vertical_line = []
    all_line_list = []

    for l in polyline_9_coords:
        xmin_to_xmax = math.sqrt((l[0][0] - l[4][0]) ** 2 + (l[0][1] - l[0][1]) ** 2)
        ymin_to_ymax = math.sqrt((l[0][0] - l[0][0]) ** 2 + (l[0][1] - l[4][1]) ** 2)
        if xmin_to_xmax < ymin_to_ymax:
            vertical_line.append(l)
        else:
            horizontal_line.append(l)

    # for i in horizontal_line:
    # print(i)
    # if int(i[0][1]) > int(i[4][1]):
    #     print("ymin is greater than ymax")
    # cv2.rectangle(image, (i[0][0] - 1, i[0][1] - 1), (i[4][0] + 1, i[4][1] + 1), (0, 0, 255), 1)

    # print()
    # print()
    # for i in txt_pnt_lst:
    #     print(i[0], i[7], i[8], i[3], i[9])
    # if int(i[0][1]) > int(i[4][1]):
    #     # print("ymin is greater than ymax")
    #     cv2.rectangle(image, (int(i[0][0]), int(i[4][1])), (int(i[4][0]), int(i[0][1])), (0, 255, 0), 1)
    # else:
    # cv2.rectangle(image, (int(i[0][0]), int(i[0][1])), (int(i[4][0]), int(i[4][1])), (0, 255, 0), 1)

    # cv2.imwrite("final_"+image_name, image)

    # print(txt_pnt_lst)
    only_numbers = []
    only_texts = []
    vertical_numbers = []
    horizontal_numbers = []
    vertical_texts = []
    horizontal_texts = []
    horizontal_line = []
    vertical_line = []

    for l in polyline_9_coords:
        xmin_to_xmax = math.sqrt((l[0][0] - l[4][0]) ** 2 + (l[0][1] - l[0][1]) ** 2)
        ymin_to_ymax = math.sqrt((l[0][0] - l[0][0]) ** 2 + (l[0][1] - l[4][1]) ** 2)
        if xmin_to_xmax < ymin_to_ymax:
            vertical_line.append(l)
        else:
            horizontal_line.append(l)

    for text in txt_pnt_lst:
        try:
            num = float(text[9])
            only_numbers.append(text)
            xmin_to_xmax = math.sqrt((text[0][0] - text[4][0]) ** 2 + (text[0][1] - text[0][1]) ** 2)
            ymin_to_ymax = math.sqrt((text[0][0] - text[0][0]) ** 2 + (text[0][1] - text[4][1]) ** 2)
            if xmin_to_xmax < ymin_to_ymax:
                vertical_numbers.append(text)
            else:
                horizontal_numbers.append(text)
        except:
            only_texts.append(text)
            xmin_to_xmax = math.sqrt((text[0][0] - text[4][0]) ** 2 + (text[0][1] - text[0][1]) ** 2)
            ymin_to_ymax = math.sqrt((text[0][0] - text[0][0]) ** 2 + (text[0][1] - text[4][1]) ** 2)
            if xmin_to_xmax < ymin_to_ymax:
                vertical_texts.append(text)
            else:
                horizontal_texts.append(text)

    # print(proposed_list)
    if horizontal_numbers and vertical_numbers and proposed_list and irrigation_line_list:
        red_horizontal_numbers, red_vertical_numbers = get_red_strings(image, horizontal_numbers, vertical_numbers,
                                                                       proposed_list, irrigation_line_list)

        # print(len(vertical_texts))

        for i in proposed_list:
            for j in only_texts:
                if i[0] == j[0] and i[4] == j[4]:
                    only_texts.remove(j)

        for i in irrigation_line_list:
            for j in only_texts:
                if i[0] == j[0] and i[4] == j[4]:
                    only_texts.remove(j)

        # print(len(vertical_texts))

        for rhn in red_horizontal_numbers:
            for hn in horizontal_numbers:
                if rhn[0] == hn[0] and rhn[4] == hn[4]:
                    horizontal_numbers.remove(hn)

        for vhn in red_vertical_numbers:
            for vn in vertical_numbers:
                if vhn[0] == vn[0] and vhn[4] == vn[4]:
                    vertical_numbers.remove(vn)

    # print(horizontal_texts)
    # print(vertical_texts)
    # print(horizontal_numbers)
    # print(vertical_numbers)
    # print(horizontal_line)
    # print(vertical_line)

    connection_list = []

    for text in only_texts:
        for hline in horizontal_line:
            for num in only_numbers:
                if text[0][1] > hline[0][1] > num[0][1] and text[0][0] > hline[0][0] < num[0][0]:

                    xmin, ymin, x, y, xmax, ymax, x1min, y1min, x1, y1, x1max, y1max, x2min, y2min, x2, y2, x2max, y2max = \
                        int(text[7][0]), int(text[7][1]), int(text[8][0]), int(text[8][1]), int(text[3][0]), int(
                            text[3][1]), \
                        int(hline[7][0]), int(hline[7][1]), int(hline[8][0]), int(hline[8][1]), int(hline[3][0]), int(
                            hline[3][1]), \
                        int(num[7][0]), int(num[7][1]), int(num[8][0]), int(num[8][1]), int(num[3][0]), int(num[3][1])

                    xmin, ymin, x, y, xmax, ymax, x1min, y1min, x1, y1, x1max, y1max, x2min, y2min, x2, y2, x2max, y2max = xmin / w, ymin / h, x / w, y / h, xmax / w, ymax / h, x1min / w, y1min / h, x1 / w, y1 / h, x1max / w, y1max / h, x2min / w, y2min / h, x2 / w, y2 / h, x2max / w, y2max / h

                    xmin, ymin, x, y, xmax, ymax, x1min, y1min, x1, y1, x1max, y1max, x2min, y2min, x2, y2, x2max, y2max = '{:.2f}'.format(
                        xmin), '{:.2f}'.format(ymin), '{:.2f}'.format(x), '{:.2f}'.format(y), '{:.2f}'.format(
                        xmax), '{:.2f}'.format(ymax), '{:.2f}'.format(x1min), '{:.2f}'.format(y1min), '{:.2f}'.format(
                        x1), '{:.2f}'.format(y1), '{:.2f}'.format(x1max), '{:.2f}'.format(y1max), '{:.2f}'.format(
                        x2min), '{:.2f}'.format(y2min), '{:.2f}'.format(x2), '{:.2f}'.format(y2), '{:.2f}'.format(
                        x2max), '{:.2f}'.format(y2max)

                    xmin, ymin, x, y, xmax, ymax, x1min, y1min, x1, y1, x1max, y1max, x2min, y2min, x2, y2, x2max, y2max = float(
                        xmin), float(ymin), float(x), float(y), float(xmax), float(ymax), float(x1min), float(
                        y1min), float(
                        x1), float(y1), float(x1max), float(y1max), float(x2min), float(y2min), float(x2), float(
                        y2), float(
                        x2max), float(y2max)

                    data_list = \
                        [[xmin, ymin, x, y, xmax, ymax, x1min, y1min, x1, y1, x1max, y1max, x2min, y2min, x2, y2, x2max,
                          y2max]]

                    data_list = np.array(data_list)

                    predictions = model.predict_classes(data_list)

                    if predictions[0][0] == 1:
                        # print("prediction:", 1)
                        connection_list.append([text, hline, num])
                        print(text[9])
                        cv2.rectangle(image, (text[0][0] - 1, text[0][1] - 1), (text[4][0] + 1, text[4][1] + 1),
                                      (0, 0, 255), 1)
                        cv2.rectangle(image, (hline[0][0] - 1, hline[0][1] - 1), (hline[4][0] + 1, hline[4][1] + 1),
                                      (0, 0, 255), 1)
                        cv2.rectangle(image, (num[0][0] - 1, num[0][1] - 1), (num[4][0] + 1, num[4][1] + 1),
                                      (0, 0, 255), 1)
                        cv2.line(image, text[8], hline[8], (0, 255, 255), 2)
                        cv2.line(image, hline[8], num[8], (0, 255, 255), 2)
                        cv2.imwrite("connection_by_cnn1.jpg", image)

    print(connection_list)


section_a_to_z(
    r'E:\dewa\pdfs\GCNN\ClusterGCN\OUTPUT_HOUSE_IRRIGATION\COMPLEX\RTA_ROW_CROSS_SECTION_LAYOUT_SECTION_B_B.csv',
    r'checkpoints\model-429-0.10')

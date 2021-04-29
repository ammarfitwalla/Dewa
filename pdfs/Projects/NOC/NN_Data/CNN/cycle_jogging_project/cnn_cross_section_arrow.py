import cv2
import math
import re
import sys
# from prettytable import PrettyTable
import numpy as np
# import silence_tensorflow
# silence_tensorflow.silence_tensorflow()
import tensorflow as tf
# from find_red_section import get_red_strings
from glob import glob
import os
from pathlib import Path
import csv


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


def average(lst):
    return sum(lst) / len(lst)


def section_a_to_z(csv_name, model_path):
    model = tf.keras.models.load_model(model_path)
    image_name = r'D:\KS\Projects\Dewa\pdfs\Projects\NOC\OUTPUT_CycleJogging_Projects\Design\Akram\CrossSections_and_markers-8.png'
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
    # if horizontal_numbers and vertical_numbers and proposed_list and irrigation_line_list:
    #     red_horizontal_numbers, red_vertical_numbers = get_red_strings(image, horizontal_numbers, vertical_numbers,
    #                                                                    proposed_list, irrigation_line_list)
    #
    #     # print(len(vertical_texts))
    #
    #     for i in proposed_list:
    #         for j in only_texts:
    #             if i[0] == j[0] and i[4] == j[4]:
    #                 only_texts.remove(j)
    #
    #     for i in irrigation_line_list:
    #         for j in only_texts:
    #             if i[0] == j[0] and i[4] == j[4]:
    #                 only_texts.remove(j)
    #
    #     # print(len(vertical_texts))
    #
    #     for rhn in red_horizontal_numbers:
    #         for hn in horizontal_numbers:
    #             if rhn[0] == hn[0] and rhn[4] == hn[4]:
    #                 horizontal_numbers.remove(hn)
    #
    #     for vhn in red_vertical_numbers:
    #         for vn in vertical_numbers:
    #             if vhn[0] == vn[0] and vhn[4] == vn[4]:
    #                 vertical_numbers.remove(vn)

    # print(horizontal_texts)
    # print(vertical_texts)
    # print(horizontal_numbers)
    # print(vertical_numbers)
    # print(horizontal_line)
    # print(vertical_line)

    """
    Finding the arrow line using the numbers 
    """
    num_line_final = []
    counter = 0
    for h_num in horizontal_numbers:
        h_num_to_line_list = []
        for line in horizontal_line:

            if line[4][1] > h_num[4][1]:  # checking if the line is below the number
                # print("line[4][1] > h_num[4][1] -", line[4][1] , h_num[4][1])
                for n in horizontal_numbers:
                    if n[0] != h_num[0] and line[8][1] > n[8][1] > h_num[8][1] and line[0][0] < n[0][0] and line[4][0] > \
                            n[4][0]:
                        counter += 1

                if counter == 0:
                    h_num_pt, line_pt, ed = get_pnts(h_num, line)
                    dist = math.sqrt((h_num_pt[0] - line_pt[0]) ** 2 + (h_num_pt[1] - line_pt[1]) ** 2)
                    if dist < 40:
                        h_num_to_line_list.append([h_num, line, ed, h_num_pt, line_pt])

            counter = 0

        if h_num_to_line_list:
            closest_1 = Sort_Tuple(h_num_to_line_list)[0]
            num_line_final.append(closest_1)

            # cv2.line(image, (closest_1[-2]), closest_1[-1], (255, 0, 0), 2)
            # cv2.rectangle(image, closest_1[1][0], closest_1[1][4], (0, 255, 0), 1)

            xmin, ymin, xmax, ymax = 0, 0, 0, 0
            #
            # [0][0] = xmin
            # [0][1] = ymin
            # [4][0] = xmax
            # [4][1] = ymax
            number = closest_1[0]
            # print(number)
            pt_list = closest_1[1]
            point_1 = closest_1[3]
            point_2 = closest_1[4]

            cl_list = []
            cl_list2 = []
            x_list = []
            y_list = []

            if (pt_list[0][0] < number[0][0] and pt_list[4][0] < number[4][0]) or (
                    pt_list[0][0] > number[0][0] and pt_list[4][0] > number[4][
                0]):  # condition to check if the line is right or left to number

                cv2.rectangle(image, pt_list[0], pt_list[4], (255, 0, 0), 2)

                if pt_list[0][0] < number[0][0]:  # left line
                    for hl in horizontal_line:
                        if hl[0] != pt_list[0] and pt_list[0][0] - 2 < hl[0][0]:
                            # if pt_list[0][0] < number[0][0] and number[4][0] > pt_list[4][0]:
                            #     print(pt_list[0][0] , number[0][0], number[4][0] , pt_list[4][0])
                            pt1, hl_pt, ed = get_pnts(pt_list, hl)
                            cl_list.append([pt_list, hl, ed])
                else:  # right lline
                    for hl in horizontal_line:
                        if hl[0] != pt_list[0] and pt_list[4][0] + 2 > hl[4][0]:
                            # if pt_list[0][0] < number[0][0] and number[4][0] > pt_list[4][0]:
                            #     print(pt_list[0][0] , number[0][0], number[4][0] , pt_list[4][0])
                            pt1, hl_pt, ed = get_pnts(pt_list, hl)
                            cl_list.append([pt_list, hl, ed])

                close_1 = Sort_Tuple(cl_list)[0]
                # print(close_1[1])
                # sys.exit()

                for hl1 in horizontal_line:
                    if close_1[1][0] != hl1[0] != pt_list[0] and close_1[1][4] != hl1[4] != pt_list[4]:
                        # print(close_1[1])
                        # print(hl1)
                        # print(pt_list)
                        # print()
                        # if pt_list[0][0] < number[0][0] and number[4][0] > pt_list[4][0]:
                        #     print(pt_list[0][0] , number[0][0], number[4][0] , pt_list[4][0])
                        pt1, hl_pt, ed = get_pnts(close_1[1], hl1)
                        cl_list2.append([close_1[1], hl1, ed])
                # sys.exit()
                close_2 = Sort_Tuple(cl_list2)[0]

                # print(type(close_1))
                # print(type(close_2))
                # print(pt_list)
                # print(close_1[1])
                # print(close_2[1])
                # print()
                # sys.exit()
                x_list.append(pt_list[0][0])
                x_list.append(pt_list[4][0])

                x_list.append(close_1[1][0][0])
                x_list.append(close_1[1][4][0])

                x_list.append(close_2[1][0][0])
                x_list.append(close_2[1][4][0])

                y_list.append(pt_list[0][1])
                y_list.append(pt_list[4][1])

                y_list.append(close_1[1][0][1])
                y_list.append(close_1[1][4][1])

                y_list.append(close_2[1][0][1])
                y_list.append(close_2[1][4][1])
            else:
                for hl in horizontal_line:
                    if hl[0] != pt_list[0]:
                        # if pt_list[0][0] < number[0][0] and number[4][0] > pt_list[4][0]:
                        #     print(pt_list[0][0] , number[0][0], number[4][0] , pt_list[4][0])
                        pt1, hl_pt, ed = get_pnts(pt_list, hl)

                        cl_list.append([pt_list, hl, ed])
                close_1 = Sort_Tuple(cl_list)[:2]

                if close_1:
                    for i in close_1:
                        for j in i:
                            if type(j) != float:
                                # print(pt1, hl_pt, ed,j)
                                x_list.append(j[0][0])
                                x_list.append(j[4][0])
                                y_list.append(j[0][1])
                                y_list.append(j[4][1])

            xmin, ymin, xmax, ymax = (min(x_list)), (min(y_list)), (max(x_list)), (max(y_list))
            cv2.rectangle(image, (xmin, ymin), (xmax, ymax), (0, 0, 255), 2)

            line_coords = get_pnt_lst([[xmin, ymin, xmax, ymax]])
            line_coords = [e for sl in line_coords for e in sl]
            all_line_list.append(line_coords)

    """
    Final prediction using model
    """

    connection_list = []
    all_hline_to_num_ed_list = []
    all_text_to_hline_ed_list = []
    for text in only_texts:
        for hline in all_line_list:
            if text[0][0] > hline[0][0] and text[4][0] < hline[4][0] and text[0][1] > hline[0][1]:
                for num in only_numbers:
                    if num[0][0] > hline[0][0] and num[4][0] < hline[4][0] and num[0][1] < hline[0][1]:
                        xmin, ymin, x, y, xmax, ymax, x1min, y1min, x1, y1, x1max, y1max, x2min, y2min, x2, y2, x2max, y2max = \
                            round(text[7][0] / w, 2), round(text[7][1] / h, 2), \
                            round(text[8][0] / w, 2), round(text[8][1] / h, 2), \
                            round(text[3][0] / w, 2), round(text[3][1] / h, 2), \
                            round(hline[7][0] / w, 2), round(hline[7][1] / h, 2), \
                            round(hline[8][0] / w, 2), round(hline[8][1] / h, 2), \
                            round(hline[3][0] / w, 2), round(hline[3][1] / h, 2), \
                            round(num[7][0] / w, 2), round(num[7][1] / h, 2), \
                            round(num[8][0] / w, 2), round(num[8][1] / h, 2), \
                            round(num[3][0] / w, 2), round(num[3][1] / h, 2)

                        data_list = \
                            [[xmin, ymin, x, y, xmax, ymax, x1min, y1min, x1, y1, x1max, y1max, x2min, y2min, x2, y2,
                              x2max,
                              y2max]]

                        data_list = np.array(data_list)
                        conf = model.predict(data_list)
                        print(conf)
                        # sys.exit()
                        predictions = model.predict_classes(data_list)

                        if predictions[0][0] == 1:
                            text_to_hline_e_dist = math.sqrt(
                                (text[8][0] - hline[8][0]) ** 2 + (text[8][1] - hline[8][1]) ** 2)
                            hline_to_num_e_dist = math.sqrt(
                                (hline[8][0] - num[8][0]) ** 2 + (hline[8][1] - num[8][1]) ** 2)
                            text_to_num = math.sqrt(
                                (text[8][0] - num[8][0]) ** 2 + (text[8][1] - num[8][1]) ** 2)
                            all_text_to_hline_ed_list.append(text_to_hline_e_dist)
                            all_hline_to_num_ed_list.append(hline_to_num_e_dist)
                            connection_list.append([text, hline, num, text_to_num, conf])
            else:
                print("line below text")
    avg_text_to_hline = average(all_text_to_hline_ed_list)
    avg_hline_to_num = average(all_hline_to_num_ed_list)
    # print(len(connection_list))
    # connection_list = [e for e in connection_list if e[4] < avg_hline_to_num and e[3] < avg_text_to_hline]
    # connection_list = [e for e in connection_list if e[3] < avg_text_to_hline]
    # print(len(connection_list))
    csv_filename = '../model_18pts_data.csv'
    # if not os.path.isfile(csv_filename):
    #     print("new csv file created")
    #     with open(csv_filename, 'w') as csv_file:
    #         csv_file = csv.writer(csv_file)
    #         csv_file.writerow(
    #             ['xmin', 'ymin', 'x', 'y', 'xmax', 'ymax', 'x1min', 'y1min', 'x1', 'y1', 'x1max', 'y1max', 'x2min',
    #              'y2min',
    #              'x2', 'y2', 'x2max', 'y2max', 'output'])

    for i in connection_list:
        cv2.rectangle(image, (i[0][0][0], i[0][0][1]), (i[0][4][0], i[0][4][1]), (255, 0, 0), 2)
        cv2.rectangle(image, (i[1][0][0], i[1][0][1]), (i[1][4][0], i[1][4][1]), (255, 0, 0), 2)
        cv2.rectangle(image, (i[2][0][0], i[2][0][1]), (i[2][4][0], i[2][4][1]), (255, 0, 0), 2)
        cv2.line(image, i[0][8], i[1][8], (0, 255, 0), 2)
        cv2.line(image, i[1][8], i[2][8], (0, 255, 0), 2)


    # img_copy = image.copy()
    # cv2.rectangle(img_copy, (i[0][0][0], i[0][0][1]), (i[0][4][0], i[0][4][1]), (255, 0, 0), 2)
    # cv2.rectangle(img_copy, (i[1][0][0], i[1][0][1]), (i[1][4][0], i[1][4][1]), (255, 0, 0), 2)
    # cv2.rectangle(img_copy, (i[2][0][0], i[2][0][1]), (i[2][4][0], i[2][4][1]), (255, 0, 0), 2)
    # cv2.line(img_copy, i[0][8], i[1][8], (0, 255, 0), 2)
    # cv2.line(img_copy, i[1][8], i[2][8], (0, 255, 0), 2)
    # tk_xmin, tk_ymin, tk_xmax, tk_ymax = i[1][0][0] - 5, i[2][0][1] - 5, i[1][4][0] + 5, i[0][4][1] + 5
    # cropped_img = img_copy[tk_ymin: tk_ymax, tk_xmin: tk_xmax]
    # # if cropped_img.shape[0] > cropped_img.shape[1]:
    # cropped_img = cv2.resize(cropped_img, (cropped_img.shape[1] - 10, cropped_img.shape[0] - 10))
    # cv2.imshow("winname", cropped_img)
    #
    # if cv2.waitKey(0) & 0xFF == ord('y'):
    #     print("yes")
    #     with open(csv_filename, 'a', newline='') as csv_file:
    #         writer = csv.writer(csv_file)
    #         writer.writerow(
    #             [str(round(i[0][7][0] / w, 2)), str(round(i[0][7][1] / h, 2)), str(round(i[0][8][0] / w, 2)),
    #              str(round(i[0][8][1] / h, 2)),
    #              str(round(i[0][3][0] / w, 2)), str(round(i[0][3][1] / h, 2)),
    #              str(round(i[1][7][0] / w, 2)), str(round(i[1][7][1] / h, 2)), str(round(i[1][8][0] / w, 2)),
    #              str(round(i[1][8][1] / h, 2)),
    #              str(round(i[1][3][0] / w, 2)), str(round(i[1][3][1] / h, 2)),
    #              str(round(i[2][7][0] / w, 2)), str(round(i[2][7][1] / h, 2)), str(round(i[2][8][0] / w, 2)),
    #              str(round(i[2][8][1] / h, 2)),
    #              str(round(i[2][3][0] / w, 2)), str(round(i[2][3][1] / h, 2)),
    #              str(1)])
    # else:
    #     print("no")
    #     with open(csv_filename, 'a', newline='') as csv_file:
    #         writer = csv.writer(csv_file)
    #         writer.writerow(
    #             [str(round(i[0][7][0] / w, 2)), str(round(i[0][7][1] / h, 2)), str(round(i[0][8][0] / w, 2)),
    #              str(round(i[0][8][1] / h, 2)),
    #              str(round(i[0][3][0] / w, 2)), str(round(i[0][3][1] / h, 2)),
    #              str(round(i[1][7][0] / w, 2)), str(round(i[1][7][1] / h, 2)), str(round(i[1][8][0] / w, 2)),
    #              str(round(i[1][8][1] / h, 2)),
    #              str(round(i[1][3][0] / w, 2)), str(round(i[1][3][1] / h, 2)),
    #              str(round(i[2][7][0] / w, 2)), str(round(i[2][7][1] / h, 2)), str(round(i[2][8][0] / w, 2)),
    #              str(round(i[2][8][1] / h, 2)),
    #              str(round(i[2][3][0] / w, 2)), str(round(i[2][3][1] / h, 2)),
    #              str(0)])
    cv2.imwrite("../connection_by_cnn7.jpg", image)

    return connection_list


# current_dir = os.getcwd()
# PROJECT_NAME = (current_dir.split("\\")[-1])
# print(PROJECT_NAME)
#
# all_sub_dir_paths = glob(str(current_dir) + '/*/')  # returns list of sub directory paths
#
# all_sub_dir_names = [Path(sub_dir).name for sub_dir in all_sub_dir_paths if Path(sub_dir).name == 'Design']
# print(all_sub_dir_names)
# print()
#
# uid = 0
#
#
# with open("graphdb_csv/noc_entity.csv", "w", newline='') as entity_csv:
#     writer = csv.writer(entity_csv)
#     writer.writerow(["uid", "parent", "type", "description", "xmin", "ymin", "xmax", "ymax"])
#     writer.writerow(
#         [uid, "None", "project", PROJECT_NAME, "None", "None", "None", "None"])
#     uid += 1
#
#
# entity_csv_parent = read_csv('graphdb_csv/noc_entity.csv')
#
# for i in all_sub_dir_names:
#     with open("graphdb_csv/noc_entity.csv", "a") as entity_csv:
#         writer = csv.writer(entity_csv)
#         for pname in entity_csv_parent:
#             if pname[3] == PROJECT_NAME:
#                 writer.writerow(
#                     [uid, pname[0], "file", i, "None", "None", "None", "None"])
#                 uid += 1
# entity_csv_ = read_csv('graphdb_csv/noc_entity.csv')
# # print(entity_csv_)
#
# for dir_ in all_sub_dir_names:
#     all_csvs = glob(str(dir_) + "/*.csv")
#     for ac in all_csvs:
#         ac_name = ac.split("\\")[-1]
#         ac_dir = ac.split("\\")[-2]
#         dname_id = [i[0] for i in entity_csv_ if i[3] == ac_dir]
#
#         with open("graphdb_csv/noc_entity.csv", "a") as entity_csv:
#             writer = csv.writer(entity_csv)
#             writer.writerow(
#                 [uid, dname_id[0], "document", ac_name, "None", "None", "None", "None"])
#             uid += 1
#
# entity_csv_ = read_csv('graphdb_csv/noc_entity.csv')
#
# # print(entity_csv_)
#
# with open("graphdb_csv/noc_parent_child.csv", "w") as pccsv:
#     writer = csv.writer(pccsv)
#     writer.writerow(["parent", "child", "confidence"])
#
# with open("graphdb_csv/noc_relation.csv", "w") as ed_rel:
#     writer = csv.writer(ed_rel)
#     writer.writerow(["entity1", "entity2", "eDistance", "confidence"])
# temp_id = uid


# section_a_to_z(
#     r'D:\KS\Projects\Dewa\pdfs\Projects\NOC\OUTPUT_CycleJogging_Projects\Design\Akram\CrossSections_and_markers-8.csv',
#     r'D:\KS\Projects\Dewa\pdfs\Projects\NOC\NN_Data\CNN\checkpoints_custom\model-246-0.02')

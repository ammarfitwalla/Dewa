import cv2
import csv
import sys
import numpy as np
import math


def get_pnt_lst(data):
    fpl = []
    for i in data:
        # print(len(i))
        xmin, ymin, xmax, ymax = int(i[0]), int(i[1]), int(i[2]), int(i[3])

        x1_midpoint = ((xmin + xmax) // 2, (ymin + ymin) // 2)
        x2_midpoint = ((xmin + xmax) // 2, (ymax + ymax) // 2)
        y1_midpoint = ((xmin + xmin) // 2, (ymin + ymax) // 2)
        y2_midpoint = ((xmax + xmax) // 2, (ymin + ymax) // 2)

        center_coord = int((xmin + xmax) // 2), int((ymin + ymax) // 2)

        if len(i) == 5:
            templ = [(xmin, ymin), x1_midpoint, (xmax, ymin), y1_midpoint, (xmax, ymax), x2_midpoint, (xmin, ymax),
                     y2_midpoint, center_coord, i[len(i) - 1].split(";")[-1]]
        else:
            templ = [(xmin, ymin), x1_midpoint, (xmax, ymin), y1_midpoint, (xmax, ymax), x2_midpoint, (xmin, ymax),
                     y2_midpoint, center_coord]

        fpl.append(templ)

    return fpl


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


def Sort_Tuple(tup):
    tup.sort(key=lambda x: x[2])
    return tup


image_name = r'E:\dewa\pdfs\GCNN\ClusterGCN\OUTPUT_HOUSE_IRRIGATION\COMPLEX\RTA_ROW_CROSS_SECTION_LAYOUT_SECTION_A_A.png'
image = cv2.imread(image_name)

p_list = [
    [(4070, 1130), (4182, 1130), (4295, 1130), (4070, 1117), (4295, 1105), (4182, 1105), (4070, 1105), (4295, 1117),
     (4182, 1117), 'PROPOSED 3&quot'],
    [(97, 1130), (209, 1130), (321, 1130), (97, 1117), (321, 1105), (209, 1105), (97, 1105), (321, 1117), (209, 1117),
     'PROPOSED 3&quot'],
    [(3706, 2244), (3930, 2244), (4155, 2244), (3706, 2219), (4155, 2195), (3930, 2195), (3706, 2195), (4155, 2219),
     (3930, 2219), 'PROPOSED 3&quot'],
    [(252, 2249), (477, 2249), (702, 2249), (252, 2224), (702, 2200), (477, 2200), (252, 2200), (702, 2224),
     (477, 2224), 'PROPOSED 3&quot']]
i_list = [
    [(4070, 1173), (4206, 1173), (4343, 1173), (4070, 1161), (4343, 1149), (4206, 1149), (4070, 1149), (4343, 1161),
     (4206, 1161), 'IRRIGATION LINE'],
    [(49, 1173), (185, 1173), (322, 1173), (49, 1161), (322, 1149), (185, 1149), (49, 1149), (322, 1161), (185, 1161),
     'IRRIGATION LINE'],
    [(3706, 2332), (3979, 2332), (4252, 2332), (3706, 2307), (4252, 2282), (3979, 2282), (3706, 2282), (4252, 2307),
     (3979, 2307), 'IRRIGATION LINE'],
    [(158, 2337), (431, 2337), (704, 2337), (158, 2312), (704, 2288), (431, 2288), (158, 2288), (704, 2312),
     (431, 2312), 'IRRIGATION LINE'],
    [(4529, 105), (4704, 105), (4879, 105), (4529, 96), (4879, 88), (4704, 88), (4529, 88), (4879, 96), (4704, 96),
     'IRRIGATION LINE'],
    [(2736, 3360), (3244, 3360), (3753, 3360), (2736, 3335), (3753, 3311), (3244, 3311), (2736, 3311), (3753, 3335),
     (3244, 3335), ' IRRIGATION LINE'],
    [(650, 3360), (1159, 3360), (1668, 3360), (650, 3335), (1668, 3311), (1159, 3311), (650, 3311), (1668, 3335),
     (1159, 3335), ' IRRIGATION LINE']]

horizontal_numbers_4_pts = [['248', '1231', '314', '1204', '\W1.001125;1.50'],
                            ['553', '2451', '684', '2397', '\W1.001125;1.50'],
                            ['3256', '2406', '3386', '2352', '\W1.001125;1.50'],
                            ['3843', '1211', '3908', '1184', '\W1.001125;1.50'],
                            ['3329', '1225', '3355', '1162', '\W1.001125;1.20]']]
vertical_numbers_4_pts = [['3693', '1079', '3717', '1020', '\W1.001125;1.00'],
                          ['619', '1079', '643', '1020', '\W1.001125;1.00'],
                          ['1285', '1520', '1340', '1497', '\W1.001125;1.00'],
                          ['2957', '2145', '3005', '2027', '\W1.001125;1.00'],
                          ['1287', '2150', '1335', '2032', '\W1.001125;1.00']]

horizontal_numbers_9_pts = get_pnt_lst(horizontal_numbers_4_pts)
vertical_numbers_9_pts = get_pnt_lst(vertical_numbers_4_pts)

# print(red_horizontal_numbers_9_pts)
# print(red_vertical_numbers_9_pts)


def get_red_strings(image, horizontal_numbers_9_pts, vertical_numbers_9_pts, proposed_list, irrigation_line_list):

    red_horizontal_numbers = []
    red_vertical_numbers = []

    for h_n in horizontal_numbers_9_pts:
        xmin, ymin, xmax, ymax = h_n[0][0], h_n[0][1], h_n[4][0], h_n[4][1]
        if ymin > ymax:
            ymin, ymax = ymax, ymin
        crop_img = image[ymin - 2:ymax + 2, xmin - 2:xmax + 2]
        h, w, c = crop_img.shape
        lower_red = 200
        higher_red = 255
        counter = 0
        for i in range(h):
            for j in range(w):
                color = crop_img[i, j]
                if color[1] == 0 and lower_red < color[2] <= higher_red:
                    counter += 1
        if counter > 300:
            # print(h_n)
            red_horizontal_numbers.append(h_n)

    # print()

    for v_n in vertical_numbers_9_pts:
        xmin, ymin, xmax, ymax = v_n[0][0], v_n[0][1], v_n[4][0], v_n[4][1]
        if ymin > ymax:
            ymin, ymax = ymax, ymin
        crop_img = image[ymin - 2:ymax + 2, xmin - 2:xmax + 2]
        h, w, c = crop_img.shape
        lower_red = 220
        higher_red = 255
        counter = 0
        for i in range(h):
            for j in range(w):
                color = crop_img[i, j]
                if color[1] == 0 and lower_red < color[2] <= higher_red:
                    counter += 1
        if counter > 300:
            # print(v_n)
            red_vertical_numbers.append(v_n)

    for r_h_n in red_horizontal_numbers:

        rhn_pl_list = []
        for pl in proposed_list:
            rhn_pt, pl_pt, ed = get_pnts(r_h_n, pl)
            rhn_pl_list.append([r_h_n, pl, ed, rhn_pt, pl_pt])

        close_rhn_pl = Sort_Tuple(rhn_pl_list)[0]
        # cv2.line(image, close_rhn_pl[3], close_rhn_pl[4], (0, 255, 0), 3)

        rhn_il_list = []
        for il in irrigation_line_list:
            rhn1_pt, il_pt, ed_ = get_pnts(r_h_n, il)
            rhn_il_list.append([r_h_n, il, ed_, rhn1_pt, il_pt])

        close_rhn_il = Sort_Tuple(rhn_il_list)[0]
        # print(close_rhn_il)
        # cv2.line(image, close_rhn_il[3], close_rhn_il[4], (0, 255, 0), 3)

    for v_h_n in red_vertical_numbers:
        vhn_pl_list = []
        for pl in proposed_list:
            vhn_pt, pl_pt, ed = get_pnts(v_h_n, pl)
            vhn_pl_list.append([v_h_n, pl, ed, vhn_pt, pl_pt])

        close_vhn_pl = Sort_Tuple(vhn_pl_list)[0]
        # cv2.line(image, close_vhn_pl[3], close_vhn_pl[4], (0, 255, 0), 3)

        vhn_il_list = []
        for il in irrigation_line_list:
            vhn1_pt, il_pt, ed_ = get_pnts(v_h_n, il)
            vhn_il_list.append([v_h_n, il, ed_, vhn1_pt, il_pt])

        close_vhn_il = Sort_Tuple(vhn_il_list)[0]
        # cv2.line(image, close_vhn_il[3], close_vhn_il[4], (0, 255, 0), 3)

    # cv2.imwrite("red_color_test.jpg", image)
    return red_horizontal_numbers, red_vertical_numbers

import csv
import re
import math
import sys

CONSOLIDATED_CSV = "sld_25_consolidated.csv"
LINKAGE_CSV = "25_5000_func_rel_v1.csv"

global vals
vals = {"0": "FEEDER", "1": "CONNECTOR", "2": "TP", "3": "STP", "4": "EP"}
uid = 0


def read_csv(file):
    data = []
    with open(file, "r") as fo:
        reader = csv.reader(fo)
        for i in reader:
            if i: data.append(i)
    return data


def segregate_whl_dta(data):
    vi, txt, pllin = True, False, False
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
            txtl.append([d[3], d[4], d[5], d[6], d[7]])

        elif pllin:
            pllinl.append([d[0], d[1], d[2]])
    return vil, txtl, pllinl


def fnd_rct(sym, lst):
    return [x for x in lst if int(x[9]) == sym]


def get_pnt_lst(data):
    fpl = []
    for i in data:
        xmin, ymin, xmax, ymax = int(i[0]), int(i[1]), int(i[2]), int(i[3])

        x1_midpoint = ((xmin + xmax) // 2, (ymin + ymin) // 2)
        x2_midpoint = ((xmin + xmax) // 2, (ymax + ymax) // 2)
        y1_midpoint = ((xmin + xmin) // 2, (ymin + ymax) // 2)
        y2_midpoint = ((xmax + xmax) // 2, (ymin + ymax) // 2)

        center_coord = int((xmin + xmax) // 2), int((ymin + ymax) // 2)

        templ = [(xmin, ymin), x1_midpoint, (xmax, ymin), y1_midpoint, (xmax, ymax), x2_midpoint, (xmin, ymax),
                 y2_midpoint, center_coord, i[len(i) - 1]]
        fpl.append(templ)

    return fpl


def get_spnt(fndlst):
    tl = []
    for i in fndlst: tl.append(i[0])
    stmp_elmnt = min(tl)
    for i in fndlst:
        if stmp_elmnt == i[0]: frstv, scndv, ed = i[1], i[2], i[0]
    return frstv, scndv, ed


def get_pnts_from_point(pnt, lst):
    lst = lst[:-1]
    x1, y1 = pnt
    tl = []

    for i in lst:
        x2 = i[0]
        y2 = i[1]
        e_dist = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
        tl.append([e_dist, pnt, i])

    alist = sorted(tl, key=lambda x: x[0])
    return alist[0]


def get_pnts(flist, slist):
    sml_ed_pnts = []
    flist = flist[:-1]
    slist = slist[:-1]

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
    fval, sval, ed1 = get_spnt(sml_ed_pnts)
    return fval, sval, ed1


def rem_and_min_ed(ed_lst, frst_val, scnd_val, ed, fndn_lst):
    for i in ed_lst:
        if frst_val in i and scnd_val in i and ed in i: ed_lst.remove(i)

    frst, scnd, new_ed = get_spnt(ed_lst)
    rect = []
    for i in fndn_lst:
        if scnd in i: rect = i.copy()
    rect.append(frst);
    rect.append(scnd);
    rect.append(new_ed)
    return rect, ed_lst, frst, scnd, new_ed


def get_custom_min_ed(trgt_rct, fndn_lst):
    ed_lst = []
    for i in fndn_lst:
        if i == trgt_rct: continue
        frst_pnt, scnd_pnt, ed = get_pnts(trgt_rct, i)
        ed_lst.append([ed, frst_pnt, scnd_pnt])

    frst_val, scnd_val, ed = get_spnt(ed_lst)

    rect1 = []
    for i in fndn_lst:
        if scnd_val in i: rect1 = i.copy()

    rect1.append(frst_val);
    rect1.append(scnd_val);
    rect1.append(ed)
    rect2, ed_lst, frst_val, scnd_val, ed = rem_and_min_ed(ed_lst, frst_val, scnd_val, ed, fndn_lst)
    rect3, ed_lst, frst_val, scnd_val, ed = rem_and_min_ed(ed_lst, frst_val, scnd_val, ed, fndn_lst)
    rect4, ed_lst, frst_val, scnd_val, ed = rem_and_min_ed(ed_lst, frst_val, scnd_val, ed, fndn_lst)
    return [rect1, rect2, rect3, rect4]


def get_min_ed_with_point(pnt, lst):
    tl = []
    for i in lst:
        ed, first, second = get_pnts_from_point(pnt, i)
        tl.append([ed, first, second])

    tmplst = sorted(tl, key=lambda i: i[0])[0]
    return tmplst


def get_min_ed(trgt_rct, fndn_lst):
    ed_lst = []
    for i in fndn_lst:
        if i == trgt_rct: continue
        frst_pnt, scnd_pnt, ed = get_pnts(trgt_rct, i)
        ed_lst.append([ed, frst_pnt, scnd_pnt])

    frst_val, scnd_val, ed = get_spnt(ed_lst)

    rect1 = []
    for i in fndn_lst:
        if scnd_val in i: rect1 = i.copy()

    rect1.append(frst_val);
    rect1.append(scnd_val);
    rect1.append(ed)
    rect2, ed_lst, frst_val, scnd_val, ed = rem_and_min_ed(ed_lst, frst_val, scnd_val, ed, fndn_lst)
    rect3, ed_lst, frst_val, scnd_val, ed = rem_and_min_ed(ed_lst, frst_val, scnd_val, ed, fndn_lst)
    rect4, ed_lst, frst_val, scnd_val, ed = rem_and_min_ed(ed_lst, frst_val, scnd_val, ed, fndn_lst)
    rect5, ed_lst, frst_val, scnd_val, ed = rem_and_min_ed(ed_lst, frst_val, scnd_val, ed, fndn_lst)
    rect6, ed_lst, frst_val, scnd_val, ed = rem_and_min_ed(ed_lst, frst_val, scnd_val, ed, fndn_lst)
    rect7, ed_lst, frst_val, scnd_val, ed = rem_and_min_ed(ed_lst, frst_val, scnd_val, ed, fndn_lst)
    rect8, ed_lst, frst_val, scnd_val, ed = rem_and_min_ed(ed_lst, frst_val, scnd_val, ed, fndn_lst)
    rect9, ed_lst, frst_val, scnd_val, ed = rem_and_min_ed(ed_lst, frst_val, scnd_val, ed, fndn_lst)
    rect10, ed_lst, frst_val, scnd_val, ed = rem_and_min_ed(ed_lst, frst_val, scnd_val, ed, fndn_lst)
    return rect1, rect2, rect3, rect4, rect5, rect6, rect7, rect8, rect9, rect10


def get_min_pline(trgt_rct, fndn_lst):
    ed_lst = []
    for i in fndn_lst:
        if i == trgt_rct: continue

        frst_pnt, scnd_pnt, ed = get_pnts(trgt_rct, i)
        ed_lst.append([ed, frst_pnt, scnd_pnt])

    frst_val, scnd_val, ed = get_spnt(ed_lst)

    rect1 = []
    for i in fndn_lst:
        if scnd_val in i: rect1 = i.copy()

    rect1.append(frst_val);
    rect1.append(scnd_val);
    rect1.append(ed)
    rect2, ed_lst, frst_val, scnd_val, ed = rem_and_min_ed(ed_lst, frst_val, scnd_val, ed, fndn_lst)
    rect3, ed_lst, frst_val, scnd_val, ed = rem_and_min_ed(ed_lst, frst_val, scnd_val, ed, fndn_lst)
    return rect1, rect2, rect3


def segregate_ids(lst):
    one = []
    two = []
    start1, start2 = True, True

    for i in lst:
        if start1:
            start2 = False
            if i[1] == "text":
                start1 = False
                start2 = True
            else:
                one.append(i)
        if start2: two.append(i)
    return one, two


def get_rect_of_text(txt, txt_lst):
    return [x for x in txt_lst if x[9] == txt]


def get_id(pnt, data):
    for i in data:
        if pnt[0] in i and pnt[1] in i:
            return i[0]
        elif str(pnt[0]) in i and str(pnt[1]) in i:
            return i[0]


def get_id_frm_xmin_ymin_xmax_ymax(xmin, ymin, xmax, ymax, data):
    for i in data:
        if xmin in i and ymin in i and xmax in i and ymax in i: return i[0]
        if str(xmin) in i and str(ymin) in i and str(xmax) in i and str(ymax) in i: return i[0]


def sort_polyline(data):
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


def make_entity_csv(lst, writer, type_):
    """
    entity.csv | uid | type | description | xmin | ymin | xmax | ymax |
    """
    global uid
    uid = 1

    for i in lst:
        if type_ == "symbol":
            writer.writerow([uid, "symbol", vals.get(i[4]), i[0], i[1], i[2], i[3]])
            uid += 1
        if type_ == "text":
            writer.writerow([uid, "text", i[4], i[0], i[1], i[2], i[3]])
            uid += 1
        if type_ == "polyline":
            writer.writerow([uid, "polyline", "None", i[0], i[1], i[2], i[3]])
            uid += 1


def make_parent_child_csv(attr, lst):
    for i in lst:
        if int(attr[0]) in i and int(attr[1]) in i and int(attr[2]) in i and int(attr[3]) in i: return [0, i[0], 1]
        if str(attr[0]) in i and str(attr[1]) in i and str(attr[2]) in i and str(attr[3]) in i: return [0, i[0], 1]


def convert_int(pnt):
    tmp = pnt[1:-1].split()
    l11 = int(tmp[0][:-1])
    l22 = int(tmp[1])
    return l11, l22


def get_accurate_pnts(pnt, data):
    for i in data:
        if pnt in i:
            return i[0][0], i[0][1], i[4][0], i[4][1]
    return 0, 0, 0, 0


def get_min_lst(lst):
    sorted(lst, key=lambda x: x[2])
    return lst[0]


def get_real_pnt_wrt_ed(pnt, list1, list2, list3):
    tl = []
    tl.append(get_min_ed_with_point((pnt[0], pnt[1]), list1))
    tl.append(get_min_ed_with_point((pnt[0], pnt[1]), list2))
    tl.append(get_min_ed_with_point((pnt[0], pnt[1]), list3))
    alist = sorted(tl, key=lambda i: i[1])[0]
    return alist[2][0], alist[2][1]


def get_coords_from_pnt(pnt, list1, list2, list3):
    xmin, ymin, xmax, ymax = get_accurate_pnts((pnt[0], pnt[1]), list1)
    if xmin == 0 and ymin == 0 and xmax == 0 and ymax == 0:
        print("not found coords in symbols")
        xmin, ymin, xmax, ymax = get_accurate_pnts((pnt1x, pnt1y), list2)
        if xmin == 0 and ymin == 0 and xmax == 0 and ymax == 0:
            print("not found coords in texts")
            xmin, ymin, xmax, ymax = get_accurate_pnts((pnt1x, pnt1y), list3)

    if xmin or ymin or xmax or ymax:
        return xmin, ymin, xmax, ymax
    else:
        return None, None, None, None


whl_dta = read_csv(CONSOLIDATED_CSV)
whl_dta.remove(whl_dta[0])
vsl_insght_lst, txt_lst, plylin_lst = segregate_whl_dta(whl_dta)

txt_pnt_lst = get_pnt_lst(txt_lst)
vsl_insght_pnt_lst = get_pnt_lst(vsl_insght_lst)

with open("entity.csv", "w") as entity_csv:
    writer = csv.writer(entity_csv)
    writer.writerow(["uid", "type", "description", "xmin", "ymin", "xmax", "ymax"])
    writer.writerow([uid, "drawing", CONSOLIDATED_CSV.split('//')[-1].split(".")[0], "None", "None", "None", "None"])

    plylin_lst = sort_polyline(plylin_lst)
    plylin_pnt_lst = get_pnt_lst(plylin_lst)
    make_entity_csv(vsl_insght_lst, writer, "symbol")
    make_entity_csv(txt_lst, writer, "text")
    make_entity_csv(plylin_lst, writer, "polyline")

print("[INFO] entity.csv is created")

whl_lst = read_csv("entity.csv")
whl_lst.pop(0)
whl_lst.pop(0)

'''
with open("parent_child.csv", "w") as pccsv:
    writer = csv.writer(pccsv)
    writer.writerow(["parent", "child", "confidence"])
    writer.writerows(make_parent_child_csv(i, whl_lst) for i in vsl_insght_lst)
    writer.writerows(make_parent_child_csv(i, whl_lst) for i in txt_lst)
    # writer.writerows(make_parent_child_csv(i, whl_lst) for i in plylin_lst)
'''
print("[INFO] parent_child.csv is created")

e_list = []
for i in vsl_insght_pnt_lst:
    one, two, three, four, five, six, seven, eight, nine, ten = get_min_ed(i, txt_pnt_lst)
    one.append(1);
    two.append(1);
    three.append(1);
    four.append(1);
    five.append(0.5)
    six.append(0.5);
    seven.append(0.5);
    eight.append(0.5);
    nine.append(0.25);
    ten.append(0.25)
    e_list.append([one, two, three, four, five, six, seven, eight, nine, ten])


print(e_list)

fnl_tmp_list = []
for numi, i in enumerate(e_list):
    sym_id_entity = get_id_frm_xmin_ymin_xmax_ymax(vsl_insght_pnt_lst[numi][0][0], vsl_insght_pnt_lst[numi][0][1],
                                                   vsl_insght_pnt_lst[numi][4][0], vsl_insght_pnt_lst[numi][4][1],
                                                   whl_lst)
    tmp = []
    for j in i:
        sym_id_attr = get_id_frm_xmin_ymin_xmax_ymax(j[0][0], j[0][1], j[4][0], j[4][1], whl_lst)
        tmp.append([sym_id_entity, sym_id_attr, j[-2], j[-1]])
    fnl_tmp_list.append(tmp)

print(fnl_tmp_list)
# sys.exit()
# checks if one attribute is present in another entity
tmp_lst1 = []
for i in fnl_tmp_list:
    tmp_lst2 = []
    for j in i:
        tmp_lst3 = []
        brk = False
        for x in fnl_tmp_list:
            if i == x: continue
            for y in x:
                if int(j[1]) == int(y[1]):
                    if j[2] <= y[2]:
                        tmp_lst3.append(j)
                    else:
                        brk = True
                        break
            if brk: break
        if not brk: tmp_lst3.append(j)
        if tmp_lst3:
            minlst = get_min_lst(tmp_lst3)
            tmp_lst2.append(minlst)
    tmp_lst1.append(tmp_lst2)

# print(tmp_lst1)
with open("ed_relation.csv", "w") as ed_rel:
    writer = csv.writer(ed_rel)
    writer.writerow(["entity1", "entity2", "eDistance", "confidence"])
    for i in tmp_lst1:
        print(i)
        writer.writerows(i)

print("[INFO] ed_relation.csv is created")

linkage_lst = read_csv(LINKAGE_CSV)
linkage_lst.pop(0)
print(len(linkage_lst))

linkage_tmp_lst = []

for i in linkage_lst:
    pnt1x, pnt1y = convert_int(i[2])
    pnt2x, pnt2y = convert_int(i[3])
    print(i)
    print(pnt1x, pnt1y, pnt2x, pnt2y)

    point1x, point1y = get_real_pnt_wrt_ed((pnt1x, pnt1y), vsl_insght_pnt_lst, txt_pnt_lst, plylin_pnt_lst)
    point2x, point2y = get_real_pnt_wrt_ed((pnt2x, pnt2y), vsl_insght_pnt_lst, txt_pnt_lst, plylin_pnt_lst)

    xmin1, ymin1, xmax1, ymax1 = get_coords_from_pnt((point1x, point1y), vsl_insght_pnt_lst, txt_pnt_lst,
                                                     plylin_pnt_lst)
    xmin2, ymin2, xmax2, ymax2 = get_coords_from_pnt((point2x, point2y), vsl_insght_pnt_lst, txt_pnt_lst,
                                                     plylin_pnt_lst)

    entity1_id = get_id_frm_xmin_ymin_xmax_ymax(xmin1, ymin1, xmax1, ymax1, whl_lst)
    entity2_id = get_id_frm_xmin_ymin_xmax_ymax(xmin2, ymin2, xmax2, ymax2, whl_lst)

    if (xmin1 or ymin1 or xmax1 or ymax1) and (xmin2 or ymin2 or xmax2 or ymax2):
        pnt = get_min_ed_with_point((pnt1x, pnt1y), plylin_pnt_lst)[2]
        linkage_tmp = get_id(pnt, whl_lst)
        linkage_tmp_lst.append([entity1_id, entity2_id, linkage_tmp, 1])

with open("polyline_relation.csv", "w") as prcsv:
    writer = csv.writer(prcsv)
    writer.writerow(["entity1", "entity2", "linkage_id", "confidence"])
    writer.writerows(linkage_tmp_lst)

print("[INFO] polyline_relation.csv is created")

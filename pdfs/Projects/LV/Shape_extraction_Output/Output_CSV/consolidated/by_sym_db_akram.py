import csv
import re
import math
import sys
from prettytable import PrettyTable
# from db_connect_updated import fetch_from_madb
from db_connect_local import fetch_from_localdb

# CONSOLIDATED_CSV = "sld_26_consolidated.csv"
CONSOLIDATED_CSV = "sld_25_consolidated.csv"


# vals = {"0": "FEEDER", "1": "CONNECTOR", "2": "TP", "3": "STP", "4": "EP"}


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
    return rect1, rect2, rect3, rect4


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


def get_text_id(txt):
    with open("id.csv", "r") as id_csv:
        reader = csv.reader(id_csv)
        for i in reader:
            if i:
                if i[1] == txt: return i[2]


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


whl_dta = read_csv(CONSOLIDATED_CSV)
whl_dta.remove(whl_dta[0])
vsl_insght_lst, txt_lst, plylin_lst = segregate_whl_dta(whl_dta)

txt_pnt_lst = get_pnt_lst(txt_lst)
vsl_insght_pnt_lst = get_pnt_lst(vsl_insght_lst)

argtable = PrettyTable()
argtable.field_names = ["Entity", "Attribute 1", "Attribute 2", "Attribute 3", "Attribute 4"]
vals = fetch_from_localdb()

# id_lst = [drawing name, has child, child id]
uid = 0

id_csv = open("id.csv", "w")
writer = csv.writer(id_csv)

id_lst = []
for i in txt_lst:
    apnd = True
    for j in id_lst:
        if i[4] in j:
            apnd = False
            break
    if apnd:
        id_lst.append([CONSOLIDATED_CSV.split('//')[-1].split(".")[0], i[4], uid])
        uid += 1

writer.writerow(["drawing_name", "text", "uid"])
writer.writerows([i for i in id_lst])

id_csv.close()

# id_lst = read_csv("id.csv")
# sym_lst, t_lst = segregate_ids(id_lst)
#
# sym_lst.remove(sym_lst[0])
# t_lst.remove(t_lst[0])

tlst = []
sym_coords = []
for i in vals:
    if int(i) == 0:
        trgt_rct = fnd_rct(int(i), vsl_insght_pnt_lst)
        if trgt_rct:
            for j in trgt_rct:
                print(j)
                one, two, three, four = get_min_ed(j, txt_pnt_lst)
                tlst.append(
                    [int(i), one[9], one[12], one[0], one[4], two[9], two[12], two[0], two[4], three[9], three[12],
                     three[0], three[4], four[9], four[12], four[0], four[4]])
                sym_coords.append([j[0], j[4]])
                symbol = vals.get(i)
                argtable.add_row([str(i) + " (" + symbol.upper() + ")", one[9], two[9], three[9], four[9]])

argtable.align = "l"
# print(argtable)
# print(tlst)
sys.exit()
# gdb = [has attribute, xmin, ymin, xmax, ymax, text value, confidence]
gdb = open("graphdb.csv", "w")
writer2 = csv.writer(gdb)
# writer2.writerow(["has_attribute", "xmin", "ymin", "xmax", "ymax", "text_value", "confidence"])
writer2.writerow(["has_child", "c_xmin", "c_ymin", "c_xmax", "c_ymax", "has_attribute", "xmin", "ymin", "xmax", "ymax", "text_value", "confidence"])

id_csv = open("id.csv", "a")
writer = csv.writer(id_csv)
writer.writerow(["drawing_name", "symbol_id", "uid"])

for numi_outer, (i, sc) in enumerate(zip(tlst, sym_coords)):
    for numj_outer, j in enumerate(i):
        confidence = 1
        if type(j) is int or type(j) is float or type(j) is tuple: continue
        for numk_inner, k in enumerate(tlst):
            for numl_inner, l in enumerate(k):
                if numi_outer == numk_inner and numj_outer == numl_inner: continue
                if type(l) is int or type(l) is float or type(l) is tuple: continue
                if j == l:
                    confidence = 1 if i[numj_outer + 1] < k[numl_inner + 1] else 0
                    print(j, i[numj_outer + 1], k[numl_inner + 1], l, confidence)
        writer2.writerow(
            [uid, sc[0][0], sc[0][1], sc[1][0], sc[1][1], get_text_id(j), i[numj_outer + 2][0], i[numj_outer + 2][1],
             i[numj_outer + 3][0], i[numj_outer + 3][1], j,
             confidence])
    writer.writerow([CONSOLIDATED_CSV.split('//')[-1].split(".")[0], i[0], uid])
    uid += 1
    for vil in vsl_insght_lst:
        # print(i[0])
        if i[0] == int(vil[4]):
            # print("inside it")
            vsl_insght_lst.remove(vil)

id_lst = []
print(vsl_insght_lst)
for i in vsl_insght_lst:
    apnd = True
    for j in id_lst:
        if i[4] in j:
            apnd = False
            break
    if apnd:
        id_lst.append([CONSOLIDATED_CSV.split('//')[-1].split(".")[0], i[4], uid])
        uid += 1


writer.writerows([i for i in id_lst])

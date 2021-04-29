import csv
import re
import math
import sys
from prettytable import PrettyTable
# from db_connect_updated import fetch_from_madb
from db_connect_local import fetch_from_localdb

# CONSOLIDATED_CSV = "sld_26_consolidated.csv"
CONSOLIDATED_CSV = "sld_25_consolidated.csv"


# DICTIONARY_TO_REMEMBER = {"0":"FEEDER", "1":"CONNECTOR", "2":"TP", "3":"STP", "4":"EP"}

def read_csv(file):
    data = []
    with open(file, "r") as fo:
        reader = csv.reader(fo)
        for i in reader:
            if i: data.append(i)
    data.remove(data[0])
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


whl_dta = read_csv(CONSOLIDATED_CSV)
vsl_insght_lst, txt_lst, plylin_lst = segregate_whl_dta(whl_dta)

txt_pnt_lst = get_pnt_lst(txt_lst)
vsl_insght_pnt_lst = get_pnt_lst(vsl_insght_lst)

argtable = PrettyTable()
argtable.field_names = ["Entity", "Attribute 1", "Attribute 2", "Attribute 3", "Attribute 4"]
vals = fetch_from_localdb()

for i in vals:
    trgt_rct = fnd_rct(i, vsl_insght_pnt_lst)
    if trgt_rct:
        for j in trgt_rct:
            # for txt in txt_pnt_lst:
            frst_min_ed, scnd_min_ed, thrd_min_ed, frth_min_ed = get_min_ed(j, txt_pnt_lst)
            symbol = vals.get(i)
            argtable.add_row(
                [str(i) + " (" + symbol.upper() + ")", frst_min_ed[9], scnd_min_ed[9], thrd_min_ed[9], frth_min_ed[9]])

argtable.align = "l"
print(argtable)

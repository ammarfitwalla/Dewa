from glob import glob
import os
from pathlib import Path
import csv
from cnn_cross_section_arrow import section_a_to_z


def read_csv(file):
    data = []
    with open(file, "r") as fo:
        reader = csv.reader(fo)
        for i in reader:
            if i: data.append(i)
    data.remove(data[0])
    return data


def make_entity_csv(parent_id, lst, writer, type_):
    """
    noc_entity.csv | uid | type | description | xmin | ymin | xmax | ymax |
    """
    global uid

    for i in lst:
        # if type_ == "symbol":
        #     writer.writerow([uid, "symbol", vals.get(i[4]), i[0], i[1], i[2], i[3]])
        #     uid += 1
        if type_ == "text":
            writer.writerow([uid, parent_id, "text", i[4], i[0], i[1], i[2], i[3]])
            uid += 1
        if type_ == "polyline":
            writer.writerow([uid, parent_id, "polyline", "None", i[0], i[1], i[2], i[3]])
            uid += 1


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


def get_id_frm_xmin_ymin_xmax_ymax(xmin, ymin, xmax, ymax, data):
    for i in data:
        if xmin in i and ymin in i and xmax in i and ymax in i: return i[3]
        if str(xmin) in i and str(ymin) in i and str(xmax) in i and str(ymax) in i: return i[3]


current_dir = os.getcwd()
PROJECT_NAME = (current_dir.split("\\")[-1])
# print(PROJECT_NAME)

all_sub_dir_paths = glob(str(current_dir) + '/*/')  # returns list of sub directory paths

all_sub_dir_names = [Path(sub_dir).name for sub_dir in all_sub_dir_paths if Path(sub_dir).name == 'Design']
# print(all_sub_dir_names)
# print()

uid = 0

with open("graphdb_csv/noc_entity.csv", "w", newline='') as entity_csv:
    writer = csv.writer(entity_csv)
    writer.writerow(["uid", "parent", "type", "description", "xmin", "ymin", "xmax", "ymax"])
    writer.writerow(
        [uid, "None", "project", PROJECT_NAME, "None", "None", "None", "None"])
    uid += 1

entity_csv_parent = read_csv('graphdb_csv/noc_entity.csv')

for i in all_sub_dir_names:
    with open("graphdb_csv/noc_entity.csv", "a", newline='') as entity_csv:
        writer = csv.writer(entity_csv)
        for pname in entity_csv_parent:
            if pname[3] == PROJECT_NAME:
                writer.writerow(
                    [uid, pname[0], "file", i, "None", "None", "None", "None"])
                uid += 1
entity_csv_ = read_csv('graphdb_csv/noc_entity.csv')
# print(entity_csv_)

for dir_ in all_sub_dir_names:
    all_csvs = glob(str(dir_) + "/*.csv")
    for ac in all_csvs:
        ac_name = ac.split("\\")[-1]
        ac_dir = ac.split("\\")[-2]
        dname_id = [i[0] for i in entity_csv_ if i[3] == ac_dir]

        with open("graphdb_csv/noc_entity.csv", "a", newline='') as entity_csv:
            writer = csv.writer(entity_csv)
            writer.writerow(
                [uid, dname_id[0], "document", ac_name, "None", "None", "None", "None"])
            uid += 1

entity_csv_ = read_csv('graphdb_csv/noc_entity.csv')

# print(entity_csv_)

# with open("graphdb_csv/noc_parent_child.csv", "w", newline='') as pccsv:
#     writer = csv.writer(pccsv)
#     writer.writerow(["parent", "child", "confidence"])

with open("graphdb_csv/noc_ed_relation.csv", "w", newline='') as ed_rel:
    writer = csv.writer(ed_rel)
    writer.writerow(["entity1", "entity2", "eDistance", "confidence"])

temp_id = uid

for dir_ in all_sub_dir_names:
    all_csvs = glob(str(dir_) + "/*.csv")
    # print(all_csvs)
    for one_csv in all_csvs:
        data = read_csv(one_csv)
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

        whl_lst_1 = read_csv("graphdb_csv/noc_entity.csv")
        pn = []
        dn = []
        cn = []
        for tl in whl_lst_1:
            if tl[3] == PROJECT_NAME:
                pn.append(tl[0])
                pn.append(tl[1])
            elif tl[3] == dir_:
                dn.append(tl[0])
                dn.append(tl[1])
            elif tl[3] == one_csv.split("\\")[-1]:
                cn.append(tl[0])
                cn.append(tl[1])
        print(pn, dn, cn)

        with open("graphdb_csv/noc_entity.csv", "a", newline='') as entity_csv:
            writer = csv.writer(entity_csv)
            plylin_lst = sort_polyline(plylin_lst)
            # plylin_pnt_lst = get_pnt_lst(plylin_lst)
            # make_entity_csv(vsl_insght_lst, writer, "symbol")
            make_entity_csv(cn[0], txt_lst, writer, "text")
            make_entity_csv(cn[0], plylin_lst, writer, "polyline")

        entity_lst = read_csv("graphdb_csv/noc_entity.csv")

        whole_list = []

        for txt in txt_lst:
            for one_data in entity_lst:
                if one_data[1] == cn[0] and one_data[3] == txt[4] and one_data[4] == txt[0] and one_data[5] == txt[
                        1] and one_data[6] == txt[2] and one_data[7] == txt[3]:
                    # print(one_data[1], cn[0])
                    whole_list.append(
                        [pn[0], dn[0], cn[0], one_data[0], one_data[4], one_data[5], one_data[6], one_data[7], 1])

        for pl in plylin_lst:
            for one_data in entity_lst:
                if one_data[1] == cn[0] and one_data[2] == 'polyline' and one_data[3] == 'None' and int(
                        one_data[4]) == pl[0] and int(one_data[5]) == pl[1] and int(one_data[6]) == pl[2] and int(
                        one_data[7]) == pl[3]:
                    # print(one_data[1], cn[0])
                    whole_list.append(
                        [pn[0], dn[0], cn[0], one_data[0], one_data[4], one_data[5], one_data[6], one_data[7], 1])

        # with open("graphdb_csv/noc_parent_child.csv", "a", newline='') as pccsv:
        #     writer = csv.writer(pccsv)
        #     for wd in whole_list:
        #         # print(wd)
        #         # writer.writerow([wd[0], wd[1], wd[2], wd[3], 1])
        #         writer.writerow([wd[2], wd[3], 1])

        all_section_connection = section_a_to_z(one_csv,
                                                r'D:\KS\Projects\Dewa\pdfs\Projects\NOC\NN_Data\CNN\checkpoints\model-653-0.06')
        # x_list = [i[2] for i in all_section_connection]
        # thresh_list = confidence_value(x_list)

        ed_section_list = []
        for num, i in enumerate(all_section_connection):
            sym_id_entity = get_id_frm_xmin_ymin_xmax_ymax(i[0][0][0], i[0][0][1], i[0][4][0], i[0][4][1],
                                                           whole_list)
            sym_id_attr = get_id_frm_xmin_ymin_xmax_ymax(i[2][0][0], i[2][0][1], i[2][4][0], i[2][4][1],
                                                         whole_list)
            ed_section_list.append([sym_id_entity, sym_id_attr, i[3], i[4][0][0]])

        with open("graphdb_csv/noc_ed_relation.csv", "a", newline='') as ed_rel:
            writer = csv.writer(ed_rel)
            writer.writerows(ed_section_list)

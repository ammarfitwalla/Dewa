import csv
import sys
import numpy as np
import cv2


def read_csv(file):
    data = []
    with open(file, "r") as fo:
        reader = csv.reader(fo)
        for i in reader:
            if i: data.append(i)
    data.remove(data[0])
    return data


def add_zero_value(csv_name):
    temp = []
    azv_data = read_csv(csv_name)
    with open(csv_name, 'a', newline='') as nn_data:
        writer = csv.writer(nn_data)
        for i in azv_data:
            print(i)
            if len(temp) == 0:
                temp.append(i)
            elif len(temp) == 1:
                if temp[0][0] == i[0] and temp[0][1] == i[1] and temp[0][2] == i[2] and temp[0][3] == i[3] and temp[0][
                    4] == i[4] and temp[0][5] == i[5]:
                    temp.append(i)
                else:
                    writer.writerow(
                        [temp[0][0], temp[0][1], temp[0][2], temp[0][3], temp[0][4], temp[0][5], temp[0][6], temp[0][7],
                         temp[0][8], temp[0][9], temp[0][10], temp[0][11], i[12], i[13], i[14], i[15], i[16], i[17], 0])
                    writer.writerow(
                        [i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9], i[10], i[11], temp[0][12],
                         temp[0][13], temp[0][14], temp[0][15], temp[0][16], temp[0][17], 0])
                    temp.clear()

            elif len(temp) == 2:
                if temp[0][0] == i[0] and temp[0][1] == i[1] and temp[0][2] == i[2] and temp[0][3] == i[3] and temp[0][
                    4] == i[4] and temp[0][5] == i[5]:
                    temp.append(i)
                else:
                    writer.writerow(
                        [temp[0][0], temp[0][1], temp[0][2], temp[0][3], temp[0][4], temp[0][5], temp[0][6], temp[0][7],
                         temp[0][8], temp[0][9], temp[0][10], temp[0][11], i[12], i[13], i[14], i[15], i[16], i[17], 0])
                    writer.writerow(
                        [i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9], i[10], i[11], temp[0][12],
                         temp[0][13], temp[0][14], temp[0][15], temp[0][16], temp[0][17], 0])

                    writer.writerow(
                        [i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9], i[10], i[11], temp[1][12],
                         temp[1][13], temp[1][14], temp[1][15], temp[1][16], temp[1][17], 0])
                    temp.clear()
                    temp.append(i)

            elif len(temp) == 3:
                writer.writerow(
                    [temp[0][0], temp[0][1], temp[0][2], temp[0][3], temp[0][4], temp[0][5], temp[0][6], temp[0][7],
                     temp[0][8], temp[0][9], temp[0][10], temp[0][11], i[12], i[13], i[14], i[15], i[16], i[17], 0])
                writer.writerow(
                    [i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9], i[10], i[11], temp[0][12],
                     temp[0][13], temp[0][14], temp[0][15], temp[0][16], temp[0][17], 0])

                writer.writerow(
                    [i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9], i[10], i[11], temp[1][12],
                     temp[1][13], temp[1][14], temp[1][15], temp[1][16], temp[1][17], 0])

                writer.writerow(
                    [i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9], i[10], i[11], temp[2][12],
                     temp[2][13], temp[2][14], temp[2][15], temp[2][16], temp[2][17], 0])
                temp.clear()
                temp.append(i)


def get_val_by_hw(csv_name, h, w):
    vbhw_data = read_csv(csv_name)
    with open('NN_final_18_pts.csv', 'a', newline='') as nn_data:
        writer = csv.writer(nn_data)
        # writer.writerow(['xmin', 'ymin', 'x', 'y', 'xmax', 'ymax',
        #                  'x1min', 'y1min', 'x1', 'y1', 'x1max', 'y1max',
        #                  'x2min', 'y2min', 'x2', 'y2', 'x2max', 'y2max',
        #                  'output'])
        for i in vbhw_data:
            # x, y, x1, y1, x2, y2 = int(i[0]) / w, int(i[1]) / h, int(i[2]) / w, int(i[3]) / h, int(i[4]) / w, int(
            #     i[5]) / h
            # writer.writerow(
            #     ['{:.2f}'.format(x), '{:.2f}'.format(y), '{:.2f}'.format(x1), '{:.2f}'.format(y1), '{:.2f}'.format(x2),
            #      '{:.2f}'.format(y2), i[6]])

            xmin, ymin, x, y, xmax, ymax, x1min, y1min, x1, y1, x1max, y1max, x2min, y2min, x2, y2, x2max, y2max = \
                int(i[0]) / w, int(i[1]) / h, int(i[2]) / w, int(i[3]) / h, int(i[4]) / w, int(i[5]) / h, \
                int(i[6]) / w, int(i[7]) / h, int(i[8]) / w, int(i[9]) / h, int(i[10]) / w, int(i[11]) / h, \
                int(i[12]) / w, int(i[13]) / h, int(i[14]) / w, int(i[15]) / h, int(i[16]) / w, int(i[17]) / h

            writer.writerow(
                ['{:.2f}'.format(xmin), '{:.2f}'.format(ymin), '{:.2f}'.format(x), '{:.2f}'.format(y),
                 '{:.2f}'.format(xmax), '{:.2f}'.format(ymax),
                 '{:.2f}'.format(x1min), '{:.2f}'.format(y1min), '{:.2f}'.format(x1), '{:.2f}'.format(y1),
                 '{:.2f}'.format(x1max), '{:.2f}'.format(y1max),
                 '{:.2f}'.format(x2min), '{:.2f}'.format(y2min), '{:.2f}'.format(x2), '{:.2f}'.format(y2),
                 '{:.2f}'.format(x2max), '{:.2f}'.format(y2max), int(i[18])
                 ])


def find_duplicate_vals(csv_name):
    counter = 0
    dup_data = read_csv(csv_name)

    for numi, i in enumerate(dup_data):
        for numj, j in enumerate(dup_data):
            if numi != numj:
                if i[:-1] == j[:-1] and i[-1] != j[-1]:
                    pr = ''
                    for k in i:
                        pr += k + ","
                    print(pr[:-1])
                    pr = ''
                    for k in j:
                        pr += k + ","
                    print(pr[:-1])
                    print()
                    counter += 1
                    dup_data.remove(j)

    print(counter)


def plot_circle(csv_name, h, w):
    plot_data = read_csv(csv_name)
    image = np.ones((h, w, 3), dtype="uint8") * 255
    x_, y_, z_ = False, False, True
    x, y, z = 0, 0, 255
    for i in plot_data:
        if i[18] == '1':
            if z_:
                x, y, z = 0, 0, 255; z_ = False; y_ = True
            elif y_:
                x, y, z = 0, 255, 0; y_ = False; x_ = True
            elif x_:
                x, y, z = 255, 0, 0; x_ = False; z_ = True

            cv2.circle(image, (int(i[0]), int(i[1])), 4, (x, y, z), 4)
            cv2.circle(image, (int(i[2]), int(i[3])), 4, (x, y, z), 4)
            cv2.circle(image, (int(i[4]), int(i[5])), 4, (x, y, z), 4)
            cv2.circle(image, (int(i[6]), int(i[7])), 4, (x, y, z), 4)
            cv2.circle(image, (int(i[8]), int(i[9])), 4, (x, y, z), 4)
            cv2.circle(image, (int(i[10]), int(i[11])), 4, (x, y, z), 4)
            cv2.circle(image, (int(i[12]), int(i[13])), 4, (x, y, z), 4)
            cv2.circle(image, (int(i[14]), int(i[15])), 4, (x, y, z), 4)
            cv2.circle(image, (int(i[16]), int(i[17])), 4, (x, y, z), 4)
    cv2.imwrite("plotted_circle1.jpg", image)


def write_other_csv(csv_name):
    other_csv_data = read_csv(csv_name)
    for i in other_csv_data:
        with open(r'E:\dewa\pdfs\GCNN\ClusterGCN\NN_Data\NN_final_18_pts.csv', 'a', newline='') as nn_data:
            writer = csv.writer(nn_data)
            if i[-1] == '0':
                writer.writerow(i)


# add_zero_value('NN_data_18_pts_raw_secA.csv')
# get_val_by_hw(r'Cross_Section_Markers_3_4\CrossSections_and_markers-31_updated.csv', 3944, 5000)
# get_val_by_hw(r'Cross_Section_Markers_3_4\CrossSections_and_markers-41_updated.csv', 4050, 5000)
# get_val_by_hw(r'Cross_Section_Markers_5_6\CrossSections_and_markers-5_nn_data_updated.csv', 3938, 5000)
# get_val_by_hw(r'Cross_Section_Markers_5_6\CrossSections_and_markers-6_nn_data_updated.csv', 3943, 5000)
# get_val_by_hw(r'Cross_Section_Markers_7\CrossSections_and_markers-7_nn_data_updated.csv', 3971, 5000)
# get_val_by_hw(r'Cross_Section_Markers_9\CrossSections_and_markers-9_nn_data_updated.csv', 3765, 5000)
# get_val_by_hw(r'Cross_Section_Markers_10\CrossSections_and_markers-10_nn_data_updated.csv', 4046, 5000)
# get_val_by_hw(r'Cross_Section_Markers_11\CrossSections_and_markers-11_nn_data_updated.csv', 3784, 5000)
# get_val_by_hw(r'Cross_Section_Markers_12\CrossSections_and_markers-12_nn_data_updated.csv', 3529, 5000)
# get_val_by_hw(r'Cross_Sections_markers_2\NN_CrossSections_and_markers-2_data_updated.csv', 3917, 5000)
# get_val_by_hw(r'Cross_Sections_markers_8\CrossSections_and_markers-8_nn_data_updated.csv', 4041, 5000)
# get_val_by_hw(r'Cross_Sections_markers_1B_1B\NN_data_18_pts_1B_1B_updated.csv', 3429, 5000)
# get_val_by_hw(r'sectionA\NN_data_18_pts_raw_secA_updated.csv', 3539, 5000)
# get_val_by_hw(r'sectionB\NN_data_18_pts_raw_secB_updated.csv', 3506, 5000)

find_duplicate_vals(r'NN_final_18_pts.csv')
# find_duplicate_vals(r'E:\dewa\pdfs\GCNN\ClusterGCN\OUTPUT_HOUSE_IRRIGATION\NN_section_AB36.csv')

# plot_circle(r'Cross_Section_Markers_3_4\CrossSections_and_markers-31_updated.csv', 3944, 5000)

# write_other_csv(r'E:\dewa\pdfs\GCNN\ClusterGCN\NN_Data\CNN\model_18pts_csv.csv')

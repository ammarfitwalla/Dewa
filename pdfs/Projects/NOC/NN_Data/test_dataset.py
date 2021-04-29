import csv


def read_csv(file):
    data = []
    with open(file, "r") as fo:
        reader = csv.reader(fo)
        for i in reader:
            if i: data.append(i)
    data.remove(data[0])
    return data


csv_name = r'E:\dewa\pdfs\GCNN\ClusterGCN\NN_Data\Cross_Sections_markers_1B_1B\NN_data_18_pts_1B_1B.csv'
all_data = read_csv(csv_name)

all_data_copy = []

for enu, i in enumerate(all_data):
    # print(i)
    if int(i[18]) == 1:
        if (int(i[0]) > int(i[6]) and int(i[12]) > int(i[6])) and (int(i[4]) < int(i[10]) and int(i[16]) < int(i[10])):
            all_data_copy.append(i)
        else:
            pass
    else:
        all_data_copy.append(i)

print(len(all_data))
print(len(all_data_copy))

with open(csv_name.split(".")[0]+"_updated.csv", 'w', newline='') as nn_data:
    writer = csv.writer(nn_data)
    for i in all_data_copy:
        # print(i)
        writer.writerow(i)

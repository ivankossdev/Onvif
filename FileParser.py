def file_parser(read_file):
    with open(f"{read_file}", "r") as file:
        out = []
        while True:
            line = file.readline()
            if not line:
                break
            elif line[0] == "P" or line[0] == "M":
                break
            readline = line.strip()
            out.append(readline[11:28])

    mac_dic = {}
    for x in range(len(out)):
        mac_dic[out[x]] = x
    return list(mac_dic.keys())


def glue_file_value():
    temp_array = []
    temp_dict = {}
    for x in range(4):
        temp_array.extend(file_parser(f"mac_{x + 1}.txt"))

    for x in range(len(temp_array)):
        if temp_array[x] != '':
            temp_dict[temp_array[x]] = x
    return list(temp_dict.keys())
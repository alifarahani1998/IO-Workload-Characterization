import seaborn as sn
import matplotlib.pyplot as plt


def read_file(file_name):
    with open(file_name) as f:
        return f.readlines()


def preprocess(context):
    result = []

    for i in context:
        tmp = (" ".join(i.split())).split(" ")
        if 'C' in tmp[0]:
            break
        result.append(tmp)

    return result


def select_info(context):
    sectors = []

    for i in context:
        if not invalid_operation(i[6]) and len(i) == 11:
            sectors.append(int(i[7]))

    return sectors


def invalid_operation(operation):
    if 'F' in operation or 'M' in operation or 'N' in operation:
        return True


def byte_to_gigabyte(sectors):
    result = []
    unit = 1024 * 1024 * 1024

    for i in sectors:
        result.append(int(i * 512 / unit))

    return result


def prepare_data_to_visualization(sectors_location):
    result, tmp = [], []

    for i in sectors_location:
        tmp.append(i)
        if len(tmp) == 42:
            result.append(tmp)
            tmp = []

    return result


def visualize(data):
    sn.set(rc={'figure.figsize': (16, 16)})
    sn.color_palette("flare", as_cmap=True)
    hm = sn.heatmap(data=data,
                    linewidths=0.5,
                    linecolor="black",
                    cbar_kws={'label': 'Total I/Os During Test'},
                    cmap='coolwarm')

    plt.title('Heat Map of IOPS Over the Disk')
    plt.show()


def main():
    input_file = input('Enter trace path: ')
    print('Executing ...')
    file_context = preprocess(read_file(input_file))
    sectors = byte_to_gigabyte(select_info(file_context))

    sectors_location = [0] * 1764
    for i in sectors:
        if i <= 1764:
            sectors_location[i - 1] += 1
        else:
            sectors_location[-1] += 1

    data = prepare_data_to_visualization(sectors_location)

    visualize(data)


if __name__ == '__main__':
    main()

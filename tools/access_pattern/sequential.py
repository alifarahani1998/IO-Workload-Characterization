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
    operation_address = []

    for i in context:
        if not invalid_operation(i[6]) and len(i) == 11:
            operation_address.append((i[6], int(i[7]), int(i[9])))

    return operation_address


def invalid_operation(operation):
    if 'F' in operation or 'M' in operation or 'N' in operation:
        return True


def byte_to_gigabyte(num1, num2, num3):
    unit = 1024 * 1024 * 1024

    return num1 / unit, num2 / unit, num3 / unit


def sequential_operations(operation_address, window_size):
    total, reads, writes = 0, 0, 0
    reads_size, writes_size, total_size = 0, 0, 0
    seen_list = []

    for i in operation_address:
        for j in seen_list:
            if i[0] == j[0] and i[1] - ((j[1] + j[2]) - 1) == 1:

                if 'R' in i[0]:
                    reads += 1
                    reads_size += i[2]
                else:
                    writes += 1
                    writes_size += i[2]

                total += 1
                total_size += i[2]
                break

        seen_list.append(i)

        if len(seen_list) > window_size:
            seen_list.pop(0)

    total_size, reads_size, writes_size = byte_to_gigabyte(total_size * 512, reads_size * 512, writes_size * 512)

    return total, reads, writes, total_size, reads_size, writes_size


def all_operations(operation_address):
    reads, writes = 0, 0
    reads_size, writes_size, total_size = 0, 0, 0

    for i in operation_address:
        if 'R' in i[0]:
            reads += 1
            reads_size += i[2]
        else:
            writes += 1
            writes_size += i[2]

        total_size += i[2]

    total = len(operation_address)

    total_size, reads_size, writes_size = byte_to_gigabyte(total_size * 512, reads_size * 512, writes_size * 512)

    return total, reads, writes, total_size, reads_size, writes_size


def main():
    input_file = input('Enter trace path: ')
    window_size = input('Enter window size: ')
    print('Executing ...')
    file_context = preprocess(read_file(input_file))
    operation_address = select_info(file_context)

    # All
    total, reads, writes, total_size, reads_size, writes_size = all_operations(operation_address)

    # Sequential
    total_seq, reads_seq, writes_seq, total_seq_size, reads_seq_size, writes_seq_size = sequential_operations(operation_address, int(window_size))

    with open('sequential.txt', "w") as f:
        f.write('All operations:\n')
        f.write(f'Sequential: {format((total_seq / total) * 100, ".2f")} % ---> {format(total_seq_size, ".2f")} GB of {format(total_size, ".2f")} GB\n')
        f.write(f'Separate:   {format(((total - total_seq) / total) * 100, ".2f")}  % ---> {format(total_size - total_seq_size, ".2f")}  GB of {format(total_size, ".2f")} GB\n')
        f.write("\n")
        f.write('Read operations:\n')
        f.write(f'Sequential: {format((reads_seq / reads) * 100, ".2f")} % ---> {format(reads_seq_size, ".2f")} GB of {format(reads_size, ".2f")} GB\n')
        f.write(f'Separate:   {format(((reads - reads_seq) / reads) * 100, ".2f")}  % ---> {format(reads_size - reads_seq_size, ".2f")}  GB of {format(reads_size, ".2f")} GB\n')
        f.write("\n")
        f.write('Write operations:\n')
        f.write(f'Sequential: {format((writes_seq / writes) * 100, ".2f")} % ---> {format(writes_seq_size, ".2f")} GB of {format(writes_size, ".2f")} GB\n')
        f.write(f'Separate:   {format(((writes - writes_seq) / writes) * 100, ".2f")}  % ---> {format(writes_size - writes_seq_size, ".2f")}  GB of {format(writes_size, ".2f")} GB')


if __name__ == '__main__':
    main()

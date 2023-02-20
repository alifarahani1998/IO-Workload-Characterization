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


def prepare_next_operations_list(operation_address, index, next_operations_list_count):
    length = next_operations_list_count
    result = []

    while length != 0 and index != len(operation_address):
        result.append(operation_address[index])
        length -= 1
        index += 1

    return result


def intersection(element1, element2):
    a = [[element1[1], element1[1] + element1[2] - 1]]
    b = [[element2[1], element2[1] + element2[2] - 1]]

    result = []
    i, j = 0, 0

    while i < len(a) and j < len(b):
        a_left, a_right = a[i]
        b_left, b_right = b[j]

        if a_right < b_right:
            i += 1
        else:
            j += 1

        if a_right >= b_left and b_right >= a_left:
            end_pts = sorted([a_left, a_right, b_left, b_right])
            middle = [end_pts[1], end_pts[2]]
            result.append(middle)

    ri = 0

    while ri < len(result) - 1:
        if result[ri][1] == result[ri + 1][0]:
            result[ri:ri + 2] = [[result[ri][0], result[ri + 1][1]]]

        ri += 1

    return result


def byte_to_gigabyte(num):
    unit = 1024 * 1024 * 1024

    return num / unit


def calculate_shared_volume(shared_interval):
    return byte_to_gigabyte(shared_interval[1] - shared_interval[0] + 1)


def overlapped_operations(operation_address, next_operations_list_count):
    total, reads, writes = 0, 0, 0
    reads_size, writes_size, total_size = 0, 0, 0

    for i in operation_address:
        next_operations_list = prepare_next_operations_list(operation_address, operation_address.index(i) + 1, next_operations_list_count)

        for j in next_operations_list:
            result = intersection(i, j)
            if len(result) > 0:
                # Total
                total += 1
                volume = calculate_shared_volume(result[0])
                total_size += volume
                # Read
                if 'R' in i[0] and 'R' in j[0]:
                    reads += 1
                    reads_size += volume
                # Write
                elif 'W' in i[0] and 'W' in j[0]:
                    writes += 1
                    writes_size += volume
                # Read_Write
                break

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

    total_size = byte_to_gigabyte(total_size * 512)
    reads_size = byte_to_gigabyte(reads_size * 512)
    writes_size = byte_to_gigabyte(writes_size * 512)

    return total, reads, writes, total_size, reads_size, writes_size


def main():
    input_file = input('Enter trace path: ')
    print('Executing ...')
    file_context = preprocess(read_file(input_file))
    operation_address = select_info(file_context)

    # All
    total, reads, writes, total_size, reads_size, writes_size = all_operations(operation_address)

    # Overlapped
    next_operations_list_count = [200, 500, 1000]
    for i in next_operations_list_count:
        total_over, reads_over, writes_over, total_over_size, reads_over_size, writes_over_size = overlapped_operations(operation_address, i)

        with open('overlapped.txt', "a") as f:
            f.write(f"Next operations list = {i}\n\n")

            f.write("All operations:\n")
            f.write(f"Overlapped: {format((total_over / total) * 100, '.2f')} %\n")
            f.write(f"Count: {total_over}\n")
            f.write(f"Overlapped volume: {format(total_over_size, '.10f')} GB of {format(total_size, '.10f')} GB\n\n")

            f.write("Read operations:\n")
            f.write(f"Overlapped: {format((reads_over / reads) * 100, '.2f')} %\n")
            f.write(f"Count: {reads_over}\n")
            f.write(f"Overlapped volume: {format(reads_over_size, '.10f')} GB of {format(reads_size, '.10f')} GB\n\n")

            f.write("Write operations:\n")
            f.write(f"Overlapped: {format((writes_over / writes) * 100, '.2f')} %\n")
            f.write(f"Count: {writes_over}\n")
            f.write(f"Overlapped volume: {format(writes_over_size, '.10f')} GB of {format(writes_size, '.10f')} GB\n\n")

            f.write("------------------------------------------------------------------\n")


if __name__ == '__main__':
    main()

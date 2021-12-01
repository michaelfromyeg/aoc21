lines = None

target = "day1.txt"

# Process the input to a list of numbers
with open(target) as f:
    lines = f.readlines()
    number_lines = []
    for line in lines:
        line = line.replace("\n", "")
        if line == "":
            continue
        number_line = int(line)
        number_lines.append(number_line)
    lines = number_lines

# print(lines)

count = 0

for i in range(1, len(lines), 1):
    if lines[i - 1] < lines[i]:
        count = count + 1

window_count = 0


def window_sum(i: int) -> int:
    """
    Return window sum, treating i as the last index of the window
    """
    return lines[i - 2] + lines[i - 1] + lines[i]


for i in range(2, len(lines) - 1, 1):
    if window_sum(i) < window_sum(i + 1):
        window_count = window_count + 1
        # print(f"window_count={window_count}")

print(f"len(lines)={len(lines)}")
print(f"count={count}")
print(f"window_count={window_count}")

import numpy as np


def make_h(binary_image2d):
    result = np.zeros_like(binary_image2d, dtype=int)
    result[0] = binary_image2d[0]
    for i in range(1, result.shape[0]):
        result[i] = np.where(binary_image2d[i], result[i-1] + 1, 0)
    return result


class Node:
    def __init__(self, value, index):
        self.value = value
        self.index = index
        self.left = None
        self.right = None

    def __repr__(self):
        return f'Node(value={self.value}, index={self.index})'

    def __str__(self):
        return self.__repr__()


def make_tree(arr):
    stack = []
    nodes = []
    for i, elem in enumerate(arr):
        new_node = Node(elem, i)
        last = None
        while stack:
            top = stack[-1]
            if top.value > elem:
                last = stack.pop()
            else:
                break
        if last is not None:
            new_node.left = last
        if stack:
            stack[-1].right = new_node
        stack.append(new_node)
    return stack[0]


# note: we could bias this towards more square rectangles if we
# use some measure of "squareness" for the second value in the tuple
def largest_rectangle(low, high, root):
    if low == high or root is None:
        return (0,)
    return max(
        (root.value * (high - low), root.value, low, high),
        largest_rectangle(low, root.index, root.left),
        largest_rectangle(root.index + 1, high, root.right),
        )

# find the largest rectangle in a 2D binary mask, return its coordinates
# as slices
# uses https://stackoverflow.com/a/12387148/224254
# and https://stackoverflow.com/a/50651622/224254
def largest_rectangle_in_mask(binary_mask2d):
    h = make_h(binary_mask2d)
    max_rect_size = 0
    for i, row in enumerate(h):
        tree = make_tree(row)
        max_rect_ending_in_row = largest_rectangle(
            0, row.size, tree
            )
        size, height, curr_start_col, curr_end_col = (
            max_rect_ending_in_row
            )
        if size > max_rect_size:
            start_row = i - height + 1
            end_row = i + 1
            start_col = curr_start_col
            end_col = curr_end_col
            max_rect_size = size
    return (slice(start_row, end_row), slice(start_col, end_col))


array = np.array([
    [0, 0, 0, 0, 1, 0],
    [0, 0, 1, 0, 0, 1],
    [0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1],
    [0, 0, 1, 0, 0, 0]], dtype=bool)
mask = ~array
print(mask.astype(int))
image = np.random.random(array.shape)
print(image)
image_cropped = image[largest_rectangle_in_mask(mask)]
print(image_cropped)

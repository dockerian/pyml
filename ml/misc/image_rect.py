"""
misc/image_rect.py

An image is represented by a simple 2D array where every pixel is a 1 or a 0.


"""
from ml.utils.logger import get_logger

LOGGER = get_logger(__name__)


def find_rectangle(image: list) -> list:
    """
    Find single rectangle:

    Each image may have a single rectangle of 0's on a background of 1's.
    The function takes in the image and returns one of the following
    representations of the rectangle of 0's:
        [[top,left], [bottom,right]]  # coordinates, or
        [[top,left], [width,height]]

        Sample:
        ```
        image1 = [
            [1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 0, 0, 0, 1],
            [1, 1, 1, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1],
        ]
        ```

        Sample output variations (only one is necessary):
        ```
        findRectangle(image1) =>
            {x: 3, y: 2, width: 3, height: 2}
            [[2,3], [3,5]] -- row,column of the top-left and bottom-right corners
        ```

        Other test cases:
        ```
        image2 = [
            [1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 0],
        ]

        findRectangle(image2) =>
            {x: 6, y: 4, width: 1, height: 1}
            [[4,6], [4,6]]

        image3 = [
            [1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 0, 0],
            [1, 1, 1, 1, 1, 0, 0],
        ]

        findRectangle(image3) =>
            {x: 5, y: 3, width: 2, height: 2}
            [[3,5], [4,6]]

        image4 = [
            [0, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1],
        ]

        findRectangle(image4) =>
            {x: 0, y: 0, width: 1, height: 1}
            [[0,0], [0,0]]

        image5 = [
            [0],
        ]

        findRectangle(image5) =>
            {x: 0, y: 0, width: 1, height: 1}
            [[0,0], [0,0]]
        ```
    """
    rows = len(image)
    cols = len(image[0])
    start = None
    end = None
    for y in range(rows):
        for x in range(cols):
            if start is None and image[y][x] == 0:
                start = {'x': x, 'y': y}

            x1 = cols - x - 1
            y1 = rows - y - 1
            if end is None and x1 < cols and y1 < rows and image[y1][x1] == 0:
                end = {'x': x1, 'y': y1}

            if start is not None and end is not None:
                break

    result = {
        'x': start['x'],
        'y': start['y'],
        'height': end['y'] - start['y'] + 1,
        'width': end['x'] - start['x'] + 1,
    }
    LOGGER.debug(result)

    return [
        [start['y'], start['x']],
        [end['y'], end['x']],
    ]


def find_rects(image: list) -> list:
    """
    Find multiple rectangles:

    Potentially the image may have many distinct rectangles of 0's on a
    background of 1's. The function that takes in the image and returns the
    coordinates of all the 0 rectangles in either one of the following formats:
        [[top,left], [bottom,right]]  # coordinates, or
        [[top,left], [width,height]]

        Samples:

        ```
        image1 = [
          [0, 1, 1, 1, 1, 1, 1],
          [1, 1, 1, 1, 1, 1, 1],
          [1, 1, 1, 0, 0, 0, 1],
          [1, 0, 1, 0, 0, 0, 1],
          [1, 0, 1, 1, 1, 1, 1],
          [1, 0, 1, 0, 0, 1, 1],
          [1, 1, 1, 0, 0, 1, 1],
          [1, 1, 1, 1, 1, 1, 0],
        ]
        ```
        Sample output variations (only one is necessary):

        ```
        findRectangles(image1) =>
            // (using top-left and bottom-right):
            [
                [[0,0],[0,0]],
                [[2,3],[3,5]],
                [[3,1],[5,1]],
                [[5,3],[6,4]],
                [[7,6],[7,6]],
            ]
            // (using top-left and width/height):
            [
                [[0,0],[1,1]],
                [[2,3],[3,2]],
                [[3,1],[1,3]],
                [[5,3],[2,2]],
                [[7,6],[1,1]],
            ]
        ```

        Other test cases:

        ```
        image2 = [
            [0],
        ]

        findRectangles(image2) =>
            // (using top-left and bottom-right):
            [
                [[0,0],[0,0]],
            ]

            // (using top-left and width/height):
            [
                [[0,0],[1,1]],
            ]

        image3 = [
            [1],
        ]

        findRectangles(image3) => []
        ```
    """
    rows = len(image)
    cols = len(image[0])
    results, startx, starty = [], [], []
    found = False
    x, y = 0, 0

    for y in range(rows):
        for x in range(cols):
            # print('Checking:', y, x, 'in', starty, startx)
            if found and image[y][x] != 0:
                found = False
            if not found and image[y][x] == 0:
                found = True
                contx = y in starty and x-1 >= 0 and image[y][x-1] == 0
                conty = x in startx and y-1 >= 0 and image[y-1][x] == 0
                existed = y in starty and x in startx
                if not existed and not conty and not contx:
                    # print('Found:', y, x)
                    startx.append(x)
                    starty.append(y)

    for i, x in enumerate(startx):
        y = starty[i]
        x1, y1 = x+1, y+1
        while x1 < cols and image[y][x1] == 0:
            x1 += 1
        while y1 < rows and image[y1][x1-1] == 0:
            y1 += 1
        x2, y2 = x+1, y+1
        while y2 < rows and image[y2][x] == 0:
            y2 += 1
        while x2 < cols and image[y2-1][x2] == 0:
            x2 += 1
        xd, yd = min(x1-1, x2-1), min(y1-1, y2-1)
        results.append([[y, x], [yd, xd]])
    return results

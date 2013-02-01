def getBoundingBox( obj ):
    min = Vector ((0, 0, 0))
    max = Vector ((0, 0, 0))
    size = Vector ((0, 0, 0))
    first = True
    for v in obj.data.vertices:
        if first:
            min[0] = v.co[0]
            min[1] = v.co[1]
            min[2] = v.co[2]
            max[0] = v.co[0]
            max[1] = v.co[1]
            max[2] = v.co[2]
            first = False
        else:
            if min[0] > v.co[0]:
                min[0] = v.co[0]
            if min[1] > v.co[1]:
                min[1] = v.co[1]
            if min[2] > v.co[2]:
                min[2] = v.co[2]
            if max[0] < v.co[0]:
                max[0] = v.co[0]
            if max[1] < v.co[1]:
                max[1] = v.co[1]
            if max[2] < v.co[2]:
                max[2] = v.co[2]
    size[0] = max[0] - min[0]
    size[1] = max[1] - min[1]
    size[2] = max[2] - min[2]
    return size

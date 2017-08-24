class ObjReader:
    """Read obj files. Specified here
    http://www.fileformat.info/format/wavefrontobj/egff.htm
    Blender can be used to create these files. Remove faces to get lines only.
    """

    def __init__(self, filename):
        self.vs = []
        self.ls = []

        with open(filename, 'r') as f:
            for line in f:
                # print("line", line)

                if line.startswith('v'):
                    # handling vertex spec
                    _v, x, y, z = line.split(' ')

                    self.vs.append((float(x), float(y), float(z)))

                if line.startswith('l'):
                    # handling line spec
                    _l, v1, v2 = line.split(' ')
                    self.ls.append((int(v1) - 1, int(v2) - 1))


def main():
    for obj in ["cube.obj", "cone.obj", "monkey.obj",
                "oszi.obj", "four_cubes.obj"]:
        print("reading " + obj)
        objr = ObjReader("ressources/" + obj)
        print(" vertices", str(objr.vs)[:70], "..")
        print(" lines", str(objr.ls)[:70], "..")
        print(" ", len(objr.vs), "vertices ", len(objr.ls), "lines")


if __name__ == "__main__":
    main()

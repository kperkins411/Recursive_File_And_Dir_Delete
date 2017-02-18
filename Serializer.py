
__author__ = 'Perkins'

import sys
import pickle
import traceback

class Serializer():
    def save_list(self, thelist, thefile):
        if dir:
            # save for later
            try:
                fileObject = open(thefile, "w")
                for item in thelist:
                    fileObject.write("%s\n" % item)
                fileObject.close()
            except OSError as err:
                print("OS error: {0}".format(err))
            except ValueError:
                print("Could not convert data to an integer.")
            except:
                print("Unexpected error:", sys.exc_info()[0])

    def get_list(self,thefile):
        retval = ''
        try:
            fileObject = open(thefile, "r")
            retval = fileObject.readline()
            fileObject.close()
        except OSError as err:
            print("OS error: {0}".format(err))
        except ValueError:
            print("Could not convert data to an integer.")
        except:
            print("Unexpected error:", sys.exc_info()[0])

    def get_p(self, thefile):
        try:
            with open(thefile, "rb") as fp:
                return pickle.load(fp)
        except Exception as e:
            # everything else, possibly fatal
            print(traceback.format_exc(e))
            return

    def save_p(self, thelist, thefile):
        try:
            with open(thefile, "wb") as fp:
                pickle.dump(thelist, fp)
        except Exception as e:
            # everything else, possibly fatal
            print(traceback.format_exc(e))
            return

def main():
    #some simple tests
    s = Serializer()
    s.save_p("toast", "test1.txt")

    r = "str"
    s.save_p(r, "test2.txt")
    z = s.get_p("test2.txt")
    assert r == z

    r = [x for x in range(10)]
    s.save_p(r, "test2.txt")
    z = s.get_p("test2.txt")
    assert r == z


if __name__ == "__main__":
    main()
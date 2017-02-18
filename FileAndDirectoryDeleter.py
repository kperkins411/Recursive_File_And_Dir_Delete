
from Tkinter import *
import tkMessageBox
import tkFileDialog as filedialog


import logging
# from settings import Settings

import os
import Serializer
import shutil

class UI_Dir_and_File_Purge(Frame):
    def __init__(self, parent, str_filename=''):
        Frame.__init__(self, parent)
        # self.logger = logging.getLogger(__name__)
        self.parent = parent
        self.serialize = Serializer.Serializer()
        self.defaultDir = self.serialize.get_p("defaultdir")
        if self.defaultDir is None:
            self.defaultDir=''
        self.recursive_deleter = Delete_File_and_Dir_recursor()

        self.create_widgets()

    def create_widgets(self):

        self.parent.title("UI_Directory_and_File_Purge")
        self.pack(fill=BOTH, expand=1)

        #col 1 fills unused columns
        self.columnconfigure(1, weight=1)

        label1 = Label(self,
                       text="Choose directory with 475-575 in title, This directory will have all rubbish\n"
                            "files and directories as defined below deleted. Click Purge to finish\n",
                       justify=LEFT)
        label1.grid(row=0, column=0, columnspan=4, sticky=W, padx=5, pady=5)
        ######################
        #create a button and text to select a dir
        find_file_button = Button(self, text="Choose dir", command=self.select_dir)
        find_file_button.grid(row=1, column=0, sticky=W, padx=5, pady=5)

        self.entry_file_name = Entry(self)
        self.entry_file_name.grid(row=1, column=1, columnspan=3, sticky=W + E, padx=5, pady=5)
        self.entry_file_name.insert(0, self.defaultDir)

        ######################
        #tell the user what goes
        label1 = Label(self,
                       text="WARNING, this program will recurse that directory\n "+
                            "and will delete all dirs with the following names\n"+
                            " ".join([x for x in self.recursive_deleter.dirnames_to_ignore]) +
                            "\nAnd will delete all files other than those with the following extensions\n"+
                            "".join([x for x in self.recursive_deleter.fileexts]) +
                            '\nClick the purge button when ready',
                        justify=LEFT)
        label1.grid(row=3, column=0, columnspan=4, sticky=W, padx=5, pady=5)
        #create a go button

        self.lb_del_files = Button(self, text="Purge", command=self.del_files, state=DISABLED)
        self.lb_del_files.grid(row=9, column=0, sticky=W, padx=5)

        labelResults = Label(self, text="Waiting", justify=LEFT)
        labelResults.grid(row=9, column=1, columnspan=3, sticky=W, padx=5, pady=5)
        self.isValidDirectory(False)

    def isValidDirectory(self, promptuser=False):
        ret = "475-575" in self.defaultDir
        if not ret:
            self.lb_del_files.config(state="disabled")
            if promptuser==True:
                tkMessageBox.showerror("Title", "Dir must have 475-575 in it")
        else:
            self.lb_del_files.config(state="normal")
        return ret


    def select_dir(self):
        # TODO filepicker
        dir = filedialog.askdirectory(initialdir=self.defaultDir)

        if "475-575" not in dir:
            tkMessageBox.showerror("Title", "Dir must have 475-575 in it")
            self.lb_del_files.config(state="disabled")
            return

        self.lb_del_files.config(state="normal")
        self.defaultDir = dir
        self.serialize.save_p(self.defaultDir,"defaultdir")
        # set textbox value
        self.entry_file_name.delete(0, END)
        self.entry_file_name.insert(0, self.defaultDir)

    def del_files(self):
        if not self.isValidDirectory(True):
            return
        result = tkMessageBox.askquestion("Delete recursively from: "+ self.defaultDir, "Are You Sure?", icon='warning')
        if result == 'yes':
            self.recursive_deleter.recursive_delete(self.defaultDir)
            tkMessageBox.showinfo("Done", "You can run jPlag on the directory now")


class Delete_File_and_Dir_recursor:
    '''
    recurses a directory and gets a list of unique
    filenames and extensions
    '''
    def __init__(self):
        #the directory to recursively iterate over
        self.setFileExtensions_to_find(['.java', '.xml'])
        self.setDirNamestoIgnore(['build', 'gradle','.gradle','.idea','libs','.git','androidTest','test','__MACOSX'])

    def setFileExtensions_to_find(self, exts):
        self.fileexts = exts

    def setDirNamestoIgnore(self,dirnames_to_ignore):
        self.dirnames_to_ignore = dirnames_to_ignore

    def recursive_delete(self, path=os.getcwd()):
        assert os.path.isdir(path)

        self.filenames = []
        self.__recursive_delete(path)

    def __recursive_delete(self, path):
        allfiles = os.listdir(path)

        #build the lists
        for file in allfiles:
            fqn = os.path.join(path,file)
            if os.path.islink(fqn): #ignore all symlinks
                continue
            elif os.path.isfile(fqn):
                #split out ext
                ext = os.path.splitext(file)[1]

                #if we are  ignoring this extension
                if ext not in self.fileexts:
                    #then delete it
                    os.remove(fqn)

            elif os.path.isdir(fqn):
                if file not in self.dirnames_to_ignore:
                    self.__recursive_delete(fqn)
                else:
                    shutil.rmtree(fqn, ignore_errors=False, onerror=None)


def main():
    # myDI = Delete_File_and_Dir_recursor()
    # myDI.recursive_delete()
    # myDI.recursive_delete('/home/keith/PycharmProjects')
    #
    # myDI.setFileExtensions_to_find(['.py'])
    # myDI.recursive_delete('/home/keith/PycharmProjects')

    pass
    # Configure only in your main program clause
    # logging.basicConfig(level=logging.DEBUG,
    #                     filename='UI.log', filemode='w',
    #                     format='%(name)s %(levelname)s %(message)s')
    root = Tk()
    app = UI_Dir_and_File_Purge(root)
    root.mainloop()


if __name__ == "__main__":
    main()

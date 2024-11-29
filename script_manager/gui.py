import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
import os, shutil

# Setup
def set_dpi_awareness():
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except:
        pass

# GLOBALS
REDIRECT_VALUES = ["SingleSelectionSingleProcess", "MultipleSelectionSingleProcessSpaceSeparated", "MultipleSelectionMultipleProcesses"]

# Files

class DataManager():
    def __init__(self) -> None:
        self.scriptsPath = os.getcwd() + r"\waapi-scripts"
        self.fileList = os.listdir(self.scriptsPath)
        self.json_file = "Commands/waapi_tools_commands copy.json"
        self.script_template = self.scriptsPath+r"\waapi_template.py"
        self.currentScript = tk.StringVar()
        self.jsonCommand = {
            "id": "",
            "displayName": "",
            "program": "pythonw",
            "startMode": "",
            "args": "\"${WwiseUserAddons}/waapi-scripts/_.py\" ${id}",
            "redirectOutputs": True,
            "contextMenu": {
                "basePath": "",
                "enabledFor":"",
                "visibleFor": ""
            }
        }

#GUI
def toggle_frame(bool_var: tk.BooleanVar, widget: tk.Frame, column: int, row: int, sticky: str):
    if bool_var.get():
        widget.grid(column=column, row=row, sticky=sticky)
    else:
        widget.grid_remove()

def updateString(var: tk.StringVar, dest: str):
    dest = var
    

class WaapiScriptsManager(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("WAAPI Script Manager")
        self.minsize(720,480)
        self.dataManager = DataManager()
        scriptModule = ScriptsModuleFrame(self, self.dataManager)
        scriptModule.grid(column=0, row=0, padx=15, pady=15, sticky="NSEW")
        jsonModule = JsonModuleFrame(self, self.dataManager)
        jsonModule.grid(column=1,row=0, padx=15,pady=15, sticky="NSEW")

        #Configure
        # Configure grid weights
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

class ScriptsModuleFrame(ttk.Frame):
    def __init__(self, container:tk.Tk, dm):
        super().__init__(container)
        self.dm = dm
        # Create menu bar
        menuBar = tk.Menu(container)
        container.config(menu=menuBar)
        
        # Create file menu
        fileMenu = tk.Menu(menuBar, tearoff=False)
        menuBar.add_cascade(label="File", menu=fileMenu)
        fileMenu.add_command(label="New Script", command=self.createScript)
        fileMenu.add_command(label = "Exit", command = exit)
        
        scriptsLabel = ttk.Label(self,text="Scripts in Folder: ")
        self.scriptsListbox = tk.Listbox(self, selectmode="single", width=50, height=20)
        self.scriptsListbox.bind("<<ListboxSelect>>", self.updateSelectedScript)
        scrollBar = ttk.Scrollbar(self.scriptsListbox, orient = "vertical", command=self.scriptsListbox.yview)
        selectedScriptVar = tk.StringVar()
        selectedScriptVar.trace_add("write", lambda *args: updateString(selectedScriptVar,self.dm.currentScript))
        self.updateScripts()

        # Packing
        scriptsLabel.grid(column=0,row=0, sticky="EW")
        self.scriptsListbox.grid(column=0,row=1, sticky="NSEW")

        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.scriptsListbox.configure(yscrollcommand=scrollBar.set)
        scrollBar.place(relx=1, rely=0,relheight=1,anchor="ne")


    def updateScripts(self):
        self.scriptsListbox.delete(0,tk.END)
        for script in self.dm.fileList:
            self.scriptsListbox.insert(tk.END, script)

    def createScript(self):
        scriptName = simpledialog.askstring("Script Name", "Enter the Script Name: ")
        scriptDest = self.dm.scriptsPath+"\\"+scriptName+".py"
        shutil.copyfile(self.dm.script_template, scriptDest)
        self.dm.fileList = os.listdir(self.dm.scriptsPath)
        self.updateScripts()

    def updateSelectedScript(self, *_):
        selectedItem = '' if len(self.scriptsListbox.curselection())==0 else self.scriptsListbox.selection_get()
        self.dm.currentScript.set(selectedItem)

        
class JsonModuleFrame(ttk.Frame):
    def __init__(self, container, dm: DataManager) -> None:
        super().__init__(container)
        self.dm = dm
        JsonFrameStartLabel = ttk.Label(self,text="Arguments to pass to the JSON file: ")
        JsonSettingsFrame = ttk.Frame(self)
        JsonScriptNameLabel = ttk.Label(self, textvariable = self.dm.currentScript)
        # JsonUpdateBtn = ttk.Button(text="Update JSON", command = updateJson)

        #Id field
        JsonIdLabel = ttk.Label(JsonSettingsFrame, text = "Id: ")
        self.JsonIdVar = tk.StringVar()
        JsonIdEntry = ttk.Entry(JsonSettingsFrame, width=35, textvariable=self.JsonIdVar)

        #displayName
        self.JsonDisplayVar = tk.StringVar()
        JsonDisplayLabel = ttk.Label(JsonSettingsFrame, text = "Display Name: ")
        JsonDisplayEntry = ttk.Entry(JsonSettingsFrame, width=35, textvariable=self.JsonDisplayVar)
        #startMode
        self.JsonStartModeVar = tk.StringVar()
        JsonStartModeLabel = ttk.Label(JsonSettingsFrame, text = "Start Mode: ")
        JsonStartModeEntry = ttk.Combobox(JsonSettingsFrame, values=REDIRECT_VALUES)
        #args
        self.JsonArgsVar = tk.StringVar()
        JsonArgsLabel = ttk.Label(JsonSettingsFrame, text = "Args: ")
        JsonArgsEntry = ttk.Entry(JsonSettingsFrame, width=35, textvariable=self.JsonArgsVar)
        #redirectOutputs
        JsonRedirectVar = tk.BooleanVar(value=True)
        JsonRedirectEntry = ttk.Checkbutton(JsonSettingsFrame, text="Redirect Outputs", variable=JsonRedirectVar)
        #contextMenu
        JsonContextMenuVar = tk.BooleanVar(value=False)
        JsonContextMenuEntry = ttk.Checkbutton(JsonSettingsFrame, text="Context Menu", variable=JsonContextMenuVar)
        JsonContextMenuFrame = ttk.Frame(JsonSettingsFrame)
        JsonContextMenuVar.trace_add("write", lambda *args: toggle_frame(JsonContextMenuVar, JsonContextMenuFrame, 1, 6, "EW"))
        #basePath
        JsonctxBasePathVar = tk.StringVar()
        JsonctxBasePathLabel = ttk.Label(JsonContextMenuFrame, width=15, text= "Base Path: ")
        JsonctxBasePathEntry = ttk.Entry(JsonContextMenuFrame, width=35, textvariable=JsonctxBasePathVar)
        #enabledFor
        JsonEnabledVar = tk.StringVar()
        JsonEnabledLabel = ttk.Label(JsonContextMenuFrame, width=15,  text="Enabled for: ")
        JsonEnabledEntry = ttk.Entry(JsonContextMenuFrame, width=35, textvariable=JsonEnabledVar)
        #visibleFor
        JsonVisibleVar = tk.StringVar()
        JsonVisibleLabel = ttk.Label(JsonContextMenuFrame, width=15, text="Visible for: ")
        JsonVisibleEntry = ttk.Entry(JsonContextMenuFrame, width=35, textvariable=JsonVisibleVar)
        #mainMenu
        JsonMainMenuVar = tk.BooleanVar(value=False)
        JsonMainMenuEntry = ttk.Checkbutton(JsonSettingsFrame, width=15, text="Main Menu", variable=JsonMainMenuVar)
        JsonMainMenuFrame = ttk.Frame(JsonSettingsFrame)
        JsonMainMenuVar.trace_add("write", lambda *args: toggle_frame(JsonMainMenuVar, JsonMainMenuFrame, 1, 8, "EW"))
        #basePath
        JsonMainBasePathVar = tk.StringVar()
        JsonMainBasePathLabel = ttk.Label(JsonMainMenuFrame, width=15, text= "Base Path: ")
        JsonMainBasePathEntry = ttk.Entry(JsonMainMenuFrame, width=35, textvariable=JsonMainBasePathVar)


        JsonFrameStartLabel.grid(column=0,row=0,sticky="EW")
        JsonSettingsFrame.grid(column=0,row=1,sticky= "NSEW")

        #Json Frame 
        JsonIdLabel.grid(column=0, row=0, sticky="EW")
        JsonIdEntry.grid(column=1, row=0, sticky="EW")
        JsonDisplayLabel.grid(column = 0, row = 1, sticky="EW")
        JsonDisplayEntry.grid(column = 1, row = 1, sticky="EW")
        JsonStartModeLabel.grid(column = 0, row = 2, sticky="EW")
        JsonStartModeEntry.grid(column = 1, row = 2, sticky="EW")
        JsonArgsLabel.grid(column = 0, row = 3, sticky="EW")
        JsonArgsEntry.grid(column = 1, row = 3, sticky="EW")
        JsonRedirectEntry.grid(column = 1, row = 4, sticky="EW")
        JsonContextMenuEntry.grid(column = 1, row = 5, sticky="EW")
        JsonMainMenuEntry.grid(column = 1, row = 7, sticky="EW")
        JsonScriptNameLabel.grid(column=0,row = 8, sticky="EW")

        #Context Menu Frame
        
        JsonctxBasePathLabel.grid(column=0, row=0)
        JsonctxBasePathEntry.grid(column=1, row=0, sticky="EW")
        JsonEnabledLabel.grid(column=0, row=1, sticky="EW")
        JsonEnabledEntry.grid(column=1, row=1, sticky="EW")
        JsonVisibleLabel.grid(column=0, row=2, sticky="EW")
        JsonVisibleEntry.grid(column=1, row=2, sticky="EW")

        #MainMenu Frame
        JsonMainBasePathLabel.grid(column=0, row=0)
        JsonMainBasePathEntry.grid(column=1, row=0, sticky="EW")

        self.dm.currentScript.trace_add('write', self.updateScriptInfo)
        self.JsonArgsVar.trace_add('write', self.updateScriptInfo2)

    def updateScriptInfo2(self, *_):
        self.JsonDisplayVar.set(self.JsonArgsVar.get())
        self.JsonIdVar.set(self.JsonArgsVar.get())

    def updateScriptInfo(self, *_):
        self.JsonDisplayVar.set(self.dm.currentScript.get())
        self.JsonIdVar.set(self.dm.currentScript.get())

if __name__ == "__main__":
    root = WaapiScriptsManager()
    

    root.mainloop()





'''
    Change Logs: May 14, 2024
    Added navigation toolbar
    Added plot window resize options
    Removed X and Y limit changing

'''

from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog, Frame
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import os
from pathlib import Path
import easygui
from matplotlib.ticker import ScalarFormatter
import matplotlib

global skiprowss
matplotlib.rcParams["font.family"] = "Arial"
matplotlib.rcParams["font.weight"] = "bold"
matplotlib.rcParams["font.size"] = 14

pd.set_option("display.float_format", "{:.2e}".format)

easygui.msgbox(
    msg="Welcome to BbDS Interactive Plotter!"
        "\n\nInstructions: \nSelect how many rows to skip\n"
        "Select Sample TXT file\n"
        "Select Files and Plot!",
    title="BbDS Interactive Plotter",
    ok_button="Go on!",
)
skiprowss = int(easygui.enterbox(msg="How many rows to skip?"))
dfs = []
df_names = []


def select_file():
    filepath = filedialog.askopenfilename(
        title="Select Sample File",
        filetypes=(("Text files", "*.txt"), ("Text Files", "*.TXT")),
    )
    df = pd.read_csv(filepath, skiprows=skiprowss, delimiter="\t", header=None)
    return df


# Create a function for each button


def button_click(i):
    global width_entry, height_entry
    plt.cla()
    plt.clf()

    global savedata, canvas
    savedata = pd.DataFrame()
    savedata["Freq"] = dfs[0][df.iloc[0, 0]]

    fig = plt.figure(layout="constrained")
    ax = fig.add_subplot(111)

    for k, dff in enumerate(dfs):
        dfs[k].plot(
            kind="line", x=df.iloc[0, 0], y=df.iloc[0, i + 1], ax=ax, linewidth=2
        )

        ax.legend(df_names)
        savedata[df_names[k]] = dfs[k][df.iloc[0, i + 1]]
    plt.xticks(weight="bold")
    plt.yticks(weight="bold")
    plt.grid(which="both", axis="x", linestyle="-", linewidth=0.1)
    plt.grid(which="major", axis="y", linestyle="-", linewidth=0.1)
    plt.ticklabel_format(style="sci", axis="y", scilimits=(0, 0))
    ax.set_xscale("log")
    ax.set_xlabel("Frequency (Hz)", fontweight="bold")
    ax.set_ylabel(df.iloc[0, i + 1], fontweight="bold")
    ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
    canvas = FigureCanvasTkAgg(plt.gcf(), master=root)
    canvas.get_tk_widget().grid(row=6, column=0, columnspan=50)
    frame = Frame(root)
    frame.grid(row=7, column=0, columnspan=26)
    toolbar = NavigationToolbar2Tk(canvas, frame)
    toolbar.update()
    canvas.draw()


def save_file():
    filepath = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[
            ("txt File", "*.txt"),
            ("CSV File", "*.csv"),
            ("Data File", "*.dat"),
        ],
    )
    savedata.to_csv(filepath, sep="\t", index=False)


def save_plot():
    filepath = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("JPG File", "*.jpg"), ("PNG File", "*.png"), ("EPS File", "*.eps")],
    )
    plt.savefig(filepath, dpi=600)


def create_gui():
    global ax, canvas

    def open_files():
        del dfs[:]
        del df_names[:]
        files = filedialog.askopenfilenames(
            title="Select files",
            filetypes=(("Text files", "*.txt"), ("all files", "*.*")),
        )
        for file in files:
            dfs.append(pd.read_csv(file, delimiter="\t", skiprows=skiprowss, header=0))
            df_names.append(Path(file).stem)
        listbox.delete(0, tk.END)
        for file in df_names:
            listbox.insert(tk.END, file)

    def resize():

        plt.cla()
        plt.clf()
        canvas.get_tk_widget().destroy()

        matplotlib.rcParams["figure.figsize"] = (width_entry.get(), height_entry.get())

        canvas.draw()

    def open_folder():
        del dfs[:]
        del df_names[:]
        folderpath = filedialog.askdirectory()
        for file in sorted(os.listdir(folderpath), key=len):
            if file.endswith(".TXT"):
                filepath = os.path.join(folderpath, file)
                dfs.append(
                    pd.read_csv(filepath, delimiter="\t", skiprows=skiprowss, header=0)
                )
                df_names.append(Path(filepath).stem)
        listbox.delete(0, tk.END)
        for file in df_names:
            listbox.insert(tk.END, file)

    # Figure window resize
    width_label = tk.Label(root, text="Width:")
    width_label.grid(row=10, column=2)
    width_entry = tk.Entry(root, textvariable=w_fig)
    width_entry.grid(row=11, column=2)

    height_label = tk.Label(root, text="Height:")
    height_label.grid(row=12, column=2)
    height_entry = tk.Entry(root, textvariable=h_fig)
    height_entry.grid(row=13, column=2)

    resize_button = tk.Button(root, text="Resize", command=resize)
    resize_button.grid(row=14, column=2)
    Label_Resize = tk.Label(root, text="Resize Window", font="Helvetica 9 bold")
    Label_Resize.grid(row=9, column=2)  # , columnspan=60)

    # Title
    var = tk.StringVar()
    label = tk.Label(root, textvariable=var, font="Helvetica 18 bold")
    label.grid(row=0, column=2, columnspan=30)
    var.set("BBDS Interactive Plotter")

    # Open Folder and find txts
    open_button = tk.Button(
        root,
        text="Open Folder",
        command=open_folder,
        activebackground="#00ff00",
        bd=3,
        font="Helvetica 10 bold",
    )
    open_button.grid(row=9, column=16)  # , columnspan=3)

    # Open Files
    open_file_button = tk.Button(
        root,
        text="Open Files",
        command=open_files,
        activebackground="#00ff00",
        bd=3,
        font="Helvetica 10 bold",
    )
    open_file_button.grid(row=9, column=17)

    # save data button
    save_txt_button = tk.Button(
        root,
        text="Save Data",
        command=save_file,
        activebackground="#00ff00",
        bd=3,
        font="Helvetica 10 bold",
    )
    save_txt_button.grid(row=9, column=18)  # , columnspan=5)

    # save plot button
    save_button = tk.Button(
        root,
        text="Save Plot",
        command=save_plot,
        activebackground="#00ff00",
        bd=3,
        font="Helvetica 10 bold",
    )
    save_button.grid(row=9, column=19)  # , columnspan=3)

    var2 = tk.StringVar()
    label2 = tk.Label(root, textvariable=var2, font="Helvetica 9 bold")
    label2.grid(row=16, column=2)  # , columnspan=3)
    var2.set("Selected Files")
    listbox = tk.Listbox(root)
    listbox.grid(row=17, column=0, columnspan=5)

    # Create the figure and axes and canvas

    fig = plt.figure(layout="constrained")
    ax = fig.add_subplot(111)
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().grid(row=6, column=0, columnspan=50)

    # Create the buttons
    for i in range(4):
        button = tk.Button(
            root,
            text=(df.iloc[0, i + 1]).strip(),
            command=lambda i=i: button_click(i),
            activebackground="#00ff00",
            font="Helvetica 10 bold",
            justify="center",
        )
        # k=i+4
        button.grid(row=12, column=16 + i)  # , columnspan=15)

    k = 0
    for i in range(4, 8):
        button = tk.Button(
            root,
            text=(df.iloc[0, i + 1]).strip(),
            command=lambda i=i: button_click(i),
            activebackground="#00ff00",
            font="Helvetica 10 bold",
            justify="center",
        )
        # k=i
        button.grid(row=13, column=12 + i)  # , columnspan=15)


    # MSAS Logo
    image = Image.open("msas2.png")
    image = image.resize((300, 100))

    # Convert the image to PhotoImage object
    image = ImageTk.PhotoImage(image, master=root)

    # Create a label for the image
    label_im = tk.Label(root, image=image)
    label_im.grid(row=17, column=10, columnspan=15)

    frame = Frame(root)
    frame.grid(row=7, column=0, columnspan=26)
    toolbar = NavigationToolbar2Tk(canvas, frame)
    toolbar.update()
    canvas.draw()

    # Run the main loop
    root.mainloop()


# Create the main window
root = tk.Tk()
# root.geometry("640x900")
root.title("BBDS Plotter v2")

h_fig = tk.IntVar()
h_fig.set(4)
w_fig = tk.IntVar()
w_fig.set(6)

df = select_file()
create_gui()

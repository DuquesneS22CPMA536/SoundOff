import tkinter as tk
from tkinter import ttk
from tkinter import *


class View(tk.Toplevel):
    """A window to view the report of the lufs and peak values against the standards selected within
     the report results window

    Will use a scrollable frame to print results.

    """
    def __init__(self, parent, names_selected, lufs_or_peak, peak, lufs, report_window):
        """Initializes the view report window

        Will print the report a user selected in the report results window. Will print the report in
        a scrollable frame.

        Args:
          self: The instance of the view results window
          parent: App object, window it came from
          names_selected: a list of all names to report for
          lufs_or_peak: whether to test against lufs, peak, or both
          peak: the peak value of the file to test
          lufs: the lufs value of the file to test
          report_window: the previous window, will destroy upon initialization

        Raises:
          Any errors raised should be put here

        """
        report_window.destroy()
        super().__init__(parent)
        # create basic window properties
        self.title("View Report")
        max_name_length = parent.get_max_platform_name_length()
        size = str(max_name_length * 6 + 800) + "x300"
        self.geometry(size)

        container = ttk.Frame(self)
        container.pack(fill="both", expand=1)
        canvas = tk.Canvas(container)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # define a style of labels to display
        style = ttk.Style()
        style.configure(
            "Input.TLabel",
            foreground="white",
            background="#333147",
            font=('Helvetica', 10)
        )
        style.configure(
            "Column.TLabel",
            font=("Helvetica", 11, "bold")
        )
        style.configure(
            "Result.TLabel",
            font=("Helvetica", 10)
        )
        style.configure(
            "Pass.TLabel",
            foreground="green",
            font=("Helvetica", 10, "bold")
        )
        style.configure(
            "Fail.TLabel",
            foreground="red",
            font=("Helvetica", 10, "bold")
        )
        style.configure(
            "Close.TLabel",
            foreground="orange",
            font=("Helvetica", 10, "bold")
        )

        # create header labels
        platform_name_label = ttk.Label(
            scrollable_frame,
            text="Platform Name",
            style="Column.TLabel")
        max_lufs_label = ttk.Label(
            scrollable_frame,
            text="Max Integrated Loudness (LUFS)",
            style="Column.TLabel")
        max_peak_label = ttk.Label(
            scrollable_frame,
            text="Max True Peak (dBFS)",
            style="Column.TLabel")
        lufs_result_label = ttk.Label(
            scrollable_frame,
            text="LUFS Difference",
            style="Column.TLabel")
        peak_result_label = ttk.Label(
            scrollable_frame,
            text="Peak Difference",
            style="Column.TLabel")
        input_lufs_label = ttk.Label(
            scrollable_frame,
            text="Input Integrated Loudness (LUFS) from file: " + "{:.1f}".format(lufs),
            style="Input.TLabel")
        input_peak_label = ttk.Label(
            scrollable_frame,
            text="Input True Peak (dBFS) from file: " + "{:.1f}".format(peak),
            style="Input.TLabel")

        # always display platform name header
        platform_name_label.grid(column=0, row=1, padx=5)

        # only display headers for the type of report requested
        if lufs_or_peak == "LUFS Value":
            max_lufs_label.grid(column=1, row=1, padx=5)
            lufs_result_label.grid(column=2, row=1)
            input_lufs_label.grid(column=0, row=0, columnspan=2)
        elif lufs_or_peak == "Peak Value":
            max_peak_label.grid(column=1, row=1, padx=5)
            peak_result_label.grid(column=2, row=1)
            input_peak_label.grid(column=0, row=0, columnspan=2)
        else:
            max_lufs_label.grid(column=1, row=1, padx=5)
            max_peak_label.grid(column=2, row=1, padx=5)
            lufs_result_label.grid(column=3, row=1, padx=5)
            peak_result_label.grid(column=4, row=1, padx=5)
            input_lufs_label.grid(column=0, row=0, columnspan=2, padx=10)
            input_peak_label.grid(column=2, row=0, columnspan=2)

        i = 2
        for name in names_selected:
            name_label = ttk.Label(
                scrollable_frame,
                text=name,
                style="Result.TLabel"
            )

            values = parent.get_platform_standard(name)
            # format the max lufs and peak to only display one decimal point
            if values[0] != "":
                lufs_from_platform = "{:.1f}".format(values[0])
            else:
                lufs_from_platform = ""
            if values[1] != "":
                peak_from_platform = "{:.1f}".format(values[1])
            else:
                peak_from_platform = ""

            # create labels for the max luf and peak from the current platform
            lufs_label = ttk.Label(
                scrollable_frame,
                text=lufs_from_platform,
                style="Result.TLabel"
            )

            peak_label = ttk.Label(
                scrollable_frame,
                text=peak_from_platform,
                style="Result.TLabel"
            )

            # test whether the input luf value is less than or equal to the max luf value
            # if true: pass, if false: fail
            if values[0] == "":
                result_lufs = ttk.Label(
                    scrollable_frame,
                    text=""
                )
            elif values[0] - lufs > 2:
                result_lufs = ttk.Label(
                    scrollable_frame,
                    text="{:.1f}".format(-(lufs-values[0])),
                    style="Pass.TLabel"
                )
            elif values[0] - lufs > - 2:
                result_lufs = ttk.Label(
                    scrollable_frame,
                    text="{:.1f}".format(-(lufs-values[0])),
                    style="Close.TLabel"
                )
            else:
                result_lufs = ttk.Label(
                    scrollable_frame,
                    text="{:.1f}".format(-(lufs-values[0])),
                    style="Fail.TLabel"
                )
            # test whether the input peak value is less than or equal to the max peak value
            # if true: pass, if false: fail
            if values[1] == "":
                result_peak = ttk.Label(
                    scrollable_frame,
                    text=""
                )
            elif values[1] - peak > .5:
                result_peak = ttk.Label(
                    scrollable_frame,
                    text="{:.1f}".format(-(peak-values[1])),
                    style="Pass.TLabel"
                )
            elif values[1] - peak > -.5:
                result_peak = ttk.Label(
                    scrollable_frame,
                    text="{:.1f}".format(-(peak-values[1])),
                    style="Close.TLabel"
                )
            else:
                result_peak = ttk.Label(
                    scrollable_frame,
                    text="{:.1f}".format(-(peak-values[1])),
                    style="Fail.TLabel"
                )
            # always place name on the screen
            name_label.grid(column=0, row=i, padx=5, sticky="w")

            # only display report the user requested
            if lufs_or_peak == "LUFS Value":
                lufs_label.grid(column=1, row=i, padx=5)
                result_lufs.grid(column=2, row=i, padx=5)
            elif lufs_or_peak == "Peak Value":
                peak_label.grid(column=1, row=i, padx=5)
                result_peak.grid(column=2, row=i, padx=5)
            else:
                lufs_label.grid(column=1, row=i, padx=5)
                peak_label.grid(column=2, row=i, padx=5)
                result_lufs.grid(column=3, row=i, padx=5)
                result_peak.grid(column=4, row=i, padx=5)
            i += 1

        container.pack()
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # make the window modal
        self.focus_set()
        self.grab_set()
        self.transient(parent)
        self.wait_window(self)

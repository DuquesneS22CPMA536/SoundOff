import tkinter as tk
from tkinter import ttk
from tkinter import *


class View(tk.Toplevel):
    """A window to view the report of the lufs and peak values against the standards selected within the
        report results window

        Will use a scrollable frame to print results.

    """
    def __init__(self, parent, name_selected, lufs_or_peak, peak, lufs, report_window):
        """Initializes the view report window

        more info

        Args:
          self: An add new variable object
          parent: App object, window it came from
          name selected: the standards to test the new file against
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
        self.geometry("630x300")

        container = ttk.Frame(self)
        container.pack(fill=BOTH, expand=1)
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

        style = ttk.Style()

        style.configure(
            "Input.TLabel",
            foreground="white",
            background="#333147",
            font=('Helvetica', 10)
        )

        style.configure(
            "Column.TLabel",
            font=("Helvetica", 9, "bold")
        )

        style.configure(
            "Result.TLabel",
            font=("Helvetica", 8)
        )

        style.configure(
            "Pass.TLabel",
            foreground="green",
            font=("Helvetica", 8, "bold")
        )

        style.configure(
            "Fail.TLabel",
            foreground="red",
            font=("Helvetica", 8, "bold")
        )

        ttk.Label(
            scrollable_frame,
            text="Standard Name",
            style="Column.TLabel").grid(column=0, row=1, padx=5)

        standard_names = parent.get_standard_names_dict()

        if lufs_or_peak == "LUFS Value":
            ttk.Label(
                scrollable_frame,
                text="Max Integrated (LUFS)",
                style="Column.TLabel").grid(column=1, row=1, padx=5)
            ttk.Label(
                scrollable_frame,
                text="LUFS Result",
                style="Column.TLabel").grid(column=2, row=1)
            ttk.Label(
                scrollable_frame,
                text="Input LUF from file: " + str(lufs),
                style="Input.TLabel").grid(column=0, row=0, columnspan=2)

        elif lufs_or_peak == "Peak Value":
            ttk.Label(
                scrollable_frame,
                text="Max True Peak (dB)",
                style="Column.TLabel").grid(column=1, row=1, padx=5)
            ttk.Label(
                scrollable_frame,
                text="Peak Result",
                style="Column.TLabel").grid(column=2, row=1)
            ttk.Label(
                scrollable_frame,
                text="Input Peak from file: " + str(peak),
                style="Input.TLabel").grid(column=0, row=0, columnspan=2)

        else:
            ttk.Label(
                scrollable_frame,
                text="Max Integrated (LUFS)",
                style="Column.TLabel").grid(column=1, row=1, padx=5)
            ttk.Label(
                scrollable_frame,
                text="Max True Peak (dB)",
                style="Column.TLabel").grid(column=2, row=1, padx=5)
            ttk.Label(
                scrollable_frame,
                text="LUFS Result",
                style="Column.TLabel").grid(column=3, row=1, padx=5)
            ttk.Label(
                scrollable_frame,
                text="Peak Result",
                style="Column.TLabel").grid(column=4, row=1, padx=5)
            ttk.Label(
                scrollable_frame,
                text="Input LUF from file: " + str(lufs),
                style="Input.TLabel").grid(column=0, row=0, columnspan=2, padx=10)
            ttk.Label(
                scrollable_frame,
                text="Input Peak from file: " + str(peak),
                style="Input.TLabel").grid(column=2, row=0, columnspan=2)
            # we need a report of everything
        if name_selected == "All Available Standards":
            if lufs_or_peak == "LUFS Value":
                i = 2
                for name in standard_names:
                    name_label = ttk.Label(
                        scrollable_frame,
                        text=name,
                        style="Result.TLabel"
                    )

                    values = parent.get_standard_value(name)
                    lufs_label = ttk.Label(
                        scrollable_frame,
                        text=values[0],
                        style="Result.TLabel"
                    )

                    name_label.grid(column=0, row=i, padx=5)
                    lufs_label.grid(column=1, row=i, padx=5)

                    if lufs <= values[0]:
                        result_lufs = ttk.Label(
                            scrollable_frame,
                            text="Pass",
                            style="Pass.TLabel"
                        )
                    else:
                        result_lufs = ttk.Label(
                            scrollable_frame,
                            text="Fail",
                            style="Fail.TLabel"
                        )
                    result_lufs.grid(column=2, row=i, padx=5)
                    i += 1

            elif lufs_or_peak == "Peak Value":
                i = 2
                for name in standard_names:
                    name_label = ttk.Label(
                        scrollable_frame,
                        text=name,
                        style="Result.TLabel"
                    )

                    values = parent.get_standard_value(name)
                    peak_label = ttk.Label(
                        scrollable_frame,
                        text=values[1],
                        style="Result.TLabel"
                    )

                    name_label.grid(column=0, row=i, padx=5)
                    peak_label.grid(column=1, row=i, padx=5)

                    if peak <= values[1]:
                        result_peak = ttk.Label(
                            scrollable_frame,
                            text="Pass",
                            style="Pass.TLabel"
                        )
                    else:
                        result_peak = ttk.Label(
                            scrollable_frame,
                            text="Fail",
                            style="Fail.TLabel"
                        )
                    result_peak.grid(column=2, row=i, padx=5)
                    i += 1
            else:
                i = 2
                for name in standard_names:
                    name_label = ttk.Label(
                        scrollable_frame,
                        text=name,
                        style="Result.TLabel"
                    )

                    values = parent.get_standard_value(name)
                    lufs_label = ttk.Label(
                        scrollable_frame,
                        text=values[0],
                        style="Result.TLabel"
                    )
                    peak_label = ttk.Label(
                        scrollable_frame,
                        text=values[1],
                        style="Result.TLabel"
                    )

                    name_label.grid(column=0, row=i, padx=5)
                    lufs_label.grid(column=1, row=i, padx=5)
                    peak_label.grid(column=2, row=i, padx=5)

                    if lufs <= values[0]:
                        result_lufs = ttk.Label(
                            scrollable_frame,
                            text="Pass",
                            style="Pass.TLabel"
                        )
                    else:
                        result_lufs = ttk.Label(
                            scrollable_frame,
                            text="Fail",
                            style="Fail.TLabel"
                        )
                    result_lufs.grid(column=3, row=i, padx=5)
                    if peak <= values[1]:
                        result_peak = ttk.Label(
                            scrollable_frame,
                            text="Pass",
                            style="Pass.TLabel"
                        )
                    else:
                        result_peak = ttk.Label(
                            scrollable_frame,
                            text="Fail",
                            style="Fail.TLabel"
                        )
                    result_peak.grid(column=4, row=i, padx=5)
                    i += 1

            # result of just 1 standard
        else:
            name_label = ttk.Label(
                scrollable_frame,
                text=name_selected,
                style="Result.TLabel"
            )
            name_label.grid(column=0, row=2, padx=5)
            values = parent.get_standard_value(name_selected)
            if lufs_or_peak == "LUFS Value":
                lufs_value_label = ttk.Label(
                    scrollable_frame,
                    text=values[0],
                    style="Result.TLabel"
                )
                lufs_value_label.grid(column=1, row=2, padx=5)
                if lufs <= values[0]:
                    result_lufs = ttk.Label(
                        scrollable_frame,
                        text="Pass",
                        style="Pass.TLabel"
                    )
                else:
                    result_lufs = ttk.Label(
                        scrollable_frame,
                        text="Fail",
                        style="Fail.TLabel"
                    )

                result_lufs.grid(column=2, row=2, padx=5)

            elif lufs_or_peak == "Peak Value":
                peak_value_label = ttk.Label(
                    scrollable_frame,
                    text=values[1],
                    style="Result.TLabel"
                )
                peak_value_label.grid(column=1, row=2, padx=5)
                if peak <= values[1]:
                    result_peak = ttk.Label(
                        scrollable_frame,
                        text="Pass",
                        style="Pass.TLabel"
                    )
                else:
                    result_peak = ttk.Label(
                        scrollable_frame,
                        text="Fail",
                        style="Fail.TLabel"
                    )
                result_peak.grid(column=2, row=2, padx=5)

            else:
                lufs_value_label = ttk.Label(
                    scrollable_frame,
                    text=values[0],
                    style="Result.TLabel"
                )
                lufs_value_label.grid(column=1, row=2, padx=5)
                peak_value_label = ttk.Label(
                    scrollable_frame,
                    text=values[1],
                    style="Result.TLabel"
                )
                peak_value_label.grid(column=2, row=2, padx=5)
                if lufs <= values[0]:
                    result_lufs = ttk.Label(
                        scrollable_frame,
                        text="Pass",
                        style="Pass.TLabel"
                    )
                else:
                    result_lufs = ttk.Label(
                        scrollable_frame,
                        text="Fail",
                        style="Fail.TLabel"
                    )
                if peak <= values[1]:
                    result_peak = ttk.Label(
                        scrollable_frame,
                        text="Pass",
                        style="Pass.TLabel"
                    )
                else:
                    result_peak = ttk.Label(
                        scrollable_frame,
                        text="Fail",
                        style="Fail.TLabel"
                    )
                result_lufs.grid(column=3, row=2, padx=5)
                result_peak.grid(column=4, row=2, padx=5)

        container.pack()
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

# *****************************************************************************
# Author:           	Mike Winebarger
# Lab:              	Lab 9
# Date:		            March 10, 2022
# Description:	        This program uses a UI to prompt the user to select
#                       data to filter a list of popular names
# Input:            	user choices via comboboxes
# Output:           	scrollable table of the top 25 names by user input
# Sources:          	Lab 9 Documentation
# Note:                 I originally had this program using NameCount instead
#                       of Rating, but I assumed the results would be more
#                       intelligible using rating, as it gauges popularity vs
#                       number of names. I also have DISTINCT in my sql query,
#                       but it does not seem to work.
# *****************************************************************************


import pathlib
import tkinter as tk
import pygubu

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "browser.ui"


class BrowserApp:
    # Initialize with UI elements and methods
    def __init__(self, parent):
        self._builder = None
        self.mainwindow = None
        self.tree = None
        self.year_combo = None
        self.gender_combo = None
        self.build_ui(parent)
        self.setup_tree()
        self.setup_gender_combo()
        self.setup_year_combo()

    # Build UI
    def build_ui(self, parent):
        builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        self.mainwindow = builder.get_object('root', parent)
        builder.connect_callbacks(self)

        self._builder = builder
        self.gender_combo = builder.get_object('gender_combo', parent)
        self.year_combo = builder.get_object('year_combo', parent)
        self.tree = builder.get_object('names_tree', parent)

    # Setup treeview
    def setup_tree(self):
        tree = self.tree
        tree.configure(columns=(0, 1, 2, 3), style="Custom.Treeview")

        # Label and format the columns
        tree.heading(0, text="Name", anchor=tk.W)
        tree.heading(1, text="Gender")
        tree.heading(2, text="Year")
        tree.heading(3, text="Rank")

        tree.column(0, width=75)
        tree.column(1, width=75, anchor=tk.CENTER)
        tree.column(2, width=75, anchor=tk.CENTER)
        tree.column(3, width=75, anchor=tk.CENTER)

    # Populate gender selection box
    def setup_gender_combo(self):
        from Name import NameGender
        genders = NameGender.fetch_genders()
        self.gender_combo['values'] = [NameGender.ALL_GENDERS] + \
                                      [gender.get_gender() for gender in genders]
        self.gender_combo.current(0)

    # Populate year selection box
    def setup_year_combo(self):
        from Name import NameYear
        years = NameYear.fetch_years()
        self.year_combo['values'] = [NameYear.ALL_YEARS] + \
                                    [year.get_year() for year in years]
        self.year_combo.current(0)

    def gender_selected(self, event):
        pass

    def year_selected(self, event):
        pass

    # Respond to button click, initiate query
    def start_search(self):
        from Name import Name

        # Clear treeview for each button click
        self.tree.delete(*self.tree.get_children())

        # Get list of names
        names = Name.fetch_names(self.year_combo.get(),
                                 self.gender_combo.get())

        # Populate treeview
        for name in names:
            self.tree.insert('', 'end',
                             values=(name[0], name[1], name[2], name[3]))

    def run(self):
        self.mainwindow.mainloop()


if __name__ == '__main__':
    root = tk.Tk()
    root.title("** Top Names **")
    app = BrowserApp(root)
    app.run()

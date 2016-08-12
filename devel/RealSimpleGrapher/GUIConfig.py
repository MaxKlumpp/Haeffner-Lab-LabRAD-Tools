'''
Configuration settings for Grapher gui
'''
import pyqtgraph as pg
pg.setConfigOption('background', 'k')
pg.setConfigOption('foreground', 'y')

class traceListConfig():
    def __init__(self, background_color = 'white'):
        self.background_color = background_color

class graphConfig():
    def __init__(self, name, ylim=[0,1], isScrolling=False, max_datasets = 6,
                 show_points = True, grid_on = False):
        self.name = name
        self.ylim = ylim
        self.isScrolling = isScrolling
        self.max_datasets = max_datasets
        self.graphs = 1 # just a single graph
        self.show_points = show_points
	self.grid_on = grid_on

class gridGraphConfig():
    def __init__(self, tab, config_list):
        self.tab = tab
        self.config_list = config_list[0::3]
        self.row_list = config_list[1::3]
        self.column_list = config_list[2::3]

        self.graphs = len(self.config_list)


tabs =[
    gridGraphConfig('pmt', [graphConfig('pmt', ylim=[0,30], isScrolling=True, max_datasets = 1, show_points = False, grid_on = True), 0, 0]),
    gridGraphConfig('current', [graphConfig('current', max_datasets = 1, show_points = False), 0, 0]),
    gridGraphConfig('spectrum', [graphConfig('spectrum', show_points=False), 0, 0]),
    gridGraphConfig('tickle', [graphConfig('tickle', show_points=False), 0, 0])
]


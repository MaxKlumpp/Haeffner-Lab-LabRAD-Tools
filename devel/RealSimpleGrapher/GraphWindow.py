'''
Window for holding Graphs
'''
import sys
from PyQt4 import QtGui
from GraphWidgetPyQtGraph import Graph_PyQtGraph as Graph
from ScrollingGraphWidgetPyQtGraph import ScrollingGraph_PyQtGraph as ScrollingGraph
from DoubleGraphWindow import DoubleGraphWindow
import GUIConfig
from twisted.internet.defer import Deferred, inlineCallbacks, returnValue
from twisted.internet.task import LoopingCall
from twisted.internet.threads import blockingCallFromThread

class GraphWindow(QtGui.QTabWidget):
    def __init__(self, reactor, parent=None):
        super(GraphWindow, self).__init__(parent)
        self.reactor = reactor        
        self.initUI()
        self.show()
        
    def initUI(self):
        reactor = self.reactor

        self.graphDict = {}

        for gc in GUIConfig.tabs:
            if gc.graphs == 1: # standalone graph
                name = gc.name
                if gc.isScrolling:
                    g = ScrollingGraph(name, reactor)
                else:
                    g = Graph(name, reactor)
                self.graphDict[name] = g
                self.addTab(g, name)
                g.set_ylimits(gc.ylim)

            if gc.graphs == 2: # double graph
                gcli = [gc.config1, gc.config2]
                gli = []
                for config in gcli:
                    name = config.name
                    if config.isScrolling:
                        g = ScrollingGraph(name, reactor)
                    else:
                        g = Graph(name, reactor)
                    g.set_ylimits(config.ylim)
                    self.graphDict[name] = g
                    gli.append(g)
                self.addTab(DoubleGraphWindow(gli[0], gli[1], reactor), gc.tab)

    def insert_tab(self, t):
        g = Graph(t, reactor)
        self.graphDict[t] = g
        self.addTab(g, t)
        
    def closeEvent(self, x):
        self.reactor.stop()

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    import qt4reactor
    qt4reactor.install()
    from twisted.internet import reactor
    main = GraphWindow(reactor)
    main.show()
    #sys.exit(app.exec_())
    reactor.run()

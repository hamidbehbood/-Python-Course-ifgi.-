# Import of the necessary modules
from qgis.PyQt.QtCore import QUrl
from qgis.PyQt.QtWebKitWidgets import QWebView

# Creation of a QWebView instance
myWV = QWebView(None)

# Loading the URL with a dynamic parameter from the feature
myWV.load(QUrl('https://wikipedia.org/wiki/[%Name%]'))

# Show the final window
myWV.show()
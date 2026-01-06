"""
	Venom Add-on
"""

from resources.lib.modules.control import addonPath, addonId, getzwpseudoVersion, joinPath
from resources.lib.windows.textviewer import TextViewerXML


def get(file):
	zwpseudo_path = addonPath(addonId())
	zwpseudo_version = getzwpseudoVersion()
	helpFile = joinPath(zwpseudo_path, 'resources', 'help', file + '.txt')
	f = open(helpFile, 'r', encoding='utf-8', errors='ignore')
	text = f.read()
	f.close()
	heading = '[B]zwpseudo -  v%s - %s[/B]' % (zwpseudo_version, file)
	windows = TextViewerXML('textviewer.xml', zwpseudo_path, heading=heading, text=text)
	windows.run()
	del windows

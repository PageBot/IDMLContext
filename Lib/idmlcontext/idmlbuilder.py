#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens
#     www.pagebot.io
#     Licensed under MIT conditions
#
#     Supporting DrawBot, www.drawbot.com
#     Supporting Flat, xxyxyz.org/flat
#     Supporting usage of InDesign API-scripting
# -----------------------------------------------------------------------------
#
#     idmlbuilder.py
#
import codecs
import os, shutil
import zipfile
from lxml import etree

from pagebot.contexts.xml.xmlbuilder import XmlBuilder
from idmlcontext.objects.designmap import DesignMap

class IdmlBuilder(XmlBuilder):
    """TODO: Implement functions to make it work.
    """
    PB_ID = 'idml'

    def __init__(self):
        self.designMap = DesignMap()
        self.xmlNodes = {}
        self.masterSpreads = []
        self.spreads = []
        self.stories = []
        self.resources = {}
        self.metaInfo = {}

    def rect(self, x, y, w, h):
        pass

    def lineDash(self, line):
        pass

    def line(self, p1, p2):
        pass

    def save(self):
        pass

    def restore(self):
        pass

    def newPage(self, w, h):
        pass
        
    def saveDocument(self, path):
        """Write the IDML file from idmlRoot, indicated by path.
        """
        tmpPath = path.replace('.idml', '.tmp')
        if os.path.exists(tmpPath):
            shutil.rmtree(tmpPath)
        os.mkdir(tmpPath)

        zf = zipfile.ZipFile(tmpPath + '.idml', mode='w') # Open export as Zip.

        filePath = '/mimetype'
        f = codecs.open(tmpPath + filePath, 'w', encoding='utf-8')
        f.write('application/vnd.adobe.indesign-idml-package')
        f.close()
        zf.write(tmpPath + filePath, arcname=filePath)

        #shutil.copy('../../Test/MagentaYellowRectangle/designmap.xml', tmpPath + '/designmap.xml')
        
        filePath = '/designmap.xml'
        f = codecs.open(tmpPath + filePath, 'w', encoding='utf-8')
        self.designMap.writePreXml(f)
        self.designMap.writeXml(f)
        f.close()
        zf.write(tmpPath + filePath, arcname=filePath)
        
        os.mkdir(tmpPath + '/META-INF')

        for infoName in self.metaInfo.keys():
            filePath = '/META-INF/%s.xml' % infoName
            f = codecs.open(tmpPath + filePath, 'w', encoding='utf-8')
            self.metaInfo[infoName].writePreXml(f)
            self.metaInfo[infoName].writeXml(f)
            f.close()
            zf.write(tmpPath + filePath, arcname=filePath)

        os.mkdir(tmpPath + '/XML')

        for fileName in ('Tags', 'BackingStory'):
            filePath = '/XML/%s.xml' % fileName
            f = codecs.open(tmpPath + filePath, 'w', encoding='utf-8')
            if fileName in self.xmlNodes:
                self.xmlNodes[fileName].writePreXml(f)
                self.xmlNodes[fileName].writeXml(f)
            f.close()
            zf.write(tmpPath + filePath, arcname=filePath)

        os.mkdir(tmpPath + '/Spreads')

        #shutil.copy('../../Test/MagentaYellowRectangle/Spreads/Spread_udc.xml', tmpPath + '/Spreads/Spread_udc.xml')
        for spread in self.spreads:
            filePath = '/' + spread.fileName
            f = codecs.open(tmpPath + filePath, 'w', encoding='utf-8')
            spread.writePreXml(f)
            spread.writeXml(f)
            f.close()
            zf.write(tmpPath + filePath, arcname=filePath)
        
        os.mkdir(tmpPath + '/MasterSpreads')

        for masterSpread in self.masterSpreads:
            filePath = '/' + masterSpread.fileName
            f = codecs.open(tmpPath + filePath, 'w', encoding='utf-8')
            masterSpread.writePreXml(f)
            masterSpread.writeXml(f)
            f.close()
            zf.write(tmpPath + filePath, arcname=filePath)

        os.mkdir(tmpPath + '/Resources')

        for fileName in ('Fonts', 'Graphic', 'Preferences', 'Styles'):
            filePath = '/Resources/%s.xml' % fileName
            f = codecs.open(tmpPath + filePath, 'w', encoding='utf-8')
            if fileName in self.resources:
                self.resources[fileName].writePreXml(f)
                self.resources[fileName].writeXml(f)
            f.close()
            zf.write(tmpPath + filePath, arcname=filePath)

        os.mkdir(tmpPath + '/Stories')

        for story in self.stories:
            filePath = '/' + story.fileName
            f = codecs.open(tmpPath + filePath, 'w', encoding='utf-8')
            story.writePreXml(f)
            story.writeXml(f)
            f.close()
            zf.write(tmpPath + filePath, arcname=filePath)
        zf.close()

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])

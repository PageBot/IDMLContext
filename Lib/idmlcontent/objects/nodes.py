# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens
#     www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#
# -----------------------------------------------------------------------------
#

def asNumber(v):
    try:
        vInt = int(v)
        vFloat = float(v)
        if vInt == vFloat:
            v = vInt
        else:
            v = vFloat
    except ValueError:
        pass
    return v

class IdmlNode:
    TAG = None
    PRE_XML = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>']

    def __init__(self, fileName=None, name=None, nsmap=None, prefix=None, 
            nodes=None, text=None, tail=None, attributes=None, **kwargs):
        if name is None:
            name = self.__class__.__name__
        #print('===', name, fileName)
        self.fileName = fileName
        self.tag = self.TAG or name
        self.name = name
        self.nsmap = nsmap
        self.prefix = prefix
        self.text = text
        self.tail = tail
        if nodes is None:
            nodes = []
        self.nodes = nodes
        self.attrs = {}
        if attributes is None:
            attributes = {}
        for attrName, value in attributes.items():
            if value == 'true':
                value = True
            elif value == 'false':
                value = False
            else:
                value = asNumber(value)
            self.attrs[attrName] = value

    def __getitem__(self, index):
        return self.elements[index]

    def __repr__(self):
        return '<%s>' % self.tag

    def writePreXml(self, f):
        for preXml in self.PRE_XML:
            f.write(preXml + '\n')

    def writeXml(self, f, tab=0):
        s = '%s<' % (tab*'\t')
        if self.prefix:
            s += self.prefix + ':'
        s += self.tag
        if tab == 0 and self.nsmap:
            for nsKey, nsValue in self.nsmap.items():
                if nsKey is None:
                    s += ' xmlns="%s"' % nsValue
                else:
                    s += ' xmlns:%s="%s"' % (nsKey, nsValue)
        for attrName, value in self.attrs.items():
            if value in (True, False):
                value = {True:'true',False:'false'}[value]
            elif isinstance(value, str):
                value = value.replace('&','&amp;') # Order matters
                value = value.replace('"','&quot;')  
                value = value.replace('<','&lt;')  
                value = value.replace('>','&gt;')  
            s += ' %s="%s"' % (attrName, value)
        if self.text or self.nodes:
            s += '>\n'
            f.write(s)
            if self.text is not None:
                f.write(self.text.strip())
            for node in self.nodes:
                node.writeXml(f, tab+1)
            if self.nodes:
                s = tab*'\t'
            else:
                s = ''
            s += '</'
            if self.prefix:
                s += self.prefix + ':'
            s += '%s>\n' % self.tag
            f.write(s)
        else:
            s += '/>\n'
            f.write(s)
        if self.tail is not None:
            f.write(self.tail) 

class Page(IdmlNode):
    def __init__(self, **kwargs):
        IdmlNode.__init__(self,  **kwargs)

class DesignMap(IdmlNode):
    TAG = 'Document'
    PRE_XML = [
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
        '<?aid style="50" type="document" readerVersion="6.0" featureSet="257" product="14.0(324)"?>'
    ]
    def __init__(self, attributes=None, **kwargs):
        if attributes is None:
            attributes = {}
            attributes['xmlns:idPkg'] = "http://ns.adobe.com/AdobeInDesign/idml/1.0/packaging"
            attributes['DOMVersion'] = "14.0"
            attributes['Self'] = "d"
            attributes['StoryList'] = "u91"
            attributes['Name'] = "MagentaYellowRectangle.indd"
            attributes['ZeroPoint'] = "0 0" 
            attributes['ActiveLayer'] = "ub1" 
            attributes['CMYKProfile'] = "U.S. Web Coated (SWOP) v2"
            attributes['RGBProfile'] = "sRGB IEC61966-2.1"
            attributes['SolidColorIntent'] = "UseColorSettings"
            attributes['AfterBlendingIntent'] = "UseColorSettings"
            attributes['DefaultImageIntent'] = "UseColorSettings"
            attributes['RGBPolicy'] = "PreserveEmbeddedProfiles"
            attributes['CMYKPolicy'] = "CombinationOfPreserveAndSafeCmyk"
            attributes['AccurateLABSpots'] = False
        IdmlNode.__init__(self, attributes=attributes, **kwargs)

        properties = Properties(
            nodes=[Label(
                nodes=[KeyValuePair(attributes=dict(
                    Key="kAdobeDPS_Version", Value=2
                ))]
            )]
        )
        self.nodes.append(properties)
        self.nodes.append(Language(attributes=dict(Self="Language/$ID/English%3a USA",
            Name="$ID/English: USA",
            SingleQuotes="‘’",
            DoubleQuotes="“”",
            PrimaryLanguageName="$ID/English",
            SublanguageName="$ID/USA",
            Id=269,
            HyphenationVendor="Hunspell",
            SpellingVendor="Hunspell")))
        self.nodes.append(idPkg_Graphic(attributes=dict(src='Resources/Graphic.xml')))
        self.nodes.append(idPkg_Fonts(attributes=dict(src='Resources/Fonts.xml')))
        self.nodes.append(idPkg_Styles(attributes=dict(src='Resources/Styles.xml')))
        self.nodes.append(NumberingList(attributes=dict(
            Self="NumberingList/$ID/[Default]",
            Name="$ID/[Default]",
            ContinueNumbersAcrossStories=False,
            ContinueNumbersAcrossDocuments=False)))
        
        namedGrid = NamedGrid(attributes=dict(
            Self="NamedGrid/$ID/[Page Grid]",
            Name="$ID/[Page Grid]"),
            nodes=[GridDataInformation(attributes=dict(
                FontStyle="Regular",
                PointSize=12,
                CharacterAki=0,
                LineAki=9,
                HorizontalScale=100,
                VerticalScale=100,
                LineAlignment="LeftOrTopLineJustify",
                GridAlignment="AlignEmCenter",
                CharacterAlignment="AlignEmCenter",
                ),
                nodes=[Properties(nodes=[AppliedFont(attributes=dict(type='string', value='Minion Pro'))])]
            )]
        )
        self.nodes.append(namedGrid)
        self.nodes.append(idPkg_Preferences(attributes=dict(src='Resources/Preferences.xml')))

        self.nodes.append(EndnoteOption(attributes=dict(
            EndnoteTitle="Endnotes",
            EndnoteTitleStyle="ParagraphStyle/$ID/NormalParagraphStyle",
            StartEndnoteNumberAt="1",
            EndnoteMarkerStyle="CharacterStyle/$ID/[No character style]",
            EndnoteTextStyle="ParagraphStyle/$ID/NormalParagraphStyle",
            EndnoteSeparatorText="&#x9;",
            EndnotePrefix="",
            EndnoteSuffix=""),
            nodes=[Properties(nodes=[
                EndnoteNumberingStyle(attributes=dict(type='enumeration', value='Arabic')),
                RestartEndnoteNumbering(attributes=dict(type='enumeration', value='Continuous')),
                EndnoteMarkerPositioning(attributes=dict(type='enumeration', value='SuperscriptMarker')),
                ScopeValue(attributes=dict(type='enumeration', value='EndnoteDocumentScope')),
                FrameCreateOption(attributes=dict(type='enumeration', value='NewPage')),
                ShowEndnotePrefixSuffix(attributes=dict(type='enumeration', value='NoPrefixSuffix')),
            ])]
        ))
        self.nodes.append(TextFrameFootnoteOptionsObject(attributes=dict(
            EnableOverrides=False,
            SpanFootnotesAcross=False,
            MinimumSpacingOption=12,
            SpaceBetweenFootnotes=6,
        )))
        self.nodes.append(LinkedStoryOption(attributes=dict(
            UpdateWhileSaving=False,
            WarnOnUpdateOfEditedStory=True,
            RemoveForcedLineBreaks=False,
            ApplyStyleMappings=False,
        )))
        self.nodes.append(LinkedPageItemOption(attributes=dict(
            UpdateLinkWhileSaving=False,
            WarnOnUpdateOfEditedPageItem=True,
            PreserveSizeAndShape=False,
            PreserveAppearance=False,
            PreserveInteractivity=False,
            PreserveFrameContent=False,
            PreserveOthers=False,
        )))
        self.nodes.append(TaggedPDFPreference(attributes=dict(
            StructureOrder="UseXMLStructure",
        )))
        self.nodes.append(WatermarkPreference(attributes=dict(
            WatermarkVisibility=False,
            WatermarkDoPrint=False,
            WatermarkDrawInBack=True,
            WatermarkText="",
            WatermarkFontFamily="Minion Pro",
            WatermarkFontStyle="Regular",
            WatermarkFontPointSize=48,
            WatermarkOpacity=50,
            WatermarkRotation=0,
            WatermarkHorizontalPosition="WatermarkHCenter",
            WatermarkHorizontalOffset=0,
            WatermarkVerticalPosition="WatermarkVCenter",
            WatermarkVerticalOffset=0,
            ),
            nodes=[Properties(nodes=[WatermarkFontColor(attributes=dict(
                type='enumeration', value='Black'))])]
        ))
        self.nodes.append(ConditionalTextPreference(attributes=dict(
            ShowConditionIndicators="ShowIndicators",
            ActiveConditionSet="n"
        )))
        self.nodes.append(AdjustLayoutPreference(attributes=dict(
            EnableAdjustLayout=False,
            AllowLockedObjectsToAdjust=True,
            AllowFontSizeAndLeadingAdjustment=False,
            ImposeFontSizeRestriction=False,
            MinimumFontSize=6,
            MaximumFontSize=324,
            EnableAutoAdjustMargins=False,
        )))
        self.nodes.append(HTMLFXLExportPreference(attributes=dict(
            EpubPageRange="",
            EpubPageRangeFormat="ExportAllPages",
        )))
        self.nodes.append(PublishExportPreference(attributes=dict(
            PublishCover="FirstPage",
            CoverImageFile="",
            PublishPageRange="",
            PublishPageRangeFormat="ExportAllPages",
            ImageConversion="Automatic",
            ImageExportResolution="Ppi96",
            PublishDescription="",
            PublishFileName="",
            PublishFormat="PublishByPages",
            CoverPage="$ID/",
            GIFOptionsPalette="AdaptivePalette",
            JPEGOptionsQuality="High",
            PublishPdf=False
        )))
        self.nodes.append(TextVariable(attributes=dict(
            Self="dTextVariablen&lt;?AID 001b?&gt;TV XRefChapterNumber",
            Name="&lt;?AID 001b?&gt;TV XRefChapterNumber",
            VariableType="XrefChapterNumberType",
        )))
        self.nodes.append(TextVariable(attributes=dict(
            Self="dTextVariablen&lt;?AID 001b?&gt;TV XRefPageNumber",
            Name="&lt;?AID 001b?&gt;TV XRefPageNumber",
            VariableType="XrefPageNumberType",
        )))
        self.nodes.append(TextVariable(attributes=dict(
            Self="dTextVariablenChapter Number",
            Name="Chapter Number",
            VariableType="ChapterNumberType",
            ),
            nodes=[ChapterNumberVariablePreference(attributes=dict(
                TextBefore="",
                Format="Current",
                TextAfter="",
            ))]
        ))
        self.nodes.append(TextVariable(attributes=dict(
            Self="dTextVariablenCreation Date",
            Name="Creation Date",
            VariableType="CreationDateType",
            ),
            nodes=[DateVariablePreference(attributes=dict(
                TextBefore="",
                Format="MM/dd/yy",
                TextAfter="",
            ))]
        ))
        """
    <TextVariable Self="dTextVariablenFile Name" Name="File Name" VariableType="FileNameType">
        <FileNameVariablePreference TextBefore="" IncludePath="false" IncludeExtension="false" TextAfter="" />
    </TextVariable>
    <TextVariable Self="dTextVariablenImage Name" Name="Image Name" VariableType="LiveCaptionType">
        <CaptionMetadataVariablePreference TextBefore="" MetadataProviderName="$ID/#LinkInfoNameStr" TextAfter="" />
    </TextVariable>
    <TextVariable Self="dTextVariablenLast Page Number" Name="Last Page Number" VariableType="LastPageNumberType">
        <PageNumberVariablePreference TextBefore="" Format="Current" TextAfter="" Scope="SectionScope" />
    </TextVariable>
    <TextVariable Self="dTextVariablenModification Date" Name="Modification Date" VariableType="ModificationDateType">
        <DateVariablePreference TextBefore="" Format="MMMM d, yyyy h:mm aa" TextAfter="" />
    </TextVariable>
    <TextVariable Self="dTextVariablenOutput Date" Name="Output Date" VariableType="OutputDateType">
        <DateVariablePreference TextBefore="" Format="MM/dd/yy" TextAfter="" />
    </TextVariable>
    <TextVariable Self="dTextVariablenRunning Header" Name="Running Header" VariableType="MatchParagraphStyleType">
        <MatchParagraphStylePreference TextBefore="" TextAfter="" AppliedParagraphStyle="ParagraphStyle/$ID/NormalParagraphStyle" SearchStrategy="FirstOnPage" ChangeCase="None" DeleteEndPunctuation="false" />
    </TextVariable>
        """
        self.nodes.append(idPkg_Tags(attributes=dict(src="XML/Tags.xml")))

class Properties(IdmlNode):
    pass

class Label(IdmlNode):
    pass

class KeyValuePair(IdmlNode):
    pass

class Language(IdmlNode):
    pass

class idPkg_Graphic(IdmlNode):
    TAG = 'idPkg:Graphic'

class idPkg_Fonts(IdmlNode):
    TAG = 'idPkg:Fonts'

class idPkg_Styles(IdmlNode):
    TAG = 'idPkg:Styles'

class idPkg_Preferences(IdmlNode):
    TAG = 'idPkg:Preferences'

class idPkg_Tags(IdmlNode):
    TAG = 'idPkg:Tags'

class NumberingList(IdmlNode):
    pass

class NamedGrid(IdmlNode):
    pass

class GridDataInformation(IdmlNode):
    pass

class EndnoteOption(IdmlNode):
    pass

class TextFrameFootnoteOptionsObject(IdmlNode):
    pass

class LinkedStoryOption(IdmlNode):
    pass

class LinkedPageItemOption(IdmlNode):
    pass

class TaggedPDFPreference(IdmlNode):
    pass

class WatermarkPreference(IdmlNode):
    pass

class ConditionalTextPreference(IdmlNode):
    pass

class AdjustLayoutPreference(IdmlNode):
    pass

class HTMLFXLExportPreference(IdmlNode):
    pass

class PublishExportPreference(IdmlNode):
    pass

class TextVariable(IdmlNode):
    pass

class ChapterNumberVariablePreference(IdmlNode):
    pass

class DateVariablePreference(IdmlNode):
    pass


class IdmlValueNode(IdmlNode):
    def writeXml(self, f, tab=0):
        f.write(('\t'*tab) + '<%s type="%s">%s</%s>\n' % (
            self.tag, self.attrs['type'], self.attrs['value'], self.tag)
        )

class AppliedFont(IdmlValueNode):
    pass
class EndnoteNumberingStyle(IdmlValueNode):
    pass
class RestartEndnoteNumbering(IdmlValueNode):
    pass
class EndnoteMarkerPositioning(IdmlValueNode):
    pass
class ScopeValue(IdmlValueNode):
    pass
class FrameCreateOption(IdmlValueNode):
    pass
class ShowEndnotePrefixSuffix(IdmlValueNode):
    pass
class WatermarkFontColor(IdmlValueNode):
    pass

NODE_CLASSES = {
    # Expanding set of IdmlNode classes, that know more about their
    # content so the can generate, manipulate and validate. 
    'IdmlNode': IdmlNode,
    'Page': Page,
    'Document': DesignMap,
    'Properties': Properties,
    'Label': Label,
    'KeyValuePair': KeyValuePair,
    'Language': Language,
    'idPkg:Graphic': idPkg_Graphic,
    'idPkg:Fonts': idPkg_Fonts,
    'idPkg:Styles': idPkg_Styles,
    'NumberingList': NumberingList,
    'NamedGrid': NamedGrid,
    'GridDataInformation': GridDataInformation,
    'EndnoteOption': EndnoteOption,
    'AppliedFont': AppliedFont,
    'EndnoteNumberingStyle': EndnoteNumberingStyle,
    'RestartEndnoteNumbering': RestartEndnoteNumbering,
    'EndnoteMarkerPositioning': EndnoteMarkerPositioning,
    'ScopeValue': ScopeValue,
    'FrameCreateOption': FrameCreateOption,
    'ShowEndnotePrefixSuffix': ShowEndnotePrefixSuffix,
    'TextFrameFootnoteOptionsObject': TextFrameFootnoteOptionsObject,
    'LinkedStoryOption': LinkedStoryOption,
    'LinkedPageItemOption': LinkedPageItemOption,
    'TaggedPDFPreference': TaggedPDFPreference,
    'WatermarkPreference': WatermarkPreference,
    'WatermarkFontColor': WatermarkFontColor,
    'ConditionalTextPreference': ConditionalTextPreference,
    'AdjustLayoutPreference': AdjustLayoutPreference,
    'HTMLFXLExportPreference': HTMLFXLExportPreference,
    'PublishExportPreference': PublishExportPreference,
    'ChapterNumberVariablePreference': ChapterNumberVariablePreference,
    'DateVariablePreference': DateVariablePreference,
}


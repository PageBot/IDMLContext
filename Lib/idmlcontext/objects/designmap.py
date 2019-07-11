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
from idmlcontext.objects.nodes import *

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


if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])

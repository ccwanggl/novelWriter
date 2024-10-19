"""
novelWriter – DocX Text Converter
=================================

File History:
Created: 2024-10-18 [2.6b1] ToDocX
Created: 2024-10-18 [2.6b1] DocXParagraph

This file is a part of novelWriter
Copyright 2018–2024, Veronica Berglyd Olsen

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.
"""
from __future__ import annotations

import logging
import xml.etree.ElementTree as ET

from datetime import datetime
from pathlib import Path
from typing import NamedTuple
from zipfile import ZipFile

from novelwriter import __version__
from novelwriter.common import firstFloat, xmlIndent, xmlSubElem
from novelwriter.constants import nwHeadFmt, nwKeyWords, nwLabels, nwStyles
from novelwriter.core.project import NWProject
from novelwriter.formats.tokenizer import T_Formats, Tokenizer

logger = logging.getLogger(__name__)

# Types and Relationships
WORD_BASE = "application/vnd.openxmlformats-officedocument"
RELS_TYPE = "application/vnd.openxmlformats-package.relationships+xml"
REL_CORE = "http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties"
REL_BASE = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"

# Main XML NameSpaces
PROPS_NS = "http://schemas.openxmlformats.org/officeDocument/2006/extended-properties"
TYPES_NS = "http://schemas.openxmlformats.org/package/2006/content-types"
RELS_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
XML_NS = {
    "w":       W_NS,
    "cp":      "http://schemas.openxmlformats.org/package/2006/metadata/core-properties",
    "dc":      "http://purl.org/dc/elements/1.1/",
    "xsi":     "http://www.w3.org/2001/XMLSchema-instance",
    "xml":     "http://www.w3.org/XML/1998/namespace",
    "dcterms": "http://purl.org/dc/terms/",
}
for ns, uri in XML_NS.items():
    ET.register_namespace(ns, uri)


def _wTag(tag: str) -> str:
    """Assemble namespace and tag name for standard w namespace."""
    return f"{{{W_NS}}}{tag}"


def _mkTag(ns: str, tag: str) -> str:
    """Assemble namespace and tag name."""
    if uri := XML_NS.get(ns, ""):
        return f"{{{uri}}}{tag}"
    logger.warning("Missing xml namespace '%s'", ns)
    return tag


# Formatting Codes
X_BLD = 0x001  # Bold format
X_ITA = 0x002  # Italic format
X_DEL = 0x004  # Strikethrough format
X_UND = 0x008  # Underline format
X_MRK = 0x010  # Marked format
X_SUP = 0x020  # Superscript
X_SUB = 0x040  # Subscript
X_DLG = 0x080  # Dialogue
X_DLA = 0x100  # Alt. Dialogue

# Formatting Masks
M_BLD = ~X_BLD
M_ITA = ~X_ITA
M_DEL = ~X_DEL
M_UND = ~X_UND
M_MRK = ~X_MRK
M_SUP = ~X_SUP
M_SUB = ~X_SUB
M_DLG = ~X_DLG
M_DLA = ~X_DLA

# DocX Styles
S_NORM  = "Normal"
S_TITLE = "Title"
S_HEAD1 = "Heading1"
S_HEAD2 = "Heading2"
S_HEAD3 = "Heading3"
S_HEAD4 = "Heading4"
S_SEP   = "Separator"
S_FIND  = "FirstLineIndent"
S_META  = "TextMeta"

# Colours
COL_HEAD_L12 = "2a6099"
COL_HEAD_L34 = "444444"
COL_DIALOG_M = "2a6099"
COL_DIALOG_A = "813709"
COL_META_TXT = "813709"
COL_MARK_TXT = "ffffa6"


class DocXParStyle(NamedTuple):

    name: str
    styleId: str
    size: float
    basedOn: str | None = None
    nextStyle: str | None = None
    before: float | None = None
    after: float | None = None
    line: float | None = None
    align: str | None = None
    default: bool = False
    level: int | None = None
    color: str | None = None


class ToDocX(Tokenizer):
    """Core: DocX Document Writer

    Extend the Tokenizer class to writer DocX Document files.
    """

    def __init__(self, project: NWProject) -> None:
        super().__init__(project)

        # XML
        self._dDoc  = ET.Element("")  # document.xml
        self._dStyl = ET.Element("")  # styles.xml

        self._xBody = ET.Element("")  # Text body

        # Properties
        self._headerFormat = ""
        self._pageOffset   = 0

        # Internal
        self._fontFamily = "Liberation Serif"
        self._fontSize   = 12.0
        self._dLanguage  = "en-GB"

        # Maps
        self._styles: dict[str, DocXParStyle] = {}

        return

    ##
    #  Setters
    ##

    def setLanguage(self, language: str | None) -> None:
        """Set language for the document."""
        if language:
            self._dLanguage = language
        return

    def setPageLayout(
        self, width: float, height: float, top: float, bottom: float, left: float, right: float
    ) -> None:
        """Set the document page size and margins in millimetres."""
        return

    def setHeaderFormat(self, format: str, offset: int) -> None:
        """Set the document header format."""
        self._headerFormat = format.strip()
        self._pageOffset = offset
        return

    ##
    #  Class Methods
    ##

    def _emToSz(self, scale: float) -> int:
        return int()

    def initDocument(self) -> None:
        """Initialises the DocX document structure."""

        self._fontFamily = self._textFont.family()
        self._fontSize = self._textFont.pointSizeF()

        self._dDoc  = ET.Element(_wTag("document"))
        self._dStyl = ET.Element(_wTag("styles"))

        self._xBody = xmlSubElem(self._dDoc, _wTag("body"))

        self._defaultStyles()
        self._useableStyles()

        return

    def doConvert(self) -> None:
        """Convert the list of text tokens into XML elements."""
        self._result = ""  # Not used, but cleared just in case

        # xText = self._xText
        for tType, _, tText, tFormat, tStyle in self._tokens:

            # Styles
            par = DocXParagraph()
            if tStyle is not None:
                if tStyle & self.A_LEFT:
                    par.setAlignment("left")
                elif tStyle & self.A_RIGHT:
                    par.setAlignment("right")
                elif tStyle & self.A_CENTRE:
                    par.setAlignment("center")
                # elif tStyle & self.A_JUSTIFY:
                #     oStyle.setTextAlign("justify")

                if tStyle & self.A_PBB:
                    par.setPageBreakBefore(True)
                if tStyle & self.A_PBA:
                    par.setPageBreakAfter(True)

                if tStyle & self.A_Z_BTMMRG:
                    par.setMarginBottom(0.0)
                if tStyle & self.A_Z_TOPMRG:
                    par.setMarginTop(0.0)

        #         if tStyle & self.A_IND_L:
        #             oStyle.setMarginLeft(self._fBlockIndent)
        #         if tStyle & self.A_IND_R:
        #             oStyle.setMarginRight(self._fBlockIndent)

            # Process Text Types
            if tType == self.T_TEXT:
                # Text indentation is processed here because there is a
                # dedicated pre-defined style for it
                # if tStyle & self.A_IND_T:
                # else:
                self._processFragments(par, S_NORM, tText, tFormat)

            elif tType == self.T_TITLE:
                tHead = tText.replace(nwHeadFmt.BR, "\n")
                self._processFragments(par, S_TITLE, tHead, tFormat)

            elif tType == self.T_HEAD1:
                tHead = tText.replace(nwHeadFmt.BR, "\n")
                self._processFragments(par, S_HEAD1, tHead, tFormat)

            elif tType == self.T_HEAD2:
                tHead = tText.replace(nwHeadFmt.BR, "\n")
                self._processFragments(par, S_HEAD2, tHead, tFormat)

            elif tType == self.T_HEAD3:
                tHead = tText.replace(nwHeadFmt.BR, "\n")
                self._processFragments(par, S_HEAD3, tHead, tFormat)

            elif tType == self.T_HEAD4:
                tHead = tText.replace(nwHeadFmt.BR, "\n")
                self._processFragments(par, S_HEAD4, tHead, tFormat)

            elif tType == self.T_SEP:
                self._processFragments(par, S_SEP, tText)

            elif tType == self.T_SKIP:
                self._processFragments(par, S_NORM, "")

            elif tType == self.T_SYNOPSIS and self._doSynopsis:
                tTemp, tFmt = self._formatSynopsis(tText, tFormat, True)
                self._processFragments(par, S_META, tTemp, tFmt)

            elif tType == self.T_SHORT and self._doSynopsis:
                tTemp, tFmt = self._formatSynopsis(tText, tFormat, False)
                self._processFragments(par, S_META, tTemp, tFmt)

            elif tType == self.T_COMMENT and self._doComments:
                tTemp, tFmt = self._formatComments(tText, tFormat)
                self._processFragments(par, S_META, tTemp, tFmt)

            elif tType == self.T_KEYWORD and self._doKeywords:
                tTemp, tFmt = self._formatKeywords(tText)
                self._processFragments(par, S_META, tTemp, tFmt)

            par.finalise(self._xBody)

        return

    def saveDocument(self, path: Path) -> None:
        """Save the data to a .docx file."""
        timeStamp = datetime.now().isoformat(sep="T", timespec="seconds")

        # .rels
        dRels = ET.Element("Relationships", attrib={"xmlns": RELS_NS})
        xmlSubElem(dRels, "Relationship", attrib={
            "Id": "rId1", "Type": REL_CORE, "Target": "docProps/core.xml",
        })
        xmlSubElem(dRels, "Relationship", attrib={
            "Id": "rId2", "Type": f"{REL_BASE}/extended-properties", "Target": "docProps/app.xml",
        })
        xmlSubElem(dRels, "Relationship", attrib={
            "Id": "rId3", "Type": f"{REL_BASE}/officeDocument", "Target": "word/document.xml",
        })

        # core.xml
        dCore = ET.Element("coreProperties")
        tsAttr = {_mkTag("xsi", "type"): "dcterms:W3CDTF"}
        xmlSubElem(dCore, _mkTag("dcterms", "created"), timeStamp, attrib=tsAttr)
        xmlSubElem(dCore, _mkTag("dcterms", "modified"), timeStamp, attrib=tsAttr)
        xmlSubElem(dCore, _mkTag("dc", "creator"), self._project.data.author)
        xmlSubElem(dCore, _mkTag("dc", "title"), self._project.data.name)
        xmlSubElem(dCore, _mkTag("dc", "creator"), self._project.data.author)
        xmlSubElem(dCore, _mkTag("dc", "language"), self._dLanguage)
        xmlSubElem(dCore, _mkTag("cp", "revision"), str(self._project.data.saveCount))
        xmlSubElem(dCore, _mkTag("cp", "lastModifiedBy"), self._project.data.author)

        # app.xml
        dApp = ET.Element("Properties", attrib={"xmlns": PROPS_NS})
        xmlSubElem(dApp, "TotalTime", self._project.data.editTime // 60)
        xmlSubElem(dApp, "Application", f"novelWriter/{__version__}")
        if count := self._counts.get("allWords"):
            xmlSubElem(dApp, "Words", count)
        if count := self._counts.get("textWordChars"):
            xmlSubElem(dApp, "Characters", count)
        if count := self._counts.get("textChars"):
            xmlSubElem(dApp, "CharactersWithSpaces", count)
        if count := self._counts.get("paragraphCount"):
            xmlSubElem(dApp, "Paragraphs", count)

        # document.xml.rels
        dDRels = ET.Element("Relationships", attrib={"xmlns": RELS_NS})
        xmlSubElem(dDRels, "Relationship", attrib={
            "Id": "rId1", "Type": f"{REL_BASE}/styles", "Target": "styles.xml",
        })

        # [Content_Types].xml
        dCont = ET.Element("Types", attrib={"xmlns": TYPES_NS})
        xmlSubElem(dCont, "Default", attrib={
            "Extension": "xml", "ContentType": "application/xml",
        })
        xmlSubElem(dCont, "Default", attrib={
            "Extension": "rels", "ContentType": RELS_TYPE,
        })
        xmlSubElem(dCont, "Override", attrib={
            "PartName": "/_rels/.rels",
            "ContentType": RELS_TYPE,
        })
        xmlSubElem(dCont, "Override", attrib={
            "PartName": "/docProps/core.xml",
            "ContentType": f"{WORD_BASE}.extended-properties+xml",
        })
        xmlSubElem(dCont, "Override", attrib={
            "PartName": "/docProps/app.xml",
            "ContentType": "application/vnd.openxmlformats-package.core-properties+xml",
        })
        xmlSubElem(dCont, "Override", attrib={
            "PartName": "/word/_rels/document.xml.rels",
            "ContentType": RELS_TYPE,
        })
        xmlSubElem(dCont, "Override", attrib={
            "PartName": "/word/document.xml",
            "ContentType": f"{WORD_BASE}.wordprocessingml.document.main+xml",
        })
        xmlSubElem(dCont, "Override", attrib={
            "PartName": "/word/styles.xml",
            "ContentType": f"{WORD_BASE}.wordprocessingml.styles+xml",
        })

        def xmlToZip(name: str, xObj: ET.Element, zipObj: ZipFile) -> None:
            with zipObj.open(name, mode="w") as fObj:
                xml = ET.ElementTree(xObj)
                xmlIndent(xml)
                xml.write(fObj, encoding="utf-8", xml_declaration=True)

        with ZipFile(path, mode="w") as outZip:
            xmlToZip("_rels/.rels", dRels, outZip)
            xmlToZip("docProps/core.xml", dCore, outZip)
            xmlToZip("docProps/app.xml", dApp, outZip)
            xmlToZip("word/_rels/document.xml.rels", dDRels, outZip)
            xmlToZip("word/document.xml", self._dDoc, outZip)
            xmlToZip("word/styles.xml", self._dStyl, outZip)
            xmlToZip("[Content_Types].xml", dCont, outZip)

        return

    ##
    #  Internal Functions
    ##

    def _formatSynopsis(self, text: str, fmt: T_Formats, synopsis: bool) -> tuple[str, T_Formats]:
        """Apply formatting to synopsis lines."""
        name = self._localLookup("Synopsis" if synopsis else "Short Description")
        shift = len(name) + 2
        rTxt = f"{name}: {text}"
        rFmt: T_Formats = [(0, self.FMT_B_B, ""), (len(name) + 1, self.FMT_B_E, "")]
        rFmt.extend((p + shift, f, d) for p, f, d in fmt)
        return rTxt, rFmt

    def _formatComments(self, text: str, fmt: T_Formats) -> tuple[str, T_Formats]:
        """Apply formatting to comments."""
        name = self._localLookup("Comment")
        shift = len(name) + 2
        rTxt = f"{name}: {text}"
        rFmt: T_Formats = [(0, self.FMT_B_B, ""), (len(name) + 1, self.FMT_B_E, "")]
        rFmt.extend((p + shift, f, d) for p, f, d in fmt)
        return rTxt, rFmt

    def _formatKeywords(self, text: str) -> tuple[str, T_Formats]:
        """Apply formatting to keywords."""
        valid, bits, _ = self._project.index.scanThis("@"+text)
        if not valid or not bits or bits[0] not in nwLabels.KEY_NAME:
            return "", []

        rTxt = f"{self._localLookup(nwLabels.KEY_NAME[bits[0]])}: "
        rFmt: T_Formats = [(0, self.FMT_B_B, ""), (len(rTxt) - 1, self.FMT_B_E, "")]
        if len(bits) > 1:
            if bits[0] == nwKeyWords.TAG_KEY:
                rTxt += bits[1]
            else:
                rTxt += ", ".join(bits[1:])

        return rTxt, rFmt

    def _processFragments(
        self, par: DocXParagraph, pStyle: str, text: str, tFmt: T_Formats | None = None
    ) -> None:
        """Apply formatting tags to text."""
        par.setStyle(self._styles.get(pStyle))
        xFmt = 0x00
        fStart = 0
        for fPos, fFmt, fData in tFmt or []:

            par.addContent(self._textRunToXml(text[fStart:fPos], xFmt))

            if fFmt == self.FMT_B_B:
                xFmt |= X_BLD
            elif fFmt == self.FMT_B_E:
                xFmt &= M_BLD
            elif fFmt == self.FMT_I_B:
                xFmt |= X_ITA
            elif fFmt == self.FMT_I_E:
                xFmt &= M_ITA
            elif fFmt == self.FMT_D_B:
                xFmt |= X_DEL
            elif fFmt == self.FMT_D_E:
                xFmt &= M_DEL
            elif fFmt == self.FMT_U_B:
                xFmt |= X_UND
            elif fFmt == self.FMT_U_E:
                xFmt &= M_UND
            elif fFmt == self.FMT_M_B:
                xFmt |= X_MRK
            elif fFmt == self.FMT_M_E:
                xFmt &= M_MRK
            elif fFmt == self.FMT_SUP_B:
                xFmt |= X_SUP
            elif fFmt == self.FMT_SUP_E:
                xFmt &= M_SUP
            elif fFmt == self.FMT_SUB_B:
                xFmt |= X_SUB
            elif fFmt == self.FMT_SUB_E:
                xFmt &= M_SUB
            elif fFmt == self.FMT_DL_B:
                xFmt |= X_DLG
            elif fFmt == self.FMT_DL_E:
                xFmt &= M_DLG
            elif fFmt == self.FMT_ADL_B:
                xFmt |= X_DLA
            elif fFmt == self.FMT_ADL_E:
                xFmt &= M_DLA
            # elif fmt == self.FMT_FNOTE:
            #     xNode = self._generateFootnote(fData)
            elif fFmt == self.FMT_STRIP:
                pass

            # Move pos for next pass
            fStart = fPos

        if rest := text[fStart:]:
            par.addContent(self._textRunToXml(rest, xFmt))

        return

    def _textRunToXml(self, text: str, fmt: int) -> ET.Element:
        """Encode the text run into XML."""
        run = ET.Element(_wTag("r"))
        rPr = xmlSubElem(run, _wTag("rPr"))
        if fmt & X_BLD == X_BLD:
            xmlSubElem(rPr, _wTag("b"))
        if fmt & X_ITA == X_ITA:
            xmlSubElem(rPr, _wTag("i"))
        if fmt & X_UND == X_UND:
            xmlSubElem(rPr, _wTag("u"), attrib={_wTag("val"): "single"})
        if fmt & X_MRK == X_MRK:
            xmlSubElem(rPr, _wTag("shd"), attrib={
                _wTag("fill"): COL_MARK_TXT, _wTag("val"): "clear",
            })
        if fmt & X_DEL == X_DEL:
            xmlSubElem(rPr, _wTag("strike"))
        if fmt & X_SUP == X_SUP:
            xmlSubElem(rPr, _wTag("vertAlign"), attrib={_wTag("val"): "superscript"})
        if fmt & X_SUB == X_SUB:
            xmlSubElem(rPr, _wTag("vertAlign"), attrib={_wTag("val"): "subscript"})
        if fmt & X_DLG == X_DLG:
            xmlSubElem(rPr, _wTag("color"), attrib={_wTag("val"): COL_DIALOG_M})
        if fmt & X_DLA == X_DLA:
            xmlSubElem(rPr, _wTag("color"), attrib={_wTag("val"): COL_DIALOG_A})

        remaining = text
        while (parts := remaining.partition("\n"))[0]:
            segment = parts[0]
            attr = {}
            if len(segment) != len(segment.strip()):
                attr[_mkTag("xml", "space")] = "preserve"
            xmlSubElem(run, _wTag("t"), segment, attrib=attr)
            if parts[1]:
                xmlSubElem(run, _wTag("br"))
            remaining = parts[2]

        return run

    ##
    #  Style Elements
    ##

    def _defaultStyles(self) -> None:
        """Set the default styles."""
        xStyl = xmlSubElem(self._dStyl, _wTag("docDefaults"))
        xRDef = xmlSubElem(xStyl, _wTag("rPrDefault"))
        xPDef = xmlSubElem(xStyl, _wTag("pPrDefault"))
        xRPr = xmlSubElem(xRDef, _wTag("rPr"))
        xPPr = xmlSubElem(xPDef, _wTag("pPr"))

        size = str(int(2.0 * self._fontSize))
        line = str(int(20.0 * self._lineHeight * self._fontSize))

        xmlSubElem(xRPr, _wTag("rFonts"), attrib={
            _wTag("ascii"): self._fontFamily,
            _wTag("hAnsi"): self._fontFamily,
            _wTag("cs"): self._fontFamily,
        })
        xmlSubElem(xRPr, _wTag("sz"), attrib={_wTag("val"): size})
        xmlSubElem(xRPr, _wTag("szCs"), attrib={_wTag("val"): size})
        xmlSubElem(xRPr, _wTag("lang"), attrib={_wTag("val"): self._dLanguage})
        xmlSubElem(xPPr, _wTag("spacing"), attrib={_wTag("line"): line})

        return

    def _useableStyles(self) -> None:
        """Set the usable styles."""
        hScale = self._scaleHeads
        hColor = self._colorHeads
        fSz = self._fontSize
        fSz0 = (nwStyles.H_SIZES[0] * fSz) if hScale else fSz
        fSz1 = (nwStyles.H_SIZES[1] * fSz) if hScale else fSz
        fSz2 = (nwStyles.H_SIZES[2] * fSz) if hScale else fSz
        fSz3 = (nwStyles.H_SIZES[3] * fSz) if hScale else fSz
        fSz4 = (nwStyles.H_SIZES[4] * fSz) if hScale else fSz

        # Add Normal Style
        self._addParStyle(DocXParStyle(
            name="Normal",
            styleId=S_NORM,
            size=fSz,
            default=True,
            before=fSz * self._marginText[0],
            after=fSz * self._marginText[1],
            line=fSz * self._lineHeight,
        ))

        # Add Title
        self._addParStyle(DocXParStyle(
            name="Title",
            styleId=S_TITLE,
            size=fSz0,
            basedOn=S_NORM,
            nextStyle=S_NORM,
            before=fSz * self._marginTitle[0],
            after=fSz * self._marginTitle[1],
            line=fSz0 * self._lineHeight,
            level=0,
        ))

        # Add Heading 1
        self._addParStyle(DocXParStyle(
            name="Heading 1",
            styleId=S_HEAD1,
            size=fSz1,
            basedOn=S_NORM,
            nextStyle=S_NORM,
            before=fSz * self._marginHead1[0],
            after=fSz * self._marginHead1[1],
            line=fSz1 * self._lineHeight,
            level=0,
            color=COL_HEAD_L12 if hColor else None,
        ))

        # Add Heading 2
        self._addParStyle(DocXParStyle(
            name="Heading 2",
            styleId=S_HEAD2,
            size=fSz2,
            basedOn=S_NORM,
            nextStyle=S_NORM,
            before=fSz * self._marginHead2[0],
            after=fSz * self._marginHead2[1],
            line=fSz2 * self._lineHeight,
            level=1,
            color=COL_HEAD_L12 if hColor else None,
        ))

        # Add Heading 3
        self._addParStyle(DocXParStyle(
            name="Heading 3",
            styleId=S_HEAD3,
            size=fSz3,
            basedOn=S_NORM,
            nextStyle=S_NORM,
            before=fSz * self._marginHead3[0],
            after=fSz * self._marginHead3[1],
            line=fSz3 * self._lineHeight,
            level=1,
            color=COL_HEAD_L34 if hColor else None,
        ))

        # Add Heading 4
        self._addParStyle(DocXParStyle(
            name="Heading 4",
            styleId=S_HEAD4,
            size=fSz4,
            basedOn=S_NORM,
            nextStyle=S_NORM,
            before=fSz * self._marginHead4[0],
            after=fSz * self._marginHead4[1],
            line=fSz4 * self._lineHeight,
            level=1,
            color=COL_HEAD_L34 if hColor else None,
        ))

        # Add Separator
        self._addParStyle(DocXParStyle(
            name="Separator",
            styleId=S_SEP,
            size=fSz,
            basedOn=S_NORM,
            nextStyle=S_NORM,
            before=fSz * self._marginSep[0],
            after=fSz * self._marginSep[1],
            line=fSz * self._lineHeight,
            align="center",
        ))

        # Add Text Meta Style
        self._addParStyle(DocXParStyle(
            name="Text Meta",
            styleId=S_META,
            size=fSz,
            basedOn=S_NORM,
            nextStyle=S_NORM,
            before=fSz * self._marginMeta[0],
            after=fSz * self._marginMeta[1],
            line=fSz * self._lineHeight,
            color=COL_META_TXT,
        ))

        return

    def _addParStyle(self, style: DocXParStyle) -> None:
        """Add a paragraph style."""
        sAttr = {}
        sAttr[_wTag("type")] = "paragraph"
        sAttr[_wTag("styleId")] = style.styleId
        if style.default:
            sAttr[_wTag("default")] = "1"

        size = firstFloat(style.size, self._fontSize)

        xStyl = xmlSubElem(self._dStyl, _wTag("style"), attrib=sAttr)
        xmlSubElem(xStyl, _wTag("name"), attrib={_wTag("val"): style.name})
        if style.basedOn:
            xmlSubElem(xStyl, _wTag("basedOn"), attrib={_wTag("val"): style.basedOn})
        if style.nextStyle:
            xmlSubElem(xStyl, _wTag("next"), attrib={_wTag("val"): style.nextStyle})
        if style.level is not None:
            xmlSubElem(xStyl, _wTag("outlineLvl"), attrib={_wTag("val"): str(style.level)})

        pPr = xmlSubElem(xStyl, _wTag("pPr"))
        xmlSubElem(pPr, _wTag("spacing"), attrib={
            _wTag("before"): str(int(20.0 * firstFloat(style.before))),
            _wTag("after"): str(int(20.0 * firstFloat(style.after))),
            _wTag("line"): str(int(20.0 * firstFloat(style.line, size))),
        })
        if style.align:
            xmlSubElem(pPr, _wTag("jc"), attrib={_wTag("val"): style.align})

        rPr = xmlSubElem(xStyl, _wTag("rPr"))
        xmlSubElem(rPr, _wTag("sz"), attrib={_wTag("val"): str(int(2.0 * size))})
        xmlSubElem(rPr, _wTag("szCs"), attrib={_wTag("val"): str(int(2.0 * size))})
        if style.color:
            xmlSubElem(rPr, _wTag("color"), attrib={_wTag("val"): style.color})

        self._styles[style.styleId] = style

        return


class DocXParagraph:

    def __init__(self) -> None:
        self._content: list[ET.Element] = []
        self._style: DocXParStyle | None = None
        self._textAlign: str | None = None
        self._topMargin: float | None = None
        self._bottomMargin: float | None = None
        self._breakBefore = False
        self._breakAfter = False
        return

    ##
    #  Setters
    ##

    def setStyle(self, style: DocXParStyle | None) -> None:
        """Set the paragraph style."""
        self._style = style
        return

    def setAlignment(self, value: str) -> None:
        """Set paragraph alignment."""
        if value in ("left", "center", "right"):
            self._textAlign = value
        return

    def setMarginTop(self, value: float) -> None:
        """Set margin above in pt."""
        self._topMargin = value
        return

    def setMarginBottom(self, value: float) -> None:
        """Set margin below in pt."""
        self._bottomMargin = value
        return

    def setPageBreakBefore(self, state: bool) -> None:
        """Set page break before flag."""
        self._breakBefore = state
        return

    def setPageBreakAfter(self, state: bool) -> None:
        """Set page break after flag."""
        self._breakAfter = state
        return

    ##
    #  Methods
    ##

    def addContent(self, run: ET.Element) -> None:
        """Add a run segment to the paragraph."""
        self._content.append(run)
        return

    def finalise(self, body: ET.Element) -> None:
        """Called after all content is set."""
        if style := self._style:
            par = xmlSubElem(body, _wTag("p"))

            # Values
            spacing = {}
            if self._topMargin is not None:
                spacing["before"] = str(self._topMargin)
            if self._bottomMargin is not None:
                spacing["after"] = str(self._bottomMargin)

            # Paragraph
            pPr = xmlSubElem(par, _wTag("pPr"))
            xmlSubElem(pPr, _wTag("pStyle"), attrib={_wTag("val"): style.styleId})
            if self._topMargin is not None or self._bottomMargin is not None:
                xmlSubElem(pPr, _wTag("spacing"), attrib={
                    _wTag("before"): str(int(20.0 * firstFloat(self._topMargin, style.before))),
                    _wTag("after"): str(int(20.0 * firstFloat(self._bottomMargin, style.after))),
                    _wTag("line"): str(int(20.0 * firstFloat(style.line, style.size))),
                })
            if self._textAlign:
                xmlSubElem(pPr, _wTag("jc"), attrib={_wTag("val"): self._textAlign})

            # Text
            if self._breakBefore:
                wr = xmlSubElem(par, _wTag("r"))
                xmlSubElem(wr, _wTag("br"), attrib={_wTag("type"): "page"})
            for run in self._content:
                par.append(run)
            if self._breakAfter:
                wr = xmlSubElem(par, _wTag("r"))
                xmlSubElem(wr, _wTag("br"), attrib={_wTag("type"): "page"})

        return

# -*- coding:utf8 -*-
"""
    this is tool script which help fix chinese messy code
    when using python reportLab library convert html to pdf.
    DO NOT CHANGE IT.

    usage:
        import it at beginning of other class file where use reportlab/xhtml2pdf
        i.e. {{from core.utils.encode import *}}
"""

import reportlab.rl_config
reportlab.rl_config.warnOnMissingFontGlyphs = 0

import reportlab.pdfbase.pdfmetrics
import reportlab.pdfbase.ttfonts
from django.conf import settings


reportlab.pdfbase.pdfmetrics.registerFont(
    reportlab.pdfbase.ttfonts.TTFont('simsun', '%s/fonts/simsun.ttf' % settings.PROJECT_STATIC_ROOT))

import reportlab.lib.fonts

reportlab.lib.fonts.ps2tt = lambda psfn: ('simsun', 0, 0)
reportlab.lib.fonts.tt2ps = lambda fn, b, i: 'simsun'
import reportlab.platypus


def wrap(self, availWidth, availHeight):
    # work out widths array for breaking
    self.width = availWidth
    leftIndent = self.style.leftIndent
    first_line_width = availWidth - (leftIndent + self.style.firstLineIndent) - self.style.rightIndent
    later_widths = availWidth - leftIndent - self.style.rightIndent
    try:
        self.blPara = self.breakLinesCJK([first_line_width, later_widths])
    except:
        self.blPara = self.breakLines([first_line_width, later_widths])
        self.height = len(self.blPara.lines) * self.style.leading
    return (self.width, self.height)


reportlab.platypus.Paragraph.wrap = wrap

# -*- coding: utf-8 -*-

import os

from ..utils import get_page_layout, get_text_objects, get_rect_objects


class BaseParser(object):
    """Defines a base parser.
    """

    def _generate_layout(self, filename, layout_kwargs):
        self.filename = filename
        self.layout_kwargs = layout_kwargs
        self.layout, self.dimensions = get_page_layout(filename, **layout_kwargs)
        self.images = get_text_objects(self.layout, ltype="image")
        self.horizontal_text = get_text_objects(self.layout, ltype="horizontal_text")
        self.vertical_text = get_text_objects(self.layout, ltype="vertical_text")
        self.rectangles = get_rect_objects(self.layout)
        self.pdf_width, self.pdf_height = self.dimensions
        self.rootname, __ = os.path.splitext(self.filename)

    @staticmethod
    def is_inside(cell, rect):
        # Fill rects can be sloppy.  The +/- 1 here allows some overlap between cell bounds and fill bounds.
        return cell.lb[0] >= rect.x0-1 and cell.lb[0] <= rect.x1+1 \
               and cell.lb[1] >= rect.y0-1 and cell.lb[1] <= rect.y1+1 \
               and cell.rt[0] >= rect.x0-1 and cell.rt[0] <= rect.x1+1 \
               and cell.rt[1] >= rect.y0-1 and cell.rt[1] <= rect.y1+1

    def find_rectangles(self, cell):
        overlaps = [r for r in reversed(self.rectangles) if r.fill and BaseParser.is_inside(cell, r)]
        if len(overlaps) > 0:
            return overlaps[0].non_stroking_color
        else:
            return None

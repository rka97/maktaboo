import fitz


class PDFDocument:
    def __init__(self, path: str):
        self._path = path
        self._doc = fitz.open(path)
        self._metadata = None

    def path(self):
        return self._path

    def metadata(self):
        if not self._metadata:
            self._metadata = self._extract_metadata()
        return self._metadata

    def title(self):
        return self.metadata()['title']

    def author(self):
        return self.metadata()['author']

    def page_count(self):
        return self._doc.page_count

    def _extract_metadata(self):
        metadata = self._doc.metadata
        if not metadata['title']:
            metadata['title'] = self._extract_title()

        if not metadata['author']:
            metadata['author'] = self._extract_author()

        return metadata

    def _extract_title(self):
        # extracts document title using the simple heuristic of finding the text block
        # with the biggest font in the first two pages

        num_pages = 2

        title = ["", 0, float('inf')]
        for i in range(min(num_pages, self._doc.page_count)):
            page = self._doc[i]
            for block in page.get_textpage().extractDICT()['blocks']:
                lines = block['lines']
                max_size = max([span['size']
                               for line in lines for span in line['spans']])
                bbox = block['bbox']
                y_min, y_max = bbox[1], bbox[3]
                y_coordinate = (y_min + y_max) / 2
                if max_size > title[1] or (max_size == title[1] and y_coordinate < title[2]):
                    title[0] = " ".join([span['text']
                                        for line in lines for span in line['spans']])
                    title[1] = max_size
                    title[2] = y_coordinate

        return title[0]

    def _extract_author(self):
        return ""

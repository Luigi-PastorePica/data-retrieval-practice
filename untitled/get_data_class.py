# this class does not do anything useful and most probably will go away

from pdfminer.pdfparser import PDFParser,
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfdocument import PDFNoOutlines
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice

from pdfminer.layout import LAParams, LTTextBox, LTTextLine, LTFigure, LTImage
from pdfminer.converter import PDFPageAggregator

class Gdata(object):
    def __init__(self, path):
        # set an if to detect whether file is pdf or word or smthg else.
        # Open a PDF file.
        fp = open(path, 'rb')
        # Create a PDF parser object associated with the file object.
        parser = PDFParser(fp)
        # Create a PDF document object that stores the document structure.
        # Supply the password for initialization.
        self.document = PDFDocument(parser)
        # Check if the document allows text extraction. If not, abort.
        if not self.document.is_extractable:
            raise PDFTextExtractionNotAllowed
        # Create a PDF resource manager object that stores shared resources.
        self.rsrcmgr = PDFResourceManager()
        # Create a PDF device object.
        device = PDFDevice(self.rsrcmgr)
        # Create a PDF interpreter object.
        interpreter = PDFPageInterpreter(self.rsrcmgr, device)
        # Process each page contained in the document.
        for page in PDFPage.create_pages(self.document):
            interpreter.process_page(page)

    def la(self):
        # Set parameters for analysis.
        laparams = LAParams()
        # Create a PDF page aggregator object.
        device = PDFPageAggregator(self.rsrcmgr, laparams=laparams)
        interpreter = PDFPageInterpreter(self.rsrcmgr, device)
        for page in PDFPage.create_pages(self.document):
            interpreter.process_page(page)
            # receive the LTPage object for the page.
            layout = device.get_result()

def get_email(path):
    with open(path, 'rb') as textf:
        textf.get_text()

pdf_obj = Gdata('/Users/Twilit_Zero/Desktop/trash/anastasia_lenskiy_resume_jan_2016.pdf')

print pdf_obj.la()

# get_email('/Users/Twilit_Zero/Desktop/trash/anastasia_lenskiy_resume_jan_2016.pdf')
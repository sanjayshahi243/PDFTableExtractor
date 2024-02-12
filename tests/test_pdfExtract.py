import os

import camelot
import pytest

from pdfExtractor.utils.pdfExtractor import extract_tables_from_pdf


def test_extract_tables_success():
    # Arrange
    pdf_path = os.path.abspath("tests/test_pdf/DummyTablePDF1.pdf")

    # Act
    tables = extract_tables_from_pdf(pdf_path)

    # Assert
    assert isinstance(tables, camelot.core.TableList)
    assert len(tables) > 0
    assert len(tables) == 3


def test_extract_tables_specific_page_success():
    # Arrange
    pdf_path = os.path.abspath("tests/test_pdf/DummyTablePDF1.pdf")
    page = "2"

    # Act
    tables = extract_tables_from_pdf(pdf_path, pages=page)

    # Assert
    assert isinstance(tables, camelot.core.TableList)
    assert len(tables) > 0


def test_extract_tables_no_tables():
    # Arrange
    pdf_path = os.path.abspath("tests/test_pdf/DummyTablePDF_NO_TABLE.pdf")

    # Act
    tables = extract_tables_from_pdf(pdf_path)

    # Assert
    assert isinstance(tables, camelot.core.TableList)
    assert len(tables) == 0


def test_incorrect_file_format():
    # Arrange
    pdf_path = os.path.abspath("tests/test_pdf/NonPDFFile.txt")

    # Act
    with pytest.raises(NotImplementedError) as excinfo:
        extract_tables_from_pdf(pdf_path)

    # Assert
    assert "File format not supported" in str(excinfo.value)

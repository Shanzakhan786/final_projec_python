from pypdf import PdfReader


def extract_text_from_pdf(file_path: str) -> str:
    """
    Extracts text from a PDF file.

    Args:
        file_path (str): The path to the PDF file.

    Returns:
        str: The extracted text as a single string, or an empty string if extraction fails.
    """
    try:
        reader = PdfReader(file_path)
        full_text = []

        for page in reader.pages:
            text = page.extract_text()
            if text:
                full_text.append(text)

        return "\n".join(full_text) if full_text else ""

    except FileNotFoundError:
        print(f"Error: file not found at {file_path}")
        return ""
    except Exception as e:
        print(f"An error occurred while extracting text from the PDF: {str(e)}")
        return ""


from fastapi import APIRouter, File, UploadFile, File , HTTPException, Query
import uuid as uuid_pkg #Use alias to avoid to conflict with path parameter name
import os

# import the shared data store
from src.utils.data_store import data_store   

# PDF file upload and processing
from src.utils.pdf_processing import extract_text_from_pdf

# LLM client utility
from src.utils.llm_client import get_llm_response

# Create a router instance
router = APIRouter()

# Define temporary directory for uploads
UPLOAD_DIR = "temp/cag_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload/{uuid}", status_code=201)
def upload_pdf(uuid: uuid_pkg.UUID, file: UploadFile = File(...)):
    """
    Upload a PDF file associated with a unique UUID.
    Extracts text from the PDF and stores it in the data store.
    If the UUID already exists, it raises a 400 error.(use PUT update).
    """
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400, detail="File must be a PDF."
        )
    uuid_str = str(uuid)
    if uuid_str in data_store:
        raise HTTPException(
            status_code=400,
             detail=f"UUID  {uuid_str}  already exists. Use PUT /api/v1/upload/{uuid_str} to append data.",
        )
    
    file_path = os.path.join(UPLOAD_DIR, f"{uuid_str}_{file.filename}")
    try:
        #Save the uploaded file to the temporary directory
        with open(file_path, "wb") as buffer:
            buffer.write(file.file.read())

        #Extract text using the ultility function
        extracted_text = extract_text_from_pdf(file_path)

        if extracted_text is None:
            raise HTTPException(
                status_code=500, detail="Failed to extract text from PDF."
            )
        
        #Store the extracted text in the data store
        data_store[uuid_str] = extracted_text
        return {
            "message":"file uploaded and text extracted successfully.",
            "uuid": uuid_str,

        }
    
    except Exception as e:
        #log the exception e
        raise HTTPException(
            status_code=500, detail=f"An error occurred while processing the file: {str(e)}"
        )
    finally:
        #Clean up the temporary file
        if os.path.exists(file_path):
            os.remove(file_path)

@router.put("/upload/{uuid}")
def update_pdf(uuid: uuid_pkg.UUID, file: UploadFile = File(...)):
    """
    Update an existing PDF file associated with a unique UUID.
    Appends the new text to the existing text in the data store.
    If the UUID does not exist, it raises a 404 error.
    """
    
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400, detail=" Invalid file type. Only PDF files are accepted."
        )
    
    uuid_str = str(uuid)
    if uuid_str not in data_store:
        raise HTTPException(
            status_code=404, detail=f"UUID {uuid_str} not found. Use POST /api/v1/upload/{uuid_str} to create it first.",
        )

    file_path = os.path.join(UPLOAD_DIR, f"{uuid_str}_update_{file.filename}")
    try:
        #Save the uploaded file to the temporary directory
        with open(file_path, "wb") as buffer:
            buffer.write(file.file.read())

        #Extract text using the ultility function
        new_text = extract_text_from_pdf(file_path)

        if new_text is None:
            raise HTTPException(
                status_code=500, detail="Failed to extract text from PDF."
            )
        
        #Append the new text to the existing text in the data store
        data_store[uuid_str] += "\n" + new_text
        return {
            "message": "file updated and text appended successfully.",
            "uuid": uuid_str,
        }
    
    except Exception as e:
        #log the exception e
        raise HTTPException(
            status_code=500, detail=f"An error occurred while processing the file: {str(e)}"
        )
    
    finally:
        #Clean up the temporary file
        if os.path.exists(file_path):
            os.remove(file_path)

@router.get("/query/{uuid}")
def query_pdf(uuid: uuid_pkg.UUID, query: str = Query(..., min_length=1)):
    """
    Retrieve the stored text for a given UUID and sends it along with the query to the LLM.
    to a placeholder LLM service.
    Return the placeholder response.
    """

    uuid_str = str(uuid)
    if uuid_str not in data_store:
        raise HTTPException(
            status_code=404, detail=f"UUID {uuid_str} not found."
        )

    store_text = data_store[uuid_str]

    llm_response = get_llm_response(query=query, context=store_text)

    return {"uuid": uuid_str, "query": query, "llm_response": llm_response}


@router.get("/status/{uuid}", status_code=200)
def get_status(uuid: uuid_pkg.UUID):
    """
    Check the status of the PDF processing for a given UUID.
    """
    uuid_str = str(uuid)
    if uuid_str not in data_store:
        raise HTTPException(
            status_code=404, detail=f"UUID {uuid_str} not found."
        )

    return {"uuid": uuid_str, "status": "processed"}

@router.delete("/delete/{uuid}", status_code=200)
def delete_pdf(uuid: uuid_pkg.UUID):
    """
    Delete the stored PDF and its associated text for a given UUID.
    """
    uuid_str = str(uuid)
    if uuid_str not in data_store:
        raise HTTPException(
            status_code=404, detail=f"UUID {uuid_str} not found."
        )

    del data_store[uuid_str]
    return {"message": f"Data for UUID {uuid_str} deleted successfully."}

@router.get("/list_uuids")
def list_all_uuids():
    """"
    Returns a list of all stored UUIDs.
    """
    return {"uuids": list(data_store.keys())}
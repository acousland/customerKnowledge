#pip install pii-preprocess pii-extract-plg-regex pii-extract-plg-transformers pii-transform
from pii_data.types.doc import DocumentChunk
from pii_extract.api import PiiProcessor, PiiCollectionBuilder

def PiiDetect(file):
    print("Detecting PII")
    with open(file, 'r') as file:
            transcript = file.read()   
    chunk = DocumentChunk(id=0, data=transcript)
    proc = PiiProcessor()
    proc.build_tasks(lang="en")
    piic = PiiCollectionBuilder(lang="en")
    proc.detect_chunk(chunk, piic)
    results = []  # Create an empty list
    for pii in piic:
        results.append(pii.asdict())  # Append each dictionary to the list
    return(results)

def PiiDetectAggregate(file):
    results = PiiDetect(file)

    # Extract distinct types using a set comprehension
    distinct_types = {result['type'] for result in results}

    # Convert the set to a list if you need a list specifically
    distinct_types_list = list(distinct_types)
            # Now you can write distinct_list to your NEO4J database
            # Make sure to handle the conversion for all numpy.float32 values before writing to the database

    return(distinct_types_list)

PiiBannedTypes = ['CREDIT_CARD', 'GOV_ID']
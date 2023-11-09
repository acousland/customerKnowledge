#pip install pii-preprocess pii-extract-plg-regex pii-extract-plg-transformers pii-transform
from pii_data.types.doc import DocumentChunk
from pii_extract.api import PiiProcessor, PiiCollectionBuilder

def PiiDetect(file):
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

    if not results:
        return ""
    else:
        max_scores = {}

        for item in results:
            item_type = item['type']
            # Convert numpy.float32 to Python float
            item_score = float(item['process']['score'])
            
            if item_type not in max_scores or item_score > max_scores[item_type]:
                max_scores[item_type] = item_score

        distinct_list = [{'type': type_, 'max_score': score} for type_, score in max_scores.items()]

        # Now you can write distinct_list to your NEO4J database
        # Make sure to handle the conversion for all numpy.float32 values before writing to the database

        return(distinct_list)
import openai
import os
import json

def callFeatures(transcript, model):    
    print("Extracting call features")
    response = openai.ChatCompletion.create(
        model=model,
        response_format={ "type": "json_object" },
        messages=[
            {"role": "system", "content": """You are a business analyst who is reviewing call centre data. 
                                            You are very professional and will only respond in JSON format. 
                                            Your job is to identify the following features and return them in the right JSON field name
                                            Feature 1: Identify the product being discussed. JSON field name: Product
                                            Feature 2: Identify the issue being discussed. JSON field name: Issue
                                            Feature 3: Identify if the issue that the customer called up about has been resolved. A simple resolved/unresolved will suffice. JSON field name: Resolution
                                            Feature 4: Identify the name of the operator. If you don't know, just say Unknown. JSON field name: Operator_name
                                            Feature 5: Identify the name of the customer. If you don't know, just say Unknown. JSON field name: Customer_name
                                            Feature 6: Make a judgement on the sentiment of the operator. JSON field name: Operator_sentiment
                                            Feature 7: Make a judgement on the sentiment of the customer. JSON field name: Customer_sentiment
                                            """},
            {"role": "user", "content": transcript}
        ]
    )
    content = response['choices'][0]['message']['content']
    content_dict = json.loads(content)
    return(content_dict)


def callFeaturesPersist(transcript, destination_path, model):    
    if not os.path.isfile(destination_path):
            call_features = callFeatures(transcript, model)
            with open(destination_path, 'w') as feature_file:
                feature_file.write(f"{call_features}\n\n")

def callFeaturesRead(feature_file_path):
    if os.path.isfile(feature_file_path):
        with open(feature_file_path, 'r') as file:
            features = file.read()
        features = features.replace("'", "\"")
        features_dict = json.loads(features)
        return(features_dict)
    else:
        return("Features not found")
import os
import extractAudio as ea
import transcribe as ts
import callFeatures as cf
import openai
import PiiDetect as pii
from py2neo import Graph, Node, Relationship
from dotenv import dotenv_values
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
secrets = dotenv_values(".env")

openai.api_key = secrets["OPENAI_API_KEY"]
GPTModel = config.get('OpenAI', 'gpt_model')
whisperModel = config.get('OpenAI', 'whisper_model')
graph = Graph(secrets["NEO4J_SERVER"], 
              auth=(secrets["NEO4J_USERNAME"], 
                    secrets["NEO4J_PASSWORD"]))

# Establish working directories
video_directory = config.get('Storage_Paths', 'video_directory')
audio_directory = config.get('Storage_Paths', 'audio_directory')
os.makedirs(audio_directory, exist_ok=True)
transcription_directory = config.get('Storage_Paths', 'transcription_directory')
os.makedirs(transcription_directory, exist_ok=True)  
feature_output_directory = config.get('Storage_Paths', 'feature_output_directory')
os.makedirs(feature_output_directory, exist_ok=True)  

graph.delete_all()

# Iterate over video files
for video_file in os.listdir(video_directory):
    if video_file.endswith('.mp4'):  # Assuming the video files are in mp4 format
        video_path = os.path.join(video_directory, video_file)
        base_filename = os.path.splitext(video_file)[0]
        print("Processing " + str(base_filename))
        # Prepare paths for the outputs
        audio_path = os.path.join(audio_directory, base_filename + '.wav')
        transcription_path = os.path.join(transcription_directory, base_filename + '.txt')
        feature_file_path = os.path.join(feature_output_directory, base_filename + '_features.txt')
        
        # Extract audio from video
        ea.extractAudio(video_path, audio_path)
        
        # Transcribe
        ts.transcribePersist(audio_path, transcription_path, whisperModel)
        transcript = ts.transcribeRead(transcription_path)
        
        # Detect Pii
        PiiResults = pii.PiiDetectAggregate(transcription_path)

        # Using a for loop and an if statement to check for a match
        for value in PiiResults:
            if value in pii.PiiBannedTypes:
                print("Writing to graph database")
                callNode = Node("Customer Call", call_name = base_filename)
                PiiNodes = []
                for index in PiiResults:
                    node = Node("PII", Pii_Type = index, Call = base_filename) 
                    PiiNodes.append(node)
                for index in PiiNodes:
                    graph.create(index)
                    graph.create(Relationship(callNode, "HAS_PII", index))
                break  # Breaks the loop after the first match is found
        else:  
            # Extract call features
            cf.callFeaturesPersist(transcript, feature_file_path, GPTModel)
            call_features = cf.callFeaturesRead(feature_file_path)

            print("Writing to graph database")
            if len(PiiResults) > 0:
                PiiNodes = []
                for index in PiiResults:
                    node = Node("PII", Pii_Type = index, Call = base_filename) 
                    PiiNodes.append(node)

            callNode = Node("Customer Call", call_name = base_filename)
            productNode = Node("Product", product=call_features["Product"])
            productIssueNode = Node("Issue", issue=call_features["Issue"])
            customerSentimentNode = Node("Customer_Sentiment" , sentiment=call_features["Customer_sentiment"])
            operatorSentimentNode = Node("Operator_Sentiment" , sentiment=call_features["Operator_sentiment"])
            callOutcomeNode = Node("Call_Outcome" , resolved=call_features["Resolution"])
            operatorNode = Node("Operator", name=call_features["Operator_name"])
            customerNode = Node("Customer", name=call_features["Customer_name"])

            if len(PiiNodes) > 0:
                for index in PiiNodes:
                    graph.create(index)
                        
            graph.create(operatorNode)
            graph.create(customerNode)
            graph.create(callNode)
            graph.create(productNode)
            graph.create(productIssueNode)
            graph.create(customerSentimentNode)
            graph.create(operatorSentimentNode)
            graph.create(callOutcomeNode)

            graph.create(Relationship(callNode, "OPERATOR", operatorNode))
            graph.create(Relationship(callNode, "CUSTOMER", customerNode))
            graph.create(Relationship(callNode, "HAS_PRODUCT", productNode))
            graph.create(Relationship(callNode, "HAS_ISSUE", productIssueNode))
            graph.create(Relationship(customerNode, "HAS_SENTIMENT", customerSentimentNode))
            graph.create(Relationship(operatorNode, "HAS_SENTIMENT", operatorSentimentNode))
            graph.create(Relationship(callNode, "HAD_OUTCOME", callOutcomeNode))

            if len(PiiNodes) > 0:
                for index in PiiNodes:
                    graph.create(Relationship(callNode, "HAS_PII", index))
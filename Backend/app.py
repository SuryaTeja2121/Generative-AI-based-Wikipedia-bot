from transformers import BlenderbotForConditionalGeneration, BlenderbotTokenizer

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

import pickle
import pysolr
import re
import requests

import nltk
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.sentiment import SentimentIntensityAnalyzer

import google.generativeai as genai

from flask import Flask, request, jsonify

from flask_cors import CORS

def chat_with_blenderbot(user_query):
    mname = 'facebook/blenderbot-400M-distill'
    model = BlenderbotForConditionalGeneration.from_pretrained(mname)
    tokenizer = BlenderbotTokenizer.from_pretrained(mname)

    inputs = tokenizer([user_query], return_tensors = 'pt')

    reply_ids = model.generate(**inputs)

    decoded_response = tokenizer.decode(reply_ids[0], skip_special_tokens = True)
    return decoded_response

def topic_classifier(user_query):
    
    topic_model_clf = pickle.load(open("topic_clf_model.sav", 'rb'))

    with open('topic_clf_vocab.pkl', 'rb') as f:
        topic_model_vocab = pickle.load(f)

    topics = ["Health", "Environment", "Technology", "Economy", "Entertainment", "Sports", "Politics", "Education", "Travel", "Food"]

    label_encoder = LabelEncoder()
    labels = label_encoder.fit_transform(topics)

    topic_clf_vectorizer = CountVectorizer(vocabulary = topic_model_vocab)

    query_vector = topic_clf_vectorizer.transform([user_query])

    predicted_label = topic_model_clf.predict(query_vector)

    predicted_topic = label_encoder.inverse_transform(predicted_label)
    
    return predicted_topic[0]

def decider(user_query):
    clf = pickle.load(open("chitchat_clf.sav", 'rb'))

    with open('chitchat_vocab.pkl', 'rb') as f:
        loaded_vocabulary = pickle.load(f)

    sentence = [user_query]

    chichat_vectorizer = CountVectorizer(vocabulary = loaded_vocabulary)
    sentence_vec = chichat_vectorizer.transform(sentence)
    prediction = clf.predict(sentence_vec)
    
    return prediction[0]

def search_documents(user_query, topic, k):

    CORE_NAME = "test"
    VM_IP = "localhost"
    
    solr = pysolr.Solr(f"http://{VM_IP}:8983/solr/{CORE_NAME}", always_commit = True, timeout = 1000)

    tokens = word_tokenize(user_query)

    tagged = pos_tag(tokens)

    key_terms = [word for word, pos in tagged if pos in ['NN', 'NNS', 'NNP', 'NNPS', 'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']]
    
    print(key_terms)
    print(topic)

    query = f"summary:({' OR '.join(key_terms)}) AND topic:{topic}"

    results = solr.search(query, rows = k)
    
    summaries = []

    for result in results:
        summaries.append(result['summary'][0])
    
    final_summary = ''.join(summaries)
    
    if(len(final_summary) < 20):
        
        return "Sorry, I am not sure of this topic"
    
    genai.configure(api_key="AIzaSyAWxvHDvfd0cLsmOWeYQJfVT1Z9R01Vd_A")
    
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content("Summaize this text given here in about 50-60 words. Just give me the summary and nothing else. Here is the text - : " + final_summary)
    
    final_result = response.text
    
    return final_result, topic

app = Flask(__name__)
CORS(app)

topics = {}
sentiment_count = {"Positive" : 0, "Negative" : 0, "Neutral" : 0}

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_query = request.json['user_input']
        user_topic = request.json["topic"]
        
        decider_output = decider(user_query)
        
        sia = SentimentIntensityAnalyzer()
        sentiment_scores = sia.polarity_scores(user_query)

        compound_score = sentiment_scores['compound']

        sentimnet = ''

        if compound_score >= 0.05:
            sentimnet = 'Positive'
        elif compound_score <= -0.05:
            sentimnet = 'Negative'
        else:
            sentimnet = 'Neutral'

        sentiment_count[sentimnet] += 1
        
        if decider_output == 1:
            
            blenderbot_response = chat_with_blenderbot(user_query)
            
            return jsonify({'final_output': blenderbot_response})
        else:
            tc_output = topic_classifier(user_query)

            if(tc_output != user_topic):
                return jsonify({'final_output': "Sorry, I am not sure of this question. Please check if you have selected appropriate topic related to your query."})
        
            final_output, topic = search_documents(user_query, tc_output, 5)

            if topic in topics:
                topics[topic] += 1
            else:
                topics[topic] = 1

            return jsonify({'final_output': final_output})
        
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/get_topics', methods = ['GET'])
def get_topics():
    return jsonify(topics)

@app.route('/sentiment_history', methods=["GET"])
def get_sentiment_history():
    return jsonify(sentiment_count)

if __name__ == '__main__':
    app.run()
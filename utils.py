from typing import List, Dict, Any, Tuple, Optional
from time import sleep
import os
import json
import requests
import streamlit as st


API_ENDPOINT = os.getenv("API_ENDPOINT", "https://d432-34-87-63-89.ngrok.io")
print("-----> API_ENDPOINT:", API_ENDPOINT)
STATUS = "initialized"
HS_VERSION = "hs_version"
DOC_REQUEST = "query"
DOC_FEEDBACK = "feedback"
DOC_UPLOAD = "file-upload"


def haystack_is_ready():
    url = f"{API_ENDPOINT}/{STATUS}"
    print(f"Haystack is ready STARTING at: {url}")
    try:
        if requests.get(url).status_code < 400:
            print("---> READY!!!!")
            return True
    except Exception as e:
        print(e)
        sleep(1)  # To avoid spamming a non-existing endpoint at startup
    return False


@st.cache
def haystack_version():
    url = f"{API_ENDPOINT}/{HS_VERSION}"
    return requests.get(url, timeout=0.1).json()["hs_version"]


def send_query(query, filters={}, top_k_reader=5, top_k_retriever=5) -> Tuple[List[Dict[str, Any]], Dict[str, str]]:
    """
    Send a query to the REST API and parse the answer.
    Returns both a ready-to-use representation of the results and the raw JSON.
    """

    url = f"{API_ENDPOINT}/{DOC_REQUEST}"
    params = {"filters": filters, "Retriever": {"top_k": top_k_retriever}, "Reader": {"top_k": top_k_reader}}
    req = {"query": query, "params": params}
    print("SENDING A QUERY TO THE API")
    print(f"url: {url}, request: {req}")
    # url: https://203d-34-73-20-231.ngrok.io/query
    # params: {'filters': {}, 'Retriever': {'top_k': 3}, 'Reader': {'top_k': 3}}
    # req: {'query': "What is space debris?", 
    # 'params': {'filters': {}, 'Retriever': {'top_k': 3}, 'Reader': {'top_k': 3}}}
    response_raw = requests.post(url, json=req)
    print(f"RESPONSE RAW: {response_raw.status_code}")
    # response_raw: <Response [200]>

    if response_raw.status_code >= 400 and response_raw.status_code != 503:
        print("-> Exception in response_raw.status_code", vars(response_raw))
        raise Exception(f"{vars(response_raw)}")

    response = response_raw.json()
    if "errors" in response:
        print("-> Errors in response:", ", ".join(response["errors"]))
        raise Exception(", ".join(response["errors"]))
    """
    200 
    { 'query': 'what is space debris?', 
      'answers': [
          {'answer': 'a problem', 'type': 'extractive', 'score': 0.3546408787369728, 'context': 'This article considers why space debris is a problem, how space  debris is distributed, what risks space debris poses to satellites, what  internation', 'offsets_in_document': [{'start': 43, 'end': 52}], 'offsets_in_context': [{'start': 43, 'end': 52}], 'document_id': 'af74b43e88ba15d077e3a03249fedf94', 'meta': {'article_title': 'sd_paper_59_m.txt'}}, 
          {'answer': 'Space Traffic Management', 'type': 'extractive', 'score': 0.009678191505372524, 'context': 'What is Space Traffic Management ', 'offsets_in_document': [{'start': 8, 'end': 32}], 'offsets_in_context': [{'start': 8, 'end': 32}], 'document_id': 'a2249fb45863b927bb51bc7185aae83c', 'meta': {'article_title': 'IAASS_paper_135_m.txt'}}, 
          {'answer': 'SPACE OBJECT', 'type': 'extractive', 'score': 0.006475328002125025, 'context': 'B. WHAT IS A SPACE OBJECT   ', 'offsets_in_document': [{'start': 13, 'end': 25}], 'offsets_in_context': [{'start': 13, 'end': 25}], 'document_id': 'c483a71487227da30562ff88bf0dbda3', 'meta': {'article_title': 'IAASS_paper_141_m.txt'}}, 
          {'answer': 'System Safety', 'type': 'extractive', 'score': 0.003304556477814913, 'context': '1.1  What is System Safety ', 'offsets_in_document': [{'start': 13, 'end': 26}], 'offsets_in_context': [{'start': 13, 'end': 26}], 'document_id': 'ffc20f651fc394543936ab6f2ca4f1b', 'meta': {'article_title': 'IAASS_paper_146_m.txt'}}, 
          {'answer': 'System Safety', 'type': 'extractive', 'score': 0.002059442806057632, 'context': '1.1   What Is System Safety . 6', 'offsets_in_document': [{'start': 14, 'end': 27}], 'offsets_in_context': [{'start': 14, 'end': 27}], 'document_id': 'ffc20f651fc394543936ab6f2ca4f1b', 'meta': {'article_title': 'IAASS_paper_146_m.txt'}}, 
          {'answer': 'SPACE OBJECT', 'type': 'extractive', 'score': 0.0012499610311351717, 'context': 'APPLIES  A. WHAT IS AN AIRCRAFT  B. WHAT IS A SPACE OBJECT  C. WHAT IS AN AEROSPACE VEHICLE  D. PROBLEMS WITH THE FUNCTIONALIST APPROACH ', 'offsets_in_document': [{'start': 46, 'end': 58}], 'offsets_in_context': [{'start': 46, 'end': 58}], 'document_id': 'c483a71487227da30562ff88bf0dbda3', 'meta': {'article_title': 'IAASS_paper_141_m.txt'}}, 
          {'answer': 'SYSTEM SAFETY', 'type': 'extractive', 'score': 0.0011647613137029111, 'context': 'WHAT IS   SYSTEM SAFETY', 'offsets_in_document': [{'start': 10, 'end': 23}], 'offsets_in_context': [{'start': 10, 'end': 23}], 'document_id': 'ffc20f651fc394543936ab6f2ca4f1b', 'meta': {'article_title': 'IAASS_paper_146_m.txt'}}, 
          {'answer': 'Risk', 'type': 'extractive', 'score': 0.00041400118061574176, 'context': 'What is the Risk ', 'offsets_in_document': [{'start': 12, 'end': 16}], 'offsets_in_context': [{'start': 12, 'end': 16}], 'document_id': 'd8bf7d33de8c65d6cbabb0237560d7b', 'meta': {'article_title': 'stm_paper_88_m.txt'}}, 
          {'answer': 'satellite', 'type': 'extractive', 'score': 0.00041361330659128726, 'context': 'space.  We must know what the satellite is capable of doing, what it is being used for and what it ', 'offsets_in_document': [{'start': 30, 'end': 39}], 'offsets_in_context': [{'start': 30, 'end': 39}], 'document_id': '1f4e7882d3a6df62696d57bf66c6c8ca', 'meta': {'article_title': 'SSA_papers_paper_222_m.txt'}}, 
          {'answer': 'Risk', 'type': 'extractive', 'score': 0.00029716818971792236, 'context': 'What is the Risk', 'offsets_in_document': [{'start': 12, 'end': 16}], 'offsets_in_context': [{'start': 12, 'end': 16}], 'document_id': 'd8bf7d33de8c65d6cbabb0237560d7b', 'meta': {'article_title': 'stm_paper_88_m.txt'}}], 
      'documents': [
          {'content': 'B. WHAT IS A SPACE OBJECT   ', 'content_type': 'text', 'id': 'c483a71487227da30562ff88bf0dbda3', 'meta': {'article_title': 'IAASS_paper_141_m.txt'}}, 
          {'content': 'What is Space Traffic Management ', 'content_type': 'text', 'id': 'a2249fb45863b927bb51bc7185aae83c', 'meta': {'article_title': 'IAASS_paper_135_m.txt'}}, 
          {'content': 'What is the Risk', 'content_type': 'text', 'id': 'd8bf7d33de8c65d6cbabb0237560d7b', 'meta': {'article_title': 'stm_paper_88_m.txt'}}, 
          {'content': 'What is the Risk ', 'content_type': 'text', 'id': 'd8bf7d33de8c65d6cbabb0237560d7b', 'meta': {'article_title': 'stm_paper_88_m.txt'}}, 
          {'content': 'This article considers why space debris is a problem, how space  debris is distributed, what risks space debris poses to satellites, what  international communities have done to ameliorate the problem, and  what we should do in the future.', 'content_type': 'text', 'id': 'af74b43e88ba15d077e3a03249fedf94', 'meta': {'article_title': 'sd_paper_59_m.txt'}}, 
          {'content': 'space.  We must know what the satellite is capable of doing, what it is being used for and what it ', 'content_type': 'text', 'id': '1f4e7882d3a6df62696d57bf66c6c8ca', 'meta': {'article_title': 'SSA_papers_paper_222_m.txt'}}, 
          {'content': 'APPLIES  A. WHAT IS AN AIRCRAFT  B. WHAT IS A SPACE OBJECT  C. WHAT IS AN AEROSPACE VEHICLE  D. PROBLEMS WITH THE FUNCTIONALIST APPROACH ', 'content_type': 'text', 'id': 'c483a71487227da30562ff88bf0dbda3', 'meta': {'article_title': 'IAASS_paper_141_m.txt'}}, 
          {'content': '1.1   What Is System Safety . 6', 'content_type': 'text', 'id': 'ffc20f651fc394543936ab6f2ca4f1b', 'meta': {'article_title': 'IAASS_paper_146_m.txt'}}, 
          {'content': 'WHAT IS   SYSTEM SAFETY', 'content_type': 'text', 'id': 'ffc20f651fc394543936ab6f2ca4f1b', 'meta': {'article_title': 'IAASS_paper_146_m.txt'}}, 
          {'content': '1.1  What is System Safety ', 'content_type': 'text', 'id': 'ffc20f651fc394543936ab6f2ca4f1b', 'meta': {'article_title': 'IAASS_paper_146_m.txt'}}
      ]
    }
    [69] 0s
    """
    # Format response
    results = []
    answers = response["answers"]
    for answer in answers:
        if answer.get("answer", None):
            results.append(
                {
                    "context": "..." + answer["context"] + "...",
                    "answer": answer.get("answer", None),
                    "relevance": round(answer["score"] * 100, 2),
                    "document": [doc for doc in response["documents"] if doc["id"] == answer["document_id"]][0],
                    "offset_start_in_doc": answer["offsets_in_document"][0]["start"],
                    "_raw": answer,
                }
            )
        else:
            results.append(
                {
                    "context": None,
                    "answer": None,
                    "document": None,
                    "relevance": round(answer["score"] * 100, 2),
                    "_raw": answer,
                }
            )
    return results, response


def send_feedback(query, answer_obj, is_correct_answer, is_correct_document, document) -> None:
    """
    Send a feedback (label) to the REST API
    """
    url = f"{API_ENDPOINT}/{DOC_FEEDBACK}"
    req = {
        "query": query,
        "document": document,
        "is_correct_answer": is_correct_answer,
        "is_correct_document": is_correct_document,
        "origin": "user-feedback",
        "answer": answer_obj,
    }
    response_raw = requests.post(url, json=req)
    if response_raw.status_code >= 400:
        raise ValueError(f"An error was returned [code {response_raw.status_code}]: {response_raw.json()}")


def get_backlink(result) -> Tuple[Optional[str], Optional[str]]:
    if result.get("document", None):
        doc = result["document"]
        if isinstance(doc, dict):
            if doc.get("meta", None):
                if isinstance(doc["meta"], dict):
                    if doc["meta"].get("url", None) and doc["meta"].get("title", None):
                        return doc["meta"]["url"], doc["meta"]["title"]
    return None, None

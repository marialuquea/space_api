print("Starting Extractive QA from document store")

from haystack.document_stores import PineconeDocumentStore
from haystack.nodes import FARMReader, TransformersReader, TfidfRetriever
from haystack.pipelines import ExtractiveQAPipeline
from haystack.retriever.dense import EmbeddingRetriever


def get_document_store():
    document_store = PineconeDocumentStore(
        api_key='2622f896-0c2f-45a4-bfff-b4a8577e54d2',
        index='testin4',
        similarity="cosine",
        embedding_dim=768
    )
    print("Document store metric type:",document_store.metric_type)
    print("Document count:",document_store.get_document_count())
    print("Document embedding count:",document_store.get_embedding_count())
    return document_store


def get_retriever(document_store):
    # option 1
    retriever1 = EmbeddingRetriever(
        document_store  = document_store,
        embedding_model = "flax-sentence-embeddings/all_datasets_v3_mpnet-base",
        model_format    = "sentence_transformers",
        use_gpu         = True
    )
    print("retriever 1:", retriever1)

    # option 2
    retriever2 = TfidfRetriever(
        document_store=document_store
    )
    print("retriever 2:", retriever2)

    return retriever1, retriever2


def get_reader():
    reader = FARMReader(
        model_name_or_path="deepset/roberta-base-squad2", 
        use_gpu=True,
        progress_bar = False
    )
    print("reader:", reader)
    # reader = TransformersReader(model_name_or_path="distilbert-base-uncased-distilled-squad", tokenizer="distilbert-base-uncased", use_gpu=-1)
    return reader


def create_pipeline(reader, retriever):
    print("---> Creating extractive QA Pipeline from reader and retriever")
    pipe = ExtractiveQAPipeline(reader, retriever)
    # print("pipeline:", pipe)
    return pipe


def ask_question(pipe, question):
    prediction = pipe.run(
        query=question, params={"Retriever": {"top_k": 10}, "Reader": {"top_k": 5}}
    )
    print(f"---> Question: {question}")
    print(f"---> Answers: ")
    return prediction


# if __name__ == "__main__":
    
    # # initialise document store
    # document_store = get_document_store()
    
    # # get retrievers
    # retriever1, retriever2 = get_retriever(document_store)

    # # get reader
    # reader = get_reader()

    # # combine them into a pipeline
    # pipeline = create_pipeline(reader, retriever2)

    # while True:
    #     question = input("Ask a question or write 'q' to exit: ")
    #     if question == "q":
    #         break
    #     ask_question(pipeline, question)

    # torch.cuda.empty_cache()
    # testing()

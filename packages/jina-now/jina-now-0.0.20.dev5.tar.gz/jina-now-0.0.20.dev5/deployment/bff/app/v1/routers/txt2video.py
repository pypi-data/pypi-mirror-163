import base64
from typing import List

from docarray import Document, DocumentArray
from fastapi import APIRouter

from deployment.bff.app.v1.models.text import NowTextSearchRequestModel
from deployment.bff.app.v1.models.video import (
    NowVideoIndexRequestModel,
    NowVideoResponseModel,
)
from deployment.bff.app.v1.routers.helper import (
    get_jina_client,
    index_all_docs,
    process_query,
    search_doc,
)

router = APIRouter()


# Index
@router.post(
    "/index",
    summary='Add more video data to the indexer',
)
def index(data: NowVideoIndexRequestModel):
    """
    Append the list of video data to the indexer. Each video data should be
    `base64` encoded using human-readable characters - `utf-8`.
    """
    index_docs = DocumentArray()
    jwt = data.jwt
    for video, tags in zip(data.videos, data.tags):
        base64_bytes = video.encode('utf-8')
        message = base64.decodebytes(base64_bytes)
        index_docs.append(Document(blob=message, tags=tags))

    index_all_docs(get_jina_client(data.host, data.port), index_docs, jwt)


# Search
@router.post(
    "/search",
    response_model=List[NowVideoResponseModel],
    summary='Search video data via text as query',
)
def search(data: NowTextSearchRequestModel):
    """
    Retrieve matching videos for a given text as query.
    """
    query_doc = process_query(text=data.text)
    jwt = data.jwt

    # for video the search requests have to be on chunk-level
    docs = search_doc(
        get_jina_client(data.host, data.port),
        Document(chunks=query_doc),
        data.limit,
        jwt,
    )

    return docs[0].matches.to_dict()

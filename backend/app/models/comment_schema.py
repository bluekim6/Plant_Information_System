"""
Comment 도메인 스키마.

PRD 9.3:
  - Tag 별 Comment 입력/조회/상태(Open/Review/Closed) 관리.
"""
from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, Field

CommentStatus = Literal["Open", "Review", "Closed"]


class Comment(BaseModel):
    """저장/응답에 사용되는 Comment 본체."""

    id: str
    tagNo: str
    content: str
    author: str
    status: CommentStatus = "Open"
    linkedDocumentNo: Optional[str] = None
    createdAt: datetime
    updatedAt: datetime


class CommentCreate(BaseModel):
    """Comment 생성 요청 body."""

    content: str = Field(min_length=1)
    author: str = Field(min_length=1)
    linkedDocumentNo: Optional[str] = None


class CommentUpdate(BaseModel):
    """Comment 본문/연결 문서 수정 요청 body."""

    content: Optional[str] = None
    linkedDocumentNo: Optional[str] = None
    author: str = Field(min_length=1)


class CommentStatusChange(BaseModel):
    """Comment 상태 전이 요청 body."""

    status: CommentStatus
    author: str = Field(min_length=1)

"""FAQ model module."""

import numpy as np
from app.models.base import BaseModel
from sqlalchemy import Column, Float, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import ARRAY


class FAQ(BaseModel):
    """FAQ model."""
    
    __tablename__ = "faq"
    
    tenant_id = Column(
        String, ForeignKey("tenant.id", ondelete="CASCADE"), nullable=False
    )
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    _embedding = Column(ARRAY(Float), nullable=True)

    def __init__(self, **kwargs):
        """Initialize FAQ."""
        super().__init__(**kwargs)
        self._embedding_array = None

    @property
    def embedding(self):
        """Get embedding."""
        return self._embedding_array

    @embedding.setter
    def embedding(self, value):
        """Set embedding."""
        self._embedding_array = value

    def cosine_similarity(self, other_embedding):
        """Calculate cosine similarity between embeddings."""
        if self.embedding is None or other_embedding is None:
            return 0.0

        a = np.array(self.embedding)
        b = np.array(other_embedding)

        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

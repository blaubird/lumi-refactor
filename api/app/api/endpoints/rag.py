# api/routers/rag.py с структурированным логированием
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session

# Исправленные импорты с использованием абсолютных путей
from app.api.deps import get_db
from app.models.tenant import Tenant
from app.services.ai import get_rag_response, load_embedding_model
from app.schemas.rag import RAGQueryRequest, RAGResponse
from app.core.logging import get_logger

# Инициализируем структурированный логгер
logger = get_logger(__name__)

router = APIRouter(
    prefix="/rag",
    tags=["RAG"],
)

@router.post("/query/", response_model=RAGResponse)
async def query_rag_system(
    query: RAGQueryRequest,
    db: Session = Depends(get_db)
):
    """
    Обрабатывает RAG-запрос и возвращает ответ, сгенерированный на основе релевантных FAQ.
    """
    try:
        # Логируем получение запроса
        logger.info(
            "RAG query received",
            extra={
                "query_length": len(query.query),
                "tenant_id": query.tenant_id
            }
        )
        
        # Получаем данные тенанта
        tenant = db.query(Tenant).filter(Tenant.id == query.tenant_id).first()
        if not tenant:
            logger.warning(
                "Tenant not found for RAG query",
                extra={"tenant_id": query.tenant_id}
            )
            raise HTTPException(status_code=404, detail="Tenant not found")
        
        # Получаем ответ от RAG-системы
        response = await get_rag_response(
            query=query.query,
            tenant_id=query.tenant_id,
            db=db,
            system_prompt=tenant.system_prompt
        )
        
        # Логируем успешный ответ
        logger.info(
            "RAG response generated",
            extra={
                "tenant_id": query.tenant_id,
                "response_length": len(response.answer),
                "sources_count": len(response.sources)
            }
        )
        
        return response
    except Exception as e:
        # Логируем ошибку
        logger.error(
            f"Error processing RAG query: {str(e)}",
            extra={
                "tenant_id": query.tenant_id,
                "error": str(e)
            },
            exc_info=True
        )
        raise HTTPException(
            status_code=500,
            detail=f"Error processing query: {str(e)}"
        )

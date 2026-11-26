"""backend/tests/conftest.py — Test fixtures for StudioForge V2."""

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database.connection import Database
from app.database.brand_repository import BrandRepository
from app.database.creative_repository import CreativeRepository
from app.database.approval_repository import ApprovalRepository
from app.rag.brand_retriever import BrandRetriever


@pytest.fixture(scope="session")
def test_db():
    db = Database("sqlite:///:memory:")
    return db


@pytest.fixture(scope="session")
def client(test_db):
    app.state.db = test_db
    app.state.brand_repo = BrandRepository(test_db)
    app.state.creative_repo = CreativeRepository(test_db)
    app.state.approval_repo = ApprovalRepository(test_db)
    app.state.retriever = BrandRetriever(app.state.brand_repo)

    with TestClient(app) as test_client:
        yield test_client

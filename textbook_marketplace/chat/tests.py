import pytest
import json
from channels.testing import WebsocketCommunicator
from django.contrib.auth import get_user_model, authenticate
from .consumers import ChatConsumer
from rest_framework_simplejwt.tokens import RefreshToken
import pytest_asyncio

@pytest.mark.django_db
@pytest.fixture
def user(db):
    get_user_model().objects.create_user(
        username="testuser", password="testpassword")
    user = authenticate(username="testuser", password="testpassword")
    return user


@pytest.fixture
def access_token(user):
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)


@pytest_asyncio.fixture
async def communicator(access_token):
    communicator = WebsocketCommunicator(
        ChatConsumer.as_asgi(), f"/ws/chat/testroom/?token={access_token}"
    )
    connected, subprotocol = await communicator.connect()
    assert connected
    yield communicator
    await communicator.disconnect()


@pytest.mark.asyncio
async def test_connection_success(communicator):
    pass


@pytest.mark.asyncio
async def test_send_message(communicator):
    await communicator.send_to(text_data=json.dumps({"message": "test_msg"}))
    response = await communicator.receive_from()
    assert json.loads(response).get("message") == "test_msg"
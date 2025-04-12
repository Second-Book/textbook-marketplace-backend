import pytest
import pytest_asyncio
from asgiref.sync import async_to_sync, sync_to_async

from channels.routing import URLRouter
from channels.testing import WebsocketCommunicator
from channels.layers import get_channel_layer

from django.contrib.auth import get_user_model
from django_channels_jwt_auth_middleware.auth import JWTAuthMiddlewareStack
from django.test import TransactionTestCase
from rest_framework_simplejwt.tokens import AccessToken

from .routing import websocket_urlpatterns
from .models import Chat, Message

User = get_user_model()


class TestChannelRedis:
    channel_layer = get_channel_layer()

    def test_call_group_send_once(self):
        async_to_sync(self.channel_layer.group_send)('channel_1',
                                                     {'message': 'message'})

    def test_call_group_send_twice(self):
        async_to_sync(self.channel_layer.group_send)('channel_1',
                                                     {'message': 'message'})
        async_to_sync(self.channel_layer.group_send)('channel_2',
                                                     {'message': 'message'})


# class TestJWTAuthMiddleware(TransactionTestCase):
#     reset_sequences = True
#
#     def setUp(self):
#         self.user = User.objects.create(username='testusername',
#                                         password='testpassword')
#         self.token = AccessToken.for_user(self.user)
#         self.application = JWTAuthMiddlewareStack(
#             URLRouter(
#                 websocket_urlpatterns
#                 )
#             )
#         self.valid_chat_url = 'chat/7429384723874237/'
#         self.invalid_chat_url = '89vhvuthei8vh'
#
#     def tearDown(self):
#         User.objects.all().delete()
#
#     async def test_websocket_without_token(self) -> None:
#         communicator = WebsocketCommunicator(
#             self.application, self.valid_chat_url
#         )
#         connected, subprotocol = await communicator.connect()
#         assert connected
#
#         await communicator.send_json_to(
#             data={'message': 'test'}
#         )
#         response = await communicator.receive_json_from()
#
#         self.assertIsNone(response['sender_id'])
#         self.assertEqual(response['message'], 'test')
#
#         await communicator.disconnect()
#
#     async def test_websocket_with_token(self) -> None:
#         communicator = WebsocketCommunicator(
#             self.application, f'{self.valid_chat_url}?token={self.token}'
#         )
#         connected, subprotocol = await communicator.connect()
#         assert connected
#
#         await communicator.send_json_to(
#             data={'message': 'test'}
#         )
#         response = await communicator.receive_json_from()
#
#         self.assertIsNotNone(response['sender_id'])
#         self.assertEqual(response['message'], 'test')
#
#         await communicator.disconnect()
#
#     async def test_websocket_with_invalid_url(self):
#         with self.assertRaises(ValueError):
#             communicator = WebsocketCommunicator(
#                     self.application, self.invalid_chat_url
#             )
#             await communicator.connect()


# pytest version of tests
# currently now the speed is x1.5 times faster than above's


@pytest.fixture
def first_user(db) -> User:
    return User.objects.create(
        username='testusername1', password='testpassword1'
    )


@pytest.fixture
def second_user(db) -> User:
    return User.objects.create(
        username='testusername2', password='testpassword2'
    )


@pytest.fixture
def chat(db, first_user, second_user) -> Chat:
    chat_name = f'{first_user.pk}{second_user.pk}'
    chat = Chat.objects.create(name=chat_name)
    chat.members.set([first_user, second_user])
    return chat


@pytest.fixture(scope='module')
def application() -> JWTAuthMiddlewareStack:
    return JWTAuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    )


@pytest.fixture(scope='module')
def valid_chat_url() -> str:
    return 'chat/testroomname/'


@pytest.fixture(scope='module')
def invalid_chat_url() -> str:
    return 'hberye4hte4hb'


@pytest.mark.asyncio
async def test_websocket_without_token(application: JWTAuthMiddlewareStack,
                                       valid_chat_url: str) -> None:
    communicator = WebsocketCommunicator(
        application, valid_chat_url
    )
    connected, subprotocol = await communicator.connect()
    assert connected

    await communicator.send_json_to(
            data={'message': 'test'}
        )
    response = await communicator.receive_json_from()

    assert response['sender_id'] is None
    assert response['message'] == 'test'

    await communicator.disconnect()


@pytest.mark.django_db(reset_sequences=True)
@pytest.mark.asyncio
async def test_websocket_with_token(application: JWTAuthMiddlewareStack,
                                    valid_chat_url: str,
                                    first_user: User) -> None:
    token = AccessToken.for_user(first_user)
    communicator = WebsocketCommunicator(
        application, f'{valid_chat_url}?token={token}'
    )
    connected, subprotocol = await communicator.connect()
    assert connected

    await communicator.send_json_to(
            data={'message': 'test'}
        )
    response = await communicator.receive_json_from()
    assert response['sender_id'] is not None
    assert response['message'] == 'test'

    await communicator.disconnect()


@pytest.mark.django_db(reset_sequences=True)
@pytest.mark.asyncio
async def test_websocket_with_invalid_url(application: JWTAuthMiddlewareStack,
                                          invalid_chat_url: str):
    with pytest.raises(ValueError):
        communicator = WebsocketCommunicator(
                application, invalid_chat_url
        )
        await communicator.connect()


@pytest.mark.django_db(reset_sequences=True)
def test_chat_created(chat, first_user, second_user):
    assert chat.pk == 1
    chat_members = chat.members.all()
    assert first_user in chat_members and second_user in chat_members


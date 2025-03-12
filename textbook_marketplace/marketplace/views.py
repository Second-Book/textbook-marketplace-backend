from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, BasePermission, SAFE_METHODS
from rest_framework import status, viewsets, permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import action, api_view

from .models import Textbook, User, Order
from .serializers import TextbookSerializer, SignupSerializer, CustomTokenObtainPairSerializer, UserSerializer, OrderSerializer


class IsAuthenticatedOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated
    

class TextbookListView(APIView):
    def get(self, request):
        username = request.query_params.get('username', None)
        if username:
            textbooks = Textbook.objects.filter(seller__username=username)
        else:
            textbooks = Textbook.objects.all()
            
        serializer = TextbookSerializer(textbooks, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = TextbookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(seller=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TextbookDetailView(APIView):
    def get_object(self, pk):
        try:
            return Textbook.objects.get(pk=pk)
        except Textbook.DoesNotExist:
            return None

    def get(self, request, pk):
        textbook = self.get_object(pk)
        if textbook is not None:
            serializer = TextbookSerializer(textbook)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)
        
class TextbookImageView(APIView): 
    def get(self, request, pk): 
        textbook = Textbook.objects.get(pk=pk) 
        image = textbook.image 
        return Response({'image': image.url})
    

class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "You have access to this protected view!"})
    

class SignupView(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class PersonalCabinetView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        pass

    def post(self, request):
        
        pass


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def get_queryset(self):
        return User.objects.all()

class TextbookViewSet(viewsets.ModelViewSet):
    queryset = Textbook.objects.all()
    serializer_class = TextbookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=False, methods=['post'])
    def create_textbook(self, request):
        print(request.data, request.user)
        serializer = TextbookSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(seller=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

@api_view(['GET'])
def get_user_data(request):
    if request.method == 'GET':
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)

class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
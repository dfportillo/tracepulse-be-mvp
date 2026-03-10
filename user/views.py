from rest_framework import status, viewsets, generics
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import login, logout
from django.shortcuts import get_object_or_404
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import User
from .serializer import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserProfileSerializer,
    UserUpdateSerializer,
    UserListSerializer,
    ChangePasswordSerializer
)
from .permission import IsAdminUser, IsOwnerOrAdmin, IsAdminOrReadOnly

class AuthViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]
    
    @method_decorator(csrf_exempt, name='post') # 🚨 AGREGAR ESTO TEMPORALMENTE
    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'message': 'Usuario registrado exitosamente',
                'user': UserProfileSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def login(self, request):
        serializer = UserLoginSerializer(
            data=request.data,
            context={'request': request}
        )
        
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)
            
            # 🚨 INICIO DEL DEBUG DE COOKIES EN EL RUNTIME DE DJANGO
            
            # Obtenemos el token CSRF que *debería* estar activo para esta sesión.
            # Django lo establecerá en la respuesta.
            csrf_token_value = get_token(request) 
            
            # El session_key solo existe si la sesión fue guardada, pero en el login 
            # se prepara para ser guardada y el ID se establece en la respuesta.
            session_key_value = request.session.session_key 

            print("\n--- 🍪 DJANGO RUNTIME - COOKIES DESPUÉS DEL LOGIN ---")
            print(f"1. CSRFTOKEN (Valor esperado por Django): {csrf_token_value}")
            print(f"2. SESSIONID (Clave de sesión a enviar): {session_key_value}")
            print("--------------------------------------------------\n")
            
            # 🚨 FIN DEL DEBUG

            return Response({
                'message': 'Login exitoso',
                'user': UserProfileSerializer(user).data
            })
        
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def logout(self, request):
        logout(request)
        return Response({'message': 'Logout exitoso'})

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    permission_classes = [IsAdminOrReadOnly]
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return UserProfileSerializer
        elif self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        elif self.action == 'create':
            return UserRegistrationSerializer
        return UserListSerializer
    
    def get_permissions(self):
        if self.action in ['profile', 'change_password','update_profile']:
            return [IsAuthenticated()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsOwnerOrAdmin()]
        return super().get_permissions()
    
    @action(detail=False, methods=['get'])
    def profile(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['put'])
    def update_profile(self, request):
        serializer = UserUpdateSerializer(
            request.user,
            data=request.data,
            partial=True
        )
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Perfil actualizado exitosamente',
                'user': UserProfileSerializer(request.user).data
            })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def change_password(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        
        if serializer.is_valid():
            old_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password']
            
            if not request.user.check_password(old_password):
                return Response(
                    {'old_password': 'Contraseña actual incorrecta'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            request.user.set_password(new_password)
            request.user.save()
            
            return Response({'message': 'Contraseña cambiada exitosamente'})
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        user = self.get_object()
        user.is_active = True
        user.save()
        return Response({'message': 'Usuario activado'})
    
    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        user = self.get_object()
        user.is_active = False
        user.save()
        return Response({'message': 'Usuario desactivado'})

@api_view(['POST'])
@permission_classes([AllowAny])
def user_registration(request):
    view_set = AuthViewSet()
    view_set.request = request
    return view_set.register(request)

@api_view(['POST'])
@permission_classes([AllowAny])
def user_login(request):
    view_set = AuthViewSet()
    view_set.request = request
    return view_set.login(request)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_logout(request):
    view_set = AuthViewSet()
    view_set.request = request
    return view_set.logout(request)
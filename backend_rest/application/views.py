from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Application
from .serializers import ApplicationSerializer


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def application_list(request):
    print("USER:", request.user)  # add this line temporarily
    print("AUTH:", request.auth)
    if request.method == 'GET':
        apps = Application.objects.filter(U_ID=request.user).order_by('-changed_at')
        serializer = ApplicationSerializer(apps, many=True)
        return Response({'success': True, 'applications': serializer.data})

    if request.method == 'POST':
        data = request.data.copy()
        serializer = ApplicationSerializer(data=data)
        if serializer.is_valid():
            serializer.save(U_ID=request.user)
            return Response({'success': True, 'application': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def application_detail(request, app_id):

    try:
        app = Application.objects.get(APP_ID=app_id, U_ID=request.user)
    except Application.DoesNotExist:
        return Response({'success': False, 'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = ApplicationSerializer(app, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': True, 'application': serializer.data})
        return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        app.delete()
        return Response({'success': True, 'message': 'Deleted'})
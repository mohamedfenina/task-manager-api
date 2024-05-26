from django.http import JsonResponse
from .backends import AccountBackend
from django.shortcuts import render

# Create your views here.
# views.py
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Accounts, Task
from .serializers import TaskSerializer, AccountsAdminSerializer, AccountSerializer, TaskGSerializer


@api_view(['POST'])
def register_account(request):
    if request.method == 'POST':
        serializer = AccountsAdminSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = {
                'code': 201,
                'status': 'success',
                'message': 'Account created successfully.'
            }
            return JsonResponse(data, status=status.HTTP_201_CREATED)

        else:
            errors = serializer.errors
            if '__all__' in errors:
                # All fields are required error
                return Response({'error': 'All fields are required'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def create_account(request):
    if request.method == 'POST':
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = {
                'code': 201,
                'status': 'success',
                'message': 'Account created successfully.'
            }
            return JsonResponse(data, status=status.HTTP_201_CREATED)

        else:
            errors = serializer.errors
            if '__all__' in errors:
                # All fields are required error
                return Response({'error': 'All fields are required'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    role = request.POST.get('role')

    account_backend = AccountBackend()
    print('auth')
    user = account_backend.authenticate(request, email=email, password=password, role=role)
    if user is not None:
        # Login successful
        data = {
            'code': 200,
            'status': 'success',
            'message': 'Login successfully',
            'userId': user.id
        }
        return JsonResponse(data, status=status.HTTP_200_OK)
    else:
        # Login failed
        return JsonResponse({'status_code': 401, 'message': 'Invalid credentials'},
                            status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_tasks_by_admin(request):
    admin_id = request.GET.get('adminId')
    status = request.GET.get('status')
    tasks = Task.objects.filter(adminId=admin_id, status=status).order_by('date')

    serializer = TaskGSerializer(tasks, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_tasks_by_user(request):
    userId = request.GET.get('userId')
    status = request.GET.get('status')
    tasks = Task.objects.filter(userId=userId, status=status).order_by('date')
    serializer = TaskGSerializer(tasks, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def create_task(request):
    serializer = TaskSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Task created successfully'}, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def done_tasks(request):
    task_id = request.data.get('id')

    if task_id is None:
        return Response({'error': 'id  parameters is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        task = Task.objects.get(id=task_id)
        task.status = True
        task.save()
        return Response({'message': 'Task status updated successfully'}, status=status.HTTP_200_OK)
    except Accounts.DoesNotExist:
        return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_accounts_by_admin(request):
    admin_id = request.GET.get('adminId')

    if not admin_id:
        return JsonResponse({'error': 'adminId parameter is required'}, status=403)

    try:
        accounts = Accounts.objects.filter(adminId=admin_id)
        accounts_data = list(accounts.values('id', 'name', 'email', 'phone', 'password', 'adminId', 'status'))
        response_data = {'data': accounts_data}
        return JsonResponse(response_data, safe=False)
    except Accounts.DoesNotExist:
        return JsonResponse({'error': 'No accounts found for the given adminId'}, status=404)


@api_view(['POST'])
def update_account_status(request):
    account_id = request.data.get('id')
    new_status = request.data.get('status')

    if account_id is None or new_status is None:
        return Response({'error': 'id and status parameters are required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        account = Accounts.objects.get(id=account_id)
        account.status = new_status
        account.save()
        return Response({'message': 'Account status updated successfully'}, status=status.HTTP_200_OK)
    except Accounts.DoesNotExist:
        return Response({'error': 'Account not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def update_account_details(request):
    account_id = request.data.get('id')

    if not account_id:
        return Response({'error': 'id parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        account = Accounts.objects.get(id=account_id)
    except Accounts.DoesNotExist:
        return Response({'error': 'Account not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = AccountSerializer(account, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Account details updated successfully'}, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

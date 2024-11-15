from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from .models import Question, UserResponse, UserScore
from .serializers import QuestionSerializer
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.models import User
import json
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

def sign_up(request):
    return render(request, 'signup.html')

def save_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.info(request, "UserName already exists")
                return redirect(sign_up)
            elif User.objects.filter(email=email).exists():
                messages.info(request, "Email already exists")
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                return redirect(login_page)
        else:
            messages.info(request, "Passwords does not match")
            return redirect(signup)

def login_page(request):
    users = User.objects.all()
    return render(request, 'login.html', {'users':users})
    
def logged(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.filter(username=username)
        if User.objects.filter(username=username).exists():
            user = authenticate(request,username=username, password=password)
            print(user)
            if user is not None:
                login(request, user)
                request.session['username'] = username
                return redirect(home) 
            else:
                messages.error(request, "Incorrect Username or Password")
                return render(request, 'signup.html')
        else:
            return render(request, 'signup.html')

def logout(request):
    request.session.pop('username', None)  
    request.session.pop('password', None)  
    messages.info(request, "You have logged out successfully")
    return render(request, 'signup.html')

@login_required
def home(request):
    return render(request, 'home.html')

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_questions(request):
    questions = Question.objects.all()
    question_serializer = QuestionSerializer(questions, many=True)
    return Response(question_serializer.data, status=status.HTTP_200_OK)

@csrf_exempt
@login_required
def save_response(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            responses = data.get('responses', [])
            # Check if responses is a non-empty list
            if not isinstance(responses, list) or len(responses) == 0:
                return JsonResponse({'success': False, 'error': 'Invalid or empty responses list'})
            for response_data in responses:
                question_id = response_data.get('question_id')
                answer = response_data.get('answer')
                if not all([question_id, answer, request.user.id]):
                    return JsonResponse({'success': False, 'error': 'Incomplete response data'})
                # Get the user and question objects
                user = request.user
                question = Question.objects.get(id=question_id)                
                UserResponse.objects.create(
                    user=user,
                    question=question,
                    selected_answer=answer,
                    timestamp=timezone.now()
                )              
            return JsonResponse({'success': True, 'message': 'All responses saved successfully'})
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'User not found'})
        except Question.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Question not found'})
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON format'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': f'Unexpected error: {str(e)}'})

@login_required
def calculate_user_score(request):
    user = request.user
    # Retrieve all responses for the user
    responses = UserResponse.objects.filter(user=user)
    if not responses:
        return JsonResponse({'success': False, 'error': 'No responses found for this user.'})
    total_score = 0
    # Calculate total score based on responses
    for response in responses:
        question = response.question
        score = question.get_score(response.selected_answer)
        total_score += score
     # Save or update the score in UserScore
    user_score, created = UserScore.objects.get_or_create(user=user)
    user_score.score = total_score
    user_score.save()
    return render(request, 'result.html', {'score': total_score})

  
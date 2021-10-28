from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status, viewsets

from .models import Poll,Choice
from .serializers import PollSerializer, ChoiceSerializer, VoteSerializer, UserSerializer
from django.contrib.auth import authenticate
from rest_framework.exceptions import PermissionDenied

class PollViewSet(viewsets.ModelViewSet):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer

    def destroy(self, request, *args, **kwargs):
        poll = Poll.objects.get(pk=self.kwargs['pk'])
        if not request.user == poll.created_by:
            raise PermissionDenied("You cont delite this poll")
        return super().destroy(request, *args, **kwargs)



class ChoiceList(generics.ListCreateAPIView):
    def get_queryset(self):
        print(self.kwargs)
        # queryset= Choice.objects.filter(poll_id=self.kwargs['pk'])
        queryset = Choice.objects.all()
        print("queryset" * 5, queryset)
        return queryset
    model = Choice
    serializer_class = ChoiceSerializer


class CreateVote(APIView):
    serializer_class = VoteSerializer

    def post(self, request, pk, choice_pk):
        voted_by = request.data.get('vote_by')
        data = {'choice': choice_pk, 'poll': pk, 'voted_by': voted_by}
        serializer = VoteSerializer(data=data)
        if serializer.is_valid():
            vote = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserCreate(generics.ListCreateAPIView):
    serializer_class = UserSerializer


class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            return Response({'token': user.auth_token.key})
        else:
            return Response({'error': 'Wrong Credentionals'}, status=status.HTTP_400_BAD_REQUEST)
# class PollList(APIView):
#     def get(self, request):
#         MAX_OBJECTS = 20
#         polls = Poll.objects.all()[:MAX_OBJECTS]
#         data = PollSerializer(polls, many=True).data
#         return Response(data)
#
# class PollDetail(APIView):
#     def get(self, request, pk):
#         poll = get_object_or_404(Poll, pk)
#         data = PollSerializer(poll).data
#         return Response(data)


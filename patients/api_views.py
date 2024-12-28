from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from rest_framework import viewsets, permissions, generics
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user': UserSerializer(user).data})


class LogoutView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        request.auth.delete()
        return Response({'detail': 'Successfully logged out.'}, status=status.HTTP_200_OK)



class ProfileView(APIView):
    def get(self, request):
        """
        Retrieve the profile of the currently authenticated user.
        """
        profile = get_object_or_404(Profile, user=request.user.Patient)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)


class UpdateProfileView(APIView):
    def put(self, request):
        """
        Update the profile of the currently authenticated user.
        """
        profile = get_object_or_404(Profile, user=request.user.Patient)
        serializer = ProfileSerializer(profile, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)


class MedicationReminderViewSet(viewsets.ModelViewSet):
    queryset = MedicationReminder.objects.all()
    serializer_class = MedicationReminderSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(patient=self.request.user.Patient)


class TreatmentPlanViewSet(viewsets.ModelViewSet):
    queryset = TreatmentPlan.objects.all()
    serializer_class = TreatmentPlanSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(patient=self.request.user.Patient)

# class BillViewSet(viewsets.ModelViewSet):
#     queryset = Bill.objects.all()
#     serializer_class = BillSerializer
#     permission_classes = [IsAuthenticated]
#
#     def perform_create(self, serializer):
#         serializer.save(patient=self.request.user)

class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(patient=self.request.user.Patient)


class EmergencyServiceViewSet(viewsets.ModelViewSet):
    queryset = EmergencyService.objects.all()
    serializer_class = EmergencyServiceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(patient=self.request.user.Patient)
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Application
from .FSM_transitions import validate_transition, InvalidStateTransitionError

# Create your views here.
class UpdateApplicationStatusView(APIView):

   def patch(self, request, pk):
      # Fixed: Added Application model and fixed assignment syntax
      application = get_object_or_404(Application, pk=pk)
      target_status = request.data.get("status")

      try:
         validate_transition(application.status, target_status)

         application.status = target_status
         application.save()
         # Fixed: Corrected dictionary key and space in the string
         return Response({"message": f"Status updated to {target_status} successfully"}, status=status.HTTP_200_OK)

      except InvalidStateTransitionError as e:
         # Optional: Pass the error message 'e' to the frontend so users know *why* it failed
         return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
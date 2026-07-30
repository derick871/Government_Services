from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Application, CountyNotice
from .serializers import ApplicationSerializer, CountyNoticeSerializer
from .FSM_transitions import validate_transition, InvalidStateTransitionError


# =====================================================================
# County Notices Views
# =====================================================================

class CountyNoticeListView(APIView):
    """
    API View to list all active county notices, tenders, or bursary alerts.
    """
    def get(self, request):
        notices = CountyNotice.objects.all().order_by('-created_at')
        serializer = CountyNoticeSerializer(notices, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CountyNoticeByCountyView(APIView):
    """
    API View to filter public notices by a specific county identifier.
    """
    def get(self, request, county_id):
        notices = CountyNotice.objects.filter(county_id=county_id).order_by('-created_at')
        serializer = CountyNoticeSerializer(notices, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# =====================================================================
# Applications Views
# =====================================================================

class ApplicationListCreateView(APIView):
    """
    API View to list applications for the authenticated user or submit a new one.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Enforces profile/role constraints: Officers see their county's applications, citizens see their own
        if hasattr(request.user, 'is_officer') and request.user.is_officer:
            applications = Application.objects.filter(county_id=request.user.county_id)
        else:
            applications = Application.objects.filter(user=request.user)
            
        serializer = ApplicationSerializer(applications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ApplicationSerializer(data=request.data)
        if serializer.is_valid():
            # Inject authenticated user domain metadata into application record
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApplicationDetailView(APIView):
    """
    Public or authenticated tracking endpoint to retrieve an application by its unique tracking number.
    """
    def get(self, request, tracking_number):
        application = get_object_or_404(Application, tracking_number=tracking_number)
        serializer = ApplicationSerializer(application)
        return Response(serializer.data, status=status.HTTP_200_OK)


# =====================================================================
# State Machine Lifecycle View
# =====================================================================

class UpdateApplicationStatusView(APIView):
    """
    Patches application workflow lifecycle states using custom FSM transition validation rules.
    """
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        application = get_object_or_404(Application, pk=pk)
        target_status = request.data.get("status")
        
        # Pull role from active JWT user instance to check against transition rights
        user_role = getattr(request.user, 'role', 'CITIZEN')

        if not target_status:
            return Response({"error": "Target status field is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Pass user_role context to match your FSM_transitions configuration signature
            validate_transition(
                current_state=application.status, 
                target_state=target_status, 
                user_role=user_role
            )

            application.status = target_status
            application.save()
            
            # Optional: Log the workflow transition step in a tracking audit history table here
            
            return Response(
                {"message": f"Status updated to {target_status} successfully"}, 
                status=status.HTTP_200_OK
            )

        except InvalidStateTransitionError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
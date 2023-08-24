import re
from lodging.api.pagination import Pagination, StayPagination, PartnerStayPagination
from .serializers import *
from lodging.models import *
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from anymail.message import EmailMessage
from .permissions import IsUserStayInstance, ObjectPermission, IsUserRoomStayInstance
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from .filterset import StayFilter, ReviewFilter, BookingsFilter
from django.db.models import Q, Subquery
from lodging.models import Review
from rest_framework.validators import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, serializers, status
from django.db.models import F, Value, CharField
from django.conf import settings
from django.contrib.sessions.backends.db import SessionStore
from django.db.models import Prefetch
from user.models import CustomUser

from rest_framework_bulk import (
    ListBulkCreateUpdateDestroyAPIView,
)


class StaysCreateView(generics.CreateAPIView):
    serializer_class = StaysSerializer
    queryset = Stays.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class StaysDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = StaysSerializer
    permission_classes = [ObjectPermission]
    lookup_field = "slug"

    def get_queryset(self):
        queryset = Stays.objects.filter(
            is_active=True,
        )
        slug = self.kwargs.get("slug")

        if slug is not None:
            queryset = Stays.objects.filter(
                slug=slug,
                is_active=True,
            )
        return queryset


class StaysListView(generics.ListAPIView):
    serializer_class = StaysSerializer
    filterset_class = StayFilter
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = [
        "date_posted",
        "rooms",
        "beds",
        "bathrooms",
    ]
    pagination_class = StayPagination

    def get_queryset(self):
        queryset = Stays.objects.filter(
            is_active=True,
        )

        querystring = self.request.GET.get("search")
        querystring_detail_search = self.request.GET.get("d_search")
        if querystring:
            querystring = querystring.split(",")[0]
            words = re.split(r"[^A-Za-z']+", querystring)
            query = Q()  # empty Q object
            for word in words:
                # 'or' the queries together
                query |= Q(location__icontains=word) | Q(city__icontains=word)
            queryset = Stays.objects.filter(
                query,
                is_active=True,
            ).all()

        if querystring_detail_search:
            querystring_detail_search = querystring_detail_search.split(",")[0]
            words = re.split(r"[^A-Za-z']+", querystring_detail_search)
            query = Q()  # empty Q object
            for word in words:
                # 'or' the queries together
                query |= (
                    Q(location__icontains=word)
                    | Q(city__icontains=word)
                    | Q(country__icontains=word)
                )
            queryset = Stays.objects.filter(
                query,
                is_active=True,
            ).all()

        return queryset


class HighlightedStaysListView(generics.ListAPIView):
    serializer_class = StaysSerializer

    def get_queryset(self):
        return Stays.objects.filter(in_homepage=True, has_options=True)


class HighlightedStaysDetailView(generics.RetrieveAPIView):
    serializer_class = StaysSerializer
    lookup_field = "slug"

    def get_queryset(self):
        slug = self.kwargs.get("slug")
        return Stays.objects.filter(in_homepage=True, has_options=True, slug=slug)


class UserStays(generics.ListAPIView):
    serializer_class = StaysSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Stays.objects.filter(user=self.request.user)


class UserStaysEmail(generics.ListAPIView):
    serializer_class = LodgeStaySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        email = self.request.user.email
        return (
            Stays.objects.filter(contact_email=email)
            .select_related("user")
            .prefetch_related(
                "stay_images",
            )
        )


class TestPartnerStaysListView(generics.ListAPIView):
    serializer_class = StaysSerializer
    queryset = Stays.objects.filter(is_partner_property=True)


class PartnerStaysDetailView(generics.ListAPIView):
    serializer_class = PartnerStaySerializer

    def get_queryset(self):
        list_ids = self.kwargs.get("list_ids")
        list_ids = list_ids.split(",")
        user = generics.get_object_or_404(CustomUser, id=self.request.user.id)
        queryset = (
            Stays.objects.filter(is_partner_property=True, id__in=list_ids, agents__user=user)
            .select_related("user")
            .prefetch_related(
                "activity_fees",
                "other_fees_resident",
                "other_fees_non_resident",
                "stay_images",
            ).all().distinct()
        )

        # order queryset based on the list_ids
        queryset = sorted(queryset, key=lambda x: list_ids.index(str(x.id)))

        return queryset
    

class PartnerStaysWithoutContractView(generics.ListAPIView):
    serializer_class = LodgeStayWaitingForApprovalSerializer
    ordering_fields = [
        "date_posted"
    ]
    pagination_class = PartnerStayPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        search_query = self.request.GET.get("search", "")
        user = generics.get_object_or_404(CustomUser, id=self.request.user.id)

        approved_agents = Agents.objects.filter(
            approved=True, user=user
        )

        approved_agents_by_email = AgentsByEmail.objects.filter(
            email=user.email
        )

        queryset = (
            Stays.objects.filter(
                Q(location__icontains=search_query)
                | Q(property_name__icontains=search_query),
                is_partner_property=True,
            )
            .exclude(
                Q(agents__in=approved_agents) | Q(agents_by_email__in=approved_agents_by_email),
            )
            .select_related("user")
            .prefetch_related(
                "stay_images",
            )
            .all()
        )

        return queryset


class PartnerStaysListView(generics.ListAPIView):
    serializer_class = LodgeStaySerializer
    ordering_fields = [
        "date_posted"
    ]
    pagination_class = PartnerStayPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        search_query = self.request.GET.get("search", "")
        user = generics.get_object_or_404(CustomUser, id=self.request.user.id)

        queryset = (
            Stays.objects.filter(
                Q(location__icontains=search_query)
                | Q(property_name__icontains=search_query),
                Q(agents__user=user,
                agents__approved=True) | Q(agents_by_email__email=user.email),
                is_partner_property=True,
            )
            .select_related("user")
            .prefetch_related(
                "stay_images",
            )
            .all().distinct()
        )

        return queryset


class UserStaysEmailDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LodgeStaySerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "slug"

    def get_queryset(self):
        queryset = Stays.objects.filter(
            user=self.request.user,
        )
        slug = self.kwargs.get("slug")
        email = self.request.user.email

        if slug is not None:
            queryset = Stays.objects.filter(slug=slug, contact_email=email).select_related("user").prefetch_related(
                "stay_images",
            )
        return queryset
    

class UserStayEmailAgentListView(generics.ListAPIView):
    serializer_class = AgentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        slug = self.kwargs.get("slug")
        email = self.request.user.email
        queryset = generics.get_object_or_404(Stays, slug=slug, contact_email=email)
        return queryset.agents.filter(approved=True)
    

class UserStayEmailAgentNotVerifiedListView(generics.ListAPIView):
    serializer_class = AgentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        slug = self.kwargs.get("slug")
        email = self.request.user.email
        queryset = generics.get_object_or_404(Stays, slug=slug, contact_email=email)
        return queryset.agents.filter(approved=False)
    

class AgentAccessDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AgentSerializer
    permission_classes = [IsAuthenticated]
    queryset = Agents.objects.all()


class HiglighedDetailStayListView(generics.ListAPIView):
    serializer_class = DetailStaySerializer

    def get_queryset(self):
        return Stays.objects.filter(in_homepage=True, has_options=True).select_related("user").prefetch_related(
                "stay_images",
            )
    
class HiglighedDetailStayRetrieveView(generics.RetrieveAPIView):
    serializer_class = DetailStayWithAmenitiesSerializer
    lookup_field = "slug"

    def get_queryset(self):
        slug = self.kwargs.get("slug")
        return Stays.objects.filter(in_homepage=True, has_options=True, slug=slug).select_related("user").prefetch_related(
                "stay_images",
                "extras_included",
                "other_options",
                "private_safari",
                "shared_safari",
                "all_inclusive",
                "facts",
                "inclusions",
            )
    
    
class UserStayEmailUpdateAgentsView(generics.UpdateAPIView):
    serializer_class = LodgeStaySerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "slug"

    def get_queryset(self):
        queryset = Stays.objects.filter(
            user=self.request.user,
        )
        slug = self.kwargs.get("slug")
        email = self.request.user.email

        if slug is not None:
            queryset = Stays.objects.filter(slug=slug, contact_email=email).select_related("user").prefetch_related(
                "stay_images",
            )
        return queryset
    
    def perform_update(self, serializer):
        instance = serializer.save()
        agent_id = self.request.data.get("agent_id")
        agent_id = int(agent_id)
        stay_slug = self.kwargs.get("slug")
        stay = generics.get_object_or_404(Stays, slug=stay_slug)
        user = generics.get_object_or_404(CustomUser, id=agent_id)
        agent = Agents.objects.create(user=user, stay=stay, approved=True)
        if user.is_agent == False:
            raise PermissionDenied("This user is not an agent")
        
        # check if agent is already added
        if instance.agents.filter(user=user).exists():
            agent_obj = instance.agents.get(user=user)
            instance.agents.remove(agent_obj)
            agent_obj.delete()

        
        instance.agents.add(agent)
        instance.save()
        return instance
    

class UserStayEmailUpdateAgentsWithFileView(generics.UpdateAPIView):
    serializer_class = LodgeStaySerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "slug"

    def get_queryset(self):
        slug = self.kwargs.get("slug")
        queryset = Stays.objects.filter(slug=slug).select_related("user").prefetch_related(
                "stay_images",
            )

        return queryset
    
    def perform_update(self, serializer):
        instance = serializer.save()
        user = self.request.user
        stay_slug = self.kwargs.get("slug")
        stay = generics.get_object_or_404(Stays, slug=stay_slug)
        document = self.request.data.get("document")
        agent = Agents.objects.create(user=user, stay=stay, document=document, approved=False)
        if user.is_agent == False:
            raise PermissionDenied("This user is not an agent")
        
        # check if agent is already added
        if instance.agents.filter(user=user).exists():
            agent_obj = instance.agents.get(user=user)
            instance.agents.remove(agent_obj)
            agent_obj.delete()
        
        instance.agents.add(agent)
        instance.save()
        return instance
    

class AgentAccessByEmailDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AgentByEmailSerializer
    permission_classes = [IsAuthenticated]
    queryset = AgentsByEmail.objects.all()


class UserAgentAccessByEmailListView(generics.ListAPIView):
    serializer_class = AgentByEmailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_qs = []
        stay_slug = self.kwargs.get("slug")
        stay = generics.get_object_or_404(Stays, slug=stay_slug)

        for obj in AgentsByEmail.objects.filter(stay=stay):
            if CustomUser.objects.filter(email=obj.email).exists():
                user_qs.append(
                    {
                        "id": obj.id,
                        "user": CustomUser.objects.get(email=obj.email),
                    }
                )

        return user_qs
    

class UserAgentAccessByEmailNotVerifiedListView(generics.ListAPIView):
    serializer_class = AgentByEmailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_qs = []
        stay_slug = self.kwargs.get("slug")
        stay = generics.get_object_or_404(Stays, slug=stay_slug)

        for obj in AgentsByEmail.objects.filter(stay=stay):
            if not CustomUser.objects.filter(email=obj.email).exists():
                user_qs.append(obj)

        return user_qs


class CheckAgentByEmailExistsView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        if AgentsByEmail.objects.filter(email=email).exists():
            return Response({"exists": True}, status=status.HTTP_200_OK)
        else:
            return Response({"exists": False}, status=status.HTTP_404_NOT_FOUND)
    
    

class AddAgentToStayView(generics.UpdateAPIView):
    serializer_class = LodgeStaySerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "slug"

    def get_queryset(self):
        slug = self.kwargs.get("slug")
        queryset = Stays.objects.filter(slug=slug).select_related("user").prefetch_related(
                "stay_images",
            )

        return queryset
    
    def perform_update(self, serializer):
        instance = serializer.save()
        stay_slug = self.kwargs.get("slug")
        stay = generics.get_object_or_404(Stays, slug=stay_slug)
        email = self.request.data.get("email")
        
        if CustomUser.objects.filter(email=email).exists() and stay.agents.filter(user__email=email).exists() != True:
            user = generics.get_object_or_404(CustomUser, email=email)
            if user.is_agent == False:
                return
            agent = Agents.objects.create(user=user, stay=stay, approved=True)
            instance.agents.add(agent)
            instance.save()
            return instance
        elif CustomUser.objects.filter(email=email).exists() and stay.agents.filter(user__email=email).exists() == True:
            return
        else:
            if instance.agents_by_email.filter(email=email).exists():
                return
            
            agents_by_email = AgentsByEmail.objects.create(email=email, stay=stay)

            encoded_email = self.request.data.get("encoded_email")
            
            activate_url = f"http://localhost:3000/partner/signin/agent/{encoded_email}" if settings.DEBUG else f"https://www.safaripricer.com/partner/signin/agent/{encoded_email}"

            message = EmailMessage(
                to=(email, ),
            )
            message.template_id = "5032694"
            message.from_email = None
            message.merge_data = {
                email: {
                    "activate_url": activate_url
                },
            }

            message.merge_global_data = {
                "activate_url": activate_url
            }
            message.send()
            
            instance.agents_by_email.add(agents_by_email)
            instance.save()
            return instance
    

class UserStayEmailRemoveAgentsView(generics.UpdateAPIView):
    serializer_class = LodgeStaySerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "slug"

    def get_queryset(self):
        queryset = Stays.objects.filter(
            user=self.request.user,
        )
        slug = self.kwargs.get("slug")
        email = self.request.user.email

        if slug is not None:
            queryset = Stays.objects.filter(slug=slug, contact_email=email).select_related("user").prefetch_related(
                "stay_images",
            )
        return queryset
    
    def perform_update(self, serializer):
        instance = serializer.save()
        agent_id = self.request.data.get("agent_id")
        agent_id = int(agent_id)
        agent = generics.get_object_or_404(Agents, id=agent_id)
        if agent.user.is_agent == False:
            raise PermissionDenied("This user is not an agent")
        
        # check if agent is already added
        if agent not in instance.agents.all():
            raise ValidationError("This agent is not added")
        
        instance.agents.remove(agent)
        agent.delete()
        instance.save()
        return instance



class RoomTypeCreateView(generics.CreateAPIView):
    serializer_class = RoomTypeSerializer
    queryset = RoomType.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        stay_slug = self.kwargs.get("stay_slug")
        stay = generics.get_object_or_404(Stays, slug=stay_slug)

        if stay.contact_email != self.request.user.email:
            raise PermissionDenied("You are not the owner of this stay")

        serializer.save(stay=stay)


class RoomTypeDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RoomTypeSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "slug"

    def get_queryset(self):
        stay_slug = self.kwargs.get("stay_slug")
        stay = generics.get_object_or_404(Stays, slug=stay_slug)

        if stay.contact_email != self.request.user.email:
            raise PermissionDenied("You are not the owner of this stay")

        queryset = RoomType.objects.filter(stay=stay)

        return queryset


class RoomTypeListView(generics.ListAPIView):
    queryset = RoomType.objects.all()
    serializer_class = RoomTypeSerializer

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        stay_slug = self.kwargs.get("stay_slug")
        stay = generics.get_object_or_404(Stays, slug=stay_slug)

        queryset = queryset.filter(stay=stay)

        start_date = self.request.query_params.get("start_date")
        end_date = self.request.query_params.get("end_date")

        if start_date and end_date:
            queryset = queryset.filter(stay=stay).prefetch_related(
                Prefetch(
                    "room_resident_availabilities",
                    queryset=RoomAvailabilityResident.objects.filter(
                        date__range=[start_date, end_date]
                    ),
                ),
                Prefetch(
                    "room_non_resident_availabilities",
                    queryset=RoomAvailabilityNonResident.objects.filter(
                        date__range=[start_date, end_date]
                    ),
                ),
            )
        return queryset
    

class RoomTypeDetailListView(generics.ListAPIView):
    queryset = RoomType.objects.all()
    serializer_class = RoomTypeDetailSerializer

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        stay_slug = self.kwargs.get("stay_slug")
        stay = generics.get_object_or_404(Stays, slug=stay_slug)

        queryset = queryset.filter(stay=stay)
        return queryset
    

class RoomTypeListDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = RoomType.objects.all()
    serializer_class = RoomTypeDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        stay_slug = self.kwargs.get("stay_slug")
        stay = generics.get_object_or_404(Stays, slug=stay_slug)

        if stay.contact_email != self.request.user.email:
            raise PermissionDenied("You are not the owner of this stay")

        queryset = RoomType.objects.filter(stay=stay)

        return queryset


class RoomAvailabilityListView(generics.ListAPIView):
    serializer_class = RoomAvailabilitySerializer

    def get_queryset(self):
        room_type_slug = self.kwargs.get("room_type_slug")

        room_type = generics.get_object_or_404(RoomType, slug=room_type_slug)
        queryset = RoomAvailability.objects.filter(room_type=room_type)

        return queryset


class OtherFeesResidentListView(generics.ListCreateAPIView):
    serializer_class = OtherFeesResidentSerializer

    def get_queryset(self):
        stay_slug = self.kwargs.get("stay_slug")
        stay = generics.get_object_or_404(Stays, slug=stay_slug)

        queryset = OtherFeesResident.objects.filter(stay=stay)

        return queryset

    def perform_create(self, serializer):
        stay_slug = self.kwargs.get("stay_slug")
        stay = generics.get_object_or_404(Stays, slug=stay_slug)

        serializer.save(stay=stay)


class ActivityFeesListCreateView(generics.ListCreateAPIView):
    serializer_class = ActivityFeesSerializer

    def get_queryset(self):
        stay_slug = self.kwargs.get("stay_slug")
        stay = generics.get_object_or_404(
            Stays, slug=stay_slug, is_partner_property=True
        )

        queryset = ActivityFee.objects.filter(stay=stay)

        return queryset

    def perform_create(self, serializer):
        stay_slug = self.kwargs.get("stay_slug")
        stay = generics.get_object_or_404(Stays, slug=stay_slug)

        serializer.save(stay=stay)


class ParkFeesListCreateView(generics.ListCreateAPIView):
    serializer_class = ParkFeesSerializer

    def get_queryset(self):
        stay_slug = self.kwargs.get("stay_slug")
        stay = generics.get_object_or_404(
            Stays, slug=stay_slug, is_partner_property=True
        )

        queryset = ParkFees.objects.filter(stay=stay)

        return queryset

    def perform_create(self, serializer):
        stay_slug = self.kwargs.get("stay_slug")
        stay = generics.get_object_or_404(Stays, slug=stay_slug)

        serializer.save(stay=stay)


class ParkFeesDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ParkFeesSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        stay_slug = self.kwargs.get("stay_slug")
        stay = generics.get_object_or_404(
            Stays, slug=stay_slug, is_partner_property=True
        )

        queryset = ParkFees.objects.filter(stay=stay)

        return queryset


class ActivityFeesDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ActivityFeesSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        stay_slug = self.kwargs.get("stay_slug")
        stay = generics.get_object_or_404(
            Stays, slug=stay_slug, is_partner_property=True
        )

        queryset = ActivityFee.objects.filter(stay=stay)

        return queryset


class OtherFeesNonResidentListView(generics.ListCreateAPIView):
    serializer_class = OtherFeesNonResidentSerializer

    def get_queryset(self):
        stay_slug = self.kwargs.get("stay_slug")
        stay = generics.get_object_or_404(Stays, slug=stay_slug)

        queryset = OtherFeesNonResident.objects.filter(stay=stay)

        return queryset

    def perform_create(self, serializer):
        stay_slug = self.kwargs.get("stay_slug")
        stay = generics.get_object_or_404(Stays, slug=stay_slug)

        serializer.save(stay=stay)


class OtherFeesResidentDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OtherFeesResidentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        stay_slug = self.kwargs.get("stay_slug")
        stay = generics.get_object_or_404(Stays, slug=stay_slug)

        queryset = OtherFeesResident.objects.filter(stay=stay)

        return queryset


class OtherFeesNonResidentDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OtherFeesNonResidentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        stay_slug = self.kwargs.get("stay_slug")
        stay = generics.get_object_or_404(Stays, slug=stay_slug)

        queryset = OtherFeesNonResident.objects.filter(stay=stay)

        return queryset


class RoomAvailabilityResidentView(ListBulkCreateUpdateDestroyAPIView):
    serializer_class = RoomAvailabilityResidentSerializer

    def get_queryset(self):
        room_type_slug = self.kwargs.get("room_type_slug")

        room_type = generics.get_object_or_404(RoomType, slug=room_type_slug)

        queryset = RoomAvailabilityResident.objects.filter(room_type=room_type)

        start_date = self.request.query_params.get("start_date")
        end_date = self.request.query_params.get("end_date")

        if start_date and end_date:
            queryset = RoomAvailabilityResident.objects.filter(
                room_type=room_type,
                date__range=[start_date, end_date],
            ).order_by("date")

        return queryset

    def perform_create(self, serializer):
        room_type_slug = self.kwargs.get("room_type_slug")
        room_type = generics.get_object_or_404(RoomType, slug=room_type_slug)

        if room_type.stay.contact_email != self.request.user.email:
            raise PermissionDenied("You are not the owner of this stay")

        # check if date already exists then delete it
        dates_to_delete = [data["date"] for data in self.request.data]

        RoomAvailabilityResident.objects.filter(
            room_type=room_type, date__in=dates_to_delete
        ).delete()

        availabilities = serializer.save(room_type=room_type)

        resident_guest_list = []

        for data, availability in zip(self.request.data, availabilities):
            for item in data["room_resident_guest_availabilities"]:
                resident_guest = RoomAvailabilityResidentGuest(
                    room_availability_resident=availability, **item
                )
                resident_guest_list.append(resident_guest)

        RoomAvailabilityResidentGuest.objects.bulk_create(
            resident_guest_list, batch_size=100
        )

    def perform_update(self, serializer):
        room_type_slug = self.kwargs.get("room_type_slug")
        room_type = generics.get_object_or_404(RoomType, slug=room_type_slug)

        if room_type.stay.contact_email != self.request.user.email:
            raise PermissionDenied("You are not the owner of this stay")

        availabilities = serializer.save(room_type=room_type)

        for data, availability in zip(self.request.data, availabilities):
            for item in data["room_resident_guest_availabilities"]:
                RoomAvailabilityResidentGuest.objects.update_or_create(
                    room_availability_resident=availability,
                    id=item["id"],
                    defaults=item,
                )


class RoomAvailabilityResidentDeleteView(generics.DestroyAPIView):
    serializer_class = RoomAvailabilityResidentSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "slug"

    def get_queryset(self):
        room_type_slug = self.kwargs.get("room_type_slug")

        room_type = generics.get_object_or_404(RoomType, slug=room_type_slug)
        queryset = RoomAvailabilityResident.objects.filter(room_type=room_type)

        return queryset


class RoomAvailabilityNonResidentView(ListBulkCreateUpdateDestroyAPIView):
    serializer_class = RoomAvailabilityNonResidentSerializer

    def get_queryset(self):
        room_type_slug = self.kwargs.get("room_type_slug")

        room_type = generics.get_object_or_404(RoomType, slug=room_type_slug)
        queryset = RoomAvailabilityNonResident.objects.filter(room_type=room_type)

        start_date = self.request.query_params.get("start_date")
        end_date = self.request.query_params.get("end_date")

        if start_date and end_date:
            queryset = RoomAvailabilityNonResident.objects.filter(
                room_type=room_type,
                date__range=[start_date, end_date],
            ).order_by("date")

        return queryset

    def perform_create(self, serializer):
        room_type_slug = self.kwargs.get("room_type_slug")
        room_type = generics.get_object_or_404(RoomType, slug=room_type_slug)

        if room_type.stay.contact_email != self.request.user.email:
            raise PermissionDenied("You are not the owner of this stay")

        # check if date already exists then delete it
        dates_to_delete = [data["date"] for data in self.request.data]

        RoomAvailabilityNonResident.objects.filter(
            room_type=room_type, date__in=dates_to_delete
        ).delete()

        availabilities = serializer.save(room_type=room_type)

        non_resident_guest_list = []

        for data, availability in zip(self.request.data, availabilities):
            for item in data["room_non_resident_guest_availabilities"]:
                non_resident_guest = RoomAvailabilityNonResidentGuest(
                    room_availability_non_resident=availability, **item
                )
                non_resident_guest_list.append(non_resident_guest)

        RoomAvailabilityNonResidentGuest.objects.bulk_create(
            non_resident_guest_list, batch_size=100
        )

    def perform_update(self, serializer):
        room_type_slug = self.kwargs.get("room_type_slug")
        room_type = generics.get_object_or_404(RoomType, slug=room_type_slug)

        if room_type.stay.contact_email != self.request.user.email:
            raise PermissionDenied("You are not the owner of this stay")

        availabilities = serializer.save(room_type=room_type)

        for data, availability in zip(self.request.data, availabilities):
            for item in data["room_non_resident_guest_availabilities"]:
                RoomAvailabilityNonResidentGuest.objects.update_or_create(
                    room_availability_non_resident=availability,
                    id=item["id"],
                    defaults=item,
                )

    def allow_bulk_destroy(self, qs, filtered):
        return qs is not filtered


class RoomAvailabilityNonResidentDeleteView(generics.DestroyAPIView):
    serializer_class = RoomAvailabilityNonResidentSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "slug"

    def get_queryset(self):
        room_type_slug = self.kwargs.get("room_type_slug")

        room_type = generics.get_object_or_404(RoomType, slug=room_type_slug)
        queryset = RoomAvailabilityNonResident.objects.filter(room_type=room_type)

        return queryset


class RoomAvailabilityDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RoomAvailabilitySerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "slug"

    def get_queryset(self):
        room_type_slug = self.kwargs.get("room_type_slug")
        room_type = generics.get_object_or_404(RoomType, slug=room_type_slug)

        if room_type.stay.contact_email != self.request.user.email:
            raise PermissionDenied("You are not the owner of this stay")

        queryset = RoomAvailability.objects.filter(room_type=room_type)

        return queryset


class RoomAvailabilityResidentDeleteView(generics.DestroyAPIView):
    serializer_class = RoomTypeSerializer
    permission_classes = [IsAuthenticated]
    queryset = RoomType.objects.all()
    lookup_field = "slug"

    def perform_destroy(self, instance):
        room_type_slug = self.kwargs.get("slug")
        room_type = generics.get_object_or_404(RoomType, slug=room_type_slug)
        RoomAvailabilityResident.objects.filter(room_type=room_type).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RoomAvailabilityNonResidentDeleteView(generics.DestroyAPIView):
    serializer_class = RoomTypeSerializer
    permission_classes = [IsAuthenticated]
    queryset = RoomType.objects.all()
    lookup_field = "slug"

    def perform_destroy(self, instance):
        room_type_slug = self.kwargs.get("slug")
        room_type = generics.get_object_or_404(RoomType, slug=room_type_slug)
        RoomAvailabilityNonResident.objects.filter(room_type=room_type).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RoomAvailabilityCreateView(generics.CreateAPIView):
    serializer_class = RoomAvailabilitySerializer
    queryset = RoomAvailability.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        room_type_slug = self.kwargs.get("room_type_slug")
        room_type = generics.get_object_or_404(RoomType, slug=room_type_slug)

        date = self.request.data.get("date")
        if date:
            RoomAvailability.objects.filter(room_type=room_type, date=date).delete()

        if room_type.stay.contact_email != self.request.user.email:
            raise PermissionDenied("You are not the owner of this stay")

        serializer.save(room_type=room_type)


class RoomAvailabilityResidentGuestDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RoomAvailabilityResidentGuestSerializer
    queryset = RoomAvailabilityResidentGuest.objects.all()
    permission_classes = [IsAuthenticated]


class RoomAvailabilityNonResidentGuestDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RoomAvailabilityNonResidentGuestSerializer
    queryset = RoomAvailabilityNonResidentGuest.objects.all()
    permission_classes = [IsAuthenticated]

class BookingsCreateView(generics.CreateAPIView):
    serializer_class = BookingsSerializer
    queryset = Bookings.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        room_type_slug = self.kwargs.get("room_type_slug")
        room_type = generics.get_object_or_404(RoomType, slug=room_type_slug)

        serializer.save(room_type=room_type)


class BookingsListView(generics.ListAPIView):
    serializer_class = BookingsSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = BookingsFilter
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    def get_queryset(self):
        queryset = Bookings.objects.all()
        date = self.request.query_params.get("date")
        if date:
            queryset = Bookings.objects.filter(
                Q(check_in_date__lte=date) & Q(check_out_date__gte=date)
            )
        return queryset


class UserStayDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = StaysSerializer
    permission_classes = [IsAuthenticated, IsUserStayInstance]
    lookup_field = "slug"

    def get_queryset(self):
        queryset = Stays.objects.filter(
            user=self.request.user,
        )
        slug = self.kwargs.get("slug")

        if slug is not None:
            queryset = Stays.objects.filter(slug=slug, user=self.request.user)
        return queryset


class EventListView(generics.ListAPIView):
    serializer_class = StaysSerializer
    filterset_class = StayFilter
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = [
        "date_posted",
        "rooms",
        "beds",
        "bathrooms",
    ]
    pagination_class = StayPagination

    def get_queryset(self):
        queryset = Stays.objects.filter(is_active=True, is_an_event=True)
        return queryset


class AllStaysListView(generics.ListAPIView):
    serializer_class = StaysSerializer
    filterset_class = StayFilter
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = [
        "date_posted",
        "rooms",
        "beds",
        "bathrooms",
    ]
    ordering = []

    def get_queryset(self):
        queryset = Stays.objects.filter(
            is_active=True,
        )

        querystring = self.request.GET.get("search")
        querystring_detail_search = self.request.GET.get("d_search")
        if querystring:
            querystring = querystring.split(",")[0]
            words = re.split(r"[^A-Za-z']+", querystring)
            query = Q()  # empty Q object
            for word in words:
                # 'or' the queries together
                query |= Q(location__icontains=word) | Q(city__icontains=word)
            queryset = Stays.objects.filter(
                query,
                is_active=True,
            ).all()

        if querystring_detail_search:
            querystring_detail_search = querystring_detail_search.split(",")[0]
            words = re.split(r"[^A-Za-z']+", querystring_detail_search)
            query = Q()  # empty Q object
            for word in words:
                # 'or' the queries together
                query |= (
                    Q(location__icontains=word)
                    | Q(city__icontains=word)
                    | Q(country__icontains=word)
                )
            queryset = Stays.objects.filter(
                query,
                is_active=True,
            ).all()

        return queryset


class StayImageListView(generics.ListAPIView):
    serializer_class = StayImageSerializer
    pagination_class = None

    def get_queryset(self):
        queryset = StayImage.objects.all()

        stay_slug = self.kwargs.get("stay_slug")
        if stay_slug is not None:
            stay = generics.get_object_or_404(Stays, slug=stay_slug)
            queryset = StayImage.objects.filter(stay=stay)

        return queryset


class StayImageCreateView(generics.CreateAPIView):
    queryset = StayImage.objects.all()
    serializer_class = StayImageSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        stay_slug = self.kwargs.get("stay_slug")
        stay = generics.get_object_or_404(Stays, slug=stay_slug)
        stay_queryset = Stays.objects.filter(
            slug=stay_slug, contact_email=self.request.user.email
        )

        if not stay_queryset.exists():
            raise PermissionDenied("You can't add an image to this stay.")
        return serializer.save(stay=stay)


class StayImageDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = StayImageSerializer
    permission_classes = [IsUserStayInstance]

    def get_queryset(self):
        stay_slug = self.kwargs.get("stay_slug")
        if stay_slug is not None:
            stay = generics.get_object_or_404(Stays, slug=stay_slug)
            queryset = StayImage.objects.filter(stay=stay)

            return queryset


class ReviewListView(generics.ListAPIView):
    serializer_class = ReviewSerializer
    filterset_class = ReviewFilter
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = ["date_posted", "rate"]
    pagination_class = Pagination

    def get_queryset(self):
        queryset = Review.objects.all()

        stay_slug = self.kwargs.get("stay_slug")
        if stay_slug is not None:
            stay = generics.get_object_or_404(Stays, slug=stay_slug)
            queryset = Review.objects.filter(stay=stay)

        return queryset


class CreateStayViews(generics.CreateAPIView):
    serializer_class = StayViewsSerializer
    queryset = Views.objects.all()

    def get_user_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[-1].strip()
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip

    def perform_create(self, serializer):
        stay_slug = self.kwargs.get("stay_slug")
        stay = generics.get_object_or_404(Stays, slug=stay_slug)

        ip = self.get_user_ip(self.request)
        stay_queryset = Views.objects.filter(stay=stay, user_ip=ip)

        if stay_queryset.exists():
            return None
        return serializer.save(stay=stay, user_ip=ip)


class ReviewCreateView(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        stay_slug = self.kwargs.get("stay_slug")
        stay = generics.get_object_or_404(Stays, slug=stay_slug)

        review_queryset = Review.objects.filter(user=self.request.user, stay=stay)

        stay_queryset = Stays.objects.filter(slug=stay_slug, user=self.request.user)

        if review_queryset.exists():
            raise ValidationError("User has already reviewed this listing")

        elif stay_queryset.exists():
            raise PermissionDenied("You can't make a review on your listing")

        serializer.save(stay=stay, user=self.request.user)


class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [ObjectPermission]

    def get_queryset(self):
        stay_slug = self.kwargs.get("stay_slug")
        if stay_slug is not None:
            stay = generics.get_object_or_404(Stays, slug=stay_slug)
            queryset = Review.objects.filter(stay=stay)

        return queryset


class CartItemAPIView(generics.CreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated, ObjectPermission]

    def perform_create(self, serializer):
        stay_slug = self.kwargs.get("stay_slug")
        stay = generics.get_object_or_404(Stays, slug=stay_slug)

        serializer.save(user=self.request.user, stay=stay)


class CartListView(generics.ListAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)


class CartDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CartSerializer

    permission_classes = [IsAuthenticated, ObjectPermission]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)


class OrderCreateView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        stay_slug = self.kwargs.get("stay_slug")
        stay = generics.get_object_or_404(Stays, slug=stay_slug)

        serializer.save(user=self.request.user, stay=stay)

        # message sent to the user
        message = EmailMessage(
            to=[self.request.data["email"]],
        )
        message.template_id = "4282998"
        message.from_email = None
        message.merge_data = {
            self.request.data["email"]: {
                "name": self.request.data["first_name"],
                "stay_name": stay.name,
            },
        }

        message.merge_global_data = {
            "name": self.request.data["first_name"],
            "stay_name": stay.name,
        }
        message.send(fail_silently=True)

        # message sent to the admin
        order_message = EmailMessage(
            to=[settings.DEFAULT_FROM_EMAIL],
        )
        order_message.template_id = "4219329"
        order_message.from_email = None
        order_message.merge_data = {
            self.request.data["email"]: {
                "user_email": self.request.data["email"],
                "booking_type": "an accommodation",
                "name": stay.name,
            },
        }

        order_message.merge_global_data = {
            "user_email": self.request.data["email"],
            "booking_type": "an accommodation",
            "name": stay.name,
        }
        order_message.send(fail_silently=True)


class EventCreateView(generics.CreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def perform_create(self, serializer):
        stay_slug = self.kwargs.get("stay_slug")
        stay = generics.get_object_or_404(Stays, slug=stay_slug)

        serializer.save(stay=stay)

        # message sent to the user
        message = EmailMessage(
            to=[self.request.data["email"]],
        )
        message.template_id = "4282998"
        message.from_email = None
        message.merge_data = {
            self.request.data["email"]: {
                "name": self.request.data["first_name"],
            },
        }

        message.merge_global_data = {
            "name": self.request.data["first_name"],
        }
        message.send(fail_silently=True)

        # message sent to the admin
        order_message = EmailMessage(
            to=[settings.DEFAULT_FROM_EMAIL],
        )
        order_message.template_id = "4219329"
        order_message.from_email = None
        order_message.merge_data = {
            self.request.data["email"]: {
                "user_email": self.request.data["email"],
                "booking_type": "an accommodation",
                "name": stay.name,
            },
        }

        order_message.merge_global_data = {
            "user_email": self.request.data["email"],
            "booking_type": "an accommodation",
            "name": stay.name,
        }

        order_message.send(fail_silently=True)


class LodgePackageBookingCreateView(generics.CreateAPIView):
    queryset = LodgePackageBooking.objects.all()
    serializer_class = LodgePackageBookingSerializer

    def perform_create(self, serializer):
        stay_slug = self.kwargs.get("stay_slug")
        stay = generics.get_object_or_404(Stays, slug=stay_slug)

        serializer.save(stay=stay)

        # message sent to the user
        message = EmailMessage(
            to=[self.request.data["email"]],
        )
        message.template_id = "4491051"
        message.from_email = None
        message.merge_data = {
            self.request.data["email"]: {
                "name": self.request.data["first_name"],
            },
        }

        message.merge_global_data = {
            "name": self.request.data["first_name"],
        }
        message.send(fail_silently=True)

        # message sent to the admin
        order_message = EmailMessage(
            to=[settings.DEFAULT_FROM_EMAIL],
        )
        order_message.template_id = "4219329"
        order_message.from_email = None
        order_message.merge_data = {
            self.request.data["email"]: {
                "user_email": self.request.data["email"],
                "booking_type": "a lodge",
                "name": stay.name,
            },
        }

        order_message.merge_global_data = {
            "user_email": self.request.data["email"],
            "booking_type": "a lodge",
            "name": stay.name,
        }

        order_message.send(fail_silently=True)


class LodgePackageBookingInstallmentCreateView(generics.CreateAPIView):
    queryset = LodgePackageBookingInstallment.objects.all()
    serializer_class = LodgePackageBookingInstallmentSerializer

    def perform_create(self, serializer):
        stay_slug = self.kwargs.get("stay_slug")
        stay = generics.get_object_or_404(Stays, slug=stay_slug)

        serializer.save(stay=stay)


class RequestMail(APIView):
    def post(self, request, *args, **kwargs):
        if not request.user.is_partner:
            raise PermissionDenied

        elif request.method == "POST":
            message = EmailMessage(
                to=[settings.DEFAULT_FROM_EMAIL],
            )
            message.template_id = "4571457"
            message.from_email = None
            message.merge_data = {
                request.user.email: {
                    "name": request.user.first_name,
                    "user_email": request.user.email,
                },
            }

            message.merge_global_data = {
                "name": request.user.first_name,
                "user_email": request.user.email,
            }
            message.send(fail_silently=True)

            return Response({"message": "Mail sent successfully"})


class EventTransportCreateView(generics.CreateAPIView):
    queryset = EventTransport.objects.all()
    serializer_class = EventTransportSerializer

    def perform_create(self, serializer):
        serializer.save()

        message = EmailMessage(
            to=[self.request.data["email"]],
        )
        message.template_id = "4208873"
        message.from_email = None
        message.merge_data = {
            self.request.data["email"]: {
                "name": self.request.data["first_name"],
            },
        }

        message.merge_global_data = {
            "name": self.request.data["first_name"],
        }
        message.send(fail_silently=True)

        order_message = EmailMessage(
            to=[settings.DEFAULT_FROM_EMAIL],
        )
        order_message.template_id = "4219329"
        order_message.from_email = None
        order_message.merge_data = {
            self.request.data["email"]: {
                "user_email": self.request.data["email"],
            },
        }

        order_message.merge_global_data = {
            "user_email": self.request.data["email"],
        }

        order_message.send(fail_silently=True)


class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderPaidListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user, paid=True)


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, ObjectPermission]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class SaveStaysCreateView(generics.CreateAPIView):
    serializer_class = SaveStaysSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return SaveStays.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        stay_slug = self.kwargs.get("stay_slug")
        stay = generics.get_object_or_404(Stays, slug=stay_slug)

        save_queryset = SaveStays.objects.filter(user=self.request.user, stay=stay)

        if save_queryset.exists():
            raise ValidationError("User has already saved this listing")

        serializer.save(stay=stay, user=self.request.user)


class SaveStaysListView(generics.ListAPIView):
    serializer_class = SaveStaysSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return SaveStays.objects.filter(user=self.request.user)


class SaveStaysDetailView(generics.RetrieveDestroyAPIView):
    serializer_class = SaveStaysSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return SaveStays.objects.filter(user=self.request.user)


class SaveStaysDeleteView(generics.DestroyAPIView):
    serializer_class = SaveStaysSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "stay_id"

    def get_queryset(self):
        return SaveStays.objects.filter(user=self.request.user)

    def perform_destroy(self, instance):
        stay_id = self.kwargs.get("stay_id")
        stay = generics.get_object_or_404(Stays, id=stay_id)

        save_queryset = SaveStays.objects.filter(user=self.request.user, stay=stay)

        if save_queryset.exists():
            save_queryset.delete()


class ScheduleDemo(APIView):
    def post(self, request, *args, **kwargs):
        if request.method == "POST":
            message = EmailMessage(
                to=[settings.DEFAULT_FROM_EMAIL],
            )
            message.template_id = "4934533"
            message.from_email = None
            message.merge_data = {
                request.data["email"]: {
                    "first_name": request.data["first_name"],
                    "last_name": request.data["last_name"],
                    "user_email": request.data["email"],
                    "message": request.data["message"],
                },
            }

            message.merge_global_data = {
                "first_name": request.data["first_name"],
                "last_name": request.data["last_name"],
                "user_email": request.data["email"],
                "message": request.data["message"],
            }
            message.send(fail_silently=True)

            return Response({"message": "Mail sent successfully"})

import re
from lodging.api.pagination import Pagination, StayPagination, PartnerStayPagination
from .serializers import *
from lodging.models import *
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
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
import uuid

from rest_framework_bulk import (
    ListBulkCreateUpdateDestroyAPIView,
)


class StaysCreateView(generics.CreateAPIView):
    serializer_class = StaysSerializer
    queryset = Stays.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        stay = serializer.save(user=self.request.user)
        property_access = PropertyAccess.objects.get_or_create(
            email=self.request.user.email,
            stay=stay,
        )
        serializer.save(user=self.request.user)


class StaysDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = StaysSerializer
    permission_classes = [AllowAny]
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
    permission_classes = [AllowAny]

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
        return (
            Stays.objects.filter(
                Q(property_access__email=self.request.user.email)
                | Q(property_access__email=self.request.user.primary_email)
                | Q(user=self.request.user),
                is_partner_property=True,
            )
            .select_related("user")
            .prefetch_related(
                "stay_images",
            )
            .distinct()
        )


class TestPartnerStaysListView(generics.ListAPIView):
    serializer_class = StaysSerializer
    queryset = Stays.objects.filter(is_partner_property=True)


class PartnerStaysDetailView(generics.ListAPIView):
    serializer_class = PartnerStaySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        list_ids = self.kwargs.get("list_ids")
        list_ids = list_ids.split(",")
        user = generics.get_object_or_404(CustomUser, id=self.request.user.id)
        queryset = (
            Stays.objects.filter(
                is_partner_property=True,
                id__in=list_ids,
            )
            .select_related("user")
            .prefetch_related(
                "activity_fees",
                "other_fees_resident",
                "other_fees_non_resident",
                "stay_images",
            )
            .all()
            .distinct()
        )

        # order queryset based on the list_ids
        queryset = sorted(queryset, key=lambda x: list_ids.index(str(x.id)))

        return queryset


class PartnerStaysWithoutContractView(generics.ListAPIView):
    serializer_class = LodgeStayWaitingForApprovalSerializer
    ordering_fields = ["date_posted"]
    pagination_class = PartnerStayPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        search_query = self.request.GET.get("search", "")
        user = generics.get_object_or_404(CustomUser, id=self.request.user.id)

        approved_agents = Agents.objects.filter(approved=True, user=user)

        approved_agents_by_email = AgentsByEmail.objects.filter(
            email=user.primary_email
        )

        queryset = (
            Stays.objects.filter(
                Q(location__icontains=search_query)
                | Q(property_name__icontains=search_query),
                is_partner_property=True,
            )
            .exclude(
                Q(agent_access__in=approved_agents)
                | Q(agents_email__in=approved_agents_by_email)
                | Q(property_access__email=user.email)
                | Q(property_access__email=user.primary_email)
                | Q(user=user),
            )
            .select_related("user")
            .prefetch_related(
                "stay_images",
            )
            .all()
        )

        return queryset


class CombinedPartnerStaysListView(generics.ListAPIView):
    serializer_class = LodgeStaySerializer
    ordering_fields = ["date_posted"]
    pagination_class = PartnerStayPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        search_query = self.request.GET.get("search", "")
        contracts = self.request.GET.get("contracts", "")
        user = generics.get_object_or_404(CustomUser, id=self.request.user.id)

        approved_agents = Agents.objects.filter(approved=True, user=user)

        queryset = (
            Stays.objects.filter(
                Q(location__icontains=search_query)
                | Q(property_name__icontains=search_query),
                is_partner_property=True,
            )
            .select_related("user")
            .prefetch_related(
                "stay_images",
            )
            .all()
            .distinct()
        )

        if contracts == "1":
            queryset = queryset.filter(
                Q(agent_access__in=approved_agents)
                | Q(agents_email__email=user.email)
                | Q(property_access__email=user.email)
                | Q(property_access__email=user.primary_email)
                | Q(user=user),
            ).distinct()

        queryset = sorted(
            queryset,
            key=lambda x: (
                x.agent_access.filter(user=user).exists()
                or x.agents_email.filter(email=user.email).exists()
                or x.property_access.filter(email=user.primary_email).exists()
                or x.user == user
            ),
            reverse=True,
        )

        return queryset


class PartnerStaysListView(generics.ListAPIView):
    serializer_class = LodgeStaySerializer
    ordering_fields = ["date_posted"]
    pagination_class = PartnerStayPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        search_query = self.request.GET.get("search", "")
        user = generics.get_object_or_404(CustomUser, id=self.request.user.id)

        queryset = (
            Stays.objects.filter(
                Q(location__icontains=search_query)
                | Q(property_name__icontains=search_query),
                Q(agent_access__user=user, agent_access__approved=True)
                | Q(agents_email__email=user.email)
                | Q(property_access__email=user.email)
                | Q(property_access__email=user.primary_email)
                | Q(user=user),
                is_partner_property=True,
            )
            .select_related("user")
            .prefetch_related(
                "stay_images",
            )
            .all()
            .distinct()
        )

        return queryset


class UserStaysEmailDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LodgeStaySerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "slug"

    def get_queryset(self):
        slug = self.kwargs.get("slug")

        queryset = Stays.objects.filter(user=self.request.user, slug=slug)
        email = self.request.user.primary_email

        if slug is not None:
            queryset = (
                Stays.objects.filter(
                    Q(property_access__email=email)
                    | Q(property_access__email=self.request.user.email)
                    | Q(user=self.request.user),
                    slug=slug,
                )
                .select_related("user")
                .prefetch_related(
                    "stay_images",
                )
                .distinct()
            )
        return queryset


class UserStayEmailAgentListView(generics.ListAPIView):
    serializer_class = AgentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        slug = self.kwargs.get("slug")
        email = self.request.user.email
        queryset = generics.get_object_or_404(Stays, slug=slug)
        return Agents.objects.filter(stay=queryset, approved=True)


class UserStayEmailAgentNotVerifiedListView(generics.ListAPIView):
    serializer_class = AgentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        slug = self.kwargs.get("slug")
        email = self.request.user.email
        queryset = generics.get_object_or_404(Stays, slug=slug)
        return Agents.objects.filter(stay=queryset, approved=False)


class AgentAccessDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AgentSerializer
    permission_classes = [IsAuthenticated]
    queryset = Agents.objects.all()


class HiglighedDetailStayListView(generics.ListAPIView):
    serializer_class = DetailStaySerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return (
            Stays.objects.filter(in_homepage=True, has_options=True)
            .select_related("user")
            .prefetch_related(
                "stay_images",
            )
        )


class HiglighedDetailStayRetrieveView(generics.RetrieveAPIView):
    serializer_class = DetailStayWithAmenitiesSerializer
    lookup_field = "slug"
    permission_classes = [AllowAny]

    def get_queryset(self):
        slug = self.kwargs.get("slug")
        return (
            Stays.objects.filter(in_homepage=True, has_options=True, slug=slug)
            .select_related("user")
            .prefetch_related(
                "stay_images",
                "extras_included",
                "other_options",
                "private_safari",
                "shared_safari",
                "all_inclusive",
                "facts",
                "inclusions",
            )
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
            queryset = (
                Stays.objects.filter(
                    Q(property_access__email=self.request.user.email)
                    | Q(property_access__email=self.request.user.primary_email),
                    slug=slug,
                )
                .select_related("user")
                .prefetch_related(
                    "stay_images",
                )
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

        # check if agent is already added
        if instance.agents.filter(user=user).exists():
            agent_obj = instance.agents.get(user=user)
            instance.agents.remove(agent_obj)
            agent_obj.delete()

        instance.save()
        return instance


class UserStayEmailUpdateAgentsWithFileView(generics.UpdateAPIView):
    serializer_class = LodgeStaySerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "slug"

    def get_queryset(self):
        slug = self.kwargs.get("slug")
        queryset = (
            Stays.objects.filter(slug=slug)
            .select_related("user")
            .prefetch_related(
                "stay_images",
            )
        )

        return queryset

    def perform_update(self, serializer):
        instance = serializer.save()
        user = self.request.user
        stay_slug = self.kwargs.get("slug")
        stay = generics.get_object_or_404(Stays, slug=stay_slug)
        document = self.request.data.get("document")
        agent = Agents.objects.create(
            user=user, stay=stay, document=document, approved=False
        )
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
            if CustomUser.objects.filter(primary_email=obj.email).exists():
                user_qs.append(
                    {
                        "id": obj.id,
                        "user": CustomUser.objects.get(primary_email=obj.email),
                    }
                )

        return user_qs


class PropertyAccessListView(generics.ListAPIView):
    serializer_class = PropertyAccessSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_qs = []
        stay_slug = self.kwargs.get("slug")
        stay = generics.get_object_or_404(Stays, slug=stay_slug)

        for obj in PropertyAccess.objects.filter(stay=stay).exclude(
            email=stay.user.primary_email
        ):
            if CustomUser.objects.filter(primary_email=obj.email).exists():
                user_qs.append(
                    {
                        "id": obj.id,
                        "user": CustomUser.objects.get(primary_email=obj.email),
                    }
                )

        return user_qs


class ProperyAccessNotVerifiedListView(generics.ListAPIView):
    serializer_class = PropertyAccessSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_qs = []
        stay_slug = self.kwargs.get("slug")
        stay = generics.get_object_or_404(Stays, slug=stay_slug)

        for obj in PropertyAccess.objects.filter(stay=stay):
            if not CustomUser.objects.filter(primary_email=obj.email).exists():
                user_qs.append(obj)

        return user_qs


class UserAgentAccessByEmailNotVerifiedListView(generics.ListAPIView):
    serializer_class = AgentByEmailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_qs = []
        stay_slug = self.kwargs.get("slug")
        stay = generics.get_object_or_404(Stays, slug=stay_slug)

        for obj in AgentsByEmail.objects.filter(stay=stay, accepted=False):
            if not CustomUser.objects.filter(primary_email=obj.email).exists():
                user_qs.append(obj)

        return user_qs


class CheckAgentByEmailExistsView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        invitation_code = request.data.get("invitation_code")
        email = request.data.get("email")
        if AgentsByEmail.objects.filter(
            invitation_code=invitation_code, email=email, accepted=False
        ).exists():
            return Response({"exists": True}, status=status.HTTP_200_OK)
        else:
            return Response({"exists": False}, status=status.HTTP_404_NOT_FOUND)


class CheckPropertyAccessExistsView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        invitation_code = request.data.get("invitation_code")
        email = request.data.get("email")
        if PropertyAccess.objects.filter(
            invitation_code=invitation_code, email=email, accepted_invite=False
        ).exists():
            return Response({"exists": True}, status=status.HTTP_200_OK)
        else:
            return Response({"exists": False}, status=status.HTTP_404_NOT_FOUND)


class PropertyAccessDetailView(generics.DestroyAPIView):
    serializer_class = PropertyAccessSerializer
    permission_classes = [IsAuthenticated]
    queryset = PropertyAccess.objects.all()


class PropertyAccessCreateView(generics.CreateAPIView):
    serializer_class = PropertyAccessSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        email = self.request.data.get("email")
        stay_slug = self.kwargs.get("slug")
        stay = generics.get_object_or_404(Stays, slug=stay_slug)

        if PropertyAccess.objects.filter(email=email, stay=stay).exists():
            return

        else:
            if not CustomUser.objects.filter(primary_email=email).exists():
                invitation_code = uuid.uuid4()
                encoded_email = self.request.data.get("encoded_email")

                activate_url = (
                    f"http://localhost:3000/signin/property/{invitation_code}/{encoded_email}"
                    if settings.DEBUG
                    else f"https://www.safaripricer.com/signin/property/{invitation_code}/{encoded_email}"
                )

                message = EmailMessage(
                    to=(email,),
                )
                message.template_id = "5044128"
                message.from_email = None
                message.merge_data = {
                    email: {"activate_url": activate_url},
                }

                message.merge_global_data = {"activate_url": activate_url}
                message.send(fail_silently=True)

                PropertyAccess.objects.create(
                    email=email,
                    stay=stay,
                    invitation_code=invitation_code,
                )

            else:
                PropertyAccess.objects.create(
                    email=email,
                    stay=stay,
                )


class AddAgentFromInviteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, serializer):
        invitation_code = self.request.data.get("invitation_code")

        agent_by_email = generics.get_object_or_404(
            AgentsByEmail, invitation_code=invitation_code
        )

        if agent_by_email.accepted == True:
            return Response(
                {"message": "This invitation has already been accepted"},
                status=status.HTTP_404_NOT_FOUND,
            )
        Agents.objects.create(
            user=self.request.user,
            approved=True,
            stay=agent_by_email.stay,
            contract_rate=agent_by_email.contract_rate,
            resident_contract_rate=agent_by_email.resident_contract_rate,
        )

        AgentDiscountRate.objects.create(
            user=self.request.user,
            stay=agent_by_email.stay,
            percentage=agent_by_email.contract_rate,
            resident_percentage=agent_by_email.resident_contract_rate,
        )
        agent_by_email.accepted = True
        agent_by_email.save()
        return Response(
            {"message": "Agent added successfully"}, status=status.HTTP_200_OK
        )


class AcceptPropertyInviteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, serializer):
        invitation_code = self.request.data.get("invitation_code")

        property_access = generics.get_object_or_404(
            PropertyAccess, invitation_code=invitation_code
        )

        if property_access.accepted_invite == True:
            return Response(
                {"message": "This invitation has already been accepted"},
                status=status.HTTP_404_NOT_FOUND,
            )
        property_access.accepted_invite = True
        property_access.email = self.request.user.primary_email
        property_access.save()
        return Response(
            {"message": "Property added successfully"}, status=status.HTTP_200_OK
        )


class AddAgentToStayView(generics.UpdateAPIView):
    serializer_class = LodgeStaySerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "slug"

    def get_queryset(self):
        slug = self.kwargs.get("slug")
        queryset = (
            Stays.objects.filter(slug=slug)
            .select_related("user")
            .prefetch_related(
                "stay_images",
            )
        )

        return queryset

    def perform_update(self, serializer):
        instance = serializer.save()
        stay_slug = self.kwargs.get("slug")
        stay = generics.get_object_or_404(Stays, slug=stay_slug)
        email = self.request.data.get("email")
        contract_rate = self.request.data.get("contract_rate")
        contract_rate = float(contract_rate)
        resident_contract_rate = self.request.data.get("resident_contract_rate")

        if (
            CustomUser.objects.filter(primary_email=email).exists()
            and Agents.objects.filter(user__primary_email=email).exists() != True
        ):
            user = generics.get_object_or_404(CustomUser, primary_email=email)
            agent = Agents.objects.create(
                user=user,
                stay=stay,
                approved=True,
                contract_rate=contract_rate,
                resident_contract_rate=resident_contract_rate,
            )
            instance.save()
            return instance
        elif (
            CustomUser.objects.filter(email=email).exists()
            and Agents.objects.filter(user__primary_email=email).exists() == True
        ):
            return
        else:
            if AgentsByEmail.objects.filter(email=email, stay=stay).exists():
                return

            invitation_code = uuid.uuid4()

            encoded_email = self.request.data.get("encoded_email")

            agents_by_email = AgentsByEmail.objects.create(
                email=email,
                stay=stay,
                invitation_code=invitation_code,
                contract_rate=contract_rate,
                resident_contract_rate=resident_contract_rate,
            )

            activate_url = (
                f"http://localhost:3000/signin/agent/{invitation_code}/{encoded_email}"
                if settings.DEBUG
                else f"https://www.safaripricer.com/signin/agent/{invitation_code}/{encoded_email}"
            )

            message = EmailMessage(
                to=(email,),
            )
            message.template_id = "5032694"
            message.from_email = None
            message.merge_data = {
                email: {
                    "activate_url": activate_url,
                    "property_name": stay.property_name,
                },
            }

            message.merge_global_data = {
                "activate_url": activate_url,
                "property_name": stay.property_name,
            }
            message.send(fail_silently=True)

            instance.save()
            return instance


class ResendAgentInviteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, serializer):
        agent_id = self.request.data.get("agent_id")
        agent_id = int(agent_id)
        agent_by_email = generics.get_object_or_404(AgentsByEmail, id=agent_id)
        invitation_code = agent_by_email.invitation_code
        encoded_email = self.request.data.get("encoded_email")

        activate_url = (
            f"http://localhost:3000/signin/agent/{invitation_code}/{encoded_email}"
            if settings.DEBUG
            else f"https://www.safaripricer.com/signin/agent/{invitation_code}/{encoded_email}"
        )

        message = EmailMessage(
            to=(agent_by_email.email,),
        )
        message.template_id = "5032694"
        message.from_email = None
        message.merge_data = {
            agent_by_email.email: {
                "activate_url": activate_url,
                "property_name": agent_by_email.stay.property_name,
            },
        }

        message.merge_global_data = {
            "activate_url": activate_url,
            "property_name": agent_by_email.stay.property_name,
        }
        message.send(fail_silently=True)
        return Response(
            {"message": "Invitation resent successfully"}, status=status.HTTP_200_OK
        )


class ResendPropertyInviteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, serializer):
        property_access_id = self.request.data.get("property_access_id")
        property_access_id = int(property_access_id)
        property_access = generics.get_object_or_404(
            PropertyAccess, id=property_access_id
        )
        invitation_code = property_access.invitation_code
        encoded_email = self.request.data.get("encoded_email")

        activate_url = (
            f"http://localhost:3000/signin/property/{invitation_code}/{encoded_email}"
            if settings.DEBUG
            else f"https://www.safaripricer.com/signin/property/{invitation_code}/{encoded_email}"
        )

        message = EmailMessage(
            to=(property_access.email,),
        )
        message.template_id = "5044128"
        message.from_email = None
        message.merge_data = {
            property_access.email: {
                "activate_url": activate_url,
            },
        }

        message.merge_global_data = {
            "activate_url": activate_url,
        }
        message.send(fail_silently=True)
        return Response(
            {"message": "Invitation resent successfully"}, status=status.HTTP_200_OK
        )


class AgentDiscountRateListCreateView(generics.ListCreateAPIView):
    serializer_class = AgentDiscountRateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        stay_slug = self.kwargs.get("slug")
        stay = generics.get_object_or_404(Stays, slug=stay_slug)
        queryset = AgentDiscountRate.objects.filter(
            stay=stay, user=self.request.user
        ).order_by("-start_date")

        # # sort queryset by start_date
        # queryset = sorted(queryset, key=lambda x: x.start_date, reverse=True)

        return queryset

    def perform_create(self, serializer):
        stay_slug = self.kwargs.get("slug")
        stay = generics.get_object_or_404(Stays, slug=stay_slug)
        agent_discount_no_date = AgentDiscountRate.objects.filter(
            stay=stay, user=self.request.user, start_date=None, end_date=None
        )

        check_date_exists = AgentDiscountRate.objects.filter(
            stay=stay,
            user=self.request.user,
            start_date=self.request.data.get("start_date"),
            end_date=self.request.data.get("end_date"),
        )
        if (
            agent_discount_no_date.exists()
            and not self.request.data.get("start_date")
            and not self.request.data.get("end_date")
        ):
            agent_discount_no_date.delete()

        if check_date_exists.exists():
            check_date_exists.delete()
        serializer.save(stay=stay, user=self.request.user)


class AgentDiscountRateDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AgentDiscountRateSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "pk"

    def get_queryset(self):
        stay_slug = self.kwargs.get("slug")
        stay = generics.get_object_or_404(Stays, slug=stay_slug)
        return AgentDiscountRate.objects.filter(stay=stay, user=self.request.user)


class UserStayEmailRemoveAgentsView(generics.DestroyAPIView):
    serializer_class = AgentSerializer
    queryset = Agents.objects.all()
    permission_classes = [IsAuthenticated]


class RoomTypeCreateView(generics.CreateAPIView):
    serializer_class = RoomTypeSerializer
    queryset = RoomType.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        stay_slug = self.kwargs.get("stay_slug")
        stay = generics.get_object_or_404(Stays, slug=stay_slug)

        # if not PropertyAccess.objects.filter(
        #     stay=stay, email=self.request.user.email
        # ).exists():
        #     raise PermissionDenied("You are not the owner of this stay")

        serializer.save(stay=stay)


class RoomTypeDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RoomTypeSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "slug"

    def get_queryset(self):
        stay_slug = self.kwargs.get("stay_slug")
        stay = generics.get_object_or_404(Stays, slug=stay_slug)

        if not PropertyAccess.objects.filter(
            stay=stay, email=self.request.user.email
        ).exists():
            raise PermissionDenied("You are not the owner of this stay")

        queryset = RoomType.objects.filter(stay=stay)

        return queryset


class RoomTypeListView(generics.ListAPIView):
    queryset = RoomType.objects.all()
    serializer_class = RoomTypeSerializer
    permission_classes = [IsAuthenticated]

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
                    ).order_by("date"),
                ),
                Prefetch(
                    "room_non_resident_availabilities",
                    queryset=RoomAvailabilityNonResident.objects.filter(
                        date__range=[start_date, end_date]
                    ).order_by("date"),
                ),
            )
        return queryset


class RoomTypeDetailListView(generics.ListAPIView):
    queryset = RoomType.objects.all()
    serializer_class = RoomTypeDetailSerializer
    permission_classes = [IsAuthenticated]

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

        # if not PropertyAccess.objects.filter(
        #     stay=stay, email=self.request.user.email
        # ).exists():
        #     raise PermissionDenied("You are not the owner of this stay")

        queryset = RoomType.objects.filter(stay=stay)

        return queryset


class RoomAvailabilityListView(generics.ListAPIView):
    serializer_class = RoomAvailabilitySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        room_type_slug = self.kwargs.get("room_type_slug")

        room_type = generics.get_object_or_404(RoomType, slug=room_type_slug)
        queryset = RoomAvailability.objects.filter(room_type=room_type)

        return queryset


class OtherFeesResidentListView(generics.ListCreateAPIView):
    serializer_class = OtherFeesResidentSerializer
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsAuthenticated]

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

        # if not PropertyAccess.objects.filter(
        #     stay=room_type.stay, email=self.request.user.email
        # ).exists():
        #     raise PermissionDenied("You are not the owner of this stay")

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

        # if not PropertyAccess.objects.filter(
        #     stay=room_type.stay, email=self.request.user.email
        # ).exists():
        #     raise PermissionDenied("You are not the owner of this stay")

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
    permission_classes = [IsAuthenticated]

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

        # if not PropertyAccess.objects.filter(
        #     stay=room_type.stay, email=self.request.user.email
        # ).exists():
        #     raise PermissionDenied("You are not the owner of this stay")

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

        if not PropertyAccess.objects.filter(
            stay=room_type.stay, email=self.request.user.email
        ).exists():
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

        if not PropertyAccess.objects.filter(
            stay=room_type.stay, email=self.request.user.email
        ).exists():
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

        if not PropertyAccess.objects.filter(
            stay=room_type.stay, email=self.request.user.email
        ).exists():
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
    permission_classes = [AllowAny]

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
            Q(property_access__email=self.request.user.email)
            | Q(property_access__email=self.request.user.primary_email),
            slug=stay_slug,
        )

        if not stay_queryset.exists():
            raise PermissionDenied("You can't add an image to this stay.")
        return serializer.save(stay=stay)


class StayImageDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = StayImageSerializer
    permission_classes = [IsAuthenticated]

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
    permission_classes = [AllowAny]

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
    permission_classes = [AllowAny]

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
    permission_classes = [AllowAny]

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
    permission_classes = [AllowAny]

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

from rest_framework import serializers
from skilltrace.models import (
    State, District, Scheme, Course, Provider, Person, PersonPII,
    ContactPoint, SchemeCrosswalk, ConsentArtefact, Employer,
    OutcomeEpisode, EvidenceItem, VerificationRequest, FollowUpTask,
    SurveyResponse, IdentityMatchQueue, ActionCase, AuditEvent
)


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = '__all__'


class DistrictSerializer(serializers.ModelSerializer):
    state_name = serializers.CharField(source='state.name', read_only=True)
    class Meta:
        model = District
        fields = '__all__'


class SchemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scheme
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class ProviderSerializer(serializers.ModelSerializer):
    district_name = serializers.CharField(source='district.name', read_only=True)
    state_name = serializers.CharField(source='state.name', read_only=True)
    class Meta:
        model = Provider
        fields = '__all__'


class EmployerSerializer(serializers.ModelSerializer):
    district_name = serializers.CharField(source='district.name', read_only=True)
    state_name = serializers.CharField(source='state.name', read_only=True)
    class Meta:
        model = Employer
        fields = '__all__'


class EvidenceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvidenceItem
        fields = '__all__'


class OutcomeEpisodeSerializer(serializers.ModelSerializer):
    employer_name = serializers.CharField(source='employer.legal_name', read_only=True)
    district_name = serializers.CharField(source='district.name', read_only=True)
    state_name = serializers.CharField(source='state.name', read_only=True)
    evidence_items = EvidenceItemSerializer(many=True, read_only=True)

    class Meta:
        model = OutcomeEpisode
        fields = '__all__'


class PersonPIISerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonPII
        exclude = ['phone_hash']


class SchemeCrosswalkSerializer(serializers.ModelSerializer):
    scheme_name = serializers.CharField(source='scheme.name', read_only=True)
    course_title = serializers.CharField(source='course.title', read_only=True)
    provider_name = serializers.CharField(source='provider.name', read_only=True)

    class Meta:
        model = SchemeCrosswalk
        fields = '__all__'


class TraineeDetailSerializer(serializers.ModelSerializer):
    pii = PersonPIISerializer(read_only=True)
    crosswalks = SchemeCrosswalkSerializer(many=True, read_only=True)
    outcome_episodes = OutcomeEpisodeSerializer(many=True, read_only=True)

    class Meta:
        model = Person
        fields = ['stid', 'state_code_first', 'status', 'created_at', 'pii', 'crosswalks', 'outcome_episodes']


class IdentityMatchQueueSerializer(serializers.ModelSerializer):
    candidate_a_details = serializers.SerializerMethodField()
    candidate_b_details = serializers.SerializerMethodField()

    class Meta:
        model = IdentityMatchQueue
        fields = '__all__'

    def get_candidate_a_details(self, obj):
        p = obj.candidate_a
        pii = getattr(p, 'pii', None)
        return {
            "stid": p.stid,
            "full_name": pii.full_name if pii else "Redacted",
            "dob": pii.dob if pii else "",
            "phone_last4": pii.phone_last4 if pii else "",
            "address": pii.address_line if pii else "",
            "state_code": p.state_code_first,
        }

    def get_candidate_b_details(self, obj):
        p = obj.candidate_b
        pii = getattr(p, 'pii', None)
        return {
            "stid": p.stid,
            "full_name": pii.full_name if pii else "Redacted",
            "dob": pii.dob if pii else "",
            "phone_last4": pii.phone_last4 if pii else "",
            "address": pii.address_line if pii else "",
            "state_code": p.state_code_first,
        }


class ConsentArtefactSerializer(serializers.ModelSerializer):
    stid = serializers.CharField(source='person.stid', read_only=True)

    class Meta:
        model = ConsentArtefact
        fields = '__all__'


class FollowUpTaskSerializer(serializers.ModelSerializer):
    stid = serializers.CharField(source='person.stid', read_only=True)
    full_name = serializers.CharField(source='person.pii.full_name', read_only=True)
    phone_masked = serializers.SerializerMethodField()
    district_name = serializers.SerializerMethodField()
    course_title = serializers.SerializerMethodField()

    class Meta:
        model = FollowUpTask
        fields = '__all__'

    def get_phone_masked(self, obj):
        cp = obj.person.contact_points.filter(is_primary=True).first()
        return cp.value_masked if cp else "+91 **********"

    def get_district_name(self, obj):
        cw = obj.person.crosswalks.first()
        return cw.provider.district.name if cw else "General"

    def get_course_title(self, obj):
        cw = obj.person.crosswalks.first()
        return cw.course.title if cw else "Vocational Skill"


class ActionCaseSerializer(serializers.ModelSerializer):
    district_name = serializers.CharField(source='district.name', read_only=True)
    state_name = serializers.CharField(source='state.name', read_only=True)
    provider_name = serializers.CharField(source='provider.name', read_only=True)
    course_title = serializers.CharField(source='course.title', read_only=True)

    class Meta:
        model = ActionCase
        fields = '__all__'


class AuditEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditEvent
        fields = '__all__'

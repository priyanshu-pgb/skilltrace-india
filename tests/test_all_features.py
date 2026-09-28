from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import User, Profile
from skills.models import Skill, UserSkill, score_to_level
from assessments.models import Question, AssessmentAttempt, PracticalTask
from jobs.models import Job, JobRequirement
from training.models import TrainingCourse, TrainingEnrollment
from employment.models import EmploymentRecord

class SkillBridgeCoreTests(TestCase):
    def setUp(self):
        self.client = Client()

        # Users
        self.student = User.objects.create_user(
            username='test_student',
            email='student@example.com',
            password='password123',
            role='user'
        )
        self.admin = User.objects.create_user(
            username='test_admin',
            email='admin@example.com',
            password='password123',
            role='admin',
            is_staff=True
        )

        # Skills
        self.python_skill = Skill.objects.create(name='Python', category='tech')
        self.sql_skill = Skill.objects.create(name='SQL', category='data')

        # Job
        self.job = Job.objects.create(
            title='Junior Data Engineer',
            slug='junior-data-engineer',
            department='Engineering'
        )
        self.req_python = JobRequirement.objects.create(
            job=self.job,
            skill=self.python_skill,
            required_level=4 # Advanced
        )
        self.req_sql = JobRequirement.objects.create(
            job=self.job,
            skill=self.sql_skill,
            required_level=3 # Intermediate
        )

        # Training
        self.course = TrainingCourse.objects.create(
            name='Mastering Python',
            skill=self.python_skill,
            target_level=4,
            provider='SkillBridge Lab'
        )

    # 1. Authentication Tests
    def test_user_registration(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'role': 'user',
            'password1': 'newsecurepass123',
            'password2': 'newsecurepass123',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())
        new_u = User.objects.get(username='newuser')
        self.assertTrue(hasattr(new_u, 'profile'))

    def test_user_login_and_logout(self):
        login_success = self.client.login(username='test_student', password='password123')
        self.assertTrue(login_success)
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)

    # 2. Skill Verification & Score Calculation Tests
    def test_claimed_vs_verified_distinction(self):
        # Claim level 3
        user_skill = UserSkill.objects.create(
            user=self.student,
            skill=self.python_skill,
            claimed_level=3,
            is_verified=False
        )
        self.assertFalse(user_skill.is_verified)
        self.assertEqual(user_skill.claimed_level, 3)

        # Perform verification calculation (MCQ=80, Practical=80, Project=80)
        # Final = (80 * 0.20) + (80 * 0.50) + (80 * 0.30) = 16 + 40 + 24 = 80.0%
        user_skill.mcq_score = 80.0
        user_skill.practical_score = 80.0
        user_skill.project_score = 80.0
        final_score = user_skill.recalculate_score()

        self.assertEqual(final_score, 80.0)
        self.assertTrue(user_skill.is_verified)
        self.assertEqual(user_skill.verified_level, 4) # 75-89 is Advanced (Level 4)
        self.assertEqual(user_skill.verified_level_name, 'Advanced')

    # 3. Mathematical Skill Gap Engine Tests
    def test_skill_gap_analysis(self):
        # Student has Python verified Level 4 (Advanced)
        UserSkill.objects.create(
            user=self.student,
            skill=self.python_skill,
            claimed_level=4,
            is_verified=True,
            verified_level=4,
            verified_score=80.0
        )
        # SQL is unverified (Level 0)
        analysis = self.job.calculate_match_for_user(self.student)
        
        # Total requirements: 2 (Python, SQL)
        # Matched: 1 (Python meets Level 4)
        # Missing/Gaps: 1 (SQL requires 3, student has 0 -> Gap = 3)
        self.assertEqual(analysis['total_count'], 2)
        self.assertEqual(analysis['matched_count'], 1)
        self.assertEqual(analysis['gap_count'], 1)
        self.assertEqual(analysis['match_percentage'], 50)

    # 4. Training & Longitudinal Re-Assessment Tests
    def test_training_enrollment_and_improvement_delta(self):
        enrollment = TrainingEnrollment.objects.create(
            user=self.student,
            course=self.course,
            status='in_progress',
            progress_percent=20,
            score_before=45.0
        )
        self.assertEqual(enrollment.score_before, 45.0)
        self.assertIsNone(enrollment.improvement_delta)

        # Complete course & record post-training score
        enrollment.status = 'completed'
        enrollment.progress_percent = 100
        enrollment.score_after = 75.0
        enrollment.save()

        # Delta should be +30.0 points
        self.assertEqual(enrollment.improvement_delta, 30.0)

    # 5. Employment Tracker Tests
    def test_employment_tracking(self):
        record, _ = EmploymentRecord.objects.get_or_create(user=self.student)
        record.status = 'employed'
        record.company_name = 'Enterprise Tech'
        record.job_role = 'Junior Developer'
        record.salary_range = '₹6 - ₹8 LPA'
        record.save()

        self.assertEqual(record.status, 'employed')
        self.assertEqual(record.company_name, 'Enterprise Tech')

    # 6. Authorization & RBAC Route Protection Tests
    def test_student_cannot_access_admin_dashboard(self):
        self.client.login(username='test_student', password='password123')
        response = self.client.get(reverse('admin_dashboard'))
        # Should redirect student to user dashboard
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('user_dashboard'), response.url)

    def test_admin_can_access_admin_dashboard(self):
        self.client.login(username='test_admin', password='password123')
        response = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(response.status_code, 200)

from django.core.management.base import BaseCommand
from django.utils import timezone
from accounts.models import User, Profile
from skills.models import Skill, UserSkill, Certificate
from assessments.models import Question, AssessmentAttempt, AttemptAnswer, PracticalTask, PracticalSubmission
from projects.models import ProjectSubmission
from jobs.models import Job, JobRequirement
from training.models import TrainingCourse, TrainingEnrollment, TrainingProvider, TrainingCentre, Cohort, District
from employment.models import (
    EmploymentRecord,
    LongitudinalMilestone,
    NonPlacementReason,
    FollowUpLog,
    EmployerVerificationRequest,
)

class Command(BaseCommand):
    help = 'Seeds initial demonstration data for SkillBridge (Skills, MCQs, Practicals, Jobs, Training, Users)'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Seeding SkillBridge demonstration data..."))

        # 1. Seed Skills (Section 25)
        skills_data = [
            ('Python', 'tech', 'High-level programming language for web, data analysis, and automation.', 'fa-brands fa-python'),
            ('SQL', 'data', 'Standard language for storing, manipulating and retrieving data in relational databases.', 'fa-solid fa-database'),
            ('HTML/CSS', 'tech', 'Fundamental building blocks for structuring and styling modern web interfaces.', 'fa-brands fa-html5'),
            ('JavaScript', 'tech', 'Versatile language powering dynamic frontend experiences and server logic.', 'fa-brands fa-js'),
            ('Excel', 'data', 'Spreadsheet application for financial modeling, data cleanup, and pivoting.', 'fa-solid fa-file-excel'),
            ('Power BI', 'data', 'Business analytics service for interactive visualizations and BI dashboards.', 'fa-solid fa-chart-pie'),
            ('Communication', 'soft', 'Verbal and written professional communication and cross-functional leadership.', 'fa-solid fa-comments'),
            ('REST APIs', 'tech', 'Architectural style for network-based hypermedia systems and microservices.', 'fa-solid fa-network-wired'),
            ('Git', 'tools', 'Distributed version control system for tracking changes in source code.', 'fa-brands fa-git-alt'),
            ('Statistics', 'data', 'Mathematical science concerning data collection, analysis, interpretation, and presentation.', 'fa-solid fa-calculator'),
        ]

        skills = {}
        for name, cat, desc, icon in skills_data:
            skill_obj, _ = Skill.objects.get_or_create(
                name=name,
                defaults={'category': cat, 'description': desc, 'icon_class': icon}
            )
            skills[name] = skill_obj

        self.stdout.write(self.style.SUCCESS(f"Seeded {len(skills)} primary skills."))

        # 2. Seed 20 MCQs for Python (Section 27)
        py_questions = [
            ("What is the output of print(type([])) in Python?", "easy", "<class 'tuple'>", "<class 'list'>", "<class 'set'>", "<class 'dict'>", "b", "In Python, square brackets define a list object."),
            ("Which of the following functions converts a string to an integer in Python?", "easy", "str()", "float()", "int()", "parse()", "c", "int() converts eligible numbers and strings into integer objects."),
            ("How do you start a comment in Python?", "easy", "//", "/*", "#", "<!--", "c", "Python uses the hash symbol # for single-line comments."),
            ("Which keyword is used to create a function in Python?", "easy", "function", "def", "fun", "define", "b", "The def keyword declares a function definition in Python."),
            ("What is the correct syntax to output 'Hello World' in Python?", "easy", "echo 'Hello World'", "p('Hello World')", "print('Hello World')", "Console.WriteLine('Hello World')", "c", "print() is the built-in output function."),
            ("Which data type is immutable in Python?", "medium", "List", "Dictionary", "Tuple", "Set", "c", "Tuples cannot be modified after initial creation, making them immutable."),
            ("What does the 'is' operator test for in Python?", "medium", "Value equality", "Object identity in memory", "Type equality", "Subclass relationship", "b", "'is' checks whether two variables point to the exact same memory location."),
            ("What will list(range(1, 5)) produce?", "medium", "[1, 2, 3, 4, 5]", "[1, 2, 3, 4]", "[0, 1, 2, 3, 4]", "[1, 3, 5]", "b", "range(start, stop) generates numbers up to but excluding the stop value."),
            ("How do you handle exceptions in Python?", "medium", "try...catch", "do...except", "try...except", "attempt...handle", "c", "Python uses try/except/finally blocks to handle runtime exceptions."),
            ("What is the result of 3 * [1, 2]?", "medium", "[3, 6]", "[1, 2, 1, 2, 1, 2]", "Error", "[[1, 2], [1, 2], [1, 2]]", "b", "Multiplying a sequence by an integer repeats its elements."),
            ("Which method removes and returns the last element from a list?", "medium", "remove()", "pop()", "discard()", "delete()", "b", "pop() without arguments removes and returns the last item in a list."),
            ("What is a Python decorator?", "hard", "A class attribute", "A function that takes another function and extends its behavior without modifying it", "A compiler directive", "A GUI widget", "b", "Decorators wrap another function to augment its execution dynamically."),
            ("What is the purpose of __init__ in Python classes?", "medium", "To allocate memory", "Constructor initializer method called when an instance is created", "To import libraries", "To delete the object", "b", "__init__ initializes attributes of newly instantiated class objects."),
            ("What is the time complexity of dictionary key lookups on average?", "hard", "O(n)", "O(log n)", "O(1)", "O(n^2)", "c", "Python dictionaries utilize optimized hash tables giving average O(1) time complexity."),
            ("What does the Global Interpreter Lock (GIL) in CPython do?", "hard", "Prevents memory leaks", "Allows only one thread to execute Python bytecode at a time", "Enforces strict type checks", "Compiles code to C", "b", "GIL restricts multi-threaded CPython execution to one native thread at a time."),
            ("Which module in Python is used for regular expressions?", "easy", "regex_lib", "re", "pyregex", "string", "b", "The standard library module 're' provides regular expression operations."),
            ("What does *args indicate in a function parameter list?", "medium", "Keyword arguments", "Variable number of non-keyword positional arguments", "Pointer reference", "Multiplication factor", "b", "*args captures surplus positional parameters into a tuple."),
            ("What will bool('False') evaluate to in Python?", "hard", "False", "True", "None", "ValueError", "b", "Non-empty strings evaluate to True in boolean contexts, regardless of contents."),
            ("What is a generator function in Python?", "hard", "A function that returns a list", "A function that produces a sequence using yield without loading all items in memory", "A function generating random numbers", "An async callback", "b", "Generators use yield to lazily produce values one at a time via iterator protocol."),
            ("Which builtin function returns both index and item while iterating?", "medium", "zip()", "map()", "enumerate()", "counter()", "c", "enumerate() yields tuples containing (index, item) during sequence iteration."),
        ]

        for text, diff, a, b, c, d, correct, expl in py_questions:
            Question.objects.get_or_create(
                skill=skills['Python'],
                text=text,
                defaults={'difficulty': diff, 'option_a': a, 'option_b': b, 'option_c': c, 'option_d': d, 'correct_option': correct, 'explanation': expl}
            )

        # 3. Seed 20 MCQs for SQL (Section 27)
        sql_questions = [
            ("Which SQL clause is used to extract only those records that fulfill a specified condition?", "easy", "SELECT", "WHERE", "FROM", "GROUP BY", "b", "The WHERE clause filters rows based on conditional boolean logic."),
            ("Which SQL command is used to fetch data from a database table?", "easy", "GET", "FETCH", "SELECT", "EXTRACT", "c", "SELECT retrieves data rows and columns from relational tables."),
            ("Which SQL statement is used to insert new records into a table?", "easy", "ADD RECORD", "INSERT INTO", "PUT INTO", "INSERT ROW", "b", "INSERT INTO is the standard ANSI SQL command to append rows."),
            ("Which constraint uniquely identifies each record in a database table?", "easy", "FOREIGN KEY", "UNIQUE", "PRIMARY KEY", "CHECK", "c", "A PRIMARY KEY constraint uniquely identifies each record and prohibits nulls."),
            ("How do you select distinct values from a column named 'City'?", "easy", "SELECT DIFFERENT City FROM Customers", "SELECT DISTINCT City FROM Customers", "SELECT UNIQUE City FROM Customers", "SELECT City FROM Customers WITHOUT DUPLICATES", "b", "SELECT DISTINCT filters out duplicate values in the result set."),
            ("Which keyword sorts the result set in ascending order by default?", "easy", "SORT BY", "ORDER BY", "ARRANGE BY", "GROUP BY", "b", "ORDER BY sorts the returned records (defaults to ASC)."),
            ("What is the difference between WHERE and HAVING in SQL?", "medium", "WHERE filters groups, HAVING filters rows", "WHERE filters rows before aggregation, HAVING filters groups after aggregation", "They are completely interchangeable", "HAVING only works with PRIMARY KEY", "b", "WHERE evaluates row-by-row before GROUP BY; HAVING evaluates aggregated group metrics."),
            ("Which JOIN returns all rows from the left table, and matching rows from the right table?", "medium", "INNER JOIN", "RIGHT JOIN", "LEFT JOIN", "FULL OUTER JOIN", "c", "LEFT JOIN retains every record from the left table even if right table matches are null."),
            ("What does the COUNT(*) function return?", "medium", "Total sum of numeric columns", "Number of rows matching the query criteria", "Average count of non-null values", "Table column count", "b", "COUNT(*) counts total matched rows regardless of nulls."),
            ("Which operator is used to search for a specified pattern in a column?", "medium", "MATCH", "LIKE", "CONTAINS", "IN", "b", "LIKE is used with wildcards like % and _ to match character patterns."),
            ("Which SQL function calculates the arithmetic mean of a column?", "medium", "MEAN()", "AVG()", "TOTAL()", "SUM()", "b", "AVG() computes the mathematical average of a numeric column."),
            ("What does ACID stand for in database management systems?", "hard", "Access, Control, Index, Data", "Atomicity, Consistency, Isolation, Durability", "Action, Commit, Instance, Distributed", "Auto, Concurrent, Indexed, Durable", "b", "ACID guarantees transactional validity despite errors, power failures, and concurrent queries."),
            ("What is the purpose of database indexing?", "hard", "To enforce foreign key cascades", "To optimize search and query retrieval performance at the cost of write overhead", "To encrypt table columns", "To format output text", "b", "B-tree and hash indexes dramatically speed up SELECT filtering at the cost of index storage."),
            ("What will happen if a transaction performs a ROLLBACK command?", "medium", "All committed changes are published", "All modifications made during the transaction are undone", "The table schema is deleted", "The database restarts", "b", "ROLLBACK reverts the database to its state before the transaction began."),
            ("Which normal form eliminates transitive dependencies?", "hard", "First Normal Form (1NF)", "Second Normal Form (2NF)", "Third Normal Form (3NF)", "Boyce-Codd Normal Form (BCNF)", "c", "3NF requires that every non-key column depends solely and non-transitively on the primary key."),
            ("What is a subquery in SQL?", "medium", "A query executed in a separate thread", "A query nested inside another SQL statement", "A stored procedure", "An index lookup", "b", "A subquery (or inner query) is nested within a SELECT, INSERT, UPDATE, or DELETE."),
            ("What does COALESCE(col1, col2, 'default') do?", "hard", "Concatenates strings", "Returns the first non-null expression from the list", "Counts non-nulls", "Creates a computed column", "b", "COALESCE evaluates arguments sequentially and returns the first non-null value."),
            ("Which SQL command deletes all rows from a table without logging individual row deletions?", "hard", "DELETE FROM table", "DROP TABLE table", "TRUNCATE TABLE table", "REMOVE TABLE table", "c", "TRUNCATE deallocates data pages directly, making it faster than row-by-row DELETE."),
            ("What is a VIEW in SQL?", "medium", "A physical copy of table data", "A virtual table based on the result-set of an SQL statement", "A database backup file", "A graphical UI diagram", "b", "A VIEW is a stored query that can be queried exactly like a physical table."),
            ("Which window function assigns a rank to each row within a partition without gaps in ranking values?", "hard", "RANK()", "DENSE_RANK()", "ROW_NUMBER()", "NTILE()", "b", "DENSE_RANK() leaves no gaps in ranking sequences when duplicate values occur."),
        ]

        for text, diff, a, b, c, d, correct, expl in sql_questions:
            Question.objects.get_or_create(
                skill=skills['SQL'],
                text=text,
                defaults={'difficulty': diff, 'option_a': a, 'option_b': b, 'option_c': c, 'option_d': d, 'correct_option': correct, 'explanation': expl}
            )

        self.stdout.write(self.style.SUCCESS("Seeded 40 comprehensive MCQs for Python and SQL."))
        from django.core.management import call_command
        call_command('seed_all_questions')

        # 4. Seed Practical Tasks (Section 29)
        PracticalTask.objects.get_or_create(
            skill=skills['Python'],
            title='Find the Largest Element in a List',
            defaults={
                'difficulty': 'easy',
                'description': 'Write a Python function find_largest(numbers) that returns the maximum value in an integer list.',
                'requirements': '1. Function must be named find_largest(numbers)\n2. Must handle negative numbers correctly\n3. Must return None if list is empty\n4. Do not use external third-party libraries',
                'starter_code': 'def find_largest(numbers):\n    # Write your solution below\n    if not numbers:\n        return None\n    max_val = numbers[0]\n    for n in numbers:\n        if n > max_val:\n            max_val = n\n    return max_val\n',
                'test_cases_count': 5,
            }
        )

        PracticalTask.objects.get_or_create(
            skill=skills['SQL'],
            title='Aggregate Department Salary Above Threshold',
            defaults={
                'difficulty': 'medium',
                'description': 'Construct a query to compute the average salary per department for departments having more than 5 employees.',
                'requirements': '1. Use SELECT department_id, AVG(salary) FROM employees\n2. Group by department_id\n3. Filter using HAVING COUNT(*) > 5\n4. Order by average salary descending',
                'starter_code': 'SELECT department_id, AVG(salary) AS avg_sal\nFROM employees\nGROUP BY department_id\nHAVING COUNT(*) > 5\nORDER BY avg_sal DESC;\n',
                'test_cases_count': 5,
            }
        )

        # 5. Seed Jobs & Requirements (Section 35)
        jobs_data = [
            ('Data Analyst', 'data-analyst', 'Technology & BI', 'Entry / Associate', 'Analyze business datasets, build dashboards, and extract actionable insights.', '₹6,00,000 - ₹9,50,000 PA', [
                ('Python', 4),
                ('SQL', 3),
                ('Excel', 4),
                ('Power BI', 3),
                ('Statistics', 3),
            ]),
            ('Web Developer', 'web-developer', 'Frontend Engineering', 'Associate / Mid', 'Build responsive, accessible, dynamic frontend web applications.', '₹7,00,000 - ₹11,00,000 PA', [
                ('HTML/CSS', 4),
                ('JavaScript', 4),
                ('Git', 3),
                ('SQL', 2),
            ]),
            ('Backend Developer', 'backend-developer', 'Platform Engineering', 'Associate / Mid', 'Design scalable server-side systems, relational databases, and REST APIs.', '₹8,00,000 - ₹13,00,000 PA', [
                ('Python', 4),
                ('SQL', 3),
                ('REST APIs', 3),
                ('Git', 3),
            ]),
        ]

        for title, slug, dept, exp, desc, salary, reqs in jobs_data:
            job_obj, _ = Job.objects.get_or_create(
                slug=slug,
                defaults={'title': title, 'department': dept, 'experience_level': exp, 'description': desc, 'salary_range': salary}
            )
            for s_name, level_req in reqs:
                if s_name in skills:
                    JobRequirement.objects.get_or_create(
                        job=job_obj,
                        skill=skills[s_name],
                        defaults={'required_level': level_req, 'is_mandatory': True}
                    )

        self.stdout.write(self.style.SUCCESS("Seeded 3 industry jobs with level requirements."))

        # 6. Seed Training Courses (Section 40)
        training_data = [
            ('Intermediate SQL Mastery', 'SQL', 3, 'Comprehensive relational query construction, subqueries, grouping, and indexing.', 'SkillBridge Academy', '4 Weeks (16 Hours)'),
            ('Python Advanced Programming', 'Python', 4, 'Decorators, generators, object-oriented architecture, and performance optimization.', 'SkillBridge Academy', '6 Weeks (24 Hours)'),
            ('Power BI Fundamentals for Analysts', 'Power BI', 3, 'Data modeling, DAX expressions, interactive report authoring, and workspace publishing.', 'SkillBridge Data Lab', '3 Weeks (12 Hours)'),
            ('Modern JavaScript ES6+ Deep Dive', 'JavaScript', 4, 'Asynchronous promises, closures, DOM manipulation, and modular architecture.', 'SkillBridge Academy', '4 Weeks (20 Hours)'),
        ]

        courses = {}
        for c_name, s_name, lvl, desc, prov, dur in training_data:
            course_obj, _ = TrainingCourse.objects.get_or_create(
                name=c_name,
                defaults={'skill': skills[s_name], 'target_level': lvl, 'description': desc, 'provider': prov, 'duration': dur}
            )
            courses[c_name] = course_obj

        self.stdout.write(self.style.SUCCESS("Seeded 4 training courses."))

        # 6.5. Seed National Skilling Hierarchy (Districts, Providers, Centres, Cohorts)
        districts_data = [
            ('Ranchi', 'Jharkhand', True),
            ('Nuh', 'Haryana', True),
            ('Khurda', 'Odisha', True),
            ('Dharmapuri', 'Tamil Nadu', True),
            ('Varanasi', 'Uttar Pradesh', False),
            ('Bengaluru Urban', 'Karnataka', False),
        ]
        districts = {}
        for d_name, d_state, is_asp in districts_data:
            d_obj, _ = District.objects.get_or_create(
                name=d_name, state=d_state,
                defaults={'is_aspirational': is_asp}
            )
            districts[d_name] = d_obj

        # Training Providers (NSDC Accredited)
        tp_apex, _ = TrainingProvider.objects.get_or_create(
            nsdc_partner_code='TP-NSDC-2024-089',
            defaults={
                'name': 'Apex SkillTech Academy',
                'accreditation_grade': 'A+',
                'contact_person': 'Dr. K. Sharma',
                'contact_email': 'contact@apexskilltech.org',
                'contact_phone': '+91 9811223344',
            }
        )
        tp_gramin, _ = TrainingProvider.objects.get_or_create(
            nsdc_partner_code='TP-NSDC-2024-041',
            defaults={
                'name': 'Gramin Vocational Vikas Mission',
                'accreditation_grade': 'A',
                'contact_person': 'Sunita Soren',
                'contact_email': 'info@graminvikas.org',
                'contact_phone': '+91 9822334455',
            }
        )
        tp_national, _ = TrainingProvider.objects.get_or_create(
            nsdc_partner_code='TP-NSDC-2024-112',
            defaults={
                'name': 'National Technical Training Hub',
                'accreditation_grade': 'B',
                'contact_person': 'Anand Verma',
                'contact_email': 'reach@nationalhub.in',
                'contact_phone': '+91 9833445566',
            }
        )

        # Training Centres
        tc_ranchi, _ = TrainingCentre.objects.get_or_create(
            center_code='TC-RNC-01',
            defaults={
                'provider': tp_gramin,
                'district': districts['Ranchi'],
                'center_name': 'Gramin Skill Centre, Ranchi Main',
                'address': 'Circular Road, Lalpur, Ranchi, Jharkhand',
            }
        )
        tc_bengaluru, _ = TrainingCentre.objects.get_or_create(
            center_code='TC-BLR-02',
            defaults={
                'provider': tp_apex,
                'district': districts['Bengaluru Urban'],
                'center_name': 'Apex Digital Tech Centre, Bengaluru',
                'address': 'Electronic City Phase 1, Bengaluru, Karnataka',
            }
        )
        tc_nuh, _ = TrainingCentre.objects.get_or_create(
            center_code='TC-NUH-03',
            defaults={
                'provider': tp_national,
                'district': districts['Nuh'],
                'center_name': 'Mewat Vocational Skill Centre, Nuh',
                'address': 'Sohna-Alwar Highway, Nuh, Haryana',
            }
        )

        # Cohorts
        cohort_pmkvy, _ = Cohort.objects.get_or_create(
            batch_code='PMKVY4-WD-2025-01',
            defaults={
                'scheme_name': 'pmkvy4',
                'training_centre': tc_ranchi,
                'course': courses['Python Advanced Programming'],
            }
        )
        cohort_naps, _ = Cohort.objects.get_or_create(
            batch_code='NAPS-DA-2025-02',
            defaults={
                'scheme_name': 'naps',
                'training_centre': tc_bengaluru,
                'course': courses['Intermediate SQL Mastery'],
            }
        )
        cohort_vishwakarma, _ = Cohort.objects.get_or_create(
            batch_code='VISWAKARMA-2025-03',
            defaults={
                'scheme_name': 'vishwakarma',
                'training_centre': tc_nuh,
                'course': courses['Power BI Fundamentals for Analysts'],
            }
        )

        self.stdout.write(self.style.SUCCESS("Seeded National Hierarchy (Districts, Providers, Centres, Cohorts)."))

        # 7. Seed Demo Users & Longitudinal Outcomes (Section 59)
        # Admin User
        admin_user, _ = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@skillbridge.edu',
                'first_name': 'System',
                'last_name': 'Administrator',
                'role': 'admin',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        admin_user.set_password('adminpassword123')
        admin_user.save()

        # Candidate 1: Alex (Active Student)
        alex, _ = User.objects.get_or_create(
            username='alex_candidate',
            defaults={
                'email': 'alex@example.com',
                'first_name': 'Alex',
                'last_name': 'Sharma',
                'role': 'user',
                'phone': '+91 9876543210',
                'alt_phone': '+91 9876543219',
                'guardian_phone': '+91 9876543218',
                'trainee_id': 'SIDH-2026-JH-8832',
                'gender': 'male',
                'category': 'general',
                'area_type': 'semi_urban',
                'consent_given': True,
            }
        )
        alex.set_password('candidatepass123')
        alex.save()
        alex.profile.degree = 'B.Tech Computer Science'
        alex.profile.institution = 'National Institute of Technology'
        alex.profile.graduation_year = 2026
        alex.profile.target_role = 'Data Analyst'
        alex.profile.headline = 'Passionate data analyst building skills in Python, SQL, and Power BI'
        alex.profile.save()

        # Skills for Alex: Python (Verified 82%), SQL (Claimed 2, Verified 50%), Excel (Claimed 4)
        us_py, _ = UserSkill.objects.get_or_create(
            user=alex, skill=skills['Python'],
            defaults={'claimed_level': 4, 'mcq_score': 85.0, 'practical_score': 80.0, 'project_score': 80.0}
        )
        us_py.recalculate_score()

        us_sql, _ = UserSkill.objects.get_or_create(
            user=alex, skill=skills['SQL'],
            defaults={'claimed_level': 2, 'mcq_score': 50.0, 'practical_score': 50.0, 'project_score': 0.0}
        )
        us_sql.recalculate_score()

        us_excel, _ = UserSkill.objects.get_or_create(
            user=alex, skill=skills['Excel'],
            defaults={'claimed_level': 4, 'is_verified': False}
        )

        # Assessment Attempt for Alex
        if not AssessmentAttempt.objects.filter(user=alex, skill=skills['Python']).exists():
            AssessmentAttempt.objects.create(
                user=alex, skill=skills['Python'],
                total_questions=10, correct_answers=8, score_percent=80.0, is_completed=True, completed_at=timezone.now()
            )

        # Training Enrollment for Alex
        TrainingEnrollment.objects.get_or_create(
            user=alex, course=courses['Intermediate SQL Mastery'],
            defaults={'status': 'in_progress', 'progress_percent': 65, 'score_before': 50.0, 'cohort': cohort_naps, 'district': districts['Ranchi']}
        )

        # Project for Alex
        ProjectSubmission.objects.get_or_create(
            user=alex, skill=skills['Python'],
            title='Autonomous Data Cleaning Tool',
            defaults={
                'description': 'Python tool to clean and validate large CSV datasets with automated anomaly reporting.',
                'technologies': 'Python, Pandas, SQLite',
                'github_url': 'https://github.com/alex-sharma/data-cleaner',
                'status': 'approved',
                'score': 85.0,
                'admin_feedback': 'Clean architecture, thorough unit tests, and modular code.',
                'reviewed_by': admin_user,
                'reviewed_at': timezone.now()
            }
        )

        # Candidate 2: Priya (Employed Candidate demonstrating Longitudinal Skilling & Wage Progression)
        priya, _ = User.objects.get_or_create(
            username='priya_analyst',
            defaults={
                'email': 'priya@example.com',
                'first_name': 'Priya',
                'last_name': 'Nair',
                'role': 'user',
                'phone': '+91 9844001122',
                'alt_phone': '+91 9844001123',
                'guardian_phone': '+91 9844001124',
                'trainee_id': 'SIDH-2026-KA-4412',
                'gender': 'female',
                'category': 'obc',
                'area_type': 'rural',
                'consent_given': True,
            }
        )
        priya.set_password('candidatepass123')
        priya.save()
        priya.profile.degree = 'B.Sc Data Science'
        priya.profile.institution = 'Apex University'
        priya.profile.graduation_year = 2025
        priya.profile.target_role = 'Data Analyst'
        priya.profile.save()

        # Priya before vs after training
        us_priya_sql, _ = UserSkill.objects.get_or_create(
            user=priya, skill=skills['SQL'],
            defaults={'claimed_level': 4, 'mcq_score': 88.0, 'practical_score': 90.0, 'project_score': 85.0}
        )
        us_priya_sql.recalculate_score()

        TrainingEnrollment.objects.get_or_create(
            user=priya, course=courses['Intermediate SQL Mastery'],
            defaults={
                'status': 'completed',
                'progress_percent': 100,
                'score_before': 48.0,
                'score_after': 88.0, # +40 points improvement delta!
                'cohort': cohort_naps,
                'district': districts['Bengaluru Urban'],
                'completed_at': timezone.now()
            }
        )

        # Employment Record for Priya
        EmploymentRecord.objects.update_or_create(
            user=priya,
            defaults={
                'status': 'employed',
                'company_name': 'TechCorp Analytics Ltd.',
                'job_role': 'Associate Data Analyst',
                'salary_range': '₹6 - ₹8 LPA',
                'current_monthly_wage': 28000,
                'location': 'Bangalore, India',
                'employment_type': 'full_time',
                'skills_used': 'SQL, Python, Power BI',
                'training_relevance': 'high',
                'is_verified_by_admin': True,
                'epfo_uan': 'EPFO-10192837465',
                'employer_gstin': '29ABCDE1234F1Z5',
                'last_milestone_month': 12,
            }
        )

        # Longitudinal Milestones for Priya (Demonstrating ₹18k -> ₹20k -> ₹24k -> ₹28k Wage Progression!)
        priya_milestones = [
            (0, 'employed', 'TechCorp Analytics Ltd.', 'Junior Trainee Analyst', 18000, True, False, 'employer_confirmed', 'Initial exit placement'),
            (3, 'employed', 'TechCorp Analytics Ltd.', 'Junior Data Analyst', 20000, True, True, 'employer_confirmed', 'Completed 3-month probation with wage hike'),
            (6, 'employed', 'TechCorp Analytics Ltd.', 'Data Analyst', 24000, True, True, 'assisted_call', '6-Month retention audit validated by Rozgar Sahayak'),
            (12, 'employed', 'TechCorp Analytics Ltd.', 'Associate Data Analyst', 28000, True, True, 'epfo_signal', '1-Year sustained formal livelihood validated via EPFO signal'),
        ]
        for m_month, m_status, m_comp, m_role, m_wage, m_ret, m_inc, m_src, m_notes in priya_milestones:
            LongitudinalMilestone.objects.update_or_create(
                user=priya,
                milestone_month=m_month,
                defaults={
                    'status': m_status,
                    'company_name': m_comp,
                    'job_role': m_role,
                    'monthly_wage': m_wage,
                    'is_retained': m_ret,
                    'is_wage_increased': m_inc,
                    'training_relevance': 'high',
                    'verification_source': m_src,
                    'check_in_date': timezone.now().date(),
                    'notes': m_notes,
                }
            )

        # Candidate 3: Rahul (Ranchi Aspirational District Candidate - Formally Employed)
        rahul, _ = User.objects.get_or_create(
            username='rahul_trainee',
            defaults={
                'email': 'rahul@example.com',
                'first_name': 'Rahul',
                'last_name': 'Karmakar',
                'role': 'user',
                'phone': '+91 9771122334',
                'alt_phone': '+91 9771122335',
                'guardian_phone': '+91 9771122336',
                'trainee_id': 'SIDH-2026-JH-1902',
                'gender': 'male',
                'category': 'st',
                'area_type': 'rural',
                'consent_given': True,
            }
        )
        rahul.set_password('candidatepass123')
        rahul.save()
        EmploymentRecord.objects.update_or_create(
            user=rahul,
            defaults={
                'status': 'employed',
                'company_name': 'Jharkhand Tech Solutions',
                'job_role': 'Frontend Web Technician',
                'current_monthly_wage': 17500,
                'training_relevance': 'high',
                'is_verified_by_admin': True,
                'employer_gstin': '20AAAAA0000A1Z5',
                'last_milestone_month': 3,
            }
        )
        LongitudinalMilestone.objects.update_or_create(
            user=rahul, milestone_month=0,
            defaults={'status': 'employed', 'company_name': 'Jharkhand Tech Solutions', 'job_role': 'Frontend Intern', 'monthly_wage': 14000, 'is_retained': True, 'training_relevance': 'high', 'verification_source': 'employer_confirmed', 'check_in_date': timezone.now().date()}
        )
        LongitudinalMilestone.objects.update_or_create(
            user=rahul, milestone_month=3,
            defaults={'status': 'employed', 'company_name': 'Jharkhand Tech Solutions', 'job_role': 'Frontend Web Technician', 'monthly_wage': 17500, 'is_retained': True, 'is_wage_increased': True, 'training_relevance': 'high', 'verification_source': 'self_reported', 'check_in_date': timezone.now().date()}
        )

        # Candidate 4: Anjali (Nuh Aspirational District - NAPS Apprenticeship)
        anjali, _ = User.objects.get_or_create(
            username='anjali_apprentice',
            defaults={
                'email': 'anjali@example.com',
                'first_name': 'Anjali',
                'last_name': 'Kumari',
                'role': 'user',
                'phone': '+91 9650011223',
                'alt_phone': '+91 9650011224',
                'guardian_phone': '+91 9650011225',
                'trainee_id': 'SIDH-2026-HR-3184',
                'gender': 'female',
                'category': 'sc',
                'area_type': 'rural',
                'consent_given': True,
            }
        )
        anjali.set_password('candidatepass123')
        anjali.save()
        EmploymentRecord.objects.update_or_create(
            user=anjali,
            defaults={
                'status': 'internship',
                'company_name': 'Maruti Vendor Logistics (NAPS)',
                'job_role': 'Quality Apprentice Technician',
                'current_monthly_wage': 13500,
                'training_relevance': 'high',
                'is_verified_by_admin': True,
                'last_milestone_month': 0,
            }
        )
        LongitudinalMilestone.objects.update_or_create(
            user=anjali, milestone_month=0,
            defaults={'status': 'internship', 'company_name': 'Maruti Vendor Logistics (NAPS)', 'job_role': 'Quality Apprentice Technician', 'monthly_wage': 13500, 'is_retained': True, 'training_relevance': 'high', 'verification_source': 'employer_confirmed', 'check_in_date': timezone.now().date()}
        )

        # Candidate 5: Deepak (Khurda District - Relocation Attrition Diagnostic Case)
        deepak, _ = User.objects.get_or_create(
            username='deepak_candidate',
            defaults={
                'email': 'deepak@example.com',
                'first_name': 'Deepak',
                'last_name': 'Patra',
                'role': 'user',
                'phone': '+91 9437011223',
                'alt_phone': '+91 9437011224',
                'guardian_phone': '+91 9437011225',
                'trainee_id': 'SIDH-2026-OD-5591',
                'gender': 'male',
                'category': 'general',
                'area_type': 'rural',
                'consent_given': True,
            }
        )
        deepak.set_password('candidatepass123')
        deepak.save()
        EmploymentRecord.objects.update_or_create(
            user=deepak,
            defaults={'status': 'dropped_out', 'current_monthly_wage': None}
        )
        NonPlacementReason.objects.get_or_create(
            user=deepak,
            defaults={
                'category': 'relocation_refusal',
                'details': 'Candidate was offered a position in Bengaluru (₹16k/mo), but could not relocate due to aging dependent parents in Khurda.',
                'recommended_action': 'Map to Bhubaneswar-Cuttack IT MSME cluster apprenticeship or local BPO tele-work.',
            }
        )

        # 8. Seed Employer Verification Requests
        EmployerVerificationRequest.objects.get_or_create(
            user=priya,
            company_name='TechCorp Analytics Ltd.',
            defaults={
                'employer_contact_name': 'Amitabha Sen (VP HR)',
                'employer_email': 'hr@techcorpanalytics.com',
                'status': 'confirmed',
                'confirmed_role': 'Associate Data Analyst',
                'confirmed_monthly_wage': 28000,
                'confirmed_joining_date': timezone.now().date(),
                'gstin': '29ABCDE1234F1Z5',
                'has_epfo_coverage': True,
                'feedback_on_trainee': 'Priya demonstrates outstanding SQL mastery and rapid problem-solving capability.',
                'responded_at': timezone.now(),
            }
        )
        EmployerVerificationRequest.objects.get_or_create(
            user=alex,
            company_name='Apex Data Systems Pvt Ltd',
            defaults={
                'employer_contact_name': 'Rohit Gupta (Talent Acquisition)',
                'employer_email': 'talent@apexdata.com',
                'status': 'pending',
            }
        )

        # 9. Seed Multi-Channel Follow-up & Contact Traceability Logs
        FollowUpLog.objects.get_or_create(
            user=priya,
            channel='whatsapp_bot',
            defaults={
                'contact_number_used': '+91 9844001122',
                'contact_type': 'primary',
                'status': 'responded',
                'response_text': 'Confirmed: Month 12 retention at TechCorp, Monthly wage ₹28,000, Training high relevance.',
            }
        )
        FollowUpLog.objects.get_or_create(
            user=rahul,
            channel='whatsapp_bot',
            defaults={
                'contact_number_used': '+91 9771122334',
                'contact_type': 'primary',
                'status': 'responded',
                'response_text': 'Confirmed: Employed in Ranchi, Monthly wage ₹17,500.',
            }
        )
        FollowUpLog.objects.get_or_create(
            user=deepak,
            channel='whatsapp_bot',
            defaults={
                'contact_number_used': '+91 9437011223',
                'contact_type': 'primary',
                'status': 'wrong_number',
                'response_text': 'Delivery failed: SIM inactive. Automatically escalated to village/guardian phone +91 9437011225.',
            }
        )
        FollowUpLog.objects.get_or_create(
            user=deepak,
            channel='assisted_call',
            defaults={
                'contact_number_used': '+91 9437011225',
                'contact_type': 'guardian',
                'status': 'responded',
                'response_text': 'Rozgar Sahayak connected with father. Trainee is seeking local MSME work in Khurda.',
            }
        )

        self.stdout.write(self.style.SUCCESS("Seeded sample users, longitudinal before/after impact records, wage progression, and employment verification."))
        self.stdout.write(self.style.SUCCESS("Demo seeding completed successfully!"))

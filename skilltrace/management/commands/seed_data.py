import os
import random
import uuid
import hashlib
from datetime import date, timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from skilltrace.models import (
    State, District, Scheme, Course, Provider, Person, PersonPII,
    ContactPoint, SchemeCrosswalk, ConsentArtefact, Employer,
    OutcomeEpisode, EvidenceItem, VerificationRequest, FollowUpTask,
    SurveyResponse, IdentityMatchQueue, ActionCase, AuditEvent
)


class Command(BaseCommand):
    help = 'Seeds realistic national longitudinal skilling outcome data for SkillTrace India'

    def handle(self, *args, **options):
        self.stdout.write("Initializing National LGD Masters and Skilling Registry Data...")

        # 1. STATES (LGD Codes & Minimum Wages)
        states_data = [
            ("27", "Maharashtra", 15500),
            ("29", "Karnataka", 14800),
            ("09", "Uttar Pradesh", 12500),
            ("33", "Tamil Nadu", 14200),
            ("07", "Delhi (NCT)", 17500),
            ("08", "Rajasthan", 13200),
            ("36", "Telangana", 14000),
            ("10", "Bihar", 11800),
            ("24", "Gujarat", 14500),
            ("19", "West Bengal", 12900),
            ("03", "Punjab", 13800),
            ("18", "Assam", 12200),
        ]
        states_dict = {}
        for code, name, wage in states_data:
            s, _ = State.objects.get_or_create(code=code, defaults={"name": name, "min_wage_monthly": wage})
            states_dict[code] = s

        # 2. DISTRICTS
        districts_data = [
            ("519", "27", "Pune", 0.88),
            ("518", "27", "Mumbai Suburban", 0.92),
            ("515", "27", "Nagpur", 0.74),
            ("521", "27", "Nashik", 0.76),
            ("572", "29", "Bengaluru Urban", 0.94),
            ("577", "29", "Mysuru", 0.81),
            ("555", "29", "Dharwad", 0.75),
            ("138", "09", "Lucknow", 0.79),
            ("157", "09", "Varanasi", 0.69),
            ("178", "09", "Kanpur Nagar", 0.77),
            ("603", "33", "Chennai", 0.91),
            ("604", "33", "Coimbatore", 0.86),
            ("093", "07", "New Delhi", 0.95),
            ("115", "08", "Jaipur", 0.82),
            ("532", "36", "Hyderabad", 0.93),
            ("230", "10", "Patna", 0.70),
            ("474", "24", "Ahmedabad", 0.89),
            ("342", "19", "Kolkata", 0.87),
        ]
        districts_dict = {}
        for code, state_code, name, lmi in districts_data:
            d, _ = District.objects.get_or_create(
                code=code,
                defaults={"state": states_dict[state_code], "name": name, "labour_market_index": lmi}
            )
            districts_dict[code] = d

        # 3. SCHEMES
        schemes_data = [
            ("PMKVY", "Pradhan Mantri Kaushal Vikas Yojana 4.0", "Ministry of Skill Development & Entrepreneurship (MSDE)"),
            ("DDU_GKY", "Deen Dayal Upadhyaya Grameen Kaushalya Yojana", "Ministry of Rural Development (MoRD)"),
            ("NAPS", "National Apprenticeship Promotion Scheme", "MSDE & DGT"),
            ("ITI_CTS", "Craftsmen Training Scheme (ITI)", "Directorate General of Training (DGT)"),
            ("MSSDS", "Maharashtra State Skill Development Mission", "State Government of Maharashtra"),
            ("UPSDM", "Uttar Pradesh Skill Development Mission", "State Government of Uttar Pradesh"),
        ]
        schemes_dict = {}
        for code, name, ministry in schemes_data:
            sc, _ = Scheme.objects.get_or_create(code=code, defaults={"name": name, "central_ministry": ministry})
            schemes_dict[code] = sc

        # 4. COURSES (NSQF + NCO-2015)
        courses_data = [
            ("AUTO-CNC-401", "CNC Machine Operator", "Automotive", 4, "7223.0101", 360),
            ("AUTO-TW-402", "Two Wheeler Service Technician", "Automotive", 4, "7231.0401", 300),
            ("ELEC-SOLAR-401", "Solar PV Installation Technician", "Electronics & IT", 4, "7421.0302", 400),
            ("IT-DDEO-301", "Domestic Data Entry Operator", "Electronics & IT", 3, "4132.0402", 240),
            ("IT-IOT-501", "IoT Systems Field Technician", "Electronics & IT", 5, "3114.0201", 450),
            ("HLTH-GDA-401", "General Duty Assistant", "Healthcare", 4, "5321.0100", 380),
            ("HLTH-EMT-501", "Emergency Medical Technician", "Healthcare", 5, "3258.0101", 480),
            ("APPR-SMO-301", "Sewing Machine Operator", "Apparel & Textiles", 3, "7533.0101", 200),
            ("CONS-ELEC-301", "Assistant Electrician", "Construction", 3, "7411.0101", 320),
            ("CONS-PLUMB-401", "Plumber General", "Construction", 4, "7126.0101", 300),
        ]
        courses_dict = {}
        for code, title, sector, nsqf, nco, dur in courses_data:
            c, _ = Course.objects.get_or_create(
                course_code=code,
                defaults={"title": title, "sector": sector, "nsqf_level": nsqf, "nco_code": nco, "duration_hours": dur}
            )
            courses_dict[code] = c

        # 5. PROVIDERS
        providers_data = [
            ("TC-MH-0192", "Pimpri Chinchwad Skill Academy", "27", "519", "Sector 10, Bhosari MIDC, Pune", "A++", 0.04),
            ("TC-MH-0481", "Vidarbha Industrial Training Centre", "27", "515", "Hingna Road, Nagpur", "B", 0.14),
            ("TC-KA-0220", "Bengaluru Tech Skill Institute", "29", "572", "Peenya Industrial Area Phase 2, Bengaluru", "A++", 0.02),
            ("TC-UP-0105", "Awadh Kaushal Kendra", "09", "138", "Gomti Nagar Extension, Lucknow", "A", 0.07),
            ("TC-TN-0312", "Coimbatore Precision Engineering Centre", "33", "604", "Avinashi Road, Coimbatore", "A", 0.05),
            ("TC-DL-0084", "National Capital Skills Hub", "07", "093", "Okhla Industrial Area Phase 1, New Delhi", "A++", 0.03),
            ("TC-RJ-0155", "Jaipur Rural Artisan & Technical Centre", "08", "115", "Sitapura Industrial Area, Jaipur", "B", 0.12),
            ("TC-TS-0290", "Deccan Advanced Vocational Centre", "36", "532", "Sanathnagar, Hyderabad", "A", 0.06),
        ]
        providers_dict = {}
        for code, name, st_code, dist_code, addr, grade, risk in providers_data:
            p, _ = Provider.objects.get_or_create(
                code=code,
                defaults={
                    "name": name,
                    "state": states_dict[st_code],
                    "district": districts_dict[dist_code],
                    "address": addr,
                    "accreditation_grade": grade,
                    "risk_score": risk
                }
            )
            providers_dict[code] = p

        # 6. EMPLOYERS
        employers_data = [
            ("EMP-MH-50491", "Tata AutoComp Systems Ltd", "27AAACT2941K1ZP", "UDYAM-MH-26-0019284", "Automotive", "27", "519", 0.95, True),
            ("EMP-KA-30182", "Bosch India Automotive Ltd", "29AAACB1942A1Z4", "UDYAM-KR-03-0049182", "Automotive", "29", "572", 0.94, True),
            ("EMP-DL-10928", "Schneider Electric India Pvt Ltd", "07AAACS4812L1Z9", "UDYAM-DL-02-0012849", "Electronics & IT", "07", "093", 0.92, True),
            ("EMP-TN-40192", "Apollo Hospitals Enterprise Ltd", "33AAACA0192M1ZK", "UDYAM-TN-01-0091823", "Healthcare", "33", "603", 0.96, True),
            ("EMP-UP-60281", "Dixon Technologies India Ltd", "09AAACD3912N1Z1", "UDYAM-UP-12-0081294", "Electronics & IT", "09", "138", 0.89, True),
            ("EMP-MH-50999", "Shree Samarth Fabrication Works", "27BBBPS1920J1ZQ", "UDYAM-MH-26-0099412", "Capital Goods", "27", "519", 0.78, False),
            ("EMP-KA-30811", "Infosys BPM Logistics", "29AAACI0129D1ZN", "UDYAM-KR-03-0099182", "Electronics & IT", "29", "572", 0.93, True),
            ("EMP-RJ-70192", "Jaipur Rugs Weaving Collective", "08AAACJ4912P1ZR", "UDYAM-RJ-10-0041289", "Apparel & Textiles", "08", "115", 0.86, True),
            ("EMP-TS-80123", "MedPlus Health Services", "36AAACM8129Q1ZT", "UDYAM-TS-04-0019283", "Healthcare", "36", "532", 0.91, True),
            ("EMP-MH-99999", "QuickHire Services (Flagged Ghost Agency)", "27ZZZZZ9999Z1ZZ", "", "Manpower Staffing", "27", "519", 0.22, False),
        ]
        employers_dict = {}
        for eid, name, cin, udyam, sec, st_c, dist_c, score, badge in employers_data:
            emp, _ = Employer.objects.get_or_create(
                employer_id=eid,
                defaults={
                    "legal_name": name,
                    "cin_or_gstin": cin,
                    "udyam_reg": udyam,
                    "sector": sec,
                    "state": states_dict[st_c],
                    "district": districts_dict[dist_c],
                    "trust_score": score,
                    "is_verified_badge": badge,
                    "fraud_flag": (score < 0.35),
                    "fraud_reason": "High placement volume anomaly from single provider with zero statutory filings" if score < 0.35 else ""
                }
            )
            employers_dict[eid] = emp

        # 7. TRAINEES & LONGITUDINAL EPISODES (200 Curated Synthetic Trainees)
        names = [
            ("Rameshwar", "Kadam", "MALE", "27"), ("Pooja", "Shinde", "FEMALE", "27"),
            ("Sunil", "Patil", "MALE", "27"), ("Priyanka", "Deshmukh", "FEMALE", "27"),
            ("Ajit", "Pawar", "MALE", "27"), ("Kavita", "Gaikwad", "FEMALE", "27"),
            ("Naveen", "Gowda", "MALE", "29"), ("Deepika", "Bhat", "FEMALE", "29"),
            ("Kiran", "Kumar", "MALE", "29"), ("Shweta", "Shetty", "FEMALE", "29"),
            ("Amit", "Verma", "MALE", "09"), ("Suman", "Yadav", "FEMALE", "09"),
            ("Rajesh", "Tiwari", "MALE", "09"), ("Anjali", "Maurya", "FEMALE", "09"),
            ("Karthik", "Raman", "MALE", "33"), ("Lakshmi", "Subramanian", "FEMALE", "33"),
            ("Murugan", "Selvam", "MALE", "33"), ("Divya", "Krishnan", "FEMALE", "33"),
            ("Vikram", "Chauhan", "MALE", "07"), ("Neha", "Kapoor", "FEMALE", "07"),
            ("Arjun", "Singh", "MALE", "08"), ("Soniya", "Meena", "FEMALE", "08"),
            ("Srikanth", "Reddy", "MALE", "36"), ("Haritha", "Rao", "FEMALE", "36"),
        ]

        categories = ["GEN", "OBC", "SC", "ST", "EWS"]
        non_placement_reasons = [
            "Skill mismatch with local employer requirements",
            "No local vacancies in candidate district",
            "Wage offered below state reservation threshold",
            "Family constraints and inability to migrate",
            "Commute transport distance prohibitive",
            "Enrolled in formal higher degree program",
            "Started micro-enterprise in unorganized sector",
            "Medical / health condition during placement window",
        ]

        self.stdout.write("Generating longitudinal cohort records...")
        random.seed(42)

        for i in range(1, 161):
            name_tuple = names[(i - 1) % len(names)]
            st_code = name_tuple[3]
            state = states_dict[st_code]
            dist_options = [d for d in districts_dict.values() if d.state == state]
            district = dist_options[0] if dist_options else list(districts_dict.values())[0]

            stid = f"ST-{st_code}-{10000000 + i:08d}"
            person, created = Person.objects.get_or_create(
                stid=stid,
                defaults={"state_code_first": st_code, "status": "ACTIVE"}
            )

            if not created:
                continue

            full_name = f"{name_tuple[0]} {name_tuple[1]}"
            gender = name_tuple[2]
            birth_year = random.randint(1997, 2004)
            dob = date(birth_year, random.randint(1, 12), random.randint(1, 28))
            phone_num = f"9{random.randint(100000000, 999999999)}"
            phone_hash = hashlib.sha256(phone_num.encode('utf-8')).hexdigest()
            phone_last4 = phone_num[-4:]

            PersonPII.objects.create(
                person=person,
                full_name=full_name,
                dob=dob,
                gender=gender,
                guardian_name=f"{name_tuple[1]} Senior",
                address_line=f"House {random.randint(10, 400)}, Ward {random.randint(1, 15)}, {district.name}",
                phone_hash=phone_hash,
                phone_last4=phone_last4,
                category=random.choice(categories),
                disability=(i % 17 == 0),
                urban_rural="URBAN" if (i % 3 == 0) else "RURAL"
            )

            # Contact point (simulate 25% mobile churn)
            has_churned = (i % 4 == 0)
            ContactPoint.objects.create(
                person=person,
                contact_type="MOBILE",
                value_masked=f"+91 {phone_num[:2]}****{phone_last4}",
                value_hash=phone_hash,
                is_verified=not has_churned,
                is_primary=True,
                churn_count=1 if has_churned else 0
            )

            # Consent Artefact (DPDP Act 2023 compliant)
            consent_hash = hashlib.sha256(f"{stid}:v2.1-DPDP2023:HIN:MOBILE_OTP".encode('utf-8')).hexdigest()
            ConsentArtefact.objects.create(
                person=person,
                notice_version="v2.1-DPDP2023",
                language=random.choice(["HIN", "ENG", "MAR", "TAM", "TEL"]),
                channel="MOBILE_OTP",
                purpose_flags={
                    "followup_contact": True,
                    "employer_verification": True,
                    "registry_linkage": True,
                    "job_matching": True,
                    "deidentified_research": True
                },
                receipt_hash=consent_hash,
                status="ACTIVE"
            )

            # Scheme Enrolment & Certification
            scheme = random.choice(list(schemes_dict.values()))
            course = random.choice(list(courses_dict.values()))
            prov_options = [p for p in providers_dict.values() if p.state == state]
            provider = prov_options[0] if prov_options else list(providers_dict.values())[0]

            cert_days_ago = random.randint(60, 400)
            cert_date = date.today() - timedelta(days=cert_days_ago)
            enrolled_date = cert_date - timedelta(days=course.duration_hours // 4)

            SchemeCrosswalk.objects.create(
                scheme=scheme,
                scheme_trainee_id=f"{scheme.code}-2024-{st_code}-{10000 + i}",
                person=person,
                enrolled_date=enrolled_date,
                certified_date=cert_date,
                provider=provider,
                course=course
            )

            # Outcome Episode & Evidence Tiers
            # Distribution:
            # 45% Placed Tier A (Registry EPFO verified)
            # 22% Placed Tier B (Employer 3-Tap confirmed)
            # 10% Self-Employed Tier B/C
            # 5% Apprenticeship Tier A
            # 12% Not Employed Tier C (With granular reason)
            # 6% Unknown / Unreachable Tier U
            outcome_roll = i % 100
            start_date = cert_date + timedelta(days=random.randint(15, 45))

            if outcome_roll < 45:
                # Tier A: Wage Employment with EPFO match
                emp = random.choice(list(employers_dict.values())[:-1])
                wage_ratio = random.choice([1.1, 1.25, 1.4, 1.6, 2.1])
                wage_amt = int(state.min_wage_monthly * wage_ratio)
                wage_band = "1.0X_TO_1.5X" if wage_ratio < 1.5 else ("1.5X_TO_2.0X" if wage_ratio <= 2.0 else "ABOVE_2.0X")

                ep = OutcomeEpisode.objects.create(
                    person=person,
                    kind="WAGE_EMPLOYMENT",
                    start_date=start_date,
                    employer=emp,
                    nco_code=course.nco_code,
                    district=district,
                    state=state,
                    wage_band=wage_band,
                    monthly_wage_inr=wage_amt,
                    tier="A",
                    tier_source="EPFO_STATUTORY_REGISTRY",
                    rules_version="v2.0_NAT"
                )
                EvidenceItem.objects.create(
                    episode=ep,
                    kind="EPFO_HASH_CONFIRMED",
                    document_ref=f"EPFO-UAN-HASH-{hashlib.md5(stid.encode()).hexdigest()[:12].upper()}",
                    verified_by="EPFO API Setu Automated Gateway"
                )

            elif outcome_roll < 67:
                # Tier B: Wage Employment with 3-Tap Employer Confirmation
                emp = random.choice(list(employers_dict.values())[:-1])
                wage_amt = int(state.min_wage_monthly * 1.15)
                ep = OutcomeEpisode.objects.create(
                    person=person,
                    kind="WAGE_EMPLOYMENT",
                    start_date=start_date,
                    employer=emp,
                    nco_code=course.nco_code,
                    district=district,
                    state=state,
                    wage_band="1.0X_TO_1.5X",
                    monthly_wage_inr=wage_amt,
                    tier="B",
                    tier_source="EMPLOYER_3TAP_CONFIRMED",
                    rules_version="v2.0_NAT"
                )
                EvidenceItem.objects.create(
                    episode=ep,
                    kind="EMPLOYER_3TAP_CONFIRMED",
                    document_ref=f"VERIFY-TOKEN-{uuid.uuid4().hex[:12].upper()}",
                    verified_by=f"HR Portal: {emp.legal_name}"
                )
                VerificationRequest.objects.create(
                    employer=emp,
                    person=person,
                    episode=ep,
                    status="CONFIRMED",
                    is_currently_employed=True,
                    confirmed_start_date=start_date,
                    confirmed_wage_band="1.0X_TO_1.5X",
                    skill_rating=random.randint(4, 5),
                    responded_at=timezone.now()
                )

            elif outcome_roll < 77:
                # Tier B/C: Self-Employment (Udyam or Merchant QR)
                wage_amt = int(state.min_wage_monthly * 1.3)
                tier_choice = "B" if (i % 2 == 0) else "C"
                ep = OutcomeEpisode.objects.create(
                    person=person,
                    kind="SELF_EMPLOYMENT",
                    start_date=start_date,
                    district=district,
                    state=state,
                    wage_band="1.0X_TO_1.5X",
                    monthly_wage_inr=wage_amt,
                    tier=tier_choice,
                    tier_source="UDYAM_MSME_PROOF" if tier_choice == "B" else "UPI_MERCHANT_CORROBORATED",
                    rules_version="v2.0_NAT"
                )
                EvidenceItem.objects.create(
                    episode=ep,
                    kind="UDYAM_REGISTRATION" if tier_choice == "B" else "BANK_UPI_MERCHANT",
                    document_ref=f"UDYAM-{st_code}-94819" if tier_choice == "B" else "UPI-TXN-SUMMARY",
                    verified_by="MSME Udyam API" if tier_choice == "B" else "Account Aggregator Consent Flow"
                )

            elif outcome_roll < 82:
                # Tier A: Registered Apprenticeship
                emp = random.choice(list(employers_dict.values())[:-1])
                stipend = int(state.min_wage_monthly * 0.9)
                ep = OutcomeEpisode.objects.create(
                    person=person,
                    kind="APPRENTICESHIP",
                    start_date=start_date,
                    employer=emp,
                    nco_code=course.nco_code,
                    district=district,
                    state=state,
                    wage_band="BELOW_MIN_WAGE",
                    monthly_wage_inr=stipend,
                    tier="A",
                    tier_source="NAPS_PORTAL_CONTRACT",
                    rules_version="v2.0_NAT"
                )
                EvidenceItem.objects.create(
                    episode=ep,
                    kind="APPRENTICE_PORTAL_CONTRACT",
                    document_ref=f"NAPS-CNTR-2024-{random.randint(100000, 999999)}",
                    verified_by="DGT National Apprenticeship Portal"
                )

            elif outcome_roll < 94:
                # Tier C: Not Employed with granular non-placement reason
                reason = random.choice(non_placement_reasons)
                OutcomeEpisode.objects.create(
                    person=person,
                    kind="NOT_EMPLOYED",
                    start_date=cert_date,
                    district=district,
                    state=state,
                    wage_band="NOT_APPLICABLE",
                    monthly_wage_inr=0,
                    tier="C",
                    tier_source="CORROBORATED_FIELD_SURVEY",
                    rules_version="v2.0_NAT",
                    non_placement_reason=reason
                )

            else:
                # Tier U: Unknown / Unreachable
                OutcomeEpisode.objects.create(
                    person=person,
                    kind="UNKNOWN_UNREACHABLE",
                    start_date=cert_date,
                    district=district,
                    state=state,
                    wage_band="NOT_APPLICABLE",
                    monthly_wage_inr=0,
                    tier="U",
                    tier_source="CHURN_EXHAUSTED",
                    rules_version="v2.0_NAT",
                    non_placement_reason="Unreachable after 6 multi-channel escalation attempts"
                )

            # Follow Up Task (Wave tracking)
            waves = ["T+30", "T+90", "T+180", "T+365"]
            task_wave = waves[i % len(waves)]
            due = cert_date + timedelta(days=int(task_wave.replace("T+", "")))
            fu_status = "ANSWERED" if outcome_roll < 94 else ("UNREACHABLE" if has_churned else "ESCALATED")
            fu_channel = "TELEGRAM" if i % 3 == 0 else ("WHATSAPP" if i % 3 == 1 else "ASSISTED_CALL")

            task = FollowUpTask.objects.create(
                person=person,
                wave=task_wave,
                due_date=due,
                channel_current=fu_channel,
                escalation_step=5 if has_churned else (1 if fu_status == "ANSWERED" else 3),
                attempts_count=4 if has_churned else 1,
                status=fu_status,
                response_propensity_score=0.42 if has_churned else 0.88,
                intensive_subsample=(i % 10 == 0)
            )

            if fu_status == "ANSWERED":
                SurveyResponse.objects.create(
                    task=task,
                    channel=fu_channel,
                    employment_status="Employed" if outcome_roll < 82 else "Seeking Employment",
                    employer_name="Confirmed" if outcome_roll < 82 else "",
                    wage_reported=int(state.min_wage_monthly * 1.2) if outcome_roll < 82 else 0,
                    non_placement_reason_raw="" if outcome_roll < 82 else "No matching job in my tehsil",
                    reason_nlp_classified="" if outcome_roll < 82 else "No local vacancies in candidate district",
                    disposition_code="COMPLETE"
                )

        # 8. HUMAN REVIEW QUEUE (Scores in grey band 0.75 to 0.92)
        self.stdout.write("Populating Identity Resolution Review Queue...")
        p1 = Person.objects.filter(state_code_first="27").first()
        p2 = Person.objects.filter(state_code_first="27").last()
        if p1 and p2 and p1 != p2:
            IdentityMatchQueue.objects.get_or_create(
                candidate_a=p1,
                candidate_b=p2,
                defaults={
                    "match_score": 0.86,
                    "match_reasons": "Indic phonetic match (Jaro-Winkler: 0.94); Exact DOB match (1999-04-12); Alternate father name token overlap: 0.88; SIM phone hash mismatch (Carrier porting churn)",
                    "status": "PENDING_REVIEW"
                }
            )

        p3 = Person.objects.filter(state_code_first="29").first()
        p4 = Person.objects.filter(state_code_first="29").last()
        if p3 and p4 and p3 != p4:
            IdentityMatchQueue.objects.get_or_create(
                candidate_a=p3,
                candidate_b=p4,
                defaults={
                    "match_score": 0.81,
                    "match_reasons": "Transliterated Kannada to Latin script match; Same pincode 560058; Differing scheme roll numbers across PMKVY and NAPS",
                    "status": "PENDING_REVIEW"
                }
            )

        # 9. PENDING VERIFICATION REQUEST (For live 3-tap employer demo)
        pending_person = Person.objects.filter(outcome_episodes__tier="B").first()
        pending_emp = employers_dict["EMP-MH-50491"]
        demo_token = uuid.UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6")
        VerificationRequest.objects.get_or_create(
            token=demo_token,
            defaults={
                "employer": pending_emp,
                "person": pending_person or Person.objects.first(),
                "status": "PENDING"
            }
        )

        # 10. ACTION CASES (Rule Alerts & District Officer Remediation)
        self.stdout.write("Configuring District Remediation Cases...")
        ActionCase.objects.get_or_create(
            case_id="CASE-2026-MH-019",
            defaults={
                "rule_id": "RULE-AL1-LOW-PLACEMENT",
                "state": states_dict["27"],
                "district": districts_dict["519"],
                "provider": providers_dict["TC-MH-0481"],
                "course": courses_dict["AUTO-CNC-401"],
                "severity": "HIGH",
                "title": "Low 6-Month Placement Velocity in CNC Machine Operator Batch",
                "description": "Provider TC-MH-0481 reports verified placement rate of only 28.4% (Threshold: 60%). High concentration of non-placement reason: 'Skill mismatch with local CNC tolerances'.",
                "assignee": "District Skill Officer, Pune (DSO-PUN-01)",
                "status": "IN_PROGRESS",
                "corrective_action_log": "Inspection notice issued to training centre. Employer round-table scheduled with Bhosari Industrial Association for curriculum recalibration."
            }
        )
        ActionCase.objects.get_or_create(
            case_id="CASE-2026-KA-004",
            defaults={
                "rule_id": "RULE-AL5-GHOST-EMPLOYER",
                "state": states_dict["29"],
                "district": districts_dict["572"],
                "provider": providers_dict["TC-KA-0220"],
                "severity": "CRITICAL",
                "title": "Suspected Ghost Employer Placement Claims Detected",
                "description": "24 trainees reported placed at 'QuickHire Staffing' without corresponding EPFO statutory deposits or valid GSTIN active status.",
                "assignee": "State Mission Director, Karnataka Skill Mission",
                "status": "OPEN",
                "corrective_action_log": "Automated payment freeze enacted. On-site verification squad deputed to registered corporate address."
            }
        )

        # 11. AUDIT TRAIL (Hash chained events)
        self.stdout.write("Initializing Cryptographic Audit Trail...")
        AuditEvent.objects.create(
            actor="SYSTEM_INIT",
            action="GENESIS_REGISTRY_BOOTSTRAP",
            target_object="Registry/NationalMaster",
            purpose="National Longitudinal Skilling Outcomes Engine initialized under DPDP Act 2023 regulations"
        )
        AuditEvent.objects.create(
            actor="officer_dso_pune@skilltrace.gov.in",
            action="READ_PII_DECRYPT",
            target_object="Person/ST-27-00000001",
            purpose="Assisted follow-up verification under Section 6 DPDP Act 2023"
        )

        self.stdout.write(self.style.SUCCESS("Successfully seeded SkillTrace India master data and longitudinal records."))

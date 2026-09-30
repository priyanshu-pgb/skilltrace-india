from django.core.management.base import BaseCommand
from skills.models import Skill
from assessments.models import Question, PracticalTask

class Command(BaseCommand):
    help = 'Seeds complete comprehensive MCQs and Practical Tasks for all 10 skills'

    def handle(self, *args, **options):
        self.stdout.write("Starting comprehensive question and practical seeding...")

        all_questions = {
            'HTML/CSS': [
                ("Which HTML5 semantic element is used to define navigation links?", "easy", "<nav>", "<navigation>", "<links>", "<menu>", "a", "The <nav> tag specifies a section that contains major navigation links."),
                ("Which CSS property is used to control spacing inside an element's border?", "easy", "margin", "padding", "border-spacing", "gap", "b", "Padding controls internal whitespace between the content and the element border."),
                ("What does CSS 'display: flex' establish on a container?", "easy", "A grid formatting context", "A block formatting context", "A flex formatting context for child items", "An inline text flow", "c", "display: flex transforms direct children into flexible flex items."),
                ("Which unit is relative to the font-size of the root element (html)?", "medium", "em", "rem", "px", "vh", "b", "rem (root em) computes relative to the <html> root element's font size."),
                ("What is the CSS Box Model order from inside to outside?", "medium", "Content, Margin, Border, Padding", "Content, Padding, Border, Margin", "Content, Border, Padding, Margin", "Padding, Content, Border, Margin", "b", "The Box Model consists of Content, surrounded by Padding, Border, and Margin."),
                ("Which CSS selector has the highest specificity?", "medium", "div.card", "#user-profile", ".btn-primary:hover", "input[type='text']", "b", "ID selectors (#id) carry a higher specificity weight than class, attribute, or tag selectors."),
                ("What does 'box-sizing: border-box' do?", "medium", "Excludes padding from element width", "Includes padding and border within the declared width and height", "Adds an automatic drop shadow", "Removes default margins", "b", "border-box ensures padding and borders do not expand the element beyond width/height."),
                ("Which media query targets mobile screens narrower than 768px?", "medium", "@media (min-width: 768px)", "@media (max-width: 767px)", "@media (device: mobile)", "@media screen and (orientation: portrait)", "b", "max-width: 767px matches screens 767px and below."),
                ("In CSS Grid, what does 'repeat(auto-fit, minmax(250px, 1fr))' achieve?", "hard", "A fixed 4-column layout", "A responsive grid that wraps columns automatically without media queries", "An animated slider", "A fixed height scroll area", "b", "auto-fit with minmax provides fluid wrapping columns adapted to viewport width."),
                ("What is the purpose of the CSS ':focus-visible' pseudo-class?", "hard", "Applies focus styles only when the browser determines keyboard/non-mouse focus is active", "Styles all links on click", "Forces an element to remain focused permanently", "Hides the element", "a", ":focus-visible provides accessibility focus rings for keyboard users while avoiding mouse-click focus rings.")
            ],
            'JavaScript': [
                ("What is the difference between 'let' and 'var' in JavaScript?", "easy", "var is block-scoped, let is function-scoped", "let is block-scoped, var is function-scoped", "There is no difference", "let cannot be reassigned", "b", "let and const provide block scoping, whereas var is scoped to the enclosing function."),
                ("What does the '===' operator check in JavaScript?", "easy", "Value only with type coercion", "Both value and type without coercion", "Memory pointer only", "String equivalence only", "b", "The strict equality operator === compares both data type and value."),
                ("Which method transforms every element of an array and returns a new array?", "easy", "forEach()", "filter()", "map()", "reduce()", "c", "Array.prototype.map() transforms each item and returns a new array of matching length."),
                ("What does 'typeof null' return in JavaScript?", "medium", "'null'", "'undefined'", "'object'", "'boolean'", "c", "Due to a historic bug in JS implementation, typeof null returns 'object'."),
                ("What is the Event Loop in JavaScript runtime?", "hard", "A loop iterating through DOM elements", "A runtime mechanism that coordinates asynchronous callbacks with the call stack", "A web worker thread", "A syntax for loops", "b", "The event loop continuously transfers queued macrotasks and microtasks into the call stack when empty."),
                ("What is a Closure in JavaScript?", "medium", "A closed browser tab", "A function bundled with references to its surrounding lexical state", "A JSON object", "A method to delete cookies", "b", "A closure gives an inner function access to an outer function's scope even after the outer function has returned."),
                ("Which array method returns the first element that satisfies a test condition?", "medium", "filter()", "find()", "indexOf()", "some()", "b", "Array.prototype.find() returns the value of the first matching element, or undefined."),
                ("What is the output of '2' + 2 - 1 in JavaScript?", "medium", "3", "21", "NaN", "Error", "b", "'2' + 2 evaluates to '22' (string concatenation), then '22' - 1 coerces to number 21."),
                ("How do you create an asynchronous function that handles Promises cleanly?", "easy", "async / await", "try / catch", "then / catch", "defer / sync", "a", "async/await allows working with Promises in an imperative, readable structure."),
                ("What does Object.freeze() do to an object?", "hard", "Prevents garbage collection", "Makes an object completely immutable by preventing additions, deletions, and property modifications", "Deep-clones an object", "Encrypts the object", "b", "Object.freeze() prevents extensions and marks all existing properties as non-writable and non-configurable.")
            ],
            'Excel': [
                ("Which formula searches for a value in the leftmost column of a table and returns a value in the same row?", "easy", "INDEX", "VLOOKUP", "MATCH", "SEARCH", "b", "VLOOKUP searches vertically in the first column and retrieves corresponding values."),
                ("What symbol is used to create absolute cell references in Excel (e.g. locking row and column)?", "easy", "#", "$", "@", "&", "b", "The $ sign (e.g. $A$1) locks row and column references during formula dragging."),
                ("Which function calculates the sum of cells that meet multiple specified criteria?", "easy", "SUM", "SUMIF", "SUMIFS", "TOTALIF", "c", "SUMIFS handles multiple criteria ranges simultaneously."),
                ("What combination of functions is modernly preferred over VLOOKUP for dynamic lookups?", "medium", "INDEX and MATCH", "HLOOKUP and TRANSPOSE", "CONCATENATE and MID", "COUNT and AVERAGE", "a", "INDEX/MATCH allows flexible lookups across any column without column-index hardcoding."),
                ("What feature summarizes, groups, and aggregates large datasets without writing formulas?", "easy", "Pivot Tables", "Conditional Formatting", "Data Validation", "Text to Columns", "a", "Pivot Tables provide drag-and-drop aggregation, slicing, and reporting."),
                ("What does the IFERROR function do in Excel?", "medium", "Causes the formula to throw an error", "Returns a specified fallback value if a formula evaluates to an error", "Counts syntax errors", "Deletes erroneous cells", "b", "IFERROR(value, value_if_error) traps errors like #N/A and returns a friendly fallback."),
                ("Which function counts the number of non-empty cells in a range?", "medium", "COUNT", "COUNTA", "COUNTBLANK", "COUNTIF", "b", "COUNTA counts cells containing any data, whereas COUNT only counts numeric values."),
                ("What major advantage does XLOOKUP have over legacy VLOOKUP?", "hard", "Defaults to exact match and can look to the left and return arrays", "Runs only on macOS", "Requires sorted columns", "Only works on dates", "a", "XLOOKUP does not require column numbering, looks left/right, and defaults to exact match."),
                ("Which tool restricts the type of data or values that users can enter into a cell?", "medium", "Conditional Formatting", "Data Validation", "Goal Seek", "Solver", "b", "Data Validation creates dropdowns, date limits, and numeric validation rules."),
                ("What is the purpose of Goal Seek in Excel?", "hard", "To format tables", "To find the input value needed to achieve a target formula output (reverse calculation)", "To sort rows", "To automate VBA macros", "b", "Goal Seek performs what-if analysis to determine input parameters needed for a specific result.")
            ],
            'Power BI': [
                ("What does DAX stand for in Power BI?", "easy", "Data Analysis Expressions", "Digital Analytics XML", "Direct Access Query", "Database Automation Extension", "a", "DAX is the formula and query language utilized across Power BI and Analysis Services."),
                ("Which Power BI component is used to extract, transform, and clean raw data before loading?", "easy", "Power View", "Power Query", "Power Pivot", "DAX Studio", "b", "Power Query (M language) performs ETL operations to shape and clean data."),
                ("What is the difference between a Calculated Column and a Measure in DAX?", "medium", "Calculated columns compute row-by-row and consume RAM; Measures compute on aggregation dynamically", "There is no difference", "Measures can only calculate sums", "Calculated columns are created in Python", "a", "Calculated columns evaluate row-context upon data load; measures evaluate dynamically based on filter context."),
                ("Which DAX function overrides or alters the existing filter context in a measure?", "medium", "FILTER", "CALCULATE", "SUMX", "ALL", "b", "CALCULATE is the fundamental DAX function that modifies filter contexts during aggregation."),
                ("What is a Star Schema in Power BI data modeling?", "medium", "A model where visuals are shaped like stars", "A model consisting of central Fact tables connected to surrounding Dimension tables", "A decentralized multi-cloud model", "A web-scraping schema", "b", "Star schema organizes numeric facts centrally surrounded by descriptive dimension lookup tables."),
                ("What does the DAX function ALL(TableName) do?", "medium", "Selects all columns", "Removes all filters applied to the specified table or columns", "Sums all rows", "Generates a table of distinct values", "b", "ALL ignores active visual and slicer filters, useful for calculating grand totals and percentages."),
                ("What is a Slicer in Power BI?", "easy", "A tool to slice images", "An on-canvas visual filter that enables users to segment data dynamically", "A database partitioning command", "A DAX mathematical operator", "b", "Slicers are interactive visual controls allowing end-users to filter reports."),
                ("What is the purpose of Row-Level Security (RLS) in Power BI?", "hard", "Encrypts database backups", "Restricts data access for given users based on role filters", "Compresses row storage", "Sorts tables by primary key", "b", "RLS enforces security filters so users only see data rows relevant to their department or permissions."),
                ("Which DAX function performs row-by-row iteration before summing the results?", "hard", "SUM", "SUMX", "TOTAL", "AGGREGATE", "b", "SUMX is an iterator function that evaluates an expression for every row in a table and sums the outcomes."),
                ("What is the M language in Power BI?", "hard", "A machine learning language", "The functional programming language behind Power Query data transformation steps", "A markup language like HTML", "A DAX synonym", "b", "M is the Power Query formula language used to document ETL step execution.")
            ],
            'Communication': [
                ("What is active listening in a professional workplace?", "easy", "Waiting impatiently for your turn to speak", "Fully concentrating, understanding, responding thoughtfully, and retaining what is said", "Nodding while typing an email", "Recording conversations without permission", "b", "Active listening requires full engagement, validating understanding, and respectful feedback."),
                ("When communicating critical project delays to stakeholders, what is the best approach?", "easy", "Hide the delay until the final deadline", "Proactively communicate the issue early, explain root causes, and present mitigation solutions", "Blame other team members", "Send an ambiguous one-line email", "b", "Proactive transparency accompanied by actionable remediation builds stakeholder trust."),
                ("What does the 'STAR' method stand for in behavioral updates and interviews?", "medium", "Situation, Task, Action, Result", "Strategy, Team, Analysis, Report", "Start, Test, Align, Review", "Summary, Timing, Assessment, Resolution", "a", "STAR (Situation, Task, Action, Result) structures concise, impact-oriented narratives."),
                ("What is the ideal tone for formal client correspondence regarding a disputed deliverable?", "medium", "Aggressive and defensive", "Objective, polite, evidence-based, and solution-focused", "Informal with casual slang", "Dismissive and brief", "b", "A calm, professional, factual tone defuses tension and drives alignment."),
                ("Which channel is best suited for complex, emotionally sensitive, or high-conflict feedback?", "medium", "Group chat message", "1-on-1 private video or in-person discussion", "Company-wide email", "Anonymous memo", "b", "Direct personal conversations facilitate empathy, tone nuance, and immediate two-way clarification."),
                ("What is the 7 Cs framework of effective business communication?", "hard", "Clear, Concise, Concrete, Correct, Coherent, Complete, Courteous", "Chatty, Clever, Complex, Casual, Colorful, Cryptic, Cheap", "Coding, Cloud, Compute, Connect, Cache, Cluster, Control", "Create, Copy, Check, Cancel, Cut, Close, Commit", "a", "The 7 Cs ensure messages are clear, concise, accurate, courteous, and easily comprehended."),
                ("How should constructive feedback be delivered to a colleague?", "medium", "Publicly in the team standup", "Privately, focusing on specific behaviors and outcomes rather than personal traits", "Through a third party", "In a vague joke", "b", "Effective feedback is timely, private, behavior-focused, and actionable."),
                ("What is empathetic communication?", "medium", "Agreeing with everything everyone says", "Understanding and acknowledging the other person's perspective and feelings before offering advice", "Using dramatic expressions", "Ignoring client feedback", "b", "Empathy demonstrates genuine consideration for the other person's viewpoint."),
                ("In technical documentation, what is the primary goal of the author?", "easy", "To impress readers with obscure vocabulary", "To convey complex concepts with simplicity, clarity, and reproducible accuracy", "To write as many pages as possible", "To hide proprietary secrets", "b", "Technical writing should enable readers to understand and reproduce systems without ambiguity."),
                ("What is an effective way to conclude a cross-functional alignment meeting?", "medium", "Abruptly end the call when time expires", "Summarize key decisions, agreed action items, owners, and clear target deadlines", "Ask everyone to figure out their own next steps", "Schedule another meeting without discussion", "b", "Explicit alignment on action items, owners, and timelines ensures execution accountability.")
            ],
            'REST APIs': [
                ("What HTTP method should be used to retrieve data from a resource without causing side effects?", "easy", "POST", "GET", "PUT", "DELETE", "b", "GET requests are idempotent and read-only, retrieving resource representations safely."),
                ("Which HTTP status code signifies that a resource was successfully created?", "easy", "200 OK", "201 Created", "204 No Content", "400 Bad Request", "b", "HTTP 201 indicates that the request succeeded and led to resource creation."),
                ("What is the difference between PUT and PATCH in RESTful design?", "medium", "PUT updates partial fields; PATCH replaces the whole resource", "PUT replaces the complete resource; PATCH updates specific partial fields", "They are identical in HTTP specification", "PATCH is only for delete operations", "b", "PUT is idempotent full replacement; PATCH applies partial modifications."),
                ("Which HTTP status code indicates that the client request lacks valid authentication credentials?", "easy", "401 Unauthorized", "403 Forbidden", "404 Not Found", "500 Internal Error", "a", "401 Unauthorized indicates the request has not been applied because it lacks valid auth credentials."),
                ("What does idempotency mean in the context of HTTP methods?", "medium", "The method executes faster than others", "Making multiple identical requests has the same outcome as a single request", "The server deletes cache on every call", "The request requires an API key", "b", "Methods like GET, PUT, and DELETE are idempotent because repeated identical calls produce identical server state."),
                ("Which HTTP status code is returned when a client is authenticated but lacks permission to access the resource?", "medium", "401 Unauthorized", "403 Forbidden", "400 Bad Request", "405 Method Not Allowed", "b", "403 Forbidden indicates the server understands who the client is, but refuses authorization."),
                ("What is the purpose of the 'Content-Type' request header?", "easy", "Specifies the client's screen resolution", "Indicates the media type / MIME format of the request payload (e.g. application/json)", "Contains user passwords", "Sets cookie expiration", "b", "Content-Type informs the receiver how to parse the request body."),
                ("What is CORS (Cross-Origin Resource Sharing)?", "hard", "A server optimization technique", "A browser security mechanism that restricts HTTP requests made from a different domain/origin", "A database protocol", "A JSON compression library", "b", "CORS uses HTTP headers to tell browsers whether a web app on one origin can access resources from another."),
                ("What is a stateless API architecture?", "hard", "An API that has no database", "An architecture where each client request must contain all information necessary to process it, without server session affinity", "An API that only returns static files", "An API without authentication", "b", "Statelessness means the server does not store client session context between requests."),
                ("Which HTTP header is standardly used to pass Bearer tokens for API authentication?", "medium", "Authentication", "Authorization", "X-Api-Token", "Bearer-Token", "b", "The standard Authorization header passes credentials (e.g. 'Authorization: Bearer <token>').")
            ],
            'Git': [
                ("Which Git command initializes a new repository in the current directory?", "easy", "git start", "git init", "git new", "git create", "b", "git init creates a new Git repository or reinitializes an existing one."),
                ("What does 'git add' do?", "easy", "Commits changes to GitHub directly", "Adds file changes from the working tree to the staging area / index", "Reverts changes", "Deletes untracked files", "b", "git add stages changes in preparation for the next commit."),
                ("Which command shows the working tree status and staged vs untracked files?", "easy", "git log", "git status", "git branch", "git diff", "b", "git status summarizes modified, staged, and untracked files in the current repository."),
                ("What is the difference between 'git merge' and 'git rebase'?", "medium", "merge combines commits and creates a merge commit; rebase replays commits on top of another branch for linear history", "merge deletes branches; rebase renames branches", "rebase is only used on remote repositories", "They produce identical git logs", "a", "rebase rewrites commit history onto a new base commit for clean linear progression."),
                ("What command creates and switches to a new branch named 'feature-auth'?", "easy", "git branch feature-auth", "git checkout -b feature-auth (or git switch -c feature-auth)", "git new feature-auth", "git fork feature-auth", "b", "git checkout -b or git switch -c creates and immediately checks out the new branch."),
                ("What does 'git stash' do?", "medium", "Deletes all uncommitted work", "Temporarily shelves (stashes) uncommitted modifications so you can work on a clean tree", "Pushes code to origin", "Compiles the application", "b", "git stash saves dirty working directory state to a stack and restores a clean branch."),
                ("What does the command 'git pull' do under the hood?", "medium", "git push followed by git merge", "git fetch followed by git merge", "git clone followed by git commit", "git reset --hard", "b", "git pull fetches remote changes and immediately integrates them via merge or rebase."),
                ("How do you undo the last commit while keeping the modified files staged in your working directory?", "hard", "git reset --hard HEAD~1", "git reset --soft HEAD~1", "git revert HEAD", "git rm HEAD", "b", "git reset --soft HEAD~1 undoes the commit but leaves changes staged."),
                ("What does 'git cherry-pick <commit-hash>' do?", "hard", "Deletes a specific commit", "Applies the changes introduced by a specific existing commit onto your current branch", "Finds the latest tag", "Creates a cherry branch", "b", "git cherry-pick applies a single commit from another branch onto HEAD."),
                ("What is the purpose of a .gitignore file?", "easy", "To configure user emails", "To tell Git which files or directories to ignore and never track (e.g. node_modules, .env)", "To password-protect files", "To speed up download speeds", "b", ".gitignore prevents specified files from being tracked by version control.")
            ],
            'Statistics': [
                ("What is the difference between Mean, Median, and Mode?", "easy", "Mean is the average, Median is the middle value, Mode is the most frequent value", "Mean is the middle, Median is the sum, Mode is the variance", "They are identical in all distributions", "Mode is only used for negative numbers", "a", "Mean is arithmetic average; Median is 50th percentile; Mode is highest frequency."),
                ("Which measure of spread represents the average squared deviation from the mean?", "medium", "Range", "Variance", "Interquartile Range", "Standard Deviation", "b", "Variance measures average squared dispersion; Standard Deviation is its square root."),
                ("What is the Empirical Rule (68-95-99.7) for normal distributions?", "medium", "68% within 1 SD, 95% within 2 SD, 99.7% within 3 SD of the mean", "99% within 1 SD, 95% within 2 SD, 68% within 3 SD", "All data points must fall within 2 SD", "Only applies to uniform data", "a", "The 68-95-99.7 rule characterizes proportions of data within 1, 2, and 3 standard deviations in normal curves."),
                ("What does a P-value represent in statistical hypothesis testing?", "medium", "The probability that the alternate hypothesis is 100% true", "The probability of observing results at least as extreme as observed, assuming the null hypothesis is true", "The sample size percentage", "The statistical power of the test", "b", "A low p-value (typically <= 0.05) suggests observed data is unlikely under the null hypothesis."),
                ("What is Type I Error in hypothesis testing?", "hard", "Accepting the null hypothesis when it is false", "Rejecting the null hypothesis when it is actually true (false positive)", "Making a calculation typo", "Having too small of a sample", "b", "Type I error is a false positive (rejecting a true null hypothesis)."),
                ("What is the difference between correlation and causation?", "easy", "Correlation means one event causes another", "Correlation indicates a statistical association between variables; causation proves one variable directly causes change in another", "They are mathematically interchangeable", "Causation only applies to medicine", "b", "Correlation does not imply causation; confounding variables may explain the association."),
                ("What is the Central Limit Theorem (CLT)?", "hard", "The mean always equals the median", "The distribution of sample means approaches a normal distribution as sample size increases, regardless of population distribution", "Every sample must be larger than 10,000", "Outliers are automatically removed", "b", "CLT states that sample means will follow an approximately normal distribution for sufficiently large n."),
                ("What does the Interquartile Range (IQR) represent?", "medium", "Maximum minus Minimum", "The range between the 75th percentile (Q3) and 25th percentile (Q1)", "Standard deviation divided by mean", "Variance squared", "b", "IQR = Q3 - Q1, capturing the spread of the middle 50% of observations resiliently to outliers."),
                ("What is an R-squared value in regression analysis?", "hard", "The slope of the line", "The proportion of variance in the dependent variable explained by independent variables", "The standard error of residuals", "The probability of multicollinearity", "b", "R² (coefficient of determination) indicates goodness-of-fit of a regression model (0 to 1)."),
                ("What is stratified sampling?", "medium", "Picking numbers completely at random", "Dividing the population into distinct subgroups (strata) and sampling proportionally from each", "Sampling only the first 50 respondents", "Surveying only friends", "b", "Stratified sampling ensures balanced representation across key demographic subgroups.")
            ]
        }

        total_questions_seeded = 0
        for skill_name, q_list in all_questions.items():
            try:
                skill = Skill.objects.get(name=skill_name)
            except Skill.DoesNotExist:
                self.stdout.write(self.style.WARNING(f"Skill '{skill_name}' not found, skipping."))
                continue

            for text, diff, a, b, c, d, correct, expl in q_list:
                _, created = Question.objects.get_or_create(
                    skill=skill,
                    text=text,
                    defaults={
                        'difficulty': diff,
                        'option_a': a,
                        'option_b': b,
                        'option_c': c,
                        'option_d': d,
                        'correct_option': correct,
                        'explanation': expl
                    }
                )
                if created:
                    total_questions_seeded += 1

        self.stdout.write(self.style.SUCCESS(f"Seeded {total_questions_seeded} questions across skills."))

        # Seed practical tasks
        practicals_data = [
            (
                'HTML/CSS',
                'Responsive Flexbox Profile Card',
                'Build a clean HTML/CSS profile card structure using semantic tags and flexbox alignment.',
                'easy',
                '1. Use flexbox centering\n2. Style card with 12px border radius\n3. Include user name, title, and contact badge',
                '<div class="profile-card">\n  <h2>Candidate Name</h2>\n  <p>Software Engineer</p>\n</div>',
                3
            ),
            (
                'JavaScript',
                'Array Deduplication & Numerical Sort',
                'Write a JavaScript function deduplicate(arr) that filters out duplicate numbers from an array and sorts it ascending.',
                'medium',
                '1. Function must be named deduplicate(arr)\n2. Must return unique numbers sorted ascending\n3. Must handle empty arrays',
                'function deduplicate(arr) {\n  return [...new Set(arr)].sort((a, b) => a - b);\n}',
                4
            ),
            (
                'REST APIs',
                'Design RESTful Employee Status Endpoint Parser',
                'Implement a Python function parse_api_status(response_json) that extracts status and wage increases safely.',
                'medium',
                '1. Safely extract "status" defaulting to "unemployed"\n2. Parse "monthly_wage" integer\n3. Calculate annual wage projection',
                'def parse_api_status(data):\n    status = data.get("status", "unemployed")\n    wage = int(data.get("monthly_wage", 0))\n    return {"status": status, "annual_projected": wage * 12}\n',
                3
            ),
            (
                'Git',
                'Git Conflict Resolution & Rebase Commands',
                'Provide the sequence of Git commands needed to rebase a feature branch onto main and resolve merge conflicts.',
                'medium',
                '1. Rebase onto origin/main\n2. Stage resolved conflicts\n3. Continue rebase without merge commits',
                '# 1. git fetch origin\n# 2. git rebase origin/main\n# 3. git add .\n# 4. git rebase --continue\n',
                3
            ),
            (
                'Excel',
                'Sales Commission & Target Aggregation Formula',
                'Write the logic for computing tiered sales commissions based on performance threshold brackets.',
                'easy',
                '1. 5% commission on sales up to 100,000\n2. 10% commission on sales exceeding 100,000\n3. Return rounded integer',
                'def calculate_commission(sales):\n    if sales <= 100000:\n        return round(sales * 0.05)\n    return round(5000 + (sales - 100000) * 0.10)\n',
                3
            ),
            (
                'Power BI',
                'DAX YoY Revenue Growth Measure',
                'Formulate the DAX measure for computing Year-over-Year (YoY) revenue percentage growth using SAMEPERIODLASTYEAR.',
                'hard',
                '1. Calculate current year revenue\n2. Calculate prior year revenue using SAMEPERIODLASTYEAR\n3. Return DIVIDE difference by prior revenue',
                'YoY_Growth = \nVAR CurrentRev = [Total_Revenue]\nVAR PriorRev = CALCULATE([Total_Revenue], SAMEPERIODLASTYEAR(\'Calendar\'[Date]))\nRETURN DIVIDE(CurrentRev - PriorRev, PriorRev, 0)\n',
                3
            ),
            (
                'Communication',
                'Executive Status Escalation Memo',
                'Draft a professional, solution-oriented executive email addressing a 2-week deliverable delay to key enterprise clients.',
                'medium',
                '1. Use empathetic, accountable opening\n2. Clearly articulate root cause\n3. Present 2 mitigation recovery options\n4. Confirm review date',
                'Subject: Project Status Update & Remediation Schedule\n\nDear Steering Committee,\n\nWe are proactively sharing a revised schedule for the upcoming deployment...',
                3
            ),
            (
                'Statistics',
                'Z-Score & Outlier Detection Function',
                'Implement a Python function calculate_z_scores(values) that identifies data points with |z| > 2.5 as statistical outliers.',
                'medium',
                '1. Calculate mean and standard deviation\n2. Compute z = (x - mean) / std\n3. Flag outliers exceeding threshold 2.5',
                'import statistics\n\ndef calculate_z_scores(values):\n    if len(values) < 2:\n        return []\n    m = statistics.mean(values)\n    s = statistics.stdev(values)\n    if s == 0:\n        return [0] * len(values)\n    return [(x - m) / s for x in values]\n',
                3
            ),
        ]

        total_practicals = 0
        for skill_name, title, desc, diff, reqs, starter, count in practicals_data:
            try:
                skill = Skill.objects.get(name=skill_name)
                _, created = PracticalTask.objects.get_or_create(
                    skill=skill,
                    title=title,
                    defaults={
                        'description': desc,
                        'difficulty': diff,
                        'requirements': reqs,
                        'starter_code': starter,
                        'test_cases_count': count
                    }
                )
                if created:
                    total_practicals += 1
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error practical for {skill_name}: {e}"))

        self.stdout.write(self.style.SUCCESS(f"Seeded {total_practicals} practical tasks."))

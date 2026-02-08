import os
from datetime import datetime
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy

# Configuration
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')

# Database Configuration
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'data', 'jobs.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Ensure data directory exists
os.makedirs('data', exist_ok=True)

# Database Setup
db = SQLAlchemy(app)

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    company = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    job_type = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    requirements = db.Column(db.Text, nullable=False)
    salary_range = db.Column(db.String(100), nullable=False)
    how_to_apply = db.Column(db.Text, nullable=False)
    posted_date = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'company': self.company,
            'location': self.location,
            'job_type': self.job_type,
            'salary_range': self.salary_range,
            'posted_date': self.posted_date.isoformat()
        }

# Seeding Logic
def seed_database():
    if Job.query.first() is None:
        jobs_data = [
            {
                "title": "Senior Python Developer",
                "company": "TechStream Solutions",
                "location": "Remote",
                "job_type": "Full-time",
                "description": "We are looking for an experienced Python developer to lead our backend team. You will be responsible for architecting scalable solutions and mentoring junior developers.",
                "requirements": "- 5+ years of Python experience\n- Experience with Flask or Django\n- Knowledge of SQL and NoSQL databases\n- Strong problem-solving skills",
                "salary_range": "$120k - $160k",
                "how_to_apply": "Send your resume and GitHub profile to careers@techstream.example.com"
            },
            {
                "title": "DevOps Engineer",
                "company": "CloudScale Inc.",
                "location": "San Francisco, CA",
                "job_type": "Full-time",
                "description": "Join our infrastructure team to build and maintain our cloud-native platform. You'll work with Kubernetes, Docker, and AWS.",
                "requirements": "- 3+ years in DevOps\n- Strong Linux administration skills\n- Experience with CI/CD pipelines\n- AWS certification is a plus",
                "salary_range": "$130k - $170k",
                "how_to_apply": "Apply via our portal at cloudscale.example.com/careers"
            },
            {
                "title": "Marketing Manager",
                "company": "GrowthX Agency",
                "location": "New York, NY",
                "job_type": "Contract",
                "description": "We need a creative Marketing Manager to drive our new campaign. You will oversee social media, content strategy, and paid ads.",
                "requirements": "- Proven experience in digital marketing\n- Excellent communication skills\n- Data-driven mindset",
                "salary_range": "$50 - $70 / hr",
                "how_to_apply": "Email hello@growthx.example.com with your portfolio."
            },
            {
                "title": "Frontend Developer (React)",
                "company": "PixelPerfect",
                "location": "Austin, TX",
                "job_type": "Full-time",
                "description": "Craft beautiful user interfaces for our flagship product. You will work closely with designers and backend engineers.",
                "requirements": "- Expert in React.js and CSS\n- Familiarity with TypeScript\n- Eye for design detail",
                "salary_range": "$100k - $130k",
                "how_to_apply": "Send your resume to jobs@pixelperfect.example.com"
            },
            {
                "title": "Data Scientist",
                "company": "DataMind Analytics",
                "location": "Boston, MA",
                "job_type": "Full-time",
                "description": "Analyze large datasets to derive actionable insights for our clients. Machine learning and statistical modeling expertise required.",
                "requirements": "- MS/PhD in Computer Science or Statistics\n- Proficiency in Python/R and SQL\n- Experience with ML frameworks",
                "salary_range": "$140k - $180k",
                "how_to_apply": "Submit your application at datamind.example.com"
            },
            {
                "title": "Technical Writer",
                "company": "DocuSoft",
                "location": "Remote",
                "job_type": "Part-time",
                "description": "Help us improve our developer documentation. You will write API guides, tutorials, and release notes.",
                "requirements": "- Strong technical writing background\n- Ability to understand code\n- Experience with Markdown and Git",
                "salary_range": "$40 - $60 / hr",
                "how_to_apply": "Email docs@docusoft.example.com"
            },
            {
                "title": "Product Manager",
                "company": "InnovateNow",
                "location": "Seattle, WA",
                "job_type": "Full-time",
                "description": "Lead the product vision from conception to launch. You will define the roadmap and prioritize features based on user feedback.",
                "requirements": "- 4+ years of Product Management experience\n- Experience in Agile environments\n- Strong analytical skills",
                "salary_range": "$135k - $165k",
                "how_to_apply": "Apply on LinkedIn or email hr@innovatenow.example.com"
            },
            {
                "title": "Customer Success Specialist",
                "company": "HappyUser",
                "location": "Denver, CO",
                "job_type": "Full-time",
                "description": "Ensure our customers get the most value out of our product. You will handle onboarding, support queries, and renewals.",
                "requirements": "- Excellent interpersonal skills\n- Problem-solving attitude\n- Previous experience in SaaS support",
                "salary_range": "$60k - $80k",
                "how_to_apply": "Send a cover letter and resume to support-jobs@happyuser.example.com"
            },
            {
                "title": "UX/UI Designer",
                "company": "CreativeFlow",
                "location": "Los Angeles, CA",
                "job_type": "Contract",
                "description": "Design intuitive and engaging user experiences for mobile and web apps. Figma proficiency is a must.",
                "requirements": "- Strong portfolio showcasing UX/UI work\n- Proficiency in Figma and Adobe Suite\n- Understanding of user research",
                "salary_range": "$80 - $120 / hr",
                "how_to_apply": "Portfolio link to design@creativeflow.example.com"
            },
            {
                "title": "Golang Engineer",
                "company": "FastTrack Systems",
                "location": "Remote",
                "job_type": "Full-time",
                "description": "Build high-performance microservices in Go. You'll be working on a high-throughput transaction processing system.",
                "requirements": "- Strong experience with Go\n- Experience with gRPC and Protocol Buffers\n- Knowledge of distributed systems",
                "salary_range": "$140k - $175k",
                "how_to_apply": "Email careers@fasttrack.example.com"
            },
            {
                "title": "QA Automation Engineer",
                "company": "BugFree Zone",
                "location": "Chicago, IL",
                "job_type": "Full-time",
                "description": "Design and implement automated test scripts. You will ensure the quality of our releases.",
                "requirements": "- Experience with Selenium or Cypress\n- Python or Java scripting skills\n- CI/CD integration experience",
                "salary_range": "$90k - $120k",
                "how_to_apply": "Apply at bugfree.example.com/jobs"
            },
            {
                "title": "Junior Web Developer",
                "company": "StartUp Hub",
                "location": "Remote",
                "job_type": "Part-time",
                "description": "Great opportunity for a junior developer to learn and grow. You'll assist with website maintenance and minor feature updates.",
                "requirements": "- Basic knowledge of HTML, CSS, and JS\n- Eagerness to learn\n- Good communication skills",
                "salary_range": "$25 - $35 / hr",
                "how_to_apply": "Send your resume to intern@startuphub.example.com"
            }
        ]

        for job_data in jobs_data:
            job = Job(**job_data)
            db.session.add(job)
        
        db.session.commit()
        print(f"Seeded {len(jobs_data)} jobs.")

# Decorator for admin required
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('is_admin'):
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Routes
@app.route('/')
def index():
    query = request.args.get('q')
    job_type = request.args.get('type')
    
    jobs_query = Job.query
    
    if query:
        search = f"%{query}%"
        jobs_query = jobs_query.filter(
            (Job.title.ilike(search)) | (Job.company.ilike(search))
        )
    
    if job_type and job_type in ['Full-time', 'Part-time', 'Contract', 'Remote']:
        jobs_query = jobs_query.filter_by(job_type=job_type)
    
    # Sort by newest first
    jobs = jobs_query.order_by(Job.posted_date.desc()).all()
    
    return render_template('index.html', jobs=jobs)

@app.route('/job/<int:job_id>')
def job_detail(job_id):
    job = Job.query.get_or_404(job_id)
    return render_template('detail.html', job=job)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == 'admin' and password == 'admin123':
            session['is_admin'] = True
            flash('Logged in successfully.', 'success')
            return redirect(url_for('post_job'))
        else:
            flash('Invalid credentials.', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('is_admin', None)
    flash('Logged out successfully.', 'success')
    return redirect(url_for('index'))

@app.route('/admin/post', methods=['GET', 'POST'])
@login_required
def post_job():
    if request.method == 'POST':
        try:
            new_job = Job(
                title=request.form['title'],
                company=request.form['company'],
                location=request.form['location'],
                job_type=request.form['job_type'],
                description=request.form['description'],
                requirements=request.form['requirements'],
                salary_range=request.form['salary_range'],
                how_to_apply=request.form['how_to_apply']
            )
            db.session.add(new_job)
            db.session.commit()
            flash('Job posted successfully!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error posting job: {str(e)}', 'error')

    return render_template('post_job.html')

@app.route('/health')
def health():
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        seed_database()
    
    # Running on 0.0.0.0:8000 as requested
    app.run(host='0.0.0.0', port=8000, debug=False)

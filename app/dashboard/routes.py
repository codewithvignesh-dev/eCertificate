from flask import render_template
from flask_login import login_required
from ..extensions import db
from ..models import CertificateBatch
from . import dashboard

@dashboard.get("/")
@login_required
def index():
    total_certificates=db.fetchone("SELECT COUNT(*) AS count FROM certificates")["count"]
    total_batches=db.fetchone("SELECT COUNT(*) AS count FROM certificate_batches")["count"]
    total_colleges=db.fetchone("SELECT COUNT(*) AS count FROM colleges")["count"]
    generated_certificates=db.fetchone("SELECT COUNT(*) AS count FROM certificates WHERE status='generated'")["count"]
    failed_certificates=db.fetchone("SELECT COUNT(*) AS count FROM certificates WHERE status='failed'")["count"]
    active_colleges=db.fetchone("SELECT COUNT(*) AS count FROM colleges WHERE is_active=1")["count"]
    college_stats = db.fetchall("SELECT college_name, COUNT(*) AS certificate_count FROM certificates WHERE college_name IS NOT NULL AND college_name != '' GROUP BY college_name ORDER BY certificate_count DESC LIMIT 10")
    recent_batches=[CertificateBatch.from_row(r) for r in db.fetchall("SELECT * FROM certificate_batches ORDER BY created_at DESC LIMIT 10")]
    return render_template("dashboard/index.html",total_certificates=total_certificates,total_batches=total_batches,total_colleges=total_colleges,generated_certificates=generated_certificates,failed_certificates=failed_certificates,active_colleges=active_colleges,college_stats=college_stats,recent_batches=recent_batches)

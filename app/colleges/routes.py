from flask import flash, redirect, render_template, request, url_for
from flask_login import login_required
from ..extensions import db
from ..models import College
from ..utils.decorators import manager_required
from . import colleges

def row(r): return College.from_row(r)

@colleges.get("/")
@login_required
@manager_required
def index():
    search=request.args.get("search","").strip()
    if search:
        p=f"%{search}%"
        rows=db.fetchall("SELECT c.*,COUNT(cert.id) AS certificate_count FROM colleges c LEFT JOIN certificates cert ON cert.college_id=c.id WHERE c.name LIKE %s OR c.code LIKE %s OR c.city LIKE %s OR c.district LIKE %s OR c.state LIKE %s GROUP BY c.id ORDER BY c.name ASC",(p,p,p,p,p))
    else:
        rows=db.fetchall("SELECT c.*,COUNT(cert.id) AS certificate_count FROM colleges c LEFT JOIN certificates cert ON cert.college_id=c.id GROUP BY c.id ORDER BY c.name ASC")
    return render_template("colleges/index.html",colleges=[row(r) for r in rows],search=search)

@colleges.post("/create")
@login_required
@manager_required
def create():
    name=request.form.get("name","").strip()
    code=request.form.get("code","").strip() or None
    email=request.form.get("email","").strip() or None
    phone=request.form.get("phone","").strip() or None
    address=request.form.get("address","").strip() or None
    city=request.form.get("city","").strip() or None
    district=request.form.get("district","").strip() or None
    state=request.form.get("state","").strip() or None
    if not name:
        flash("College name is required.","danger"); return redirect(url_for("colleges.index"))
    if code and db.fetchone("SELECT id FROM colleges WHERE code=%s LIMIT 1",(code,)):
        flash("College code already exists.","danger"); return redirect(url_for("colleges.index"))
    db.execute("INSERT INTO colleges (name,code,email,phone,address,city,district,state,is_active) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,1)",(name,code,email,phone,address,city,district,state))
    flash("College created successfully.","success")
    return redirect(url_for("colleges.index"))

@colleges.post("/toggle/<int:college_id>")
@login_required
@manager_required
def toggle(college_id):
    college=row(db.fetchone("SELECT * FROM colleges WHERE id=%s LIMIT 1",(college_id,)))
    if not college: return render_template("errors/404.html"),404
    db.execute("UPDATE colleges SET is_active=IF(is_active=1,0,1) WHERE id=%s",(college_id,))
    flash("College status updated successfully.","success")
    return redirect(url_for("colleges.index"))

@colleges.post("/delete/<int:college_id>")
@login_required
@manager_required
def delete(college_id):
    college=row(db.fetchone("SELECT * FROM colleges WHERE id=%s LIMIT 1",(college_id,)))
    if not college: return render_template("errors/404.html"),404
    count=db.fetchone("SELECT COUNT(*) AS count FROM certificates WHERE college_id=%s",(college_id,))["count"]
    if count>0:
        flash("College cannot be deleted because certificates are associated with it.","warning")
        return redirect(url_for("colleges.index"))
    db.execute("DELETE FROM colleges WHERE id=%s",(college_id,))
    flash("College deleted successfully.","success")
    return redirect(url_for("colleges.index"))

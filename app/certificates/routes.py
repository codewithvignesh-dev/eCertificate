import io
import secrets
from pathlib import Path
import pandas as pd
from flask import current_app, flash, redirect, render_template, request, send_file, url_for
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
from ..extensions import db
from ..models import Certificate, CertificateBatch
from ..utils.decorators import staff_required
from . import certificates
from .forms import CertificateGenerationForm
from .generator import generate_certificate_number, generate_pdf, generate_public_token
from .services import get_temp_path, get_upload_path, read_certificate_file, read_certificate_file_from_path, save_temp_upload

def batch_from_row(row):
    return CertificateBatch.from_row(row) if row else None

def certificate_from_row(row):
    return Certificate.from_row(row) if row else None

@certificates.route("/generate",methods=["GET","POST"])
@login_required
@staff_required
def generate():
    form=CertificateGenerationForm()
    if form.validate_on_submit():
        uploaded_file=form.file.data
        try: dataframe=read_certificate_file(uploaded_file)
        except ValueError as exc:
            flash(str(exc),"danger"); return render_template("certificates/generate.html",form=form)
        temp_name=save_temp_upload(uploaded_file)
        return render_template("certificates/preview.html",form=form,records=dataframe.head(3).to_dict("records"),total_records=len(dataframe),valid_records=len(dataframe),title=form.title.data,description=form.description.data,temp_name=temp_name,original_filename=uploaded_file.filename)
    return render_template("certificates/generate.html",form=form)

@certificates.post("/generate/process")
@login_required
@staff_required
def process_generation():
    temp_name=request.form.get("temp_name","").strip()
    original_filename=request.form.get("original_filename","").strip()
    title=request.form.get("title","").strip()
    description=request.form.get("description","").strip()
    if not temp_name or not original_filename or not title or not description:
        flash("File, title and description are required.","danger"); return redirect(url_for("certificates.generate"))
    try: temp_path=get_temp_path(temp_name)
    except ValueError:
        flash("Your upload session has expired. Please upload the file again.","danger"); return redirect(url_for("certificates.generate"))
    if not temp_path.is_file():
        flash("Your upload session has expired. Please upload the file again.","danger"); return redirect(url_for("certificates.generate"))
    try: dataframe=read_certificate_file_from_path(temp_path,original_filename)
    except ValueError as exc:
        flash(str(exc),"danger"); temp_path.unlink(missing_ok=True); return redirect(url_for("certificates.generate"))
    upload_path=get_upload_path(original_filename)
    try: upload_path.write_bytes(temp_path.read_bytes())
    finally: temp_path.unlink(missing_ok=True)
    batch_id=db.execute("INSERT INTO certificate_batches (user_id,title,description,source_filename,total_records,valid_records,status) VALUES (%s,%s,%s,%s,%s,%s,'processing')",(current_user.id,title,description,original_filename,len(dataframe),len(dataframe)))
    generated=failed=0
    for record in dataframe.to_dict("records"):
        name=str(record["name"]).strip()
        college_name=str(record["college_name"]).strip()
        certificate_id=None
        try:
            college=db.fetchone("SELECT * FROM colleges WHERE LOWER(name)=LOWER(%s) LIMIT 1",(college_name,))
            if college: college_id=college["id"]
            else: college_id=db.execute("INSERT INTO colleges (name,is_active) VALUES (%s,1)",(college_name,))
            token=generate_public_token()
            certificate_id=db.execute("INSERT INTO certificates (batch_id,college_id,recipient_name,college_name,certificate_number,public_token,status) VALUES (%s,%s,%s,%s,'TEMP',%s,'pending')",(batch_id,college_id,name,college_name,token))
            certificate_number=generate_certificate_number(certificate_id)
            user_folder=Path(current_app.config["GENERATED_FOLDER"])/str(current_user.id)
            user_folder.mkdir(parents=True,exist_ok=True)
            pdf_filename=f"{secrets.token_hex(16)}.pdf"
            full_pdf_path=user_folder/pdf_filename
            generate_pdf(title=title,description=description,name=name,college_name=college_name,certificate_number=certificate_number,output_path=full_pdf_path)
            pdf_path=str(Path(str(current_user.id))/pdf_filename)
            db.execute("UPDATE certificates SET certificate_number=%s,pdf_filename=%s,pdf_path=%s,status='generated' WHERE id=%s",(certificate_number,pdf_filename,pdf_path,certificate_id))
            generated+=1
        except Exception:
            failed+=1
            if certificate_id:
                db.execute("UPDATE certificates SET status='failed' WHERE id=%s",(certificate_id,))
    status="completed" if failed==0 else "completed_with_errors"
    db.execute("UPDATE certificate_batches SET generated_records=%s,failed_records=%s,status=%s,completed_at=NOW() WHERE id=%s",(generated,failed,status,batch_id))
    flash(f"{generated} certificates generated successfully.","success" if failed==0 else "warning")
    return redirect(url_for("certificates.generated",batch_id=batch_id))

def can_access_batch(batch):
    return batch and (current_user.is_admin or batch.user_id==current_user.id)

@certificates.get("/generated/<int:batch_id>")
@login_required
@staff_required
def generated(batch_id):
    batch=batch_from_row(db.fetchone("SELECT * FROM certificate_batches WHERE id=%s LIMIT 1",(batch_id,)))
    if not batch: return render_template("errors/404.html"),404
    if not can_access_batch(batch): return render_template("errors/403.html"),403
    rows=db.fetchall("SELECT * FROM certificates WHERE batch_id=%s ORDER BY id ASC",(batch.id,))
    return render_template("certificates/generated.html",batch=batch,certificates=[certificate_from_row(r) for r in rows])

@certificates.get("/export/<int:batch_id>/<export_format>")
@login_required
@staff_required
def export(batch_id,export_format):
    batch=batch_from_row(db.fetchone("SELECT * FROM certificate_batches WHERE id=%s LIMIT 1",(batch_id,)))
    if not batch: return render_template("errors/404.html"),404
    if not can_access_batch(batch): return render_template("errors/403.html"),403
    if export_format not in {"xlsx","csv"}:
        flash("Invalid export format.","danger"); return redirect(url_for("certificates.generated",batch_id=batch.id))
    certificates_list=[certificate_from_row(r) for r in db.fetchall("SELECT * FROM certificates WHERE batch_id=%s ORDER BY id ASC",(batch.id,))]
    rows=[{"Name":c.recipient_name,"College Name":c.college_name,"Certificate Number":c.certificate_number,"Status":c.status,"Certificate Link":url_for("certificates.public_certificate",token=c.public_token,_external=True) if c.status=="generated" else ""} for c in certificates_list]
    dataframe=pd.DataFrame(rows,columns=["Name","College Name","Certificate Number","Status","Certificate Link"])
    buffer=io.BytesIO(); safe_title=secure_filename(batch.title) or "certificates"
    if export_format=="csv":
        buffer.write(dataframe.to_csv(index=False).encode("utf-8-sig")); mimetype="text/csv"
    else:
        with pd.ExcelWriter(buffer,engine="openpyxl") as writer: dataframe.to_excel(writer,index=False,sheet_name="Certificates")
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    buffer.seek(0)
    return send_file(buffer,as_attachment=True,download_name=f"{safe_title}_certificates.{export_format}",mimetype=mimetype)

def get_certificate(certificate_id):
    row=db.fetchone("SELECT c.*,b.user_id AS batch_user_id FROM certificates c JOIN certificate_batches b ON b.id=c.batch_id WHERE c.id=%s LIMIT 1",(certificate_id,))
    if not row: return None
    c=certificate_from_row(row); c.batch_user_id=row["batch_user_id"]; return c

@certificates.get("/download/<int:certificate_id>")
@login_required
@staff_required
def download(certificate_id):
    certificate=get_certificate(certificate_id)
    if not certificate: return render_template("errors/404.html"),404
    if not current_user.is_admin and certificate.batch_user_id!=current_user.id: return render_template("errors/403.html"),403
    if certificate.status!="generated" or not certificate.pdf_path:
        flash("Certificate PDF is not available.","danger"); return redirect(url_for("certificates.generated",batch_id=certificate.batch_id))
    pdf_path=(Path(current_app.config["GENERATED_FOLDER"])/certificate.pdf_path).resolve()
    generated_folder=Path(current_app.config["GENERATED_FOLDER"]).resolve()
    if generated_folder!=pdf_path and generated_folder not in pdf_path.parents:
        flash("Invalid certificate file.","danger"); return redirect(url_for("certificates.generated",batch_id=certificate.batch_id))
    if not pdf_path.is_file():
        flash("Certificate PDF file was not found.","danger"); return redirect(url_for("certificates.generated",batch_id=certificate.batch_id))
    return send_file(pdf_path,as_attachment=True,download_name=f"{certificate.certificate_number}.pdf",mimetype="application/pdf")

def public_certificate_lookup(token):
    return certificate_from_row(db.fetchone("SELECT * FROM certificates WHERE public_token=%s AND status='generated' LIMIT 1",(token,)))

def safe_pdf(certificate,download):
    if not certificate or not certificate.pdf_path: return render_template("errors/404.html"),404
    pdf_path=(Path(current_app.config["GENERATED_FOLDER"])/certificate.pdf_path).resolve()
    root=Path(current_app.config["GENERATED_FOLDER"]).resolve()
    if root!=pdf_path and root not in pdf_path.parents: return render_template("errors/404.html"),404
    if not pdf_path.is_file(): return render_template("errors/404.html"),404
    return send_file(pdf_path,as_attachment=download,download_name=f"{certificate.certificate_number}.pdf",mimetype="application/pdf")

@certificates.get("/public/<token>")
def public_certificate(token):
    certificate=public_certificate_lookup(token)
    if not certificate: return render_template("errors/404.html"),404
    return render_template("certificates/public.html",certificate=certificate)

@certificates.get("/public/<token>/pdf")
def public_pdf(token):
    return safe_pdf(public_certificate_lookup(token),False)

@certificates.get("/public/<token>/download")
def public_download(token):
    return safe_pdf(public_certificate_lookup(token),True)

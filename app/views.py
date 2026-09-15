from datetime import datetime
from django.shortcuts import render, redirect
from django.db import connection
from .models import Patient, MedicalService, Worker, Appointment, Order


def _auth(req):
    return "patient_id" in req.session


def login_view(request):
    if request.method == "POST":
        l = request.POST.get("login", "").strip()
        p = request.POST.get("password", "").strip()
        try:
            pat = Patient.objects.get(login=l, password=p)
            request.session["patient_id"] = pat.id
            return redirect("home")
        except Patient.DoesNotExist:
            return render(
                request, "app/login.html", {"error": "Неверный логин или пароль"}
            )
    return render(request, "app/login.html")


def logout_view(request):
    request.session.flush()
    return redirect("login")


def register_view(request):
    if request.method == "POST":
        fio = request.POST.get("fio", "").strip().split()
        lname = fio[0] if len(fio) > 0 else ""
        fname = fio[1] if len(fio) > 1 else ""
        mname = fio[2] if len(fio) > 2 else None
        Patient.objects.create(
            lname=lname,
            fname=fname,
            mname=mname,
            adress=request.POST.get("adress", ""),
            phone=request.POST.get("phone", "")[:12],
            email=request.POST.get("email", ""),
            dateofbirth=request.POST.get("dateofbirth"),
            idgender_id=int(request.POST.get("gender", 1)),
            login=request.POST.get("login"),
            password=request.POST.get("password"),
        )
        return redirect("login")
    return render(request, "app/register.html")


def home_view(request):
    if not _auth(request):
        return redirect("login")
    return render(request, "app/home.html")


def upcoming_view(request):
    if not _auth(request):
        return redirect("login")
    pid = request.session["patient_id"]
    with connection.cursor() as cur:
        cur.execute(
            """
            SELECT a.DataService, m.TitleService, w.LName, w.FName, w.MName
            FROM [Order] o
            JOIN Appointment a     ON a.Id = o.IdAppoinment
            JOIN MedicalService m  ON m.Id = a.IdMedicalService
            JOIN Worker w          ON w.Id = a.IdWorker
            WHERE o.IdPatient = %s AND a.DataService >= GETDATE()
            ORDER BY a.DataService
        """,
            [pid],
        )
        rows = cur.fetchall()
    return render(request, "app/upcoming.html", {"rows": rows})


def me_view(request):
    if not _auth(request):
        return redirect("login")
    p = Patient.objects.select_related("idgender").get(id=request.session["patient_id"])
    return render(request, "app/me.html", {"p": p})


def me_edit_view(request):
    if not _auth(request):
        return redirect("login")
    pid = request.session["patient_id"]
    if request.method == "POST":
        Patient.objects.filter(id=pid).update(
            lname=request.POST.get("lname", ""),
            fname=request.POST.get("fname", ""),
            mname=request.POST.get("mname") or None,
            phone=request.POST.get("phone", "")[:12],
            adress=request.POST.get("adress", ""),
            email=request.POST.get("email", ""),
            idgender_id=int(request.POST.get("gender", 1)),
        )
        return redirect("me")
    p = Patient.objects.get(id=pid)
    return render(request, "app/me_edit.html", {"p": p})


def history_view(request):
    if not _auth(request):
        return redirect("login")
    pid = request.session["patient_id"]
    with connection.cursor() as cur:
        cur.execute(
            """
            SELECT a.DataService, m.TitleService, w.LName, w.FName, w.MName,
                   ISNULL((
                       SELECT STRING_AGG(d.DiagnosisName, ', ')
                       FROM PatientDiagnosis pd
                       JOIN Diagnosis d ON d.Id = pd.IdDiagnosis
                       WHERE pd.IdPatient = o.IdPatient
                   ), '-') AS Diag
            FROM [Order] o
            JOIN Appointment a     ON a.Id = o.IdAppoinment
            JOIN MedicalService m  ON m.Id = a.IdMedicalService
            JOIN Worker w          ON w.Id = a.IdWorker
            WHERE o.IdPatient = %s AND a.DataService < GETDATE()
            ORDER BY a.DataService DESC
        """,
            [pid],
        )
        rows = cur.fetchall()
    return render(request, "app/history.html", {"rows": rows})


def book_view(request):
    if not _auth(request):
        return redirect("login")
    pid = request.session["patient_id"]
    services = MedicalService.objects.all()
    if request.method == "POST":
        svc = MedicalService.objects.get(id=request.POST["service_id"])
        dt = datetime.fromisoformat(request.POST["datetime"])
        worker = Worker.objects.first()
        apt = Appointment.objects.create(
            idworker_id=worker.id,
            idmedicalservice_id=svc.id,
            dataservice=dt,
        )
        Order.objects.create(
            idappoinment_id=apt.id,
            idpatient_id=pid,
            totalprice=svc.cost,
        )
        return redirect("home")
    return render(request, "app/book.html", {"services": services})

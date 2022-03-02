from django.shortcuts import render
import requests, json, urllib3

# Create your views here.
def hello(request):
    return render(request,'index.html')

def sessions(request):
    return render(request,'session.html')

def connect(request):
    global server
    server = request.POST['serverurl']
    urllib3.disable_warnings()
    url = "https://" + server + "/api/v1/sessions"
    headers = {
    'accept': "application/json",
    'content-type': "application/json"
    }
    data = {'username': 'bigid', 'password': 'Bigid@111'}
    response = requests.post(url, headers=headers, json=data, verify=False)
    output = response.json()
    global token
    token = output['auth_token']
    return render(request,'result.html', {'server':response, 'token':output['auth_token']})

def profileid(request):
    urllib3.disable_warnings()
    url = "https://" + server + "/api/v1/sar/profiles"
    headers = {
    'accept': "application/json",
    'content-type': "application/json",
    'Authorization': token
    }
    response = requests.get(url, headers=headers, verify=False)
    output = response.json()
    mydict = {'newprofiles': []}
    for x in output['profiles']:
        i = 0
        mydict['newprofiles'].insert(i, {'profid': x.pop('_id'), 'profname': x.pop('name')})
        i += 1
        print(mydict)

    return render(request,'profile.html', {'profileid':mydict['newprofiles']})

def search(request):
    state = ""
    global profid
    profid = request.POST['profid']
    return render(request,'search.html', {'output':state})

def datauser(request):
    data = request.POST['searchtext']
    urllib3.disable_warnings()
    url = "https://" + server + "/api/v1/sar/search/entity-sources"
    headers = {
    'accept': "application/json",
    'content-type': "application/json",
    'Authorization': token
    }
    checktxt = data.isalpha()
    if bool(checktxt) == True:
        queryparam = {'userName': data}
    else:
        queryparam = {'userId': data}

    response = requests.get(url, headers=headers, params=queryparam, verify=False)
    result = response.json()
    item = result['usersArray']

    if result['usersArray'] == []:
        result = "Not Found"
        return render(request,'search.html', {'output':result})
    else:
        return render(request,'search.html', {'output':item})

def rundsar(request):
    uid = request.POST['uid']
    nm = request.POST['dname']
    urllib3.disable_warnings()
    url = "https://" + server + "/api/v1/sar/reports"
    headers = {
    'accept': "application/json",
    'content-type': "application/json",
    'Authorization': token
    }
    data = {'userDetails':{'userId': uid, 'displayName': nm}}
    queryparam = {'userId': uid, 'displayName': nm, 'profileId': profid}
    response = requests.post(url, headers=headers, params=queryparam, json=data, verify=False)
    result = response.json()
    global reqid
    reqid = result["requestId"]
    return render(request,'rundsar.html', {'output':result})

def viewreports(request):
    reqid = request.GET['reqid']
    typeOpt = request.GET['typeOpt']
    urllib3.disable_warnings()
    #url = "https://" + server + "/api/v1/sar/reports/" + reqid + "/short-report"
    url = "https://" + server + "/api/v1/sar/reports/" + reqid
    if typeOpt == "CSV":
        headers = {
        'accept': "text/csv",
        'content-type': "text/csv",
        'Authorization': token
        }
        querystring = {'format':'csv'}
        response = requests.get(url, headers=headers, params=querystring, verify=False)
        return render(request,'report.html', {'output':response.text})
    else:
        headers = {
        'accept': "application/json",
        'content-type': "application/json",
        'Authorization': token
        }
        response = requests.get(url, headers=headers, verify=False)
        result = response.json()
        return render(request,'report.html', {'output':result})

def scanhistory(request):
    urllib3.disable_warnings()
    url = "https://" + server + "/api/v1/sar/scans"
    headers = {
    'accept': "application/json",
    'content-type': "application/json",
    'Authorization': token
    }
    response = requests.get(url, headers=headers, verify=False)
    result = response.json()
    items = result["scans"]
    print(type(items))
    return render(request,'scanhistory.html', {'output':items})

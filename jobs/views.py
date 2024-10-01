from django.contrib.auth import authenticate, login, logout
import json
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.http import JsonResponse
from django.urls import reverse
from django.core.serializers import serialize
from django.core.paginator import Paginator
from .models import *
from decimal import Decimal


# Create your views here.

def index(request):
    if(request.user.is_authenticated):
        return render(request, "jobs/index.html")
    else:
        return HttpResponseRedirect(reverse("login"))

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "jobs/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "jobs/login.html")


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "jobs/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "jobs/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "jobs/register.html")

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

@login_required
@csrf_exempt
def new_post(request):
    if (request.method=='POST'):
        owner= request.user
        title= request.POST["title"]
        description= request.POST["description"]
        max_participants= request.POST["max_participants"]
        price= request.POST["price"]
        
    
        
        if int(max_participants) <= 0:
            return render(request,"jobs/new_post.html",{
                "message":"the amount of participants must be greater than 0!"
            })
        
        new_job= Job(owner=owner,title=title,description=description,max_participants=max_participants,price=price)
        
        # we decrement the balance of the user 
        owner.wallet.balance -= Decimal(max_participants)*Decimal(price)
        new_job.save()
        owner.wallet.save()

        return HttpResponseRedirect(reverse("my_jobs"))

    
    else:
        return render(request,"jobs/new_post.html")
    
@login_required
def jobs(request):
    return render(request,"jobs/jobs.html",{
        "owner_": ""
    })

@login_required
def job(request, job_id):
    job= Job.objects.get(pk=job_id)
    valid = job.max_participants > job.participants.count()
    job_done = request.user in job.participants.all()
    proofs= None
    if job.owner == request.user:
        proofs= job.proofs.filter(status= "no-status")
    
    return render(request, "jobs/job_details.html",{
      "job":job,
      "valid": valid,
      "job_done": job_done,
      "proofs":proofs
    })


@login_required
def jobsAPI(request, i=1):
    
    # we exluce the jobs of the owner, and exlude also when the user is a participant, don't worry django will handle participants=request.user 
    jobs_list = Job.objects.exclude(owner=request.user).exclude(participants=request.user)
    
    # we exluce jobs that have 0 remaining participants
    jobs_list = [job for job in jobs_list if job.max_participants > job.participants.count()]

    p = Paginator(jobs_list, 12)

    # check if out of range
    if i > p.num_pages:
        return JsonResponse({'jobs': []}, status=200) # if so return empty

    jobs_to_post = p.page(i)
    jobs_json = [job.serialize() for job in jobs_to_post]
    
    # Return the jobs in JSON format
    return JsonResponse({'jobs': jobs_json}, status=200)


@login_required
def owner_jobsAPI(request, i=1):
    
    # we exluce the jobs of the owner
    jobs_list = Job.objects.filter(owner=request.user)
    
    p = Paginator(jobs_list, 12)

    # check if out of range
    if i > p.num_pages:
        return JsonResponse({'jobs': []}, status=200) # if so return empty

    jobs_to_post = p.page(i)
    jobs_json = [job.serialize() for job in jobs_to_post]
    
    # Return the jobs in JSON format
    return JsonResponse({'jobs': jobs_json}, status=200)


@login_required
@csrf_exempt
def submit_proof(request, job_id):
    if request.method == 'POST':
        job = Job.objects.get(pk=job_id)
        user = request.user
        description = request.POST.get('proof_description')
        image = request.FILES.get('proof_image')

        # Create or update the proof
        if not Proof.objects.filter(job=job, owner=user).exists():
            proof= Proof(owner=user, job=job, description= description, image=image)
            proof.save()
            user.jobs_done.add(job)

        #else return a message saying that it's impossible to submit

    return HttpResponseRedirect(reverse('job', kwargs={'job_id': job_id}))

@login_required
def wallet(request):
    owner = request.user
    if not hasattr(owner, 'wallet'):  
        wallet = Wallet.objects.create(user=owner)

    pending= 0
    proofs= owner.proofs.filter(status="no-status")
    for proof in proofs:
        pending+= proof.job.price
    
    return render(request, "jobs/wallet.html", {"wallet": owner.wallet,
                                                "pending": pending,})
    
@login_required
@csrf_exempt
def change_stat(request, proof_id):
    try:
        proof = Proof.objects.get(pk=proof_id)
    except Proof.DoesNotExist:
        return JsonResponse({'error': 'Proof not found'}, status=404)
    
    if request.method == "PUT":
        try:
            data = json.loads(request.body)
            action = data.get('action')

            if action == 'approve':
                proof.status = 'approved'
                proof.owner.wallet.balance += Decimal(proof.job.price)
                proof.owner.wallet.save() 
                
            elif action == 'decline':
                proof.status = 'declined'
                proof.job.owner.wallet.balance += Decimal(proof.job.price)
                proof.job.owner.wallet.save()
            else:
                return JsonResponse({'error': 'Invalid action'}, status=400)

            proof.save()
            return JsonResponse({'message': 'Proof status updated successfully'})
        
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
@login_required
def my_jobs(request):
    return render(request,"jobs/jobs.html",{
        "owner_": "owner_"
    })
    
@login_required
def my_proofs(request):
    
    owner= request.user
    proofs= Proof.objects.filter(owner=owner)
    
    return render(request,"jobs/proofs_submited.html",{
        "proofs": proofs
    })
    
@login_required
def profile(request, user_id):
    user = User.objects.get(pk=user_id)

    jobs_published_count = Job.objects.filter(owner=user).count()

    jobs_approved_count = Proof.objects.filter(owner=user, status='approved').count()
    jobs_declined_count = Proof.objects.filter(owner=user, status='declined').count()
    jobs_pending_count = Proof.objects.filter(owner=user, status='no-status').count()

    wallet_balance = user.wallet.balance if hasattr(user, 'wallet') else 0

    return render(request, "jobs/profile.html", {
        "user_profile": user,
        "jobs_published_count": jobs_published_count,
        "jobs_approved_count": jobs_approved_count,
        "jobs_declined_count": jobs_declined_count,
        "jobs_pending_count": jobs_pending_count,
        "wallet_balance": wallet_balance
    })
    
    
@login_required
def deposit(request):
    if request.method == 'POST':
        amount = Decimal(request.POST.get('amount', '0'))  # Ensure '0' is a string for Decimal conversion
        if amount > 0:
            wallet = Wallet.objects.get(user=request.user)
            wallet.balance += amount
            wallet.save()
        return HttpResponseRedirect(reverse('wallet'))

@login_required
def withdrawal(request):
    if request.method == 'POST':
        amount = Decimal(request.POST.get('amount', '0'))  # Ensure '0' is a string for Decimal conversion
        wallet = Wallet.objects.get(user=request.user)
        if amount > 0 and amount <= wallet.balance:
            wallet.balance -= amount
            wallet.save()
        return HttpResponseRedirect(reverse('wallet'))
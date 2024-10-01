from django.urls import path
from . import views

urlpatterns = [
	path("", views.index , name="index"),
	path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
	path("register", views.register, name="register"),
	path("new_post", views.new_post, name="new_post"),
	path("jobs", views.jobs , name="jobs"),
	path("jobs/<int:job_id>", views.job , name="job"),
	path("jobsAPI/<int:i>",views.jobsAPI, name="jobsAPI"),
	path("owner_jobsAPI/<int:i>",views.owner_jobsAPI, name="jobsAPI"),
 	path('submit-proof/<int:job_id>/', views.submit_proof, name='submit_proof'),
	path("wallet", views.wallet , name="wallet"),
	path("jobs/<int:proof_id>/change_stat",views.change_stat, name="change_stat"),
	path("my_jobs", views.my_jobs , name="my_jobs"),
	path("my_proofs", views.my_proofs , name="my_proofs"),
	path("profile/<int:user_id>", views.profile , name="profile"),
    path('deposit/', views.deposit, name='deposit'),
    path('withdrawal/', views.withdrawal, name='withdrawal'),
]
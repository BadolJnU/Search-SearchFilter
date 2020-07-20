from django.shortcuts import render, HttpResponse, redirect
from blog.models import Post
from rest_framework.generics import ListAPIView
from home.models import SearchHistory
from home.serializers import SearchSerializers
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
import datetime
from django.http import JsonResponse
import json

# Create your views here.

def home(request):
   return render(request, 'Home/home.html')

def about(request):
   return render(request, 'Home/about.html')


def handleSignup(request):
   if request.method == 'POST':
      username = request.POST['username']
      fname = request.POST['fname']
      lname = request.POST['lname']
      email = request.POST['email']
      Password1 = request.POST['Password1']
      Password2= request.POST['Password2']

      #error check
      if len(username) > 10:
         messages.error(request,"Username must be under ten characters")
         return redirect('/')
      if not username.isalnum():
         messages.error(request,"Username should only contains character and numbers")
         return redirect('/')
      if Password1 != Password2:
         messages.error(request,"Password does not match")
         return redirect('/')

      #create user
      myuser = User.objects.create_user(username, email, Password1)
      myuser.first_name = fname
      myuser.last_name = lname
      myuser.save()
      messages.success(request,"Your account has been successfully created")
      return redirect('/')

   else:
      return HttpResponse('404 error')

def handleLogin(request):
   if request.method == 'POST':
      loginusername = request.POST['loginusername']
      loginpassword = request.POST['loginpassword']

      user = authenticate(username=loginusername, password=loginpassword)

      if user is not None:
         login(request,user)
         messages.success(request,'you are logged in')
         return redirect('/')
      else:
         messages.error(request,'invalid username or password, please log in')
         return redirect('/')
def handleLogout(request):
   logout(request)
   messages.success(request,'you are logged out')
   return redirect('/')

def search(request):
   query = request.GET['query']
   if len(query)>78:
      allPosts = Post.objects.none()
   else:
      allPoststitle = Post.objects.filter(title__icontains=query)
      allPostsauthor = Post.objects.filter(author__icontains=query)
      allPostscontent = Post.objects.filter(content__icontains=query)
      allPosts = allPoststitle.union(allPostsauthor,allPostscontent)
      keyword = query
      loginuser = request.user
      x = datetime.datetime.now()
      searchdate = x.strftime("%Y-%m-%d")
      if allPosts.count() > 0:
            b = SearchHistory(keyword=query, loginuser=loginuser, searchdate=searchdate, searchresult='Yes')
            b.save()
      else:
         b = SearchHistory(keyword=query, loginuser=loginuser, searchdate=searchdate, searchresult='No')
         b.save()
         messages.error(request, "No search result found, please search again")
   params = {'allPosts':allPosts, 'query':query}
   return render(request, 'Home/search.html', params)







def searchHistory(request):
   return render(request, 'Home/SearchHistory.html',{})

class HomeListing(ListAPIView):
    # set the pagination and serializer class

	#pagination_class = StandardResultsSetPagination
	serializer_class = SearchSerializers


	def get_queryset(self):
        # filter the queryset based on the filters applied

		queryList = SearchHistory.objects.all()
		loginuser = self.request.query_params.get('loginuser', None)
		keyword = self.request.query_params.get('keyword', None)
		startdate = self.request.query_params.get('startdate', None)
		enddate = self.request.query_params.get('enddate', None)
		sort_by = self.request.query_params.get('sort_by', None)
      
		
		if loginuser:
		   queryList = queryList.filter(loginuser = loginuser)
		if keyword:
		   queryList = queryList.filter(keyword = keyword)
		if startdate:
		   queryList = queryList.filter(searchdate__gte = startdate)
		if enddate:
		   queryList = queryList.filter(searchdate__lte = enddate)
      # sort it if applied on based on price/points

		if sort_by == "loginuser":
		    queryList = queryList.order_by("loginuser")
		elif sort_by == "keyword":
		    queryList = queryList.order_by("keyword")
		elif sort_by == "searchdate":
		    queryList = queryList.order_by("searchdate")
		return queryList

def getLoginuser(request):
   if request.method == "GET" and request.is_ajax():
      user = SearchHistory.objects.exclude(loginuser__isnull=True).\
         exclude(loginuser__exact='').order_by('loginuser').values_list('loginuser').distinct()
      user = [i[0] for i in list(user)]
      data = {
         "loginuser":user,
      }
      return JsonResponse(data, status = 200)

def getKeyword(request):
   if request.method == "GET" and request.is_ajax():
      loginuser = request.GET.get('loginuser')
      keyword = SearchHistory.objects.filter(loginuser=loginuser).\
         exclude(keyword__isnull=True).exclude(keyword__exact='').\
            order_by('keyword').values_list('keyword').distinct()
      keyword = [i[0] for i in list(keyword)]
      data = {
         "keyword":keyword,
      }
      return JsonResponse(data, status = 200)



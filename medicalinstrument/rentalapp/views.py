from django.shortcuts import render
from django.template import loader
from django.template import context
from django.shortcuts import redirect
from django.views import View
from .forms import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
import json
from django.contrib.auth import logout
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views.decorators.http import require_POST







def homepage(request):
    if 'user' in request.session:
        current_user=request.session['user']
        context={'current_user':current_user}
        return render(request,'homepage.html',context)
    
    return render(request,'homepage.html')



def contact(request):
      
      current_user = None
      if 'user' in request.session:
        current_user=request.session['user']
      context={'current_user':current_user}
     
      return render(request,'contact_us.html',context)



def logout_page(request):
        try:
            del request.session['user']
        except: 
            return redirect('home')   
        return redirect('home')



def navbar(request):
    return render(request,'navbar.html')
def index(request):
     
    products=Product.objects.filter(status=0)
    query = request.GET.get('query')
    current_user = None
    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
    if 'user' in request.session:
        current_user=request.session['user']
    context = {
        'products': products,
        'query': query,
        'current_user':current_user
    }
    
    return render(request,'index.html',context)   



 
def products(request):
    products = Product.objects.all()  
    query = request.GET.get('query')

    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
    
    context = {
        'products': products,
        'query': query
    }
    return render(request, 'products.html', context)   

    

def collections(request):
    category=Category.objects.filter(status=0)
    query = request.GET.get('query')
    current_user=None


    if 'user' in request.session:
        current_user=request.session['user']
       
    if query:

        category=category.filter(
           Q(name__icontains=query) | Q(description__icontains=query)
            )
    context={'category':category,'query':query,'current_user':current_user}
    return render(request,'collections.html',context)





# ===============  SERVICES VIEWS ========================

def nursing_services(request):

    current_user = None
    if 'user' in request.session:
        current_user=request.session['user']
    context={'current_user':current_user}
     
    return render(request,'services/nursing_services.html',context)

def health(request):
    current_user = None
    if 'user' in request.session:
        current_user=request.session['user']
    context={'current_user':current_user}
     
    return render(request,'services/health.html',context)

def equipments(request):
    current_user = None
    if 'user' in request.session:
        current_user=request.session['user']
    context={'current_user':current_user}
     
    return render(request,'services/medical_equipments.html',context)


# =============== REGISTER & LOGIN VIEWS ========================

def register(request):
        
     if request.method=="POST": 
        name=request.POST['Username']
        pwd=request.POST['password']
        dateofbirth=request.POST.get('dob')
        mno=request.POST.get('mobno')
        email=request.POST.get('email')
        gender=request.POST.get('gender')
        addr=request.POST.get('address')
        img=request.FILES.get('image')
        
        account =Register(username=name,userid=email,password=pwd,dob=dateofbirth,mobile_number= mno,gender=gender,address=addr,photo=img)
        account.save()
        messages.success(request,"Registration Success You Can Login Now..!")
        return  redirect('login')
     else:
        
        return render(request,'register/register.html')


def login_page(request):
    
        if request.method=="POST":
                userid=request.POST.get('email')
                pwd=request.POST.get('password')
                
                check_user=Register.objects.filter(userid=userid,password=pwd)
                if check_user:
                    request.session['user']=userid
                    return redirect('home')
                else:
                    return HttpResponse('Please enter valid userid or password')

        return render(request,'register/login_page.html')    
          







#===========  Cart,Rent,Order views =================== 

# def Rent_products(request):
    
#     products=Product.objects.filter(status=0)
#     current_user = None
#     if 'user' in request.session:
#         current_user=request.session['user']
   
   
#     return render(request,'CRB/Rent_products.html',{'products':products,'current_user':current_user})   




def add_to_cart(request, productid):
    current_user = None
    

    if 'user' in request.session:
        current_user = request.session['user']
        current_user = get_object_or_404(Register, userid=current_user)
    
    
    product = get_object_or_404(Product, id=productid)
    
    
    cart, created = Cart1.objects.get_or_create(user=current_user)
    

    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    
    if not item_created:
        
        cart_item.save()
        messages.success(request, "Product added to cart successfully.")
        return redirect('cart') 
    
    
    return render(request, 'CRB/addtocart.html', {'products': products, 'current_user': current_user})

def add_to_rent(request):
    products=Product.objects.filter(status=0)
    if request.method == "POST":
        pid=request.POST.get('product_id')
        pqty=request.POST.get('product_qty')
        uid=request.POST.get('email')
        sd=request.POST.get('stdt')
        rd=request.POST.get('rtdt')
        td=request.POST.get('tdays')
        ta=request.POST.get('tamnt')

        product_id=Product.objects.get(product_id=pid)
        user_id=Register.objects.get(userid=uid)

        rentacc=Rental(product=product_id, product_qty= pqty,user=user_id,start_date=sd,return_date=rd ,total_days=td,total_amount=ta)
        rentacc.save()
        messages.success(request,"You have Rented the product successfully")
        return redirect('rented')
    return render(request,'CRB/addtorent.html',{'products':products})
 


def add_to_buy(request):
    products=Product.objects.filter(status=0)
    current_user = None
    if 'user' in request.session:
        current_user=request.session['user']
   
    if request.method == "POST":
        pid=request.POST.get('product_id')
        pqty=request.POST.get('product_qty')
        uid=request.POST.get('email')
        od=request.POST.get('ordt')
        amnt=request.POST.get('amnt')

        product_id=Product.objects.get(product_id=pid)
        user_id=Register.objects.get(userid=uid)

        buyacc=Order(product=product_id, product_qty= pqty,user=user_id,order_date=od,amount=amnt)
        buyacc.save()
        messages.success(request,"You have Ordered the product successfully")
        return redirect('ordered')
    return render(request,'CRB/addtobuy.html',{'products':products,'current_user':current_user})

#=========== Display of Cart,Rent,Order  views =================== 




        



def Cart_display(request):
    current_user = None
    
    if 'user' in request.session:
        current_userid = request.session['user']
        
        current_user = get_object_or_404(Register, userid=current_userid)
    cart, created = Cart1.objects.get_or_create(user=current_user)
    cart_items = CartItem.objects.filter(cart=cart)
    query = request.GET.get('query')
    if query:
        cart_items = cart_items.filter(
            Q(product_id=query) | Q(product_qty=query)
        )
    context = {
        'cart_items': cart_items,
        'query': query,
        'current_user': current_user,
    }
    return render(request, 'CRB display/cart.html', context)

    
    





def Rented_display(request):
    current_user = None
    if 'user' in request.session:
        current_user=request.session['user']
    rent_items=Rental.objects.all()
    context={'rent_items':rent_items,'current_user':current_user}
    return render(request,'CRB display/Rented.html',context)







def Ordered_display(request):
    current_user = None
    if 'user' in request.session:
        current_user=request.session['user']
    ordered_items=Order.objects.all()
    context={'ordered_items':ordered_items,'current_user':current_user}
    return render(request,'CRB display/ordered.html',context)

# ==========================================================================================
















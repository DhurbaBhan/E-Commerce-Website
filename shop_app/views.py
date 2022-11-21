from django.shortcuts import render,redirect
from django.views import View
from django.contrib import auth
from django.contrib.auth.models import User
from shop_app.models import Product,Cart,Customer,OrderPlaced
from shop_app.forms import CustomerRegistrationForm ,CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


# def home(request):
#  return render(request, 'app/home.html')
class ProductView(View):
    def get(self,request):
        topwears=Product.objects.filter(category='TW')
        bottomwears=Product.objects.filter(category='BW')
        mobiles=Product.objects.filter(category='M')
        context={'topwears':topwears,'bottomwears':bottomwears,'mobiles':mobiles}

        return render(request, 'app/home.html',context)



class ProductDetailView(View):
    def get(self,request,pk):
        product=Product.objects.get(id=pk)
        cart_already=False
        if request.user.is_authenticated:
            cart_already=Cart.objects.filter(Q(user=request.user) & Q(product=product)).exists()
            return render(request, 'app/productdetail.html',{'product':product,'cart_already':cart_already})
        else:
            return render(request,'app/productdetail.html',{'product':product})

@login_required
def add_to_cart(request):
    user=request.user
    product_id=request.GET.get('prod_id')
    product=Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect("showcart")

@login_required
def show_cart(request):
    user=request.user
    carts=Cart.objects.filter(user=user)
    amount=0.0
    shipping_amount=100
    total_amount=0.0
    cart_products=list(carts)
    if cart_products:
        for p in cart_products:
            temp_amount=p.quantity*p.product.discounted_price
            amount+=temp_amount
        total_amount=amount+shipping_amount    
        return render(request,"app/showcart.html",{'carts':carts,'total_amount':total_amount,'amount':amount,'shipping_amount':shipping_amount})
    else:
        return render(request,'app/emptycart.html')

def plus_cart(request):
    prod_id=request.GET['prod_id']
    c=Cart.objects.get(Q(user=request.user) & Q(product=prod_id))        
    c.quantity+=1
    c.save()
    amount=0.0
    shipping_amount=100
    total_amount=0.0
    carts=Cart.objects.filter(user=request.user)
    for p in list(carts):
        temp_amount=p.quantity*p.product.discounted_price
        amount+=temp_amount
    total_amount=amount+shipping_amount 
    data={'quantity':c.quantity,
    'total_amount':total_amount,
    'amount':amount,
    'shipping_amount':shipping_amount}   
    return JsonResponse(data)

def minus_cart(request):
    prod_id=request.GET['prod_id']
    c=Cart.objects.get(Q(user=request.user) & Q(product=prod_id))        
    c.quantity-=1
    c.save()
    amount=0.0
    shipping_amount=100
    total_amount=0.0
    carts=Cart.objects.filter(user=request.user)
    for p in list(carts):
        temp_amount=p.quantity*p.product.discounted_price
        amount+=temp_amount
    total_amount=amount+shipping_amount 
    data={'quantity':c.quantity,
    'total_amount':total_amount,
    'amount':amount,
    'shipping_amount':shipping_amount}   
    return JsonResponse(data)    

def remove_cart(request):
    prod_id=request.GET['prod_id']
    c=Cart.objects.get(Q(user=request.user) & Q(product=prod_id))        
    c.delete()
    amount=0.0
    shipping_amount=100
    total_amount=0.0
    carts=Cart.objects.filter(user=request.user)
    for p in carts:
        temp_amount=p.quantity*p.product.discounted_price
        amount+=temp_amount
    total_amount=amount+shipping_amount 
    data={
    'total_amount':total_amount,
    'amount':amount,
    'shipping_amount':shipping_amount}   
    return JsonResponse(data)     


@method_decorator(login_required,name='dispatch')
class address(View):
    def get(self,request):
        addr=Customer.objects.filter(user=self.request.user)
        return render(request, 'app/address.html',{'addr':addr,'active':'btn-primary'})
@login_required
def orders(request):
    op=OrderPlaced.objects.filter(user=request.user)

    return render(request, 'app/orders.html',{'orders':op})


def mobile(request,data=None):
    if data==None:
        mobiles=Product.objects.filter(category='M')
    elif data=='Redmi' or data=='Samsung' or data=='Apple':
        mobiles=Product.objects.filter(category="M").filter(brand=data)
    elif data=="below":
        mobiles=Product.objects.filter(category="M").filter(discounted_price__lt=50000)        
    elif data=="above":
        mobiles=Product.objects.filter(category="M").filter(discounted_price__gt=50000)    
    return render(request, 'app/mobile.html',{'mobiles':mobiles})

def fashion(request,data):
    if data=="tw":
        products=Product.objects.filter(category="TW")
    elif data=="bw":
        products=Product.objects.filter(category="BW")
    return render(request,'app/fashion.html',{'products':products})    


class CustomerRegistrationView(View):
    def get(self,request):
        form=CustomerRegistrationForm()
        return render (request,'app/customerregistration.html',{'form':form})
    def post(self,request):
        form=CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Account Registered Successfully.")
        return render(request,'app/customerregistration.html',{'form':form})    
    # form=CustomerRegistrationForm
    # if request.method=='POST': 
    #     obj=User()
    #     obj.full_name=request.POST.get('full_name')
    #     obj.email=request.POST.get('email')
    #     obj.password=request.POST.get('password')
    #     obj.save()
    #     return render(request,'app/customerregistration.html',{'form':form,'msg':'Account Registered Successfully..'})
    # else:
    #     return render(request,'app/customerregistration.html',{'form':form})      
  
# def profile(request):
#     if request.method=="POST":
#         form=CustomerProfileForm(request.POST)
#         if form.is_valid(): 
#             form.save()
#             messages.success(request,"Congratulations, Profile Updated Successfully.")
#         return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})   
#         # return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})
#     else:
#         form=CustomerProfileForm()
#         return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})   
@method_decorator(login_required,name='dispatch')      
class ProfileView(View):
    def get(self,request):
        form=CustomerProfileForm()
        return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})  
    
    def post(self,request):
        customer = Customer()
        customer.user = request.user
        customer.name= request.POST.get('name')
        customer.locality=request.POST.get('locality')
        customer.city=request.POST.get('city')
        customer.state=request.POST.get('state')
        customer.zipcode=request.POST.get('zipcode')
        customer.save()
        form=CustomerProfileForm()
        # if form.is_valid():            
            # usr=request.user
            # name=form.cleaned_data['name']
            # locality=form.cleaned_data['locality']
            # city=form.cleaned_data['city']
            # state=form.cleaned_data['state']
            # zipcode=form.cleaned_data['zipcode']
            # obj=Customer(user=usr,name=name,locality=locality,city=city,state=state,zipcode=zipcode)
            # obj.save()
        messages.success(request,"Congratulations, Profile Updated Successfully.")
        return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})   
@login_required
def checkout(request):
    user=request.user
    addrs=Customer.objects.filter(user=user)
    carts=Cart.objects.filter(user=user)
    amount=0.0
    shipping_amount=100
    total_amount=0.0
    
    for cart in carts:
        temp_amount=cart.quantity*cart.product.discounted_price
        amount+=temp_amount
    total_amount=amount+shipping_amount

    context={
        'addrs':addrs,
        'carts':carts,
        'total_amount':total_amount
    }
    return render(request, 'app/checkout.html',context)
@login_required    
def payment_done(request):
        user=request.user
        custid=request.GET.get('custid')
        print(custid)
        customer=Customer.objects.get(id=custid)
        cart=Cart.objects.filter(user=user)
        for c in cart:
            OrderPlaced(user=user,customer=customer,product=c.product,quantity=c.quantity).save()
            c.delete()
        return redirect("orders")    

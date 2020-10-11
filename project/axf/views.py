from django.shortcuts import render,redirect
from .models import Wheel,Nav,FoodTypes,Goods,User,Cart
from .forms.login import LoginForm
from django.http import HttpResponse,JsonResponse
from django.conf import settings
from django.contrib.auth import logout
import time,random,os
# Create your views here.
def home(request):
    wheelsList =Wheel.objects.all()
    navList =Nav.objects.all()
    return render(request,'axf/home.html',{"title":"主页",'wheelsList':wheelsList,
                                           'navList':navList})
def market(request,categoryid,cid,sortid):
    leftSlider = FoodTypes.objects.all()
    if cid == '0':
        productList = Goods.objects.filter(categoryid=categoryid)
    else:
        productList = Goods.objects.filter(categoryid=categoryid,childcid=cid)
    group = leftSlider.get(typeid=categoryid)
    childList = []
    content = group.childtypenames.split("#")
    for i in content:
        arr=i.split(":")
        obj = {"childName":arr[0],"childId":arr[1]}
        childList.append(obj)
    cartList = []
    token = request.session.get('token')
    if token :
        user = User.objects.get(userToken=token)
        cartList = Cart.objects.get(userAccount=user.userAccount)
    if sortid == "1":
        productList = productList.order_by("productnum")
    return render(request,'axf/market.html',{"title":"超市",'leftSlider':leftSlider
        ,'productList':productList,"childList":childList,"categoryid":categoryid,'cid':cid
                                             ,"cartList":cartList})
def cart(request):
    cartList = []
    token = request.session.get('token')
    if token:
        user = User.objects.get(userToken=token)
        cartList = Cart.objects.get(userAccount=user.userAccount)
    return render(request,'axf/cart.html',{"title":"购物车"})
def mine(request):
    username = request.session.get('userName')
    return render(request,'axf/mine.html',{"title":"我的",'username':username})
def login(request):
    print("333 %s"%request.method)
    if request.method == 'POST':
        print(11111)
        f = LoginForm(request.POST)
        if f.is_valid():
            print(222222222222)
            name = f.cleaned_data['username']
            passwd = f.cleaned_data['passwd']
            user = User.objects.get(userAccount=name)

            print("******%s"%user)
            try:
                if user.userPasswd != passwd:
                    return redirect('/login/')
            except User.DoesNotExist as e :
                return redirect('/login/')
            token = time.time() + random.randrange(1, 10000)
            user.userToken = str(token)
            user.save()
            request.session['userName'] = user.userName
            request.session['token'] = user.userToken
            return redirect('/mine/')
        else:
            return render(request, 'axf/login.html', {"title": "登录","form":f,"error":f.errors})
    else:
        f=LoginForm()
        return render(request,'axf/login.html',{"title":"登录","form":f})

def register(request):
    if request.method == 'POST':
        userAccount = request.POST.get("userAccount")
        userPasswd = request.POST.get("userPasswd")
        userName = request.POST.get("userName")
        userPhone = request.POST.get("userPhone")
        userAddress = request.POST.get("userAddress")
        userRank =0
        token = time.time()+random.randrange(1,10000)
        userToken = str(token)
        f= request.FILES['userImg']
        userImg = os.path.join(settings.MDEIA_ROOT,userAccount+'.png')
        with open(userImg,'wb') as fp:
            for data in f.chunks():
                fp.write(data)
        user = User.creatuser(userAccount,userPasswd,userName,userPhone,userAddress,
                              userImg,userRank,userToken)
        user.save()
        request.session['userName']=userName
        request.session['token']=userToken

        return  redirect("/mine/")
    return render(request,'axf/register.html',{"title":'注册'})

def checkuserid(request):
    userid = request.POST.get("userid")
    try:
        user = User.objects.get(userAccount=userid)
        return JsonResponse({"data":"用户被注册","status":"error"})
    except User.DoesNotExist as e:
        return JsonResponse({"data":"成功","status":"success"})
def quit(request):
    logout(request)
    return redirect("/mine/")

def changecart(request,flag):
    token =request.session.get("token")
    if token == None:
        return JsonResponse({"data":-1,"status":"error"})
    productid = request.POST.get("productid")
    product = Goods.objects.get(productid=productid)
    user = User.objects.get(userToken=token)
    if flag == "0":
        if product.storenums == 0:
            return JsonResponse({"data":-2,"status":"error"})
        carts = Cart.objects.filter(userAccount=user.userAccount)
        if carts.count() == 0:
           c=Cart.creatcart(user.userAccount,productid,1,product.price,True,product
                            .productimg,product.productlongname,False)
           c.save()
        else:
            try:
                c = Cart.objects.get(productid=productid)
                c.productnum+=1
                c.productprice = c.productnum*float(product.price)
                c.save()
            except Cart.DoesNotExist :
                c = Cart.creatcart(user.userAccount, productid, 1, product.price, True, product
                                   .productimg, product.productlongname, False)
                c.save()
            product.storenums-=1
            product.save()
            return JsonResponse({"data":c.productnum,"status":"success"})
    else:
        pass
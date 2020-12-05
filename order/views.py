from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.utils.crypto import get_random_string

from order.models import ShopCart, ShopCartForm, OrderForm, Order, OrderProduct
from product.models import Category, Product, Variants
from user.models import UserProfile


def index(request):
    return HttpResponse ("Order Page")


def addtoshopcart(request,id):

    url = request.META.get('HTTP_REFERER')  # get last url
    product= Product.objects.get(pk=id)
    product_variant = product.variant


    if product_variant != 'None':
        variantid = request.POST.get('variantid')  # from variant add to cart
        if request.user.is_authenticated:
            checkinvariant = ShopCart.objects.filter(variant_id=variantid, user_id=request.user.id)  # Check product in shopcart
            
        else:
            # checkinvariant = ShopCart.objects.filter(variant_id=variantid, session_id=request.session.session_key)  # Check product in shopcart
            checkinvariant = ShopCart.objects.filter(session_id=request.session.session_key)  # Check product in shopcart
        if checkinvariant:
            control = 1 # The product is in the cart
            print("checkinvariant")
        else:
            control = 0 # The product is not in the cart"""
    else:
        if request.user.is_authenticated:
            checkinproduct = ShopCart.objects.filter(product_id=id, user_id=request.user.id) # Check product in shopcart
        else:
            checkinproduct = ShopCart.objects.filter(product_id=id, session_id=request.session.session_key) # Check product in shopcart    
        if checkinproduct:
            control = 1 # The product is in the cart
            print("checkinproduct")
        else:
            control = 0 # The product is not in the cart"""

    if request.method == 'POST':  # if there is a post
        print('Adding item to cart!')
        form = ShopCartForm(request.POST)
        if form.is_valid():
            if control==1: # Update  shopcart
                if product.variant == 'None':
                    print('block without variant and update')
                    if request.user.is_authenticated:
                        data = ShopCart.objects.get(product_id=id, user_id=request.user.id)
                        data.quantity += form.cleaned_data['quantity']
                        data.save()
                    else:
                        data = ShopCart.objects.get(product_id=id, session_id=request.session.session_key)
                        data.quantity += form.cleaned_data['quantity']
                        data.save()
                else:
                    print('block with variant and update')
                    if request.user.is_authenticated:
                        try:
                            data = ShopCart.objects.get(product_id=id, user_id=request.user.id)
                            data.quantity += form.cleaned_data['quantity']
                            data.save()
                        except:
                            variantid = ""
                            data = ShopCart()
                            if request.user.is_authenticated:
                                data.user_id = request.user.id
                            data.product_id =id
                            if variantid:
                                data.variant_id = variantid
                            data.quantity = form.cleaned_data['quantity']
                            data.session_id = request.session.session_key
                            data.save()    
                    else:
                        try:
                            data = ShopCart.objects.get(product_id=id, session_id=request.session.session_key)
                            data.quantity += form.cleaned_data['quantity']
                            data.save()
                        except:
                            variantid = ""
                            data = ShopCart()
                            if request.user.is_authenticated:
                                data.user_id = request.user.id
                            data.product_id =id
                            if variantid:
                                data.variant_id = variantid
                            data.quantity = form.cleaned_data['quantity']
                            print("Quantity id " + str(form.cleaned_data['quantity']))
                            data.session_id = request.session.session_key
                            data.save()
            else : # Inser to Shopcart
                print("block create")
                variantid = ""
                data = ShopCart()
                if request.user.is_authenticated:
                    data.user_id = request.user.id
                data.product_id =id
                if variantid:
                    data.variant_id = variantid
                data.quantity = form.cleaned_data['quantity']
                data.session_id = request.session.session_key
                data.save()
        messages.success(request, "Product added to Shopcart ")
        return HttpResponseRedirect(url)

    else: # if there is no post
        if control == 1:  # Update  shopcart
            print("block with update and no post")
            try:
                print("block with update and no post")
                data = ShopCart.objects.get(product_id=id, user_id=request.user.id)
                data.quantity += 1
                data.save()
            except:
                data = ShopCart()  # model ile bağlantı kur
                if request.user.is_authenticated:
                    data.user_id = request.user.id
                data.product_id = id
                data.quantity = 1
                data.variant_id =None
                data.session_id = request.session.session_key
                data.quantity += 1
                data.save()  #
        else:  #  Inser to Shopcart
            print("block without update and no post")
            data = ShopCart()  # model ile bağlantı kur
            if request.user.is_authenticated:
                data.user_id = request.user.id
            data.product_id = id
            data.quantity = form.cleaned_data['quantity']
            data.variant_id =None
            data.session_id = request.session.session_key
            data.save()
        messages.success(request, "Product added to Shopcart")
        return HttpResponseRedirect(url)


def shopcart(request):
    if request.user.is_authenticated:
        category = Category.objects.all()
        current_user = request.user  # Access User Session information
        shopcart = ShopCart.objects.filter(user_id=current_user.id)
        total=0
        for rs in shopcart:
            total += rs.product.price * rs.quantity
        context={'shopcart': shopcart, 'category':category, 'total': total}
    else:
        category = Category.objects.all()
        shopcart = ShopCart.objects.filter(session_id=request.session.session_key)
        total=0
        for rs in shopcart:
            total += rs.product.price * rs.quantity
        # context={'shopcart': shopcart, 'category':category, 'total': total}
    return render(request,'shopcart_products.html', {'shopcart': shopcart, 'category': category, 'total': total})   

@login_required(login_url='/login') # Check login
def deletefromcart(request,id):
    ShopCart.objects.filter(id=id).delete()
    messages.success(request, "Your item deleted form Shopcart.")
    return HttpResponseRedirect("/shopcart")


@login_required(login_url='/login') # Check login
def orderproduct(request):
    category = Category.objects.all()
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total = 0
    for rs in shopcart:
        if rs.product.variant == 'None':
            total += rs.product.price * rs.quantity
        else:
            # total += rs.variant.price * rs.quantity
            total += rs.product.price * rs.quantity

    if request.method == 'POST':  # if there is a post
        form = OrderForm(request.POST)
        #return HttpResponse(request.POST.items())
        if form.is_valid():
            # Send Credit card to bank,  If the bank responds ok, continue, if not, show the error
            # ..............

            data = Order()
            data.first_name = form.cleaned_data['first_name'] #get product quantity from form
            data.last_name = form.cleaned_data['last_name']
            data.address = form.cleaned_data['address']
            data.city = form.cleaned_data['city']
            data.phone = form.cleaned_data['phone']
            data.user_id = current_user.id
            data.total = total
            data.ip = request.META.get('REMOTE_ADDR')
            ordercode= get_random_string(5).upper() # random cod
            data.code =  ordercode
            data.save() #

            for rs in shopcart:
                detail = OrderProduct()
                detail.order_id     = data.id # Order Id
                detail.product_id   = rs.product_id
                detail.user_id      = current_user.id
                detail.quantity     = rs.quantity
                if rs.product.variant == 'None':
                    detail.price    = rs.product.price
                else:
                    # variant issue here
                    # detail.price = rs.variant.price
                    detail.price = rs.product.price
                detail.variant_id   = rs.variant_id
                detail.amount        = rs.amount
                detail.save()
                # ***Reduce quantity of sold product from Amount of Product
                if  rs.product.variant=='None':
                    product = Product.objects.get(id=rs.product_id)
                    product.amount -= rs.quantity
                    product.save()
                else:
                    variant = Variants.objects.get(id=rs.product_id)
                    variant.quantity -= rs.quantity
                    variant.save()
                #************ <> *****************

            ShopCart.objects.filter(user_id=current_user.id).delete() # Clear & Delete shopcart
            request.session['cart_items']=0
            messages.success(request, "Your Order has been completed. Thank you ")
            return render(request, 'Order_Completed.html',{'ordercode':ordercode,'category': category})
        else:
            messages.warning(request, form.errors)
            return HttpResponseRedirect("/order/orderproduct")

    form= OrderForm()
    profile = UserProfile.objects.get(user_id=current_user.id)
    context = {'shopcart': shopcart,
               'category': category,
               'total': total,
               'form': form,
               'profile': profile,
               }
    return render(request, 'Order_Form.html', context)
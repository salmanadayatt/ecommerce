from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from shop.models import Product
from cart.models import Cart, Order, Account


@login_required
def cart_view(request):
    u = request.user
    total = 0
    c = Cart.objects.filter(user=u)
    for i in c:
        total = total + i.quantity * i.product.price

    return render(request, 'cart.html', {'c': c, 'total': total})


@login_required
def addtocart(request, p):
    p = Product.objects.get(id=p)
    u = request.user
    try:
        cart = Cart.objects.get(user=u, product=p)
        if (p.stock > 0):
            cart.quantity += 1
            cart.save()
            p.stock -= 1
            p.save()
    except:

        cart = Cart.objects.create(product=p, user=u, quantity=1)
        cart.save()
        p.stock -= 1
        p.save()
    return cart_view(request)


def cart_remove(request, p):
    p = Product.objects.get(id=p)
    u = request.user
    try:
        cart = Cart.objects.get(product=p, user=u)
        if (cart.quantity > 1):
            cart.quantity -= 1
            cart.save()
            p.stock += 1
            p.save()
        else:
            cart.delete()
            p.stock += 1
            p.save()
    except:
        pass
    return cart_view(request)


def full_remove(request, p):
    p = Product.objects.get(id=p)
    u = request.user
    try:
        cart = Cart.objects.get(product=p, user=u)
        cart.delete()
        cart.stock += cart.quantity
        cart.save()
    except:
        pass
    return cart_view(request)


@login_required()
def order_form(request):
    if request.method == "POST":
        a = request.POST['a']
        p = request.POST['p']
        n = request.POST['n']

        u = request.user
        c = Cart.objects.filter(user=u)

        total = 0
        for i in c:
            total = total + i.quantity * i.product.price

        try:
            ac = Account.objects.get(acctnum=n)
            if ac.amount >= total:
                ac.amount = ac.amount - total
                ac.save()
                for i in c:
                    o = Order.objects.create(user=u, product=i.product, no_of_items=i.quantity, address=a, phone=p, order_status = "paid")
                    o.save()

                c.delete()
                msg = "Order Placed Successfully"
                return render(request, "orderdetails.html", {'message': msg})
            else:
                msg = "Insufficient Amount.You Can't Place Order"
                return render(request, "orderdetails.html", {'message': msg})
        except:
            pass

    return render(request, 'orderform.html',)
@login_required
def your_order(request):
    u=request.user
    o=Order.objects.filter(user=u)
    return render(request,'your_order.html',{'o':o,'u':u.username})

from django.shortcuts import render, redirect
from .models import Product, Category, Review
from django.contrib import messages

def product_list(request):
    categories = Category.objects.all()
    products = Product.objects.filter(category__id=categories[0].id)
    context = {'products':products, 'categories':categories}
    return render(request, 'homepage.html', context)

def product_list_category(request, category_id):
    user_query = str(request.GET.get('query', ''))
    categories = Category.objects.all()
    products = Product.objects.filter(category__id=category_id, name__icontains=user_query)
    if products.exists():
        context = {'products': products, 'categories': categories}
        return render(request, 'homepage.html', context)
    else:
        messages.info(request, 'Product not available!!')
        return render(request, 'homepage.html')

def product_detail(request, id):
    categories = Category.objects.all()
    product = Product.objects.get(id=id)
    reviews = product.reviews.all()
    context = {'product': product, 'categories': categories, 'reviews':reviews}
    return render(request, 'productdetail.html', context)


def review(request, product_id):
    if request.method == 'POST':
        data = {
            'user':request.user,
            'rating': int(request.POST.get('rating')),
            'comment': request.POST.get('comment'),

        }
        try:
            response = Review.objects.create(
                user=request.user,
                rating=data.get('rating'),
                comment=data.get('comment'),
                product=Product.objects.get(id=product_id),
            )
            print("added review")
            messages.success(request, "New Review added")
        except Exception as e:
            print(e)
            messages.warning(
                request, 'Got an error when trying to add a new Review')
    return redirect('products:product_detail', id=product_id)






from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views.generic import View
from products.models import Product
from .models import OrderProduct, Order, BillingAddress, Payment
from .forms import CheckoutForm
import stripe
from django.conf import settings


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            #order_products =  order.products.all()
            context = {'order':order}
            return render(self.request, 'order_summary.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order")
            return redirect('/')

@login_required
def add_to_cart(request, id):
    # get the particular product
    product = get_object_or_404(Product, id=id)
    # create or add the product to the order
    order_product, created = OrderProduct.objects.get_or_create(product=product, user=request.user, ordered=False)
    # add the order particular product to the Order which is not complete
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    # if the order exists
    if order_qs.exists():
        # grab the order
        order = order_qs[0]
        #checking if the order item is in the order
        if order.products.filter(product__id=product.id).exists():
            # if it exists increment the quantity by 1
            order_product.quantity += 1
            # and save
            order_product.save()
            messages.info(request, "This item quantity was updated")
            return redirect("orders:order_summary")
        # if not add the product to the order
        else:
            order.products.add(order_product)
            order.save()
            messages.info(request, "This item was added to your cart")
            #return redirect("orders:order_summary")
    else:
        ordered_date = timezone.now()
        # else create a new order
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        # and add the product
        order.products.add(order_product)
        messages.info(request, "This item was added to your cart")
    return redirect("products:product_detail", id=product.id)

@login_required
def remove_from_cart(request, id):
    # get the particular product
    product = get_object_or_404(Product, id=id)
    # get the order based on the condition that its not complete and it belongs to the particular user
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    # if it exist
    if order_qs.exists():
        # grab the order
        order = order_qs[0]
        # checking if the order products is in the order
        if order.products.filter(product__id=product.id).exists():
            # get the order product
            order_product = OrderProduct.objects.filter(product=product, user=request.user, ordered=False)[0]
            # and remove the product from the order
            order.products.remove(order_product)
            messages.info(request, "This item was removed from your cart")
            return redirect("products:product_detail", id=product.id)
        else:
            # and add a message saying the order products is not in the order
            messages.info(request, "This item was not in your cart")
            return redirect("products:product_detail", id=product.id)
    else:
        # if not redirect back to the details page
        # and add a message saying the user doesn't have an order
        messages.info(request, "You do not have an active order")
        return redirect("products:product_detail", id=product.id)

@login_required
def remove_single_product_from_cart(request, id):
    # get the particular product
    product = get_object_or_404(Product, id=id)
    # get the order based on the condition that its not complete and it belongs to the particular user
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    # if it exist
    if order_qs.exists():
        # grab the order
        order = order_qs[0]
        # checking if the order products is in the order
        if order.products.filter(product__id=product.id).exists():
            # get the order product
            order_product = OrderProduct.objects.filter(product=product, user=request.user, ordered=False)[0]
            if order_product.quantity > 1:
                # if it exists decrease the quantity by 1
                order_product.quantity -= 1
                # and save
                order_product.save()
            else:
                order.products.remove(order_product)
            messages.info(request, "This item was updated")
            return redirect("orders:order_summary")
        else:
            # and add a message saying the order products is not in the order
            messages.info(request, "This item was not in your cart")
            return redirect("products:product_detail", id=product.id)
    else:
        # if not redirect back to the details page
        # and add a message saying the user doesn't have an order
        messages.info(request, "You do not have an active order")
        return redirect("products:product_detail", id=product.id)


class CheckoutView(View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            form = CheckoutForm()
            context ={'form': form, 'order':order}
            return render(self.request, 'checkout.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, 'You do not have an active order')
            return redirect('orders:checkout')


    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                street_address = form.cleaned_data.get('street_address')
                apartment_address = form.cleaned_data.get('apartment_address')
                country = form.cleaned_data.get('country')
                zip = form.cleaned_data.get('zip')
                # TODO: add functionality for these fields
                #same_shipping_address = form.cleaned_data.get('same_shipping_address')
                #save_info = form.cleaned_data.get('save_info')
                payment_option = form.cleaned_data.get('payment_option')
                billing_address = BillingAddress(
                    user=self.request.user,
                    street_address=street_address,
                    apartment_address=apartment_address,
                    country=country,
                    zip=zip
                )
                billing_address.save()
                order.billing_address = billing_address
                order.save()
                if payment_option == 'S':
                    return redirect('orders:payment', payment_option='stripe')
                elif payment_option == 'P':
                    return redirect('orders:payment', payment_option='paypal')
                else:
                    messages.warning(self.request, 'Invalid payment option selected')
                    return redirect('orders:checkout')
            messages.warning(self.request, 'failed checkout')
            return redirect('orders:checkout')
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order")
            return redirect('orders:order_summary')

class PaymentView(View):
    def get(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        if order.billing_address:
            context = {'order':order}
            return render(self.request, "payment.html", context)
        else:
            messages.error(self.request, "You have not added a billing address")
            return redirect('orders:checkout')

    def post(self, *args, **kwargs):
        #keys = read_credentials()
        #stripe.api_key = keys["STRIPE_SECRET_KEY"]
        #stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.api_key = "sk_test_4eC39HqLyjWDarjtT1zdp7dc"

        print(stripe.api_key)
        order = Order.objects.get(user=self.request.user, ordered=False)
        amount = int(order.get_total() * 100)
        token = self.request.POST['stripeToken']
        print(token)
        try:
            charge = stripe.Charge.create(
                amount=amount,  # cents
                currency="usd",
                source=token
            )
            # Create Payment
            print("create payment")
            payment = Payment()
            payment.stripe_charge_id = charge['id']
            payment.user = self.request.user
            payment.amount = order.get_total()
            payment.save()

            # Assign payment to the order

            order_products = order.products.all()
            order_products.update(ordered=True)
            for product in order_products:
                product.save()

            order.ordered = True
            order.payment = payment
            order.save()
            messages.success(self.request, "Your Order was successful")
            #redirect to profile page or order success page
            return redirect("/")

        except stripe.error.CardError as e:
            messages.error(self.request, e.error.message)
            return redirect("/")

        except stripe.error.RateLimitError as e:
            messages.error(self.request, "Rate limit error")
            return redirect("/")
        except stripe.error.InvalidRequestError as e:
            messages.error(self.request, "Invalid parameters")
            return redirect("/")
        except stripe.error.AuthenticationError as e:
            messages.error(self.request, "Not authenticated")
            return redirect("/")
        except stripe.error.APIConnectionError as e:
            messages.error(self.request, "Network error")
            return redirect("/")
        except stripe.error.StripeError as e:
            messages.error(self.request, "Something went wrong, you were not charged, please try again")
            return redirect("/")
        except Exception as e:
            messages.error(self.request, "A serious error occurred we have been notified")
            return redirect("/")


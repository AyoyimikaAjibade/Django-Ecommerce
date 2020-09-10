from django.contrib import admin
from .models import OrderProduct, Order, Payment, Refund, Tracker

def make_refund_accepted(modeladmin, request, queryset):
    queryset.update(refund_requested=False, refund_granted=True)

make_refund_accepted.short_description = 'Update orders to refund granted'


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user',
                    'ordered',
                    'being_delivered',
                    'received',
                    'refund_requested',
                    'refund_granted',
                    'billing_address',
                    'payments',
                    ]
    list_filter = ['ordered',
                    'being_delivered',
                    'received',
                    'refund_requested',
                    'refund_granted'
                    ]
    list_display_links = ['user', 'billing_address', 'payments']
    search_fields = ['user__username', 'ref_code']
    actions = [make_refund_accepted]


admin.site.register(OrderProduct)
admin.site.register(Order, OrderAdmin)
admin.site.register(Payment)
admin.site.register(Refund)
admin.site.register(Tracker)

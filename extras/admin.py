from django.contrib import admin
from .models import Clients, InvoicesTypes, Invoices  # obtengo el modelo de clientes para mostrar en el admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter  # Filtra por rango de fechas
from django.db.models import Sum, Avg
from totalsum.admin import TotalsumAdmin

from django.utils.translation import ugettext, ugettext_lazy as _

@property
def is_staff(self):
    return self.staff

@property
def is_superuser(self):
    return self.superuser

class MyUserAdmin(admin.ModelAdmin):
    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets

        if request.user.is_superuser:
            perm_fields = ('is_active', 'is_staff', 'is_superuser',
                           'groups', 'user_permissions')
        else:
            # modify these to suit the fields you want your
            # staff user to be able to edit
            perm_fields = ('is_active',)


        print(request.user)

        return [(None, {'fields': ('username', 'password')}),
                (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
                (_('Permissions'), {'fields': perm_fields}),
                (_('Important dates'), {'fields': ('last_login', 'date_joined')})]


# Unregister the provided model admin
admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)

@admin.register(Clients)
class ClientsAdmin(admin.ModelAdmin):
    list_display = ['codigo_interno', 'razon_social', 'cuit_formateado']


@admin.register(InvoicesTypes)
class InvoicesTypesAdmin(admin.ModelAdmin):
    list_display = ['name', 'punto_venta']

#class InvoicesAdmin(admin.ModelAdmin):
@admin.register(Invoices)
class InvoicesAdmin(TotalsumAdmin):
    totalsum_list = ('amount',)
    unit_of_measure = '&#36;'

    normaluser_fields = ['date', 'client_id', 'invoice_type_id', 'invoice_number', 'amount']
    superuser_fields = ['user_id', 'state']

    actions = ['aprobar']
    def aprobar(self, request, queryset):
        queryset.update(state=True)

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


    def get_date(self, obj):
        return obj.date.strftime('%d/%m/%y')
    get_date.short_description = 'Fecha'

    def get_invoice_number(self, obj):
        i = obj.invoice_type_id.punto_venta
        return i + '-' + obj.invoice_number.zfill(8)
    get_invoice_number.short_description = 'Nro Comprobante'

    def get_invoice_type(self, obj):
        return obj.invoice_type_id.punto_venta

    def get_amount(self, obj):
        return '$ ' + str(obj.amount)
    get_amount.short_description = 'Monto'

    # Redefino la funcion que lista los campos segun los permisos
    def get_form(self, request, obj=None, **kwargs):
        if not request.user.is_superuser:
            self.fields = self.normaluser_fields
        else:
            self.fields = self.normaluser_fields + self.superuser_fields

        return super(InvoicesAdmin, self).get_form(request, obj, **kwargs)

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser and request.user.has_perm('invoices.state'):
            return [f.name for f in self.model._meta.fields]
        return super(InvoicesAdmin, self).get_readonly_fields(
            request, obj=obj
        )

    list_filter = (('date', DateRangeFilter),'state')
    list_display = ['get_date', 'get_invoice_number', 'client_id', 'amount','state']
    search_fields = ('invoice_number', 'date', 'client_id', 'invoice_type_id', 'amount')
    ordering = ('date', 'invoice_number')
    '''
    if User.is_superuser:
        print(User.username)
        list_display = ['get_date', 'get_invoice_number', 'client_id', 'amount', 'state']
        list_filter = (('date', DateRangeFilter), 'client_id', 'state')
        search_fields = ('invoice_number', 'date', 'client_id', 'invoice_type_id', 'amount', 'state')
        ordering = ('date', 'invoice_number', 'state')
    '''
    date_hierarchy = 'date'

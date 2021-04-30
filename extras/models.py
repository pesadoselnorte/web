from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError  # Validaciones de campos
from django.db.models import Sum # Suma registros de un queryset

def validar_cuit(cuit):
    # validaciones minimas
    #if len(cuit) != 13 or cuit[2] != "-" or cuit[11] != "-": return False

    base = [5, 4, 3, 2, 7, 6, 5, 4, 3, 2]

    #cuit = cuit.replace("-", "")  # remuevo las barras

    # calculo el digito verificador:
    aux = 0
    for i in range(10):
        aux += int(cuit[i]) * base[i]

    aux = 11 - (aux - (int(aux / 11) * 11))

    if aux == 11:
        aux = 0
    if aux == 10:
        aux = 9

    return aux == int(cuit[10])

def only_int(value):
    if validar_cuit(value) == False:
        raise ValidationError('Ingresar un cuit válido')


class Clients(models.Model):  # Tabla de Clientes
    name = models.CharField(max_length=200, db_index=True, verbose_name='Nombre')
    internal_id = models.PositiveIntegerField(default=0, unique=True, verbose_name='Codigo interno')
    cuit = models.CharField(validators=[only_int], max_length=11, unique=True, verbose_name='CUIT')

    @property
    def codigo_interno(self):  # Formateo el nro de cliente con los ceros adelante
        return (self.internal_id.zfill(8))

    @property
    def razon_social(self):
        return (self.name.title())

    @property
    def cuit_formateado(self):
        cuit = int(self.cuit)
        if (cuit != 0):
            cuit = self.cuit[0:2]+'-'+self.cuit[2:10]+'-'+self.cuit[10:]
        else:
            cuit = 'No registra'
        return (cuit)

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        # self.internal_id = self.internal_id.
        return super(Clients, self).save(*args, **kwargs)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

    def __str__(self):
        return self.name


class InvoicesTypes(models.Model):  # Tipos de comprobantes
    name = models.CharField(max_length=200, db_index=True, verbose_name='Nombre')
    punto_venta = models.CharField(max_length=5, unique=True, verbose_name='Punto de Venta')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Tipo de Comprobante'
        verbose_name_plural = 'Tipos de Comprobante'

    def __str__(self):
        return self.name


class Invoices(models.Model):  # Tipos de comprobantes
    user_id = models.ForeignKey(User, default=2, verbose_name=('Usuario'), on_delete=models.PROTECT)
    date = models.DateField(blank=False, verbose_name='Fecha')  # , input_formats='%d/%m/%y')
    client_id = models.ForeignKey(Clients, on_delete=models.PROTECT, verbose_name='Cliente')
    invoice_type_id = models.ForeignKey(InvoicesTypes, on_delete=models.PROTECT, verbose_name='Tipo Comprobante')
    invoice_number = models.CharField(max_length=8, verbose_name='Nro Factura')
    amount = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name='Monto')
    state = models.BooleanField(default=False, verbose_name='Aprobado')

    class Meta:
        ordering = ('invoice_number',)
        verbose_name = 'Comprobante'
        verbose_name_plural = 'Comprobantes'
        permissions = (
            ('state', 'Solo lectura amiguito'),
        )

    def __str__(self):
        return self.invoice_number

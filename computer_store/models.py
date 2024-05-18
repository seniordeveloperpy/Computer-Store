from django.db import models
from random import sample
import string
from django.utils import timezone
from django.contrib.auth.models import User
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw


class CodeGenerate(models.Model):
    code = models.CharField(max_length=255, blank=True,unique=True)
    
    @staticmethod
    def generate_code():
        return ''.join(sample(string.ascii_letters + string.digits, 15)) 

    def save(self, *args, **kwargs):
        if not self.id:
            while True:
                code = self.generate_code()
                if not self.__class__.objects.filter(code=code).count():
                    self.code = code
                    break
        super(CodeGenerate,self).save(*args, **kwargs)

    class Meta:
        abstract = True


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(CodeGenerate):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    image = models.ImageField(upload_to='product/', blank=True, null=True)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        qrcode_img = qrcode.make(self.name)
        canvas = Image.new('RGB', (290, 290), 'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_img)
        fname = f'qr_code-{self.name}.png'
        buffer = BytesIO()
        canvas.save(buffer, 'PNG')
        self.qr_code.save(fname, File(buffer), save=False)
        canvas.close()
        super().save(*args, **kwargs)
    

class EnterProduct(CodeGenerate):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Enter {self.product.name} - {self.quantity}"
    
    def save(self, *args, **kwargs):
        if self.pk:
            object = EnterProduct.objects.get(id=self.id)
            self.product.quantity -= object.quantity
        
        self.product.quantity += self.quantity
        self.product.save()
        super(EnterProduct, self).save(*args, **kwargs)

    

class OutProduct(CodeGenerate):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Out {self.product.name} - {self.quantity}"
    
    def save(self, *args, **kwargs):
        if self.pk:
            object = OutProduct.objects.get(id=self.id)
            self.product.quantity += object.quantity

        self.product.quantity -= self.quantity
        self.product.save()
        super(OutProduct, self).save(*args, **kwargs)


class ReturnedProduct(CodeGenerate):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    out_product = models.ForeignKey(OutProduct, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    reason = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Returned {self.product.name} - {self.quantity}"

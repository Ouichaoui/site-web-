from django.db import models
from django.contrib.auth.models import User



class Userprofile(models.Model):
    user = models.OneToOneField(User,related_name='userprofile', on_delete=models.CASCADE)

User.userprofile = property(lambda u:Userprofile.objects.get_or_create(user=u)[0])

class Brand(models.Model):
    name = models.CharField(max_length=200, null=False)
    image = models.ImageField(null=False, blank=True)

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

    def __str__(self):
        return self.name

    @property
    def get_total(self):
        mark = Brand.objects.get(pk=self.id)
        products = mark.brand.all()
        total_brand = products.filter(brand=self.id).count()

        return total_brand


class Catalogue(models.Model):
    title = models.CharField(max_length=200, null=False)
    description = models.CharField(max_length=200)
    image =models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.title

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


    @property
    def get_total(self):
        mark = Catalogue.objects.get(pk=self.id)
        products = mark.catalog.all()
        total_cata = products.filter(catalog=self.id).count()

        return total_cata


#product Model

class Product(models.Model):
    by = models.ForeignKey('auth.user', on_delete=models.SET_NULL, null=True, blank=True, )
    name = models.CharField(max_length=200 , null=True)
    catalog = models.ForeignKey(Catalogue,null=True, blank=True,related_name='catalog',on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand,null=True, blank=True,related_name='brand',on_delete=models.CASCADE)
    price = models.FloatField()
    Product_details  = models.CharField(max_length=1000 , null=True)
    Téléphone = models.CharField(max_length=200 , null=True , blank=True)
    Addresse = models.CharField(max_length=200 , null=True , blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    image =models.ImageField(null=True, blank=True,upload_to='images/')

    def __str__(self):
        return self.name

    @property
    def imageURL (self):
        try:
            url = self.image.url
        except :
            url =''
        return url

















class Customer(models.Model):
    user = models.OneToOneField(User, null=True , blank=True , on_delete=models.CASCADE)
    name = models.CharField(max_length=200 , null=True )
    email = models.CharField( max_length=200)

    def __str__(self):
        return self.name







class Offre(models.Model):
    produit = models.ForeignKey(Product ,related_name='offre', on_delete=models.CASCADE,blank=True , null=True)
    created_by = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    Addresse = models.CharField(max_length=500,blank=True , null=True)
    Téléphone = models.CharField(max_length=10,blank=True , null=True)
    Prix_Proposé = models.IntegerField(blank=True , null=True)
    Message = models.CharField(max_length=500,blank=True , null=True)


    def __str__(self):
        return str(self.produit)


class ConversationMessage(models.Model):
    offer=models.ForeignKey(Offre,related_name='conversationmessages', on_delete=models.CASCADE)
    content = models.TextField()
    created_by = models.ForeignKey(User,related_name='conversationmessages', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['created_at']
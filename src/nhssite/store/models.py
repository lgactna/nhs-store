from django.db import models
from django.urls import reverse

# Create your models here.
class Product(models.Model):
    """Model representing a standard product.
    
    Relationships to others (a product can have many of these):
    - ProductImage (related_name = "images")
    - ProductInstance (related_name = "instances")
    - Materials (related_name = "materials")
    """
    id = models.AutoField(primary_key=True) #explicit so vs code knows what this is
    name = models.CharField(
        max_length=50,
        help_text="Product name.",
        verbose_name="Product name")
    #as of definition, prices are fixed
    #but in the future, it may be better to define product mass (or volume?)
    #and then define unit cost for the material
    price = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )
    description = models.TextField()
    materials = models.ManyToManyField("Material", related_name="materials")
    available = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    
    def get_absolute_url(self):
        """Returns the url for this player."""
        return reverse('player-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object.
        
        Returns the product name."""
        return self.name

class ProductImage(models.Model):
    """Model representing an image of a product.
    
    Separated model because there can be zero to infinity images 
    for each product."""
    #see https://medium.com/ibisdev/upload-multiple-images-to-a-model-with-django-fd00d8551a1c
    #for more expansive implementation
    name = models.CharField(max_length=100)
    product = models.ForeignKey("Product", on_delete=models.SET_NULL, blank=True, null=True)
    image = models.ImageField(upload_to='media/images')

    def __str__(self):
        """String for representing the Model object.
        
        Returns {image name} ({product})."""
        try:
            return f'{self.name} ({self.product.name})'
        except:
            return f'{self.name} (no product)'

class Material(models.Model):
    """Model representing a 3D print material and color.
    
    Intended for showing availability of a product in a certain color or material.
    """
    color_name = models.CharField(max_length=100)
    hex = models.CharField(
        max_length=7,
        help_text="Color as a hexadecimal in the form #FFFFFF.")
    material_type = models.CharField(
        max_length=20,
        help_text="Actual 3D print material (ABS, PLA, resin, etc.)")
    available = models.BooleanField(default=True)
    #consider using unit prices in future

    def __str__(self):
        """String for representing the Model object.
        
        Returns {color_name} {material_type}."""
        return f'{self.color_name} ({self.material_type})'

class ProductInstance(models.Model):
    """Model representing a single product with desired user specifications."""
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    #this should never happen but...
    material = models.ForeignKey("Material", on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField()
    total_price = models.DecimalField(max_digits=5, decimal_places=2)
    order = models.ForeignKey("Order", related_name="items", on_delete=models.CASCADE)

    def __str__(self):
        """String for representing the Model object.
        
        Returns {quantity}x {product} - {material}"""
        return f'{self.quantity}x {self.product} - {self.material}'

class Order(models.Model):
    """Model representing a completed order.
    
    Relationships to others (an order can have many of these):
    - ProductInstance (related_name = "items") **not "instances"!**"""
    id = models.AutoField(primary_key=True) #explicit so vs code knows what this is
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    student_id = models.CharField(max_length=10)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=15) #you will provide number or perish
    extra_notes = models.TextField(default="", blank=True, null=True)
    fulfilled = models.BooleanField(default=False)

    #need to write save funct for both product instance and order to generate this
    #should be read-only field to user (discounts and the like should be noted in extra_notes)
    grand_total = models.DecimalField(max_digits=6, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['created_at']

    def __str__(self):
        """String for representing the Model object.
        
        Returns #{id} - {last_name}, {first_name} ({student_id})"""
        return f'#{self.id} - {self.last_name}, {self.first_name} ({self.student_id})'
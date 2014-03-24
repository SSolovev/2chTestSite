from mysite.forum.models import *


cat1 = Categories(category='Hobby',description='This category is for disscussions about different hobbies')
cat2 = Categories(category='Hi-Tech',description='This category is for disscussions about new technologies')
cat3 = Categories(category='Talks',description='This category is for simple talk')

cat1.save()
cat2.save()
cat3.save()

#######################################################################################################################################

subcat1 = Subcategories(subcategory='C++',description='This category is for disscussions about different hobbies', category=cat2)
subcat2 = Subcategories(subcategory='Java',description='This category is for disscussions about new technologies', category=cat2)
subcat3 = Subcategories(subcategory='Python',description='This category is for simple talk', category=cat2)

subcat4 = Subcategories(subcategory='Voronezh',description='This category is for Voronezh talks', category=cat3)
subcat5 = Subcategories(subcategory='Peter',description='This category is for Peter talks', category=cat3)
subcat6 = Subcategories(subcategory='Moscow',description='This category is for Moscow talks', category=cat3)

subcat7 = Subcategories(subcategory='Football',description='This category is for Football', category=cat1)
subcat8 = Subcategories(subcategory='Basketball',description='This category is for Basketball', category=cat1)
subcat9 = Subcategories(subcategory='Volleyball',description='This category is for Volleyball talk', category=cat1)

subcat1.save()
subcat2.save()
subcat3.save()

subcat4.save()
subcat5.save()
subcat6.save()

subcat7.save()
subcat8.save()
subcat9.save()

#######################################################################################################################################

class Topics(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    date = models.DateField()
    creator_name = models.CharField(max_length=10)
    subcategory = models.ForeignKey(Subcategories)

    subcat1 = Topics(subcategory='C++',description='This category is for disscussions about different hobbies', category=cat2)

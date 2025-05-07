from .models import Category
from .models import CartItem

def menu_categories(request):
    categories = Category.objects.all()
    return {'menu_categories': categories}


def cart_item_count(request):
    count = 0
    if request.user.is_authenticated:
        count = CartItem.objects.filter(cart__user=request.user).count()
    return {'cart_item_count': count}
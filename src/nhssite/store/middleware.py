class EnsureCartMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            request.session['cart']
        except:
            cart = request.session.get('cart', {})
            request.session['cart'] = cart

        response = self.get_response(request)

        return response
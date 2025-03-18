class NavigationHistoryMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == 'GET' and request.path.startswith('/help'):
            history = request.session.get('history', [])
            if not history or history[-1] != request.path:
                history.append(request.path)
                if len(history) > 10:
                    history.pop(0)
                request.session['history'] = history

        response = self.get_response(request)
        return response

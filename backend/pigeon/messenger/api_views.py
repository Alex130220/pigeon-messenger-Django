# messenger/api_views.py
class MessageSearchView(APIView):
    def get(self, request):
        query = request.GET.get('q')
        messages = Message.objects.filter(content__icontains=query)
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)
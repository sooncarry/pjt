from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import FinanceTerm
from .serializers import FinanceTermSerializer

@api_view(['GET'])
def finance_terms(request):
    query = request.GET.get('q', '')
    if query:
        terms = FinanceTerm.objects.filter(
            title__icontains=query
        ) | FinanceTerm.objects.filter(
            eng_title__icontains=query
        ) | FinanceTerm.objects.filter(
            content__icontains=query
        )
    else:
        terms = FinanceTerm.objects.all()
    serializer = FinanceTermSerializer(terms, many=True)
    return Response(serializer.data)

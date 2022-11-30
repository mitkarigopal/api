from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import Data
from .serializers import DataSerializers
import spacy
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
@api_view(['POST'])
def data_api(request):
    if request.method == 'POST':
        serializer = DataSerializers(data=request.data)
        print(serializer)
        if serializer.is_valid():
            serializer.save()
            nlp = spacy.load("en_core_web_sm")
            var = request.data['text']
            doc = nlp(var)
            for ent in doc.ents:
                print(ent.text, ":", ent.label_)
                datas = {ent.text : ent.label_}
                json_data = JSONRenderer().render(datas)
                print(json_data)
                return HttpResponse(json_data, content_type='application/json')


# from fastapi import FastAPI
# from pydantic import BaseModel
# import spacy
# from django.views.decorators.csrf import csrf_exempt
#
# nlp_en = spacy.load("en_core_web_sm")
# app = FastAPI()
#
#
# class Data(BaseModel):
#     text: str
#
# @csrf_exempt
# @app.post('text')
# def extract_entities(data: Data):
#     doc_en = nlp_en(data.text)['text']
#     ents = []
#     for ent in doc_en.ents:
#         ents.append({"text": ent.text, "label_": ent.label_})
#     return {"message": data.text,  "ents": ents}
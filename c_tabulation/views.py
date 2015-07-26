from django.shortcuts import render
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from c_tabulation.models import CalculatedData

import csv
import pandas as pd
import base64
import os
import json
# Create your views here.

def upload_or_render_csv(request):
    """ This will upload the CSV file to the server and will try to save it somewhere"""
    context = {}
    if request.method =='GET':
        return render(request, 'c_tabulation/upload.html', context)
    elif request.method =='POST':
        try:
            uploaded_file=request.FILES['upload_file']
            if str(uploaded_file.content_type) != 'text/csv':
               raise Exception('Incorrect file uploaded.')
            else:#Process the request and read CSV
                uploaded, file_name_with_path = save_file_to_disk(uploaded_file)
                if uploaded:
                    context =  read_and_parse_csv(file_name_with_path)
                    context['uploaded_file_base_encoded'] = base64.b64encode(file_name_with_path)
                    context['file_name'] = uploaded_file.name
                    context['showtabulationdata_url'] = reverse('showtabulationdata')
                    context['savetabulationdata_url'] = reverse('savetabulateddata')
                    return render(request, 'c_tabulation/select_tabulation.html', context)
                else:
                    raise Exception('Parsing of CSV Failed. Upload a proper one')
        except Exception as errormessage:
            print errormessage

def save_file_to_disk(file):
    """Move the uploaded file to the disk"""
    file_name_with_path = settings.UPLOAD_PATH+str(file.name)
    with open(file_name_with_path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    return True, file_name_with_path
    
def read_and_parse_csv(cvs_file_with_path):
    """Read CSV with pandas and show dropdown option"""
    df =  pd.read_csv(cvs_file_with_path)
    gender_groups       =  df.groupby('Gender').groups
    handedness_groups   =  df.groupby('Handedness').groups
    context     = {'data_frame_html':df.to_html(),'Handedness':handedness_groups, 'Gender':gender_groups}
    return context


def show_tabulation(request):
    """Send Response to Ajax Request for selected tabulated data"""
    required_fields =  ['gender','handedness','uploaded_file_base_encoded']
    for field_name in required_fields:
        try:
            request.POST[field_name]
        except:
            raise Exception(field_name+' is required')
    
    uploaded_file_name = request.POST.get('uploaded_file_base_encoded',None)
    uploaded_file_name_base_decoded = base64.b64decode(uploaded_file_name)
    gender = [request.POST['gender']]
    handedness = [request.POST['handedness']]
    
    if uploaded_file_name_base_decoded and  os.path.isfile(uploaded_file_name_base_decoded):
        df =  pd.read_csv(uploaded_file_name_base_decoded)
        
        gender_groups       =  df.groupby('Gender').groups.keys()
        handedness_groups   =  df.groupby('Handedness').groups.keys()
    
        if gender and gender[0]!='all':
            gender_groups = gender
        if handedness and handedness[0]!='all':
            handedness_groups = handedness
        
        df_filtered = df[df.Gender.isin(gender_groups) & df.Handedness.isin(handedness_groups)]
        df_calc     = pd.crosstab(df_filtered.Gender , df_filtered.Handedness, rownames=['Gender'],  colnames=['Handedness'], margins=True)
        
        response_data = {}
        response_data['tab_data'] = str(df_calc.to_html())
        response_data['json_data'] = str(df_calc.to_json())
        return HttpResponse(json.dumps(response_data),  content_type="application/json")
    else:
        raise Exception('File not found or missing.')

def save_tab_data(request):
    """Save the tab data to data SQL LITE as of now"""
    try:
        save_tab_data = request.POST['tab_json_data']
    except Exception as errormessage:
        print errormessage
        raise Exception('Data not in proper format.')
    
    try:
        CalculatedData_instance = CalculatedData(searched_data=save_tab_data)
        response_data = CalculatedData_instance.save()
        return HttpResponse(json.dumps({}), status=200,content_type="application/json")
    except:
        return HttpResponse(status=500,content_type="application/json")
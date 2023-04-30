from django.shortcuts import render
import pickle
# Create your views here.

def home(request):
    return render(request, 'index.html')

def getPredictions(gender,age,hypertension,	heart_disease,	ever_married,work_type, Residence_type,avg_glucose_level,bmi,smoking_status):
    model = pickle.load(open('random_forest_model.sav', 'rb'))
    scaled = pickle.load(open('scaler.sav', 'rb'))
    num_col = [[age, avg_glucose_level, bmi]]
    num_col = scaled.transform(num_col)    
    age = num_col[0][0] 
    avg_glucose_level = num_col[0][1]
    bmi = num_col[0][2]
    prediction = model.predict([
        [gender,age,hypertension,heart_disease,ever_married,work_type, Residence_type,avg_glucose_level,bmi,smoking_status]
    ])[0]
    print(prediction)
    
    if prediction == 0:
        return 'no'
    elif prediction == 1:
        return 'yes'
    else:
        return 'error'

def result(request):
    gender = int(request.POST.get('gender', ''))
    age= float(request.POST.get('age',''))
    hypertension = int(request.POST.get('hypertension', ''))
    heart_disease = int(request.POST.get('heart_disease', ''))
    ever_married = int(request.POST.get('ever_married', ''))
    work_type = int(request.POST.get('work_type', ''))
    Residence_type = int(request.POST.get('Residence_type', ''))
    avg_glucose_level = float(request.POST.get('avg_glucose_level',''))
    bmi =float(request.POST.get('bmi',''))
    smoking_status = (request.POST.get('smoking_status', ''))
    # print(gender,age,hypertension,heart_disease,ever_married)
    result = getPredictions(gender,age,hypertension,heart_disease,ever_married,work_type,
                             Residence_type,avg_glucose_level,bmi,smoking_status)
    return render(request, 'result.html', {'result': result})
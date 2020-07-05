import pandas as pd
appointment = pd.read_csv('appointment.csv')

def return_appointment(disease):
    diseases = list(appointment[appointment.columns[0]])
    ind = diseases.index(disease)
    doc_name = appointment[appointment.columns[1]][ind]
    specilization = appointment[appointment.columns[2]][ind]
    timing = appointment[appointment.columns[3]][ind]
    report = "Your problem is related to " + disease.lower() +"<br>" + "The appropriate specialist for yor issue is " +  specilization + "<br>" + "Doctor name : " + doc_name +"<br>"+"Your appointment is on "+ timing
    return {'data1':disease , 'data2':report}
    
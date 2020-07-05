import pandas as pd
import random
cure = pd.read_csv('cure.csv')
diseases = list(cure.disease)
resp = {
        'critical':['I would highly suggest you to visit a doctor for this issue.' , 
        'Its better if you see a doctor for your disease.',
        'I would suggest you to consult a doctor for this disease.'],
        'safe':['Your disease is not critical , if you wish u can visit the doctor',
        "I'm happy to say that your disease does not come under critical , but you can always visit a doctor! ",
        'phew , your safe your disease is not critical , if you wish you can see a doctor !'
        ]
}

def return_diagnosis_report(disease):
    ind = diseases.index(disease.lower())
    global cure
    desc = cure['desc'][ind]
    cure_ = cure['cure'][ind]
    deg = cure[cure.columns[2]][ind]
    if deg == 1:
        string = "you have {}".format(disease) + "<br><br>" + "DESCRIPTION : <br>" + desc + "<br><br>" + "CURE : <br>" + cure_ + "<br><br>" + random.choice(resp['critical'])
    else:
        string = "you have {}".format(disease) + "<br><br>" + "DESCRIPTION : <br>" + desc + "<br><br>" + "CURE : <br>" + cure_ + "<br><br>" + random.choice(resp['safe'])
    return string



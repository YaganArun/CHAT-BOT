import pandas as pd
cure = pd.read_csv('cure.csv')
diseases = list(cure.disease)

def return_diagnosis_report(disease):
    ind = diseases.index(disease)
    global cure
    desc = cure['desc'][ind]
    cure_ = cure['cure'][ind]
    string = "you have {}".format(disease) + "<br><br>" + "DESCRIPTION : <br>" + desc + "<br><br>" + "CURE : <br>" + cure_

    return string



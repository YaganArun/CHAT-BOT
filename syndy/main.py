from flask import Flask , render_template , request
from textblob import TextBlob
from inferenceEngine import  inferenceEngine
from knowledgeBase import cure , appt
app = Flask(__name__)
g_node = 0 
age_group = ' '

@app.route('/')                             #loading the conversation UI
def home():
    return render_template('botLoad.html')

@app.route('/info')
def additional_info():
    global age_group
    age = int(request.args.get('age'))
    if age <= 18 :
        age_group = 'children'
    else:
        age_group = 'adult'
    return ' '

@app.route('/ie')                           #loading the inference engine 
def inferenceEngine_():
    global g_node , age_group
    g_node = 0
    return render_template('bot.html' , question = inferenceEngine.print_question(age_group , g_node) , age_grp = age_group)

@app.route('/booking')                      #loading booking appoinment page
def appointment_booking():
    return render_template('appointment.html')


@app.route('/userInput')                      #recieve input from inference Engine - (bot.html)
def userInput():
    global g_node , age_group
    userMsg = str(request.args.get('msg'))
    ####
    conv = TextBlob(u'{}'.format(userMsg))
    userMsg = str(conv.translate(from_lang='ta' , to = 'en'))
    print(userMsg)
    ##
    g_node = inferenceEngine.decision(age_group , g_node , userMsg)
    if age_group == 'children':
        if inferenceEngine.tree_children.feature[g_node] == inferenceEngine._tree.TREE_UNDEFINED: #reached leaf node or disease
            res = TextBlob(cure.return_diagnosis_report(inferenceEngine.print_disease(inferenceEngine.tree_children.value[g_node])[0]))
            return str(res.translate(from_lang='en' , to = 'ta'))
            #return cure.return_diagnosis_report(inferenceEngine.print_disease(inferenceEngine.tree_children.value[g_node])[0])
        else:
            res = TextBlob(inferenceEngine.print_question(age_group , g_node))
            #return  inferenceEngine.print_question(age_group , g_node)
            return str(res.translate(from_lang ='en' , to = 'ta'))
    else:
        if inferenceEngine.tree.feature[g_node] == inferenceEngine._tree.TREE_UNDEFINED: #reached leaf node or disease
            res = TextBlob(cure.return_diagnosis_report(inferenceEngine.print_disease(inferenceEngine.tree.value[g_node])[0]))
            #return  str(res.translate(from_lang = 'en' , to = 'ta'))
            #return cure.return_diagnosis_report(inferenceEngine.print_disease(inferenceEngine.tree.value[g_node])[0])
        else:
            res = TextBlob(inferenceEngine.print_question( age_group , g_node))
            #return str(res.translate(from_lang = 'en' , to = 'ta'))
            #return  inferenceEngine.print_question( age_group , g_node)


@app.route('/appointment')                    #recieve input from appointment - (appointment.html)
def appointment_response():
    userText = request.args.get('msg')
    return appt.return_appointment(str(inferenceEngine.booking_appointment_response(userText)))

@app.route('/queries')
def user_queries():
    userQuery = request.args.get('msg')
    print(userQuery , "  predicted :  " , inferenceEngine.nlp.predict_text_class(userQuery))
    return inferenceEngine.nlp.predict_text_class(userQuery) 


if __name__ == '__main__':
    app.run()
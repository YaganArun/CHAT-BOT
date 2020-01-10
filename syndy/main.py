from flask import Flask , render_template , request
from inferenceEngine import inferenceEngine 
from knowledgeBase import cure
app = Flask(__name__)
g_node = 0

@app.route('/')                             #loading the conversation UI
def home():
    return render_template('botLoad.html')

@app.route('/ie')                           #loading the inference engine 
def inferenceEngine_():
    global g_node 
    g_node = 0
    return render_template('bot.html' , question = inferenceEngine.print_question(g_node))

@app.route('/booking')                      #loading booking appoinment page
def appointment_booking():
    return render_template('appointment.html')

@app.route('/userInput')                      #recieve input from inference Engine - (bot.html)
def userInput():
    userMsg = str(request.args.get('msg'))
    global g_node
    g_node = inferenceEngine.decision(g_node , userMsg)
    if inferenceEngine.tree.feature[g_node] == inferenceEngine._tree.TREE_UNDEFINED: #reached leaf node or disease
        return cure.return_diagnosis_report(inferenceEngine.print_disease(inferenceEngine.tree.value[g_node])[0])
    else:
        return  inferenceEngine.print_question(g_node)

@app.route('/appointment')                    #recieve input from appointment - (appointment.html)
def appointment_response():
    userText = request.args.get('msg')
    return inferenceEngine.booking_appointment_response(userText)


if __name__ == '__main__':
    app.run()
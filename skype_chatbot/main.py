# This is Simple Echo Bot

import skype_chatbot
import json
from flask import Flask, request
import urllib
import json

app = Flask(__name__)

app_id = '###############'
app_secret = '##########'

bot = skype_chatbot.SkypeBot(app_id, app_secret)



@app.route('/api/messages', methods=['POST', 'GET'])
def webhook():
    if request.method == 'POST':
        try:
            data = json.loads(request.data)
            print (data)
            bot_id = data['recipient']['id']
            bot_name = data['recipient']['name']
            recipient = data['from']
            service = data['serviceUrl']
            sender = data['conversation']['id']
            text = data['text']
            data = urllib.parse.urlencode({"text": text}).encode('utf-8')
            u = urllib.request.urlopen("http://text-processing.com/api/sentiment/", data)
            the_page = u.read()
            out=json.loads(the_page)
            #print (out)
            if out['label']=="neg":
                output_text= "SENTIMENT == NEGATIVE"
            elif out['label']=="pos":
                output_text= "SENTIMENT == POSITIVE"
            elif out['label']=="neutral":
                output_text= "SENTIMENT == NEUTRAL"
            bot.send_message(bot_id, bot_name, recipient, service, sender, output_text)

        except Exception as e:
            print(e)

    return 'Code: 200'


if __name__ == '__main__':
    #context = ('domain.cer', 'domain.key')
    #context = ()

    #app.run(host='127.0.0.1', port=8080, debug=False, ssl_context=context)
    app.run(host='127.0.0.1', port=8080, debug=False)

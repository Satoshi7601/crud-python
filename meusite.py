from App import app

import os 
# informaçoes referente a porta de acesso

if __name__ =='main':
    port = int(os.genv('PORT'), '5000')
    app.run(host='0.0.0.0', port=port)
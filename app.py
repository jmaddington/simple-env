from flask import Flask, render_template, request, Response
import os
from functools import wraps

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.debug = True

ENV_FILE_PATH = '/home/user/.env'
SSH_DIR_PATH = '/home/user/.ssh/'
ENV_PASSWORD = os.environ.get('ENV_PASSWORD')

def check_auth(username, password):
    """Check if the password matches ENV_PASSWORD (username is ignored)"""
    return bool(ENV_PASSWORD and password == ENV_PASSWORD)

def authenticate():
    """Send 401 response that enables basic auth"""
    return Response(
        'Could not verify your credentials.\n'
        'You must login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'}
    )

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

@app.route('/', methods=['GET', 'POST'])
@requires_auth
def index():
    message = None
    message_type = None

    if request.method == 'POST':
        if 'env_content' in request.form:
            
            # Make sure /app exists
            if not os.path.exists('/home/user'):
                os.makedirs('/home/user')
                
            try:
                with open(ENV_FILE_PATH, 'w') as file:
                    file.write(request.form['env_content'])
                message = 'ENV file saved successfully!'
                message_type = 'success'
            except Exception as e:
                message = f'Error saving ENV file: {str(e)}'
                message_type = 'error'
        
        elif 'ssh_key' in request.form:
            try:
                if not os.path.exists(SSH_DIR_PATH):
                    os.makedirs(SSH_DIR_PATH, mode=0o700)
                key_content = request.form['ssh_key'].strip()
                if key_content:
                    with open(os.path.join(SSH_DIR_PATH, 'authorized_keys'), 'a') as file:
                        if not key_content.endswith('\n'):
                            key_content += '\n'
                        file.write(key_content)
                    os.chmod(os.path.join(SSH_DIR_PATH, 'authorized_keys'), 0o600)
                    message = 'SSH key added successfully!'
                    message_type = 'success'
                else:
                    message = 'No SSH key provided'
                    message_type = 'error'
            except Exception as e:
                message = f'Error adding SSH key: {str(e)}'
                message_type = 'error'

        elif 'ssh_key_file' in request.files:
            try:
                if not os.path.exists(SSH_DIR_PATH):
                    os.makedirs(SSH_DIR_PATH, mode=0o700)
                file = request.files['ssh_key_file']
                if file and file.filename:
                    key_content = file.read().decode('utf-8').strip()
                    if key_content:
                        with open(os.path.join(SSH_DIR_PATH, 'authorized_keys'), 'a') as f:
                            if not key_content.endswith('\n'):
                                key_content += '\n'
                            f.write(key_content)
                        os.chmod(os.path.join(SSH_DIR_PATH, 'authorized_keys'), 0o600)
                        message = 'SSH key file processed successfully!'
                        message_type = 'success'
                    else:
                        message = 'Uploaded file was empty'
                        message_type = 'error'
                else:
                    message = 'No file uploaded'
                    message_type = 'error'
            except Exception as e:
                message = f'Error processing SSH key file: {str(e)}'
                message_type = 'error'

    response = app.make_response(render_template('index.html', 
                                               message=message, 
                                               message_type=message_type))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

if __name__ == '__main__':
    if not ENV_PASSWORD:
        print("ERROR: ENV_PASSWORD must be set!")
        exit(1)
    print("Starting Flask in debug mode...")
    app.run(host='0.0.0.0', port=8081, debug=True)
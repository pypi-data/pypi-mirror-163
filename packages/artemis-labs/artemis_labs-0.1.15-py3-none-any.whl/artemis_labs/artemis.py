from asyncio import constants
from .artemis_socket import artemis_socket 
import json 
from time import sleep
import base64
import matplotlib.pyplot as plt
import os
import numpy as np
import io
import subprocess

class artemis:
    
    APP_PATH = "app.json"

    def __init__(self, runner_path="", launch_command = "", code_path="", launch=True, dev=False):
        self.runner_path = runner_path
        self.launch_command = launch_command
        self.dev = dev

        self.onLock = False
        self.onLockContent = ''

        self.queryLock = False
        self.queryLockContent = ''

        self.submitLock = False
        self.submitContent = ''

        self.nextLock = False

        self.callbackMap = {}
        self.queryCallbackQueue = []

        self.mode = "code"

        self.code_path = code_path

        self.artemis_socket = artemis_socket(self.callback_handler)
        try:
            with open(self.APP_PATH, "r") as f:
                self.app = json.load(f)
        except Exception as e:
            print(e)
            print('[Artemis] Exception: Unable to load app.json')
            self.app = {}       

        print('Launch = ', launch)
        self.run(launch) 


    # Callback handler
    def callback_handler(self, message):        

        # Skip pings
        message = json.loads(message)
        if message['type'] != 'ping':

            # Handle query and callback responses separately
            if message['type'] == 'query':
                if len(self.queryCallbackQueue) > 0:
                    self.queryCallbackQueue[0](message)
                    self.queryCallbackQueue.pop(0)
            elif message['type'] == 'submit':
                self.submitContent = message['content']
                self.submitLock = False
            elif message['type'] == 'next':
                self.nextLock = False
            elif message['type'] == 'exit':
                os._exit(1)
            elif message['type'] == 'reload':
                dev_arg = ''
                if self.dev:
                    dev_arg = ' dev'
                subprocess.Popen(['artemis_labs', self.code_path, self.launch_command , dev_arg, 'nolaunch'], creationflags=subprocess.CREATE_NO_WINDOW)
                os._exit(1)
            else:
                callbackTag = message["type"] + "-" + message["attribute"] + "-" + message["name"]
                if callbackTag in self.callbackMap:
                    self.callbackMap[callbackTag](json.loads(message["state"]))
                else:
                    print('Callback not found: ', message)

    # Check if connected
    def isConnected(self):
        return self.artemis_socket.isConnected()

    # Enqueue callback to receive message when message received
    def on(self, action, name, callback):
        onPacket = {}
        onPacket["type"] = "callback"
        onPacket["attribute"] = action
        onPacket["name"] = name
        callbackTag = onPacket["type"] + "-" + onPacket["attribute"] + "-" + onPacket["name"]
        self.callbackMap[callbackTag] = callback
        self.artemis_socket.send(json.dumps(onPacket))

    # Send update message
    def update(self, elementName, newValue):
        updatePacket = {}
        updatePacket["type"] = "update"
        updatePacket['name'] = elementName
        updatePacket['value'] = newValue
        self.artemis_socket.send(json.dumps(updatePacket))

    # Send navigate message
    def navigate(self, pageName):
        navigatePacket = {}
        navigatePacket["type"] = "navigate"
        navigatePacket['pageName'] = pageName
        self.artemis_socket.send(json.dumps(navigatePacket))

    def query(self, callback):
        queryPacket = {}
        queryPacket["type"] = "query"
        self.queryCallbackQueue.append(callback)
        self.artemis_socket.send(json.dumps(queryPacket))

    def query_unlock(self, content):
        self.queryLockContent = content
        self.queryLock = False

    def query_wait(self):
        self.queryLock = True
        self.query(self.query_unlock)
        while self.queryLock:
            sleep(0.1)
        returnContent = self.queryLockContent
        self.queryLockContent = ''
        return returnContent

    def on_unlock(self, content):
        self.onLockContent = content
        self.onLock = False

    def wait(self, action, name):
        self.onLock = True
        self.on(action, name, self.on_unlock)
        while self.onLock:
            sleep(0.1)
        returnContent = self.onLockContent
        self.onLockContent = ''
        return returnContent

    # Enqueue callback
    def setCallback(self, callback):
        self.artemis_socket.enqueueCallback(callback)

    # Create input
    def createInput(self, line, name, comment):
        self.artemis_socket.send(json.dumps({"type": "create", "element": "input", 'line': line, 'name' : name, 'comment': comment}))
        self.submitLock = True

    def hideInput(self):
        self.artemis_socket.send(json.dumps({'type': 'hide', "element": "input"}))

    def waitForInput(self):
        while self.submitLock:
            sleep(0.1)
        return self.submitContent

    '''
    Output Processing
    '''
    def convertType(self, value, componentType):
        graph_types = ['line-graph', 'scatter-graph']
        table_types = ['table']

        if isinstance(value, list) and componentType not in graph_types:
            value = str(value)
            value = value.replace("'", '"')
        if isinstance(value, np.ndarray) and componentType not in graph_types:
            value = list(value)
            for i, el in enumerate(value):
                if isinstance(el, np.ndarray):
                    value[i] = list(el)
                elif isinstance(el,list):
                    value[i] = list(el)
            value = str(value)
            value = value.replace("'", '"')
        return value

    def setup_plot_args(named_args):

        # Graph parameters
        xmin = None
        xmax = None
        ymin = None
        ymax = None
        figsize = (8,3)
        xlabel = ""
        ylabel = ""
        title = ""

        # Run args
        for named_arg in named_args:
            if named_arg[0] == 'xmin':
                xmin = float(named_arg[1])
            if named_arg[0] == 'xmax':
                xmax = float(named_arg[1])
            if named_arg[0] == 'ymin':
                ymin = float(named_arg[1])
            if named_arg[0] == 'ymax':
                ymax = float(named_arg[1])
            if named_arg[0] == 'xlabel':
                xlabel = named_arg[1]
            if named_arg[0] == 'ylabel':
                ylabel = named_arg[1]
            if named_arg[0] == 'title':
                title = named_arg[1]
            if named_arg[0] == 'figsize':
                figsize_input = named_arg[1].replace(')', '').replace('(', '')
                figsize_components = figsize_input.split(',')
                figsize = (float(figsize_components[0]), float(figsize_components[1]))

        # Make plot
        plt.figure(figsize=figsize)

        # Set limits
        if xmin != None:
            plt.xlim(left=xmin)
        if xmax != None:
            plt.xlim(right=xmax)
        if ymax != None:
            plt.ylim(top = ymax)
        if ymin != None:
            plt.ylim(bottom=ymin)

        # Set labels
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)

        # Set title
        plt.title(title)

    def preprocess(self, value, componentType, named_args=[]):
        if componentType == "scatter-graph":
            arr = np.array(value)
            artemis.setup_plot_args(named_args)
            plt.scatter(arr[:,0], arr[:,1])
            value = artemis.load_image_from_data(artemis.save_plt_to_bytes())
            componentType = "graph"
        elif componentType == "line-graph":
            plt.figure(figsize=(8,3))
            arr = np.array(value)
            artemis.setup_plot_args(named_args)
            plt.plot(arr[:,0], arr[:,1])
            value = artemis.load_image_from_data(artemis.save_plt_to_bytes())
            componentType = "graph"
        elif componentType == "graph":
            value = artemis.load_image_from_data(artemis.save_fig_to_bytes(value))

        return value, componentType

    def format_output(self, name, line, value, componentType, comment):
        return json.dumps({
            "type": "create", 
            "element": "output", 
            'line': line, 
            'name' : name, 
            'value': value, 
            "componentType" : componentType, 
            "comment" : comment
        })

    def createOutput(self, line, name, value, componentType, comment, named_args=[]):
        if named_args != []:
            print(named_args)

        value = self.convertType(value, componentType)
        value, componentType = self.preprocess(value, componentType, named_args)
        value = self.format_output(name, line, value, componentType, comment)
        self.artemis_socket.send(value)
        self.nextLock = True

    def waitForNext(self):
        while self.nextLock:
            sleep(0.1)

    def hideOutput(self):
        self.artemis_socket.send(json.dumps({'type': 'hide', "element": "output"}))

    def convert(type_id, value):
        return type_id(value)

    # Launch server
    def run(self, launch=True):

        self.artemis_socket.run()

        if launch:
            if os.name == 'nt':
                if self.mode == "code":
                    
                    # Start up server
                    if launch:

                        # Get directory of file
                        directory = os.path.dirname(os.path.abspath(__file__))

                        # Start server there
                        cur_dir = os.getcwd()
                        os.chdir(directory)
                        print('[Artemis] Starting using launch_server.py on port 8081...')
                        subprocess.Popen(['python', 'launch_server.py'])
                        os.chdir(cur_dir)
                        
                    # Open file on server
                    html_path = f'"http://localhost:8081/htdocs/launcher_code.html"'

                    # Start app
                    print(f'start chrome {html_path}')
                    os.system(f"start chrome {html_path}")
                else:
                    os.system("start chrome https://artemisardesignerdev.com/launcher_local.html")
            else:
                print('[Artemis] Please open Chrome and navigate to https://artemisardesignerdev.com/launcher_local.html')

        while not self.artemis_socket.isConnected():
            sleep(0.1)

        if self.mode == "code":
            init_packet = { 'type' : 'init', 'state' : json.dumps(self.app) }
            with open(self.code_path) as f:
                init_packet = { 'type' : 'init', 'state' : f.read() }            
                self.artemis_socket.send(json.dumps(init_packet))
        else:
            init_packet = { 'type' : 'init', 'state' : json.dumps(self.app) }
            self.artemis_socket.send(json.dumps(init_packet))

    # Helpers
    def load_image_from_data(data):
        return "data:image/png;base64," + base64.b64encode(data).decode('utf-8')

    def load_image(path):
        try:
            with open(path, "rb") as image_file:
                b64Encoding = "data:image/png;base64," + base64.b64encode(image_file.read()).decode('utf-8')
                return b64Encoding
        except Exception as e:
            print('[Artemis] Exception: Unable to load image')
            print('[Artemis] ' + str(e))
    
    def load_gif(path):
        try:
            with open(path, "rb") as image_file:
                b64Encoding = "data:image/png;base64," + base64.b64encode(image_file.read()).decode('utf-8')
                return b64Encoding
        except Exception as e:
            print('[Artemis] Exception: Unable to load image')
            print('[Artemis] ' + str(e))

    def save_plt_to_bytes():
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', bbox_inches='tight')
        buffer.seek(0)
        return buffer.read()
        
    def save_fig_to_bytes(fig):
        buffer = io.BytesIO()
        fig.savefig(buffer, format='png', bbox_inches='tight')
        buffer.seek(0)
        return buffer.read()
import ollama

base_url='http://100.101.54.114:11434'
models = ['mistral:7b', 'llama2:7b','llama2:13b','llama2:70b','mixtral:latest','tinyllama:latest']
ranked_models = ['tinyllama:latest', 'llama2:7b','llama2:13b','llama2:70b']
default_model='mistral:7b'
_debug = True
debug = lambda message: print(message) if _debug else None
class ChaosLLM:
    
    
    messages = []
    model = ''
    models = ranked_models

    def __init__(self, model='tinyllama:latest',base_url=base_url):
        self.ollama = ollama.Client(host=base_url)
        self.model = model
        

    def invoke(self, msg):
        debug('to ollama(' + self.model + '): ' + msg)
        self.messages.append(
            {
            'role': 'user',
            'content': msg,
            },
        )
        return self.ollama.chat(model=self.model,messages=self.messages, stream=True)
        self.messages.append(response['message'])
        debug('from ollama(' + self.model + '): ' + response['message']['content'])
        return response['message']['content']
    def chat(self, messages, model=None,format=None ,options = None):
        debug(f'to ollama ({model}): {messages}')
        try:
            response = self.ollama.chat(messages=messages,options=options if options is not None else None,model=model if model is not None else self.model, format=format if not format == None else None)
            debug(f'from ollama ({model}): {response}')
            return response['message']
        except Exception as err:
            print(f'Couldnt communicate with llm error: {err}')
            return None
    def stream(self, messages, model=None,format=None ,options = None):
        debug(f'to ollama ({model if model is not None else self.model}): {messages}')
        try:
            response=''
            for chunk in self.ollama.chat(messages=messages,stream=True,options=options if options is not None else None,model=model if model is not None else self.model, format=format if not format == None else None):
                response += chunk['message']['content']
                yield chunk
            self.messages.append(
            {
            'role': 'assistant',
            'content': response,
            },
            )
            debug(f'from ollama ({model if model is not None else self.model}): {response}')
            #return response['message']
        except Exception as err:
            print(f'Couldnt communicate with llm error: {err}')
            return None

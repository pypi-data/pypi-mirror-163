from functools import partial, wraps
from . expr import Parser
from . mqtt import topic


__all__ = ('StateAwareMixin', 'toggle', 'when')


class StateAwareMixin:
    ''' Mixin for stateful MQTT clients.
        Status updates are recorded in-memory from MQTT topics,
        e.g. `status/#`.
        The message payload for status updates is JSON-converted if possible.
        The last known state is available in `self.current_state`.
        Subclasses may define handler methods using the @when decorator`.
    '''
    
    conditions = {}
    parser = Parser()
    
    def __init__(self):
        'Register topics and the state callcack.'
        
        super().__init__()
        self.current_state = {}

        status_topic = self.get_config().get('status_topic')
        assert status_topic, 'status_topic not found in configuration'

        # Subscribe to status updates
        register = topic(status_topic, payload_converter=self.decode_json)
        register(self.update_status)


    @staticmethod
    def update_status(self, _userdata, msg):
        ''' Track the global state,
            and invoke handler methods defined by subclasses
            with the message payload.
        '''
        if self.on_status_update(msg.topic, msg.payload):
            self.invoke_handlers(msg.topic, msg.payload)


    def on_status_update(self, topic, payload):
        ''' Keep the global state in-memory.
            Returns a path to the updated attribute in `self.current_state`
            when the state has changed, or `None` otherwise.
        '''
        # Update only if the value has changed
        if self.current_state.get(topic) != payload:
            self.current_state[topic] = payload
            self.log.info('Updated: %s = %s', topic, payload)
            return topic
    
    
    def invoke_handlers(self, topic, payload):
        'Run through conditions and invoke appropriate handlers'
        for expr, method in self.conditions.items():
            if topic in expr.keys and expr.keys <= self.current_state.keys():
                method(self)


def when(expression):
    ''' Decorator for status handler methods.
        The decorated method is invoked when the expression depends 
        on the updated topic and when it evaluates to `True`.
        For the expression grammar, see the docstrings in `expr.py`.
    '''
    
    predicate = StateAwareMixin.parser.parse(expression)
    
    def wrapper(method):
        id = method.func.__name__ if type(method) is partial else method.__name__
        
        @wraps(method)
        def wrapped(self):
            if predicate(self.current_state):
                self.log.info('Invoking: %s', id)
                method(self)
            else:
                self.log.debug('Skipping: %s', id)
        StateAwareMixin.conditions[predicate] = wrapped
        return wrapped
    return wrapper


def toggle(expression):
    ''' Decorator for status handler methods.
        The decorated method is invoked with the value of the expression
        when the expression depends on the updated topic.
        For the expression grammar, see the docstrings in `expr.py`.
    '''
    
    predicate = StateAwareMixin.parser.parse(expression)
    
    def wrapper(method):
        id = method.func.__name__ if type(method) is partial else method.__name__
        
        @wraps(method)
        def wrapped(self):
            condition = predicate(self.current_state)
            self.log.info('Invoking: %s(%s)', id, condition)
            method(self, condition)
        StateAwareMixin.conditions[predicate] = wrapped
        return wrapped
    return wrapper

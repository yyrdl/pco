# -*- coding: UTF-8 -*-
import types

class co:
    def __init__(self,func):
        self.ctx = {}
        self.resumed = False
        self.exited = False
        self.suspended = False
        self.func = func
        self.handler = None
        self.iterator = None
        self.isGenerator = False
        self.excption = None
        
    def setCtx(self,ctx):
        self.ctx = ctx

    def getCtx(self):
        return self.ctx
    
    def suspend(self):
        self.suspended = True
        self.iterator.throw(StopIteration,"Suspend coroutine manually")  

    def __compile__(self):
        if type(self.func) is not types.FunctionType:
            raise TypeError("The argument must be a function!")

        def exit(error,result):
            if self.exited == True:
                 return 
            self.exited = True

            if type(self.handler) is types.FunctionType:
                return self.handler(error,result)
            else:
                if error is not None:
                    raise error

        def run(args):
            value = None
            done = False

            try:
                value = self.iterator.send(args)
            except StopIteration as e:
                if len(e.args)>0:
                    value = e.args[0]
                else:
                    value = None
                done = True
            except BaseException as excption:
                self.excption = excption

            if done == True:
                return exit(None,value)
            
            if self.excption is not None:
                return exit(self.excption,None)

           
            if isinstance(value,co):
                value.setCtx(self.ctx)
                return value(resume)
            return resume(None,value)
        
        self.run = run

        def resume(*args):
            if (self.exited is True) or (self.suspended is True):
                return 
            return run(args)

        try:

            self.iterator = self.func(self.ctx,resume)

        except BaseException as excption:

            self.excption = excption

        if self.excption is not None:
            return

        if type(self.iterator) is types.GeneratorType:
            self.isGenerator = True

    def __call__(self,*args):

        func = None

        if len(args)>0:
            func = args[0]

        if type(func) is types.FunctionType:
            self.handler = func

        self.__compile__()

        if self.isGenerator == True:
           return self.run(None)
        else:
            if self.handler is not None:
                self.handler(self.excption,self.iterator)

# basesic test


def sync_code(param):
    def run(ctx,resume):
        print(param) # 123
        print(ctx['a']) # "what's up?"
        return 'hello world'
    return co(run)


def async_code(param):
    def run(ctx,resume):
        ctx['a'] = "what's up?"
        (err,result) = yield sync_code(param)
        print(err,result)#None hello world
        return 'ok'
    return co(run)



def callback(err,result):
    print(err) # None
    print(result) # ok

async_code(123)(callback)

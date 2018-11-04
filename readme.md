# PCO
coroutine for python ,based on generator
> still under development

example code:

```python
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

```
output

```
123
what's up?
None hello world
None
ok
``` 

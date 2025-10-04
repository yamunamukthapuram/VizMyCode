class A:
    def __init__(self):
        pass

    def foo(self):
        self.helper()
        print("foo")

    def helper(self):
        print("helper")

def standalone():
    a = A()
    a.foo()
    helper_func()

def helper_func():
    print("I am helper func")
    standalone2()

def standalone2():
    print("second")

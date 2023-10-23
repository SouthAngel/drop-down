def mrundev():
    print('mrundev')
    import importlib
    tapath = r'D:\001\Temp\WorkSpace\Blender\addons\drop-me\src'
    import sys
    if tapath not in sys.path:
        sys.path.insert(0, tapath)
    import drop_me
    try:
        drop_me.unregister()
    except Exception as e:
        print([e])
    importlib.reload(drop_me)
    drop_me.register()
    import drop_me.core
    importlib.reload(drop_me.core)
    drop_me.core.test1()

def rundev():
    import runpy
    mm = runpy.run_path(r'D:\001\Temp\WorkSpace\Blender\addons\drop-me\src\drop_me\rundev.py')
    print('rundev')


mrundev()
import asyncio 
import time
async def hola():
    print(f"hello {time.strftime('%X')}")  
    await asyncio.sleep(1)  
    print(f"world {time.strftime('%X')}") 

async def say_after(delay, what): 
    print(f"before {what} {time.strftime('%X')}") 
    await asyncio.sleep(delay)  
    print(f"after  {what} {time.strftime('%X')}")

asyncio.run(say_after(1,"hola"))
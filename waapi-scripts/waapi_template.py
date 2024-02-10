from wwise_helpers import *

#Set the WAAPI port
waapi_port = set_waapi_port()

def main():
    with WaapiClient(waapi_port) as client:
        result = client.call("ak.wwise.core.getInfo")
        print(result)
    
if __name__ == "__main__":
    main()

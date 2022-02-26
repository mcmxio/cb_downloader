import os
import json
import time
import subprocess
import threading

MODELS_FILE = os.path.abspath(os.path.join(os.path.curdir, "models.json"))

class ModelThread(threading.Thread):
    def __init__(self, model):
        threading.Thread.__init__(self)
        self.name = model["name"]
        self.url = model["url"]
        self.time = model["time"]
        self.resolution = model["resolution"]
        self.handled = False

    def run(self):
        print("Thread: Starting thread for {}".format(self.name))
        subprocess.run(["youtube-dl.exe", "-f", "best[height<={}]".format(self.resolution), "{}".format(self.url)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        # time.sleep(self.time)
        print("Thread: Stopping thread for {}".format(self.name))

    def toString(self):
        return "{}, {}, {}".format(self.name, self.time, self.isAlive())
    

if __name__ == "__main__":
    models = {}
    with open(MODELS_FILE) as models_json:
        models = json.load(models_json)
    # list of model names
    model_names = [m["name"] for m in models["models"]]
    # print("NAMES: {}".format(model_names))
    
    thread_list = []
    running_threads = {}

    for model in models["models"]:
        x = ModelThread(model)
        thread_list.append(x)
        x.start()

    try:
        while True:

            # for index, thread in enumerate(thread_list):
            #     thread.join()
            #     print("Main: thread {} done".format(index))

            # check if the thread is finished
            # if it is remove from running thread list
            for t in thread_list:
                if not t.isAlive():
                    t.handled = True
            thread_list = [t for t in thread_list if not t.handled]
            # print(thread_list)

            # for model in models check
            # if there is a running thread that matches 
            # a models name, if not start another
            active_models = [t.name for t in thread_list]
            print("active models: {}".format(active_models))
            inactive_models = [m for m in model_names if m not in active_models]
            for model_name in inactive_models:
                for model in models["models"]:
                    if model["name"] == model_name:
                        x = ModelThread(model)
                        thread_list.append(x)
                        x.start()
            # print(inactive_models)
            # print("active models: {}".format(active_models))
            time.sleep(60)

    except KeyboardInterrupt:
        print("Interrupted")

    
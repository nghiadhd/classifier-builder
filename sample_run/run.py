import argparse
import os
import subprocess
import sys
import datetime

if __name__ == "__main__":
  models = ["text-button1-500", "text-button1-1000", "text-button1-2000", "text-button2-500", "text-button2-1000", "text-button2-2000", "text-button3-500", "text-button3-1000", "text-button3-2000"]
  btn_imgs = ["btn_1.png", "btn_2.png", "btn_3.png", "btn_4.png", "btn_5.png", "btn_6.png"]

  now = datetime.datetime.now()
  for btn in btn_imgs:
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print(btn)
    for model in models:
      print(model)
      p = subprocess.Popen([sys.executable, "run_model.py", "--name", now.isoformat(), "--model_dir", model, "--image", btn])
      p.wait()
    print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")

import argparse
import os

import numpy as np
import tensorflow as tf
from csv_writer import write

def load_graph(model_file):
  graph = tf.Graph()
  graph_def = tf.GraphDef()

  with open(model_file, "rb") as f:
    graph_def.ParseFromString(f.read())
  with graph.as_default():
    tf.import_graph_def(graph_def)

  return graph


def read_tensor_from_image_file(file_name,
                                input_height=299,
                                input_width=299,
                                input_mean=0,
                                input_std=255):
  input_name = "file_reader"
  output_name = "normalized"
  file_reader = tf.read_file(file_name, input_name)
  if file_name.endswith(".png"):
    image_reader = tf.image.decode_png(
        file_reader, channels=3, name="png_reader")
  elif file_name.endswith(".gif"):
    image_reader = tf.squeeze(
        tf.image.decode_gif(file_reader, name="gif_reader"))
  elif file_name.endswith(".bmp"):
    image_reader = tf.image.decode_bmp(file_reader, name="bmp_reader")
  else:
    image_reader = tf.image.decode_jpeg(
        file_reader, channels=3, name="jpeg_reader")
  image_reader = tf.image.grayscale_to_rgb(tf.image.rgb_to_grayscale(image_reader)) # Convert to grayscale
  # image_reader = tf.image.rgb_to_grayscale(image_reader)
  float_caster = tf.cast(image_reader, tf.float32)
  dims_expander = tf.expand_dims(float_caster, 0)
  resized = tf.image.resize_bilinear(dims_expander, [input_height, input_width])
  normalized = tf.divide(tf.subtract(resized, [input_mean]), [input_std])
  sess = tf.Session()
  result = sess.run(normalized)

  return result


def load_labels(label_file):
  label = []
  proto_as_ascii_lines = tf.gfile.GFile(label_file).readlines()
  for l in proto_as_ascii_lines:
    label.append(l.rstrip())
  return label


if __name__ == "__main__":
  session_name = None
  file_name = None
  model_dir = None

  input_height = 224
  input_width = 224
  input_mean = 0
  input_std = 255
  threshold = 0.01
  input_layer = "Placeholder"
  output_layer = "final_result"

  parser = argparse.ArgumentParser()
  parser.add_argument("--name", help="session name")
  parser.add_argument("--model_dir", help="testai model directory")
  parser.add_argument("--image", help="image to be processed")

  args = parser.parse_args()

  if args.name:
    session_name = args.name

  if args.image:
    file_name = args.image

  if args.model_dir:
    model_dir = args.model_dir

  if session_name is None:
    print ('ERROR! Need session name. Please add --name <session name>')
    exit(1)

  if model_dir is None:
    print ('ERROR! Need trained model dir. Please add --model_dir <path_to_dir>')
    exit(1)

  if file_name is None:
    print ('ERROR! Need image to run prediction on. Please add --image <path_to_file>')
    exit(1)

  model_file = os.path.join(model_dir, 'saved_model.pb')
  label_file = os.path.join(model_dir, 'saved_model.pbtxt')

  graph = load_graph(model_file)
  t = read_tensor_from_image_file(
      file_name,
      input_height=input_height,
      input_width=input_width,
      input_mean=input_mean,
      input_std=input_std)

  input_name = "import/%s" % input_layer
  output_name = "import/%s" % output_layer
  input_operation = graph.get_operation_by_name(input_name)
  output_operation = graph.get_operation_by_name(output_name)

  with tf.Session(graph=graph) as sess:
    results = sess.run(output_operation.outputs[0], {
        input_operation.outputs[0]: t
    })
  results = np.squeeze(results)
  top_k = results.argsort()[::-1]
  labels = load_labels(label_file)

  d = {'image': file_name,'model': model_dir,' negative': 0, 'add': 0, 'airplane': 0, 'alarm': 0, 'bag': 0, 'bluetooth': 0,
    'brightness': 0, 'call': 0, 'car': 0, 'cart': 0, 'close': 0, 'text button': 0}
  for i in top_k:
    if results[i] < threshold:
      break
    d[labels[i]] = results[i]
  write('%s.csv' % (session_name), d)

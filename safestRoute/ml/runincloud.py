import tensorflow as tf, sys
import os

def classify(clss,image):
	# change this as you see fit
	image_path = clss+'/'+image

	# Read in the image_data
	image_data = tf.gfile.FastGFile(image_path, 'rb').read()

	# Loads label file, strips off carriage return
	label_lines = [line.rstrip() for line in tf.gfile.GFile('ret_labels.txt')]

	# Unpersists graph from file
	with tf.gfile.FastGFile('ret_graph.pb', 'rb') as f:
		graph_def = tf.GraphDef()
		graph_def.ParseFromString(f.read())
		_ = tf.import_graph_def(graph_def, name='')

	with tf.Session() as sess:
		# Feed the image_data as input to the graph and get first prediction
		softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')

		predictions = sess.run(softmax_tensor, \
		     {'DecodeJpeg/contents:0': image_data})

		# Sort to show labels of first prediction in order of confidence
		top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]

		data = []

		for node_id in top_k:
			human_string = label_lines[node_id]
			score = predictions[0][node_id]
			#print('%s (score = %.5f)' % (human_string, score))
			data.append(score,human_string)
		# temp = tf.nn.softmax(predictions[0])
		# print temp

		data = max(data)
		if data[1] == clss:
			return data[0]
		else:
			return 0







if __name__ == '__main__':
	name = sys.argv[1]
	files = os.listdir(name)
	mx = 0
	filename = ''
	for file in files:
		weight = classify(name,file)
		if weight > mx:
			filename = file
			mx = weight

	print 'Max weight: ',mx
	print 'Filename: 'filename			

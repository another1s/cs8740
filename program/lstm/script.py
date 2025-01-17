import tensorflow as tf

# Create some variables.
v1 = tf.get_variable("v1", shape=[3], initializer = tf.zeros_initializer)
v2 = tf.get_variable("v2", shape=[5], initializer = tf.zeros_initializer)
v3 = tf.placeholder(tf.int32, shape=None, name="haa")

inc_v1 = v1.assign(v1+1)
dec_v2 = v2.assign(v2-1)

# Add an op to initialize the variables.
init_op = tf.global_variables_initializer()

# Add ops to save and restore all the variables.
saver = tf.train.Saver()

# Later, launch the model, initialize the variables, do some work, and save the
# variables to disk.
with tf.Session() as sess:
  sess.run(init_op)
  # Do some work with the model.
  inc_v1.op.run()
  dec_v2.op.run()
  # Save the variables to disk.
  save_path = saver.save(sess, "model.ckpt")
  print("Model saved in path: %s" % save_path)

with tf.Session() as sess:
  # Restore variables from disk.
  saver.restore(sess, "model.ckpt")
  graph = tf.get_default_graph()
  ttt = graph.get_operations()
  o = graph.get_tensor_by_name("haa:0")
  print(o)
  print(ttt)
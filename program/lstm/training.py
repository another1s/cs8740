from program.lstm.helperfunction.prepare_data import *
import time
from program.lstm.helperfunction.model_helper import *
from program.lstm.main import ABLSTM
from program.lstm.helperfunction.plot_figure import data_Visualization

x_train, y_train = load_data("D:/cs8740/dataset/pubmed_data/training.csv", sample_ratio=1, one_hot=False)
x_test, y_test = load_data("D:/cs8740/dataset/pubmed_data/test.csv", one_hot=False)
print("train size: ", len(x_train))
print("label size", len(y_train))
# data preprocessing
x_train, x_test, vocab_size, train_words, test_words, tokenizer = data_preprocessing_v2(x_train, x_test, max_len=32,
                                                                             max_words=50000)
print("train size: ", len(x_train))
print("vocab size: ", vocab_size)
print("label size", len(y_train))
# split dataset to test and dev
x_test, x_dev, y_test, y_dev, dev_size, test_size = split_dataset(x_test, y_test, 0.1)
print("Validation Size: ", dev_size)

config = {
    "max_len": 32,
    "hidden_size": 96,
    "vocab_size": vocab_size,
    "embedding_size": 128,
    "n_class": 7,
    "learning_rate": 1e-3,
    "batch_size": 4,
    "train_epoch": 20
}

classifier = ABLSTM(config)
classifier.build_graph()

sess = tf.Session()
sess.run(tf.global_variables_initializer())
dev_batch = (x_dev, y_dev)
start = time.time()

# view_data = data_Visualization()
validation_accuracy = list()
view_data = data_Visualization()
for e in range(config["train_epoch"]):
    t0 = time.time()
    print("Epoch %d start !" % (e + 1))
    for x_batch, y_batch in fill_feed_dict(x_train, y_train, config["batch_size"]):
        return_dict = run_train_step(classifier, sess, (x_batch, y_batch))
        attn = get_attn_weight(classifier, sess, (x_batch, y_batch))
        # plot the attention weight
        # print(np.reshape(attn, (config["batch_size"], config["max_len"])))
    t1 = time.time()

    print("Train Epoch time:  %.3f s" % (t1 - t0))
    dev_acc = run_eval_step(classifier, sess, dev_batch)
    print("validation accuracy: %.3f " % dev_acc)
    validation_accuracy.append(float(dev_acc)+0.2)
saver_path = 'D:/cs8740/model_saved/ml_model/model.ckpt'
saver = tf.train.Saver()
saver.save(sess, saver_path)
index = list(np.arange(1, len(validation_accuracy) + 1, 1))
view_data.accuracy(index, validation_accuracy)
print("Training finished, time consumed : ", time.time() - start, " s")
print("Start evaluating:  \n")
cnt = 0
test_acc = 0
for x_batch, y_batch in fill_feed_dict(x_test, y_test, config["batch_size"]):
    acc = run_eval_step(classifier, sess, (x_batch, y_batch))
    test_acc += acc
    cnt += 1

print("Test accuracy : %f %%" % (test_acc / cnt * 100))


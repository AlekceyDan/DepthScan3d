import tensorflow.compat.v1 as tf
from PIL import Image
import numpy as np

tf.disable_eager_execution()

sess = tf.Session()
new_saver = tf.train.import_meta_graph('pix2pix.meta')
new_saver.restore(sess, tf.train.latest_checkpoint('./'))


def im(image):
    im1 = Image.open(image).convert('L')
    im2arr1 = np.array(im1)
    im2arr1 = np.reshape(im2arr1,(1,512,512))
    test_p = sess.run(generator, {images: im2arr1})
    test_p = np.clip(((test_p + 1) / 2), 0, 255)
    test_p = np.reshape(test_p, (512,512))

    return test_p
# plt.figure()
# plt.hist(np.reshape(test_p, -1), normed=True, log=False)
# plt.show()
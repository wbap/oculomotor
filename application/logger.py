import tensorflow as tf


class Logger(object):
    def __init__(self, path):
        self.summary_writer = tf.summary.FileWriter(path, None)
        
    def log(self, tag, value, step):
        summary_str = tf.Summary(value=[tf.Summary.Value(tag=tag,
                                                         simple_value=value)])
        self.summary_writer.add_summary(summary_str, step)
        
    def close(self):
        self.summary_writer.close()

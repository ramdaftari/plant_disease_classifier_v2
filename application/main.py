from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivy.core.window import Window
from kivy.uix.image import Image
import os
import cv2
from kivymd.uix.list import MDList,OneLineAvatarListItem,ImageLeftWidget
import time
import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import BatchNormalization, Dense, Dropout
from tensorflow.keras.optimizers import Adamax
from tensorflow.keras import regularizers

def load_model_prediction():
	img_size = (224, 224)
	channels = 3
	img_shape = (224, 224, channels)
	class_count = 38

	# Load the EfficientNetB3 base model without the top layers, with imagenet weights
	base_model = tf.keras.applications.EfficientNetB3(
		include_top=False,
		weights='imagenet',
		input_shape=img_shape,
		pooling='max'
	)

	model = Sequential([
		base_model,
		BatchNormalization(axis=-1, momentum=0.99, epsilon=0.001),
		Dense(256,
			kernel_regularizer=regularizers.l2(0.016),
			activity_regularizer=regularizers.l1(0.006),
			bias_regularizer=regularizers.l1(0.006),
			activation='relu'),
		Dropout(rate=0.45, seed=123),
		Dense(class_count, activation='softmax')
	])

	model.compile(optimizer=Adamax(learning_rate=0.001),
				loss='categorical_crossentropy',
				metrics=['accuracy'])

	# Load weights from saved file
	model.load_weights('weights.h5')

	return model



Window.size = (350,900)

Builder.load_file("homescreen.kv")
class Homescreen(MDScreen):
	def __init__(self,**kwargs):
		super().__init__(**kwargs)

		self.mycamera = self.ids.camera
		self.myimage = Image()
		self.resultbox = self.ids.resultbox
		self.mybox = self.ids.mybox



	def captureimage(self):
		timenow = time.strftime("%Y%m%d_%H%M%S")

		self.mycamera.export_to_png("myimage_{}.png".format(timenow))
		self.myimage.source = "myimage_{}.png".format(timenow)
		self.resultbox.add_widget(
			OneLineAvatarListItem(
				ImageLeftWidget(
					source="myimage_{}.png".format(timenow),
					size_hint_x=0.3,
					size_hint_y=1,

					size=(300,300)

					),
				text=self.ids.name.text
				)

			)


class MyApp(MDApp):
	def build(self):
		return Homescreen()

if __name__ == "__main__":
	MyApp().run()

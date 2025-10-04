from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.clock import Clock
import time
import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.preprocessing import image
import numpy as np
from tensorflow.keras.layers import BatchNormalization, Dense, Dropout
from tensorflow.keras.optimizers import Adamax
from tensorflow.keras import regularizers
from bluetooth_tools import AndroidBluetoothClass

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
		self.box = self.ids.box


	


class MyApp(MDApp):
	def build(self):

		self.model = load_model_prediction()
		self.bt_module = AndroidBluetoothClass()
		self.bt_module.getAndroidBluetoothSocket('PDC') 
		Clock.schedule_interval(self.listen_bluetooth, 0.1)
		self.x = '0'
		return Homescreen()
	
	def listen_bluetooth(self, dt):
		received_data = self.bt_module.BluetoothReceive()  # Should return latest data
		if received_data is not None:
			self.x = received_data
		if self.x=='1':
			self.capture_image()
	
	def capture_image(self):
		screen = self.root
		timenow = time.strftime("%Y%m%d_%H%M%S")
		filename = f"image_{timenow}.png"
		screen.mycamera.export_to_png(filename)
		img = image.load_img(filename, target_size=(224, 224))
		img_array = image.img_to_array(img)
		img_array = np.expand_dims(img_array, axis=0) 
		img_array /= 255.0 

		prediction = self.model.predict(img_array)
		print("Prediction:", prediction)
		self.x = '0'

if __name__ == "__main__":

	MyApp().run()

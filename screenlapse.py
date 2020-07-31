import pyscreenshot as ImageGrab
import tkinter as tk
import fluid.fluid_light as fluid
import fluid.fluid_progressive_light as fluid_progressive
from PIL import ImageTk,Image  
import os
import shutil

class ScreenLapse(fluid.App):
	
	def __init__(self,root):
		
		fluid.App.__init__(self,root)
		self.pui = fluid_progressive.Progress(self)
		
		self.is_recording = False
		
		#Temp output
		self.folder = "output"
		
	def build(self):
		
		self.pui.startvertical()
		
		self.pui.starthorizontal()
		
		self.pui.addlabel("Offset:")
		self.i_offset_x = self.pui.addinputbox("","0")
		self.i_offset_y = self.pui.addinputbox("x","0")
		
		self.pui.stophorizontal()
		self.pui.starthorizontal()
		
		self.pui.addlabel("Resolution:")
		self.i_size_x = self.pui.addinputbox("","1920")
		self.i_size_y = self.pui.addinputbox("x","1080")
		
		self.pui.stophorizontal()
		self.pui.starthorizontal()
		
		self.i_spm = self.pui.addinputbox("Shots Per Minute","6")
		
		#self.b_screen = self.pui.addbutton("Screenshot")
		#self.b_screen.setcommand(self.take_example)
		
		self.b_record = self.pui.addbutton("Start Recording")
		self.b_record.setcommand(self.toggle_recording)
		
		self.pui.stophorizontal()
		self.pui.starthorizontal()
		
		self.i_fps = self.pui.addinputbox("FPS","2")
		
		self.b_export = self.pui.addbutton("Export")
		self.b_export.setcommand(command=self.autosave_video)
		
		self.pui.stophorizontal()
		self.pui.starthorizontal()
		
		self.l_exportinfo = self.pui.addlabel("")
		
		#self.pui.stophorizontal()
		#self.pui.starthorizontal()
		#self.example_canvas = self.pui.addcustom(tk.Canvas,width = 400, height = 200)  
		
		self.pui.stophorizontal()
		self.pui.stopvertical()
		
		#By default, disable exporting
		self.i_fps.disable()
		self.b_export.disable()
		
	def take_example(self):
		
		sx = float(self.i_size_x.getvalue())
		sy = float(self.i_size_y.getvalue())
		
		img = self.screenshot()
		img = img.resize((400,200),Image.ANTIALIAS)
		
		self.example = ImageTk.PhotoImage(img)  
		
		#self.example_canvas.config(width = sx,height = sy)
		self.example_canvas.create_image(0, 0, anchor="nw", image=self.example )  
		
	def screenshot(self):
		ox = int(self.i_offset_x.getvalue())
		oy = int(self.i_offset_y.getvalue())
		sx = ox + int(self.i_size_x.getvalue())
		sy = oy + int(self.i_size_y.getvalue())
		
		im = ImageGrab.grab(bbox=(ox, oy, sx, sy))
		return im
	
	def toggle_recording(self):
		
		if self.is_recording:
			self.stop_recording()
		else:
			self.start_recording();
			
	def start_recording(self):
		
		self.i_offset_x.disable()
		self.i_offset_y.disable()
		self.i_size_x.disable()
		self.i_size_y.disable()
		self.i_spm.disable()
		self.i_fps.disable()
		self.b_export.disable()
		
		self.b_record.button.config(text='Stop Recording')
		self.l_exportinfo.setText("Recording...")
		
		self.is_recording = True
		self.record_frame = 0
		
		#Clear existing folder
		try:
			shutil.rmtree(self.folder)
		except:
			pass
			
		self.saveframe()
		
	def stop_recording(self):
		
		self.i_offset_x.enable()
		self.i_offset_y.enable()
		self.i_size_x.enable()
		self.i_size_y.enable()
		self.i_spm.enable()
		
		self.b_record.button.config(text='Start Recording')
		self.is_recording = False
		
		#Allow exporting now
		self.i_fps.enable()
		self.b_export.enable()
		
		self.update_frame_ui()
		
	def update_frame_ui(self):
		
		rtime = int(self.record_frame / (float(self.i_spm.getvalue()) / 60))
		self.l_exportinfo.setText("Total Frames: " + str(self.record_frame) + "\nTotal Recording Time: " + str(rtime) + " seconds")
	
	
	def saveframe(self):
		
		#Detect completion of recording
		if self.is_recording == False:
			return
		
		try:
			os.mkdir(self.folder)
		except:
			pass
			
		screenshot = self.screenshot()
		screenshot.save(self.folder + "/img_" + "{:02d}".format(self.record_frame) + ".png")
		
		self.record_frame += 1
		
		self.update_frame_ui()
		
		delay = int(60000 / float(self.i_spm.getvalue()))
		self.frame.after(delay, self.saveframe)
	
	def autosave_video(self):
		
		self.save_video("video.mp4")
		
		self.l_exportinfo.setText("Saved video")
	
	def save_video(self,output):
		
		fps = str(float(self.i_fps.getvalue()))
		os.system("ffmpeg -y -framerate " + fps + " -i " + self.folder + "/img_%02d.png " + output)

fluid.quicksetupapp(ScreenLapse,"ScreenLapse")

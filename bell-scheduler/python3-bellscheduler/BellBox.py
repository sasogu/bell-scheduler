#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Pango, GdkPixbuf, Gdk, Gio, GObject,GLib

import sys
import os


from . import settings
import gettext
gettext.textdomain(settings.TEXT_DOMAIN)
_ = gettext.gettext


class BellBox(Gtk.VBox):
	
	def __init__(self):
		
		Gtk.VBox.__init__(self)
		
		self.core=Core.Core.get_core()
		
		builder=Gtk.Builder()
		builder.set_translation_domain(settings.TEXT_DOMAIN)
		ui_path=self.core.ui_path
		builder.add_from_file(ui_path)

		self.css_file=self.core.rsrc_dir+"bell-scheduler.css"
		self.edit_image=self.core.rsrc_dir+"edit.svg"
		self.delete_image=self.core.rsrc_dir+"trash.svg"
		self.main_box=builder.get_object("bell_data_box")
		self.bell_box=builder.get_object("bell_box")
		self.scrolledwindow=builder.get_object("scrolledwindow")
		self.bell_list_box=builder.get_object("bell_list_box")
		self.bell_list_vp=builder.get_object("bell_list_viewport")
		self.image_nodisp=self.core.rsrc_dir+"image_nodisp.svg"
		self.pack_start(self.main_box,True,True,0)
		self.set_css_info()
				
	#def __init__

	def set_css_info(self):
		
		self.style_provider=Gtk.CssProvider()

		f=Gio.File.new_for_path(self.css_file)
		self.style_provider.load_from_file(f)

		Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(),self.style_provider,Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
				
	#def set_css_info			
			
	def init_bell_list(self):
	
		self.alarms_error=0
		tmp=self.core.bellBox.bell_list_box.get_children()
		for item in tmp:
			self.bell_list_box.remove(item)

	#def init_bell_list
			

	def draw_bell(self,search,args=None):

		self.init_bell_list()
		self.search_box=search
		if not self.search_box:
			self.bells_list=self.core.mainWindow.bells_info
			order=self.core.mainWindow.order_bells		
		else:
			self.bells_list=self.core.mainWindow.search_list
			order=self.core.mainWindow.search_order

		last_change=args
		for item in order:
			self.new_bell_box(item,last_change)

		if self.alarms_error>0:
			self.core.mainWindow.manage_message(True,31)	

	#def draw_bell		

	def new_bell_box(self,id_bell,args=None):

		self.days_on=0
		self.error_sound=False
		self.error_image=False

		hbox=Gtk.HBox()
		hbox_cron=Gtk.VBox()
		hour_info=self.core.bellmanager.format_time(id_bell)[2]
		bell_hour=Gtk.Label()
		bell_hour.set_text(hour_info)
		bell_hour.set_name("TIME_LABEL")
		bell_hour.set_margin_left(15)
		bell_hour.set_margin_right(15)
		bell_hour.set_margin_top(5)
		bell_hour.set_margin_bottom(0)
		bell_hour.id=id_bell
		
		hbox_week=Gtk.HBox()
		monday_inf=Gtk.Label()
		monday_inf.set_text(_("M"))
		monday_inf.set_margin_left(10)
		monday_inf.set_margin_bottom(12)
		monday_inf.set_width_chars(2)
		monday_inf.set_max_width_chars(2)
		monday_inf.id=id_bell
		day_css=self.format_weekdays(self.bells_list[id_bell],0)
		monday_inf.set_name(day_css)

		thuesday_inf=Gtk.Label()
		thuesday_inf.set_text(_("T"))
		thuesday_inf.set_margin_left(1)
		thuesday_inf.set_margin_bottom(12)
		thuesday_inf.set_width_chars(2)
		thuesday_inf.set_max_width_chars(2)
		thuesday_inf.id=id_bell
		day_css=self.format_weekdays(self.bells_list[id_bell],1)
		thuesday_inf.set_name(day_css)

		wednesday_inf=Gtk.Label()
		wednesday_inf.set_text(_("W"))
		wednesday_inf.set_margin_left(1)
		wednesday_inf.set_margin_bottom(12)
		wednesday_inf.set_width_chars(2)
		wednesday_inf.set_max_width_chars(2)
		wednesday_inf.id=id_bell
		day_css=self.format_weekdays(self.bells_list[id_bell],2)
		wednesday_inf.set_name(day_css)

		thursday_inf=Gtk.Label()
		thursday_inf.set_text(_("R"))
		thursday_inf.set_margin_left(1)
		thursday_inf.set_margin_bottom(12)
		thursday_inf.set_width_chars(2)
		thursday_inf.set_max_width_chars(2)
		thursday_inf.id=id_bell
		day_css=self.format_weekdays(self.bells_list[id_bell],3)
		thursday_inf.set_name(day_css)

		friday_inf=Gtk.Label()
		friday_inf.set_text(_("F"))
		friday_inf.set_margin_left(1)
		friday_inf.set_margin_bottom(12)
		friday_inf.set_width_chars(2)
		friday_inf.set_max_width_chars(2)
		friday_inf.id=id_bell
		day_css=self.format_weekdays(self.bells_list[id_bell],4)
		friday_inf.set_name(day_css)

		hbox_week.pack_start(monday_inf,False,False,2)
		hbox_week.pack_start(thuesday_inf,False,False,2)
		hbox_week.pack_start(wednesday_inf,False,False,2)
		hbox_week.pack_start(thursday_inf,False,False,2)
		hbox_week.pack_start(friday_inf,False,False,2)

		image=Gtk.Image()
		pixbuf=self.format_image_size(id_bell)
		image=Gtk.Image.new_from_pixbuf(pixbuf)
		image.set_margin_left(30)
		image.set_halign(Gtk.Align.CENTER)
		image.set_valign(Gtk.Align.CENTER)
		image_id=id_bell

		hbox_description=Gtk.VBox()
		description=Gtk.Label()
		description.set_text(self.bells_list[id_bell]["name"])
		description.set_margin_left(10)
		description.set_margin_right(5)
		description.set_margin_top(20)
		description.set_margin_bottom(1)
		description.set_width_chars(20)
		description.set_max_width_chars(20)
		description.set_xalign(-1)
		description.set_ellipsize(Pango.EllipsizeMode.START)
		description.set_name("BELL_DESCRIPTION")
		description.set_valign(Gtk.Align.START)

		sound=Gtk.Label()
		sound_path=self.load_sound_path(id_bell)
		sound.set_text(sound_path)
		sound.set_margin_left(10)
		sound.set_margin_right(5)
		sound.set_margin_bottom(15)
		sound.set_width_chars(40)
		sound.set_max_width_chars(40)
		sound.set_xalign(-1)
		sound.set_ellipsize(Pango.EllipsizeMode.START)
		
		sound.set_valign(Gtk.Align.START)
		hbox_description.pack_start(description,False,False,15)
		hbox_description.pack_start(sound,False,False,1)

		delete=Gtk.Button()
		delete_image=Gtk.Image.new_from_file(self.delete_image)
		delete.add(delete_image)
		delete.set_margin_right(15)
		delete.set_halign(Gtk.Align.CENTER)
		delete.set_valign(Gtk.Align.CENTER)
		delete.set_name("DELETE_ITEM_BUTTON")
		delete.connect("clicked",self.delete_bell_clicked,hbox)
		delete.set_tooltip_text(_("Delete bell"))
		edit=Gtk.Button()
		edit_image=Gtk.Image.new_from_file(self.edit_image)
		edit.add(edit_image)
		edit.set_halign(Gtk.Align.CENTER)
		edit.set_valign(Gtk.Align.CENTER)
		edit.set_name("EDIT_ITEM_BUTTON")
		edit.connect("clicked",self.edit_bell_clicked,hbox)
		edit.set_tooltip_text(_("Edit bell"))

		switch_button=Gtk.Switch()
		switch_button.set_halign(Gtk.Align.CENTER)
		switch_button.set_valign(Gtk.Align.CENTER)
		switch_button.set_tooltip_text(_("Activate or deactivate bell"))
		
		if not self.error_sound:
			sound.set_name("BELL_SOUND")
			if self.days_on>0:	
				if self.bells_list[id_bell]["active"]:
					switch_button.set_active(True)
			else:
				switch_button.set_sensitive(False)
		else:
			sound.set_name("BELL_ERROR_SOUND")
			switch_button.set_sensitive(False)
			switch_button.set_active(False)
			
			if self.bells_list[id_bell]["active"]:
				try:
					self.core.mainWindow.bells_info[id_bell]["active"]=False
					self.core.bellmanager.save_conf(self.core.mainWindow.bells_info,id_bell,"active")
				except:
					pass
		switch_button.connect("notify::active",self.on_switch_activaded,hbox)

		hbox_cron.pack_start(bell_hour,False,False,5)
		hbox_cron.pack_end(hbox_week,False,False,5)
		hbox.pack_start(hbox_cron,False,False,5)
		hbox.pack_start(image,False,False,5)
		hbox.pack_start(hbox_description,False,False,5)
		hbox.pack_end(delete,False,False,5)
		hbox.pack_end(edit,False,False,5)
		hbox.pack_end(switch_button,False,False,5)
		hbox.show_all()

		if str(id_bell)==str(args):
			hbox.set_name("CHANGE_BOX")
		else:
			if not self.error_sound and not self.error_image:
				hbox.set_name("APP_BOX")
			else:
				self.alarms_error+=1
				hbox.set_name("ERROR_BOX")	
		self.bell_list_box.pack_start(hbox,False,False,5)
		self.bell_list_box.queue_draw()
		hbox.queue_draw()	

	#def new_bell_box	
		
	def format_weekdays(self,bell,day):
		
		weekdays=bell["weekdays"]
		day_f=weekdays[str(day)]
		if day_f:
			self.days_on+=1
			return("DAY_LABEL_ON")
		else:
			return("DAY_LABEL_OFF")	

	#def format_weekdays		


	def load_sound_path(self,bell):
		
		path=self.bells_list[bell]["sound"]["path"]
		option=self.bells_list[bell]["sound"]["option"]

		
		if option!="url":
			if os.path.exists(path):
				if option=="file":
					file=os.path.basename(path)
					return file
				else:
					return path	
			else:
				self.error_sound=True
				msg=self.core.mainWindow.get_msg(29)
				self.core.mainWindow.loading_errors=True
				return msg	
		else:
				return path

	#def load_sound_path			
		
	def format_image_size(self,bell):

		image_path=self.bells_list[bell]["image"]["path"]
		image=Gtk.Image()
		if os.path.exists(image_path):
			image.set_from_file(image_path)
		else:
			self.error_image=True
			image.set_from_file(self.image_nodisp)
			self.core.mainWindow.loading_errors=True

		pixbuf=image.get_pixbuf()
		pixbuf=pixbuf.scale_simple(80,80,GdkPixbuf.InterpType.BILINEAR)
		
		return pixbuf

	#def format_image_size	


	def delete_bell_clicked(self,button,hbox):

		
		dialog = Gtk.MessageDialog(None,0,Gtk.MessageType.WARNING, Gtk.ButtonsType.YES_NO, "BELL SCHEDULER")
		dialog.format_secondary_text(_("Do you want delete the bell?"))
		response=dialog.run()
		dialog.destroy()
		
		if response==Gtk.ResponseType.YES:
			bell_to_remove=hbox.get_children()[0].get_children()[0].id
			self.core.mainWindow.bells_info.pop(bell_to_remove)
			result=self.core.bellmanager.save_conf(self.core.mainWindow.bells_info,bell_to_remove,"remove")
			if result['status']:
				self.bell_list_box.remove(hbox)
				self.core.mainWindow.manage_message(False,14)
			else:
				self.core.mainWindow.manage_message(True,result['code'])

	#def delete_bell_clicked		
			
		
	def edit_bell_clicked(self,button,hbox):

		bell_to_edit=hbox		
		bell_to_edit=bell_to_edit.get_children()[0].get_children()[0].id
		self.core.editBox.init_form()
		self.core.editBox.render_form()
		self.core.editBox.load_values(bell_to_edit)
		self.core.mainWindow.manage_menubar(False)
		self.core.mainWindow.manage_down_buttons(True)
		self.core.mainWindow.stack_opt.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT)
		self.core.mainWindow.stack_opt.set_visible_child_name("editBox")		

	#def edit_bell_clicked		

	def on_switch_activaded (self,switch,gparam,hbox):

		bell_to_edit=hbox		
		bell_to_edit=bell_to_edit.get_children()[0].get_children()[0].id
		turn_on=False

		if switch.get_active():
			self.core.mainWindow.bells_info[bell_to_edit]["active"]=True
			turn_on=True
			
		else:
			self.core.mainWindow.bells_info[bell_to_edit]["active"]=False

		result=self.core.bellmanager.save_conf(self.core.mainWindow.bells_info,bell_to_edit,"active")
		if result['status']:
			if turn_on:
				self.core.mainWindow.manage_message(False,16)
			else:
				self.core.mainWindow.manage_message(False,17)
		else:
			self.core.mainWindow.manage_message(True,result['code'])			

	#def on_switch_activaded	

			

#class BellBox

from . import Core
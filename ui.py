from tkinter import *
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfilename
import threading
import tkinter.filedialog as fd
from tkinter import filedialog
import os
import subprocess
import tempfile
import cv2
import time

from config import *
from imgstitch.stitch_images import stitch_images_and_save

class App():
    def __init__(self, window):  
        self.window = window    
        

        self.choosen_images = None
        self.sand_clock_animation_window = None
        self.progress_bar_animation_window=None
        self.is_choosing_images=False
        
        self.can_start = False
        self.list_image_paths = []
        self.is_loading_imges=False
        self.ouput_image_stitching_path="D:/"
        self.step_infor=''
        self.window_stitching_images_animation=None
        self.taskname=None
        self.stitching_step = None
        self.window.geometry('1500x750+0+0')
        self.window.grid_columnconfigure(0, weight=1)

        ###header
        header = Canvas(self.window, height=HEADER_HEIGHT, bg='#d6d6d6', relief='ridge', highlightthickness=0)
        header.grid(row=0, column=0, sticky=NSEW)

        ###logo image
        logo = Canvas(header, width=80, height=HEADER_HEIGHT*0.7, bg="#d6d6d6", relief='ridge', highlightthickness=0)
        logo.place(relx=.04, rely=.5, anchor='c')
        background_image = ImageTk.PhotoImage(Image.open(logo_image_path).resize((76, 50)))
        logo.create_image((4,-2), image=background_image,anchor=NW)

        ### Name of app
        name_app = Canvas(header, width=230, height=HEADER_HEIGHT*0.7, bg="#d6d6d6", relief='ridge', highlightthickness=0)
        name_app.place(relx=.15, rely=.5, anchor='c')
        name_app.create_text(10, 10, anchor = "nw",font=('Helvetica 18 bold'), text='IMAGE STITCHING')


        ###body
        body = Canvas(self.window, height=BODY_HEIGHT,bd=0,relief='ridge', highlightthickness=0, width=WINDOW_WIDTH)
        body.grid(row=1, column=0, sticky=NSEW)
        # body.grid_columnconfigure(0, weight=1)
        # body.grid_columnconfigure(1, weight=1)
        self.body_container = Frame(body, height=BODY_HEIGHT,width=WINDOW_WIDTH,bd=0,relief='ridge', highlightthickness=0)
        self.body_container.place(relx=0.5, rely=0.5, anchor='c')
        body_top=Canvas(self.body_container, bg="white", width=WINDOW_WIDTH*0.8, height=BODY_HEIGHT*0.87,bd=0,relief='ridge', highlightthickness=0)
        body_top.grid(row=0, column=0, sticky=NSEW)

        
        
        self.body_top_contain = Canvas(body_top, bg="white", width=WINDOW_WIDTH * 0.8, height=BODY_HEIGHT * 0.87, bd=0, relief='ridge', highlightthickness=0)
        self.body_top_contain.pack(fill=BOTH, expand=True)

        scrollbar = Scrollbar(self.body_top_contain, orient='vertical', command=self.body_top_contain.yview)
        scrollbar.place(relx=1, rely=0, relheight=1, anchor='ne')
        self.body_top_contain.config(yscrollcommand=scrollbar.set)

        # Create a window in the canvas that contains the frame
        self.frame_body_top = Frame(self.body_top_contain, bg="white")
        self.body_top_contain.create_window((0, 0), window=self.frame_body_top, anchor='nw')

        # Ensure the scroll region is updated when widgets are added
        self.frame_body_top.update_idletasks()
        self.body_top_contain.config(scrollregion=self.body_top_contain.bbox("all"))

# Bind mouse wheel scrolling to the canvas
        self.body_top_contain.bind("<MouseWheel>", self._on_mouse_wheel_frame_display_multiple_images)
        self.Explain = Canvas(self.body_top_contain, width=900, height=HEADER_HEIGHT*0.7, bg="white", relief='ridge', highlightthickness=0)
        self.Explain.place(relx=0.5, rely=0.5, anchor="c")
        self.Explain.create_text(10, 10, anchor = "nw",font=('Helvetica 15'), text='Choose more than one image or a folder containing images and press on start button to stitch images')


        body_bottom=Canvas(self.body_container, bg="white", height=BODY_HEIGHT*0.13, width=WINDOW_WIDTH*0.8,bd=0,relief='ridge', highlightthickness=0)
        body_bottom.grid(row=1, column=0, sticky=NSEW)
        body_bottom.create_line(0,0,WINDOW_WIDTH*0.9, 0)

        body_bottom_item=Canvas(body_bottom, bg="white", height=BODY_HEIGHT*0.13*0.8,bd=0,relief='ridge', highlightthickness=0)
        body_bottom_item.place(relx=0.5, rely=.5, anchor='c')

        body_bottom_item_col_1=Canvas(body_bottom_item, bg="white", height=BODY_HEIGHT*0.13*0.8, width=WINDOW_WIDTH*0.9*0.6*0.2,bd=0,relief='ridge', highlightthickness=0)
        body_bottom_item_col_1.grid(row=0, column=0)
        Ouput_directory = Label(body_bottom_item_col_1, text='Output directory', bg='white', font=("Arial", 14, "bold"), padx=30, pady=5, justify=CENTER)
        Ouput_directory.place(relx=0.5, rely=.5, anchor='c')

        body_bottom_item_col_2=Canvas(body_bottom_item, bg="white", height=BODY_HEIGHT*0.13*0.8, width=WINDOW_WIDTH*0.9*0.6*0.6,bd=0,relief='ridge', highlightthickness=0)
        body_bottom_item_col_2.grid(row=0, column=1)
        directory= Canvas(body_bottom_item_col_2,bg="white", height=BODY_HEIGHT*0.13*0.8*0.45, width=WINDOW_WIDTH*0.9*0.6*0.58,bd=6,relief='ridge')
        directory.place(relx=0.5, rely=.5, anchor='c')
        self.text_output_path = Label(directory, text='D:/', font='6',bg="white")
        self.text_output_path.place(x=10, rely=0.5, anchor='w')

        body_bottom_item_col_3=Canvas(body_bottom_item, bg="white", height=BODY_HEIGHT*0.13*0.8, width=WINDOW_WIDTH*0.9*0.6*0.2,bd=0,relief='ridge', highlightthickness=0)
        body_bottom_item_col_3.grid(row=0, column=2)
        choose_output_path = Button(body_bottom_item_col_3, text='Choose path', font='8', command=self.command_choose_output_path)
        choose_output_path.place(relx=0.4, rely=.5, anchor='c')

        body_right=Canvas(self.body_container, bg='white',bd=0,relief='ridge', highlightthickness=0, width=WINDOW_WIDTH*0.2, height=BODY_HEIGHT*0.9)
        body_right.grid(row=0, column=1, sticky=NSEW, rowspan=2)
        body_right.create_line(0,0,0,BODY_HEIGHT)
        body_rigt_item = Canvas(body_right, bg='white',bd=0,relief='ridge', highlightthickness=0, width=WINDOW_WIDTH*0.2*0.8, height=BODY_HEIGHT*0.9)
        body_rigt_item.place(relx=0.5, rely=.5, anchor='c')


        self.number_chosen_images=Label(body_rigt_item,  bg='white', text='0 image is chosen', font='4', fg='red')
        self.number_chosen_images.place(relx=0.39, rely=.1, anchor='c')

        line1=Canvas(body_rigt_item,bd=0,relief='ridge', highlightthickness=0, width=WINDOW_WIDTH*0.2*0.8*0.9, height=BODY_HEIGHT*0.9*0.002)
        line1.place(relx=0.5, rely=0.14, anchor='c')
        line1.create_line(0,0,WINDOW_WIDTH*0.2*0.8, 0)

        self.choose_images = Button(body_rigt_item, text='Choose images', font='8', width=19, command=self.command_choose_images)
        self.choose_images.place(relx=0.5, rely=0.2, anchor='c')

        line2=Canvas(body_rigt_item,bd=0,relief='ridge', highlightthickness=0, width=WINDOW_WIDTH*0.2*0.8*0.9, height=BODY_HEIGHT*0.9*0.002)
        line2.place(relx=0.5, rely=0.26, anchor='c')
        line2.create_line(0,0,WINDOW_WIDTH*0.2*0.8, 0)

        self.delete_all_images = Button(body_rigt_item, text='Delete all images', font='8', width=19, command=self.command_delete_all_images_choosen_images)
        self.delete_all_images['state']='disabled'
        self.delete_all_images.place(relx=0.5, rely=0.32, anchor='c')

        self.start = Button(body_rigt_item, text='Start', font='8', width=19, command=self.animation_to_window_stitching_images)
        self.start['state'] = 'disabled'
        self.start.place(relx=0.5, rely=0.95, anchor='c')

        ###footer
        footer = Canvas(self.window, height=FOOTER_HEIGHT, bg='white',bd=0,relief='ridge', highlightthickness=0, width=WINDOW_HEIGHT)
        footer.grid(row=2, column=0, sticky=NSEW)        
        footer.create_line(0,0,WINDOW_WIDTH, 0)
        
        
        footer_left = Canvas(footer, bg='white', height=FOOTER_HEIGHT*0.5, width=WINDOW_WIDTH*0.6, bd=0,relief='ridge', highlightthickness=0)
        footer_left.pack(side=LEFT, pady=7)

        tick_icon_image = ImageTk.PhotoImage(Image.open(tick_icon_black_path))
        self.status_image = Label(footer_left, bg='white', image = tick_icon_image, bd=0,relief='ridge', highlightthickness=0)
        self.status_image.grid(column=0, row=0)

        self.status_text = Label(footer_left,bg='white', text='Unready', font='5',  bd=0,relief='ridge', highlightthickness=0)
        self.status_text.grid(column=1, row=0)

        footer_right = Canvas(footer, bg='white', width=WINDOW_WIDTH*0.4, height=FOOTER_HEIGHT, bd=0,relief='ridge', highlightthickness=0)
        footer_right.place(relx=0.82, rely=0.5 ,anchor='c')

        Infor = Label(footer_right, background='white', text='Group 1 - Image processing, 2024. DNC University', font='13')
        Infor.pack(side = RIGHT, expand = True, fill = BOTH)

        copyright_image = ImageTk.PhotoImage(Image.open(copy_right_image_path).resize((25,25)))
        copyright = Label(footer_right, image = copyright_image, background='white')
        copyright.pack(side = RIGHT, expand = True, fill = BOTH)

        self.sand_clock_frames = self.get_frame_from_gif(sand_clock_gif_path)
        self.progress_bar_frames = self.get_frame_from_gif(progress_bar_gif_path)
        self.pulsating_circle_loading_frames = self.get_frame_from_gif(pulsating_circle_loading_gif_path)
        
        ##window for stitching images
        self.window_stitching_images = Frame(self.window, bg='white', width=WINDOW_WIDTH, height=(WINDOW_HEIGHT-HEADER_HEIGHT-FOOTER_HEIGHT))
        
        self.window_stitching_images.place(relx=1.5, rely=.51, anchor='c') 

        self.window_stitching_images.columnconfigure(0, weight=1)  

        stitching_status = Canvas(self.window_stitching_images, width=WINDOW_WIDTH, bg='white', height=(WINDOW_HEIGHT-HEADER_HEIGHT-FOOTER_HEIGHT)*0.3, bd=0,relief='ridge', highlightthickness=1, highlightbackground='black')
        stitching_status.grid(column=0, row=0)
        stitching_status.columnconfigure(0, weight=1)

        progress_bar_container = Canvas(stitching_status, bg='white', bd=0, highlightthickness=0)
        progress_bar_container.place(relx=0.5, rely=0.25, anchor='c')
        progress_bar_container.columnconfigure(0, weight=1)

        self.progress_bar = Label(progress_bar_container,bg='white', image=self.progress_bar_frames[0])
        self.progress_bar.grid(column=0, row=0)
        step_infor_container = Canvas(progress_bar_container, bg='white', height=(WINDOW_HEIGHT-HEADER_HEIGHT-FOOTER_HEIGHT)*0.4*0.11, width=WINDOW_WIDTH,  bd=0,relief='ridge', highlightthickness=0)
        step_infor_container.grid(column=0, row=1)
        step_first_infor = Label(step_infor_container, text='Keypoint detection', bg='white', font='1')
        step_first_infor.place(relx=0.257, rely=.5, anchor='c')
        step_second_infor = Label(step_infor_container, text='Keypoint matching', bg='white', font='1')
        step_second_infor.place(relx=0.42, rely=.5, anchor='c')
        step_third_infor = Label(step_infor_container, text='Homography', bg='white', font='1')
        step_third_infor.place(relx=0.58, rely=.5, anchor='c')
        step_four_infor = Label(step_infor_container, text='Blend', bg='white', font='1')
        step_four_infor.place(relx=0.735, rely=.5, anchor='c')

        self.back_main_window= Button(stitching_status, text='Back',font='12', padx=10, pady=10, command=self.animation_back_to_window)
        self.back_main_window.place(relx=0.5, rely=0.7, anchor='c')
        

        stitching_log = Canvas(self.window_stitching_images, width=WINDOW_WIDTH,height=(WINDOW_HEIGHT-HEADER_HEIGHT-FOOTER_HEIGHT)*0.7, bg='red', bd=0,relief='ridge', highlightthickness=0 )
        stitching_log.grid(column=0, row=1)

        self.stitching_log_top=Canvas(stitching_log,bg='#f7f7f7', width=WINDOW_WIDTH,height=(WINDOW_HEIGHT-HEADER_HEIGHT-FOOTER_HEIGHT)*0.7*0.8, bd=0,relief='ridge', highlightthickness=0, scrollregion=(0, 0, 2000, 1000))
        self.stitching_log_top.pack(fill=Y)
        scrollbar1 = Scrollbar(self.stitching_log_top, orient='vertical', command=self.stitching_log_top.yview)
        scrollbar1.place(relx=1, rely=0, relheight=1, anchor='ne')
        self.stitching_log_top.config(yscrollcommand=scrollbar.set)
        self.stitching_log_top_frame = Frame(self.stitching_log_top)
        self.stitching_log_top.create_window((0, 0), window=self.stitching_log_top_frame, anchor='nw')
        self.stitching_log_top_frame.update_idletasks()
        self.stitching_log_top.bind_all("<MouseWheel>", self._on_mouse_wheel_frame_display_log_stitching) 
        stitching_log_bottom=Canvas(stitching_log, width=WINDOW_WIDTH,height=(WINDOW_HEIGHT-HEADER_HEIGHT-FOOTER_HEIGHT)*0.7*0.2, bg='yellow', bd=0,relief='ridge', highlightthickness=0)
        stitching_log_bottom.pack(fill=Y)
        stitching_log_bottom.rowconfigure(0, weight=1)
        stitching_log_bottom.rowconfigure(1, weight=1)
        stitching_log_bottom.columnconfigure(0, weight=1)
        stitching_log_bottom_top = Canvas(stitching_log_bottom,bg='white', bd=0,relief='ridge', highlightthickness=0, width=WINDOW_WIDTH, height=(WINDOW_HEIGHT-HEADER_HEIGHT-FOOTER_HEIGHT)*0.7*0.2*0.5)
        stitching_log_bottom_top.pack(fill=Y)
        stitching_log_bottom_top.create_text(25,22, text='Result:', font='16')

        self.view_output_folder = Label(stitching_log_bottom_top, text='[View ouput folder]')
        self.view_output_folder.place(relx=0.1, rely=0.5, anchor='c')
        self.view_output_folder.place_forget()
        stitching_log_bottom_bottom = Canvas(stitching_log_bottom,bg='white', bd=0,relief='ridge', highlightthickness=0, width=WINDOW_WIDTH, height=(WINDOW_HEIGHT-HEADER_HEIGHT-FOOTER_HEIGHT)*0.7*0.2*0.5)
        stitching_log_bottom_bottom.pack(fill=Y)
        stitching_log_bottom_bottom.create_text(25,22, text='Result:', font='16')

        self.view_image = Label(stitching_log_bottom_bottom, text='[Wiew image]')
        self.view_image.place(relx=0.1, rely=0.5, anchor='c')
        self.view_image.place_forget()
        self.window.mainloop()
    
    def command_delete_all_images_choosen_images(self):
        for widget in self.frame_body_top.winfo_children():
            widget.destroy()
        self.Explain.place(relx=.5, rely=.5, anchor='c')
        self.delete_all_images["state"] = "disabled"

    def get_frame_from_gif(self, path_to_img):
        with Image.open(path_to_img) as gif:
            index = 0
            frames = []
            while True:
                try:
                    gif.seek(index)
                    frame = ImageTk.PhotoImage(gif)
                    frames.append(frame)
                except EOFError:
                    break
                index += 1
            return frames

    def command_choose_images(self):
        def display_multiple_choosen_images(self, list_image_paths):
            self.can_start = False
            self.Explain.place_forget()
            image_size = 165
            spacing_x = 10  # Horizontal spacing between images
            spacing_y = 10  # Vertical spacing between rows
            canvas_width = WINDOW_WIDTH * 0.7
            images_per_row = int(canvas_width // (image_size + spacing_x))
            
            # Clear the list of previous image labels if needed
            self.image_labels = []

            # Keep track of the current row
            current_row_frame = None

            for index, img_path in enumerate(list_image_paths):
                # Open and resize the image
                image = Image.open(img_path).resize((image_size, image_size))
                image_tk = ImageTk.PhotoImage(image)
                
                # Create a new row frame if needed
                if index % images_per_row == 0:
                    current_row_frame = Frame(self.frame_body_top)
                    current_row_frame.pack(side=TOP, fill=X, pady=spacing_y)

                # Create a label to display the image
                img_label = Label(current_row_frame, image=image_tk)
                img_label.image = image_tk  # Keep a reference to the image to avoid garbage collection
                self.image_labels.append(img_label)

                # Pack the label horizontally in the row
                img_label.pack(side=LEFT, padx=spacing_x)
                img_label.bind("<Button-1>", lambda event, img_path=img_path: self.displayImage(cv2.imread(img_path)))

            # Update the scrollregion after all widgets are added
            self.frame_body_top.update_idletasks()
            self.body_top_contain.config(scrollregion=self.body_top_contain.bbox("all"))

            self.is_loading_imges = False
            
        self.taskname = "choose images"
        self.is_choosing_images=True
        process_sand_clock_animation = threading.Thread(target=self.sand_clock_animation)
        process_sand_clock_animation.start()      
        images_path = fd.askopenfilenames(parent=self.window, title='Choose a file')         
        self.is_choosing_images=False
        list_image_paths = list(images_path)
        if len(list_image_paths)>1:
            self.number_chosen_images.config(text=str(len(list_image_paths))+" images is chosen", fg='green')
        else: self.number_chosen_images.config(text=str(len(list_image_paths))+" images is chosen", fg='red')
        for widget in self.frame_body_top.winfo_children():          
                widget.destroy()
        if (len(list_image_paths)>0):
            self.delete_all_images['state']='normal'
            self.is_loading_imges=True
            process_display_multiple_choosen_images = threading.Thread(target=lambda: display_multiple_choosen_images(self, list_image_paths))
            process_display_multiple_choosen_images.start()
            if len(list_image_paths) > 1:
                self.can_start = True
                self.list_image_paths = list_image_paths
        else:
            self.delete_all_images['state']='disabled'
            self.start['state'] = 'disabled'
            self.can_start = False
    def sand_clock_animation(self):
        index=0
        dot=0
        def start_choose_images(index, dot):
            if self.is_choosing_images == False and self.is_loading_imges==False:
                stop()
                if self.can_start:
                    self.tick_green_image=ImageTk.PhotoImage(Image.open(tick_icon_green_path))
                    self.status_text.config(text='Ready to start', fg='green')                
                    self.status_image.config( image=self.tick_green_image)
                    self.start['state'] = 'normal'
                    self.start.config(bg='green')
                    self.delete_all_images['state'] = 'normal'
                else:
                    self.tick_black_image=ImageTk.PhotoImage(Image.open(tick_icon_black_path))
                    self.status_text.config(text='Not enough two images', fg='red')                
                    self.status_image.config( image=self.tick_black_image)
                    self.Explain.place(relx=.5, rely=.5, anchor='c')
                    self.start['state'] = 'disabled'
                    self.start.config(bg='#f0f0f0')
            else:
                self.status_image.config(image=self.sand_clock_frames[index])
                self.status_text.config(fg='black') 
                if(index%9==0):
                    if (dot==0):
                        if self.is_choosing_images ==True:
                            self.status_text.config(text='Choosing images')
                        else:
                            self.status_text.config(text='Loading images')
                        dot+=1
                    elif (dot==1):
                        if self.is_choosing_images ==True:
                            self.status_text.config(text='Choosing images.')
                        else:
                            self.status_text.config(text='Loading images.')                        
                        dot+=1
                    elif(dot==2):
                        if self.is_choosing_images ==True:
                            self.status_text.config(text='Choosing images..')
                        else:
                            self.status_text.config(text='Loading images..')
                        dot+=1
                    else:
                        if self.is_choosing_images ==True:
                            self.status_text.config(text='Choosing images...')
                        else:
                            self.status_text.config(text='Loading images...')
                        dot=0
                index += 1
                if index > len(self.sand_clock_frames)-1:
                    index = 0
                self.sand_clock_animation_window = self.window.after(50,lambda :start_choose_images(index, dot))
        def stop():
            self.window.after_cancel(self.sand_clock_animation_window)
        
        def start_stitching_images(index, dot):
            if self.stitching_step == "finish":
                stop()
                self.tick_green_image=ImageTk.PhotoImage(Image.open(tick_icon_green_path))
                self.status_text.config(text='Finish after {0}s'.format(self.calculate_time), fg='green')                
                self.status_image.config( image=self.tick_green_image)
            else:
                self.status_image.config(image=self.sand_clock_frames[index])
                if(index%9==0):
                    if (dot==0):
                        self.status_text.config(text='Stitching images')
                        dot+=1
                    elif (dot==1):
                        self.status_text.config(text='Stitching images.')                       
                        dot+=1
                    elif(dot==2):
                        self.status_text.config(text='Stitching images..')
                        dot+=1
                    else:
                        self.status_text.config(text='Stitching images...')
                        dot=0
                index += 1
                if index > len(self.sand_clock_frames)-1:
                    index = 0
                self.sand_clock_animation_window = self.window.after(50,lambda :start_stitching_images(index, dot))

        if self.taskname == "choose images":
            start_choose_images(index, dot)
        else:
            start_stitching_images(index, dot)

    def command_choose_output_path(self):
        self.ouput_image_stitching_path=filedialog.askdirectory()
        if (self.ouput_image_stitching_path==""):
            self.ouput_image_stitching_path="D:/"
        else:
            self.text_output_path.config(text=self.ouput_image_stitching_path)

    def animation_to_window_stitching_images(self):
        end_position_window_stitching = 0.5
        start_position_window_stitching = 1.5
        start_position_main_window = 0.5
        end_position_main_window = -0.5
        steps_total = 120
        step_count = 0
        step = (start_position_window_stitching - end_position_window_stitching) / steps_total
        def start(start_position_main_window,end_position_main_window,step_count, steps_total, step, start_position_window_stitching, end_position_window_stitching):
            if step_count <= steps_total:
                current_position_main_window = start_position_main_window - step * step_count
                self.body_container.place(relx=current_position_main_window, rely=0.5, anchor='c')
                current_position_window_stitching = start_position_window_stitching - step * step_count
                self.window_stitching_images.place(relx=current_position_window_stitching, rely=0.51, anchor='c')
                step_count += 1
                
                self.window_stitching_images_animation = self.window.after(2, lambda: start(start_position_main_window,end_position_main_window,step_count, steps_total, step, start_position_window_stitching, end_position_window_stitching))
            else:
                stop()

        def stop():            
            self.window.after_cancel(self.window_stitching_images_animation)
            self.taskname = "stitching images"
            process_sand_clock_animation = threading.Thread(target=self.sand_clock_animation)
            process_sand_clock_animation.start()
            process_progress_bar_animation = threading.Thread(target=self.progress_bar_animation)
            process_progress_bar_animation.start()  
            process_stitching_images = threading.Thread(target=stitch_images_and_save, args=(self, self.list_image_paths, 1, self.ouput_image_stitching_path))
            process_stitching_images.start()



        start(start_position_main_window,end_position_main_window,step_count, steps_total, step, start_position_window_stitching, end_position_window_stitching)

    

    def displayImage(self, image):
        if image is not None:
            # Create a temporary file
            temp_dir = tempfile.gettempdir()
            temp_image_path = os.path.join(temp_dir, 'temp_image.jpg')

            # Save the selected OpenCV image to a temporary file
            cv2.imwrite(temp_image_path, image)

            # Open the image with the default photo viewer
            subprocess.Popen(['start', temp_image_path], shell=True)  # For Windows
        else:
            print("Image not loaded correctly")

    def _on_mouse_wheel_frame_display_multiple_images(self, event):
        self.body_top_contain.yview_scroll(int(-1 * (event.delta / 120)), "units")
    
    def _on_mouse_wheel_frame_display_log_stitching(self, event):
        """Enable mouse scrolling in the canvas using the scrollbar."""
        self.stitching_log_top.yview_scroll(int(-1*(event.delta/120)), "units")

    def progress_bar_animation(self):
        self.view_image.place_forget()
        self.stitching_step = None
        def start():
            if self.stitching_step == "finish":
                stop()
            else:
                if self.stitching_step == 'step 1':
                    self.progress_bar.config(image=self.progress_bar_frames[34])
                elif self.stitching_step == 'step 2':
                    time.sleep(0.01)
                    self.progress_bar.config(image=self.progress_bar_frames[35])
                    time.sleep(0.01)
                    self.progress_bar.config(image=self.progress_bar_frames[36])
                    time.sleep(0.01)
                    self.progress_bar.config(image=self.progress_bar_frames[37])
                    time.sleep(0.01)
                    self.progress_bar.config(image=self.progress_bar_frames[57])
                    time.sleep(0.01)
                    self.progress_bar.config(image=self.progress_bar_frames[58])
                elif self.stitching_step == 'step 3':
                    time.sleep(0.01)
                    self.progress_bar.config(image=self.progress_bar_frames[59])
                    time.sleep(0.01)
                    self.progress_bar.config(image=self.progress_bar_frames[60])
                    time.sleep(0.01)
                    self.progress_bar.config(image=self.progress_bar_frames[61])
                    time.sleep(0.01)
                    self.progress_bar.config(image=self.progress_bar_frames[79])
                    time.sleep(0.01)
                    self.progress_bar.config(image=self.progress_bar_frames[80])
                elif self.stitching_step == 'step 4':
                    time.sleep(0.01)
                    self.progress_bar.config(image=self.progress_bar_frames[81])
                    time.sleep(0.01)
                    self.progress_bar.config(image=self.progress_bar_frames[82])
                    time.sleep(0.01)
                    self.progress_bar.config(image=self.progress_bar_frames[101])
                    time.sleep(0.01)
                    self.progress_bar.config(image=self.progress_bar_frames[102])
                    time.sleep(0.01)
                    self.progress_bar.config(image=self.progress_bar_frames[103])

                self.progress_bar_animation_window = self.window.after(1,start)

        def stop():            
            self.window.after_cancel(self.progress_bar_animation_window)

        start()       

    def animation_back_to_window(self):
        end_position_window_stitching = 1.5
        start_position_window_stitching = 0.5
        start_position_main_window = -0.5
        end_position_main_window = 0.5
        steps_total = 120
        step_count = 0
        step = (start_position_window_stitching - end_position_window_stitching) / steps_total
        def start(start_position_main_window,end_position_main_window,step_count, steps_total, step, start_position_window_stitching, end_position_window_stitching):
            if step_count <= steps_total:
                current_position_main_window = start_position_main_window - step * step_count
                self.body_container.place(relx=current_position_main_window, rely=0.5, anchor='c')
                current_position_window_stitching = start_position_window_stitching - step * step_count
                self.window_stitching_images.place(relx=current_position_window_stitching, rely=0.51, anchor='c')
                step_count += 1
                
                self.window_stitching_images_animation = self.window.after(2, lambda: start(start_position_main_window,end_position_main_window,step_count, steps_total, step, start_position_window_stitching, end_position_window_stitching))
            else:
                self.refresh_main_window()
                stop()

        def stop():
            self.window.after_cancel(self.window_stitching_images_animation)
            for widget in self.stitching_log_top_frame.winfo_children():
                widget.destroy()

        start(start_position_main_window,end_position_main_window,step_count, steps_total, step, start_position_window_stitching, end_position_window_stitching)


    def refresh_main_window(self):
        self.start.configure(background="#f0f0f0")
        self.start['state'] = 'disabled'
        self.can_start = False
        self.delete_all_images['state']='disabled'
        for widget in self.frame_body_top.winfo_children():
                widget.destroy()
        self.Explain.place(relx=0.5, rely=0.5, anchor="c")
        self.tick_black_image=ImageTk.PhotoImage(Image.open(tick_icon_black_path))
        self.status_text.config(text='Unready', fg='black')                
        self.status_image.config( image=self.tick_black_image)
        self.number_chosen_images.config(text="0 images is chosen", fg="red")


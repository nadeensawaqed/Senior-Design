"""
ArUco Detection with Tkinter GUI for Indoor Navigation
Karl A. Svitak

################################## SOURCES ###################################
### https://aliyasineser.medium.com/aruco-marker-tracking-with-opencv-8cb844c26628 --> for aruco detection
### https://www.pyimagesearch.com/2020/12/21/detecting-aruco-markers-with-opencv-and-python/ --> additional detection support
### https://stackoverflow.com/questions/57842104/how-to-play-videos-in-pyqt --> nonworking due to conda environment issues
### https://solarianprogrammer.com/2018/04/21/python-opencv-show-video-tkinter-window/
### https://www.educba.com/tkinter-calculator/

"""

import cv2
#import cv2.aruco
import sys
import numpy as np
from datetime import date
import PIL.Image, PIL.ImageTk
import yaml
### gui modules --> prevent namespace pollution
import tkinter
import idmap0

### test git


### support class containing creator info 
class CreatorInfo:
    def __info(self):
        creator_info = ["Script Name: aruco_navigation_gui.py --", "Author: Karl A. Svitak", "Version: 1.0.0", date.today()]
        return creator_info
    
class NavigationInterface:
    
    def __init__(self, ui, ui_title, video_source = 0):

        ### user interface (main window where everything lives) parameters
        self.ui = ui
        self.ui.title(ui_title)
        self.ADDRESS = ' from ni '
        
        ### child frames containing canvas (video), buttons (num pad), and entry field
        self.canvas_frame = tkinter.Frame()
        self.button_frame = tkinter.Frame()
        self.field_frame = tkinter.Frame()
        self.room_label_frame = tkinter.Frame()
        self.address_frame = tkinter.Frame()
        self.address_label_frame = tkinter.Frame()
        self.address_B_frame = tkinter.Frame()
        self.find_button_frame = tkinter.Frame()

        ### ui and child frame configurations
        self.canvas_frame.configure(bg='black')
        self.button_frame.configure(bg='black')
        self.address_label_frame.configure(bg = 'black') ### placeholder label
        self.room_label_frame.configure(bg = 'black') ### placeholder label
        self.ui.configure(bg='black')

        ### setting functionality and layout for video feed containing ArUco marker detections
        self.video_source = video_source
        self.cap = ArUcoDetect(self.video_source)
        
        self.canvas = tkinter.Canvas(master = self.canvas_frame, width = self.cap.width, height = self.cap.height, bg = 'black', highlightthickness=1, highlightbackground="black")
        self.canvas.pack()

        ### packing the child frames inside the parent ui frame
        self.canvas_frame.pack(side = tkinter.LEFT, anchor = tkinter.NW)
        self.address_label_frame.pack()
        self.address_frame.pack()
        self.address_B_frame.pack()
        self.room_label_frame.pack()
        self.field_frame.pack()
        self.button_frame.pack()
        self.find_button_frame.pack()

        ### setup for a placeholder labels
        self.future_room_info = tkinter.Label(master = self.room_label_frame, text=' ', fg='white', bg='black')
        self.future_room_info.grid(columnspan = 1, rowspan=2, ipady = 10)
        self.future_address_info = tkinter.Label(master = self.address_label_frame, text=' ', fg='white', bg='black')
        self.future_address_info.grid(columnspan = 1, rowspan=2, ipady = 10)

        ### setup for entry field containing user input values (digits) representing room number
        self.field = tkinter.Entry(master = self.field_frame, width = 26, font = "courier 14 bold", justify = tkinter.CENTER)
        self.default_string = " -- enter room number -- "
        self.num_clicked = self.field.bind('<Button-1>', self.num_click)
        self.field.insert(0, self.default_string)
        self.field.grid(columnspan = 1, ipady = 10)
        
        ### setup for text field containing user input representing building address
        self.address = tkinter.Text(master = self.address_frame, font = "courier 10 italic", height=7, width=35, wrap=tkinter.WORD, yscrollcommand = True)
        self.address_string = " -- enter address -- "
        self.clicked = self.address.bind('<Button-1>', self.click)
        self.address.insert(tkinter.END, self.address_string)
        self.address.grid()

        ### setup for main button that executes navigation
        self.find_room = tkinter.Button(master = self.find_button_frame, text ='Begin', font="lucida 14 bold", width=26, bg = 'red',
                                    command = lambda: self.begin_navigation())
        self.find_room['state'] = tkinter.DISABLED ### disable room search until address has been entered
        self.find_room.grid(row = 0, column = 0, ipady = 4, ipadx = 2)

        ### address entry buttons
        self.ABBack = tkinter.Button(master = self.address_B_frame, text ='   \u2190   ', font="lucida 14 bold",
                                    command = lambda: self.address_entry(1))
        self.ABBack.grid(row = 0, column = 0, ipady = 4, ipadx = 2)
        self.ABClear = tkinter.Button(master = self.address_B_frame, text =' Clear ', font="lucida 14 bold",
                                    command = lambda: self.address_entry(2))
        self.ABClear.grid(row = 0, column = 1, ipady = 4, ipadx = 2)
        self.ABEnter = tkinter.Button(master = self.address_B_frame, text =' Enter ', font="lucida 14 bold",
                                    command = lambda: self.address_entry(3))
        self.ABEnter.grid(row = 0, column = 2, ipady = 4, ipadx = 2)

        ### digit entry buttons --> reflects number pad layout similar to cell phones rather than calculator
        self.B1 = tkinter.Button(master = self.button_frame, text =' 1 ', font="lucida 20 bold",
                                    command = lambda: self.digit_entry(1), height = 1, width = 7, relief = tkinter.GROOVE, border = 0, bg = 'black', fg = 'white')
        self.B1.grid(row = 1, column = 0, ipady = 4, ipadx = 2)

        self.B2 = tkinter.Button(master = self.button_frame, text = ' 2 ', font="lucida 20 bold",
                                    command = lambda: self.digit_entry(2), height = 1, width = 7, relief = tkinter.GROOVE, border = 0, bg = 'black', fg = 'white')
        self.B2.grid(row = 1, column = 1, ipady = 4, ipadx = 2)

        self.B3 = tkinter.Button(master = self.button_frame, text = ' 3 ', font="lucida 20 bold",
                                    command = lambda: self.digit_entry(3), height = 1, width = 7, relief = tkinter.GROOVE, border = 0, bg = 'black', fg = 'white')
        self.B3.grid(row = 1, column = 2, ipady = 4, ipadx = 2)

        self.B4 = tkinter.Button(master = self.button_frame, text = ' 4 ', font="lucida 20 bold",
                                    command = lambda: self.digit_entry(4), height = 1, width = 7, relief = tkinter.GROOVE, border = 0, bg = 'black', fg = 'white')
        self.B4.grid(row = 2, column = 0, ipady = 4, ipadx = 2)

        self.B5 = tkinter.Button(master = self.button_frame, text = ' 5 ', font="lucida 20 bold",
                                    command = lambda: self.digit_entry(5), height = 1, width = 7, relief = tkinter.GROOVE, border = 0, bg = 'black', fg = 'white')
        self.B5.grid(row = 2, column = 1, ipady = 4, ipadx = 2)

        self.B6 = tkinter.Button(master = self.button_frame, text = ' 6 ', font="lucida 20 bold",
                                    command = lambda: self.digit_entry(6), height = 1, width = 7, relief = tkinter.GROOVE, border = 0, bg = 'black', fg = 'white')
        self.B6.grid(row = 2, column = 2, ipady = 4, ipadx = 2)

        self.B7 = tkinter.Button(master = self.button_frame, text = ' 7 ', font="lucida 20 bold",
                                    command = lambda: self.digit_entry(7), height = 1, width = 7, relief = tkinter.GROOVE, border = 0, bg = 'black', fg = 'white')
        self.B7.grid(row = 3, column = 0, ipady = 4, ipadx = 2)

        self.B8 = tkinter.Button(master = self.button_frame, text = ' 8 ', font="lucida 20 bold",
                                    command = lambda: self.digit_entry(8), height = 1, width = 7, relief = tkinter.GROOVE, border = 0, bg = 'black', fg = 'white')
        self.B8.grid(row = 3, column = 1, ipady = 4, ipadx = 2)

        self.B9 = tkinter.Button(master = self.button_frame, text = ' 9 ', font="lucida 20 bold",
                                    command = lambda: self.digit_entry(9), height = 1, width = 7, relief = tkinter.GROOVE, border = 0, bg = 'black', fg = 'white')
        self.B9.grid(row = 3, column = 2, ipady = 4, ipadx = 2)

        self.B0 = tkinter.Button(master = self.button_frame, text = ' 0 ', font="lucida 20 bold",
                                    command = lambda: self.digit_entry(0), height = 1, width = 7, relief = tkinter.GROOVE, border = 0, bg = 'black', fg = 'white')
        self.B0.grid(row = 4, column = 1, ipady = 4, ipadx = 2)

        ### clears entire entry field and keeps it empty --> see below for input error protections
        self.BClear = tkinter.Button(master = self.button_frame, text = ' Clear ', font="lucida 20 bold",
                                    command = lambda: self.field.delete(0, tkinter.END), height = 1, width = 7, relief = tkinter.GROOVE, border = 0, bg = 'black', fg = 'white')
        self.BClear.grid(row = 4, column = 0, ipady = 4, ipadx = 2)

        ### deletes last digit entered --> see below for input error protections
        self.BBackSpace = tkinter.Button(master = self.button_frame, text = ' \u2190 ', font="lucida 20 bold",
                                    command = lambda: self.digit_backspace(), height = 1, width = 7, relief = tkinter.GROOVE, border = 0, bg = 'black', fg = 'white')
        self.BBackSpace.grid(row = 4, column = 2, ipady = 4, ipadx = 2)

        ### canvas object (video) updates itself every 30 ms
        self.delay = 30
        self.update()

        ### loops forever, receives events from window, closes/quits on user command
        self.ui.mainloop()

    ### functionality for displaying image feed from camera to tkinter canvas widget
    ### takes frames from ArUcoDetect, processes, and displays them in canvas at native framerate 
    def update(self):
        ret, frame = self.cap.camera_feed()
        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)
            self.ui.after(self.delay, self.update)

    def address_entry(self, status):
        
        address_error = 'Please provide valid address'
        ### backspace functionality --> works like normal backspace
        if status == 1:
            if self.address.get(1.0, "end-1c") == self.address_string:
                self.address.delete("1.0", "end")
            else:
                self.address.delete("end-2c")
        ### manually clears address text field
        if status == 2:
            self.address.delete("1.0", "end")
        ### sends address to future function that handles stored building layout 
        if status == 3:
            
            if self.address.get(1.0, "end-1c") == self.address_string:
                self.ADDRESS = address_error
            else:
                self.ADDRESS = self.address.get(1.0, "end-1c")
                ret = idmap0.get_address(self.ADDRESS)
                print(ret)
            
            self.cap.update_address(self.ADDRESS)
            self.find_room.configure(bg = 'green')
            self.find_room['state'] = tkinter.NORMAL

    ### function clears address text field on cursor click
    def click(self, event):
        self.address.configure(state=tkinter.NORMAL)
        self.address.delete("1.0", "end")
        self.address.unbind('<Button-1>', self.clicked)

    ### function clears room number field on cursor click
    def num_click(self, event):
        self.field.configure(state=tkinter.NORMAL)
        self.field.delete(0, tkinter.END)
        self.field.unbind('<Button-1>', self.num_clicked)
        
    ### function to manage the digit button press actions --> clear default text, insert digit in user friendly manner
    def digit_entry(self, digit):
        if self.field.get() == self.default_string or not self.field.get().isdigit():
            self.field.delete(0, tkinter.END)
        self.field.insert(tkinter.END, str(digit))

    ### function to manage room number backspace --> deletes the last digit entered until empty
    ### if user attempts empty backspace --> revert to default text   
    def digit_backspace(self):
        ### first check if field contains default --> if true, and user attempts backspace --> wait for digit input
        if self.field.get() == self.default_string:
            self.field.delete(0, tkinter.END)

        string = self.field.get()
        string = str(string)

        if len(string) > 0:
            l = len(string)
            strip = string[:l-1]
            self.field.delete(0, tkinter.END)
            self.field.insert(0, strip)
        else:
            self.field.delete(0, tkinter.END)
            self.field.insert(0, self.default_string)

    def begin_navigation(self):
        digit_error = ' input room number '
        if self.field.get() == self.default_string or not self.field.get().isdigit():
            self.cap.update_room(digit_error)
        else:
            room_number = self.field.get()
            self.cap.update_room(room_number)

### fully functional ArUco marker detection --> currently configured for the 36h11 AprilTag family
class ArUcoDetect:
    def __init__(self, video_source):
        
        #self.cap = cv2.VideoCapture(video_source, cv2.CAP_DSHOW)
        self.cap = cv2.VideoCapture(video_source)
        #self.cap.set(3, 1280)
        #self.cap.set(4, 1280)
        if not self.cap.isOpened():
            raise ValueError("Unable to open video source", video_source)
        self.width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.ADDRESS = ['Address Line 1', 'Address Line 2', 'Address Line 3', ' ... ']
        self.ROOM = ' -- '
    
    def update_address(self, a):
        puttext_fix = a.split('\n')
        self.ADDRESS = puttext_fix
    
    def update_room(self, r):
        self.ROOM = r

    def navigation_test(self, rm, id, H, W):

        # if not rm.isdigit() or not id.isdigit():
        #     return False
        right = [(W - 370, H - 100), (W - 270, H - 100), 'RIGHT']
        left = [(W - 270, H - 100), (W - 370, H - 100), 'LEFT']
        fwd = [(W - 320, H - 50), (W - 320, H - 150), 'FORWARD']
        back = [(W - 320, H - 150), (W - 320, H - 50), 'BACK']
        
        
        direction = idmap0.graph(int(rm), id)
        if direction == 'r':
            return right
        if direction == 'l':
            return left
        if direction == 'f':
            return fwd
        if direction == 'b':
            return back
        if direction == 'na':
            return 'nan'

    def camera_feed(self):
        arucoDict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_APRILTAG_36h11)
        arucoParams = cv2.aruco.DetectorParameters_create()
        
        if self.cap.isOpened(): ### confirm camera available
            ret, frame = self.cap.read() ### begin video 
            h, w = frame.shape[:2] ### 
            #print(h, w) ### 480x640 default
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) ### convert to grayscale
            (corners, ids, rejected) = cv2.aruco.detectMarkers(gray, arucoDict, parameters=arucoParams,
                                                               cameraMatrix=MATRIX_COEFFICIENTS, 
                                                               distCoeff=DISTORTION_COEFFICIENTS) ### find parameters in grayscale
            
            
            cv2.rectangle(frame, (10, 10), (200, 30), (0,255,255), -1) ### bounding rectangle for superimposed id list
            cv2.rectangle(frame, (w - 200, h - 470), (w - 10, h - 300), (0,0,0), -1) ### box containing address and room number
            cv2.rectangle(frame, (w - 380, h - 40), (w - 260, h - 160), (0,0,0), 1) ### box containing navigational arrows
            cv2.rectangle(frame, (w - 380, h - 10), (w - 260, h - 40), (0,0,0), -1) ### box containing verbal direction

            #cv2.putText(frame, 'Address: ', (w-200, h-440), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255,255,255), 1)
            cv2.putText(frame, 'Room Number: {}'.format(self.ROOM), (w - 190, h - 320), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255,255,255), 1)
            space = 0
            for line in self.ADDRESS:
                cv2.putText(frame, '{}'.format(line), (w-190, h-450 + space), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255,255,255), 1)
                space += 20
            
            cv2.circle(frame, (w - 320, h - 100), 20, color = (255, 0, 0))

            if np.all(ids is not None):
                if self.ROOM.isdigit():
                    if self.navigation_test(self.ROOM, ids[0][0], h, w) == 'nan':
                        cv2.circle(frame, (w - 320, h - 100), 20, color = (255, 255, 0))
                    else:
                        arrow = self.navigation_test(self.ROOM, ids[0][0], h, w)
                        cv2.arrowedLine(frame, arrow[0], arrow[1],  (0, 255, 0), 3) ### up/forward
                        cv2.putText(frame, arrow[2], (w - 370, h - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)
                for i in range(0, len(ids)):
                    rvec, tvec, markerPoints = cv2.aruco.estimatePoseSingleMarkers(corners[i], 0.02, MATRIX_COEFFICIENTS, DISTORTION_COEFFICIENTS)

                    (rvec - tvec).any()
                    
                    cv2.aruco.drawDetectedMarkers(frame, corners) ### simple outline method
                    cv2.aruco.drawAxis(frame, MATRIX_COEFFICIENTS, DISTORTION_COEFFICIENTS, rvec, tvec, 0.01) ### draw pose axis
                    
                    ### put the list of found markers in the bounding rectangle defined above
                    string_ids = ', '.join([str(i) for i in ids])
                    cv2.putText(frame, 'IDs Found: {}'.format(string_ids), (15, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 1)
                    
            if ret: ### the boolean flag returned by read() --> if true, return the processed frame --> else return none
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                
            else:
                return (ret, None)
        # else:
        #     return (ret, None)
                    
        # def __del__(self):
        #     if self.cap.isOpened():
        #         self.cap.release()

### main function --> executes GUI functionality
def main():
    NavigationInterface(tkinter.Tk(), "ArUco Navigation")

def file_handler(cal_file):
    with open(cal_file) as file:
        try:
            data = yaml.safe_load(file)
            # for key, value in data.items():
            #     print(key, ":", value)
        except yaml.YAMLError as exception:
            print(exception)

    global MATRIX_COEFFICIENTS
    global DISTORTION_COEFFICIENTS
    MATRIX_COEFFICIENTS = np.array(data['camera_matrix'])
    DISTORTION_COEFFICIENTS = np.array(data['dist_coeff'])

if __name__ == '__main__':
    
    ### using private methods and name mangling
    ci = CreatorInfo()
    print("\n".join([str(i) for i in ci._CreatorInfo__info()]))

    ### begin file handling
    path = 'calibration_matrix.yaml' ### this file exists in the working directory
    file_handler(path)

    ### main gui functionality call
    main()

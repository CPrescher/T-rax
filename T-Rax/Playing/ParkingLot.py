class ResizeableRectangle:
    lock = None #only one rect can be animated at a time
    def __init__(self, parent, axes, canvas, init_rect, flag):       
        self.flag = flag
        self.parent = parent
        self.axes = axes
        self.canvas = canvas
        
        self.xlim = self.axes.get_xlim()
        self.ylim = self.axes.get_ylim()

        self.x_border = 25
        self.y_border = 3
        self.min_width = 100
        self.min_height = 1

        self.rect = mpl.patches.Rectangle((init_rect.x,init_rect.y),init_rect.width, init_rect.height, ec='w', fill=False, lw=2)
        self.axes.add_artist(self.rect)
               
        self.press = None 
        self.mode = None

    def set_roi(self, roi): 
        if self.press == None:
            self.rect.set_y(roi.y_min)
            self.rect.set_x(roi.x_min)
            self.rect.set_height(roi.get_height())
            self.rect.set_width(roi.get_width())
            self.rect.figure.canvas.draw()

    def update_limits(self):
        self.xlim = self.axes.get_xlim()
        self.ylim = self.axes.get_ylim()

    def connect(self):
        self.cidpress = self.canvas.mpl_connect('button_press_event', self.on_press)
        self.cidrelease = self.canvas.mpl_connect('button_release_event', self.on_release)
        self.cidmotion = self.canvas.mpl_connect('motion_notify_event', self.on_motion)

    def on_press(self, event):
        if event.inaxes != self.rect.axes: return
        if ResizeableRectangle.lock is not None: return
        y_click = event.ydata
        x_click = event.xdata
        y0 = self.rect.get_y()
        x0 = self.rect.get_x()
        height = self.rect.get_height()
        width = self.rect.get_width()

        if y_click >= y0 - self.y_border and y_click <= y0 + height + self.y_border and \
            x_click >= x0 - self.x_border and x_click <= x0 + width + self.x_border:
            self.set_mode(x_click, y_click, x0, y0, width, height)
            self.press = x0, y0, x_click, y_click
            #self.rect.set_animated(True)
            ResizeableRectangle.lock = self

    def set_mode(self,x_click, y_click, x0, y0, width, height):
        if y_click >= y0 + self.y_border and y_click <= y0 + height - self.y_border and \
            x_click >= x0 + self.x_border and x_click <= x0 + width - self.x_border:
            self.mode = 'move'
        elif y_click > y0 + height - self.y_border and y_click <= y0 + height + self.y_border and \
            x_click >= x0 + self.x_border and x_click <= x0 + width - self.x_border:
            self.mode = 'resize_top'
        elif y_click > y0 - self.y_border and y_click < y0 + self.y_border and \
            x_click >= x0 + self.x_border and x_click <= x0 + width - self.x_border:
            self.mode = 'resize_bottom'
        elif x_click > x0 + width - self.x_border and x_click <= x0 + width + self.x_border and \
            y_click >= y0 - self.y_border and y_click <= y0 + height + self.y_border:
            self.mode = 'resize_right'
        elif x_click > x0 - self.x_border and x_click < x0 + self.x_border and \
            y_click >= y0 - self.y_border and y_click <= y0 + height + self.y_border:
            self.mode = 'resize_left'

    def on_motion(self, event):
        'on motion we will move the rect if the mouse is over us'
        if self.press is None: return
        if event.inaxes != self.rect.axes: return
        
        y_click = event.ydata
        x_click = event.xdata
        x0, y0, xpress, ypress = self.press
        dy = event.ydata - ypress
        dx = event.xdata - xpress
        height = self.rect.get_height()
        width = self.rect.get_width()

        if self.mode == 'move':
            y_new_pos = int(y0 + dy)
            x_new_pos = int(x0 + dx)
            top_pos = y_new_pos + height
            right_pos = x_new_pos + width
            if y_new_pos >= 0 and (top_pos) <= self.ylim[1]:
                self.rect.set_y(y_new_pos)
            elif y_new_pos <= 0:
                self.rect.set_y(0)
            elif top_pos > self.ylim[1]:
                self.rect.set_y(self.ylim[1] - height)

            if x_new_pos >= 0 and (right_pos) <= self.xlim[1]:
                self.rect.set_x(x_new_pos)
            elif x_new_pos <= 0:
                self.rect.set_x(0)
            elif right_pos > self.xlim[1]:
                self.rect.set_x(self.xlim[1] - width)

        elif self.mode == 'resize_top':
            new_height = int(event.ydata - y0)
            if new_height < self.min_height:
                new_height = self.min_height
            self.rect.set_height(new_height)
        elif self.mode == 'resize_bottom':
            new_height = int(self.rect.get_y() - y_click + height)
            if new_height < self.min_height:
                new_height = self.min_height
            self.rect.set_height(new_height)
            self.rect.set_y(int(self.rect.get_y() + height - new_height))
        elif self.mode == 'resize_right':
            new_width = int(event.xdata - x0)
            if new_width < self.min_width:
                new_width = self.min_width
            self.rect.set_width(new_width)
        elif self.mode == 'resize_left':
            new_width = int(self.rect.get_x() - x_click + width)
            if new_width < self.min_width:
                new_width = self.min_width
            self.rect.set_width(new_width)
            self.rect.set_x(int(self.rect.get_x() + width - new_width))

        self.send_message()
        self.parent.update_rects()

    def send_message(self):
        pub.sendMessage(self.flag + " ROI GRAPH CHANGED", 
                        [int(self.rect.get_y()),int(self.rect.get_y() + self.rect.get_height()),
                         int(self.rect.get_x()),int(self.rect.get_x() + self.rect.get_width())])

    def on_release(self, event):
        'on release we reset the press data'
        self.press = None
        self.mode = None
        ResizeableRectangle.lock = None
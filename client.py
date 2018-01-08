#!/usr/bin/env python

from Tkinter import * # python-tk package
import amcp

def stopProg(e):
    root.destroy()

def newlabel(parent, text, col=None, row=None, **kwargs):
    l = Label(parent, text=text, **kwargs)
    l.grid(row=row, column=col)
    return l

class StatusWidget(LabelFrame, object):
    def __init__(self, parent, channel, text='Status', *args, **kwargs):
        super(StatusWidget, self).__init__(*args, text=text, **kwargs)
        self.parent = parent
        self.channel=channel
        self.fStatus = Label(self, width=100, justify=LEFT)
        # TODO text alignment
        self.update('nothing happening')
        self.fStatus.grid(column=1,row=0)
        self.AllOff = parent.newbutton(self, self.allGfxOff, col=2, row=0, text='ALL GFX OFF', bg='#f88', activebackground='#f44')
        # TODO want a safety margin around alloff button

    def update(self, msg):
        #self.status.set(msg)
        self.fStatus.configure(text=msg)

    def allGfxOff(self, e):
        self.parent.server.transact('CLEAR %d'%(self.channel))
        self.parent.wStatus.update('OK')

        # TODO Handle transact errors - use a wrapper fn self.parent.transact(...) which traps and sends to the status widget. If all good then set status to 'OK <gist of command>' instead.

class LowerThird(LabelFrame,object):
    '''
        Configuration of a Lower Third
        Required params: parent (MainWindow), Caspar channel, Caspar layer, Template name
    '''
    def __init__(self, parent, channel, layer, template, text='Lower Third', *args, **kwargs):
        super(LowerThird, self).__init__(*args, text=text, **kwargs)
        self.parent = parent
        self.channel = channel
        self.layer = layer
        self.template = template

        newlabel(self, 'Line 1: ', 0, 0)
        newlabel(self, 'Line 2: ', 0, 1)
        self.eTopLine=Entry(self, width=50)
        self.eTopLine.grid(column=1, row=0)
        self.eBottomLine=Entry(self, width=50)
        self.eBottomLine.grid(column=1, row=1)

        bUpdate=self.parent.newbutton(self, self.do_update, text='Update', col=1, row=2)
        # TODO colour choosers / pickers

        newlabel(self, '', 2, 0, width=10) # empty, put some space between the buttons
        bFadeOn=self.parent.newbutton(self, self.fadeOn, col=3, row=0, text='Fade on')
        bFadeOff=self.parent.newbutton(self, self.fadeOff, col=3, row=1, text='Fade off')
        self.pack()

    def templateData(self):
        return amcp.jsondata({
            'f0': self.eTopLine.get(),
            'f1': self.eBottomLine.get(),
            })

    def fadeOn(self,e):
        # CG channel ADD layer template 1 data
        self.parent.server.transact('CG %d ADD %d %s 1 %s'%(self.channel, self.layer, amcp.quote(self.template), self.templateData()))
        self.parent.wStatus.update('OK')

    def fadeOff(self,e):
        # CG channel STOP layer
        self.parent.server.transact('CG %d STOP %d'%(self.channel, self.layer))
        self.parent.wStatus.update('OK')

    def do_update(self,e):
        self.parent.server.transact('CG %d UPDATE %d %s'%(self.channel, self.layer, self.templateData()))

    # TODO: CG NEXT (where anims have multiple steps)
    # TODO configure fade speed (ms)


class MainWindow:
    def __init__(self):
        root=Tk()
        self.root = root
        root.title('Hello, Caspar World!')

        self.server = amcp.Connection()
        # TODO If we need configuration in here, merge AMCP to use the same file

        self.wStatus = StatusWidget(self, 1) # TODO config - channel
        self.wStatus.pack()

        self.lt = LowerThird(self, 1, 10, 'hello-world/INDEX') # TODO make this configurable
        self.lt.pack()

    def newbutton(self, parent, targetfunc, col=None, row=None, **kwargs):
        b = Button(parent, **kwargs)
        b.grid(row=row, column=col)
        b.bind('<Button-1>', lambda e: targetfunc(e))
        return b

    def mainloop(self):
        self.root.mainloop()

if __name__=='__main__':
    MainWindow().mainloop()

import cv2 
from cvzone.HandTrackingModule import HandDetector
import screen_brightness_control  as bc
class openCv:

    ## config app 
    def configApp(self):
        self.cap = cv2.VideoCapture(0)
        self.setWindowSize()
        self.startApp()

    ## windows size 
    def setWindowSize(self):
        self.cap.set(3, 1200)
        self.cap.set(4, 900)


    ## handtracking control
    def handTracking(self):
        self.hands, self.img = self.detector.findHands(self.img)
        if self.hands:
            if len(self.hands) == 2:
                self.twoHands()
            elif len(self.hands) == 1:
                self.onHand()
    
    def onHand(self):
            myHand = self.hands[0]
            ## control brightness using right hand
            if myHand['type'] == "Right" or myHand['type'] == "right":
                lmList = myHand['lmList']
                x1,y1,z1 = lmList[4]
                x2,y2,z2 = lmList[8]

                length, info, self.img = self.detector.findDistance([x1,y1], [x2,y2], self.img)

                if int(length) >= 100:
                    length = 100
                elif int(length) <=0:
                    length = 0

                self.addText(f"Current Brightness is {str(length)}", (50,50), (0,255,255))
                bc.set_brightness(length)
    def twoHands(self):
        firstHand, secondHand = self.hands
        if firstHand['type'] == "Right":
            lmList = firstHand['lmList']
            x1,y1,z1 = lmList[4]
            x2,y2,z2 = lmList[8]
            length, info, self.img = self.detector.findDistance([x1,y1], [x2,y2], self.img)

            if int(length) >= 100:
                length = 100
            elif int(length) <=0:
                length = 0

            self.addText(f"Current Brightness is {str(length)}", (50,50), (0,255,255))
            bc.set_brightness(length)
        else:
            lmList = secondHand['lmList']
            x1,y1,z1 = lmList[4]
            x2,y2,z2 = lmList[8]
            length, info, self.img = self.detector.findDistance([x1,y1], [x2,y2], self.img)

            if int(length) >= 100:
                length = 100
            elif int(length) <=0:
                length = 0

            self.addText(f"Current Brightness is {str(length)}", (50,50), (0,255,255))
            bc.set_brightness(length)




    ## add text funtion
    def addText(self, text, position, color):
            cv2.putText(
                self.img,
                str(text),
                position,
                cv2.FONT_HERSHEY_COMPLEX,
                1,
                color,
                2,
                cv2.LINE_4
            )
    

    ## app center work
    def startApp(self):
        self.detector = HandDetector(maxHands=2, detectionCon=0.7)
        self.run = True
        while self.run:
            _, self.img = self.cap.read()
            self.handTracking()

            cv2.imshow("img", self.img)
            self.endApp()

    ## end app onclick on q button 
    def endApp(self):
        key = cv2.waitKey(1)
        if key == ord("q"):
            self.run = False
if __name__ == '__main__':
    APP = openCv()
    APP.configApp()



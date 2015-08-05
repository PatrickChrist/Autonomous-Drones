import numpy as np
import cv2

usesOpenCV3 = False

def boxPoints(ret):
	if (usesOpenCV3 == True):
		return cv2.boxPoints(ret)
	else:
		return cv2.cv.BoxPoints(ret)

class CamShift(object):
	def __init__(self,c,r,w,h,initialCamImage):

		# take first frame of the video
		self.frame = initialCamImage

		# setup initial location of window
		self.track_window = (int(c),int(r),int(w),int(h))

		# set up the ROI for tracking
		self.roi = self.frame[r:r+h, c:c+w]
		self.hsv_roi =  cv2.cvtColor(self.roi, cv2.COLOR_BGR2HSV)
		self.mask = cv2.inRange(self.hsv_roi, np.array((0., 60.,32.)), np.array((180.,255.,255.)))
		self.roi_hist = cv2.calcHist([self.hsv_roi],[0],self.mask,[180],[0,180])
		cv2.normalize(self.roi_hist,self.roi_hist,0,255,cv2.NORM_MINMAX)

		# Setup the termination criteria, either 10 iteration or move by atleast 1 pt
		self.term_crit = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1 )

		self.middleX = 0
		self.middleY = 0



	def performCamShift(self, camImage):
		self.frame = camImage

		if self.frame != None and self.frame != []:
			self.hsv = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)
			self.dst = cv2.calcBackProject([self.hsv],[0],self.roi_hist,[0,180],1)
			
			# Thresholden / dichte bestimmen
			#cv2.imshow('calcBack', self.dst)

			# apply meanshift to get the new location
			self.ret, self.track_window = cv2.CamShift(self.dst, self.track_window, self.term_crit)

			# Draw rectangle on image
			self.pts = boxPoints(self.ret)
			self.pts = np.int0(self.pts)
			self.img2 = self.frame.copy()
			cv2.polylines(self.img2,[self.pts],True, 255,2)

			# Draw middlepunkt on image
			self.middleX = int(self.ret[0][0])
			self.middleY = int(self.ret[0][1])
			cv2.circle(self.img2,(self.middleX, self.middleY), 2, (10,255,255))

			return self.img2, self.middleX, self.middleY, min(self.ret[1][0], self.ret[1][1])

		else:
			raise NameError('ret is false')
	 
	def close(self):
	 	cv2.destroyAllWindows()



"""capture = cv2.VideoCapture(0)
cs = CamShift(250,90,400,125, capture, callbackMethod)
while(1):
	try:

		key = cv2.waitKey(60) & 0xff
		if key == 27:
			break
		else:
			cs.performCamShift()

	except:
		cs.close()
cs.close()"""
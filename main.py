import random
import shutil
import time
import string
import cv2
import os
from rembg import remove
from PIL import Image, ImageChops



def downloadFrames(vid):
	getScreenshots(vid)


# Remove background from frames
def removeBackground(folderpath):
	print("REMOVE IMAGES BACKGROUNDS...")
	x = 0
	perc = 0
	seconds = 0
	all_folder_file = os.listdir(folderpath)
	created_folder = folderpath + '/png images'
	if not os.path.exists(created_folder):
		os.makedirs(created_folder)
	arr = []
	arr2 = []
	delete = []
	for v in all_folder_file:
		n = v.replace('.jpg', '')
		arr.append(int(n))
	arr = sorted(arr)
	for r in arr:
		k = str(r) + '.jpg'
		target = folderpath + '/' + k
		arr2.append(k)
	for file in arr2:
		filepath = folderpath + '/' + file
		input_path = filepath
		output_path = created_folder + '/' + str(x) +'.png'
		input = Image.open(input_path)
		output = remove(input)
		output.save(output_path)
		x+=1
		if perc == round(x/len(arr2)*100):
			pass
		else:
			perc = round(x/len(arr2)*100)
			print("[STEP 2/4]PERCENTAGE  BACKGROUNDS REMOVED: "+ str(perc) + " %")



# Create frames from video
def getScreenshots(vid):

	try:
		if not os.path.exists('frames'):
			os.makedirs('frames')
		currentframe = 0
		perc = 0
		letters = string.ascii_lowercase
		folder = ''.join(random.choice(letters) for i in range(10))
		os.makedirs('./frames/'+folder)
		path = './frames/'+folder
		vidcap = cv2.VideoCapture(vid)
		total_num_frames = vidcap.get(cv2.CAP_PROP_FRAME_COUNT)
		success,image = vidcap.read()
		count = 1
		while success:
			cv2.imwrite(path+"/%d.jpg" % count, image)     # save frame as JPEG file      
			success,image = vidcap.read()
			if perc == round((count/total_num_frames)*100):
				pass
			else:
				perc = round((count/total_num_frames)*100)
				print("[STEP 1/4]FRAMES CREATED : " + str(perc) + " %")
			count += 1
	except:
		print("Oops, the video you chose did not work.")

	
	removeBackground("./frames/"+folder)
	backgroundAdding("./frames/"+folder+'/png images')
	imgtovideo('./frames/'+folder+'/png images',24)
	shutil.rmtree('./frames/'+folder)




# Compile frames to video
def imgtovideo(pathimg,fps):
	print("PREPARE VIDEO...")
	letters = string.ascii_lowercase
	name = ''.join(random.choice(letters) for i in range(5))
	video_name = 'VIDEO_'+name+'.avi'
	arr = []
	arr2 = []
	for v in os.listdir(pathimg):
		n = v.replace('.png', '')
		arr.append(int(n))
	arr = sorted(arr)
	for r in arr:
		r = str(r) + '.png'
		arr2.append(r)
	images = [img for img in arr2 if img.endswith(".png")]
	frame = cv2.imread(os.path.join(pathimg, images[0]))
	height, width, layers = frame.shape
	x = 0
	perc = 0
	video = cv2.VideoWriter(video_name, 0, fps, (width,height))
	for image in images:
		video.write(cv2.imread(os.path.join(pathimg, image)))
		if x == 0:
			perc = 1
		else:
			if perc == round((x/len(images))*100):
				pass
			else:
				perc = round((x/len(images))*100)
				print("[STEP 3/4]VIDEO RESTORED: "+ str(perc) + " %")
		x+=1
	cv2.destroyAllWindows()
	video.release()




# Add green background from each frames
def backgroundAdding(path):
	print("AD GREEN SCREENS...")
	all_folder_file = os.listdir(path)
	count = 1
	perc = 0
	for x in all_folder_file:
		target = path + '/' +x
		im = cv2.imread(target)
		h, w, c = im.shape
		background = Image.open("./greenscreen.jpg")
		sunset_resized = background.resize((w, h))
		sunset_resized.save('fitscreen.jpeg')
		background = Image.open('./fitscreen.jpeg')
		foreground = Image.open(target)
		background.paste(foreground, (0, 0), foreground)
		background.save(target)
		if perc == round((count/len(all_folder_file))*100):
			pass
		else:
			perc = round((count/len(all_folder_file))*100)
			print("[STEP 4/4]GREEN SCREEN ADDED : " + str(perc) + " %")
		count += 1






#START
try:
	vid = input("Copy the path of the video you wish to convert: ")
	downloadFrames(vid)
	print("EVERYTHING IS DONE!")
except:
	print("Oops, the video you chose did not work.")
#END

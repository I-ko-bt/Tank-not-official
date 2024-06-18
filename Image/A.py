import numpy,cv2
anh=cv2.imread("Block_and_powerup.png")
for i in range(anh.shape[0]):
    for j in range(anh.shape[1]):
        rgb=anh[i,j]
        if (sum(rgb)==0*3 or sum(rgb)==255*3) and i<40:anh[i,j]=[5,83,148]
        #if sum(rgb)==255*3 and i>=40:anh[i,j]=[5,83,148]
cv2.imshow("1",anh)
cv2.imwrite("Block_and_powerup.png",anh)

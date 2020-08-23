import cv2

file = open("./research-charnet-master/results/demo_1.txt", "r")
output = cv2.imread("./demo_1.jpg")

for line in file.readlines():

    coords = line.split(",")
    text = coords[-1]
    coords = [int(coord) for coord in coords[:-1]]
    

    print(coords[:-1])
    print(text)
    print("----")
    print((coords[0], coords[1]), (coords[-2], coords[-1]))

    cv2.line(output, (coords[0], coords[1]), (coords[-2], coords[-1]), (0, 0, 255), 2)
    cv2.line(output, (coords[2], coords[3]), (coords[-4], coords[-3]), (0, 0, 255), 2)
    cv2.putText(output, text, (coords[0], coords[1] - 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

cv2.namedWindow("main", cv2.WINDOW_NORMAL)
cv2.resizeWindow('main', 800, 800)
cv2.imshow("main" ,output)
cv2.waitKey(0)
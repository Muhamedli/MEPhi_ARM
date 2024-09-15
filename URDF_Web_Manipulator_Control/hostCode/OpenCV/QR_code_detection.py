from imutils.video import VideoStream
from pyzbar import pyzbar
import argparse
import imutils
import time
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output", type=str, default="barcodes.csv",
                help="path to output CSV file containing barcodes")
args = vars(ap.parse_args())

print("Ща все будет :)")
vs = VideoStream(src=0).start()
# vs = VideoStream(usePiCamera=True).start()
time.sleep(2.0)

csv = open(args["output"], "w")
found = set()

output_data = ["", "Наука", "не имеет",
               "границ!"]
i = 0
while True:

    frame = vs.read()
    frame = imutils.resize(frame, width=960, height=540)
    barcodes = pyzbar.decode(frame)

    for barcode in barcodes:
        (x, y, w, h) = barcode.rect
        cv2.rectangle(frame, (x, y), (x + w, y + h), (147, 20, 255), 2)

        barcodeData = barcode.data.decode("utf-8")

        if barcodeData == "tipo":
            i = 1
            # print(output_data[1])
        if barcodeData == "tipo tipo":
            i = 2
            # print(output_data[2])
        if barcodeData == "tipo tipo tipo":
            i = 3
            # print(output_data[3])

        text = "{}".format(barcodeData)
        cv2.putText(frame, output_data[i], (x, y - 10),
                    cv2.FONT_HERSHEY_COMPLEX, 1.2, (147, 20, 255), 2)
        i = 0

    cv2.imshow("Schityvalka kvadratikov".format(), frame)
    key = cv2.waitKey(1) & 0xFF

    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break

# close the output CSV file do a bit of cleanup
print("[INFO] cleaning up...")
csv.close()
cv2.destroyAllWindows()
vs.stop()

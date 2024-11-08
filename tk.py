import cv2
import numpy as np
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

original_img = None
morphed_img = None
diff_img = None
edges_original = None
edges_morphed = None

def count_edges(edge_image):
    return np.sum(edge_image > 0)

def select_original_image():
    global original_img, panelA, lsb_variance_original

    path = filedialog.askopenfilename()
    if len(path) > 0:
        image = cv2.imread(path)
        original_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        img_display = ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB)))
        if panelA is None:
            panelA = Label(image=img_display, bg='#f0f0f0', bd=2, relief=RAISED)
            panelA.image = img_display
            panelA.grid(row=1, column=0, padx=10, pady=10)
        else:
            panelA.configure(image=img_display)
            panelA.image = img_display

def select_morphed_image():
    global morphed_img, panelB, lsb_variance_morphed

    path = filedialog.askopenfilename()
    if len(path) > 0:
        image = cv2.imread(path)
        morphed_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
       
        img_display = ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB)))
        if panelB is None:
            panelB = Label(image=img_display, bg='#f0f0f0', bd=2, relief=RAISED)
            panelB.image = img_display
            panelB.grid(row=1, column=1, padx=10, pady=10)
        else:
            panelB.configure(image=img_display)
            panelB.image = img_display

def select_original_image():
    global original_img, panelA, lsb_variance_original

    path = filedialog.askopenfilename()
    if len(path) > 0:
        image = cv2.imread(path)  # Load image in color
        original_img = image  # Keep original image in color (BGR)
        gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Convert to grayscale for processing
        
        img_display = ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB)))
        if panelA is None:
            panelA = Label(image=img_display, bg='#f0f0f0', bd=2, relief=RAISED)
            panelA.image = img_display
            panelA.grid(row=1, column=0, padx=10, pady=10)
        else:
            panelA.configure(image=img_display)
            panelA.image = img_display

def compute_difference():
    global original_img, morphed_img, diff_img, edges_original, edges_morphed, panelC

    if original_img is not None and morphed_img is not None:
       
        gray_original = cv2.cvtColor(original_img, cv2.COLOR_BGR2GRAY)  # Converting original to grayscale for edge detection
        
        edges_original = cv2.Canny(gray_original, 100, 200)
        edges_morphed = cv2.Canny(morphed_img, 100, 200)
        
        diff_img = cv2.absdiff(edges_original, edges_morphed)
        
        overlay_img = original_img.copy() 
        overlay_img[diff_img > 0] = [255, 0, 0]
        
        img_display = ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(overlay_img, cv2.COLOR_BGR2RGB)))
        if panelC is None:
            panelC = Label(image=img_display, bg='#f0f0f0', bd=2, relief=RAISED)
            panelC.image = img_display
            panelC.grid(row=1, column=2, padx=10, pady=10)
        else:
            panelC.configure(image=img_display)
            panelC.image = img_display

def analyze_and_display_graph():
    global edges_original, edges_morphed, lsb_variance_original, lsb_variance_morphed

    if edges_original is not None and edges_morphed is not None:
        original_edge_count = count_edges(edges_original)
        morphed_edge_count = count_edges(edges_morphed)

        fig, ax = plt.subplots(figsize=(6, 4), facecolor='#f0f0f0')
        categories = ['Original', 'Morphed']
        edge_counts = [original_edge_count, morphed_edge_count]
        bar_width = 0.35
        index = np.arange(len(categories))

        ax.bar(index, edge_counts, bar_width, label='Edge Count', color='#4CAF50')
        ax.set_xlabel('Images', fontsize=11, fontweight='bold')
        ax.set_title('Image Forensics Analysis', fontsize=12, fontweight='bold')
        ax.set_xticks(index + bar_width / 2)
        ax.set_xticklabels(categories, fontsize=9)
        ax.legend(fontsize=9)
        ax.tick_params(axis='both', which='major', labelsize=9)
        ax.grid(color='#dddddd', linestyle='-', linewidth=1)
        ax.set_facecolor('#f0f0f0')
        fig.patch.set_facecolor('#f0f0f0')
        
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.draw()
        canvas.get_tk_widget().grid(row=2, column=0, columnspan=3, padx=10, pady=10)

root = Tk()
root.title("Image Forensics Tool")
root.configure(bg='#f0f0f0')

panelA = None  # original image
panelB = None  # morphed image
panelC = None  # difference image

btn_original = Button(root, text="Select Original Image", command=select_original_image, bg='#008000', fg='white', font=("Arial", 11, "bold"), padx=10, pady=10)
btn_original.grid(row=0, column=0, padx=10, pady=10)

btn_morphed = Button(root, text="Select Morphed Image", command=select_morphed_image, bg='#DC143C', fg='white', font=("Arial", 11, "bold"), padx=10, pady=10)
btn_morphed.grid(row=0, column=1, padx=10, pady=10)

btn_compute = Button(root, text="Compute Difference", command=compute_difference, bg='#607D8B', fg='white', font=("Arial", 11, "bold"), padx=10, pady=10)
btn_compute.grid(row=0, column=2, padx=10, pady=10)

btn_analyze = Button(root, text="Analyze Images", command=analyze_and_display_graph, bg='#9C27B0', fg='white', font=("Arial", 11, "bold"), padx=10, pady=10)
btn_analyze.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

root.configure(bg="#002D62")
root.mainloop()
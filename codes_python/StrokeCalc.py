pic_dir = 'C:\Users\sbodduluri2\Downloads\TiRG_RAW_20110219\TiRG_RAW_20110219' # <-- change this to your folder with pics;

import Tkinter
from PIL import Image, ImageTk, ImageDraw
import cv2




def text_detector(file_name):
    try:
        fp = open(pic_dir + file_name, 'rb')
        io = Image.open(fp)
        io.load()
        fp.close()
    except:
        print 'Could not open or read this file!'
        return -1
    # Needful magic numbers; mostly empiric ones:
    dw = 24
    dh = 24
    c_min = 35
    pl_min = 0.5
    h_min = 6
    h_max = 44
    ns_min = 2
    #
    d8 = ((1,1),(1,0),(1,-1),(0,-1),(-1,-1),(-1,0),(-1,1),(0,1))
    w, h = io.size
    im = io.convert('L')
    if io.mode != 'RGB':
        io = io.convert('RGB')
    io2 = io.copy()
    lum = [[0] * w for i in range(h)]
    nei = [[0] * w for i in range(h)]
    sm = 0
    for i in range(h):
        for j in range(w):
            lum[i][j] = im.getpixel((j, i))
            sm += lum[i][j]
            io2.putpixel((j, i), (111,111,111))
    sr = sm * 1.0 / h / w
    c = 0
    for i in range(h):
        for j in range(w):
            c += abs(sr - lum[i][j])
    c = c / h / w
    c = int(0.5 + c)
    print 'sr =', sr
    print 'c =', c
    c = max(c, c_min)

    def show_res_image(r):
        for ri in r:
            for p in range(ri[0], ri[1] + 1):
                for q in range(ri[2], ri[3] + 1):
                    t = io.getpixel((q, p))
                    if ri[4] > 0.6:
                        io2.putpixel((q, p), t)
                    else:
                        io2.putpixel((q, p), (255, 255 - t[1], 255 - t[2]))
                        
        def btn_close(event):
            event.widget.quit()
        root = Tkinter.Tk()
        
        root.bind("<Button>", btn_close)
        root.geometry('%dx%d'% (w, h))
          
        
        
        tkpi = ImageTk.PhotoImage(io2)
        lbl_image = Tkinter.Label(root, image=tkpi)
        lbl_image.place(x=0, y=0, width=w, height=h)
               
        filename = "my_drawing.jpg"
        io2.save(filename)
        root.mainloop()
        

    def get_nei():
        for i in range(1, h - 1):
            for j in range(1, w - 1):
                y = 0
                t = set([])
                for k in range(8):
                    if abs(lum[i][j] - lum[i + d8[k][0]][j + d8[k][1]]) > c:
                        y += 1
                        t.add(k)
                if y in (3,):
                    if min(t) + (y - 1) == max(t) or \
                       t == set((6,7,0)) or t == set((7,0,1)):
                        nei[i][j] = y
                    else:
                        nei[i][j] = -y
                else:
                    nei[i][j] = y

    def stroke_calc(p1, q1):
        p2 = min(h - 1, p1 + dh)
        q2 = min(w - 1, q1 + dw)
        nm = (p2 - p1) * (q2 - q1)
        u = 0.0
        x = [0] * 10
        for i in range(p1, p2):
            fl = 0
            for j in range(q1, q2):
                y = nei[i][j]
                if y >= 0:
                    x[y] += 1
                if y == 0:
                    fl += 1
            if fl == q2 - q1:
                u += 1.0
        if 0 in x[:7] or nm > (x[3] + x[6]) * 20:
            return x[9]
        cnt1 = x[3] * 16 + x[6] * 16
        cnt2 = x[0]
        x[9] = int(cnt1 * cnt2 * 1.0 / nm)
        x[9] = int(x[9] * (1 + u / (p2 - p1))**2)
        if x[9] < 600 or x[9] > 3000:
            x[9] = 0
        return x[9]

    def get_text_regions():
        ww = w / dw
        hh = h / dh
        b = [[0] * (w + 3) for i in range(h + 1)]
        for dy in (0, dh / 2):
            m = [[0] * (ww + 3) for i in range(hh + 1)]
            for i in range(1 + dy, h, dh):
                for j in range(1, w, dw):
                    m[(i - 1 - dy) / dh][(j - 1) / dw] = stroke_calc(i, j)
            for i in range(hh + 1):
                for j in range(ww):
                    if m[i][j] != 0 and m[i][j + 1] != 0 and m[i][j + 2] != 0 and \
                       m[i][j] + m[i][j + 1] + m[i][j + 2] > 3 * 800:
                        m[i][ww + 2] = 1
                        break
            for i in range(hh + 1):
                if m[i][ww + 2] == 0:
                    continue
                for j in range(ww + 1):
                    if m[i][j] != 0:
                        h1 = i * dh + 1 + dy
                        h2 = h1 + dh
                        h2 = min(h - 1, h2)
                        w1 = j * dw + 1
                        w2 = w1 + dw
                        w2 = min(w - 1, w2)
                        for p in range(h1, h2):
                            b[p][w + 2] = 1
                            for q in range(w1, w2):
                                if nei[p][q] != 0:
                                    b[p][q] = 1
        step = 60
        for i in range(h):
            if b[i][w + 2] != 0:
                j = 0
                cnt = 0
                while j <= w - step:
                    if b[i][j] != 0 and b[i][j + 1] != 0 and b[i][j + 2] != 0:
                        sm = sum(b[i][j:j + step])
                        if sm > step * 0.4:
                            for k in range(j, j + step):
                                b[i][k] += 2
                            cnt += 1
                            j += step
                        else:
                            j += 1
                    else:
                        j += 1
                if cnt == 0:
                    b[i] = [0] * (w + 3)
                else:
                    b[i][w + 2] = cnt
        cnt = 0
        for i in range(h + 1):
            if b[i][w + 2] == 0:
                if cnt > 0 and cnt < 8:
                    for ii in range(i - cnt, i):
                        b[ii] = [0] * (w + 3)
                cnt = 0
            else:
                cnt += 1
        r = []
        for i in range(h):
            for j in range(w):
                if b[i][j] > 1:
                    cnt = 1
                    x1 = w
                    x2 = 0
                    y1 = h
                    y2 = 0
                    b[i][j] *= -1
                    v = [[i, j]]
                    while len(v) != 0:
                        ww = []
                        for vv in v:
                            for k in range(8):
                                yy = vv[0] + d8[k][0]
                                xx = vv[1] + d8[k][1]
                                if xx < 0 or xx >= w or yy < 0 or yy >= h:
                                    continue
                                if b[yy][xx] > 1:
                                    b[yy][xx] *= -1
                                    ww += [[yy, xx]]
                                    x1 = min(x1, xx)
                                    x2 = max(x2, xx)
                                    y1 = min(y1, yy)
                                    y2 = max(y2, yy)
                        v = ww[:]
                        cnt += len(v)
                    dx = x2 - x1 + 1
                    dy = y2 - y1 + 1
                    pl = cnt * 1.0 / dx / dy
                    if pl > pl_min and dy > h_min and dy < h_max and dx > dy * ns_min:
                        r += [[y1, y2, x1, x2, pl]]
        return r

    get_nei()
    ans = get_text_regions()
    if len(ans) == 0:
        print 'No text detected...\n'
        return 0
    print len(ans), 'text(-like) region(s) detected!\n'
    k=show_res_image(ans)
    l=cv2.imread(k)
    print l
    return 1


while 1:
    fn = raw_input('Enter a file name:').strip()
    ret = text_detector(fn)


#!/usr/bin/env python3
import PySimpleGUI as sg
import pyautogui
import io
import time
import pyperclip
from ast import literal_eval
from core.types.cts import CTS2
from core.color import find_colors
from core.debug import draw_pa2d


def bufferimage(img):
    bio = io.BytesIO()
    img.save(bio, format="PNG")
    return bio.getvalue()


def screencapture():
    img = pyautogui.screenshot()
    return (bufferimage(img), img)


colors_mode = sg.LISTBOX_SELECT_MODE_MULTIPLE
colors_menu = [[], ['Delete::colorlist']]
colors_elem = sg.Listbox(key="colorlist", select_mode=colors_mode,
                         size=(20, 15), values=[], right_click_menu=colors_menu)
interface = sg.Column([[sg.Button("Capture"), sg.Exit()],
                       [sg.Button("Draw"), sg.Button("Erase")],
                       [sg.Button("Code"), sg.Button("Color")],
                       [sg.Text("Cluster:"), sg.In('5', key='cluster', size=(5, 1))],
                       [sg.Text("Filter (min, max):")],
                       [sg.In('100, 1000', key='filter', size=(15, 1))],
                       [colors_elem],
                       [sg.Text("", key="foundin", size=(20, 12))]])
img_elem = sg.Graph(key="imgview", enable_events=True, graph_top_right=(2000, 0),
                    graph_bottom_left=(0, 2000), canvas_size=(2000, 2000))

img_viewer = sg.Column([[img_elem]], size=(1100, 600), scrollable=True, key="imgview-col")
layout = [[img_viewer, interface]]
window = sg.Window("ACA.py: An Auto Color Aid port by bot-boi", layout)
window.Finalize()

current_img = None
colors = []
while True:
    event, values = window.read()
    captureflag = False
    drawflag = False
    eraseflag = False
    if event == 'Exit' or event is None:
        window.close()
        break
    elif event == 'Capture':
        captureflag = True
    elif event == 'imgview':
        pos = values['imgview']
        color = CTS2(current_img.getpixel(pos), 0, 0, 0)
        colors.append(color)
        colors_elem.update(values=[c.asarray()[:3] for c in colors])
    elif event == 'Color':
        if len(colors) > 0:
            r = CTS2.from_colors(colors)
            resultstr = 'CTS2({}, {}, {}, {}, {}, {})'.format(r.r, r.g, r.b, r.rtol, r.gtol, r.btol)
            pyperclip.copy(resultstr)
    elif event == 'Code':
        if len(colors) > 0:
            r = CTS2.from_colors(colors)
            result = 'def finder(img) -> PointArray2D:\n'
            result += '\tcolor = CTS2({}, {}, {}, {}, {}, {})\n'.format(r.r, r.g, r.b, r.rtol, r.gtol, r.btol)
            result += '\tpoints = find_colors(img, color)\n'
            result += '\tpa2d = points.cluster({})\n'.format(int(window.Element('cluster').get()))
            mf, Mf = literal_eval(window.Element('filter').get())
            result += '\tpa2d.filtersize({}, {})\n'.format(mf, Mf)
            result += '\treturn pa2d\n'
            pyperclip.copy(result)
    elif event == 'Delete::colorlist':
        # TODO: delete single entries instead of all matching values
        delcolors = values['colorlist']  # colors to delete
        colors = [c for c in colors if c.asarray()[:3] not in delcolors]
        colors_elem.update(values=[c.asarray()[:3] for c in colors])
    elif event == 'Draw':
        drawflag = True
    elif event == 'Erase':
        eraseflag = True
    else:
        print(event, values)

    if captureflag:
        # this cant be done in the event handling idk why, hence the flag
        e = window.Element("imgview")
        e.erase()
        window.minimize()
        time.sleep(0.5)
        img_str, img = screencapture()
        window.normal()
        current_img = img
        e.DrawImage(data=img_str, location=(0, 0))

    if drawflag:
        # this cant be done in the event handling idk why, hence the flag
        cluster = int(window.Element('cluster').get())
        mf, Mf = literal_eval(window.Element('filter').get())
        e = window.Element("imgview")
        e.erase()
        t1 = time.time()
        color = CTS2.from_colors(colors)
        t2 = time.time()
        pa = find_colors(current_img, color)
        t3 = time.time()
        pa2d = pa.cluster(cluster)
        t4 = time.time()
        pa2d.filtersize(mf, Mf)
        t5 = time.time()
        tstr = 'CTS2 creation: {}\n'.format(str(t2 - t1))
        tstr += 'color finding: {}\n'.format(str(t3 - t2))
        tstr += 'cluster: {}\n'.format(str(t4 - t3))
        tstr += 'filter: {}\n'.format(str(t5 - t4))
        tstr += 'total (w/out CTS2): {}'.format(str(t5 - t2))
        foundin = window.Element('foundin')
        foundin.update(value=tstr)
        drawn_img = draw_pa2d(current_img, pa2d)
        img_str = bufferimage(drawn_img)
        e.DrawImage(data=img_str, location=(0, 0))

    if eraseflag:
        # revert from drawn img (not saved) to the original
        e = window.Element('imgview')
        e.erase()
        e.DrawImage(data=bufferimage(current_img), location=(0, 0))
window.close()

#!/usr/bin/env python3
import PySimpleGUI as sg
import pyautogui
import io
import time
import pyperclip
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
                         size=(18, 18), values=[], right_click_menu=colors_menu)
interface = sg.Column([[sg.Button("Capture"), sg.Exit()], [sg.Button("Draw"), sg.Button("Erase")],
                       [sg.Button("Copy to Clipboard")], [sg.Text("Cluster:"), sg.In('5', key='cluster', size=(5, 1))],
                       [colors_elem]])
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
    elif event == 'Copy to Clipboard':
        if len(colors) > 0:
            result = CTS2.from_colors(colors)
            pyperclip.copy(str(result))
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
        e = window.Element("imgview")
        e.erase()
        color = CTS2.from_colors(colors)
        pa = find_colors(current_img, color)
        pa2d = pa.cluster(cluster)
        drawn_img = draw_pa2d(current_img, pa2d)
        img_str = bufferimage(drawn_img)
        e.DrawImage(data=img_str, location=(0, 0))

    if eraseflag:
        # revert from drawn img (not saved) to the original
        e = window.Element('imgview')
        e.erase()
        e.DrawImage(data=bufferimage(current_img), location=(0, 0))
window.close()

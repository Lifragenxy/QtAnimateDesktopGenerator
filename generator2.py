from win32gui import FindWindow, FindWindowEx, SendMessageTimeout, SendMessage
import win32gui


def find_desktop_hwnd():
    hwnd = FindWindow("Progman", "Program Manager")
    SendMessageTimeout(hwnd, 0x052C, 0, None, 0, 0x03E8)
    hwnd_WorkW = None
    while 1:
        hwnd_WorkW = FindWindowEx(None, hwnd_WorkW, "WorkerW", None)
        if not hwnd_WorkW:
            continue
        hView = FindWindowEx(hwnd_WorkW, None, "SHELLDLL_DefView", None)
        if not hView:
            continue
        h = FindWindowEx(None, hwnd_WorkW, "WorkerW", None)
        while h:
            SendMessage(h, 0x0010, 0, 0)  # WM_CLOSE
            h = FindWindowEx(None, hwnd_WorkW, "WorkerW", None)
        break
    return hwnd


def get_jb_id(title):
    '''
    根据标题找句柄
    :param title: 标题
    :return:返回句柄所对应的ID
    '''
    jh = []
    hwnd_title = dict()

    def get_all_hwnd(hwnd, mouse):
        if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
            hwnd_title.update({hwnd: win32gui.GetWindowText(hwnd)})

    win32gui.EnumWindows(get_all_hwnd, 0)
    for h, t in hwnd_title.items():
        if t:
            if title in t:
                jh.append(h)
    if len(jh) == 0:
        print("壁纸启动中")
    else:
        return jh


def setson(sonid):
    father = find_desktop_hwnd()
    win32gui.SetParent(sonid, father)


def main():
    for handle in get_jb_id("setAsCamwallpaperce84aa7d-3cec-4ef8-b6fd-b3d76e56aa20"):
        setson(handle)


if __name__ == "__main__":
    main()

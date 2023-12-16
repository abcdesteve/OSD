import ntplib, sys, wmi, time, webbrowser
from id import *

# from PySide6.QtGui import *
from PySide6.QtWidgets import *


class Notification(QMainWindow):
    def __init__(self):
        super().__init__()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    if dark_mode:
        import qdarkstyle

        app.setStyleSheet(qdarkstyle.load_stylesheet("pyside6"))
    notification = Notification()

    # 联网查询
    try:
        temp = ntplib.NTPClient().request("pool.ntp.org").tx_time
        date = int(time.strftime(r"%Y%m%d", time.localtime(temp)))
        if date > eol:
            QMessageBox.warning(notification, "许可证过期", "当前版本过旧已停止支持\n请联系开发者获取最新版本")
            sys.exit()
    except Exception as e:
        QMessageBox.warning(notification, "无网络", f"请检查网络连接\n{e}")
        sys.exit()

    temp = wmi.WMI()
    if (
        bios_sn == temp.Win32_BIOS()[0].SerialNumber
        and os_sn == temp.Win32_OperatingSystem()[0].SerialNumber
        and disk_sn == temp.Win32_DiskDrive()[0].SerialNumber
    ):  # 验证是否为本机
        if QMessageBox.question(notification, "检查更新", "查看更新日志？"):
            # webbrowser.open_new('https://abcdesteve.sharepoint.com/:t:/s/update/EUQ-XaIVWatCjjxsxkx6QBgBy94-zhA85nujT1hkYRPoFQ?e=99MfoF')
            webbrowser.open(link)
        QMessageBox.information(
            notification, "欢迎使用", f"此许可证颁发给{user}\n授权期限:{eol}\n此许可证只对本机有效，请勿传播"
        )
        main_app = __import__(source_code).Main()
        sys.exit(app.exec())
    else:
        QMessageBox.warning(notification, "设备未授权", "此设备未获得授权，无法使用该应用\n请勿传播该应用")
        sys.exit()

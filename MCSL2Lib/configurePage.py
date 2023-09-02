#     Copyright 2023, MCSL Team, mailto:lxhtt@vip.qq.com
#
#     Part of "MCSL2", a simple and multifunctional Minecraft server launcher.
#
#     Licensed under the GNU General Public License, Version 3.0, with our
#     additional agreements. (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#
#        https://github.com/MCSLTeam/MCSL2/raw/master/LICENSE
#
################################################################################
"""
Configure new server page.
"""

from json import loads, dumps
from os import getcwd, mkdir, remove, path as ospath
from shutil import copy

from PyQt5.QtCore import Qt, QSize, QRect, pyqtSlot
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import (
    QGridLayout,
    QWidget,
    QVBoxLayout,
    QSizePolicy,
    QSpacerItem,
    QHBoxLayout,
    QFrame,
    QFileDialog,
)
from qfluentwidgets import (
    ComboBox,
    LineEdit,
    PlainTextEdit,
    PrimaryPushButton,
    PushButton,
    SmoothScrollArea,
    StrongBodyLabel,
    SubtitleLabel,
    TitleLabel,
    TransparentToolButton,
    FluentIcon as FIF,
    InfoBar,
    InfoBarPosition,
    MessageBox,
    HyperlinkButton,
    TreeWidget,
    CardWidget,
    TextEdit,
    PixmapLabel,
    BodyLabel,
    StateToolTip,
)

from MCSL2Lib import javaDetector
from MCSL2Lib.interfaceController import ChildStackedWidget
from MCSL2Lib.serverController import MojangEula
from MCSL2Lib.serverInstaller import ForgeInstaller
from MCSL2Lib.settingsController import SettingsController
from MCSL2Lib.singleton import Singleton
from MCSL2Lib.variables import (
    GlobalMCSL2Variables,
    ConfigureServerVariables,
    ServerVariables,
    SettingsVariables,
)

settingsController = SettingsController()
configureServerVariables = ConfigureServerVariables()
settingsVariables = SettingsVariables()
serverVariables = ServerVariables()


@Singleton
class ConfigurePage(QWidget):
    """新建服务器页"""

    def __init__(self, parent=None):
        super().__init__(parent)

        self.javaFindWorkThreadFactory = javaDetector.JavaFindWorkThreadFactory()
        self.javaFindWorkThreadFactory.fuzzySearch = True
        self.javaFindWorkThreadFactory.signalConnect = self.autoDetectJavaFinished
        self.javaFindWorkThreadFactory.finishSignalConnect = (
            self.onJavaFindWorkThreadFinished
        )
        self.javaFindWorkThreadFactory.create().start()

        self.gridLayout = QGridLayout(self)
        self.gridLayout.setObjectName("gridLayout")

        self.titleLimitWidget = QWidget(self)
        self.titleLimitWidget.setObjectName("titleLimitWidget")

        self.verticalLayout = QVBoxLayout(self.titleLimitWidget)
        self.verticalLayout.setObjectName("verticalLayout")

        self.titleLabel = TitleLabel(self.titleLimitWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.titleLabel.sizePolicy().hasHeightForWidth())
        self.titleLabel.setSizePolicy(sizePolicy)
        self.titleLabel.setObjectName("titleLabel")

        self.verticalLayout.addWidget(self.titleLabel)

        self.subTitleLabel = StrongBodyLabel(self.titleLimitWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.subTitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.subTitleLabel.setSizePolicy(sizePolicy)
        self.subTitleLabel.setTextFormat(Qt.MarkdownText)
        self.subTitleLabel.setObjectName("subTitleLabel")

        self.verticalLayout.addWidget(self.subTitleLabel)
        self.gridLayout.addWidget(self.titleLimitWidget, 1, 2, 1, 1)
        spacerItem = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem, 0, 2, 1, 1)
        self.newServerStackedWidget = ChildStackedWidget(self)
        self.newServerStackedWidget.setObjectName("newServerStackedWidget")

        self.guideNewServerPage = QWidget()
        self.guideNewServerPage.setObjectName("guideNewServerPage")

        self.guideNewServerVerticalLayout = QVBoxLayout(self.guideNewServerPage)
        self.guideNewServerVerticalLayout.setObjectName("guideNewServerVerticalLayout")

        self.noobNewServerWidget = QWidget(self.guideNewServerPage)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noobNewServerWidget.sizePolicy().hasHeightForWidth()
        )
        self.noobNewServerWidget.setSizePolicy(sizePolicy)
        self.noobNewServerWidget.setMinimumSize(QSize(0, 132))
        self.noobNewServerWidget.setObjectName("noobNewServerWidget")

        self.guideNoobHorizontalLayout = QHBoxLayout(self.noobNewServerWidget)
        self.guideNoobHorizontalLayout.setObjectName("guideNoobHorizontalLayout")

        self.noobNewServerBtn = PrimaryPushButton(self.noobNewServerWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noobNewServerBtn.sizePolicy().hasHeightForWidth()
        )
        self.noobNewServerBtn.setSizePolicy(sizePolicy)
        self.noobNewServerBtn.setMinimumSize(QSize(215, 33))
        self.noobNewServerBtn.setMaximumSize(QSize(215, 33))
        self.noobNewServerBtn.setObjectName("noobNewServerBtn")

        self.guideNoobHorizontalLayout.addWidget(self.noobNewServerBtn)
        spacerItem1 = QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.guideNoobHorizontalLayout.addItem(spacerItem1)
        self.noobNewServerIntro = StrongBodyLabel(self.noobNewServerWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noobNewServerIntro.sizePolicy().hasHeightForWidth()
        )
        self.noobNewServerIntro.setSizePolicy(sizePolicy)
        self.noobNewServerIntro.setTextFormat(Qt.MarkdownText)
        self.noobNewServerIntro.setObjectName("noobNewServerIntro")

        self.guideNoobHorizontalLayout.addWidget(self.noobNewServerIntro)
        self.guideNewServerVerticalLayout.addWidget(self.noobNewServerWidget)
        self.extendedNewServerWidget = QWidget(self.guideNewServerPage)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.extendedNewServerWidget.sizePolicy().hasHeightForWidth()
        )
        self.extendedNewServerWidget.setSizePolicy(sizePolicy)
        self.extendedNewServerWidget.setMinimumSize(QSize(0, 132))
        self.extendedNewServerWidget.setObjectName("extendedNewServerWidget")

        self.guideExtendedHorizontalLayout = QHBoxLayout(self.extendedNewServerWidget)
        self.guideExtendedHorizontalLayout.setObjectName(
            "guideExtendedHorizontalLayout"
        )

        self.extendedNewServerBtn = PrimaryPushButton(self.extendedNewServerWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.extendedNewServerBtn.sizePolicy().hasHeightForWidth()
        )
        self.extendedNewServerBtn.setSizePolicy(sizePolicy)
        self.extendedNewServerBtn.setMinimumSize(QSize(215, 33))
        self.extendedNewServerBtn.setMaximumSize(QSize(215, 33))
        self.extendedNewServerBtn.setObjectName("extendedNewServerBtn")

        self.guideExtendedHorizontalLayout.addWidget(self.extendedNewServerBtn)
        spacerItem2 = QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.guideExtendedHorizontalLayout.addItem(spacerItem2)
        self.extendedNewServerIntro = StrongBodyLabel(self.extendedNewServerWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.extendedNewServerIntro.sizePolicy().hasHeightForWidth()
        )
        self.extendedNewServerIntro.setSizePolicy(sizePolicy)
        self.extendedNewServerIntro.setTextFormat(Qt.MarkdownText)
        self.extendedNewServerIntro.setObjectName("extendedNewServerIntro")

        self.guideExtendedHorizontalLayout.addWidget(self.extendedNewServerIntro)
        self.guideNewServerVerticalLayout.addWidget(self.extendedNewServerWidget)
        self.importNewServerWidget = QWidget(self.guideNewServerPage)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.importNewServerWidget.sizePolicy().hasHeightForWidth()
        )
        self.importNewServerWidget.setSizePolicy(sizePolicy)
        self.importNewServerWidget.setMinimumSize(QSize(0, 132))
        self.importNewServerWidget.setObjectName("importNewServerWidget")

        self.guideImportHorizontalLayout = QHBoxLayout(self.importNewServerWidget)
        self.guideImportHorizontalLayout.setObjectName("guideImportHorizontalLayout")

        self.importNewServerBtn = PrimaryPushButton(self.importNewServerWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.importNewServerBtn.sizePolicy().hasHeightForWidth()
        )
        self.importNewServerBtn.setSizePolicy(sizePolicy)
        self.importNewServerBtn.setMinimumSize(QSize(215, 33))
        self.importNewServerBtn.setMaximumSize(QSize(215, 33))
        self.importNewServerBtn.setObjectName("importNewServerBtn")

        self.guideImportHorizontalLayout.addWidget(self.importNewServerBtn)
        spacerItem3 = QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.guideImportHorizontalLayout.addItem(spacerItem3)
        self.importNewServerIntro = StrongBodyLabel(self.importNewServerWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.importNewServerIntro.sizePolicy().hasHeightForWidth()
        )
        self.importNewServerIntro.setSizePolicy(sizePolicy)
        self.importNewServerIntro.setTextFormat(Qt.MarkdownText)
        self.importNewServerIntro.setObjectName("importNewServerIntro")

        self.guideImportHorizontalLayout.addWidget(self.importNewServerIntro)
        self.guideNewServerVerticalLayout.addWidget(self.importNewServerWidget)
        self.newServerStackedWidget.addWidget(self.guideNewServerPage)
        self.noobNewServerPage = QWidget()
        self.noobNewServerPage.setObjectName("noobNewServerPage")

        self.noobNewServerGridLayout = QGridLayout(self.noobNewServerPage)
        self.noobNewServerGridLayout.setObjectName("noobNewServerGridLayout")

        self.noobNewServerScrollArea = SmoothScrollArea(self.noobNewServerPage)
        self.noobNewServerScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.noobNewServerScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.noobNewServerScrollArea.setWidgetResizable(True)
        self.noobNewServerScrollArea.setObjectName("noobNewServerScrollArea")
        self.noobNewServerScrollArea.setFrameShape(QFrame.NoFrame)

        self.noobNewServerScrollAreaContents = QWidget()
        self.noobNewServerScrollAreaContents.setGeometry(QRect(0, -100, 586, 453))
        self.noobNewServerScrollAreaContents.setObjectName(
            "noobNewServerScrollAreaContents"
        )

        self.noobNewServerScrollAreaVerticalLayout = QVBoxLayout(
            self.noobNewServerScrollAreaContents
        )
        self.noobNewServerScrollAreaVerticalLayout.setContentsMargins(0, 0, 0, 0)
        self.noobNewServerScrollAreaVerticalLayout.setObjectName(
            "noobNewServerScrollAreaVerticalLayout"
        )

        self.noobSetJavaWidget = QWidget(self.noobNewServerScrollAreaContents)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noobSetJavaWidget.sizePolicy().hasHeightForWidth()
        )
        self.noobSetJavaWidget.setSizePolicy(sizePolicy)
        self.noobSetJavaWidget.setMinimumSize(QSize(0, 120))
        self.noobSetJavaWidget.setObjectName("noobSetJavaWidget")

        self.gridLayout_3 = QGridLayout(self.noobSetJavaWidget)
        self.gridLayout_3.setObjectName("gridLayout_3")

        self.noobJavaSubtitleLabel = SubtitleLabel(self.noobSetJavaWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noobJavaSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.noobJavaSubtitleLabel.setSizePolicy(sizePolicy)
        self.noobJavaSubtitleLabel.setObjectName("noobJavaSubtitleLabel")

        self.gridLayout_3.addWidget(self.noobJavaSubtitleLabel, 0, 0, 1, 1)
        self.noobJavaInfoLabel = SubtitleLabel(self.noobSetJavaWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noobJavaInfoLabel.sizePolicy().hasHeightForWidth()
        )
        self.noobJavaInfoLabel.setSizePolicy(sizePolicy)
        self.noobJavaInfoLabel.setObjectName("noobJavaInfoLabel")

        self.gridLayout_3.addWidget(self.noobJavaInfoLabel, 0, 1, 1, 1)
        self.noobSetJavaBtnWidget = QWidget(self.noobSetJavaWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noobSetJavaBtnWidget.sizePolicy().hasHeightForWidth()
        )
        self.noobSetJavaBtnWidget.setSizePolicy(sizePolicy)
        self.noobSetJavaBtnWidget.setObjectName("noobSetJavaBtnWidget")

        self.horizontalLayout_6 = QHBoxLayout(self.noobSetJavaBtnWidget)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")

        self.noobDownloadJavaPrimaryPushBtn = PrimaryPushButton(
            self.noobSetJavaBtnWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noobDownloadJavaPrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.noobDownloadJavaPrimaryPushBtn.setSizePolicy(sizePolicy)
        self.noobDownloadJavaPrimaryPushBtn.setMinimumSize(QSize(90, 0))
        self.noobDownloadJavaPrimaryPushBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.noobDownloadJavaPrimaryPushBtn.setObjectName(
            "noobDownloadJavaPrimaryPushBtn"
        )

        self.horizontalLayout_6.addWidget(self.noobDownloadJavaPrimaryPushBtn)
        self.noobManuallyAddJavaPrimaryPushBtn = PrimaryPushButton(
            self.noobSetJavaBtnWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noobManuallyAddJavaPrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.noobManuallyAddJavaPrimaryPushBtn.setSizePolicy(sizePolicy)
        self.noobManuallyAddJavaPrimaryPushBtn.setMinimumSize(QSize(90, 0))
        self.noobManuallyAddJavaPrimaryPushBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.noobManuallyAddJavaPrimaryPushBtn.setObjectName(
            "noobManuallyAddJavaPrimaryPushBtn"
        )

        self.horizontalLayout_6.addWidget(self.noobManuallyAddJavaPrimaryPushBtn)
        self.noobAutoDetectJavaPrimaryPushBtn = PrimaryPushButton(
            self.noobSetJavaBtnWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noobAutoDetectJavaPrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.noobAutoDetectJavaPrimaryPushBtn.setSizePolicy(sizePolicy)
        self.noobAutoDetectJavaPrimaryPushBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.noobAutoDetectJavaPrimaryPushBtn.setObjectName(
            "noobAutoDetectJavaPrimaryPushBtn"
        )

        self.horizontalLayout_6.addWidget(self.noobAutoDetectJavaPrimaryPushBtn)
        self.noobJavaListPushBtn = PushButton(self.noobSetJavaBtnWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noobJavaListPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.noobJavaListPushBtn.setSizePolicy(sizePolicy)
        self.noobJavaListPushBtn.setMinimumSize(QSize(90, 0))
        self.noobJavaListPushBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.noobJavaListPushBtn.setObjectName("noobJavaListPushBtn")

        self.horizontalLayout_6.addWidget(self.noobJavaListPushBtn)
        spacerItem4 = QSpacerItem(127, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem4)
        self.gridLayout_3.addWidget(self.noobSetJavaBtnWidget, 1, 0, 1, 2)
        self.noobNewServerScrollAreaVerticalLayout.addWidget(self.noobSetJavaWidget)
        self.noobSetMemWidget = QWidget(self.noobNewServerScrollAreaContents)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noobSetMemWidget.sizePolicy().hasHeightForWidth()
        )
        self.noobSetMemWidget.setSizePolicy(sizePolicy)
        self.noobSetMemWidget.setObjectName("noobSetMemWidget")

        self.gridLayout_4 = QGridLayout(self.noobSetMemWidget)
        self.gridLayout_4.setObjectName("gridLayout_4")

        spacerItem5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem5, 1, 5, 1, 1)
        self.noobMinMemLineEdit = LineEdit(self.noobSetMemWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noobMinMemLineEdit.sizePolicy().hasHeightForWidth()
        )
        self.noobMinMemLineEdit.setSizePolicy(sizePolicy)
        self.noobMinMemLineEdit.setMinimumSize(QSize(0, 30))
        self.noobMinMemLineEdit.setObjectName("noobMinMemLineEdit")

        self.gridLayout_4.addWidget(self.noobMinMemLineEdit, 1, 1, 1, 1)
        self.noobMemUnitLabel = SubtitleLabel(self.noobSetMemWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noobMemUnitLabel.sizePolicy().hasHeightForWidth()
        )
        self.noobMemUnitLabel.setSizePolicy(sizePolicy)
        self.noobMemUnitLabel.setObjectName("noobMemUnitLabel")

        self.gridLayout_4.addWidget(self.noobMemUnitLabel, 1, 4, 1, 1)
        self.noobMaxMemLineEdit = LineEdit(self.noobSetMemWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noobMaxMemLineEdit.sizePolicy().hasHeightForWidth()
        )
        self.noobMaxMemLineEdit.setSizePolicy(sizePolicy)
        self.noobMaxMemLineEdit.setMinimumSize(QSize(0, 30))
        self.noobMaxMemLineEdit.setObjectName("noobMaxMemLineEdit")

        self.gridLayout_4.addWidget(self.noobMaxMemLineEdit, 1, 3, 1, 1)
        self.noobToSymbol = SubtitleLabel(self.noobSetMemWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.noobToSymbol.sizePolicy().hasHeightForWidth())
        self.noobToSymbol.setSizePolicy(sizePolicy)
        self.noobToSymbol.setObjectName("noobToSymbol")

        self.gridLayout_4.addWidget(self.noobToSymbol, 1, 2, 1, 1)
        self.noobMemSubtitleLabel = SubtitleLabel(self.noobSetMemWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noobMemSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.noobMemSubtitleLabel.setSizePolicy(sizePolicy)
        self.noobMemSubtitleLabel.setObjectName("noobMemSubtitleLabel")

        self.gridLayout_4.addWidget(self.noobMemSubtitleLabel, 0, 1, 1, 1)
        self.noobNewServerScrollAreaVerticalLayout.addWidget(self.noobSetMemWidget)
        self.noobSetCoreWidget = QWidget(self.noobNewServerScrollAreaContents)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noobSetCoreWidget.sizePolicy().hasHeightForWidth()
        )
        self.noobSetCoreWidget.setSizePolicy(sizePolicy)
        self.noobSetCoreWidget.setObjectName("noobSetCoreWidget")

        self.gridLayout_5 = QGridLayout(self.noobSetCoreWidget)
        self.gridLayout_5.setObjectName("gridLayout_5")

        spacerItem6 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_5.addItem(spacerItem6, 1, 3, 1, 1)
        self.noobDownloadCorePrimaryPushBtn = PrimaryPushButton(self.noobSetCoreWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noobDownloadCorePrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.noobDownloadCorePrimaryPushBtn.setSizePolicy(sizePolicy)
        self.noobDownloadCorePrimaryPushBtn.setMinimumSize(QSize(90, 0))
        self.noobDownloadCorePrimaryPushBtn.setObjectName(
            "noobDownloadCorePrimaryPushBtn"
        )

        self.gridLayout_5.addWidget(self.noobDownloadCorePrimaryPushBtn, 1, 2, 1, 1)
        self.noobManuallyAddCorePrimaryPushBtn = PrimaryPushButton(
            self.noobSetCoreWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noobManuallyAddCorePrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.noobManuallyAddCorePrimaryPushBtn.setSizePolicy(sizePolicy)
        self.noobManuallyAddCorePrimaryPushBtn.setMinimumSize(QSize(90, 0))
        self.noobManuallyAddCorePrimaryPushBtn.setObjectName(
            "noobManuallyAddCorePrimaryPushBtn"
        )

        self.gridLayout_5.addWidget(self.noobManuallyAddCorePrimaryPushBtn, 1, 1, 1, 1)
        self.noobCoreSubtitleLabel = SubtitleLabel(self.noobSetCoreWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noobCoreSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.noobCoreSubtitleLabel.setSizePolicy(sizePolicy)
        self.noobCoreSubtitleLabel.setObjectName("noobCoreSubtitleLabel")

        self.gridLayout_5.addWidget(self.noobCoreSubtitleLabel, 0, 1, 1, 1)
        self.noobNewServerScrollAreaVerticalLayout.addWidget(self.noobSetCoreWidget)
        self.noobSetServerNameWidget = QWidget(self.noobNewServerScrollAreaContents)
        self.noobSetServerNameWidget.setObjectName("noobSetServerNameWidget")

        self.verticalLayout_4 = QVBoxLayout(self.noobSetServerNameWidget)
        self.verticalLayout_4.setObjectName("verticalLayout_4")

        self.noobServerNameSubtitleLabel = SubtitleLabel(self.noobSetServerNameWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noobServerNameSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.noobServerNameSubtitleLabel.setSizePolicy(sizePolicy)
        self.noobServerNameSubtitleLabel.setObjectName("noobServerNameSubtitleLabel")

        self.verticalLayout_4.addWidget(self.noobServerNameSubtitleLabel)
        self.noobServerNameLineEdit = LineEdit(self.noobSetServerNameWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noobServerNameLineEdit.sizePolicy().hasHeightForWidth()
        )
        self.noobServerNameLineEdit.setSizePolicy(sizePolicy)
        self.noobServerNameLineEdit.setMinimumSize(QSize(0, 30))
        self.noobServerNameLineEdit.setObjectName("noobServerNameLineEdit")

        self.verticalLayout_4.addWidget(self.noobServerNameLineEdit)
        self.noobSaveServerPrimaryPushBtn = PrimaryPushButton(
            self.noobSetServerNameWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noobSaveServerPrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.noobSaveServerPrimaryPushBtn.setSizePolicy(sizePolicy)
        self.noobSaveServerPrimaryPushBtn.setMinimumSize(QSize(130, 0))
        self.noobSaveServerPrimaryPushBtn.setObjectName("noobSaveServerPrimaryPushBtn")

        self.verticalLayout_4.addWidget(self.noobSaveServerPrimaryPushBtn)
        self.noobNewServerScrollAreaVerticalLayout.addWidget(
            self.noobSetServerNameWidget
        )
        spacerItem7 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.noobNewServerScrollAreaVerticalLayout.addItem(spacerItem7)
        self.noobNewServerScrollArea.setWidget(self.noobNewServerScrollAreaContents)
        self.noobNewServerGridLayout.addWidget(self.noobNewServerScrollArea, 2, 2, 1, 1)
        self.noobTitleWidget = QWidget(self.noobNewServerPage)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noobTitleWidget.sizePolicy().hasHeightForWidth()
        )
        self.noobTitleWidget.setSizePolicy(sizePolicy)
        self.noobTitleWidget.setObjectName("noobTitleWidget")

        self.horizontalLayout_4 = QHBoxLayout(self.noobTitleWidget)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")

        self.noobBackToGuidePushButton = TransparentToolButton(
            FIF.PAGE_LEFT, self.noobTitleWidget
        )
        self.noobBackToGuidePushButton.setObjectName("noobBackToGuidePushButton")

        self.horizontalLayout_4.addWidget(self.noobBackToGuidePushButton)
        self.noobSubtitleLabel = SubtitleLabel(self.noobTitleWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noobSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.noobSubtitleLabel.setSizePolicy(sizePolicy)
        self.noobSubtitleLabel.setObjectName("noobSubtitleLabel")

        self.horizontalLayout_4.addWidget(self.noobSubtitleLabel)
        spacerItem8 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem8)
        self.noobNewServerGridLayout.addWidget(self.noobTitleWidget, 0, 1, 2, 2)
        spacerItem9 = QSpacerItem(20, 40, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.noobNewServerGridLayout.addItem(spacerItem9, 0, 0, 3, 1)
        self.newServerStackedWidget.addWidget(self.noobNewServerPage)

        self.extendedNewServerPage = QWidget()
        self.extendedNewServerPage.setObjectName("extendedNewServerPage")

        self.gridLayout_2 = QGridLayout(self.extendedNewServerPage)
        self.gridLayout_2.setObjectName("gridLayout_2")

        self.extendedTitleWidget = QWidget(self.extendedNewServerPage)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.extendedTitleWidget.sizePolicy().hasHeightForWidth()
        )
        self.extendedTitleWidget.setSizePolicy(sizePolicy)
        self.extendedTitleWidget.setObjectName("extendedTitleWidget")

        self.horizontalLayout_5 = QHBoxLayout(self.extendedTitleWidget)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")

        self.extendedBackToGuidePushButton = TransparentToolButton(
            FIF.PAGE_LEFT, self.extendedTitleWidget
        )
        self.extendedBackToGuidePushButton.setObjectName(
            "extendedBackToGuidePushButton"
        )

        self.horizontalLayout_5.addWidget(self.extendedBackToGuidePushButton)
        self.extendedSubtitleLabel = SubtitleLabel(self.extendedTitleWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.extendedSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.extendedSubtitleLabel.setSizePolicy(sizePolicy)
        self.extendedSubtitleLabel.setObjectName("extendedSubtitleLabel")

        self.horizontalLayout_5.addWidget(self.extendedSubtitleLabel)
        spacerItem10 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem10)
        self.gridLayout_2.addWidget(self.extendedTitleWidget, 0, 1, 1, 1)
        self.extendedNewServerScrollArea = SmoothScrollArea(self.extendedNewServerPage)
        self.extendedNewServerScrollArea.setFrameShape(QFrame.NoFrame)
        self.extendedNewServerScrollArea.setVerticalScrollBarPolicy(
            Qt.ScrollBarAsNeeded
        )
        self.extendedNewServerScrollArea.setHorizontalScrollBarPolicy(
            Qt.ScrollBarAsNeeded
        )
        self.extendedNewServerScrollArea.setWidgetResizable(True)
        self.extendedNewServerScrollArea.setObjectName("extendedNewServerScrollArea")

        self.extendedNewServerScrollAreaContents = QWidget()
        self.extendedNewServerScrollAreaContents.setGeometry(QRect(0, 0, 594, 734))
        self.extendedNewServerScrollAreaContents.setObjectName(
            "extendedNewServerScrollAreaContents"
        )

        self.noobNewServerScrollAreaVerticalLayout_2 = QVBoxLayout(
            self.extendedNewServerScrollAreaContents
        )
        self.noobNewServerScrollAreaVerticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.noobNewServerScrollAreaVerticalLayout_2.setObjectName(
            "noobNewServerScrollAreaVerticalLayout_2"
        )

        self.extendedSetJavaWidget = QWidget(self.extendedNewServerScrollAreaContents)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.extendedSetJavaWidget.sizePolicy().hasHeightForWidth()
        )
        self.extendedSetJavaWidget.setSizePolicy(sizePolicy)
        self.extendedSetJavaWidget.setMinimumSize(QSize(0, 120))
        self.extendedSetJavaWidget.setObjectName("extendedSetJavaWidget")

        self.gridLayout_6 = QGridLayout(self.extendedSetJavaWidget)
        self.gridLayout_6.setObjectName("gridLayout_6")

        self.extendedJavaSubtitleLabel = SubtitleLabel(self.extendedSetJavaWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.extendedJavaSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.extendedJavaSubtitleLabel.setSizePolicy(sizePolicy)
        self.extendedJavaSubtitleLabel.setObjectName("extendedJavaSubtitleLabel")

        self.gridLayout_6.addWidget(self.extendedJavaSubtitleLabel, 0, 0, 1, 1)
        self.extendedJavaInfoLabel = SubtitleLabel(self.extendedSetJavaWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.extendedJavaInfoLabel.sizePolicy().hasHeightForWidth()
        )
        self.extendedJavaInfoLabel.setSizePolicy(sizePolicy)
        self.extendedJavaInfoLabel.setObjectName("extendedJavaInfoLabel")

        self.gridLayout_6.addWidget(self.extendedJavaInfoLabel, 0, 1, 1, 1)
        self.extendedSetJavaBtnWidget = QWidget(self.extendedSetJavaWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.extendedSetJavaBtnWidget.sizePolicy().hasHeightForWidth()
        )
        self.extendedSetJavaBtnWidget.setSizePolicy(sizePolicy)
        self.extendedSetJavaBtnWidget.setObjectName("extendedSetJavaBtnWidget")

        self.horizontalLayout_7 = QHBoxLayout(self.extendedSetJavaBtnWidget)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")

        self.extendedDownloadJavaPrimaryPushBtn = PrimaryPushButton(
            self.extendedSetJavaBtnWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.extendedDownloadJavaPrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.extendedDownloadJavaPrimaryPushBtn.setSizePolicy(sizePolicy)
        self.extendedDownloadJavaPrimaryPushBtn.setMinimumSize(QSize(90, 0))
        self.extendedDownloadJavaPrimaryPushBtn.setCursor(
            QCursor(Qt.PointingHandCursor)
        )
        self.extendedDownloadJavaPrimaryPushBtn.setObjectName(
            "extendedDownloadJavaPrimaryPushBtn"
        )

        self.horizontalLayout_7.addWidget(self.extendedDownloadJavaPrimaryPushBtn)
        self.extendedManuallyAddJavaPrimaryPushBtn = PrimaryPushButton(
            self.extendedSetJavaBtnWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.extendedManuallyAddJavaPrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.extendedManuallyAddJavaPrimaryPushBtn.setSizePolicy(sizePolicy)
        self.extendedManuallyAddJavaPrimaryPushBtn.setMinimumSize(QSize(90, 0))
        self.extendedManuallyAddJavaPrimaryPushBtn.setCursor(
            QCursor(Qt.PointingHandCursor)
        )
        self.extendedManuallyAddJavaPrimaryPushBtn.setObjectName(
            "extendedManuallyAddJavaPrimaryPushBtn"
        )

        self.horizontalLayout_7.addWidget(self.extendedManuallyAddJavaPrimaryPushBtn)
        self.extendedAutoDetectJavaPrimaryPushBtn = PrimaryPushButton(
            self.extendedSetJavaBtnWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.extendedAutoDetectJavaPrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.extendedAutoDetectJavaPrimaryPushBtn.setSizePolicy(sizePolicy)
        self.extendedAutoDetectJavaPrimaryPushBtn.setCursor(
            QCursor(Qt.PointingHandCursor)
        )
        self.extendedAutoDetectJavaPrimaryPushBtn.setObjectName(
            "extendedAutoDetectJavaPrimaryPushBtn"
        )

        self.horizontalLayout_7.addWidget(self.extendedAutoDetectJavaPrimaryPushBtn)
        self.extendedJavaListPushBtn = PushButton(self.extendedSetJavaBtnWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.extendedJavaListPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.extendedJavaListPushBtn.setSizePolicy(sizePolicy)
        self.extendedJavaListPushBtn.setMinimumSize(QSize(90, 0))
        self.extendedJavaListPushBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.extendedJavaListPushBtn.setObjectName("extendedJavaListPushBtn")

        self.horizontalLayout_7.addWidget(self.extendedJavaListPushBtn)
        spacerItem11 = QSpacerItem(127, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem11)
        self.gridLayout_6.addWidget(self.extendedSetJavaBtnWidget, 1, 0, 1, 2)
        self.noobNewServerScrollAreaVerticalLayout_2.addWidget(
            self.extendedSetJavaWidget
        )
        self.extendedSetMemWidget = QWidget(self.extendedNewServerScrollAreaContents)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.extendedSetMemWidget.sizePolicy().hasHeightForWidth()
        )
        self.extendedSetMemWidget.setSizePolicy(sizePolicy)
        self.extendedSetMemWidget.setObjectName("extendedSetMemWidget")

        self.gridLayout_7 = QGridLayout(self.extendedSetMemWidget)
        self.gridLayout_7.setObjectName("gridLayout_7")

        self.extendedMinMemLineEdit = LineEdit(self.extendedSetMemWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.extendedMinMemLineEdit.sizePolicy().hasHeightForWidth()
        )
        self.extendedMinMemLineEdit.setSizePolicy(sizePolicy)
        self.extendedMinMemLineEdit.setMinimumSize(QSize(0, 30))
        self.extendedMinMemLineEdit.setObjectName("extendedMinMemLineEdit")

        self.gridLayout_7.addWidget(self.extendedMinMemLineEdit, 1, 1, 1, 1)
        self.extendedMemSubtitleLabel = SubtitleLabel(self.extendedSetMemWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.extendedMemSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.extendedMemSubtitleLabel.setSizePolicy(sizePolicy)
        self.extendedMemSubtitleLabel.setObjectName("extendedMemSubtitleLabel")

        self.gridLayout_7.addWidget(self.extendedMemSubtitleLabel, 0, 1, 1, 1)
        self.extendedMaxMemLineEdit = LineEdit(self.extendedSetMemWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.extendedMaxMemLineEdit.sizePolicy().hasHeightForWidth()
        )
        self.extendedMaxMemLineEdit.setSizePolicy(sizePolicy)
        self.extendedMaxMemLineEdit.setMinimumSize(QSize(0, 30))
        self.extendedMaxMemLineEdit.setObjectName("extendedMaxMemLineEdit")

        self.gridLayout_7.addWidget(self.extendedMaxMemLineEdit, 1, 3, 1, 1)
        self.extendedToSymbol = SubtitleLabel(self.extendedSetMemWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.extendedToSymbol.sizePolicy().hasHeightForWidth()
        )
        self.extendedToSymbol.setSizePolicy(sizePolicy)
        self.extendedToSymbol.setObjectName("extendedToSymbol")

        self.gridLayout_7.addWidget(self.extendedToSymbol, 1, 2, 1, 1)
        spacerItem12 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_7.addItem(spacerItem12, 1, 5, 1, 1)
        self.extendedMemUnitComboBox = ComboBox(self.extendedSetMemWidget)
        self.extendedMemUnitComboBox.setObjectName("extendedMemUnitComboBox")

        self.gridLayout_7.addWidget(self.extendedMemUnitComboBox, 1, 4, 1, 1)
        self.noobNewServerScrollAreaVerticalLayout_2.addWidget(
            self.extendedSetMemWidget
        )
        self.extendedSetCoreWidget = QWidget(self.extendedNewServerScrollAreaContents)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.extendedSetCoreWidget.sizePolicy().hasHeightForWidth()
        )
        self.extendedSetCoreWidget.setSizePolicy(sizePolicy)
        self.extendedSetCoreWidget.setObjectName("extendedSetCoreWidget")

        self.gridLayout_8 = QGridLayout(self.extendedSetCoreWidget)
        self.gridLayout_8.setObjectName("gridLayout_8")

        spacerItem13 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_8.addItem(spacerItem13, 1, 3, 1, 1)
        self.extendedDownloadCorePrimaryPushBtn = PrimaryPushButton(
            self.extendedSetCoreWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.extendedDownloadCorePrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.extendedDownloadCorePrimaryPushBtn.setSizePolicy(sizePolicy)
        self.extendedDownloadCorePrimaryPushBtn.setMinimumSize(QSize(90, 0))
        self.extendedDownloadCorePrimaryPushBtn.setObjectName(
            "extendedDownloadCorePrimaryPushBtn"
        )

        self.gridLayout_8.addWidget(self.extendedDownloadCorePrimaryPushBtn, 1, 2, 1, 1)
        self.extendedManuallyAddCorePrimaryPushBtn = PrimaryPushButton(
            self.extendedSetCoreWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.extendedManuallyAddCorePrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.extendedManuallyAddCorePrimaryPushBtn.setSizePolicy(sizePolicy)
        self.extendedManuallyAddCorePrimaryPushBtn.setMinimumSize(QSize(90, 0))
        self.extendedManuallyAddCorePrimaryPushBtn.setObjectName(
            "extendedManuallyAddCorePrimaryPushBtn"
        )

        self.gridLayout_8.addWidget(
            self.extendedManuallyAddCorePrimaryPushBtn, 1, 1, 1, 1
        )
        self.extendedCoreSubtitleLabel = SubtitleLabel(self.extendedSetCoreWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.extendedCoreSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.extendedCoreSubtitleLabel.setSizePolicy(sizePolicy)
        self.extendedCoreSubtitleLabel.setObjectName("extendedCoreSubtitleLabel")

        self.gridLayout_8.addWidget(self.extendedCoreSubtitleLabel, 0, 1, 1, 1)
        self.noobNewServerScrollAreaVerticalLayout_2.addWidget(
            self.extendedSetCoreWidget
        )
        self.extendedSetDeEncodingWidget = QWidget(
            self.extendedNewServerScrollAreaContents
        )
        self.extendedSetDeEncodingWidget.setObjectName("extendedSetDeEncodingWidget")

        self.gridLayout_9 = QGridLayout(self.extendedSetDeEncodingWidget)
        self.gridLayout_9.setObjectName("gridLayout_9")

        self.extendedOutputDeEncodingComboBox = ComboBox(
            self.extendedSetDeEncodingWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.extendedOutputDeEncodingComboBox.sizePolicy().hasHeightForWidth()
        )
        self.extendedOutputDeEncodingComboBox.setSizePolicy(sizePolicy)
        self.extendedOutputDeEncodingComboBox.setObjectName(
            "extendedOutputDeEncodingComboBox"
        )

        self.gridLayout_9.addWidget(self.extendedOutputDeEncodingComboBox, 2, 1, 1, 1)
        self.extendedDeEncodingSubtitleLabel = SubtitleLabel(
            self.extendedSetDeEncodingWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.extendedDeEncodingSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.extendedDeEncodingSubtitleLabel.setSizePolicy(sizePolicy)
        self.extendedDeEncodingSubtitleLabel.setObjectName(
            "extendedDeEncodingSubtitleLabel"
        )

        self.gridLayout_9.addWidget(self.extendedDeEncodingSubtitleLabel, 0, 0, 1, 1)
        self.extendedInputDeEncodingComboBox = ComboBox(
            self.extendedSetDeEncodingWidget
        )
        self.extendedInputDeEncodingComboBox.setText("")
        self.extendedInputDeEncodingComboBox.setObjectName(
            "extendedInputDeEncodingComboBox"
        )

        self.gridLayout_9.addWidget(self.extendedInputDeEncodingComboBox, 3, 1, 1, 1)
        self.extendedOutputDeEncodingLabel = StrongBodyLabel(
            self.extendedSetDeEncodingWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.extendedOutputDeEncodingLabel.sizePolicy().hasHeightForWidth()
        )
        self.extendedOutputDeEncodingLabel.setSizePolicy(sizePolicy)
        self.extendedOutputDeEncodingLabel.setObjectName(
            "extendedOutputDeEncodingLabel"
        )

        self.gridLayout_9.addWidget(self.extendedOutputDeEncodingLabel, 2, 0, 1, 1)
        self.extendedInputDeEncodingLabel = StrongBodyLabel(
            self.extendedSetDeEncodingWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.extendedInputDeEncodingLabel.sizePolicy().hasHeightForWidth()
        )
        self.extendedInputDeEncodingLabel.setSizePolicy(sizePolicy)
        self.extendedInputDeEncodingLabel.setObjectName("extendedInputDeEncodingLabel")

        self.gridLayout_9.addWidget(self.extendedInputDeEncodingLabel, 3, 0, 1, 1)
        self.noobNewServerScrollAreaVerticalLayout_2.addWidget(
            self.extendedSetDeEncodingWidget
        )
        self.extendedSetJVMArgWidget = QWidget(self.extendedNewServerScrollAreaContents)
        self.extendedSetJVMArgWidget.setObjectName("extendedSetJVMArgWidget")

        self.gridLayout_10 = QGridLayout(self.extendedSetJVMArgWidget)
        self.gridLayout_10.setObjectName("gridLayout_10")

        self.extendedJVMArgSubtitleLabel = SubtitleLabel(self.extendedSetJVMArgWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.extendedJVMArgSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.extendedJVMArgSubtitleLabel.setSizePolicy(sizePolicy)
        self.extendedJVMArgSubtitleLabel.setObjectName("extendedJVMArgSubtitleLabel")

        self.gridLayout_10.addWidget(self.extendedJVMArgSubtitleLabel, 0, 0, 1, 1)
        self.JVMArgPlainTextEdit = PlainTextEdit(self.extendedSetJVMArgWidget)
        self.JVMArgPlainTextEdit.setObjectName("JVMArgPlainTextEdit")

        self.gridLayout_10.addWidget(self.JVMArgPlainTextEdit, 1, 0, 1, 1)
        self.noobNewServerScrollAreaVerticalLayout_2.addWidget(
            self.extendedSetJVMArgWidget
        )
        self.extendedSetServerNameWidget = QWidget(
            self.extendedNewServerScrollAreaContents
        )
        self.extendedSetServerNameWidget.setObjectName("extendedSetServerNameWidget")

        self.verticalLayout_5 = QVBoxLayout(self.extendedSetServerNameWidget)
        self.verticalLayout_5.setObjectName("verticalLayout_5")

        self.extendedServerNameSubtitleLabel = SubtitleLabel(
            self.extendedSetServerNameWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.extendedServerNameSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.extendedServerNameSubtitleLabel.setSizePolicy(sizePolicy)
        self.extendedServerNameSubtitleLabel.setObjectName(
            "extendedServerNameSubtitleLabel"
        )

        self.verticalLayout_5.addWidget(self.extendedServerNameSubtitleLabel)
        self.extendedServerNameLineEdit = LineEdit(self.extendedSetServerNameWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.extendedServerNameLineEdit.sizePolicy().hasHeightForWidth()
        )
        self.extendedServerNameLineEdit.setSizePolicy(sizePolicy)
        self.extendedServerNameLineEdit.setMinimumSize(QSize(0, 30))
        self.extendedServerNameLineEdit.setObjectName("extendedServerNameLineEdit")

        self.verticalLayout_5.addWidget(self.extendedServerNameLineEdit)
        self.extendedSaveServerPrimaryPushBtn = PrimaryPushButton(
            self.extendedSetServerNameWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.extendedSaveServerPrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.extendedSaveServerPrimaryPushBtn.setSizePolicy(sizePolicy)
        self.extendedSaveServerPrimaryPushBtn.setMinimumSize(QSize(130, 0))
        self.extendedSaveServerPrimaryPushBtn.setObjectName(
            "extendedSaveServerPrimaryPushBtn"
        )

        self.verticalLayout_5.addWidget(self.extendedSaveServerPrimaryPushBtn)
        self.noobNewServerScrollAreaVerticalLayout_2.addWidget(
            self.extendedSetServerNameWidget
        )
        spacerItem14 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.noobNewServerScrollAreaVerticalLayout_2.addItem(spacerItem14)
        self.extendedNewServerScrollArea.setWidget(
            self.extendedNewServerScrollAreaContents
        )
        self.gridLayout_2.addWidget(self.extendedNewServerScrollArea, 1, 1, 1, 1)
        spacerItem15 = QSpacerItem(20, 40, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem15, 0, 0, 2, 1)
        self.newServerStackedWidget.addWidget(self.extendedNewServerPage)
        self.importNewServerPage = QWidget()
        self.importNewServerPage.setObjectName("importNewServerPage")

        self.gridLayout_21 = QGridLayout(self.importNewServerPage)
        self.gridLayout_21.setObjectName("gridLayout_21")

        self.importTitleWidget = QWidget(self.importNewServerPage)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.importTitleWidget.sizePolicy().hasHeightForWidth()
        )
        self.importTitleWidget.setSizePolicy(sizePolicy)
        self.importTitleWidget.setObjectName("importTitleWidget")

        self.horizontalLayout_10 = QHBoxLayout(self.importTitleWidget)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")

        self.importBackToGuidePushButton = TransparentToolButton(
            FIF.PAGE_LEFT, self.importTitleWidget
        )
        self.importBackToGuidePushButton.setObjectName("importBackToGuidePushButton")

        self.horizontalLayout_10.addWidget(self.importBackToGuidePushButton)
        self.importSubtitleLabel = SubtitleLabel(self.importTitleWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.importSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.importSubtitleLabel.setSizePolicy(sizePolicy)
        self.importSubtitleLabel.setObjectName("importSubtitleLabel")
        self.horizontalLayout_10.addWidget(self.importSubtitleLabel)

        self.horizontalLayout_10.addWidget(self.importSubtitleLabel)
        spacerItem16 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_10.addItem(spacerItem16)
        self.gridLayout_21.addWidget(self.importTitleWidget, 0, 1, 1, 1)
        spacerItem19 = QSpacerItem(20, 406, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout_21.addItem(spacerItem19, 0, 0, 2, 1)
        self.importNewServerStackWidget = ChildStackedWidget(self.importNewServerPage)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.importNewServerStackWidget.sizePolicy().hasHeightForWidth()
        )
        self.importNewServerStackWidget.setSizePolicy(sizePolicy)
        self.importNewServerStackWidget.setObjectName("importNewServerStackWidget")
        self.importNewServerFirstGuide = QWidget()
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.importNewServerFirstGuide.sizePolicy().hasHeightForWidth()
        )
        self.importNewServerFirstGuide.setSizePolicy(sizePolicy)
        self.importNewServerFirstGuide.setObjectName("importNewServerFirstGuide")
        self.gridLayout_11 = QGridLayout(self.importNewServerFirstGuide)
        self.gridLayout_11.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_11.setObjectName("gridLayout_11")
        self.importNewServerTypeComboBox = ComboBox(self.importNewServerFirstGuide)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.importNewServerTypeComboBox.sizePolicy().hasHeightForWidth()
        )
        self.importNewServerTypeComboBox.setSizePolicy(sizePolicy)
        self.importNewServerTypeComboBox.setMinimumSize(QSize(240, 35))
        self.importNewServerTypeComboBox.setMaximumSize(QSize(240, 35))
        self.importNewServerTypeComboBox.setObjectName("importNewServerTypeComboBox")
        self.gridLayout_11.addWidget(self.importNewServerTypeComboBox, 3, 3, 1, 1)
        spacerItem20 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_11.addItem(spacerItem20, 3, 0, 4, 1)
        spacerItem21 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_11.addItem(spacerItem21, 3, 5, 4, 1)
        spacerItem22 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.gridLayout_11.addItem(spacerItem22, 6, 3, 1, 1)
        self.importNewServerFirstGuideTitle = SubtitleLabel(
            self.importNewServerFirstGuide
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.importNewServerFirstGuideTitle.sizePolicy().hasHeightForWidth()
        )
        self.importNewServerFirstGuideTitle.setSizePolicy(sizePolicy)
        self.importNewServerFirstGuideTitle.setObjectName(
            "importNewServerFirstGuideTitle"
        )
        self.gridLayout_11.addWidget(self.importNewServerFirstGuideTitle, 1, 3, 1, 1)
        self.goBtnWidget = QWidget(self.importNewServerFirstGuide)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.goBtnWidget.sizePolicy().hasHeightForWidth())
        self.goBtnWidget.setSizePolicy(sizePolicy)
        self.goBtnWidget.setObjectName("goBtnWidget")
        self.horizontalLayout = QHBoxLayout(self.goBtnWidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.goBtn = TransparentToolButton(FIF.PAGE_RIGHT, self.goBtnWidget)
        self.goBtn.setMinimumSize(QSize(80, 80))
        self.goBtn.setMaximumSize(QSize(80, 80))
        self.goBtn.setIconSize(QSize(80, 80))
        self.goBtn.setObjectName("goBtn")
        self.horizontalLayout.addWidget(self.goBtn)
        self.gridLayout_11.addWidget(self.goBtnWidget, 5, 3, 1, 1)
        spacerItem23 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.gridLayout_11.addItem(spacerItem23, 4, 3, 1, 1)
        spacerItem24 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.gridLayout_11.addItem(spacerItem24, 2, 3, 1, 1)
        spacerItem25 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.gridLayout_11.addItem(spacerItem25, 0, 0, 1, 6)
        self.importNewServerStackWidget.addWidget(self.importNewServerFirstGuide)
        self.noShellArchives = QWidget()
        self.noShellArchives.setObjectName("noShellArchives")
        self.gridLayout_12 = QGridLayout(self.noShellArchives)
        self.gridLayout_12.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_12.setObjectName("gridLayout_12")
        spacerItem26 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.gridLayout_12.addItem(spacerItem26, 1, 1, 1, 1)
        self.noShellArchivesTitle = SubtitleLabel(self.noShellArchives)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noShellArchivesTitle.sizePolicy().hasHeightForWidth()
        )
        self.noShellArchivesTitle.setSizePolicy(sizePolicy)
        self.noShellArchivesTitle.setObjectName("noShellArchivesTitle")
        self.gridLayout_12.addWidget(self.noShellArchivesTitle, 0, 3, 1, 1)
        spacerItem27 = QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout_12.addItem(spacerItem27, 0, 0, 2, 1)
        self.noShellArchivesBackToMain = TransparentToolButton(
            FIF.PAGE_LEFT, self.noShellArchives
        )
        self.noShellArchivesBackToMain.setObjectName("noShellArchivesBackToMain")
        self.gridLayout_12.addWidget(self.noShellArchivesBackToMain, 0, 1, 1, 1)
        spacerItem28 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_12.addItem(spacerItem28, 0, 4, 1, 1)
        self.noShellArchivesScrollArea = SmoothScrollArea(self.noShellArchives)
        self.noShellArchivesScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.noShellArchivesScrollArea.setHorizontalScrollBarPolicy(
            Qt.ScrollBarAsNeeded
        )
        self.noShellArchivesScrollArea.setWidgetResizable(True)
        self.noShellArchivesScrollArea.setAlignment(Qt.AlignCenter)
        self.noShellArchivesScrollArea.setObjectName("noShellArchivesScrollArea")
        self.noShellArchivesScrollAreaWidgetContents = QWidget()
        self.noShellArchivesScrollAreaWidgetContents.setGeometry(QRect(0, 0, 500, 1141))
        self.noShellArchivesScrollAreaWidgetContents.setObjectName(
            "noShellArchivesScrollAreaWidgetContents"
        )
        self.verticalLayout_2 = QVBoxLayout(
            self.noShellArchivesScrollAreaWidgetContents
        )
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.noShellArchivesImport = CardWidget(
            self.noShellArchivesScrollAreaWidgetContents
        )
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noShellArchivesImport.sizePolicy().hasHeightForWidth()
        )
        self.noShellArchivesImport.setSizePolicy(sizePolicy)
        self.noShellArchivesImport.setMinimumSize(QSize(0, 150))
        self.noShellArchivesImport.setMaximumSize(QSize(16777215, 150))
        self.noShellArchivesImport.setObjectName("noShellArchivesImport")
        self.gridLayout_13 = QGridLayout(self.noShellArchivesImport)
        self.gridLayout_13.setObjectName("gridLayout_13")
        spacerItem29 = QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout_13.addItem(spacerItem29, 0, 0, 3, 1)
        self.noShellArchivesImportStatus = PixmapLabel(self.noShellArchivesImport)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noShellArchivesImportStatus.sizePolicy().hasHeightForWidth()
        )
        self.noShellArchivesImportStatus.setSizePolicy(sizePolicy)
        self.noShellArchivesImportStatus.setMinimumSize(QSize(30, 30))
        self.noShellArchivesImportStatus.setMaximumSize(QSize(30, 30))
        self.noShellArchivesImportStatus.setObjectName("noShellArchivesImportStatus")
        self.gridLayout_13.addWidget(self.noShellArchivesImportStatus, 0, 1, 1, 1)
        self.noShellArchivesImportStatusText = BodyLabel(self.noShellArchivesImport)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noShellArchivesImportStatusText.sizePolicy().hasHeightForWidth()
        )
        self.noShellArchivesImportStatusText.setSizePolicy(sizePolicy)
        self.noShellArchivesImportStatusText.setObjectName(
            "noShellArchivesImportStatusText"
        )
        self.gridLayout_13.addWidget(self.noShellArchivesImportStatusText, 1, 1, 1, 2)
        self.noShellArchivesImportBtnWidget = QWidget(self.noShellArchivesImport)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noShellArchivesImportBtnWidget.sizePolicy().hasHeightForWidth()
        )
        self.noShellArchivesImportBtnWidget.setSizePolicy(sizePolicy)
        self.noShellArchivesImportBtnWidget.setObjectName(
            "noShellArchivesImportBtnWidget"
        )
        self.horizontalLayout_2 = QHBoxLayout(self.noShellArchivesImportBtnWidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.noShellArchivesImportArchives = PrimaryPushButton(
            self.noShellArchivesImportBtnWidget
        )
        self.noShellArchivesImportArchives.setMinimumSize(QSize(110, 32))
        self.noShellArchivesImportArchives.setMaximumSize(QSize(110, 32))
        self.noShellArchivesImportArchives.setObjectName(
            "noShellArchivesImportArchives"
        )
        self.horizontalLayout_2.addWidget(self.noShellArchivesImportArchives)
        self.noShellArchivesImportFolder = PrimaryPushButton(
            self.noShellArchivesImportBtnWidget
        )
        self.noShellArchivesImportFolder.setMinimumSize(QSize(110, 32))
        self.noShellArchivesImportFolder.setMaximumSize(QSize(110, 32))
        self.noShellArchivesImportFolder.setObjectName("noShellArchivesImportFolder")
        self.horizontalLayout_2.addWidget(self.noShellArchivesImportFolder)
        self.gridLayout_13.addWidget(self.noShellArchivesImportBtnWidget, 2, 1, 1, 2)
        spacerItem30 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_13.addItem(spacerItem30, 2, 6, 1, 2)
        self.noShellArchivesImportTitle = SubtitleLabel(self.noShellArchivesImport)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noShellArchivesImportTitle.sizePolicy().hasHeightForWidth()
        )
        self.noShellArchivesImportTitle.setSizePolicy(sizePolicy)
        self.noShellArchivesImportTitle.setObjectName("noShellArchivesImportTitle")
        self.gridLayout_13.addWidget(self.noShellArchivesImportTitle, 0, 2, 1, 1)
        self.verticalLayout_2.addWidget(self.noShellArchivesImport)
        self.noShellArchivesSelectCore = CardWidget(
            self.noShellArchivesScrollAreaWidgetContents
        )
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noShellArchivesSelectCore.sizePolicy().hasHeightForWidth()
        )
        self.noShellArchivesSelectCore.setSizePolicy(sizePolicy)
        self.noShellArchivesSelectCore.setMinimumSize(QSize(0, 250))
        self.noShellArchivesSelectCore.setObjectName("noShellArchivesSelectCore")
        self.gridLayout_14 = QGridLayout(self.noShellArchivesSelectCore)
        self.gridLayout_14.setObjectName("gridLayout_14")
        self.noShellArchivesSelectCoreStatus = PixmapLabel(
            self.noShellArchivesSelectCore
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noShellArchivesSelectCoreStatus.sizePolicy().hasHeightForWidth()
        )
        self.noShellArchivesSelectCoreStatus.setSizePolicy(sizePolicy)
        self.noShellArchivesSelectCoreStatus.setMinimumSize(QSize(30, 30))
        self.noShellArchivesSelectCoreStatus.setMaximumSize(QSize(30, 30))
        self.noShellArchivesSelectCoreStatus.setObjectName(
            "noShellArchivesSelectCoreStatus"
        )
        self.gridLayout_14.addWidget(self.noShellArchivesSelectCoreStatus, 0, 1, 1, 1)
        spacerItem31 = QSpacerItem(20, 279, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout_14.addItem(spacerItem31, 0, 0, 3, 1)
        self.noShellArchivesSelectCoreStatusText = BodyLabel(
            self.noShellArchivesSelectCore
        )
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noShellArchivesSelectCoreStatusText.sizePolicy().hasHeightForWidth()
        )
        self.noShellArchivesSelectCoreStatusText.setSizePolicy(sizePolicy)
        self.noShellArchivesSelectCoreStatusText.setObjectName(
            "noShellArchivesSelectCoreStatusText"
        )
        self.gridLayout_14.addWidget(
            self.noShellArchivesSelectCoreStatusText, 1, 1, 1, 2
        )
        self.noShellArchivesSelectCoreTitle = SubtitleLabel(
            self.noShellArchivesSelectCore
        )
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noShellArchivesSelectCoreTitle.sizePolicy().hasHeightForWidth()
        )
        self.noShellArchivesSelectCoreTitle.setSizePolicy(sizePolicy)
        self.noShellArchivesSelectCoreTitle.setObjectName(
            "noShellArchivesSelectCoreTitle"
        )
        self.gridLayout_14.addWidget(self.noShellArchivesSelectCoreTitle, 0, 2, 1, 1)
        self.noShellArchivesSelectCoreTreeWidget = TreeWidget(
            self.noShellArchivesSelectCore
        )
        self.noShellArchivesSelectCoreTreeWidget.setObjectName(
            "noShellArchivesSelectCoreTreeWidget"
        )
        self.noShellArchivesSelectCoreTreeWidget.headerItem().setText(0, "1")
        self.gridLayout_14.addWidget(
            self.noShellArchivesSelectCoreTreeWidget, 2, 1, 1, 2
        )
        self.verticalLayout_2.addWidget(self.noShellArchivesSelectCore)
        self.noShellArchivesSetArgs = CardWidget(
            self.noShellArchivesScrollAreaWidgetContents
        )
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noShellArchivesSetArgs.sizePolicy().hasHeightForWidth()
        )
        self.noShellArchivesSetArgs.setSizePolicy(sizePolicy)
        self.noShellArchivesSetArgs.setMinimumSize(QSize(0, 580))
        self.noShellArchivesSetArgs.setMaximumSize(QSize(16777215, 580))
        self.noShellArchivesSetArgs.setObjectName("noShellArchivesSetArgs")
        self.gridLayout_19 = QGridLayout(self.noShellArchivesSetArgs)
        self.gridLayout_19.setObjectName("gridLayout_19")
        self.noShellArchivesSetJVMArgWidget = QWidget(self.noShellArchivesSetArgs)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noShellArchivesSetJVMArgWidget.sizePolicy().hasHeightForWidth()
        )
        self.noShellArchivesSetJVMArgWidget.setSizePolicy(sizePolicy)
        self.noShellArchivesSetJVMArgWidget.setMinimumSize(QSize(0, 171))
        self.noShellArchivesSetJVMArgWidget.setMaximumSize(QSize(16777215, 171))
        self.noShellArchivesSetJVMArgWidget.setObjectName(
            "noShellArchivesSetJVMArgWidget"
        )
        self.gridLayout_18 = QGridLayout(self.noShellArchivesSetJVMArgWidget)
        self.gridLayout_18.setObjectName("gridLayout_18")
        self.noShellArchivesJVMArgPlainTextEdit = PlainTextEdit(
            self.noShellArchivesSetJVMArgWidget
        )
        self.noShellArchivesJVMArgPlainTextEdit.setObjectName(
            "noShellArchivesJVMArgPlainTextEdit"
        )
        self.gridLayout_18.addWidget(
            self.noShellArchivesJVMArgPlainTextEdit, 1, 0, 1, 1
        )
        self.noShellArchivesJVMArgSubtitleLabel = SubtitleLabel(
            self.noShellArchivesSetJVMArgWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noShellArchivesJVMArgSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.noShellArchivesJVMArgSubtitleLabel.setSizePolicy(sizePolicy)
        self.noShellArchivesJVMArgSubtitleLabel.setObjectName(
            "noShellArchivesJVMArgSubtitleLabel"
        )
        self.gridLayout_18.addWidget(
            self.noShellArchivesJVMArgSubtitleLabel, 0, 0, 1, 1
        )
        self.gridLayout_19.addWidget(self.noShellArchivesSetJVMArgWidget, 7, 2, 1, 3)
        self.noShellArchivesSetArgsTitle = SubtitleLabel(self.noShellArchivesSetArgs)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noShellArchivesSetArgsTitle.sizePolicy().hasHeightForWidth()
        )
        self.noShellArchivesSetArgsTitle.setSizePolicy(sizePolicy)
        self.noShellArchivesSetArgsTitle.setObjectName("noShellArchivesSetArgsTitle")
        self.gridLayout_19.addWidget(self.noShellArchivesSetArgsTitle, 0, 3, 1, 1)
        spacerItem32 = QSpacerItem(20, 102, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout_19.addItem(spacerItem32, 0, 0, 19, 1)
        self.noShellArchivesSetArgsStatus = PixmapLabel(self.noShellArchivesSetArgs)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noShellArchivesSetArgsStatus.sizePolicy().hasHeightForWidth()
        )
        self.noShellArchivesSetArgsStatus.setSizePolicy(sizePolicy)
        self.noShellArchivesSetArgsStatus.setMinimumSize(QSize(30, 30))
        self.noShellArchivesSetArgsStatus.setMaximumSize(QSize(30, 30))
        self.noShellArchivesSetArgsStatus.setObjectName("noShellArchivesSetArgsStatus")
        self.gridLayout_19.addWidget(self.noShellArchivesSetArgsStatus, 0, 2, 1, 1)
        self.noShellArchivesSetJavaWidget = QWidget(self.noShellArchivesSetArgs)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noShellArchivesSetJavaWidget.sizePolicy().hasHeightForWidth()
        )
        self.noShellArchivesSetJavaWidget.setSizePolicy(sizePolicy)
        self.noShellArchivesSetJavaWidget.setMinimumSize(QSize(0, 100))
        self.noShellArchivesSetJavaWidget.setMaximumSize(QSize(16777215, 100))
        self.noShellArchivesSetJavaWidget.setObjectName("noShellArchivesSetJavaWidget")
        self.gridLayout_17 = QGridLayout(self.noShellArchivesSetJavaWidget)
        self.gridLayout_17.setObjectName("gridLayout_17")
        self.noShellArchivesSetJavaBtnWidget = QWidget(
            self.noShellArchivesSetJavaWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noShellArchivesSetJavaBtnWidget.sizePolicy().hasHeightForWidth()
        )
        self.noShellArchivesSetJavaBtnWidget.setSizePolicy(sizePolicy)
        self.noShellArchivesSetJavaBtnWidget.setObjectName(
            "noShellArchivesSetJavaBtnWidget"
        )
        self.horizontalLayout_8 = QHBoxLayout(self.noShellArchivesSetJavaBtnWidget)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.noShellArchivesDownloadJavaPrimaryPushBtn = PrimaryPushButton(
            self.noShellArchivesSetJavaBtnWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noShellArchivesDownloadJavaPrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.noShellArchivesDownloadJavaPrimaryPushBtn.setSizePolicy(sizePolicy)
        self.noShellArchivesDownloadJavaPrimaryPushBtn.setMinimumSize(QSize(90, 0))
        self.noShellArchivesDownloadJavaPrimaryPushBtn.setCursor(
            QCursor(Qt.PointingHandCursor)
        )
        self.noShellArchivesDownloadJavaPrimaryPushBtn.setObjectName(
            "noShellArchivesDownloadJavaPrimaryPushBtn"
        )
        self.horizontalLayout_8.addWidget(
            self.noShellArchivesDownloadJavaPrimaryPushBtn
        )
        self.noShellArchivesManuallyAddJavaPrimaryPushBtn = PrimaryPushButton(
            self.noShellArchivesSetJavaBtnWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noShellArchivesManuallyAddJavaPrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.noShellArchivesManuallyAddJavaPrimaryPushBtn.setSizePolicy(sizePolicy)
        self.noShellArchivesManuallyAddJavaPrimaryPushBtn.setMinimumSize(QSize(90, 0))
        self.noShellArchivesManuallyAddJavaPrimaryPushBtn.setCursor(
            QCursor(Qt.PointingHandCursor)
        )
        self.noShellArchivesManuallyAddJavaPrimaryPushBtn.setObjectName(
            "noShellArchivesManuallyAddJavaPrimaryPushBtn"
        )
        self.horizontalLayout_8.addWidget(
            self.noShellArchivesManuallyAddJavaPrimaryPushBtn
        )
        self.noShellArchivesAutoDetectJavaPrimaryPushBtn = PrimaryPushButton(
            self.noShellArchivesSetJavaBtnWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noShellArchivesAutoDetectJavaPrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.noShellArchivesAutoDetectJavaPrimaryPushBtn.setSizePolicy(sizePolicy)
        self.noShellArchivesAutoDetectJavaPrimaryPushBtn.setCursor(
            QCursor(Qt.PointingHandCursor)
        )
        self.noShellArchivesAutoDetectJavaPrimaryPushBtn.setObjectName(
            "noShellArchivesAutoDetectJavaPrimaryPushBtn"
        )
        self.horizontalLayout_8.addWidget(
            self.noShellArchivesAutoDetectJavaPrimaryPushBtn
        )
        self.noShellArchivesJavaListPushBtn = PushButton(
            self.noShellArchivesSetJavaBtnWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noShellArchivesJavaListPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.noShellArchivesJavaListPushBtn.setSizePolicy(sizePolicy)
        self.noShellArchivesJavaListPushBtn.setMinimumSize(QSize(90, 0))
        self.noShellArchivesJavaListPushBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.noShellArchivesJavaListPushBtn.setObjectName(
            "noShellArchivesJavaListPushBtn"
        )
        self.horizontalLayout_8.addWidget(self.noShellArchivesJavaListPushBtn)
        spacerItem33 = QSpacerItem(127, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem33)
        self.gridLayout_17.addWidget(self.noShellArchivesSetJavaBtnWidget, 1, 0, 1, 2)
        self.noShellArchivesJavaInfoLabel = SubtitleLabel(
            self.noShellArchivesSetJavaWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noShellArchivesJavaInfoLabel.sizePolicy().hasHeightForWidth()
        )
        self.noShellArchivesJavaInfoLabel.setSizePolicy(sizePolicy)
        self.noShellArchivesJavaInfoLabel.setObjectName("noShellArchivesJavaInfoLabel")
        self.gridLayout_17.addWidget(self.noShellArchivesJavaInfoLabel, 0, 1, 1, 1)
        self.noShellArchivesJavaSubtitleLabel = SubtitleLabel(
            self.noShellArchivesSetJavaWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noShellArchivesJavaSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.noShellArchivesJavaSubtitleLabel.setSizePolicy(sizePolicy)
        self.noShellArchivesJavaSubtitleLabel.setObjectName(
            "noShellArchivesJavaSubtitleLabel"
        )
        self.gridLayout_17.addWidget(self.noShellArchivesJavaSubtitleLabel, 0, 0, 1, 1)
        self.gridLayout_19.addWidget(self.noShellArchivesSetJavaWidget, 4, 2, 1, 3)
        self.noShellArchivesSetDeEncodingWidget = QWidget(self.noShellArchivesSetArgs)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noShellArchivesSetDeEncodingWidget.sizePolicy().hasHeightForWidth()
        )
        self.noShellArchivesSetDeEncodingWidget.setSizePolicy(sizePolicy)
        self.noShellArchivesSetDeEncodingWidget.setMinimumSize(QSize(0, 122))
        self.noShellArchivesSetDeEncodingWidget.setMaximumSize(QSize(16777215, 122))
        self.noShellArchivesSetDeEncodingWidget.setObjectName(
            "noShellArchivesSetDeEncodingWidget"
        )
        self.gridLayout_16 = QGridLayout(self.noShellArchivesSetDeEncodingWidget)
        self.gridLayout_16.setObjectName("gridLayout_16")
        self.noShellArchivesOutputDeEncodingComboBox = ComboBox(
            self.noShellArchivesSetDeEncodingWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noShellArchivesOutputDeEncodingComboBox.sizePolicy().hasHeightForWidth()
        )
        self.noShellArchivesOutputDeEncodingComboBox.setSizePolicy(sizePolicy)
        self.noShellArchivesOutputDeEncodingComboBox.setObjectName(
            "noShellArchivesOutputDeEncodingComboBox"
        )
        self.gridLayout_16.addWidget(
            self.noShellArchivesOutputDeEncodingComboBox, 2, 1, 1, 1
        )
        self.noShellArchivesInputDeEncodingComboBox = ComboBox(
            self.noShellArchivesSetDeEncodingWidget
        )
        self.noShellArchivesInputDeEncodingComboBox.setText("")
        self.noShellArchivesInputDeEncodingComboBox.setObjectName(
            "noShellArchivesInputDeEncodingComboBox"
        )
        self.gridLayout_16.addWidget(
            self.noShellArchivesInputDeEncodingComboBox, 3, 1, 1, 1
        )
        self.noShellArchivesOutputDeEncodingLabel = StrongBodyLabel(
            self.noShellArchivesSetDeEncodingWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noShellArchivesOutputDeEncodingLabel.sizePolicy().hasHeightForWidth()
        )
        self.noShellArchivesOutputDeEncodingLabel.setSizePolicy(sizePolicy)
        self.noShellArchivesOutputDeEncodingLabel.setObjectName(
            "noShellArchivesOutputDeEncodingLabel"
        )
        self.gridLayout_16.addWidget(
            self.noShellArchivesOutputDeEncodingLabel, 2, 0, 1, 1
        )
        self.noShellArchivesDeEncodingSubtitleLabel = SubtitleLabel(
            self.noShellArchivesSetDeEncodingWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noShellArchivesDeEncodingSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.noShellArchivesDeEncodingSubtitleLabel.setSizePolicy(sizePolicy)
        self.noShellArchivesDeEncodingSubtitleLabel.setObjectName(
            "noShellArchivesDeEncodingSubtitleLabel"
        )
        self.gridLayout_16.addWidget(
            self.noShellArchivesDeEncodingSubtitleLabel, 0, 0, 1, 1
        )
        self.noShellArchivesInputDeEncodingLabel = StrongBodyLabel(
            self.noShellArchivesSetDeEncodingWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noShellArchivesInputDeEncodingLabel.sizePolicy().hasHeightForWidth()
        )
        self.noShellArchivesInputDeEncodingLabel.setSizePolicy(sizePolicy)
        self.noShellArchivesInputDeEncodingLabel.setObjectName(
            "noShellArchivesInputDeEncodingLabel"
        )
        self.gridLayout_16.addWidget(
            self.noShellArchivesInputDeEncodingLabel, 3, 0, 1, 1
        )
        self.gridLayout_19.addWidget(
            self.noShellArchivesSetDeEncodingWidget, 6, 2, 1, 3
        )
        self.noShellArchivesSetMemWidget = QWidget(self.noShellArchivesSetArgs)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noShellArchivesSetMemWidget.sizePolicy().hasHeightForWidth()
        )
        self.noShellArchivesSetMemWidget.setSizePolicy(sizePolicy)
        self.noShellArchivesSetMemWidget.setMinimumSize(QSize(0, 85))
        self.noShellArchivesSetMemWidget.setMaximumSize(QSize(16777215, 85))
        self.noShellArchivesSetMemWidget.setObjectName("noShellArchivesSetMemWidget")
        self.gridLayout_15 = QGridLayout(self.noShellArchivesSetMemWidget)
        self.gridLayout_15.setObjectName("gridLayout_15")
        self.noShellArchivesMinMemLineEdit = LineEdit(self.noShellArchivesSetMemWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noShellArchivesMinMemLineEdit.sizePolicy().hasHeightForWidth()
        )
        self.noShellArchivesMinMemLineEdit.setSizePolicy(sizePolicy)
        self.noShellArchivesMinMemLineEdit.setMinimumSize(QSize(0, 30))
        self.noShellArchivesMinMemLineEdit.setObjectName(
            "noShellArchivesMinMemLineEdit"
        )
        self.gridLayout_15.addWidget(self.noShellArchivesMinMemLineEdit, 1, 1, 1, 1)
        self.noShellArchivesMemSubtitleLabel = SubtitleLabel(
            self.noShellArchivesSetMemWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noShellArchivesMemSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.noShellArchivesMemSubtitleLabel.setSizePolicy(sizePolicy)
        self.noShellArchivesMemSubtitleLabel.setObjectName(
            "noShellArchivesMemSubtitleLabel"
        )
        self.gridLayout_15.addWidget(self.noShellArchivesMemSubtitleLabel, 0, 1, 1, 1)
        self.noShellArchivesMaxMemLineEdit = LineEdit(self.noShellArchivesSetMemWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noShellArchivesMaxMemLineEdit.sizePolicy().hasHeightForWidth()
        )
        self.noShellArchivesMaxMemLineEdit.setSizePolicy(sizePolicy)
        self.noShellArchivesMaxMemLineEdit.setMinimumSize(QSize(0, 30))
        self.noShellArchivesMaxMemLineEdit.setObjectName(
            "noShellArchivesMaxMemLineEdit"
        )
        self.gridLayout_15.addWidget(self.noShellArchivesMaxMemLineEdit, 1, 3, 1, 1)
        self.noShellArchivesToSymbol = SubtitleLabel(self.noShellArchivesSetMemWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noShellArchivesToSymbol.sizePolicy().hasHeightForWidth()
        )
        self.noShellArchivesToSymbol.setSizePolicy(sizePolicy)
        self.noShellArchivesToSymbol.setObjectName("noShellArchivesToSymbol")
        self.gridLayout_15.addWidget(self.noShellArchivesToSymbol, 1, 2, 1, 1)
        spacerItem34 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_15.addItem(spacerItem34, 1, 5, 1, 1)
        self.noShellArchivesMemUnitComboBox = ComboBox(self.noShellArchivesSetMemWidget)
        self.noShellArchivesMemUnitComboBox.setObjectName(
            "noShellArchivesMemUnitComboBox"
        )
        self.gridLayout_15.addWidget(self.noShellArchivesMemUnitComboBox, 1, 4, 1, 1)
        self.gridLayout_19.addWidget(self.noShellArchivesSetMemWidget, 5, 2, 1, 3)
        self.verticalLayout_2.addWidget(self.noShellArchivesSetArgs)
        self.noShellArchivesSave = CardWidget(
            self.noShellArchivesScrollAreaWidgetContents
        )
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noShellArchivesSave.sizePolicy().hasHeightForWidth()
        )
        self.noShellArchivesSave.setSizePolicy(sizePolicy)
        self.noShellArchivesSave.setMinimumSize(QSize(0, 125))
        self.noShellArchivesSave.setMaximumSize(QSize(16777215, 125))
        self.noShellArchivesSave.setObjectName("noShellArchivesSave")
        self.gridLayout_20 = QGridLayout(self.noShellArchivesSave)
        self.gridLayout_20.setObjectName("gridLayout_20")
        self.noShellArchivesSaveTitle = SubtitleLabel(self.noShellArchivesSave)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noShellArchivesSaveTitle.sizePolicy().hasHeightForWidth()
        )
        self.noShellArchivesSaveTitle.setSizePolicy(sizePolicy)
        self.noShellArchivesSaveTitle.setObjectName("noShellArchivesSaveTitle")
        self.gridLayout_20.addWidget(self.noShellArchivesSaveTitle, 0, 1, 1, 1)
        self.noShellArchivesSaveServerNameLineEdit = LineEdit(self.noShellArchivesSave)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noShellArchivesSaveServerNameLineEdit.sizePolicy().hasHeightForWidth()
        )
        self.noShellArchivesSaveServerNameLineEdit.setSizePolicy(sizePolicy)
        self.noShellArchivesSaveServerNameLineEdit.setMinimumSize(QSize(0, 30))
        self.noShellArchivesSaveServerNameLineEdit.setObjectName(
            "noShellArchivesSaveServerNameLineEdit"
        )
        self.gridLayout_20.addWidget(
            self.noShellArchivesSaveServerNameLineEdit, 1, 1, 1, 1
        )
        spacerItem35 = QSpacerItem(20, 79, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout_20.addItem(spacerItem35, 0, 0, 3, 1)
        self.noShellArchivesSaveSaveServerPrimaryPushBtn = PrimaryPushButton(
            self.noShellArchivesSave
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noShellArchivesSaveSaveServerPrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.noShellArchivesSaveSaveServerPrimaryPushBtn.setSizePolicy(sizePolicy)
        self.noShellArchivesSaveSaveServerPrimaryPushBtn.setMinimumSize(QSize(130, 30))
        self.noShellArchivesSaveSaveServerPrimaryPushBtn.setMaximumSize(
            QSize(16777215, 30)
        )
        self.noShellArchivesSaveSaveServerPrimaryPushBtn.setObjectName(
            "noShellArchivesSaveSaveServerPrimaryPushBtn"
        )
        self.gridLayout_20.addWidget(
            self.noShellArchivesSaveSaveServerPrimaryPushBtn, 2, 1, 1, 1
        )
        self.verticalLayout_2.addWidget(self.noShellArchivesSave)
        self.noShellArchivesScrollArea.setWidget(
            self.noShellArchivesScrollAreaWidgetContents
        )
        self.gridLayout_12.addWidget(self.noShellArchivesScrollArea, 1, 3, 1, 2)
        self.importNewServerStackWidget.addWidget(self.noShellArchives)
        self.shellArchives = QWidget()
        self.shellArchives.setObjectName("shellArchives")
        self.gridLayout_30 = QGridLayout(self.shellArchives)
        self.gridLayout_30.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_30.setObjectName("gridLayout_30")
        self.shellArchivesBackToMain = TransparentToolButton(
            FIF.PAGE_LEFT, self.shellArchives
        )
        self.shellArchivesBackToMain.setObjectName("shellArchivesBackToMain")
        self.gridLayout_30.addWidget(self.shellArchivesBackToMain, 0, 1, 1, 1)
        self.shellArchivesTitle = SubtitleLabel(self.shellArchives)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.shellArchivesTitle.sizePolicy().hasHeightForWidth()
        )
        self.shellArchivesTitle.setSizePolicy(sizePolicy)
        self.shellArchivesTitle.setObjectName("shellArchivesTitle")
        self.gridLayout_30.addWidget(self.shellArchivesTitle, 0, 2, 1, 1)
        spacerItem36 = QSpacerItem(81, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_30.addItem(spacerItem36, 0, 3, 1, 1)
        spacerItem37 = QSpacerItem(20, 299, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.gridLayout_30.addItem(spacerItem37, 1, 1, 1, 1)
        self.shellArchivesScrollArea = SmoothScrollArea(self.shellArchives)
        self.shellArchivesScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.shellArchivesScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.shellArchivesScrollArea.setWidgetResizable(True)
        self.shellArchivesScrollArea.setAlignment(Qt.AlignCenter)
        self.shellArchivesScrollArea.setObjectName("shellArchivesScrollArea")
        self.shellArchivesScrollAreaWidgetContents = QWidget()
        self.shellArchivesScrollAreaWidgetContents.setGeometry(QRect(0, 0, 450, 1191))
        self.shellArchivesScrollAreaWidgetContents.setObjectName(
            "shellArchivesScrollAreaWidgetContents"
        )
        self.verticalLayout_3 = QVBoxLayout(self.shellArchivesScrollAreaWidgetContents)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.shellArchivesImport = CardWidget(
            self.shellArchivesScrollAreaWidgetContents
        )
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.shellArchivesImport.sizePolicy().hasHeightForWidth()
        )
        self.shellArchivesImport.setSizePolicy(sizePolicy)
        self.shellArchivesImport.setMinimumSize(QSize(0, 150))
        self.shellArchivesImport.setMaximumSize(QSize(16777215, 150))
        self.shellArchivesImport.setObjectName("shellArchivesImport")
        self.gridLayout_22 = QGridLayout(self.shellArchivesImport)
        self.gridLayout_22.setObjectName("gridLayout_22")
        spacerItem38 = QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout_22.addItem(spacerItem38, 0, 0, 3, 1)
        self.shellArchivesImportStatus = PixmapLabel(self.shellArchivesImport)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.shellArchivesImportStatus.sizePolicy().hasHeightForWidth()
        )
        self.shellArchivesImportStatus.setSizePolicy(sizePolicy)
        self.shellArchivesImportStatus.setMinimumSize(QSize(30, 30))
        self.shellArchivesImportStatus.setMaximumSize(QSize(30, 30))
        self.shellArchivesImportStatus.setObjectName("shellArchivesImportStatus")
        self.gridLayout_22.addWidget(self.shellArchivesImportStatus, 0, 1, 1, 1)
        self.shellArchivesImportStatusText = BodyLabel(self.shellArchivesImport)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.shellArchivesImportStatusText.sizePolicy().hasHeightForWidth()
        )
        self.shellArchivesImportStatusText.setSizePolicy(sizePolicy)
        self.shellArchivesImportStatusText.setObjectName(
            "shellArchivesImportStatusText"
        )
        self.gridLayout_22.addWidget(self.shellArchivesImportStatusText, 1, 1, 1, 2)
        self.shellArchivesImportBtnWidget = QWidget(self.shellArchivesImport)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.shellArchivesImportBtnWidget.sizePolicy().hasHeightForWidth()
        )
        self.shellArchivesImportBtnWidget.setSizePolicy(sizePolicy)
        self.shellArchivesImportBtnWidget.setObjectName("shellArchivesImportBtnWidget")
        self.horizontalLayout_3 = QHBoxLayout(self.shellArchivesImportBtnWidget)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.shellArchivesImportArchives = PrimaryPushButton(
            self.shellArchivesImportBtnWidget
        )
        self.shellArchivesImportArchives.setMinimumSize(QSize(110, 32))
        self.shellArchivesImportArchives.setMaximumSize(QSize(110, 32))
        self.shellArchivesImportArchives.setObjectName("shellArchivesImportArchives")
        self.horizontalLayout_3.addWidget(self.shellArchivesImportArchives)
        self.shellArchivesImportFolder = PrimaryPushButton(
            self.shellArchivesImportBtnWidget
        )
        self.shellArchivesImportFolder.setMinimumSize(QSize(110, 32))
        self.shellArchivesImportFolder.setMaximumSize(QSize(110, 32))
        self.shellArchivesImportFolder.setObjectName("shellArchivesImportFolder")
        self.horizontalLayout_3.addWidget(self.shellArchivesImportFolder)
        self.gridLayout_22.addWidget(self.shellArchivesImportBtnWidget, 2, 1, 1, 2)
        spacerItem39 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_22.addItem(spacerItem39, 2, 6, 1, 2)
        self.shellArchivesImportTitle = SubtitleLabel(self.shellArchivesImport)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.shellArchivesImportTitle.sizePolicy().hasHeightForWidth()
        )
        self.shellArchivesImportTitle.setSizePolicy(sizePolicy)
        self.shellArchivesImportTitle.setObjectName("shellArchivesImportTitle")
        self.gridLayout_22.addWidget(self.shellArchivesImportTitle, 0, 2, 1, 1)
        self.verticalLayout_3.addWidget(self.shellArchivesImport)
        self.shellArchivesSelectShell = CardWidget(
            self.shellArchivesScrollAreaWidgetContents
        )
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.shellArchivesSelectShell.sizePolicy().hasHeightForWidth()
        )
        self.shellArchivesSelectShell.setSizePolicy(sizePolicy)
        self.shellArchivesSelectShell.setMinimumSize(QSize(0, 250))
        self.shellArchivesSelectShell.setObjectName("shellArchivesSelectShell")
        self.gridLayout_23 = QGridLayout(self.shellArchivesSelectShell)
        self.gridLayout_23.setObjectName("gridLayout_23")
        self.shellArchivesSelectShellStatus = PixmapLabel(self.shellArchivesSelectShell)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.shellArchivesSelectShellStatus.sizePolicy().hasHeightForWidth()
        )
        self.shellArchivesSelectShellStatus.setSizePolicy(sizePolicy)
        self.shellArchivesSelectShellStatus.setMinimumSize(QSize(30, 30))
        self.shellArchivesSelectShellStatus.setMaximumSize(QSize(30, 30))
        self.shellArchivesSelectShellStatus.setObjectName(
            "shellArchivesSelectShellStatus"
        )
        self.gridLayout_23.addWidget(self.shellArchivesSelectShellStatus, 0, 1, 1, 1)
        spacerItem40 = QSpacerItem(20, 279, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout_23.addItem(spacerItem40, 0, 0, 3, 1)
        self.shellArchivesSelectShellStatusText = BodyLabel(
            self.shellArchivesSelectShell
        )
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.shellArchivesSelectShellStatusText.sizePolicy().hasHeightForWidth()
        )
        self.shellArchivesSelectShellStatusText.setSizePolicy(sizePolicy)
        self.shellArchivesSelectShellStatusText.setObjectName(
            "shellArchivesSelectShellStatusText"
        )
        self.gridLayout_23.addWidget(
            self.shellArchivesSelectShellStatusText, 1, 1, 1, 2
        )
        self.shellArchivesSelectShellTitle = SubtitleLabel(
            self.shellArchivesSelectShell
        )
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.shellArchivesSelectShellTitle.sizePolicy().hasHeightForWidth()
        )
        self.shellArchivesSelectShellTitle.setSizePolicy(sizePolicy)
        self.shellArchivesSelectShellTitle.setObjectName(
            "shellArchivesSelectShellTitle"
        )
        self.gridLayout_23.addWidget(self.shellArchivesSelectShellTitle, 0, 2, 1, 1)
        self.shellArchivesSelectShellTreeWidget = TreeWidget(
            self.shellArchivesSelectShell
        )
        self.shellArchivesSelectShellTreeWidget.setObjectName(
            "shellArchivesSelectShellTreeWidget"
        )
        self.shellArchivesSelectShellTreeWidget.headerItem().setText(0, "1")
        self.gridLayout_23.addWidget(
            self.shellArchivesSelectShellTreeWidget, 2, 1, 1, 2
        )
        self.verticalLayout_3.addWidget(self.shellArchivesSelectShell)
        self.shellArchivesValidateArgs = CardWidget(
            self.shellArchivesScrollAreaWidgetContents
        )
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.shellArchivesValidateArgs.sizePolicy().hasHeightForWidth()
        )
        self.shellArchivesValidateArgs.setSizePolicy(sizePolicy)
        self.shellArchivesValidateArgs.setMinimumSize(QSize(0, 630))
        self.shellArchivesValidateArgs.setMaximumSize(QSize(16777215, 630))
        self.shellArchivesValidateArgs.setObjectName("shellArchivesValidateArgs")
        self.gridLayout_24 = QGridLayout(self.shellArchivesValidateArgs)
        self.gridLayout_24.setObjectName("gridLayout_24")
        spacerItem41 = QSpacerItem(20, 102, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout_24.addItem(spacerItem41, 0, 0, 21, 1)
        self.shellArchivesValidateArgsJavaWidget = QWidget(
            self.shellArchivesValidateArgs
        )
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.shellArchivesValidateArgsJavaWidget.sizePolicy().hasHeightForWidth()
        )
        self.shellArchivesValidateArgsJavaWidget.setSizePolicy(sizePolicy)
        self.shellArchivesValidateArgsJavaWidget.setMinimumSize(QSize(0, 120))
        self.shellArchivesValidateArgsJavaWidget.setObjectName(
            "shellArchivesValidateArgsJavaWidget"
        )
        self.gridLayout_26 = QGridLayout(self.shellArchivesValidateArgsJavaWidget)
        self.gridLayout_26.setObjectName("gridLayout_26")
        self.shellArchivesValidateArgsAutoDetectJavaPrimaryPushBtn = PrimaryPushButton(
            self.shellArchivesValidateArgsJavaWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.shellArchivesValidateArgsAutoDetectJavaPrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.shellArchivesValidateArgsAutoDetectJavaPrimaryPushBtn.setSizePolicy(
            sizePolicy
        )
        self.shellArchivesValidateArgsAutoDetectJavaPrimaryPushBtn.setCursor(
            QCursor(Qt.PointingHandCursor)
        )
        self.shellArchivesValidateArgsAutoDetectJavaPrimaryPushBtn.setObjectName(
            "shellArchivesValidateArgsAutoDetectJavaPrimaryPushBtn"
        )
        self.gridLayout_26.addWidget(
            self.shellArchivesValidateArgsAutoDetectJavaPrimaryPushBtn, 2, 2, 1, 1
        )
        self.shellArchivesValidateArgsJavaSubtitleLabel = SubtitleLabel(
            self.shellArchivesValidateArgsJavaWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.shellArchivesValidateArgsJavaSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.shellArchivesValidateArgsJavaSubtitleLabel.setSizePolicy(sizePolicy)
        self.shellArchivesValidateArgsJavaSubtitleLabel.setObjectName(
            "shellArchivesValidateArgsJavaSubtitleLabel"
        )
        self.gridLayout_26.addWidget(
            self.shellArchivesValidateArgsJavaSubtitleLabel, 0, 0, 1, 1
        )
        self.shellArchivesValidateArgsJavaListPushBtn = PushButton(
            self.shellArchivesValidateArgsJavaWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.shellArchivesValidateArgsJavaListPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.shellArchivesValidateArgsJavaListPushBtn.setSizePolicy(sizePolicy)
        self.shellArchivesValidateArgsJavaListPushBtn.setMinimumSize(QSize(108, 31))
        self.shellArchivesValidateArgsJavaListPushBtn.setCursor(
            QCursor(Qt.PointingHandCursor)
        )
        self.shellArchivesValidateArgsJavaListPushBtn.setObjectName(
            "shellArchivesValidateArgsJavaListPushBtn"
        )
        self.gridLayout_26.addWidget(
            self.shellArchivesValidateArgsJavaListPushBtn, 3, 2, 1, 1
        )
        self.shellArchivesValidateArgsManuallyAddJavaPrimaryPushBtn = PrimaryPushButton(
            self.shellArchivesValidateArgsJavaWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.shellArchivesValidateArgsManuallyAddJavaPrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.shellArchivesValidateArgsManuallyAddJavaPrimaryPushBtn.setSizePolicy(
            sizePolicy
        )
        self.shellArchivesValidateArgsManuallyAddJavaPrimaryPushBtn.setMinimumSize(
            QSize(90, 0)
        )
        self.shellArchivesValidateArgsManuallyAddJavaPrimaryPushBtn.setCursor(
            QCursor(Qt.PointingHandCursor)
        )
        self.shellArchivesValidateArgsManuallyAddJavaPrimaryPushBtn.setObjectName(
            "shellArchivesValidateArgsManuallyAddJavaPrimaryPushBtn"
        )
        self.gridLayout_26.addWidget(
            self.shellArchivesValidateArgsManuallyAddJavaPrimaryPushBtn, 2, 1, 1, 1
        )
        self.shellArchivesValidateArgsDownloadJavaPrimaryPushBtn = PrimaryPushButton(
            self.shellArchivesValidateArgsJavaWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.shellArchivesValidateArgsDownloadJavaPrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.shellArchivesValidateArgsDownloadJavaPrimaryPushBtn.setSizePolicy(
            sizePolicy
        )
        self.shellArchivesValidateArgsDownloadJavaPrimaryPushBtn.setMinimumSize(
            QSize(90, 0)
        )
        self.shellArchivesValidateArgsDownloadJavaPrimaryPushBtn.setCursor(
            QCursor(Qt.PointingHandCursor)
        )
        self.shellArchivesValidateArgsDownloadJavaPrimaryPushBtn.setObjectName(
            "shellArchivesValidateArgsDownloadJavaPrimaryPushBtn"
        )
        self.gridLayout_26.addWidget(
            self.shellArchivesValidateArgsDownloadJavaPrimaryPushBtn, 3, 1, 1, 1
        )
        self.shellArchivesValidateArgsJavaTextEdit = TextEdit(
            self.shellArchivesValidateArgsJavaWidget
        )
        self.shellArchivesValidateArgsJavaTextEdit.setObjectName(
            "shellArchivesValidateArgsJavaTextEdit"
        )
        self.gridLayout_26.addWidget(
            self.shellArchivesValidateArgsJavaTextEdit, 2, 0, 2, 1
        )
        self.gridLayout_24.addWidget(
            self.shellArchivesValidateArgsJavaWidget, 5, 2, 1, 3
        )
        self.shellArchivesValidateArgsDeEncodingWidget = QWidget(
            self.shellArchivesValidateArgs
        )
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.shellArchivesValidateArgsDeEncodingWidget.sizePolicy().hasHeightForWidth()
        )
        self.shellArchivesValidateArgsDeEncodingWidget.setSizePolicy(sizePolicy)
        self.shellArchivesValidateArgsDeEncodingWidget.setMinimumSize(QSize(0, 122))
        self.shellArchivesValidateArgsDeEncodingWidget.setMaximumSize(
            QSize(16777215, 122)
        )
        self.shellArchivesValidateArgsDeEncodingWidget.setObjectName(
            "shellArchivesValidateArgsDeEncodingWidget"
        )
        self.gridLayout_27 = QGridLayout(self.shellArchivesValidateArgsDeEncodingWidget)
        self.gridLayout_27.setObjectName("gridLayout_27")
        self.shellArchivesValidateArgsOutputDeEncodingComboBox = ComboBox(
            self.shellArchivesValidateArgsDeEncodingWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.shellArchivesValidateArgsOutputDeEncodingComboBox.sizePolicy().hasHeightForWidth()
        )
        self.shellArchivesValidateArgsOutputDeEncodingComboBox.setSizePolicy(sizePolicy)
        self.shellArchivesValidateArgsOutputDeEncodingComboBox.setObjectName(
            "shellArchivesValidateArgsOutputDeEncodingComboBox"
        )
        self.gridLayout_27.addWidget(
            self.shellArchivesValidateArgsOutputDeEncodingComboBox, 2, 1, 1, 1
        )
        self.shellArchivesValidateArgsInputDeEncodingComboBox = ComboBox(
            self.shellArchivesValidateArgsDeEncodingWidget
        )
        self.shellArchivesValidateArgsInputDeEncodingComboBox.setText("")
        self.shellArchivesValidateArgsInputDeEncodingComboBox.setObjectName(
            "shellArchivesValidateArgsInputDeEncodingComboBox"
        )
        self.gridLayout_27.addWidget(
            self.shellArchivesValidateArgsInputDeEncodingComboBox, 3, 1, 1, 1
        )
        self.shellArchivesValidateArgsOutputDeEncodingLabel = StrongBodyLabel(
            self.shellArchivesValidateArgsDeEncodingWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.shellArchivesValidateArgsOutputDeEncodingLabel.sizePolicy().hasHeightForWidth()
        )
        self.shellArchivesValidateArgsOutputDeEncodingLabel.setSizePolicy(sizePolicy)
        self.shellArchivesValidateArgsOutputDeEncodingLabel.setObjectName(
            "shellArchivesValidateArgsOutputDeEncodingLabel"
        )
        self.gridLayout_27.addWidget(
            self.shellArchivesValidateArgsOutputDeEncodingLabel, 2, 0, 1, 1
        )
        self.shellArchivesValidateArgsDeEncodingSubtitleLabel = SubtitleLabel(
            self.shellArchivesValidateArgsDeEncodingWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.shellArchivesValidateArgsDeEncodingSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.shellArchivesValidateArgsDeEncodingSubtitleLabel.setSizePolicy(sizePolicy)
        self.shellArchivesValidateArgsDeEncodingSubtitleLabel.setObjectName(
            "shellArchivesValidateArgsDeEncodingSubtitleLabel"
        )
        self.gridLayout_27.addWidget(
            self.shellArchivesValidateArgsDeEncodingSubtitleLabel, 0, 0, 1, 1
        )
        self.shellArchivesValidateArgsInputDeEncodingLabel = StrongBodyLabel(
            self.shellArchivesValidateArgsDeEncodingWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.shellArchivesValidateArgsInputDeEncodingLabel.sizePolicy().hasHeightForWidth()
        )
        self.shellArchivesValidateArgsInputDeEncodingLabel.setSizePolicy(sizePolicy)
        self.shellArchivesValidateArgsInputDeEncodingLabel.setObjectName(
            "shellArchivesValidateArgsInputDeEncodingLabel"
        )
        self.gridLayout_27.addWidget(
            self.shellArchivesValidateArgsInputDeEncodingLabel, 3, 0, 1, 1
        )
        self.gridLayout_24.addWidget(
            self.shellArchivesValidateArgsDeEncodingWidget, 8, 2, 1, 3
        )
        self.shellArchivesValidateArgsJVMArgWidget = QWidget(
            self.shellArchivesValidateArgs
        )
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.shellArchivesValidateArgsJVMArgWidget.sizePolicy().hasHeightForWidth()
        )
        self.shellArchivesValidateArgsJVMArgWidget.setSizePolicy(sizePolicy)
        self.shellArchivesValidateArgsJVMArgWidget.setMinimumSize(QSize(0, 140))
        self.shellArchivesValidateArgsJVMArgWidget.setMaximumSize(QSize(16777215, 140))
        self.shellArchivesValidateArgsJVMArgWidget.setObjectName(
            "shellArchivesValidateArgsJVMArgWidget"
        )
        self.gridLayout_25 = QGridLayout(self.shellArchivesValidateArgsJVMArgWidget)
        self.gridLayout_25.setObjectName("gridLayout_25")
        self.shellArchivesValidateArgsJVMArgPlainTextEdit = PlainTextEdit(
            self.shellArchivesValidateArgsJVMArgWidget
        )
        self.shellArchivesValidateArgsJVMArgPlainTextEdit.setObjectName(
            "shellArchivesValidateArgsJVMArgPlainTextEdit"
        )
        self.gridLayout_25.addWidget(
            self.shellArchivesValidateArgsJVMArgPlainTextEdit, 1, 0, 1, 1
        )
        self.shellArchivesValidateArgsJVMArgSubtitleLabel = SubtitleLabel(
            self.shellArchivesValidateArgsJVMArgWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.shellArchivesValidateArgsJVMArgSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.shellArchivesValidateArgsJVMArgSubtitleLabel.setSizePolicy(sizePolicy)
        self.shellArchivesValidateArgsJVMArgSubtitleLabel.setObjectName(
            "shellArchivesValidateArgsJVMArgSubtitleLabel"
        )
        self.gridLayout_25.addWidget(
            self.shellArchivesValidateArgsJVMArgSubtitleLabel, 0, 0, 1, 1
        )
        self.gridLayout_24.addWidget(
            self.shellArchivesValidateArgsJVMArgWidget, 9, 2, 1, 3
        )
        self.shellArchivesValidateArgsStatus = PixmapLabel(
            self.shellArchivesValidateArgs
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.shellArchivesValidateArgsStatus.sizePolicy().hasHeightForWidth()
        )
        self.shellArchivesValidateArgsStatus.setSizePolicy(sizePolicy)
        self.shellArchivesValidateArgsStatus.setMinimumSize(QSize(30, 30))
        self.shellArchivesValidateArgsStatus.setMaximumSize(QSize(30, 30))
        self.shellArchivesValidateArgsStatus.setObjectName(
            "shellArchivesValidateArgsStatus"
        )
        self.gridLayout_24.addWidget(self.shellArchivesValidateArgsStatus, 0, 2, 1, 1)
        self.shellArchivesValidateArgsMemWidget = QWidget(
            self.shellArchivesValidateArgs
        )
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.shellArchivesValidateArgsMemWidget.sizePolicy().hasHeightForWidth()
        )
        self.shellArchivesValidateArgsMemWidget.setSizePolicy(sizePolicy)
        self.shellArchivesValidateArgsMemWidget.setMinimumSize(QSize(0, 85))
        self.shellArchivesValidateArgsMemWidget.setMaximumSize(QSize(16777215, 85))
        self.shellArchivesValidateArgsMemWidget.setObjectName(
            "shellArchivesValidateArgsMemWidget"
        )
        self.gridLayout_28 = QGridLayout(self.shellArchivesValidateArgsMemWidget)
        self.gridLayout_28.setObjectName("gridLayout_28")
        self.shellArchivesValidateArgsMinMemLineEdit = LineEdit(
            self.shellArchivesValidateArgsMemWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.shellArchivesValidateArgsMinMemLineEdit.sizePolicy().hasHeightForWidth()
        )
        self.shellArchivesValidateArgsMinMemLineEdit.setSizePolicy(sizePolicy)
        self.shellArchivesValidateArgsMinMemLineEdit.setMinimumSize(QSize(0, 30))
        self.shellArchivesValidateArgsMinMemLineEdit.setObjectName(
            "shellArchivesValidateArgsMinMemLineEdit"
        )
        self.gridLayout_28.addWidget(
            self.shellArchivesValidateArgsMinMemLineEdit, 1, 1, 1, 1
        )
        self.shellArchivesValidateArgsMemSubtitleLabel = SubtitleLabel(
            self.shellArchivesValidateArgsMemWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.shellArchivesValidateArgsMemSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.shellArchivesValidateArgsMemSubtitleLabel.setSizePolicy(sizePolicy)
        self.shellArchivesValidateArgsMemSubtitleLabel.setObjectName(
            "shellArchivesValidateArgsMemSubtitleLabel"
        )
        self.gridLayout_28.addWidget(
            self.shellArchivesValidateArgsMemSubtitleLabel, 0, 1, 1, 1
        )
        self.shellArchivesValidateArgsMaxMemLineEdit = LineEdit(
            self.shellArchivesValidateArgsMemWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.shellArchivesValidateArgsMaxMemLineEdit.sizePolicy().hasHeightForWidth()
        )
        self.shellArchivesValidateArgsMaxMemLineEdit.setSizePolicy(sizePolicy)
        self.shellArchivesValidateArgsMaxMemLineEdit.setMinimumSize(QSize(0, 30))
        self.shellArchivesValidateArgsMaxMemLineEdit.setObjectName(
            "shellArchivesValidateArgsMaxMemLineEdit"
        )
        self.gridLayout_28.addWidget(
            self.shellArchivesValidateArgsMaxMemLineEdit, 1, 3, 1, 1
        )
        self.shellArchivesValidateArgsToSymbol = SubtitleLabel(
            self.shellArchivesValidateArgsMemWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.shellArchivesValidateArgsToSymbol.sizePolicy().hasHeightForWidth()
        )
        self.shellArchivesValidateArgsToSymbol.setSizePolicy(sizePolicy)
        self.shellArchivesValidateArgsToSymbol.setObjectName(
            "shellArchivesValidateArgsToSymbol"
        )
        self.gridLayout_28.addWidget(self.shellArchivesValidateArgsToSymbol, 1, 2, 1, 1)
        spacerItem42 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_28.addItem(spacerItem42, 1, 5, 1, 1)
        self.shellArchivesValidateArgsMemUnitComboBox = ComboBox(
            self.shellArchivesValidateArgsMemWidget
        )
        self.shellArchivesValidateArgsMemUnitComboBox.setObjectName(
            "shellArchivesValidateArgsMemUnitComboBox"
        )
        self.gridLayout_28.addWidget(
            self.shellArchivesValidateArgsMemUnitComboBox, 1, 4, 1, 1
        )
        self.gridLayout_24.addWidget(
            self.shellArchivesValidateArgsMemWidget, 6, 2, 1, 3
        )
        self.shellArchivesValidateArgsTitle = SubtitleLabel(
            self.shellArchivesValidateArgs
        )
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.shellArchivesValidateArgsTitle.sizePolicy().hasHeightForWidth()
        )
        self.shellArchivesValidateArgsTitle.setSizePolicy(sizePolicy)
        self.shellArchivesValidateArgsTitle.setObjectName(
            "shellArchivesValidateArgsTitle"
        )
        self.gridLayout_24.addWidget(self.shellArchivesValidateArgsTitle, 0, 3, 1, 1)
        self.shellArchivesValidateArgsCoreWidget = QWidget(
            self.shellArchivesValidateArgs
        )
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.shellArchivesValidateArgsCoreWidget.sizePolicy().hasHeightForWidth()
        )
        self.shellArchivesValidateArgsCoreWidget.setSizePolicy(sizePolicy)
        self.shellArchivesValidateArgsCoreWidget.setObjectName(
            "shellArchivesValidateArgsCoreWidget"
        )
        self.gridLayout_31 = QGridLayout(self.shellArchivesValidateArgsCoreWidget)
        self.gridLayout_31.setObjectName("gridLayout_31")
        self.shellArchivesValidateArgsDownloadCorePrimaryPushBtn = PrimaryPushButton(
            self.shellArchivesValidateArgsCoreWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.shellArchivesValidateArgsDownloadCorePrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.shellArchivesValidateArgsDownloadCorePrimaryPushBtn.setSizePolicy(
            sizePolicy
        )
        self.shellArchivesValidateArgsDownloadCorePrimaryPushBtn.setMinimumSize(
            QSize(90, 0)
        )
        self.shellArchivesValidateArgsDownloadCorePrimaryPushBtn.setObjectName(
            "shellArchivesValidateArgsDownloadCorePrimaryPushBtn"
        )
        self.gridLayout_31.addWidget(
            self.shellArchivesValidateArgsDownloadCorePrimaryPushBtn, 1, 3, 1, 1
        )
        self.shellArchivesValidateArgsCoreSubtitleLabel = SubtitleLabel(
            self.shellArchivesValidateArgsCoreWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.shellArchivesValidateArgsCoreSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.shellArchivesValidateArgsCoreSubtitleLabel.setSizePolicy(sizePolicy)
        self.shellArchivesValidateArgsCoreSubtitleLabel.setObjectName(
            "shellArchivesValidateArgsCoreSubtitleLabel"
        )
        self.gridLayout_31.addWidget(
            self.shellArchivesValidateArgsCoreSubtitleLabel, 0, 1, 1, 1
        )
        self.shellArchivesValidateArgsCoreLineEdit = LineEdit(
            self.shellArchivesValidateArgsCoreWidget
        )
        self.shellArchivesValidateArgsCoreLineEdit.setObjectName(
            "shellArchivesValidateArgsCoreLineEdit"
        )
        self.gridLayout_31.addWidget(
            self.shellArchivesValidateArgsCoreLineEdit, 1, 1, 1, 1
        )
        self.shellArchivesValidateArgsManuallyAddCorePrimaryPushBtn = PrimaryPushButton(
            self.shellArchivesValidateArgsCoreWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.shellArchivesValidateArgsManuallyAddCorePrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.shellArchivesValidateArgsManuallyAddCorePrimaryPushBtn.setSizePolicy(
            sizePolicy
        )
        self.shellArchivesValidateArgsManuallyAddCorePrimaryPushBtn.setMinimumSize(
            QSize(90, 0)
        )
        self.shellArchivesValidateArgsManuallyAddCorePrimaryPushBtn.setObjectName(
            "shellArchivesValidateArgsManuallyAddCorePrimaryPushBtn"
        )
        self.gridLayout_31.addWidget(
            self.shellArchivesValidateArgsManuallyAddCorePrimaryPushBtn, 1, 2, 1, 1
        )
        self.gridLayout_24.addWidget(
            self.shellArchivesValidateArgsCoreWidget, 7, 2, 1, 3
        )
        self.verticalLayout_3.addWidget(self.shellArchivesValidateArgs)
        self.shellArchivesSave = CardWidget(self.shellArchivesScrollAreaWidgetContents)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.shellArchivesSave.sizePolicy().hasHeightForWidth()
        )
        self.shellArchivesSave.setSizePolicy(sizePolicy)
        self.shellArchivesSave.setMinimumSize(QSize(0, 125))
        self.shellArchivesSave.setMaximumSize(QSize(16777215, 125))
        self.shellArchivesSave.setObjectName("shellArchivesSave")
        self.gridLayout_29 = QGridLayout(self.shellArchivesSave)
        self.gridLayout_29.setObjectName("gridLayout_29")
        self.shellArchivesSaveTitle = SubtitleLabel(self.shellArchivesSave)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.shellArchivesSaveTitle.sizePolicy().hasHeightForWidth()
        )
        self.shellArchivesSaveTitle.setSizePolicy(sizePolicy)
        self.shellArchivesSaveTitle.setObjectName("shellArchivesSaveTitle")
        self.gridLayout_29.addWidget(self.shellArchivesSaveTitle, 0, 1, 1, 1)
        self.shellArchivesSaveServerNameLineEdit = LineEdit(self.shellArchivesSave)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.shellArchivesSaveServerNameLineEdit.sizePolicy().hasHeightForWidth()
        )
        self.shellArchivesSaveServerNameLineEdit.setSizePolicy(sizePolicy)
        self.shellArchivesSaveServerNameLineEdit.setMinimumSize(QSize(0, 30))
        self.shellArchivesSaveServerNameLineEdit.setObjectName(
            "shellArchivesSaveServerNameLineEdit"
        )
        self.gridLayout_29.addWidget(
            self.shellArchivesSaveServerNameLineEdit, 1, 1, 1, 1
        )
        spacerItem43 = QSpacerItem(20, 79, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout_29.addItem(spacerItem43, 0, 0, 3, 1)
        self.shellArchivesSaveSaveServerPrimaryPushBtn = PrimaryPushButton(
            self.shellArchivesSave
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.shellArchivesSaveSaveServerPrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.shellArchivesSaveSaveServerPrimaryPushBtn.setSizePolicy(sizePolicy)
        self.shellArchivesSaveSaveServerPrimaryPushBtn.setMinimumSize(QSize(130, 30))
        self.shellArchivesSaveSaveServerPrimaryPushBtn.setMaximumSize(
            QSize(16777215, 30)
        )
        self.shellArchivesSaveSaveServerPrimaryPushBtn.setObjectName(
            "shellArchivesSaveSaveServerPrimaryPushBtn"
        )
        self.gridLayout_29.addWidget(
            self.shellArchivesSaveSaveServerPrimaryPushBtn, 2, 1, 1, 1
        )
        self.verticalLayout_3.addWidget(self.shellArchivesSave)
        self.shellArchivesScrollArea.setWidget(
            self.shellArchivesScrollAreaWidgetContents
        )
        self.gridLayout_30.addWidget(self.shellArchivesScrollArea, 1, 2, 1, 2)
        spacerItem44 = QSpacerItem(20, 335, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout_30.addItem(spacerItem44, 0, 0, 2, 1)
        self.importNewServerStackWidget.addWidget(self.shellArchives)
        self.serverArchiveSite = QWidget()
        self.serverArchiveSite.setObjectName("serverArchiveSite")
        self.gridLayout_41 = QGridLayout(self.serverArchiveSite)
        self.gridLayout_41.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_41.setObjectName("gridLayout_41")
        spacerItem45 = QSpacerItem(256, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_41.addItem(spacerItem45, 0, 3, 1, 1)
        self.serverArchiveSiteScrollArea = SmoothScrollArea(self.serverArchiveSite)
        self.serverArchiveSiteScrollArea.setVerticalScrollBarPolicy(
            Qt.ScrollBarAsNeeded
        )
        self.serverArchiveSiteScrollArea.setHorizontalScrollBarPolicy(
            Qt.ScrollBarAsNeeded
        )
        self.serverArchiveSiteScrollArea.setWidgetResizable(True)
        self.serverArchiveSiteScrollArea.setAlignment(Qt.AlignCenter)
        self.serverArchiveSiteScrollArea.setObjectName("serverArchiveSiteScrollArea")
        self.serverArchiveSiteScrollAreaWidgetContents = QWidget()
        self.serverArchiveSiteScrollAreaWidgetContents.setGeometry(
            QRect(0, 0, 450, 935)
        )
        self.serverArchiveSiteScrollAreaWidgetContents.setObjectName(
            "serverArchiveSiteScrollAreaWidgetContents"
        )
        self.verticalLayout_6 = QVBoxLayout(
            self.serverArchiveSiteScrollAreaWidgetContents
        )
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.serverArchiveSiteImport = CardWidget(
            self.serverArchiveSiteScrollAreaWidgetContents
        )
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.serverArchiveSiteImport.sizePolicy().hasHeightForWidth()
        )
        self.serverArchiveSiteImport.setSizePolicy(sizePolicy)
        self.serverArchiveSiteImport.setMinimumSize(QSize(0, 150))
        self.serverArchiveSiteImport.setMaximumSize(QSize(16777215, 150))
        self.serverArchiveSiteImport.setObjectName("serverArchiveSiteImport")
        self.gridLayout_32 = QGridLayout(self.serverArchiveSiteImport)
        self.gridLayout_32.setObjectName("gridLayout_32")
        spacerItem46 = QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout_32.addItem(spacerItem46, 0, 0, 3, 1)
        self.serverArchiveSiteImportStatus = PixmapLabel(self.serverArchiveSiteImport)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.serverArchiveSiteImportStatus.sizePolicy().hasHeightForWidth()
        )
        self.serverArchiveSiteImportStatus.setSizePolicy(sizePolicy)
        self.serverArchiveSiteImportStatus.setMinimumSize(QSize(30, 30))
        self.serverArchiveSiteImportStatus.setMaximumSize(QSize(30, 30))
        self.serverArchiveSiteImportStatus.setObjectName(
            "serverArchiveSiteImportStatus"
        )
        self.gridLayout_32.addWidget(self.serverArchiveSiteImportStatus, 0, 1, 1, 1)
        self.serverArchiveSiteImportStatusText = BodyLabel(self.serverArchiveSiteImport)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.serverArchiveSiteImportStatusText.sizePolicy().hasHeightForWidth()
        )
        self.serverArchiveSiteImportStatusText.setSizePolicy(sizePolicy)
        self.serverArchiveSiteImportStatusText.setObjectName(
            "serverArchiveSiteImportStatusText"
        )
        self.gridLayout_32.addWidget(self.serverArchiveSiteImportStatusText, 1, 1, 1, 2)
        self.serverArchiveSiteImportBtnWidget = QWidget(self.serverArchiveSiteImport)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.serverArchiveSiteImportBtnWidget.sizePolicy().hasHeightForWidth()
        )
        self.serverArchiveSiteImportBtnWidget.setSizePolicy(sizePolicy)
        self.serverArchiveSiteImportBtnWidget.setObjectName(
            "serverArchiveSiteImportBtnWidget"
        )
        self.horizontalLayout_9 = QHBoxLayout(self.serverArchiveSiteImportBtnWidget)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.serverArchiveSiteImportArchives = PrimaryPushButton(
            self.serverArchiveSiteImportBtnWidget
        )
        self.serverArchiveSiteImportArchives.setMinimumSize(QSize(110, 32))
        self.serverArchiveSiteImportArchives.setMaximumSize(QSize(110, 32))
        self.serverArchiveSiteImportArchives.setObjectName(
            "serverArchiveSiteImportArchives"
        )
        self.horizontalLayout_9.addWidget(self.serverArchiveSiteImportArchives)
        self.serverArchiveSiteImportFolder = PrimaryPushButton(
            self.serverArchiveSiteImportBtnWidget
        )
        self.serverArchiveSiteImportFolder.setMinimumSize(QSize(110, 32))
        self.serverArchiveSiteImportFolder.setMaximumSize(QSize(110, 32))
        self.serverArchiveSiteImportFolder.setObjectName(
            "serverArchiveSiteImportFolder"
        )
        self.horizontalLayout_9.addWidget(self.serverArchiveSiteImportFolder)
        self.gridLayout_32.addWidget(self.serverArchiveSiteImportBtnWidget, 2, 1, 1, 2)
        spacerItem47 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_32.addItem(spacerItem47, 2, 6, 1, 2)
        self.serverArchiveSiteImportTitle = SubtitleLabel(self.serverArchiveSiteImport)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.serverArchiveSiteImportTitle.sizePolicy().hasHeightForWidth()
        )
        self.serverArchiveSiteImportTitle.setSizePolicy(sizePolicy)
        self.serverArchiveSiteImportTitle.setObjectName("serverArchiveSiteImportTitle")
        self.gridLayout_32.addWidget(self.serverArchiveSiteImportTitle, 0, 2, 1, 1)
        self.verticalLayout_6.addWidget(self.serverArchiveSiteImport)
        self.serverArchiveSiteSetArgs = CardWidget(
            self.serverArchiveSiteScrollAreaWidgetContents
        )
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.serverArchiveSiteSetArgs.sizePolicy().hasHeightForWidth()
        )
        self.serverArchiveSiteSetArgs.setSizePolicy(sizePolicy)
        self.serverArchiveSiteSetArgs.setMinimumSize(QSize(0, 630))
        self.serverArchiveSiteSetArgs.setMaximumSize(QSize(16777215, 630))
        self.serverArchiveSiteSetArgs.setObjectName("serverArchiveSiteSetArgs")
        self.gridLayout_34 = QGridLayout(self.serverArchiveSiteSetArgs)
        self.gridLayout_34.setObjectName("gridLayout_34")
        spacerItem48 = QSpacerItem(20, 102, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout_34.addItem(spacerItem48, 0, 0, 21, 1)
        self.serverArchiveSiteSetJavaWidget = QWidget(self.serverArchiveSiteSetArgs)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.serverArchiveSiteSetJavaWidget.sizePolicy().hasHeightForWidth()
        )
        self.serverArchiveSiteSetJavaWidget.setSizePolicy(sizePolicy)
        self.serverArchiveSiteSetJavaWidget.setMinimumSize(QSize(0, 120))
        self.serverArchiveSiteSetJavaWidget.setObjectName(
            "serverArchiveSiteSetJavaWidget"
        )
        self.gridLayout_35 = QGridLayout(self.serverArchiveSiteSetJavaWidget)
        self.gridLayout_35.setObjectName("gridLayout_35")
        self.serverArchiveSiteAutoDetectJavaPrimaryPushBtn = PrimaryPushButton(
            self.serverArchiveSiteSetJavaWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.serverArchiveSiteAutoDetectJavaPrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.serverArchiveSiteAutoDetectJavaPrimaryPushBtn.setSizePolicy(sizePolicy)
        self.serverArchiveSiteAutoDetectJavaPrimaryPushBtn.setCursor(
            QCursor(Qt.PointingHandCursor)
        )
        self.serverArchiveSiteAutoDetectJavaPrimaryPushBtn.setObjectName(
            "serverArchiveSiteAutoDetectJavaPrimaryPushBtn"
        )
        self.gridLayout_35.addWidget(
            self.serverArchiveSiteAutoDetectJavaPrimaryPushBtn, 2, 2, 1, 1
        )
        self.serverArchiveSiteJavaSubtitleLabel = SubtitleLabel(
            self.serverArchiveSiteSetJavaWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.serverArchiveSiteJavaSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.serverArchiveSiteJavaSubtitleLabel.setSizePolicy(sizePolicy)
        self.serverArchiveSiteJavaSubtitleLabel.setObjectName(
            "serverArchiveSiteJavaSubtitleLabel"
        )
        self.gridLayout_35.addWidget(
            self.serverArchiveSiteJavaSubtitleLabel, 0, 0, 1, 1
        )
        self.serverArchiveSiteJavaListPushBtn = PushButton(
            self.serverArchiveSiteSetJavaWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.serverArchiveSiteJavaListPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.serverArchiveSiteJavaListPushBtn.setSizePolicy(sizePolicy)
        self.serverArchiveSiteJavaListPushBtn.setMinimumSize(QSize(108, 31))
        self.serverArchiveSiteJavaListPushBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.serverArchiveSiteJavaListPushBtn.setObjectName(
            "serverArchiveSiteJavaListPushBtn"
        )
        self.gridLayout_35.addWidget(self.serverArchiveSiteJavaListPushBtn, 3, 2, 1, 1)
        self.serverArchiveSiteManuallyAddJavaPrimaryPushBtn = PrimaryPushButton(
            self.serverArchiveSiteSetJavaWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.serverArchiveSiteManuallyAddJavaPrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.serverArchiveSiteManuallyAddJavaPrimaryPushBtn.setSizePolicy(sizePolicy)
        self.serverArchiveSiteManuallyAddJavaPrimaryPushBtn.setMinimumSize(QSize(90, 0))
        self.serverArchiveSiteManuallyAddJavaPrimaryPushBtn.setCursor(
            QCursor(Qt.PointingHandCursor)
        )
        self.serverArchiveSiteManuallyAddJavaPrimaryPushBtn.setObjectName(
            "serverArchiveSiteManuallyAddJavaPrimaryPushBtn"
        )
        self.gridLayout_35.addWidget(
            self.serverArchiveSiteManuallyAddJavaPrimaryPushBtn, 2, 1, 1, 1
        )
        self.serverArchiveSiteDownloadJavaPrimaryPushBtn = PrimaryPushButton(
            self.serverArchiveSiteSetJavaWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.serverArchiveSiteDownloadJavaPrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.serverArchiveSiteDownloadJavaPrimaryPushBtn.setSizePolicy(sizePolicy)
        self.serverArchiveSiteDownloadJavaPrimaryPushBtn.setMinimumSize(QSize(90, 0))
        self.serverArchiveSiteDownloadJavaPrimaryPushBtn.setCursor(
            QCursor(Qt.PointingHandCursor)
        )
        self.serverArchiveSiteDownloadJavaPrimaryPushBtn.setObjectName(
            "serverArchiveSiteDownloadJavaPrimaryPushBtn"
        )
        self.gridLayout_35.addWidget(
            self.serverArchiveSiteDownloadJavaPrimaryPushBtn, 3, 1, 1, 1
        )
        self.serverArchiveSiteJavaTextEdit = TextEdit(
            self.serverArchiveSiteSetJavaWidget
        )
        self.serverArchiveSiteJavaTextEdit.setObjectName(
            "serverArchiveSiteJavaTextEdit"
        )
        self.gridLayout_35.addWidget(self.serverArchiveSiteJavaTextEdit, 2, 0, 2, 1)
        self.gridLayout_34.addWidget(self.serverArchiveSiteSetJavaWidget, 5, 2, 1, 3)
        self.serverArchiveSiteSetDeEncodingWidget = QWidget(
            self.serverArchiveSiteSetArgs
        )
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.serverArchiveSiteSetDeEncodingWidget.sizePolicy().hasHeightForWidth()
        )
        self.serverArchiveSiteSetDeEncodingWidget.setSizePolicy(sizePolicy)
        self.serverArchiveSiteSetDeEncodingWidget.setMinimumSize(QSize(0, 122))
        self.serverArchiveSiteSetDeEncodingWidget.setMaximumSize(QSize(16777215, 122))
        self.serverArchiveSiteSetDeEncodingWidget.setObjectName(
            "serverArchiveSiteSetDeEncodingWidget"
        )
        self.gridLayout_36 = QGridLayout(self.serverArchiveSiteSetDeEncodingWidget)
        self.gridLayout_36.setObjectName("gridLayout_36")
        self.serverArchiveSiteOutputDeEncodingComboBox = ComboBox(
            self.serverArchiveSiteSetDeEncodingWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.serverArchiveSiteOutputDeEncodingComboBox.sizePolicy().hasHeightForWidth()
        )
        self.serverArchiveSiteOutputDeEncodingComboBox.setSizePolicy(sizePolicy)
        self.serverArchiveSiteOutputDeEncodingComboBox.setObjectName(
            "serverArchiveSiteOutputDeEncodingComboBox"
        )
        self.gridLayout_36.addWidget(
            self.serverArchiveSiteOutputDeEncodingComboBox, 2, 1, 1, 1
        )
        self.serverArchiveSiteInputDeEncodingComboBox = ComboBox(
            self.serverArchiveSiteSetDeEncodingWidget
        )
        self.serverArchiveSiteInputDeEncodingComboBox.setText("")
        self.serverArchiveSiteInputDeEncodingComboBox.setObjectName(
            "serverArchiveSiteInputDeEncodingComboBox"
        )
        self.gridLayout_36.addWidget(
            self.serverArchiveSiteInputDeEncodingComboBox, 3, 1, 1, 1
        )
        self.serverArchiveSiteOutputDeEncodingLabel = StrongBodyLabel(
            self.serverArchiveSiteSetDeEncodingWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.serverArchiveSiteOutputDeEncodingLabel.sizePolicy().hasHeightForWidth()
        )
        self.serverArchiveSiteOutputDeEncodingLabel.setSizePolicy(sizePolicy)
        self.serverArchiveSiteOutputDeEncodingLabel.setObjectName(
            "serverArchiveSiteOutputDeEncodingLabel"
        )
        self.gridLayout_36.addWidget(
            self.serverArchiveSiteOutputDeEncodingLabel, 2, 0, 1, 1
        )
        self.serverArchiveSiteDeEncodingSubtitleLabel = SubtitleLabel(
            self.serverArchiveSiteSetDeEncodingWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.serverArchiveSiteDeEncodingSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.serverArchiveSiteDeEncodingSubtitleLabel.setSizePolicy(sizePolicy)
        self.serverArchiveSiteDeEncodingSubtitleLabel.setObjectName(
            "serverArchiveSiteDeEncodingSubtitleLabel"
        )
        self.gridLayout_36.addWidget(
            self.serverArchiveSiteDeEncodingSubtitleLabel, 0, 0, 1, 1
        )
        self.serverArchiveSiteInputDeEncodingLabel = StrongBodyLabel(
            self.serverArchiveSiteSetDeEncodingWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.serverArchiveSiteInputDeEncodingLabel.sizePolicy().hasHeightForWidth()
        )
        self.serverArchiveSiteInputDeEncodingLabel.setSizePolicy(sizePolicy)
        self.serverArchiveSiteInputDeEncodingLabel.setObjectName(
            "serverArchiveSiteInputDeEncodingLabel"
        )
        self.gridLayout_36.addWidget(
            self.serverArchiveSiteInputDeEncodingLabel, 3, 0, 1, 1
        )
        self.gridLayout_34.addWidget(
            self.serverArchiveSiteSetDeEncodingWidget, 8, 2, 1, 3
        )
        self.serverArchiveSiteSetJVMArgWidget = QWidget(self.serverArchiveSiteSetArgs)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.serverArchiveSiteSetJVMArgWidget.sizePolicy().hasHeightForWidth()
        )
        self.serverArchiveSiteSetJVMArgWidget.setSizePolicy(sizePolicy)
        self.serverArchiveSiteSetJVMArgWidget.setMinimumSize(QSize(0, 140))
        self.serverArchiveSiteSetJVMArgWidget.setMaximumSize(QSize(16777215, 140))
        self.serverArchiveSiteSetJVMArgWidget.setObjectName(
            "serverArchiveSiteSetJVMArgWidget"
        )
        self.gridLayout_37 = QGridLayout(self.serverArchiveSiteSetJVMArgWidget)
        self.gridLayout_37.setObjectName("gridLayout_37")
        self.serverArchiveSiteJVMArgPlainTextEdit = PlainTextEdit(
            self.serverArchiveSiteSetJVMArgWidget
        )
        self.serverArchiveSiteJVMArgPlainTextEdit.setObjectName(
            "serverArchiveSiteJVMArgPlainTextEdit"
        )
        self.gridLayout_37.addWidget(
            self.serverArchiveSiteJVMArgPlainTextEdit, 1, 0, 1, 1
        )
        self.serverArchiveSiteJVMArgSubtitleLabel = SubtitleLabel(
            self.serverArchiveSiteSetJVMArgWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.serverArchiveSiteJVMArgSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.serverArchiveSiteJVMArgSubtitleLabel.setSizePolicy(sizePolicy)
        self.serverArchiveSiteJVMArgSubtitleLabel.setObjectName(
            "serverArchiveSiteJVMArgSubtitleLabel"
        )
        self.gridLayout_37.addWidget(
            self.serverArchiveSiteJVMArgSubtitleLabel, 0, 0, 1, 1
        )
        self.gridLayout_34.addWidget(self.serverArchiveSiteSetJVMArgWidget, 9, 2, 1, 3)
        self.serverArchiveSiteSetArgsStatus = PixmapLabel(self.serverArchiveSiteSetArgs)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.serverArchiveSiteSetArgsStatus.sizePolicy().hasHeightForWidth()
        )
        self.serverArchiveSiteSetArgsStatus.setSizePolicy(sizePolicy)
        self.serverArchiveSiteSetArgsStatus.setMinimumSize(QSize(30, 30))
        self.serverArchiveSiteSetArgsStatus.setMaximumSize(QSize(30, 30))
        self.serverArchiveSiteSetArgsStatus.setObjectName(
            "serverArchiveSiteSetArgsStatus"
        )
        self.gridLayout_34.addWidget(self.serverArchiveSiteSetArgsStatus, 0, 2, 1, 1)
        self.serverArchiveSiteSetMemWidget = QWidget(self.serverArchiveSiteSetArgs)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.serverArchiveSiteSetMemWidget.sizePolicy().hasHeightForWidth()
        )
        self.serverArchiveSiteSetMemWidget.setSizePolicy(sizePolicy)
        self.serverArchiveSiteSetMemWidget.setMinimumSize(QSize(0, 85))
        self.serverArchiveSiteSetMemWidget.setMaximumSize(QSize(16777215, 85))
        self.serverArchiveSiteSetMemWidget.setObjectName(
            "serverArchiveSiteSetMemWidget"
        )
        self.gridLayout_38 = QGridLayout(self.serverArchiveSiteSetMemWidget)
        self.gridLayout_38.setObjectName("gridLayout_38")
        self.serverArchiveSiteMinMemLineEdit = LineEdit(
            self.serverArchiveSiteSetMemWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.serverArchiveSiteMinMemLineEdit.sizePolicy().hasHeightForWidth()
        )
        self.serverArchiveSiteMinMemLineEdit.setSizePolicy(sizePolicy)
        self.serverArchiveSiteMinMemLineEdit.setMinimumSize(QSize(0, 30))
        self.serverArchiveSiteMinMemLineEdit.setObjectName(
            "serverArchiveSiteMinMemLineEdit"
        )
        self.gridLayout_38.addWidget(self.serverArchiveSiteMinMemLineEdit, 1, 1, 1, 1)
        self.serverArchiveSiteMemSubtitleLabel = SubtitleLabel(
            self.serverArchiveSiteSetMemWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.serverArchiveSiteMemSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.serverArchiveSiteMemSubtitleLabel.setSizePolicy(sizePolicy)
        self.serverArchiveSiteMemSubtitleLabel.setObjectName(
            "serverArchiveSiteMemSubtitleLabel"
        )
        self.gridLayout_38.addWidget(self.serverArchiveSiteMemSubtitleLabel, 0, 1, 1, 1)
        self.serverArchiveSiteMaxMemLineEdit = LineEdit(
            self.serverArchiveSiteSetMemWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.serverArchiveSiteMaxMemLineEdit.sizePolicy().hasHeightForWidth()
        )
        self.serverArchiveSiteMaxMemLineEdit.setSizePolicy(sizePolicy)
        self.serverArchiveSiteMaxMemLineEdit.setMinimumSize(QSize(0, 30))
        self.serverArchiveSiteMaxMemLineEdit.setObjectName(
            "serverArchiveSiteMaxMemLineEdit"
        )
        self.gridLayout_38.addWidget(self.serverArchiveSiteMaxMemLineEdit, 1, 3, 1, 1)
        self.serverArchiveSiteToSymbol = SubtitleLabel(
            self.serverArchiveSiteSetMemWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.serverArchiveSiteToSymbol.sizePolicy().hasHeightForWidth()
        )
        self.serverArchiveSiteToSymbol.setSizePolicy(sizePolicy)
        self.serverArchiveSiteToSymbol.setObjectName("serverArchiveSiteToSymbol")
        self.gridLayout_38.addWidget(self.serverArchiveSiteToSymbol, 1, 2, 1, 1)
        spacerItem49 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_38.addItem(spacerItem49, 1, 5, 1, 1)
        self.serverArchiveSiteMemUnitComboBox = ComboBox(
            self.serverArchiveSiteSetMemWidget
        )
        self.serverArchiveSiteMemUnitComboBox.setObjectName(
            "serverArchiveSiteMemUnitComboBox"
        )
        self.gridLayout_38.addWidget(self.serverArchiveSiteMemUnitComboBox, 1, 4, 1, 1)
        self.gridLayout_34.addWidget(self.serverArchiveSiteSetMemWidget, 6, 2, 1, 3)
        self.serverArchiveSiteSetArgsTitle = SubtitleLabel(
            self.serverArchiveSiteSetArgs
        )
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.serverArchiveSiteSetArgsTitle.sizePolicy().hasHeightForWidth()
        )
        self.serverArchiveSiteSetArgsTitle.setSizePolicy(sizePolicy)
        self.serverArchiveSiteSetArgsTitle.setObjectName(
            "serverArchiveSiteSetArgsTitle"
        )
        self.gridLayout_34.addWidget(self.serverArchiveSiteSetArgsTitle, 0, 3, 1, 1)
        self.serverArchiveSiteSetCoreWidget = QWidget(self.serverArchiveSiteSetArgs)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.serverArchiveSiteSetCoreWidget.sizePolicy().hasHeightForWidth()
        )
        self.serverArchiveSiteSetCoreWidget.setSizePolicy(sizePolicy)
        self.serverArchiveSiteSetCoreWidget.setObjectName(
            "serverArchiveSiteSetCoreWidget"
        )
        self.gridLayout_39 = QGridLayout(self.serverArchiveSiteSetCoreWidget)
        self.gridLayout_39.setObjectName("gridLayout_39")
        self.serverArchiveSiteDownloadCorePrimaryPushBtn = PrimaryPushButton(
            self.serverArchiveSiteSetCoreWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.serverArchiveSiteDownloadCorePrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.serverArchiveSiteDownloadCorePrimaryPushBtn.setSizePolicy(sizePolicy)
        self.serverArchiveSiteDownloadCorePrimaryPushBtn.setMinimumSize(QSize(90, 0))
        self.serverArchiveSiteDownloadCorePrimaryPushBtn.setObjectName(
            "serverArchiveSiteDownloadCorePrimaryPushBtn"
        )
        self.gridLayout_39.addWidget(
            self.serverArchiveSiteDownloadCorePrimaryPushBtn, 1, 3, 1, 1
        )
        self.serverArchiveSiteCoreSubtitleLabel = SubtitleLabel(
            self.serverArchiveSiteSetCoreWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.serverArchiveSiteCoreSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.serverArchiveSiteCoreSubtitleLabel.setSizePolicy(sizePolicy)
        self.serverArchiveSiteCoreSubtitleLabel.setObjectName(
            "serverArchiveSiteCoreSubtitleLabel"
        )
        self.gridLayout_39.addWidget(
            self.serverArchiveSiteCoreSubtitleLabel, 0, 1, 1, 1
        )
        self.serverArchiveSiteCoreLineEdit = LineEdit(
            self.serverArchiveSiteSetCoreWidget
        )
        self.serverArchiveSiteCoreLineEdit.setObjectName(
            "serverArchiveSiteCoreLineEdit"
        )
        self.gridLayout_39.addWidget(self.serverArchiveSiteCoreLineEdit, 1, 1, 1, 1)
        self.serverArchiveSiteManuallyAddCorePrimaryPushBtn = PrimaryPushButton(
            self.serverArchiveSiteSetCoreWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.serverArchiveSiteManuallyAddCorePrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.serverArchiveSiteManuallyAddCorePrimaryPushBtn.setSizePolicy(sizePolicy)
        self.serverArchiveSiteManuallyAddCorePrimaryPushBtn.setMinimumSize(QSize(90, 0))
        self.serverArchiveSiteManuallyAddCorePrimaryPushBtn.setObjectName(
            "serverArchiveSiteManuallyAddCorePrimaryPushBtn"
        )
        self.gridLayout_39.addWidget(
            self.serverArchiveSiteManuallyAddCorePrimaryPushBtn, 1, 2, 1, 1
        )
        self.gridLayout_34.addWidget(self.serverArchiveSiteSetCoreWidget, 7, 2, 1, 3)
        self.verticalLayout_6.addWidget(self.serverArchiveSiteSetArgs)
        self.serverArchiveSiteSave = CardWidget(
            self.serverArchiveSiteScrollAreaWidgetContents
        )
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.serverArchiveSiteSave.sizePolicy().hasHeightForWidth()
        )
        self.serverArchiveSiteSave.setSizePolicy(sizePolicy)
        self.serverArchiveSiteSave.setMinimumSize(QSize(0, 125))
        self.serverArchiveSiteSave.setMaximumSize(QSize(16777215, 125))
        self.serverArchiveSiteSave.setObjectName("serverArchiveSiteSave")
        self.gridLayout_40 = QGridLayout(self.serverArchiveSiteSave)
        self.gridLayout_40.setObjectName("gridLayout_40")
        self.serverArchiveSiteSaveTitle = SubtitleLabel(self.serverArchiveSiteSave)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.serverArchiveSiteSaveTitle.sizePolicy().hasHeightForWidth()
        )
        self.serverArchiveSiteSaveTitle.setSizePolicy(sizePolicy)
        self.serverArchiveSiteSaveTitle.setObjectName("serverArchiveSiteSaveTitle")
        self.gridLayout_40.addWidget(self.serverArchiveSiteSaveTitle, 0, 1, 1, 1)
        self.serverArchiveSiteServerNameLineEdit = LineEdit(self.serverArchiveSiteSave)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.serverArchiveSiteServerNameLineEdit.sizePolicy().hasHeightForWidth()
        )
        self.serverArchiveSiteServerNameLineEdit.setSizePolicy(sizePolicy)
        self.serverArchiveSiteServerNameLineEdit.setMinimumSize(QSize(0, 30))
        self.serverArchiveSiteServerNameLineEdit.setObjectName(
            "serverArchiveSiteServerNameLineEdit"
        )
        self.gridLayout_40.addWidget(
            self.serverArchiveSiteServerNameLineEdit, 1, 1, 1, 1
        )
        spacerItem50 = QSpacerItem(20, 79, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout_40.addItem(spacerItem50, 0, 0, 3, 1)
        self.serverArchiveSiteSaveServerPrimaryPushBtn = PrimaryPushButton(
            self.serverArchiveSiteSave
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.serverArchiveSiteSaveServerPrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.serverArchiveSiteSaveServerPrimaryPushBtn.setSizePolicy(sizePolicy)
        self.serverArchiveSiteSaveServerPrimaryPushBtn.setMinimumSize(QSize(130, 30))
        self.serverArchiveSiteSaveServerPrimaryPushBtn.setMaximumSize(
            QSize(16777215, 30)
        )
        self.serverArchiveSiteSaveServerPrimaryPushBtn.setObjectName(
            "serverArchiveSiteSaveServerPrimaryPushBtn"
        )
        self.gridLayout_40.addWidget(
            self.serverArchiveSiteSaveServerPrimaryPushBtn, 2, 1, 1, 1
        )
        self.verticalLayout_6.addWidget(self.serverArchiveSiteSave)
        self.serverArchiveSiteScrollArea.setWidget(
            self.serverArchiveSiteScrollAreaWidgetContents
        )
        self.gridLayout_41.addWidget(self.serverArchiveSiteScrollArea, 1, 2, 1, 2)
        self.serverArchiveSiteBackToMain = TransparentToolButton(
            FIF.PAGE_LEFT, self.serverArchiveSite
        )
        self.serverArchiveSiteBackToMain.setObjectName("serverArchiveSiteBackToMain")
        self.gridLayout_41.addWidget(self.serverArchiveSiteBackToMain, 0, 1, 1, 1)
        self.serverArchiveSiteTitle = SubtitleLabel(self.serverArchiveSite)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.serverArchiveSiteTitle.sizePolicy().hasHeightForWidth()
        )
        self.serverArchiveSiteTitle.setSizePolicy(sizePolicy)
        self.serverArchiveSiteTitle.setObjectName("serverArchiveSiteTitle")
        self.gridLayout_41.addWidget(self.serverArchiveSiteTitle, 0, 2, 1, 1)
        spacerItem51 = QSpacerItem(20, 299, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.gridLayout_41.addItem(spacerItem51, 1, 1, 1, 1)
        spacerItem52 = QSpacerItem(20, 335, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout_41.addItem(spacerItem52, 0, 0, 2, 1)
        self.importNewServerStackWidget.addWidget(self.serverArchiveSite)
        self.MCSLv1 = QWidget()
        self.MCSLv1.setObjectName("MCSLv1")
        self.gridLayout_49 = QGridLayout(self.MCSLv1)
        self.gridLayout_49.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_49.setObjectName("gridLayout_49")
        spacerItem53 = QSpacerItem(415, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_49.addItem(spacerItem53, 0, 4, 1, 1)
        self.MCSLv1BackToMain = TransparentToolButton(FIF.PAGE_LEFT, self.MCSLv1)
        self.MCSLv1BackToMain.setObjectName("MCSLv1BackToMain")
        self.gridLayout_49.addWidget(self.MCSLv1BackToMain, 0, 2, 1, 1)
        spacerItem54 = QSpacerItem(20, 346, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.gridLayout_49.addItem(spacerItem54, 1, 2, 1, 1)
        self.MCSLv1Title = SubtitleLabel(self.MCSLv1)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.MCSLv1Title.sizePolicy().hasHeightForWidth())
        self.MCSLv1Title.setSizePolicy(sizePolicy)
        self.MCSLv1Title.setObjectName("MCSLv1Title")
        self.gridLayout_49.addWidget(self.MCSLv1Title, 0, 3, 1, 1)
        spacerItem55 = QSpacerItem(20, 335, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout_49.addItem(spacerItem55, 0, 1, 2, 1)
        self.MCSLv1ScrollArea = SmoothScrollArea(self.MCSLv1)
        self.MCSLv1ScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.MCSLv1ScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.MCSLv1ScrollArea.setWidgetResizable(True)
        self.MCSLv1ScrollArea.setAlignment(Qt.AlignCenter)
        self.MCSLv1ScrollArea.setObjectName("MCSLv1ScrollArea")
        self.MCSLv1ScrollAreaWidgetContents = QWidget()
        self.MCSLv1ScrollAreaWidgetContents.setGeometry(QRect(0, 0, 450, 935))
        self.MCSLv1ScrollAreaWidgetContents.setObjectName(
            "MCSLv1ScrollAreaWidgetContents"
        )
        self.verticalLayout_7 = QVBoxLayout(self.MCSLv1ScrollAreaWidgetContents)
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.MCSLv1Import = CardWidget(self.MCSLv1ScrollAreaWidgetContents)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.MCSLv1Import.sizePolicy().hasHeightForWidth())
        self.MCSLv1Import.setSizePolicy(sizePolicy)
        self.MCSLv1Import.setMinimumSize(QSize(0, 150))
        self.MCSLv1Import.setMaximumSize(QSize(16777215, 150))
        self.MCSLv1Import.setObjectName("MCSLv1Import")
        self.gridLayout_33 = QGridLayout(self.MCSLv1Import)
        self.gridLayout_33.setObjectName("gridLayout_33")
        self.MCSLv1ImportStatusText = BodyLabel(self.MCSLv1Import)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv1ImportStatusText.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv1ImportStatusText.setSizePolicy(sizePolicy)
        self.MCSLv1ImportStatusText.setObjectName("MCSLv1ImportStatusText")
        self.gridLayout_33.addWidget(self.MCSLv1ImportStatusText, 1, 1, 1, 2)
        self.MCSLv1ImportTitle = SubtitleLabel(self.MCSLv1Import)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv1ImportTitle.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv1ImportTitle.setSizePolicy(sizePolicy)
        self.MCSLv1ImportTitle.setObjectName("MCSLv1ImportTitle")
        self.gridLayout_33.addWidget(self.MCSLv1ImportTitle, 0, 2, 1, 1)
        spacerItem56 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_33.addItem(spacerItem56, 2, 5, 1, 3)
        self.MCSLv1ImportStatus = PixmapLabel(self.MCSLv1Import)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv1ImportStatus.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv1ImportStatus.setSizePolicy(sizePolicy)
        self.MCSLv1ImportStatus.setMinimumSize(QSize(30, 30))
        self.MCSLv1ImportStatus.setMaximumSize(QSize(30, 30))
        self.MCSLv1ImportStatus.setObjectName("MCSLv1ImportStatus")
        self.gridLayout_33.addWidget(self.MCSLv1ImportStatus, 0, 1, 1, 1)
        spacerItem57 = QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout_33.addItem(spacerItem57, 0, 0, 3, 1)
        self.MCSLv1ImportArchives = PrimaryPushButton(self.MCSLv1Import)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv1ImportArchives.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv1ImportArchives.setSizePolicy(sizePolicy)
        self.MCSLv1ImportArchives.setMinimumSize(QSize(110, 32))
        self.MCSLv1ImportArchives.setMaximumSize(QSize(150, 32))
        self.MCSLv1ImportArchives.setObjectName("MCSLv1ImportArchives")
        self.gridLayout_33.addWidget(self.MCSLv1ImportArchives, 2, 1, 1, 2)
        self.verticalLayout_7.addWidget(self.MCSLv1Import)
        self.MCSLv1ValidateArgs = CardWidget(self.MCSLv1ScrollAreaWidgetContents)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv1ValidateArgs.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv1ValidateArgs.setSizePolicy(sizePolicy)
        self.MCSLv1ValidateArgs.setMinimumSize(QSize(0, 630))
        self.MCSLv1ValidateArgs.setMaximumSize(QSize(16777215, 630))
        self.MCSLv1ValidateArgs.setObjectName("MCSLv1ValidateArgs")
        self.gridLayout_43 = QGridLayout(self.MCSLv1ValidateArgs)
        self.gridLayout_43.setObjectName("gridLayout_43")
        spacerItem58 = QSpacerItem(20, 102, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout_43.addItem(spacerItem58, 0, 0, 21, 1)
        self.MCSLv1ValidateArgsJavaWidget = QWidget(self.MCSLv1ValidateArgs)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv1ValidateArgsJavaWidget.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv1ValidateArgsJavaWidget.setSizePolicy(sizePolicy)
        self.MCSLv1ValidateArgsJavaWidget.setMinimumSize(QSize(0, 120))
        self.MCSLv1ValidateArgsJavaWidget.setObjectName("MCSLv1ValidateArgsJavaWidget")
        self.gridLayout_44 = QGridLayout(self.MCSLv1ValidateArgsJavaWidget)
        self.gridLayout_44.setObjectName("gridLayout_44")
        self.MCSLv1ValidateArgsAutoDetectJavaPrimaryPushBtn = PrimaryPushButton(
            self.MCSLv1ValidateArgsJavaWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv1ValidateArgsAutoDetectJavaPrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv1ValidateArgsAutoDetectJavaPrimaryPushBtn.setSizePolicy(sizePolicy)
        self.MCSLv1ValidateArgsAutoDetectJavaPrimaryPushBtn.setCursor(
            QCursor(Qt.PointingHandCursor)
        )
        self.MCSLv1ValidateArgsAutoDetectJavaPrimaryPushBtn.setObjectName(
            "MCSLv1ValidateArgsAutoDetectJavaPrimaryPushBtn"
        )
        self.gridLayout_44.addWidget(
            self.MCSLv1ValidateArgsAutoDetectJavaPrimaryPushBtn, 2, 2, 1, 1
        )
        self.MCSLv1ValidateArgsJavaSubtitleLabel = SubtitleLabel(
            self.MCSLv1ValidateArgsJavaWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv1ValidateArgsJavaSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv1ValidateArgsJavaSubtitleLabel.setSizePolicy(sizePolicy)
        self.MCSLv1ValidateArgsJavaSubtitleLabel.setObjectName(
            "MCSLv1ValidateArgsJavaSubtitleLabel"
        )
        self.gridLayout_44.addWidget(
            self.MCSLv1ValidateArgsJavaSubtitleLabel, 0, 0, 1, 1
        )
        self.MCSLv1ValidateArgsJavaListPushBtn = PushButton(
            self.MCSLv1ValidateArgsJavaWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv1ValidateArgsJavaListPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv1ValidateArgsJavaListPushBtn.setSizePolicy(sizePolicy)
        self.MCSLv1ValidateArgsJavaListPushBtn.setMinimumSize(QSize(108, 31))
        self.MCSLv1ValidateArgsJavaListPushBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.MCSLv1ValidateArgsJavaListPushBtn.setObjectName(
            "MCSLv1ValidateArgsJavaListPushBtn"
        )
        self.gridLayout_44.addWidget(self.MCSLv1ValidateArgsJavaListPushBtn, 3, 2, 1, 1)
        self.MCSLv1ValidateArgsManuallyAddJavaPrimaryPushBtn = PrimaryPushButton(
            self.MCSLv1ValidateArgsJavaWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv1ValidateArgsManuallyAddJavaPrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv1ValidateArgsManuallyAddJavaPrimaryPushBtn.setSizePolicy(sizePolicy)
        self.MCSLv1ValidateArgsManuallyAddJavaPrimaryPushBtn.setMinimumSize(
            QSize(90, 0)
        )
        self.MCSLv1ValidateArgsManuallyAddJavaPrimaryPushBtn.setCursor(
            QCursor(Qt.PointingHandCursor)
        )
        self.MCSLv1ValidateArgsManuallyAddJavaPrimaryPushBtn.setObjectName(
            "MCSLv1ValidateArgsManuallyAddJavaPrimaryPushBtn"
        )
        self.gridLayout_44.addWidget(
            self.MCSLv1ValidateArgsManuallyAddJavaPrimaryPushBtn, 2, 1, 1, 1
        )
        self.MCSLv1ValidateArgsDownloadJavaPrimaryPushBtn = PrimaryPushButton(
            self.MCSLv1ValidateArgsJavaWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv1ValidateArgsDownloadJavaPrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv1ValidateArgsDownloadJavaPrimaryPushBtn.setSizePolicy(sizePolicy)
        self.MCSLv1ValidateArgsDownloadJavaPrimaryPushBtn.setMinimumSize(QSize(90, 0))
        self.MCSLv1ValidateArgsDownloadJavaPrimaryPushBtn.setCursor(
            QCursor(Qt.PointingHandCursor)
        )
        self.MCSLv1ValidateArgsDownloadJavaPrimaryPushBtn.setObjectName(
            "MCSLv1ValidateArgsDownloadJavaPrimaryPushBtn"
        )
        self.gridLayout_44.addWidget(
            self.MCSLv1ValidateArgsDownloadJavaPrimaryPushBtn, 3, 1, 1, 1
        )
        self.MCSLv1ValidateArgsJavaTextEdit = TextEdit(
            self.MCSLv1ValidateArgsJavaWidget
        )
        self.MCSLv1ValidateArgsJavaTextEdit.setObjectName(
            "MCSLv1ValidateArgsJavaTextEdit"
        )
        self.gridLayout_44.addWidget(self.MCSLv1ValidateArgsJavaTextEdit, 2, 0, 2, 1)
        self.gridLayout_43.addWidget(self.MCSLv1ValidateArgsJavaWidget, 5, 2, 1, 3)
        self.MCSLv1ValidateArgsDeEncodingWidget = QWidget(self.MCSLv1ValidateArgs)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv1ValidateArgsDeEncodingWidget.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv1ValidateArgsDeEncodingWidget.setSizePolicy(sizePolicy)
        self.MCSLv1ValidateArgsDeEncodingWidget.setMinimumSize(QSize(0, 122))
        self.MCSLv1ValidateArgsDeEncodingWidget.setMaximumSize(QSize(16777215, 122))
        self.MCSLv1ValidateArgsDeEncodingWidget.setObjectName(
            "MCSLv1ValidateArgsDeEncodingWidget"
        )
        self.gridLayout_45 = QGridLayout(self.MCSLv1ValidateArgsDeEncodingWidget)
        self.gridLayout_45.setObjectName("gridLayout_45")
        self.MCSLv1ValidateArgsOutputDeEncodingComboBox = ComboBox(
            self.MCSLv1ValidateArgsDeEncodingWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv1ValidateArgsOutputDeEncodingComboBox.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv1ValidateArgsOutputDeEncodingComboBox.setSizePolicy(sizePolicy)
        self.MCSLv1ValidateArgsOutputDeEncodingComboBox.setObjectName(
            "MCSLv1ValidateArgsOutputDeEncodingComboBox"
        )
        self.gridLayout_45.addWidget(
            self.MCSLv1ValidateArgsOutputDeEncodingComboBox, 2, 1, 1, 1
        )
        self.MCSLv1ValidateArgsInputDeEncodingComboBox = ComboBox(
            self.MCSLv1ValidateArgsDeEncodingWidget
        )
        self.MCSLv1ValidateArgsInputDeEncodingComboBox.setText("")
        self.MCSLv1ValidateArgsInputDeEncodingComboBox.setObjectName(
            "MCSLv1ValidateArgsInputDeEncodingComboBox"
        )
        self.gridLayout_45.addWidget(
            self.MCSLv1ValidateArgsInputDeEncodingComboBox, 3, 1, 1, 1
        )
        self.MCSLv1ValidateArgsOutputDeEncodingLabel = StrongBodyLabel(
            self.MCSLv1ValidateArgsDeEncodingWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv1ValidateArgsOutputDeEncodingLabel.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv1ValidateArgsOutputDeEncodingLabel.setSizePolicy(sizePolicy)
        self.MCSLv1ValidateArgsOutputDeEncodingLabel.setObjectName(
            "MCSLv1ValidateArgsOutputDeEncodingLabel"
        )
        self.gridLayout_45.addWidget(
            self.MCSLv1ValidateArgsOutputDeEncodingLabel, 2, 0, 1, 1
        )
        self.MCSLv1ValidateArgsDeEncodingSubtitleLabel = SubtitleLabel(
            self.MCSLv1ValidateArgsDeEncodingWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv1ValidateArgsDeEncodingSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv1ValidateArgsDeEncodingSubtitleLabel.setSizePolicy(sizePolicy)
        self.MCSLv1ValidateArgsDeEncodingSubtitleLabel.setObjectName(
            "MCSLv1ValidateArgsDeEncodingSubtitleLabel"
        )
        self.gridLayout_45.addWidget(
            self.MCSLv1ValidateArgsDeEncodingSubtitleLabel, 0, 0, 1, 1
        )
        self.MCSLv1ValidateArgsInputDeEncodingLabel = StrongBodyLabel(
            self.MCSLv1ValidateArgsDeEncodingWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv1ValidateArgsInputDeEncodingLabel.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv1ValidateArgsInputDeEncodingLabel.setSizePolicy(sizePolicy)
        self.MCSLv1ValidateArgsInputDeEncodingLabel.setObjectName(
            "MCSLv1ValidateArgsInputDeEncodingLabel"
        )
        self.gridLayout_45.addWidget(
            self.MCSLv1ValidateArgsInputDeEncodingLabel, 3, 0, 1, 1
        )
        self.gridLayout_43.addWidget(
            self.MCSLv1ValidateArgsDeEncodingWidget, 8, 2, 1, 3
        )
        self.MCSLv1ValidateArgsJVMArgWidget = QWidget(self.MCSLv1ValidateArgs)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv1ValidateArgsJVMArgWidget.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv1ValidateArgsJVMArgWidget.setSizePolicy(sizePolicy)
        self.MCSLv1ValidateArgsJVMArgWidget.setMinimumSize(QSize(0, 140))
        self.MCSLv1ValidateArgsJVMArgWidget.setMaximumSize(QSize(16777215, 140))
        self.MCSLv1ValidateArgsJVMArgWidget.setObjectName(
            "MCSLv1ValidateArgsJVMArgWidget"
        )
        self.gridLayout_46 = QGridLayout(self.MCSLv1ValidateArgsJVMArgWidget)
        self.gridLayout_46.setObjectName("gridLayout_46")
        self.MCSLv1ValidateArgsJVMArgPlainTextEdit = PlainTextEdit(
            self.MCSLv1ValidateArgsJVMArgWidget
        )
        self.MCSLv1ValidateArgsJVMArgPlainTextEdit.setObjectName(
            "MCSLv1ValidateArgsJVMArgPlainTextEdit"
        )
        self.gridLayout_46.addWidget(
            self.MCSLv1ValidateArgsJVMArgPlainTextEdit, 1, 0, 1, 1
        )
        self.MCSLv1ValidateArgsJVMArgSubtitleLabel = SubtitleLabel(
            self.MCSLv1ValidateArgsJVMArgWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv1ValidateArgsJVMArgSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv1ValidateArgsJVMArgSubtitleLabel.setSizePolicy(sizePolicy)
        self.MCSLv1ValidateArgsJVMArgSubtitleLabel.setObjectName(
            "MCSLv1ValidateArgsJVMArgSubtitleLabel"
        )
        self.gridLayout_46.addWidget(
            self.MCSLv1ValidateArgsJVMArgSubtitleLabel, 0, 0, 1, 1
        )
        self.gridLayout_43.addWidget(self.MCSLv1ValidateArgsJVMArgWidget, 9, 2, 1, 3)
        self.MCSLv1ValidateArgsStatus = PixmapLabel(self.MCSLv1ValidateArgs)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv1ValidateArgsStatus.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv1ValidateArgsStatus.setSizePolicy(sizePolicy)
        self.MCSLv1ValidateArgsStatus.setMinimumSize(QSize(30, 30))
        self.MCSLv1ValidateArgsStatus.setMaximumSize(QSize(30, 30))
        self.MCSLv1ValidateArgsStatus.setObjectName("MCSLv1ValidateArgsStatus")
        self.gridLayout_43.addWidget(self.MCSLv1ValidateArgsStatus, 0, 2, 1, 1)
        self.MCSLv1ValidateArgsMemWidget = QWidget(self.MCSLv1ValidateArgs)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv1ValidateArgsMemWidget.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv1ValidateArgsMemWidget.setSizePolicy(sizePolicy)
        self.MCSLv1ValidateArgsMemWidget.setMinimumSize(QSize(0, 85))
        self.MCSLv1ValidateArgsMemWidget.setMaximumSize(QSize(16777215, 85))
        self.MCSLv1ValidateArgsMemWidget.setObjectName("MCSLv1ValidateArgsMemWidget")
        self.gridLayout_47 = QGridLayout(self.MCSLv1ValidateArgsMemWidget)
        self.gridLayout_47.setObjectName("gridLayout_47")
        self.MCSLv1ValidateArgsMinMemLineEdit = LineEdit(
            self.MCSLv1ValidateArgsMemWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv1ValidateArgsMinMemLineEdit.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv1ValidateArgsMinMemLineEdit.setSizePolicy(sizePolicy)
        self.MCSLv1ValidateArgsMinMemLineEdit.setMinimumSize(QSize(0, 30))
        self.MCSLv1ValidateArgsMinMemLineEdit.setObjectName(
            "MCSLv1ValidateArgsMinMemLineEdit"
        )
        self.gridLayout_47.addWidget(self.MCSLv1ValidateArgsMinMemLineEdit, 1, 1, 1, 1)
        self.MCSLv1ValidateArgsMemSubtitleLabel = SubtitleLabel(
            self.MCSLv1ValidateArgsMemWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv1ValidateArgsMemSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv1ValidateArgsMemSubtitleLabel.setSizePolicy(sizePolicy)
        self.MCSLv1ValidateArgsMemSubtitleLabel.setObjectName(
            "MCSLv1ValidateArgsMemSubtitleLabel"
        )
        self.gridLayout_47.addWidget(
            self.MCSLv1ValidateArgsMemSubtitleLabel, 0, 1, 1, 1
        )
        self.MCSLv1ValidateArgsMaxMemLineEdit = LineEdit(
            self.MCSLv1ValidateArgsMemWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv1ValidateArgsMaxMemLineEdit.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv1ValidateArgsMaxMemLineEdit.setSizePolicy(sizePolicy)
        self.MCSLv1ValidateArgsMaxMemLineEdit.setMinimumSize(QSize(0, 30))
        self.MCSLv1ValidateArgsMaxMemLineEdit.setObjectName(
            "MCSLv1ValidateArgsMaxMemLineEdit"
        )
        self.gridLayout_47.addWidget(self.MCSLv1ValidateArgsMaxMemLineEdit, 1, 3, 1, 1)
        self.MCSLv1ValidateArgsToSymbol = SubtitleLabel(
            self.MCSLv1ValidateArgsMemWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv1ValidateArgsToSymbol.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv1ValidateArgsToSymbol.setSizePolicy(sizePolicy)
        self.MCSLv1ValidateArgsToSymbol.setObjectName("MCSLv1ValidateArgsToSymbol")
        self.gridLayout_47.addWidget(self.MCSLv1ValidateArgsToSymbol, 1, 2, 1, 1)
        spacerItem59 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_47.addItem(spacerItem59, 1, 5, 1, 1)
        self.MCSLv1ValidateArgsMemUnitComboBox = ComboBox(
            self.MCSLv1ValidateArgsMemWidget
        )
        self.MCSLv1ValidateArgsMemUnitComboBox.setObjectName(
            "MCSLv1ValidateArgsMemUnitComboBox"
        )
        self.gridLayout_47.addWidget(self.MCSLv1ValidateArgsMemUnitComboBox, 1, 4, 1, 1)
        self.gridLayout_43.addWidget(self.MCSLv1ValidateArgsMemWidget, 6, 2, 1, 3)
        self.MCSLv1ValidateArgsTitle = SubtitleLabel(self.MCSLv1ValidateArgs)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv1ValidateArgsTitle.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv1ValidateArgsTitle.setSizePolicy(sizePolicy)
        self.MCSLv1ValidateArgsTitle.setObjectName("MCSLv1ValidateArgsTitle")
        self.gridLayout_43.addWidget(self.MCSLv1ValidateArgsTitle, 0, 3, 1, 1)
        self.MCSLv1ValidateArgsCoreWidget = QWidget(self.MCSLv1ValidateArgs)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv1ValidateArgsCoreWidget.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv1ValidateArgsCoreWidget.setSizePolicy(sizePolicy)
        self.MCSLv1ValidateArgsCoreWidget.setObjectName("MCSLv1ValidateArgsCoreWidget")
        self.gridLayout_48 = QGridLayout(self.MCSLv1ValidateArgsCoreWidget)
        self.gridLayout_48.setObjectName("gridLayout_48")
        self.MCSLv1ValidateArgsDownloadCorePrimaryPushBtn = PrimaryPushButton(
            self.MCSLv1ValidateArgsCoreWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv1ValidateArgsDownloadCorePrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv1ValidateArgsDownloadCorePrimaryPushBtn.setSizePolicy(sizePolicy)
        self.MCSLv1ValidateArgsDownloadCorePrimaryPushBtn.setMinimumSize(QSize(90, 0))
        self.MCSLv1ValidateArgsDownloadCorePrimaryPushBtn.setObjectName(
            "MCSLv1ValidateArgsDownloadCorePrimaryPushBtn"
        )
        self.gridLayout_48.addWidget(
            self.MCSLv1ValidateArgsDownloadCorePrimaryPushBtn, 1, 3, 1, 1
        )
        self.MCSLv1ValidateArgsCoreSubtitleLabel = SubtitleLabel(
            self.MCSLv1ValidateArgsCoreWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv1ValidateArgsCoreSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv1ValidateArgsCoreSubtitleLabel.setSizePolicy(sizePolicy)
        self.MCSLv1ValidateArgsCoreSubtitleLabel.setObjectName(
            "MCSLv1ValidateArgsCoreSubtitleLabel"
        )
        self.gridLayout_48.addWidget(
            self.MCSLv1ValidateArgsCoreSubtitleLabel, 0, 1, 1, 1
        )
        self.MCSLv1ValidateArgsCoreLineEdit = LineEdit(
            self.MCSLv1ValidateArgsCoreWidget
        )
        self.MCSLv1ValidateArgsCoreLineEdit.setObjectName(
            "MCSLv1ValidateArgsCoreLineEdit"
        )
        self.gridLayout_48.addWidget(self.MCSLv1ValidateArgsCoreLineEdit, 1, 1, 1, 1)
        self.MCSLv1ValidateArgsManuallyAddCorePrimaryPushBtn = PrimaryPushButton(
            self.MCSLv1ValidateArgsCoreWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv1ValidateArgsManuallyAddCorePrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv1ValidateArgsManuallyAddCorePrimaryPushBtn.setSizePolicy(sizePolicy)
        self.MCSLv1ValidateArgsManuallyAddCorePrimaryPushBtn.setMinimumSize(
            QSize(90, 0)
        )
        self.MCSLv1ValidateArgsManuallyAddCorePrimaryPushBtn.setObjectName(
            "MCSLv1ValidateArgsManuallyAddCorePrimaryPushBtn"
        )
        self.gridLayout_48.addWidget(
            self.MCSLv1ValidateArgsManuallyAddCorePrimaryPushBtn, 1, 2, 1, 1
        )
        self.gridLayout_43.addWidget(self.MCSLv1ValidateArgsCoreWidget, 7, 2, 1, 3)
        self.verticalLayout_7.addWidget(self.MCSLv1ValidateArgs)
        self.MCSLv1Save = CardWidget(self.MCSLv1ScrollAreaWidgetContents)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.MCSLv1Save.sizePolicy().hasHeightForWidth())
        self.MCSLv1Save.setSizePolicy(sizePolicy)
        self.MCSLv1Save.setMinimumSize(QSize(0, 125))
        self.MCSLv1Save.setMaximumSize(QSize(16777215, 125))
        self.MCSLv1Save.setObjectName("MCSLv1Save")
        self.gridLayout_50 = QGridLayout(self.MCSLv1Save)
        self.gridLayout_50.setObjectName("gridLayout_50")
        self.MCSLv1SaveTitle = SubtitleLabel(self.MCSLv1Save)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv1SaveTitle.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv1SaveTitle.setSizePolicy(sizePolicy)
        self.MCSLv1SaveTitle.setObjectName("MCSLv1SaveTitle")
        self.gridLayout_50.addWidget(self.MCSLv1SaveTitle, 0, 1, 1, 1)
        self.MCSLv1SaveServerNameLineEdit = LineEdit(self.MCSLv1Save)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv1SaveServerNameLineEdit.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv1SaveServerNameLineEdit.setSizePolicy(sizePolicy)
        self.MCSLv1SaveServerNameLineEdit.setMinimumSize(QSize(0, 30))
        self.MCSLv1SaveServerNameLineEdit.setObjectName("MCSLv1SaveServerNameLineEdit")
        self.gridLayout_50.addWidget(self.MCSLv1SaveServerNameLineEdit, 1, 1, 1, 1)
        spacerItem60 = QSpacerItem(20, 79, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout_50.addItem(spacerItem60, 0, 0, 3, 1)
        self.MCSLv1SaveServerPrimaryPushBtn = PrimaryPushButton(self.MCSLv1Save)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv1SaveServerPrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv1SaveServerPrimaryPushBtn.setSizePolicy(sizePolicy)
        self.MCSLv1SaveServerPrimaryPushBtn.setMinimumSize(QSize(130, 30))
        self.MCSLv1SaveServerPrimaryPushBtn.setMaximumSize(QSize(16777215, 30))
        self.MCSLv1SaveServerPrimaryPushBtn.setObjectName(
            "MCSLv1SaveServerPrimaryPushBtn"
        )
        self.gridLayout_50.addWidget(self.MCSLv1SaveServerPrimaryPushBtn, 2, 1, 1, 1)
        self.verticalLayout_7.addWidget(self.MCSLv1Save)
        self.MCSLv1ScrollArea.setWidget(self.MCSLv1ScrollAreaWidgetContents)
        self.gridLayout_49.addWidget(self.MCSLv1ScrollArea, 1, 3, 1, 2)
        self.importNewServerStackWidget.addWidget(self.MCSLv1)
        self.MCSLv2 = QWidget()
        self.MCSLv2.setObjectName("MCSLv2")
        self.gridLayout_58 = QGridLayout(self.MCSLv2)
        self.gridLayout_58.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_58.setObjectName("gridLayout_58")
        spacerItem61 = QSpacerItem(20, 346, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.gridLayout_58.addItem(spacerItem61, 1, 2, 1, 1)
        self.MCSLv2Title = SubtitleLabel(self.MCSLv2)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.MCSLv2Title.sizePolicy().hasHeightForWidth())
        self.MCSLv2Title.setSizePolicy(sizePolicy)
        self.MCSLv2Title.setObjectName("MCSLv2Title")
        self.gridLayout_58.addWidget(self.MCSLv2Title, 0, 3, 1, 1)
        self.MCSLv2BackToMain = TransparentToolButton(FIF.PAGE_LEFT, self.MCSLv2)
        self.MCSLv2BackToMain.setObjectName("MCSLv2BackToMain")
        self.gridLayout_58.addWidget(self.MCSLv2BackToMain, 0, 2, 1, 1)
        self.MCSLv2ScrollArea = SmoothScrollArea(self.MCSLv2)
        self.MCSLv2ScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.MCSLv2ScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.MCSLv2ScrollArea.setWidgetResizable(True)
        self.MCSLv2ScrollArea.setAlignment(Qt.AlignCenter)
        self.MCSLv2ScrollArea.setObjectName("MCSLv2ScrollArea")
        self.MCSLv2ScrollAreaWidgetContents = QWidget()
        self.MCSLv2ScrollAreaWidgetContents.setGeometry(QRect(0, 0, 526, 935))
        self.MCSLv2ScrollAreaWidgetContents.setObjectName(
            "MCSLv2ScrollAreaWidgetContents"
        )
        self.verticalLayout_8 = QVBoxLayout(self.MCSLv2ScrollAreaWidgetContents)
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.MCSLv2Import = CardWidget(self.MCSLv2ScrollAreaWidgetContents)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.MCSLv2Import.sizePolicy().hasHeightForWidth())
        self.MCSLv2Import.setSizePolicy(sizePolicy)
        self.MCSLv2Import.setMinimumSize(QSize(0, 150))
        self.MCSLv2Import.setMaximumSize(QSize(16777215, 150))
        self.MCSLv2Import.setObjectName("MCSLv2Import")
        self.gridLayout_42 = QGridLayout(self.MCSLv2Import)
        self.gridLayout_42.setObjectName("gridLayout_42")
        self.MCSLv2ImportStatusText = BodyLabel(self.MCSLv2Import)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv2ImportStatusText.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv2ImportStatusText.setSizePolicy(sizePolicy)
        self.MCSLv2ImportStatusText.setObjectName("MCSLv2ImportStatusText")
        self.gridLayout_42.addWidget(self.MCSLv2ImportStatusText, 1, 1, 1, 2)
        self.MCSLv2ImportTitle = SubtitleLabel(self.MCSLv2Import)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv2ImportTitle.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv2ImportTitle.setSizePolicy(sizePolicy)
        self.MCSLv2ImportTitle.setObjectName("MCSLv2ImportTitle")
        self.gridLayout_42.addWidget(self.MCSLv2ImportTitle, 0, 2, 1, 1)
        spacerItem62 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_42.addItem(spacerItem62, 2, 5, 1, 3)
        self.MCSLv2ImportStatus = PixmapLabel(self.MCSLv2Import)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv2ImportStatus.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv2ImportStatus.setSizePolicy(sizePolicy)
        self.MCSLv2ImportStatus.setMinimumSize(QSize(30, 30))
        self.MCSLv2ImportStatus.setMaximumSize(QSize(30, 30))
        self.MCSLv2ImportStatus.setObjectName("MCSLv2ImportStatus")
        self.gridLayout_42.addWidget(self.MCSLv2ImportStatus, 0, 1, 1, 1)
        spacerItem63 = QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout_42.addItem(spacerItem63, 0, 0, 3, 1)
        self.MCSLv2ImportArchives = PrimaryPushButton(self.MCSLv2Import)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv2ImportArchives.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv2ImportArchives.setSizePolicy(sizePolicy)
        self.MCSLv2ImportArchives.setMinimumSize(QSize(110, 32))
        self.MCSLv2ImportArchives.setMaximumSize(QSize(150, 32))
        self.MCSLv2ImportArchives.setObjectName("MCSLv2ImportArchives")
        self.gridLayout_42.addWidget(self.MCSLv2ImportArchives, 2, 1, 1, 2)
        self.verticalLayout_8.addWidget(self.MCSLv2Import)
        self.MCSLv2ValidateArgs = CardWidget(self.MCSLv2ScrollAreaWidgetContents)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv2ValidateArgs.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv2ValidateArgs.setSizePolicy(sizePolicy)
        self.MCSLv2ValidateArgs.setMinimumSize(QSize(0, 630))
        self.MCSLv2ValidateArgs.setMaximumSize(QSize(16777215, 630))
        self.MCSLv2ValidateArgs.setObjectName("MCSLv2ValidateArgs")
        self.gridLayout_51 = QGridLayout(self.MCSLv2ValidateArgs)
        self.gridLayout_51.setObjectName("gridLayout_51")
        spacerItem64 = QSpacerItem(20, 102, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout_51.addItem(spacerItem64, 0, 0, 21, 1)
        self.MCSLv2ValidateArgsJavaWidget = QWidget(self.MCSLv2ValidateArgs)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv2ValidateArgsJavaWidget.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv2ValidateArgsJavaWidget.setSizePolicy(sizePolicy)
        self.MCSLv2ValidateArgsJavaWidget.setMinimumSize(QSize(0, 120))
        self.MCSLv2ValidateArgsJavaWidget.setObjectName("MCSLv2ValidateArgsJavaWidget")
        self.gridLayout_52 = QGridLayout(self.MCSLv2ValidateArgsJavaWidget)
        self.gridLayout_52.setObjectName("gridLayout_52")
        self.MCSLv2ValidateArgsAutoDetectJavaPrimaryPushBtn = PrimaryPushButton(
            self.MCSLv2ValidateArgsJavaWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv2ValidateArgsAutoDetectJavaPrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv2ValidateArgsAutoDetectJavaPrimaryPushBtn.setSizePolicy(sizePolicy)
        self.MCSLv2ValidateArgsAutoDetectJavaPrimaryPushBtn.setCursor(
            QCursor(Qt.PointingHandCursor)
        )
        self.MCSLv2ValidateArgsAutoDetectJavaPrimaryPushBtn.setObjectName(
            "MCSLv2ValidateArgsAutoDetectJavaPrimaryPushBtn"
        )
        self.gridLayout_52.addWidget(
            self.MCSLv2ValidateArgsAutoDetectJavaPrimaryPushBtn, 2, 2, 1, 1
        )
        self.MCSLv2ValidateArgsJavaSubtitleLabel = SubtitleLabel(
            self.MCSLv2ValidateArgsJavaWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv2ValidateArgsJavaSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv2ValidateArgsJavaSubtitleLabel.setSizePolicy(sizePolicy)
        self.MCSLv2ValidateArgsJavaSubtitleLabel.setObjectName(
            "MCSLv2ValidateArgsJavaSubtitleLabel"
        )
        self.gridLayout_52.addWidget(
            self.MCSLv2ValidateArgsJavaSubtitleLabel, 0, 0, 1, 1
        )
        self.MCSLv2ValidateArgsJavaListPushBtn = PushButton(
            self.MCSLv2ValidateArgsJavaWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv2ValidateArgsJavaListPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv2ValidateArgsJavaListPushBtn.setSizePolicy(sizePolicy)
        self.MCSLv2ValidateArgsJavaListPushBtn.setMinimumSize(QSize(108, 31))
        self.MCSLv2ValidateArgsJavaListPushBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.MCSLv2ValidateArgsJavaListPushBtn.setObjectName(
            "MCSLv2ValidateArgsJavaListPushBtn"
        )
        self.gridLayout_52.addWidget(self.MCSLv2ValidateArgsJavaListPushBtn, 3, 2, 1, 1)
        self.MCSLv2ValidateArgsManuallyAddJavaPrimaryPushBtn = PrimaryPushButton(
            self.MCSLv2ValidateArgsJavaWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv2ValidateArgsManuallyAddJavaPrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv2ValidateArgsManuallyAddJavaPrimaryPushBtn.setSizePolicy(sizePolicy)
        self.MCSLv2ValidateArgsManuallyAddJavaPrimaryPushBtn.setMinimumSize(
            QSize(90, 0)
        )
        self.MCSLv2ValidateArgsManuallyAddJavaPrimaryPushBtn.setCursor(
            QCursor(Qt.PointingHandCursor)
        )
        self.MCSLv2ValidateArgsManuallyAddJavaPrimaryPushBtn.setObjectName(
            "MCSLv2ValidateArgsManuallyAddJavaPrimaryPushBtn"
        )
        self.gridLayout_52.addWidget(
            self.MCSLv2ValidateArgsManuallyAddJavaPrimaryPushBtn, 2, 1, 1, 1
        )
        self.MCSLv2ValidateArgsDownloadJavaPrimaryPushBtn = PrimaryPushButton(
            self.MCSLv2ValidateArgsJavaWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv2ValidateArgsDownloadJavaPrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv2ValidateArgsDownloadJavaPrimaryPushBtn.setSizePolicy(sizePolicy)
        self.MCSLv2ValidateArgsDownloadJavaPrimaryPushBtn.setMinimumSize(QSize(90, 0))
        self.MCSLv2ValidateArgsDownloadJavaPrimaryPushBtn.setCursor(
            QCursor(Qt.PointingHandCursor)
        )
        self.MCSLv2ValidateArgsDownloadJavaPrimaryPushBtn.setObjectName(
            "MCSLv2ValidateArgsDownloadJavaPrimaryPushBtn"
        )
        self.gridLayout_52.addWidget(
            self.MCSLv2ValidateArgsDownloadJavaPrimaryPushBtn, 3, 1, 1, 1
        )
        self.MCSLv2ValidateArgsJavaTextEdit = TextEdit(
            self.MCSLv2ValidateArgsJavaWidget
        )
        self.MCSLv2ValidateArgsJavaTextEdit.setObjectName(
            "MCSLv2ValidateArgsJavaTextEdit"
        )
        self.gridLayout_52.addWidget(self.MCSLv2ValidateArgsJavaTextEdit, 2, 0, 2, 1)
        self.gridLayout_51.addWidget(self.MCSLv2ValidateArgsJavaWidget, 5, 2, 1, 3)
        self.MCSLv2ValidateArgsDeEncodingWidget = QWidget(self.MCSLv2ValidateArgs)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv2ValidateArgsDeEncodingWidget.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv2ValidateArgsDeEncodingWidget.setSizePolicy(sizePolicy)
        self.MCSLv2ValidateArgsDeEncodingWidget.setMinimumSize(QSize(0, 122))
        self.MCSLv2ValidateArgsDeEncodingWidget.setMaximumSize(QSize(16777215, 122))
        self.MCSLv2ValidateArgsDeEncodingWidget.setObjectName(
            "MCSLv2ValidateArgsDeEncodingWidget"
        )
        self.gridLayout_53 = QGridLayout(self.MCSLv2ValidateArgsDeEncodingWidget)
        self.gridLayout_53.setObjectName("gridLayout_53")
        self.MCSLv2ValidateArgsOutputDeEncodingComboBox = ComboBox(
            self.MCSLv2ValidateArgsDeEncodingWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv2ValidateArgsOutputDeEncodingComboBox.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv2ValidateArgsOutputDeEncodingComboBox.setSizePolicy(sizePolicy)
        self.MCSLv2ValidateArgsOutputDeEncodingComboBox.setObjectName(
            "MCSLv2ValidateArgsOutputDeEncodingComboBox"
        )
        self.gridLayout_53.addWidget(
            self.MCSLv2ValidateArgsOutputDeEncodingComboBox, 2, 1, 1, 1
        )
        self.MCSLv2ValidateArgsInputDeEncodingComboBox = ComboBox(
            self.MCSLv2ValidateArgsDeEncodingWidget
        )
        self.MCSLv2ValidateArgsInputDeEncodingComboBox.setText("")
        self.MCSLv2ValidateArgsInputDeEncodingComboBox.setObjectName(
            "MCSLv2ValidateArgsInputDeEncodingComboBox"
        )
        self.gridLayout_53.addWidget(
            self.MCSLv2ValidateArgsInputDeEncodingComboBox, 3, 1, 1, 1
        )
        self.MCSLv2ValidateArgsOutputDeEncodingLabel = StrongBodyLabel(
            self.MCSLv2ValidateArgsDeEncodingWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv2ValidateArgsOutputDeEncodingLabel.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv2ValidateArgsOutputDeEncodingLabel.setSizePolicy(sizePolicy)
        self.MCSLv2ValidateArgsOutputDeEncodingLabel.setObjectName(
            "MCSLv2ValidateArgsOutputDeEncodingLabel"
        )
        self.gridLayout_53.addWidget(
            self.MCSLv2ValidateArgsOutputDeEncodingLabel, 2, 0, 1, 1
        )
        self.MCSLv2ValidateArgsDeEncodingSubtitleLabel = SubtitleLabel(
            self.MCSLv2ValidateArgsDeEncodingWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv2ValidateArgsDeEncodingSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv2ValidateArgsDeEncodingSubtitleLabel.setSizePolicy(sizePolicy)
        self.MCSLv2ValidateArgsDeEncodingSubtitleLabel.setObjectName(
            "MCSLv2ValidateArgsDeEncodingSubtitleLabel"
        )
        self.gridLayout_53.addWidget(
            self.MCSLv2ValidateArgsDeEncodingSubtitleLabel, 0, 0, 1, 1
        )
        self.MCSLv2ValidateArgsInputDeEncodingLabel = StrongBodyLabel(
            self.MCSLv2ValidateArgsDeEncodingWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv2ValidateArgsInputDeEncodingLabel.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv2ValidateArgsInputDeEncodingLabel.setSizePolicy(sizePolicy)
        self.MCSLv2ValidateArgsInputDeEncodingLabel.setObjectName(
            "MCSLv2ValidateArgsInputDeEncodingLabel"
        )
        self.gridLayout_53.addWidget(
            self.MCSLv2ValidateArgsInputDeEncodingLabel, 3, 0, 1, 1
        )
        self.gridLayout_51.addWidget(
            self.MCSLv2ValidateArgsDeEncodingWidget, 8, 2, 1, 3
        )
        self.MCSLv2ValidateArgsJVMArgWidget = QWidget(self.MCSLv2ValidateArgs)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv2ValidateArgsJVMArgWidget.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv2ValidateArgsJVMArgWidget.setSizePolicy(sizePolicy)
        self.MCSLv2ValidateArgsJVMArgWidget.setMinimumSize(QSize(0, 140))
        self.MCSLv2ValidateArgsJVMArgWidget.setMaximumSize(QSize(16777215, 140))
        self.MCSLv2ValidateArgsJVMArgWidget.setObjectName(
            "MCSLv2ValidateArgsJVMArgWidget"
        )
        self.gridLayout_54 = QGridLayout(self.MCSLv2ValidateArgsJVMArgWidget)
        self.gridLayout_54.setObjectName("gridLayout_54")
        self.MCSLv2ValidateArgsJVMArgPlainTextEdit = PlainTextEdit(
            self.MCSLv2ValidateArgsJVMArgWidget
        )
        self.MCSLv2ValidateArgsJVMArgPlainTextEdit.setObjectName(
            "MCSLv2ValidateArgsJVMArgPlainTextEdit"
        )
        self.gridLayout_54.addWidget(
            self.MCSLv2ValidateArgsJVMArgPlainTextEdit, 1, 0, 1, 1
        )
        self.MCSLv2ValidateArgsJVMArgSubtitleLabel = SubtitleLabel(
            self.MCSLv2ValidateArgsJVMArgWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv2ValidateArgsJVMArgSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv2ValidateArgsJVMArgSubtitleLabel.setSizePolicy(sizePolicy)
        self.MCSLv2ValidateArgsJVMArgSubtitleLabel.setObjectName(
            "MCSLv2ValidateArgsJVMArgSubtitleLabel"
        )
        self.gridLayout_54.addWidget(
            self.MCSLv2ValidateArgsJVMArgSubtitleLabel, 0, 0, 1, 1
        )
        self.gridLayout_51.addWidget(self.MCSLv2ValidateArgsJVMArgWidget, 9, 2, 1, 3)
        self.MCSLv2ValidateArgsStatus = PixmapLabel(self.MCSLv2ValidateArgs)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv2ValidateArgsStatus.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv2ValidateArgsStatus.setSizePolicy(sizePolicy)
        self.MCSLv2ValidateArgsStatus.setMinimumSize(QSize(30, 30))
        self.MCSLv2ValidateArgsStatus.setMaximumSize(QSize(30, 30))
        self.MCSLv2ValidateArgsStatus.setObjectName("MCSLv2ValidateArgsStatus")
        self.gridLayout_51.addWidget(self.MCSLv2ValidateArgsStatus, 0, 2, 1, 1)
        self.MCSLv2ValidateArgsMemWidget = QWidget(self.MCSLv2ValidateArgs)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv2ValidateArgsMemWidget.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv2ValidateArgsMemWidget.setSizePolicy(sizePolicy)
        self.MCSLv2ValidateArgsMemWidget.setMinimumSize(QSize(0, 85))
        self.MCSLv2ValidateArgsMemWidget.setMaximumSize(QSize(16777215, 85))
        self.MCSLv2ValidateArgsMemWidget.setObjectName("MCSLv2ValidateArgsMemWidget")
        self.gridLayout_55 = QGridLayout(self.MCSLv2ValidateArgsMemWidget)
        self.gridLayout_55.setObjectName("gridLayout_55")
        self.MCSLv2ValidateArgsMinMemLineEdit = LineEdit(
            self.MCSLv2ValidateArgsMemWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv2ValidateArgsMinMemLineEdit.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv2ValidateArgsMinMemLineEdit.setSizePolicy(sizePolicy)
        self.MCSLv2ValidateArgsMinMemLineEdit.setMinimumSize(QSize(0, 30))
        self.MCSLv2ValidateArgsMinMemLineEdit.setObjectName(
            "MCSLv2ValidateArgsMinMemLineEdit"
        )
        self.gridLayout_55.addWidget(self.MCSLv2ValidateArgsMinMemLineEdit, 1, 1, 1, 1)
        self.MCSLv2ValidateArgsMemSubtitleLabel = SubtitleLabel(
            self.MCSLv2ValidateArgsMemWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv2ValidateArgsMemSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv2ValidateArgsMemSubtitleLabel.setSizePolicy(sizePolicy)
        self.MCSLv2ValidateArgsMemSubtitleLabel.setObjectName(
            "MCSLv2ValidateArgsMemSubtitleLabel"
        )
        self.gridLayout_55.addWidget(
            self.MCSLv2ValidateArgsMemSubtitleLabel, 0, 1, 1, 1
        )
        self.MCSLv2ValidateArgsMaxMemLineEdit = LineEdit(
            self.MCSLv2ValidateArgsMemWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv2ValidateArgsMaxMemLineEdit.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv2ValidateArgsMaxMemLineEdit.setSizePolicy(sizePolicy)
        self.MCSLv2ValidateArgsMaxMemLineEdit.setMinimumSize(QSize(0, 30))
        self.MCSLv2ValidateArgsMaxMemLineEdit.setObjectName(
            "MCSLv2ValidateArgsMaxMemLineEdit"
        )
        self.gridLayout_55.addWidget(self.MCSLv2ValidateArgsMaxMemLineEdit, 1, 3, 1, 1)
        self.MCSLv2ValidateArgsToSymbol = SubtitleLabel(
            self.MCSLv2ValidateArgsMemWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv2ValidateArgsToSymbol.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv2ValidateArgsToSymbol.setSizePolicy(sizePolicy)
        self.MCSLv2ValidateArgsToSymbol.setObjectName("MCSLv2ValidateArgsToSymbol")
        self.gridLayout_55.addWidget(self.MCSLv2ValidateArgsToSymbol, 1, 2, 1, 1)
        spacerItem65 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_55.addItem(spacerItem65, 1, 5, 1, 1)
        self.MCSLv2ValidateArgsMemUnitComboBox = ComboBox(
            self.MCSLv2ValidateArgsMemWidget
        )
        self.MCSLv2ValidateArgsMemUnitComboBox.setObjectName(
            "MCSLv2ValidateArgsMemUnitComboBox"
        )
        self.gridLayout_55.addWidget(self.MCSLv2ValidateArgsMemUnitComboBox, 1, 4, 1, 1)
        self.gridLayout_51.addWidget(self.MCSLv2ValidateArgsMemWidget, 6, 2, 1, 3)
        self.MCSLv2ValidateArgsTitle = SubtitleLabel(self.MCSLv2ValidateArgs)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv2ValidateArgsTitle.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv2ValidateArgsTitle.setSizePolicy(sizePolicy)
        self.MCSLv2ValidateArgsTitle.setObjectName("MCSLv2ValidateArgsTitle")
        self.gridLayout_51.addWidget(self.MCSLv2ValidateArgsTitle, 0, 3, 1, 1)
        self.MCSLv2ValidateArgsCoreWidget = QWidget(self.MCSLv2ValidateArgs)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv2ValidateArgsCoreWidget.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv2ValidateArgsCoreWidget.setSizePolicy(sizePolicy)
        self.MCSLv2ValidateArgsCoreWidget.setObjectName("MCSLv2ValidateArgsCoreWidget")
        self.gridLayout_56 = QGridLayout(self.MCSLv2ValidateArgsCoreWidget)
        self.gridLayout_56.setObjectName("gridLayout_56")
        self.MCSLv2ValidateArgsDownloadCorePrimaryPushBtn = PrimaryPushButton(
            self.MCSLv2ValidateArgsCoreWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv2ValidateArgsDownloadCorePrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv2ValidateArgsDownloadCorePrimaryPushBtn.setSizePolicy(sizePolicy)
        self.MCSLv2ValidateArgsDownloadCorePrimaryPushBtn.setMinimumSize(QSize(90, 0))
        self.MCSLv2ValidateArgsDownloadCorePrimaryPushBtn.setObjectName(
            "MCSLv2ValidateArgsDownloadCorePrimaryPushBtn"
        )
        self.gridLayout_56.addWidget(
            self.MCSLv2ValidateArgsDownloadCorePrimaryPushBtn, 1, 3, 1, 1
        )
        self.MCSLv2ValidateArgsCoreSubtitleLabel = SubtitleLabel(
            self.MCSLv2ValidateArgsCoreWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv2ValidateArgsCoreSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv2ValidateArgsCoreSubtitleLabel.setSizePolicy(sizePolicy)
        self.MCSLv2ValidateArgsCoreSubtitleLabel.setObjectName(
            "MCSLv2ValidateArgsCoreSubtitleLabel"
        )
        self.gridLayout_56.addWidget(
            self.MCSLv2ValidateArgsCoreSubtitleLabel, 0, 1, 1, 1
        )
        self.MCSLv2ValidateArgsCoreLineEdit = LineEdit(
            self.MCSLv2ValidateArgsCoreWidget
        )
        self.MCSLv2ValidateArgsCoreLineEdit.setObjectName(
            "MCSLv2ValidateArgsCoreLineEdit"
        )
        self.gridLayout_56.addWidget(self.MCSLv2ValidateArgsCoreLineEdit, 1, 1, 1, 1)
        self.MCSLv2ValidateArgsManuallyAddCorePrimaryPushBtn = PrimaryPushButton(
            self.MCSLv2ValidateArgsCoreWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv2ValidateArgsManuallyAddCorePrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv2ValidateArgsManuallyAddCorePrimaryPushBtn.setSizePolicy(sizePolicy)
        self.MCSLv2ValidateArgsManuallyAddCorePrimaryPushBtn.setMinimumSize(
            QSize(90, 0)
        )
        self.MCSLv2ValidateArgsManuallyAddCorePrimaryPushBtn.setObjectName(
            "MCSLv2ValidateArgsManuallyAddCorePrimaryPushBtn"
        )
        self.gridLayout_56.addWidget(
            self.MCSLv2ValidateArgsManuallyAddCorePrimaryPushBtn, 1, 2, 1, 1
        )
        self.gridLayout_51.addWidget(self.MCSLv2ValidateArgsCoreWidget, 7, 2, 1, 3)
        self.verticalLayout_8.addWidget(self.MCSLv2ValidateArgs)
        self.MCSLv2Save = CardWidget(self.MCSLv2ScrollAreaWidgetContents)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.MCSLv2Save.sizePolicy().hasHeightForWidth())
        self.MCSLv2Save.setSizePolicy(sizePolicy)
        self.MCSLv2Save.setMinimumSize(QSize(0, 125))
        self.MCSLv2Save.setMaximumSize(QSize(16777215, 125))
        self.MCSLv2Save.setObjectName("MCSLv2Save")
        self.gridLayout_57 = QGridLayout(self.MCSLv2Save)
        self.gridLayout_57.setObjectName("gridLayout_57")
        self.MCSLv2SaveTitle = SubtitleLabel(self.MCSLv2Save)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv2SaveTitle.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv2SaveTitle.setSizePolicy(sizePolicy)
        self.MCSLv2SaveTitle.setObjectName("MCSLv2SaveTitle")
        self.gridLayout_57.addWidget(self.MCSLv2SaveTitle, 0, 1, 1, 1)
        self.MCSLv2SaveServerNameLineEdit = LineEdit(self.MCSLv2Save)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv2SaveServerNameLineEdit.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv2SaveServerNameLineEdit.setSizePolicy(sizePolicy)
        self.MCSLv2SaveServerNameLineEdit.setMinimumSize(QSize(0, 30))
        self.MCSLv2SaveServerNameLineEdit.setObjectName("MCSLv2SaveServerNameLineEdit")
        self.gridLayout_57.addWidget(self.MCSLv2SaveServerNameLineEdit, 1, 1, 1, 1)
        spacerItem66 = QSpacerItem(20, 79, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout_57.addItem(spacerItem66, 0, 0, 3, 1)
        self.MCSLv2SaveServerPrimaryPushBtn = PrimaryPushButton(self.MCSLv2Save)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv2SaveServerPrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv2SaveServerPrimaryPushBtn.setSizePolicy(sizePolicy)
        self.MCSLv2SaveServerPrimaryPushBtn.setMinimumSize(QSize(130, 30))
        self.MCSLv2SaveServerPrimaryPushBtn.setMaximumSize(QSize(16777215, 30))
        self.MCSLv2SaveServerPrimaryPushBtn.setObjectName(
            "MCSLv2SaveServerPrimaryPushBtn"
        )
        self.gridLayout_57.addWidget(self.MCSLv2SaveServerPrimaryPushBtn, 2, 1, 1, 1)
        self.verticalLayout_8.addWidget(self.MCSLv2Save)
        self.MCSLv2ScrollArea.setWidget(self.MCSLv2ScrollAreaWidgetContents)
        self.gridLayout_58.addWidget(self.MCSLv2ScrollArea, 1, 3, 1, 2)
        spacerItem67 = QSpacerItem(415, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_58.addItem(spacerItem67, 0, 4, 1, 1)
        spacerItem68 = QSpacerItem(20, 335, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout_58.addItem(spacerItem68, 0, 1, 2, 1)
        self.importNewServerStackWidget.addWidget(self.MCSLv2)
        self.MSL3 = QWidget()
        self.MSL3.setObjectName("MSL3")
        self.gridLayout_67 = QGridLayout(self.MSL3)
        self.gridLayout_67.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_67.setObjectName("gridLayout_67")
        self.MSL3Title = SubtitleLabel(self.MSL3)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.MSL3Title.sizePolicy().hasHeightForWidth())
        self.MSL3Title.setSizePolicy(sizePolicy)
        self.MSL3Title.setObjectName("MSL3Title")
        self.gridLayout_67.addWidget(self.MSL3Title, 0, 3, 1, 1)
        spacerItem69 = QSpacerItem(415, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_67.addItem(spacerItem69, 0, 4, 1, 1)
        self.MSL3ScrollArea = SmoothScrollArea(self.MSL3)
        self.MSL3ScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.MSL3ScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.MSL3ScrollArea.setWidgetResizable(True)
        self.MSL3ScrollArea.setAlignment(Qt.AlignCenter)
        self.MSL3ScrollArea.setObjectName("MSL3ScrollArea")
        self.MSL3ScrollAreaWidgetContents = QWidget()
        self.MSL3ScrollAreaWidgetContents.setGeometry(QRect(0, 0, 452, 1191))
        self.MSL3ScrollAreaWidgetContents.setObjectName("MSL3ScrollAreaWidgetContents")
        self.verticalLayout_9 = QVBoxLayout(self.MSL3ScrollAreaWidgetContents)
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.MSL3Import = CardWidget(self.MSL3ScrollAreaWidgetContents)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.MSL3Import.sizePolicy().hasHeightForWidth())
        self.MSL3Import.setSizePolicy(sizePolicy)
        self.MSL3Import.setMinimumSize(QSize(0, 150))
        self.MSL3Import.setMaximumSize(QSize(16777215, 150))
        self.MSL3Import.setObjectName("MSL3Import")
        self.gridLayout_59 = QGridLayout(self.MSL3Import)
        self.gridLayout_59.setObjectName("gridLayout_59")
        spacerItem70 = QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout_59.addItem(spacerItem70, 0, 0, 3, 1)
        self.MSL3ImportTitle = SubtitleLabel(self.MSL3Import)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MSL3ImportTitle.sizePolicy().hasHeightForWidth()
        )
        self.MSL3ImportTitle.setSizePolicy(sizePolicy)
        self.MSL3ImportTitle.setObjectName("MSL3ImportTitle")
        self.gridLayout_59.addWidget(self.MSL3ImportTitle, 0, 2, 1, 1)
        self.MSL3ImportStatusText = BodyLabel(self.MSL3Import)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MSL3ImportStatusText.sizePolicy().hasHeightForWidth()
        )
        self.MSL3ImportStatusText.setSizePolicy(sizePolicy)
        self.MSL3ImportStatusText.setObjectName("MSL3ImportStatusText")
        self.gridLayout_59.addWidget(self.MSL3ImportStatusText, 1, 1, 1, 2)
        self.MSL3ImportStatus = PixmapLabel(self.MSL3Import)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MSL3ImportStatus.sizePolicy().hasHeightForWidth()
        )
        self.MSL3ImportStatus.setSizePolicy(sizePolicy)
        self.MSL3ImportStatus.setMinimumSize(QSize(30, 30))
        self.MSL3ImportStatus.setMaximumSize(QSize(30, 30))
        self.MSL3ImportStatus.setObjectName("MSL3ImportStatus")
        self.gridLayout_59.addWidget(self.MSL3ImportStatus, 0, 1, 1, 1)
        spacerItem71 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_59.addItem(spacerItem71, 2, 4, 1, 4)
        self.MSL3ImportArchives = PrimaryPushButton(self.MSL3Import)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MSL3ImportArchives.sizePolicy().hasHeightForWidth()
        )
        self.MSL3ImportArchives.setSizePolicy(sizePolicy)
        self.MSL3ImportArchives.setMinimumSize(QSize(110, 32))
        self.MSL3ImportArchives.setMaximumSize(QSize(150, 32))
        self.MSL3ImportArchives.setObjectName("MSL3ImportArchives")
        self.gridLayout_59.addWidget(self.MSL3ImportArchives, 2, 1, 1, 2)
        self.verticalLayout_9.addWidget(self.MSL3Import)
        self.MSL3SelectServer = CardWidget(self.MSL3ScrollAreaWidgetContents)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MSL3SelectServer.sizePolicy().hasHeightForWidth()
        )
        self.MSL3SelectServer.setSizePolicy(sizePolicy)
        self.MSL3SelectServer.setMinimumSize(QSize(0, 250))
        self.MSL3SelectServer.setObjectName("MSL3SelectServer")
        self.gridLayout_68 = QGridLayout(self.MSL3SelectServer)
        self.gridLayout_68.setObjectName("gridLayout_68")
        self.MSL3SelectServerStatus = PixmapLabel(self.MSL3SelectServer)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MSL3SelectServerStatus.sizePolicy().hasHeightForWidth()
        )
        self.MSL3SelectServerStatus.setSizePolicy(sizePolicy)
        self.MSL3SelectServerStatus.setMinimumSize(QSize(30, 30))
        self.MSL3SelectServerStatus.setMaximumSize(QSize(30, 30))
        self.MSL3SelectServerStatus.setObjectName("MSL3SelectServerStatus")
        self.gridLayout_68.addWidget(self.MSL3SelectServerStatus, 0, 1, 1, 1)
        spacerItem72 = QSpacerItem(20, 279, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout_68.addItem(spacerItem72, 0, 0, 3, 1)
        self.MSL3SelectServerStatusText = BodyLabel(self.MSL3SelectServer)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MSL3SelectServerStatusText.sizePolicy().hasHeightForWidth()
        )
        self.MSL3SelectServerStatusText.setSizePolicy(sizePolicy)
        self.MSL3SelectServerStatusText.setObjectName("MSL3SelectServerStatusText")
        self.gridLayout_68.addWidget(self.MSL3SelectServerStatusText, 1, 1, 1, 2)
        self.MSL3SelectServerTitle = SubtitleLabel(self.MSL3SelectServer)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MSL3SelectServerTitle.sizePolicy().hasHeightForWidth()
        )
        self.MSL3SelectServerTitle.setSizePolicy(sizePolicy)
        self.MSL3SelectServerTitle.setObjectName("MSL3SelectServerTitle")
        self.gridLayout_68.addWidget(self.MSL3SelectServerTitle, 0, 2, 1, 1)
        self.MSL3SelectServerTreeWidget = TreeWidget(self.MSL3SelectServer)
        self.MSL3SelectServerTreeWidget.setObjectName("MSL3SelectServerTreeWidget")
        self.MSL3SelectServerTreeWidget.headerItem().setText(0, "1")
        self.gridLayout_68.addWidget(self.MSL3SelectServerTreeWidget, 2, 1, 1, 2)
        self.verticalLayout_9.addWidget(self.MSL3SelectServer)
        self.MSL3ValidateArgs = CardWidget(self.MSL3ScrollAreaWidgetContents)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MSL3ValidateArgs.sizePolicy().hasHeightForWidth()
        )
        self.MSL3ValidateArgs.setSizePolicy(sizePolicy)
        self.MSL3ValidateArgs.setMinimumSize(QSize(0, 630))
        self.MSL3ValidateArgs.setMaximumSize(QSize(16777215, 630))
        self.MSL3ValidateArgs.setObjectName("MSL3ValidateArgs")
        self.gridLayout_60 = QGridLayout(self.MSL3ValidateArgs)
        self.gridLayout_60.setObjectName("gridLayout_60")
        self.MSL3ValidateArgsJavaWidget = QWidget(self.MSL3ValidateArgs)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MSL3ValidateArgsJavaWidget.sizePolicy().hasHeightForWidth()
        )
        self.MSL3ValidateArgsJavaWidget.setSizePolicy(sizePolicy)
        self.MSL3ValidateArgsJavaWidget.setMinimumSize(QSize(0, 120))
        self.MSL3ValidateArgsJavaWidget.setObjectName("MSL3ValidateArgsJavaWidget")
        self.gridLayout_61 = QGridLayout(self.MSL3ValidateArgsJavaWidget)
        self.gridLayout_61.setObjectName("gridLayout_61")
        self.MSL3ValidateArgsJavaListPushBtn = PushButton(
            self.MSL3ValidateArgsJavaWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MSL3ValidateArgsJavaListPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.MSL3ValidateArgsJavaListPushBtn.setSizePolicy(sizePolicy)
        self.MSL3ValidateArgsJavaListPushBtn.setMinimumSize(QSize(108, 31))
        self.MSL3ValidateArgsJavaListPushBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.MSL3ValidateArgsJavaListPushBtn.setObjectName(
            "MSL3ValidateArgsJavaListPushBtn"
        )
        self.gridLayout_61.addWidget(self.MSL3ValidateArgsJavaListPushBtn, 3, 2, 1, 1)
        self.MSL3ValidateArgsJavaTextEdit = TextEdit(self.MSL3ValidateArgsJavaWidget)
        self.MSL3ValidateArgsJavaTextEdit.setObjectName("MSL3ValidateArgsJavaTextEdit")
        self.gridLayout_61.addWidget(self.MSL3ValidateArgsJavaTextEdit, 2, 0, 2, 1)
        self.MSL3ValidateArgsAutoDetectJavaPrimaryPushBtn = PrimaryPushButton(
            self.MSL3ValidateArgsJavaWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MSL3ValidateArgsAutoDetectJavaPrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.MSL3ValidateArgsAutoDetectJavaPrimaryPushBtn.setSizePolicy(sizePolicy)
        self.MSL3ValidateArgsAutoDetectJavaPrimaryPushBtn.setCursor(
            QCursor(Qt.PointingHandCursor)
        )
        self.MSL3ValidateArgsAutoDetectJavaPrimaryPushBtn.setObjectName(
            "MSL3ValidateArgsAutoDetectJavaPrimaryPushBtn"
        )
        self.gridLayout_61.addWidget(
            self.MSL3ValidateArgsAutoDetectJavaPrimaryPushBtn, 2, 2, 1, 1
        )
        self.MSL3ValidateArgsManuallyAddJavaPrimaryPushBtn = PrimaryPushButton(
            self.MSL3ValidateArgsJavaWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MSL3ValidateArgsManuallyAddJavaPrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.MSL3ValidateArgsManuallyAddJavaPrimaryPushBtn.setSizePolicy(sizePolicy)
        self.MSL3ValidateArgsManuallyAddJavaPrimaryPushBtn.setMinimumSize(QSize(90, 0))
        self.MSL3ValidateArgsManuallyAddJavaPrimaryPushBtn.setCursor(
            QCursor(Qt.PointingHandCursor)
        )
        self.MSL3ValidateArgsManuallyAddJavaPrimaryPushBtn.setObjectName(
            "MSL3ValidateArgsManuallyAddJavaPrimaryPushBtn"
        )
        self.gridLayout_61.addWidget(
            self.MSL3ValidateArgsManuallyAddJavaPrimaryPushBtn, 2, 1, 1, 1
        )
        self.MSL3ValidateArgsDownloadJavaPrimaryPushBtn = PrimaryPushButton(
            self.MSL3ValidateArgsJavaWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MSL3ValidateArgsDownloadJavaPrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.MSL3ValidateArgsDownloadJavaPrimaryPushBtn.setSizePolicy(sizePolicy)
        self.MSL3ValidateArgsDownloadJavaPrimaryPushBtn.setMinimumSize(QSize(90, 0))
        self.MSL3ValidateArgsDownloadJavaPrimaryPushBtn.setCursor(
            QCursor(Qt.PointingHandCursor)
        )
        self.MSL3ValidateArgsDownloadJavaPrimaryPushBtn.setObjectName(
            "MSL3ValidateArgsDownloadJavaPrimaryPushBtn"
        )
        self.gridLayout_61.addWidget(
            self.MSL3ValidateArgsDownloadJavaPrimaryPushBtn, 3, 1, 1, 1
        )
        self.MSL3ValidateArgsJavaSubtitleLabel = SubtitleLabel(
            self.MSL3ValidateArgsJavaWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MSL3ValidateArgsJavaSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.MSL3ValidateArgsJavaSubtitleLabel.setSizePolicy(sizePolicy)
        self.MSL3ValidateArgsJavaSubtitleLabel.setObjectName(
            "MSL3ValidateArgsJavaSubtitleLabel"
        )
        self.gridLayout_61.addWidget(self.MSL3ValidateArgsJavaSubtitleLabel, 0, 0, 1, 1)
        self.gridLayout_60.addWidget(self.MSL3ValidateArgsJavaWidget, 5, 2, 1, 3)
        self.MSL3ValidateArgsDeEncodingWidget = QWidget(self.MSL3ValidateArgs)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MSL3ValidateArgsDeEncodingWidget.sizePolicy().hasHeightForWidth()
        )
        self.MSL3ValidateArgsDeEncodingWidget.setSizePolicy(sizePolicy)
        self.MSL3ValidateArgsDeEncodingWidget.setMinimumSize(QSize(0, 122))
        self.MSL3ValidateArgsDeEncodingWidget.setMaximumSize(QSize(16777215, 122))
        self.MSL3ValidateArgsDeEncodingWidget.setObjectName(
            "MSL3ValidateArgsDeEncodingWidget"
        )
        self.gridLayout_62 = QGridLayout(self.MSL3ValidateArgsDeEncodingWidget)
        self.gridLayout_62.setObjectName("gridLayout_62")
        self.MSL3ValidateArgsOutputDeEncodingComboBox = ComboBox(
            self.MSL3ValidateArgsDeEncodingWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MSL3ValidateArgsOutputDeEncodingComboBox.sizePolicy().hasHeightForWidth()
        )
        self.MSL3ValidateArgsOutputDeEncodingComboBox.setSizePolicy(sizePolicy)
        self.MSL3ValidateArgsOutputDeEncodingComboBox.setObjectName(
            "MSL3ValidateArgsOutputDeEncodingComboBox"
        )
        self.gridLayout_62.addWidget(
            self.MSL3ValidateArgsOutputDeEncodingComboBox, 2, 1, 1, 1
        )
        self.MSL3ValidateArgsInputDeEncodingComboBox = ComboBox(
            self.MSL3ValidateArgsDeEncodingWidget
        )
        self.MSL3ValidateArgsInputDeEncodingComboBox.setText("")
        self.MSL3ValidateArgsInputDeEncodingComboBox.setObjectName(
            "MSL3ValidateArgsInputDeEncodingComboBox"
        )
        self.gridLayout_62.addWidget(
            self.MSL3ValidateArgsInputDeEncodingComboBox, 3, 1, 1, 1
        )
        self.MSL3ValidateArgsOutputDeEncodingLabel = StrongBodyLabel(
            self.MSL3ValidateArgsDeEncodingWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MSL3ValidateArgsOutputDeEncodingLabel.sizePolicy().hasHeightForWidth()
        )
        self.MSL3ValidateArgsOutputDeEncodingLabel.setSizePolicy(sizePolicy)
        self.MSL3ValidateArgsOutputDeEncodingLabel.setObjectName(
            "MSL3ValidateArgsOutputDeEncodingLabel"
        )
        self.gridLayout_62.addWidget(
            self.MSL3ValidateArgsOutputDeEncodingLabel, 2, 0, 1, 1
        )
        self.MSL3ValidateArgsDeEncodingSubtitleLabel = SubtitleLabel(
            self.MSL3ValidateArgsDeEncodingWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MSL3ValidateArgsDeEncodingSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.MSL3ValidateArgsDeEncodingSubtitleLabel.setSizePolicy(sizePolicy)
        self.MSL3ValidateArgsDeEncodingSubtitleLabel.setObjectName(
            "MSL3ValidateArgsDeEncodingSubtitleLabel"
        )
        self.gridLayout_62.addWidget(
            self.MSL3ValidateArgsDeEncodingSubtitleLabel, 0, 0, 1, 1
        )
        self.MSL3ValidateArgsInputDeEncodingLabel = StrongBodyLabel(
            self.MSL3ValidateArgsDeEncodingWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MSL3ValidateArgsInputDeEncodingLabel.sizePolicy().hasHeightForWidth()
        )
        self.MSL3ValidateArgsInputDeEncodingLabel.setSizePolicy(sizePolicy)
        self.MSL3ValidateArgsInputDeEncodingLabel.setObjectName(
            "MSL3ValidateArgsInputDeEncodingLabel"
        )
        self.gridLayout_62.addWidget(
            self.MSL3ValidateArgsInputDeEncodingLabel, 3, 0, 1, 1
        )
        self.gridLayout_60.addWidget(self.MSL3ValidateArgsDeEncodingWidget, 8, 2, 1, 3)
        spacerItem73 = QSpacerItem(20, 102, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout_60.addItem(spacerItem73, 0, 0, 21, 1)
        self.MSL3ValidateArgsJVMArgWidget = QWidget(self.MSL3ValidateArgs)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MSL3ValidateArgsJVMArgWidget.sizePolicy().hasHeightForWidth()
        )
        self.MSL3ValidateArgsJVMArgWidget.setSizePolicy(sizePolicy)
        self.MSL3ValidateArgsJVMArgWidget.setMinimumSize(QSize(0, 140))
        self.MSL3ValidateArgsJVMArgWidget.setMaximumSize(QSize(16777215, 140))
        self.MSL3ValidateArgsJVMArgWidget.setObjectName("MSL3ValidateArgsJVMArgWidget")
        self.gridLayout_63 = QGridLayout(self.MSL3ValidateArgsJVMArgWidget)
        self.gridLayout_63.setObjectName("gridLayout_63")
        self.MSL3ValidateArgsJVMArgPlainTextEdit = PlainTextEdit(
            self.MSL3ValidateArgsJVMArgWidget
        )
        self.MSL3ValidateArgsJVMArgPlainTextEdit.setObjectName(
            "MSL3ValidateArgsJVMArgPlainTextEdit"
        )
        self.gridLayout_63.addWidget(
            self.MSL3ValidateArgsJVMArgPlainTextEdit, 1, 0, 1, 1
        )
        self.MSL3ValidateArgsJVMArgSubtitleLabel = SubtitleLabel(
            self.MSL3ValidateArgsJVMArgWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MSL3ValidateArgsJVMArgSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.MSL3ValidateArgsJVMArgSubtitleLabel.setSizePolicy(sizePolicy)
        self.MSL3ValidateArgsJVMArgSubtitleLabel.setObjectName(
            "MSL3ValidateArgsJVMArgSubtitleLabel"
        )
        self.gridLayout_63.addWidget(
            self.MSL3ValidateArgsJVMArgSubtitleLabel, 0, 0, 1, 1
        )
        self.gridLayout_60.addWidget(self.MSL3ValidateArgsJVMArgWidget, 9, 2, 1, 3)
        self.MSL3ValidateArgsCoreWidget = QWidget(self.MSL3ValidateArgs)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MSL3ValidateArgsCoreWidget.sizePolicy().hasHeightForWidth()
        )
        self.MSL3ValidateArgsCoreWidget.setSizePolicy(sizePolicy)
        self.MSL3ValidateArgsCoreWidget.setObjectName("MSL3ValidateArgsCoreWidget")
        self.gridLayout_65 = QGridLayout(self.MSL3ValidateArgsCoreWidget)
        self.gridLayout_65.setObjectName("gridLayout_65")
        self.MSL3ValidateArgsDownloadCorePrimaryPushBtn = PrimaryPushButton(
            self.MSL3ValidateArgsCoreWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MSL3ValidateArgsDownloadCorePrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.MSL3ValidateArgsDownloadCorePrimaryPushBtn.setSizePolicy(sizePolicy)
        self.MSL3ValidateArgsDownloadCorePrimaryPushBtn.setMinimumSize(QSize(90, 0))
        self.MSL3ValidateArgsDownloadCorePrimaryPushBtn.setObjectName(
            "MSL3ValidateArgsDownloadCorePrimaryPushBtn"
        )
        self.gridLayout_65.addWidget(
            self.MSL3ValidateArgsDownloadCorePrimaryPushBtn, 1, 3, 1, 1
        )
        self.MSL3ValidateArgsCoreSubtitleLabel = SubtitleLabel(
            self.MSL3ValidateArgsCoreWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MSL3ValidateArgsCoreSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.MSL3ValidateArgsCoreSubtitleLabel.setSizePolicy(sizePolicy)
        self.MSL3ValidateArgsCoreSubtitleLabel.setObjectName(
            "MSL3ValidateArgsCoreSubtitleLabel"
        )
        self.gridLayout_65.addWidget(self.MSL3ValidateArgsCoreSubtitleLabel, 0, 1, 1, 1)
        self.MSL3ValidateArgsCoreLineEdit = LineEdit(self.MSL3ValidateArgsCoreWidget)
        self.MSL3ValidateArgsCoreLineEdit.setObjectName("MSL3ValidateArgsCoreLineEdit")
        self.gridLayout_65.addWidget(self.MSL3ValidateArgsCoreLineEdit, 1, 1, 1, 1)
        self.MSL3ValidateArgsManuallyAddCorePrimaryPushBtn = PrimaryPushButton(
            self.MSL3ValidateArgsCoreWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MSL3ValidateArgsManuallyAddCorePrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.MSL3ValidateArgsManuallyAddCorePrimaryPushBtn.setSizePolicy(sizePolicy)
        self.MSL3ValidateArgsManuallyAddCorePrimaryPushBtn.setMinimumSize(QSize(90, 0))
        self.MSL3ValidateArgsManuallyAddCorePrimaryPushBtn.setObjectName(
            "MSL3ValidateArgsManuallyAddCorePrimaryPushBtn"
        )
        self.gridLayout_65.addWidget(
            self.MSL3ValidateArgsManuallyAddCorePrimaryPushBtn, 1, 2, 1, 1
        )
        self.gridLayout_60.addWidget(self.MSL3ValidateArgsCoreWidget, 7, 2, 1, 3)
        self.MSL3ValidateArgsMemWidget = QWidget(self.MSL3ValidateArgs)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MSL3ValidateArgsMemWidget.sizePolicy().hasHeightForWidth()
        )
        self.MSL3ValidateArgsMemWidget.setSizePolicy(sizePolicy)
        self.MSL3ValidateArgsMemWidget.setMinimumSize(QSize(0, 85))
        self.MSL3ValidateArgsMemWidget.setMaximumSize(QSize(16777215, 85))
        self.MSL3ValidateArgsMemWidget.setObjectName("MSL3ValidateArgsMemWidget")
        self.gridLayout_64 = QGridLayout(self.MSL3ValidateArgsMemWidget)
        self.gridLayout_64.setObjectName("gridLayout_64")
        self.MSL3ValidateArgsMinMemLineEdit = LineEdit(self.MSL3ValidateArgsMemWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MSL3ValidateArgsMinMemLineEdit.sizePolicy().hasHeightForWidth()
        )
        self.MSL3ValidateArgsMinMemLineEdit.setSizePolicy(sizePolicy)
        self.MSL3ValidateArgsMinMemLineEdit.setMinimumSize(QSize(0, 30))
        self.MSL3ValidateArgsMinMemLineEdit.setObjectName(
            "MSL3ValidateArgsMinMemLineEdit"
        )
        self.gridLayout_64.addWidget(self.MSL3ValidateArgsMinMemLineEdit, 1, 1, 1, 1)
        self.MSL3ValidateArgsMemSubtitleLabel = SubtitleLabel(
            self.MSL3ValidateArgsMemWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MSL3ValidateArgsMemSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.MSL3ValidateArgsMemSubtitleLabel.setSizePolicy(sizePolicy)
        self.MSL3ValidateArgsMemSubtitleLabel.setObjectName(
            "MSL3ValidateArgsMemSubtitleLabel"
        )
        self.gridLayout_64.addWidget(self.MSL3ValidateArgsMemSubtitleLabel, 0, 1, 1, 1)
        self.MSL3ValidateArgsMaxMemLineEdit = LineEdit(self.MSL3ValidateArgsMemWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MSL3ValidateArgsMaxMemLineEdit.sizePolicy().hasHeightForWidth()
        )
        self.MSL3ValidateArgsMaxMemLineEdit.setSizePolicy(sizePolicy)
        self.MSL3ValidateArgsMaxMemLineEdit.setMinimumSize(QSize(0, 30))
        self.MSL3ValidateArgsMaxMemLineEdit.setObjectName(
            "MSL3ValidateArgsMaxMemLineEdit"
        )
        self.gridLayout_64.addWidget(self.MSL3ValidateArgsMaxMemLineEdit, 1, 3, 1, 1)
        self.MSL3ValidateArgsToSymbol = SubtitleLabel(self.MSL3ValidateArgsMemWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MSL3ValidateArgsToSymbol.sizePolicy().hasHeightForWidth()
        )
        self.MSL3ValidateArgsToSymbol.setSizePolicy(sizePolicy)
        self.MSL3ValidateArgsToSymbol.setObjectName("MSL3ValidateArgsToSymbol")
        self.gridLayout_64.addWidget(self.MSL3ValidateArgsToSymbol, 1, 2, 1, 1)
        spacerItem74 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_64.addItem(spacerItem74, 1, 5, 1, 1)
        self.MSL3ValidateArgsMemUnitComboBox = ComboBox(self.MSL3ValidateArgsMemWidget)
        self.MSL3ValidateArgsMemUnitComboBox.setObjectName(
            "MSL3ValidateArgsMemUnitComboBox"
        )
        self.gridLayout_64.addWidget(self.MSL3ValidateArgsMemUnitComboBox, 1, 4, 1, 1)
        self.gridLayout_60.addWidget(self.MSL3ValidateArgsMemWidget, 6, 2, 1, 3)
        self.MSL3ValidateArgsTitle = SubtitleLabel(self.MSL3ValidateArgs)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MSL3ValidateArgsTitle.sizePolicy().hasHeightForWidth()
        )
        self.MSL3ValidateArgsTitle.setSizePolicy(sizePolicy)
        self.MSL3ValidateArgsTitle.setObjectName("MSL3ValidateArgsTitle")
        self.gridLayout_60.addWidget(self.MSL3ValidateArgsTitle, 0, 3, 1, 1)
        self.MSL3ValidateArgsStatus = PixmapLabel(self.MSL3ValidateArgs)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MSL3ValidateArgsStatus.sizePolicy().hasHeightForWidth()
        )
        self.MSL3ValidateArgsStatus.setSizePolicy(sizePolicy)
        self.MSL3ValidateArgsStatus.setMinimumSize(QSize(30, 30))
        self.MSL3ValidateArgsStatus.setMaximumSize(QSize(30, 30))
        self.MSL3ValidateArgsStatus.setObjectName("MSL3ValidateArgsStatus")
        self.gridLayout_60.addWidget(self.MSL3ValidateArgsStatus, 0, 2, 1, 1)
        self.verticalLayout_9.addWidget(self.MSL3ValidateArgs)
        self.MSL3Save = CardWidget(self.MSL3ScrollAreaWidgetContents)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.MSL3Save.sizePolicy().hasHeightForWidth())
        self.MSL3Save.setSizePolicy(sizePolicy)
        self.MSL3Save.setMinimumSize(QSize(0, 125))
        self.MSL3Save.setMaximumSize(QSize(16777215, 125))
        self.MSL3Save.setObjectName("MSL3Save")
        self.gridLayout_66 = QGridLayout(self.MSL3Save)
        self.gridLayout_66.setObjectName("gridLayout_66")
        self.MSL3SaveTitle = SubtitleLabel(self.MSL3Save)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MSL3SaveTitle.sizePolicy().hasHeightForWidth()
        )
        self.MSL3SaveTitle.setSizePolicy(sizePolicy)
        self.MSL3SaveTitle.setObjectName("MSL3SaveTitle")
        self.gridLayout_66.addWidget(self.MSL3SaveTitle, 0, 1, 1, 1)
        self.MSL3SaveServerNameLineEdit = LineEdit(self.MSL3Save)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MSL3SaveServerNameLineEdit.sizePolicy().hasHeightForWidth()
        )
        self.MSL3SaveServerNameLineEdit.setSizePolicy(sizePolicy)
        self.MSL3SaveServerNameLineEdit.setMinimumSize(QSize(0, 30))
        self.MSL3SaveServerNameLineEdit.setObjectName("MSL3SaveServerNameLineEdit")
        self.gridLayout_66.addWidget(self.MSL3SaveServerNameLineEdit, 1, 1, 1, 1)
        spacerItem75 = QSpacerItem(20, 79, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout_66.addItem(spacerItem75, 0, 0, 3, 1)
        self.MSL3SaveServerPrimaryPushBtn = PrimaryPushButton(self.MSL3Save)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MSL3SaveServerPrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.MSL3SaveServerPrimaryPushBtn.setSizePolicy(sizePolicy)
        self.MSL3SaveServerPrimaryPushBtn.setMinimumSize(QSize(130, 30))
        self.MSL3SaveServerPrimaryPushBtn.setMaximumSize(QSize(16777215, 30))
        self.MSL3SaveServerPrimaryPushBtn.setObjectName("MSL3SaveServerPrimaryPushBtn")
        self.gridLayout_66.addWidget(self.MSL3SaveServerPrimaryPushBtn, 2, 1, 1, 1)
        self.verticalLayout_9.addWidget(self.MSL3Save)
        self.MSL3ScrollArea.setWidget(self.MSL3ScrollAreaWidgetContents)
        self.gridLayout_67.addWidget(self.MSL3ScrollArea, 1, 3, 1, 2)
        self.MSL3BackToMain = TransparentToolButton(FIF.PAGE_LEFT, self.MSL3)
        self.MSL3BackToMain.setObjectName("MSL3BackToMain")
        self.gridLayout_67.addWidget(self.MSL3BackToMain, 0, 2, 1, 1)
        spacerItem76 = QSpacerItem(20, 346, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.gridLayout_67.addItem(spacerItem76, 1, 2, 1, 1)
        spacerItem77 = QSpacerItem(20, 335, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout_67.addItem(spacerItem77, 0, 1, 2, 1)
        self.importNewServerStackWidget.addWidget(self.MSL3)
        self.NullCraft = QWidget()
        self.NullCraft.setObjectName("NullCraft")
        self.gridLayout_78 = QGridLayout(self.NullCraft)
        self.gridLayout_78.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_78.setObjectName("gridLayout_78")
        self.NullCraftScrollArea = SmoothScrollArea(self.NullCraft)
        self.NullCraftScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.NullCraftScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.NullCraftScrollArea.setWidgetResizable(True)
        self.NullCraftScrollArea.setAlignment(Qt.AlignCenter)
        self.NullCraftScrollArea.setObjectName("NullCraftScrollArea")
        self.NullCraftScrollAreaWidgetContents = QWidget()
        self.NullCraftScrollAreaWidgetContents.setGeometry(QRect(0, 0, 450, 935))
        self.NullCraftScrollAreaWidgetContents.setObjectName(
            "NullCraftScrollAreaWidgetContents"
        )
        self.verticalLayout_10 = QVBoxLayout(self.NullCraftScrollAreaWidgetContents)
        self.verticalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.NullCraftImport = CardWidget(self.NullCraftScrollAreaWidgetContents)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.NullCraftImport.sizePolicy().hasHeightForWidth()
        )
        self.NullCraftImport.setSizePolicy(sizePolicy)
        self.NullCraftImport.setMinimumSize(QSize(0, 150))
        self.NullCraftImport.setMaximumSize(QSize(16777215, 150))
        self.NullCraftImport.setObjectName("NullCraftImport")
        self.gridLayout_69 = QGridLayout(self.NullCraftImport)
        self.gridLayout_69.setObjectName("gridLayout_69")
        spacerItem78 = QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout_69.addItem(spacerItem78, 0, 0, 3, 1)
        self.NullCraftImportTitle = SubtitleLabel(self.NullCraftImport)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.NullCraftImportTitle.sizePolicy().hasHeightForWidth()
        )
        self.NullCraftImportTitle.setSizePolicy(sizePolicy)
        self.NullCraftImportTitle.setObjectName("NullCraftImportTitle")
        self.gridLayout_69.addWidget(self.NullCraftImportTitle, 0, 2, 1, 1)
        self.NullCraftImportStatusText = BodyLabel(self.NullCraftImport)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.NullCraftImportStatusText.sizePolicy().hasHeightForWidth()
        )
        self.NullCraftImportStatusText.setSizePolicy(sizePolicy)
        self.NullCraftImportStatusText.setObjectName("NullCraftImportStatusText")
        self.gridLayout_69.addWidget(self.NullCraftImportStatusText, 1, 1, 1, 2)
        self.NullCraftImportStatus = PixmapLabel(self.NullCraftImport)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.NullCraftImportStatus.sizePolicy().hasHeightForWidth()
        )
        self.NullCraftImportStatus.setSizePolicy(sizePolicy)
        self.NullCraftImportStatus.setMinimumSize(QSize(30, 30))
        self.NullCraftImportStatus.setMaximumSize(QSize(30, 30))
        self.NullCraftImportStatus.setObjectName("NullCraftImportStatus")
        self.gridLayout_69.addWidget(self.NullCraftImportStatus, 0, 1, 1, 1)
        spacerItem79 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_69.addItem(spacerItem79, 2, 4, 1, 4)
        self.NullCraftImportArchives = PrimaryPushButton(self.NullCraftImport)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.NullCraftImportArchives.sizePolicy().hasHeightForWidth()
        )
        self.NullCraftImportArchives.setSizePolicy(sizePolicy)
        self.NullCraftImportArchives.setMinimumSize(QSize(110, 32))
        self.NullCraftImportArchives.setMaximumSize(QSize(150, 32))
        self.NullCraftImportArchives.setObjectName("NullCraftImportArchives")
        self.gridLayout_69.addWidget(self.NullCraftImportArchives, 2, 1, 1, 2)
        self.verticalLayout_10.addWidget(self.NullCraftImport)
        self.NullCraftValidateArgs = CardWidget(self.NullCraftScrollAreaWidgetContents)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.NullCraftValidateArgs.sizePolicy().hasHeightForWidth()
        )
        self.NullCraftValidateArgs.setSizePolicy(sizePolicy)
        self.NullCraftValidateArgs.setMinimumSize(QSize(0, 630))
        self.NullCraftValidateArgs.setMaximumSize(QSize(16777215, 630))
        self.NullCraftValidateArgs.setObjectName("NullCraftValidateArgs")
        self.gridLayout_71 = QGridLayout(self.NullCraftValidateArgs)
        self.gridLayout_71.setObjectName("gridLayout_71")
        self.NullCraftValidateArgsJavaWidget = QWidget(self.NullCraftValidateArgs)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.NullCraftValidateArgsJavaWidget.sizePolicy().hasHeightForWidth()
        )
        self.NullCraftValidateArgsJavaWidget.setSizePolicy(sizePolicy)
        self.NullCraftValidateArgsJavaWidget.setMinimumSize(QSize(0, 120))
        self.NullCraftValidateArgsJavaWidget.setObjectName(
            "NullCraftValidateArgsJavaWidget"
        )
        self.gridLayout_72 = QGridLayout(self.NullCraftValidateArgsJavaWidget)
        self.gridLayout_72.setObjectName("gridLayout_72")
        self.NullCraftValidateArgsJavaListPushBtn = PushButton(
            self.NullCraftValidateArgsJavaWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.NullCraftValidateArgsJavaListPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.NullCraftValidateArgsJavaListPushBtn.setSizePolicy(sizePolicy)
        self.NullCraftValidateArgsJavaListPushBtn.setMinimumSize(QSize(108, 31))
        self.NullCraftValidateArgsJavaListPushBtn.setCursor(
            QCursor(Qt.PointingHandCursor)
        )
        self.NullCraftValidateArgsJavaListPushBtn.setObjectName(
            "NullCraftValidateArgsJavaListPushBtn"
        )
        self.gridLayout_72.addWidget(
            self.NullCraftValidateArgsJavaListPushBtn, 3, 2, 1, 1
        )
        self.NullCraftValidateArgsJavaTextEdit = TextEdit(
            self.NullCraftValidateArgsJavaWidget
        )
        self.NullCraftValidateArgsJavaTextEdit.setObjectName(
            "NullCraftValidateArgsJavaTextEdit"
        )
        self.gridLayout_72.addWidget(self.NullCraftValidateArgsJavaTextEdit, 2, 0, 2, 1)
        self.NullCraftValidateArgsAutoDetectJavaPrimaryPushBtn = PrimaryPushButton(
            self.NullCraftValidateArgsJavaWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.NullCraftValidateArgsAutoDetectJavaPrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.NullCraftValidateArgsAutoDetectJavaPrimaryPushBtn.setSizePolicy(sizePolicy)
        self.NullCraftValidateArgsAutoDetectJavaPrimaryPushBtn.setCursor(
            QCursor(Qt.PointingHandCursor)
        )
        self.NullCraftValidateArgsAutoDetectJavaPrimaryPushBtn.setObjectName(
            "NullCraftValidateArgsAutoDetectJavaPrimaryPushBtn"
        )
        self.gridLayout_72.addWidget(
            self.NullCraftValidateArgsAutoDetectJavaPrimaryPushBtn, 2, 2, 1, 1
        )
        self.NullCraftValidateArgsManuallyAddJavaPrimaryPushBtn = PrimaryPushButton(
            self.NullCraftValidateArgsJavaWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.NullCraftValidateArgsManuallyAddJavaPrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.NullCraftValidateArgsManuallyAddJavaPrimaryPushBtn.setSizePolicy(
            sizePolicy
        )
        self.NullCraftValidateArgsManuallyAddJavaPrimaryPushBtn.setMinimumSize(
            QSize(90, 0)
        )
        self.NullCraftValidateArgsManuallyAddJavaPrimaryPushBtn.setCursor(
            QCursor(Qt.PointingHandCursor)
        )
        self.NullCraftValidateArgsManuallyAddJavaPrimaryPushBtn.setObjectName(
            "NullCraftValidateArgsManuallyAddJavaPrimaryPushBtn"
        )
        self.gridLayout_72.addWidget(
            self.NullCraftValidateArgsManuallyAddJavaPrimaryPushBtn, 2, 1, 1, 1
        )
        self.NullCraftValidateArgsDownloadJavaPrimaryPushBtn = PrimaryPushButton(
            self.NullCraftValidateArgsJavaWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.NullCraftValidateArgsDownloadJavaPrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.NullCraftValidateArgsDownloadJavaPrimaryPushBtn.setSizePolicy(sizePolicy)
        self.NullCraftValidateArgsDownloadJavaPrimaryPushBtn.setMinimumSize(
            QSize(90, 0)
        )
        self.NullCraftValidateArgsDownloadJavaPrimaryPushBtn.setCursor(
            QCursor(Qt.PointingHandCursor)
        )
        self.NullCraftValidateArgsDownloadJavaPrimaryPushBtn.setObjectName(
            "NullCraftValidateArgsDownloadJavaPrimaryPushBtn"
        )
        self.gridLayout_72.addWidget(
            self.NullCraftValidateArgsDownloadJavaPrimaryPushBtn, 3, 1, 1, 1
        )
        self.NullCraftValidateArgsJavaSubtitleLabel = SubtitleLabel(
            self.NullCraftValidateArgsJavaWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.NullCraftValidateArgsJavaSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.NullCraftValidateArgsJavaSubtitleLabel.setSizePolicy(sizePolicy)
        self.NullCraftValidateArgsJavaSubtitleLabel.setObjectName(
            "NullCraftValidateArgsJavaSubtitleLabel"
        )
        self.gridLayout_72.addWidget(
            self.NullCraftValidateArgsJavaSubtitleLabel, 0, 0, 1, 1
        )
        self.gridLayout_71.addWidget(self.NullCraftValidateArgsJavaWidget, 5, 2, 1, 3)
        self.NullCraftValidateArgsDeEncodingWidget = QWidget(self.NullCraftValidateArgs)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.NullCraftValidateArgsDeEncodingWidget.sizePolicy().hasHeightForWidth()
        )
        self.NullCraftValidateArgsDeEncodingWidget.setSizePolicy(sizePolicy)
        self.NullCraftValidateArgsDeEncodingWidget.setMinimumSize(QSize(0, 122))
        self.NullCraftValidateArgsDeEncodingWidget.setMaximumSize(QSize(16777215, 122))
        self.NullCraftValidateArgsDeEncodingWidget.setObjectName(
            "NullCraftValidateArgsDeEncodingWidget"
        )
        self.gridLayout_73 = QGridLayout(self.NullCraftValidateArgsDeEncodingWidget)
        self.gridLayout_73.setObjectName("gridLayout_73")
        self.NullCraftValidateArgsOutputDeEncodingComboBox = ComboBox(
            self.NullCraftValidateArgsDeEncodingWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.NullCraftValidateArgsOutputDeEncodingComboBox.sizePolicy().hasHeightForWidth()
        )
        self.NullCraftValidateArgsOutputDeEncodingComboBox.setSizePolicy(sizePolicy)
        self.NullCraftValidateArgsOutputDeEncodingComboBox.setObjectName(
            "NullCraftValidateArgsOutputDeEncodingComboBox"
        )
        self.gridLayout_73.addWidget(
            self.NullCraftValidateArgsOutputDeEncodingComboBox, 2, 1, 1, 1
        )
        self.NullCraftValidateArgsInputDeEncodingComboBox = ComboBox(
            self.NullCraftValidateArgsDeEncodingWidget
        )
        self.NullCraftValidateArgsInputDeEncodingComboBox.setText("")
        self.NullCraftValidateArgsInputDeEncodingComboBox.setObjectName(
            "NullCraftValidateArgsInputDeEncodingComboBox"
        )
        self.gridLayout_73.addWidget(
            self.NullCraftValidateArgsInputDeEncodingComboBox, 3, 1, 1, 1
        )
        self.NullCraftValidateArgsOutputDeEncodingLabel = StrongBodyLabel(
            self.NullCraftValidateArgsDeEncodingWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.NullCraftValidateArgsOutputDeEncodingLabel.sizePolicy().hasHeightForWidth()
        )
        self.NullCraftValidateArgsOutputDeEncodingLabel.setSizePolicy(sizePolicy)
        self.NullCraftValidateArgsOutputDeEncodingLabel.setObjectName(
            "NullCraftValidateArgsOutputDeEncodingLabel"
        )
        self.gridLayout_73.addWidget(
            self.NullCraftValidateArgsOutputDeEncodingLabel, 2, 0, 1, 1
        )
        self.NullCraftValidateArgsDeEncodingSubtitleLabel = SubtitleLabel(
            self.NullCraftValidateArgsDeEncodingWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.NullCraftValidateArgsDeEncodingSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.NullCraftValidateArgsDeEncodingSubtitleLabel.setSizePolicy(sizePolicy)
        self.NullCraftValidateArgsDeEncodingSubtitleLabel.setObjectName(
            "NullCraftValidateArgsDeEncodingSubtitleLabel"
        )
        self.gridLayout_73.addWidget(
            self.NullCraftValidateArgsDeEncodingSubtitleLabel, 0, 0, 1, 1
        )
        self.NullCraftValidateArgsInputDeEncodingLabel = StrongBodyLabel(
            self.NullCraftValidateArgsDeEncodingWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.NullCraftValidateArgsInputDeEncodingLabel.sizePolicy().hasHeightForWidth()
        )
        self.NullCraftValidateArgsInputDeEncodingLabel.setSizePolicy(sizePolicy)
        self.NullCraftValidateArgsInputDeEncodingLabel.setObjectName(
            "NullCraftValidateArgsInputDeEncodingLabel"
        )
        self.gridLayout_73.addWidget(
            self.NullCraftValidateArgsInputDeEncodingLabel, 3, 0, 1, 1
        )
        self.gridLayout_71.addWidget(
            self.NullCraftValidateArgsDeEncodingWidget, 8, 2, 1, 3
        )
        spacerItem80 = QSpacerItem(20, 102, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout_71.addItem(spacerItem80, 0, 0, 21, 1)
        self.NullCraftValidateArgsJVMArgWidget = QWidget(self.NullCraftValidateArgs)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.NullCraftValidateArgsJVMArgWidget.sizePolicy().hasHeightForWidth()
        )
        self.NullCraftValidateArgsJVMArgWidget.setSizePolicy(sizePolicy)
        self.NullCraftValidateArgsJVMArgWidget.setMinimumSize(QSize(0, 140))
        self.NullCraftValidateArgsJVMArgWidget.setMaximumSize(QSize(16777215, 140))
        self.NullCraftValidateArgsJVMArgWidget.setObjectName(
            "NullCraftValidateArgsJVMArgWidget"
        )
        self.gridLayout_74 = QGridLayout(self.NullCraftValidateArgsJVMArgWidget)
        self.gridLayout_74.setObjectName("gridLayout_74")
        self.NullCraftValidateArgsJVMArgPlainTextEdit = PlainTextEdit(
            self.NullCraftValidateArgsJVMArgWidget
        )
        self.NullCraftValidateArgsJVMArgPlainTextEdit.setObjectName(
            "NullCraftValidateArgsJVMArgPlainTextEdit"
        )
        self.gridLayout_74.addWidget(
            self.NullCraftValidateArgsJVMArgPlainTextEdit, 1, 0, 1, 1
        )
        self.NullCraftValidateArgsJVMArgSubtitleLabel = SubtitleLabel(
            self.NullCraftValidateArgsJVMArgWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.NullCraftValidateArgsJVMArgSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.NullCraftValidateArgsJVMArgSubtitleLabel.setSizePolicy(sizePolicy)
        self.NullCraftValidateArgsJVMArgSubtitleLabel.setObjectName(
            "NullCraftValidateArgsJVMArgSubtitleLabel"
        )
        self.gridLayout_74.addWidget(
            self.NullCraftValidateArgsJVMArgSubtitleLabel, 0, 0, 1, 1
        )
        self.gridLayout_71.addWidget(self.NullCraftValidateArgsJVMArgWidget, 9, 2, 1, 3)
        self.NullCraftValidateArgsCoreWidget = QWidget(self.NullCraftValidateArgs)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.NullCraftValidateArgsCoreWidget.sizePolicy().hasHeightForWidth()
        )
        self.NullCraftValidateArgsCoreWidget.setSizePolicy(sizePolicy)
        self.NullCraftValidateArgsCoreWidget.setObjectName(
            "NullCraftValidateArgsCoreWidget"
        )
        self.gridLayout_75 = QGridLayout(self.NullCraftValidateArgsCoreWidget)
        self.gridLayout_75.setObjectName("gridLayout_75")
        self.NullCraftValidateArgsDownloadCorePrimaryPushBtn = PrimaryPushButton(
            self.NullCraftValidateArgsCoreWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.NullCraftValidateArgsDownloadCorePrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.NullCraftValidateArgsDownloadCorePrimaryPushBtn.setSizePolicy(sizePolicy)
        self.NullCraftValidateArgsDownloadCorePrimaryPushBtn.setMinimumSize(
            QSize(90, 0)
        )
        self.NullCraftValidateArgsDownloadCorePrimaryPushBtn.setObjectName(
            "NullCraftValidateArgsDownloadCorePrimaryPushBtn"
        )
        self.gridLayout_75.addWidget(
            self.NullCraftValidateArgsDownloadCorePrimaryPushBtn, 1, 3, 1, 1
        )
        self.NullCraftValidateArgsCoreSubtitleLabel = SubtitleLabel(
            self.NullCraftValidateArgsCoreWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.NullCraftValidateArgsCoreSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.NullCraftValidateArgsCoreSubtitleLabel.setSizePolicy(sizePolicy)
        self.NullCraftValidateArgsCoreSubtitleLabel.setObjectName(
            "NullCraftValidateArgsCoreSubtitleLabel"
        )
        self.gridLayout_75.addWidget(
            self.NullCraftValidateArgsCoreSubtitleLabel, 0, 1, 1, 1
        )
        self.NullCraftValidateArgsCoreLineEdit = LineEdit(
            self.NullCraftValidateArgsCoreWidget
        )
        self.NullCraftValidateArgsCoreLineEdit.setObjectName(
            "NullCraftValidateArgsCoreLineEdit"
        )
        self.gridLayout_75.addWidget(self.NullCraftValidateArgsCoreLineEdit, 1, 1, 1, 1)
        self.NullCraftValidateArgsManuallyAddCorePrimaryPushBtn = PrimaryPushButton(
            self.NullCraftValidateArgsCoreWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.NullCraftValidateArgsManuallyAddCorePrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.NullCraftValidateArgsManuallyAddCorePrimaryPushBtn.setSizePolicy(
            sizePolicy
        )
        self.NullCraftValidateArgsManuallyAddCorePrimaryPushBtn.setMinimumSize(
            QSize(90, 0)
        )
        self.NullCraftValidateArgsManuallyAddCorePrimaryPushBtn.setObjectName(
            "NullCraftValidateArgsManuallyAddCorePrimaryPushBtn"
        )
        self.gridLayout_75.addWidget(
            self.NullCraftValidateArgsManuallyAddCorePrimaryPushBtn, 1, 2, 1, 1
        )
        self.gridLayout_71.addWidget(self.NullCraftValidateArgsCoreWidget, 7, 2, 1, 3)
        self.NullCraftValidateArgsMemWidget = QWidget(self.NullCraftValidateArgs)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.NullCraftValidateArgsMemWidget.sizePolicy().hasHeightForWidth()
        )
        self.NullCraftValidateArgsMemWidget.setSizePolicy(sizePolicy)
        self.NullCraftValidateArgsMemWidget.setMinimumSize(QSize(0, 85))
        self.NullCraftValidateArgsMemWidget.setMaximumSize(QSize(16777215, 85))
        self.NullCraftValidateArgsMemWidget.setObjectName(
            "NullCraftValidateArgsMemWidget"
        )
        self.gridLayout_76 = QGridLayout(self.NullCraftValidateArgsMemWidget)
        self.gridLayout_76.setObjectName("gridLayout_76")
        self.NullCraftValidateArgsMinMemLineEdit = LineEdit(
            self.NullCraftValidateArgsMemWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.NullCraftValidateArgsMinMemLineEdit.sizePolicy().hasHeightForWidth()
        )
        self.NullCraftValidateArgsMinMemLineEdit.setSizePolicy(sizePolicy)
        self.NullCraftValidateArgsMinMemLineEdit.setMinimumSize(QSize(0, 30))
        self.NullCraftValidateArgsMinMemLineEdit.setObjectName(
            "NullCraftValidateArgsMinMemLineEdit"
        )
        self.gridLayout_76.addWidget(
            self.NullCraftValidateArgsMinMemLineEdit, 1, 1, 1, 1
        )
        self.NullCraftValidateArgsMemSubtitleLabel = SubtitleLabel(
            self.NullCraftValidateArgsMemWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.NullCraftValidateArgsMemSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.NullCraftValidateArgsMemSubtitleLabel.setSizePolicy(sizePolicy)
        self.NullCraftValidateArgsMemSubtitleLabel.setObjectName(
            "NullCraftValidateArgsMemSubtitleLabel"
        )
        self.gridLayout_76.addWidget(
            self.NullCraftValidateArgsMemSubtitleLabel, 0, 1, 1, 1
        )
        self.NullCraftValidateArgsMaxMemLineEdit = LineEdit(
            self.NullCraftValidateArgsMemWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.NullCraftValidateArgsMaxMemLineEdit.sizePolicy().hasHeightForWidth()
        )
        self.NullCraftValidateArgsMaxMemLineEdit.setSizePolicy(sizePolicy)
        self.NullCraftValidateArgsMaxMemLineEdit.setMinimumSize(QSize(0, 30))
        self.NullCraftValidateArgsMaxMemLineEdit.setObjectName(
            "NullCraftValidateArgsMaxMemLineEdit"
        )
        self.gridLayout_76.addWidget(
            self.NullCraftValidateArgsMaxMemLineEdit, 1, 3, 1, 1
        )
        self.NullCraftValidateArgsToSymbol = SubtitleLabel(
            self.NullCraftValidateArgsMemWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.NullCraftValidateArgsToSymbol.sizePolicy().hasHeightForWidth()
        )
        self.NullCraftValidateArgsToSymbol.setSizePolicy(sizePolicy)
        self.NullCraftValidateArgsToSymbol.setObjectName(
            "NullCraftValidateArgsToSymbol"
        )
        self.gridLayout_76.addWidget(self.NullCraftValidateArgsToSymbol, 1, 2, 1, 1)
        spacerItem81 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_76.addItem(spacerItem81, 1, 5, 1, 1)
        self.NullCraftValidateArgsMemUnitComboBox = ComboBox(
            self.NullCraftValidateArgsMemWidget
        )
        self.NullCraftValidateArgsMemUnitComboBox.setObjectName(
            "NullCraftValidateArgsMemUnitComboBox"
        )
        self.gridLayout_76.addWidget(
            self.NullCraftValidateArgsMemUnitComboBox, 1, 4, 1, 1
        )
        self.gridLayout_71.addWidget(self.NullCraftValidateArgsMemWidget, 6, 2, 1, 3)
        self.NullCraftValidateArgsTitle = SubtitleLabel(self.NullCraftValidateArgs)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.NullCraftValidateArgsTitle.sizePolicy().hasHeightForWidth()
        )
        self.NullCraftValidateArgsTitle.setSizePolicy(sizePolicy)
        self.NullCraftValidateArgsTitle.setObjectName("NullCraftValidateArgsTitle")
        self.gridLayout_71.addWidget(self.NullCraftValidateArgsTitle, 0, 3, 1, 1)
        self.NullCraftValidateArgsStatus = PixmapLabel(self.NullCraftValidateArgs)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.NullCraftValidateArgsStatus.sizePolicy().hasHeightForWidth()
        )
        self.NullCraftValidateArgsStatus.setSizePolicy(sizePolicy)
        self.NullCraftValidateArgsStatus.setMinimumSize(QSize(30, 30))
        self.NullCraftValidateArgsStatus.setMaximumSize(QSize(30, 30))
        self.NullCraftValidateArgsStatus.setObjectName("NullCraftValidateArgsStatus")
        self.gridLayout_71.addWidget(self.NullCraftValidateArgsStatus, 0, 2, 1, 1)
        self.verticalLayout_10.addWidget(self.NullCraftValidateArgs)
        self.NullCraftSave = CardWidget(self.NullCraftScrollAreaWidgetContents)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.NullCraftSave.sizePolicy().hasHeightForWidth()
        )
        self.NullCraftSave.setSizePolicy(sizePolicy)
        self.NullCraftSave.setMinimumSize(QSize(0, 125))
        self.NullCraftSave.setMaximumSize(QSize(16777215, 125))
        self.NullCraftSave.setObjectName("NullCraftSave")
        self.gridLayout_77 = QGridLayout(self.NullCraftSave)
        self.gridLayout_77.setObjectName("gridLayout_77")
        self.NullCraftSaveTitle = SubtitleLabel(self.NullCraftSave)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.NullCraftSaveTitle.sizePolicy().hasHeightForWidth()
        )
        self.NullCraftSaveTitle.setSizePolicy(sizePolicy)
        self.NullCraftSaveTitle.setObjectName("NullCraftSaveTitle")
        self.gridLayout_77.addWidget(self.NullCraftSaveTitle, 0, 1, 1, 1)
        self.NullCraftSaveServerNameLineEdit = LineEdit(self.NullCraftSave)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.NullCraftSaveServerNameLineEdit.sizePolicy().hasHeightForWidth()
        )
        self.NullCraftSaveServerNameLineEdit.setSizePolicy(sizePolicy)
        self.NullCraftSaveServerNameLineEdit.setMinimumSize(QSize(0, 30))
        self.NullCraftSaveServerNameLineEdit.setObjectName(
            "NullCraftSaveServerNameLineEdit"
        )
        self.gridLayout_77.addWidget(self.NullCraftSaveServerNameLineEdit, 1, 1, 1, 1)
        spacerItem82 = QSpacerItem(20, 79, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout_77.addItem(spacerItem82, 0, 0, 3, 1)
        self.NullCraftSaveServerPrimaryPushBtn = PrimaryPushButton(self.NullCraftSave)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.NullCraftSaveServerPrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.NullCraftSaveServerPrimaryPushBtn.setSizePolicy(sizePolicy)
        self.NullCraftSaveServerPrimaryPushBtn.setMinimumSize(QSize(130, 30))
        self.NullCraftSaveServerPrimaryPushBtn.setMaximumSize(QSize(16777215, 30))
        self.NullCraftSaveServerPrimaryPushBtn.setObjectName(
            "NullCraftSaveServerPrimaryPushBtn"
        )
        self.gridLayout_77.addWidget(self.NullCraftSaveServerPrimaryPushBtn, 2, 1, 1, 1)
        self.verticalLayout_10.addWidget(self.NullCraftSave)
        self.NullCraftScrollArea.setWidget(self.NullCraftScrollAreaWidgetContents)
        self.gridLayout_78.addWidget(self.NullCraftScrollArea, 1, 3, 1, 2)
        spacerItem83 = QSpacerItem(20, 340, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.gridLayout_78.addItem(spacerItem83, 1, 2, 1, 1)
        spacerItem84 = QSpacerItem(289, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_78.addItem(spacerItem84, 0, 4, 1, 1)
        self.NullCraftBackToMain = TransparentToolButton(FIF.PAGE_LEFT, self.NullCraft)
        self.NullCraftBackToMain.setObjectName("NullCraftBackToMain")
        self.gridLayout_78.addWidget(self.NullCraftBackToMain, 0, 2, 1, 1)
        self.NullCraftTitle = SubtitleLabel(self.NullCraft)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.NullCraftTitle.sizePolicy().hasHeightForWidth()
        )
        self.NullCraftTitle.setSizePolicy(sizePolicy)
        self.NullCraftTitle.setObjectName("NullCraftTitle")
        self.gridLayout_78.addWidget(self.NullCraftTitle, 0, 3, 1, 1)
        spacerItem85 = QSpacerItem(20, 335, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout_78.addItem(spacerItem85, 0, 1, 2, 1)
        self.importNewServerStackWidget.addWidget(self.NullCraft)
        self.MCSM8 = QWidget()
        self.MCSM8.setObjectName("MCSM8")
        self.gridLayout_87 = QGridLayout(self.MCSM8)
        self.gridLayout_87.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_87.setObjectName("gridLayout_87")
        self.MCSM8BackToMain = TransparentToolButton(FIF.PAGE_LEFT, self.MCSM8)
        self.MCSM8BackToMain.setObjectName("MCSM8BackToMain")
        self.gridLayout_87.addWidget(self.MCSM8BackToMain, 0, 2, 1, 1)
        spacerItem86 = QSpacerItem(373, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_87.addItem(spacerItem86, 0, 4, 1, 1)
        spacerItem87 = QSpacerItem(20, 340, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.gridLayout_87.addItem(spacerItem87, 1, 2, 1, 1)
        self.MCSM8Title = SubtitleLabel(self.MCSM8)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.MCSM8Title.sizePolicy().hasHeightForWidth())
        self.MCSM8Title.setSizePolicy(sizePolicy)
        self.MCSM8Title.setObjectName("MCSM8Title")
        self.gridLayout_87.addWidget(self.MCSM8Title, 0, 3, 1, 1)
        self.MCSM8ScrollArea = SmoothScrollArea(self.MCSM8)
        self.MCSM8ScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.MCSM8ScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.MCSM8ScrollArea.setWidgetResizable(True)
        self.MCSM8ScrollArea.setAlignment(Qt.AlignCenter)
        self.MCSM8ScrollArea.setObjectName("MCSM8ScrollArea")
        self.MCSM8ScrollAreaWidgetContents = QWidget()
        self.MCSM8ScrollAreaWidgetContents.setGeometry(QRect(0, 0, 450, 1191))
        self.MCSM8ScrollAreaWidgetContents.setObjectName(
            "MCSM8ScrollAreaWidgetContents"
        )
        self.verticalLayout_11 = QVBoxLayout(self.MCSM8ScrollAreaWidgetContents)
        self.verticalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.MCSM8Import = CardWidget(self.MCSM8ScrollAreaWidgetContents)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.MCSM8Import.sizePolicy().hasHeightForWidth())
        self.MCSM8Import.setSizePolicy(sizePolicy)
        self.MCSM8Import.setMinimumSize(QSize(0, 150))
        self.MCSM8Import.setMaximumSize(QSize(16777215, 150))
        self.MCSM8Import.setObjectName("MCSM8Import")
        self.gridLayout_70 = QGridLayout(self.MCSM8Import)
        self.gridLayout_70.setObjectName("gridLayout_70")
        spacerItem88 = QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout_70.addItem(spacerItem88, 0, 0, 3, 1)
        self.MCSM8ImportTitle = SubtitleLabel(self.MCSM8Import)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM8ImportTitle.sizePolicy().hasHeightForWidth()
        )
        self.MCSM8ImportTitle.setSizePolicy(sizePolicy)
        self.MCSM8ImportTitle.setObjectName("MCSM8ImportTitle")
        self.gridLayout_70.addWidget(self.MCSM8ImportTitle, 0, 2, 1, 1)
        self.MCSM8ImportStatusText = BodyLabel(self.MCSM8Import)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM8ImportStatusText.sizePolicy().hasHeightForWidth()
        )
        self.MCSM8ImportStatusText.setSizePolicy(sizePolicy)
        self.MCSM8ImportStatusText.setObjectName("MCSM8ImportStatusText")
        self.gridLayout_70.addWidget(self.MCSM8ImportStatusText, 1, 1, 1, 2)
        self.MCSM8ImportStatus = PixmapLabel(self.MCSM8Import)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM8ImportStatus.sizePolicy().hasHeightForWidth()
        )
        self.MCSM8ImportStatus.setSizePolicy(sizePolicy)
        self.MCSM8ImportStatus.setMinimumSize(QSize(30, 30))
        self.MCSM8ImportStatus.setMaximumSize(QSize(30, 30))
        self.MCSM8ImportStatus.setObjectName("MCSM8ImportStatus")
        self.gridLayout_70.addWidget(self.MCSM8ImportStatus, 0, 1, 1, 1)
        spacerItem89 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_70.addItem(spacerItem89, 2, 4, 1, 4)
        self.MCSM8ImportArchives = PrimaryPushButton(self.MCSM8Import)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM8ImportArchives.sizePolicy().hasHeightForWidth()
        )
        self.MCSM8ImportArchives.setSizePolicy(sizePolicy)
        self.MCSM8ImportArchives.setMinimumSize(QSize(110, 32))
        self.MCSM8ImportArchives.setMaximumSize(QSize(150, 32))
        self.MCSM8ImportArchives.setObjectName("MCSM8ImportArchives")
        self.gridLayout_70.addWidget(self.MCSM8ImportArchives, 2, 1, 1, 2)
        self.verticalLayout_11.addWidget(self.MCSM8Import)
        self.MCSM8SelectServer = CardWidget(self.MCSM8ScrollAreaWidgetContents)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM8SelectServer.sizePolicy().hasHeightForWidth()
        )
        self.MCSM8SelectServer.setSizePolicy(sizePolicy)
        self.MCSM8SelectServer.setMinimumSize(QSize(0, 250))
        self.MCSM8SelectServer.setObjectName("MCSM8SelectServer")
        self.gridLayout_79 = QGridLayout(self.MCSM8SelectServer)
        self.gridLayout_79.setObjectName("gridLayout_79")
        self.MCSM8SelectServerStatus = PixmapLabel(self.MCSM8SelectServer)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM8SelectServerStatus.sizePolicy().hasHeightForWidth()
        )
        self.MCSM8SelectServerStatus.setSizePolicy(sizePolicy)
        self.MCSM8SelectServerStatus.setMinimumSize(QSize(30, 30))
        self.MCSM8SelectServerStatus.setMaximumSize(QSize(30, 30))
        self.MCSM8SelectServerStatus.setObjectName("MCSM8SelectServerStatus")
        self.gridLayout_79.addWidget(self.MCSM8SelectServerStatus, 0, 1, 1, 1)
        spacerItem90 = QSpacerItem(20, 279, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout_79.addItem(spacerItem90, 0, 0, 3, 1)
        self.MCSM8SelectServerStatusText = BodyLabel(self.MCSM8SelectServer)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM8SelectServerStatusText.sizePolicy().hasHeightForWidth()
        )
        self.MCSM8SelectServerStatusText.setSizePolicy(sizePolicy)
        self.MCSM8SelectServerStatusText.setObjectName("MCSM8SelectServerStatusText")
        self.gridLayout_79.addWidget(self.MCSM8SelectServerStatusText, 1, 1, 1, 2)
        self.MCSM8SelectServerTitle = SubtitleLabel(self.MCSM8SelectServer)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM8SelectServerTitle.sizePolicy().hasHeightForWidth()
        )
        self.MCSM8SelectServerTitle.setSizePolicy(sizePolicy)
        self.MCSM8SelectServerTitle.setObjectName("MCSM8SelectServerTitle")
        self.gridLayout_79.addWidget(self.MCSM8SelectServerTitle, 0, 2, 1, 1)
        self.MCSM8SelectServerTreeWidget = TreeWidget(self.MCSM8SelectServer)
        self.MCSM8SelectServerTreeWidget.setObjectName("MCSM8SelectServerTreeWidget")
        self.MCSM8SelectServerTreeWidget.headerItem().setText(0, "1")
        self.gridLayout_79.addWidget(self.MCSM8SelectServerTreeWidget, 2, 1, 1, 2)
        self.verticalLayout_11.addWidget(self.MCSM8SelectServer)
        self.MCSM8ValidateArgs = CardWidget(self.MCSM8ScrollAreaWidgetContents)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM8ValidateArgs.sizePolicy().hasHeightForWidth()
        )
        self.MCSM8ValidateArgs.setSizePolicy(sizePolicy)
        self.MCSM8ValidateArgs.setMinimumSize(QSize(0, 630))
        self.MCSM8ValidateArgs.setMaximumSize(QSize(16777215, 630))
        self.MCSM8ValidateArgs.setObjectName("MCSM8ValidateArgs")
        self.gridLayout_80 = QGridLayout(self.MCSM8ValidateArgs)
        self.gridLayout_80.setObjectName("gridLayout_80")
        self.MCSM8ValidateArgsJavaWidget = QWidget(self.MCSM8ValidateArgs)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM8ValidateArgsJavaWidget.sizePolicy().hasHeightForWidth()
        )
        self.MCSM8ValidateArgsJavaWidget.setSizePolicy(sizePolicy)
        self.MCSM8ValidateArgsJavaWidget.setMinimumSize(QSize(0, 120))
        self.MCSM8ValidateArgsJavaWidget.setObjectName("MCSM8ValidateArgsJavaWidget")
        self.gridLayout_81 = QGridLayout(self.MCSM8ValidateArgsJavaWidget)
        self.gridLayout_81.setObjectName("gridLayout_81")
        self.MCSM8ValidateArgsJavaListPushBtn = PushButton(
            self.MCSM8ValidateArgsJavaWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM8ValidateArgsJavaListPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.MCSM8ValidateArgsJavaListPushBtn.setSizePolicy(sizePolicy)
        self.MCSM8ValidateArgsJavaListPushBtn.setMinimumSize(QSize(108, 31))
        self.MCSM8ValidateArgsJavaListPushBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.MCSM8ValidateArgsJavaListPushBtn.setObjectName(
            "MCSM8ValidateArgsJavaListPushBtn"
        )
        self.gridLayout_81.addWidget(self.MCSM8ValidateArgsJavaListPushBtn, 3, 2, 1, 1)
        self.MCSM8ValidateArgsJavaTextEdit = TextEdit(self.MCSM8ValidateArgsJavaWidget)
        self.MCSM8ValidateArgsJavaTextEdit.setObjectName(
            "MCSM8ValidateArgsJavaTextEdit"
        )
        self.gridLayout_81.addWidget(self.MCSM8ValidateArgsJavaTextEdit, 2, 0, 2, 1)
        self.MCSM8ValidateArgsAutoDetectJavaPrimaryPushBtn = PrimaryPushButton(
            self.MCSM8ValidateArgsJavaWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM8ValidateArgsAutoDetectJavaPrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.MCSM8ValidateArgsAutoDetectJavaPrimaryPushBtn.setSizePolicy(sizePolicy)
        self.MCSM8ValidateArgsAutoDetectJavaPrimaryPushBtn.setCursor(
            QCursor(Qt.PointingHandCursor)
        )
        self.MCSM8ValidateArgsAutoDetectJavaPrimaryPushBtn.setObjectName(
            "MCSM8ValidateArgsAutoDetectJavaPrimaryPushBtn"
        )
        self.gridLayout_81.addWidget(
            self.MCSM8ValidateArgsAutoDetectJavaPrimaryPushBtn, 2, 2, 1, 1
        )
        self.MCSM8ValidateArgsManuallyAddJavaPrimaryPushBtn = PrimaryPushButton(
            self.MCSM8ValidateArgsJavaWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM8ValidateArgsManuallyAddJavaPrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.MCSM8ValidateArgsManuallyAddJavaPrimaryPushBtn.setSizePolicy(sizePolicy)
        self.MCSM8ValidateArgsManuallyAddJavaPrimaryPushBtn.setMinimumSize(QSize(90, 0))
        self.MCSM8ValidateArgsManuallyAddJavaPrimaryPushBtn.setCursor(
            QCursor(Qt.PointingHandCursor)
        )
        self.MCSM8ValidateArgsManuallyAddJavaPrimaryPushBtn.setObjectName(
            "MCSM8ValidateArgsManuallyAddJavaPrimaryPushBtn"
        )
        self.gridLayout_81.addWidget(
            self.MCSM8ValidateArgsManuallyAddJavaPrimaryPushBtn, 2, 1, 1, 1
        )
        self.MCSM8ValidateArgsDownloadJavaPrimaryPushBtn = PrimaryPushButton(
            self.MCSM8ValidateArgsJavaWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM8ValidateArgsDownloadJavaPrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.MCSM8ValidateArgsDownloadJavaPrimaryPushBtn.setSizePolicy(sizePolicy)
        self.MCSM8ValidateArgsDownloadJavaPrimaryPushBtn.setMinimumSize(QSize(90, 0))
        self.MCSM8ValidateArgsDownloadJavaPrimaryPushBtn.setCursor(
            QCursor(Qt.PointingHandCursor)
        )
        self.MCSM8ValidateArgsDownloadJavaPrimaryPushBtn.setObjectName(
            "MCSM8ValidateArgsDownloadJavaPrimaryPushBtn"
        )
        self.gridLayout_81.addWidget(
            self.MCSM8ValidateArgsDownloadJavaPrimaryPushBtn, 3, 1, 1, 1
        )
        self.MCSM8ValidateArgsJavaSubtitleLabel = SubtitleLabel(
            self.MCSM8ValidateArgsJavaWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM8ValidateArgsJavaSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.MCSM8ValidateArgsJavaSubtitleLabel.setSizePolicy(sizePolicy)
        self.MCSM8ValidateArgsJavaSubtitleLabel.setObjectName(
            "MCSM8ValidateArgsJavaSubtitleLabel"
        )
        self.gridLayout_81.addWidget(
            self.MCSM8ValidateArgsJavaSubtitleLabel, 0, 0, 1, 1
        )
        self.gridLayout_80.addWidget(self.MCSM8ValidateArgsJavaWidget, 5, 2, 1, 3)
        self.MCSM8ValidateArgsDeEncodingWidget = QWidget(self.MCSM8ValidateArgs)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM8ValidateArgsDeEncodingWidget.sizePolicy().hasHeightForWidth()
        )
        self.MCSM8ValidateArgsDeEncodingWidget.setSizePolicy(sizePolicy)
        self.MCSM8ValidateArgsDeEncodingWidget.setMinimumSize(QSize(0, 122))
        self.MCSM8ValidateArgsDeEncodingWidget.setMaximumSize(QSize(16777215, 122))
        self.MCSM8ValidateArgsDeEncodingWidget.setObjectName(
            "MCSM8ValidateArgsDeEncodingWidget"
        )
        self.gridLayout_82 = QGridLayout(self.MCSM8ValidateArgsDeEncodingWidget)
        self.gridLayout_82.setObjectName("gridLayout_82")
        self.MCSM8ValidateArgsOutputDeEncodingComboBox = ComboBox(
            self.MCSM8ValidateArgsDeEncodingWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM8ValidateArgsOutputDeEncodingComboBox.sizePolicy().hasHeightForWidth()
        )
        self.MCSM8ValidateArgsOutputDeEncodingComboBox.setSizePolicy(sizePolicy)
        self.MCSM8ValidateArgsOutputDeEncodingComboBox.setObjectName(
            "MCSM8ValidateArgsOutputDeEncodingComboBox"
        )
        self.gridLayout_82.addWidget(
            self.MCSM8ValidateArgsOutputDeEncodingComboBox, 2, 1, 1, 1
        )
        self.MCSM8ValidateArgsInputDeEncodingComboBox = ComboBox(
            self.MCSM8ValidateArgsDeEncodingWidget
        )
        self.MCSM8ValidateArgsInputDeEncodingComboBox.setText("")
        self.MCSM8ValidateArgsInputDeEncodingComboBox.setObjectName(
            "MCSM8ValidateArgsInputDeEncodingComboBox"
        )
        self.gridLayout_82.addWidget(
            self.MCSM8ValidateArgsInputDeEncodingComboBox, 3, 1, 1, 1
        )
        self.MCSM8ValidateArgsOutputDeEncodingLabel = StrongBodyLabel(
            self.MCSM8ValidateArgsDeEncodingWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM8ValidateArgsOutputDeEncodingLabel.sizePolicy().hasHeightForWidth()
        )
        self.MCSM8ValidateArgsOutputDeEncodingLabel.setSizePolicy(sizePolicy)
        self.MCSM8ValidateArgsOutputDeEncodingLabel.setObjectName(
            "MCSM8ValidateArgsOutputDeEncodingLabel"
        )
        self.gridLayout_82.addWidget(
            self.MCSM8ValidateArgsOutputDeEncodingLabel, 2, 0, 1, 1
        )
        self.MCSM8ValidateArgsDeEncodingSubtitleLabel = SubtitleLabel(
            self.MCSM8ValidateArgsDeEncodingWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM8ValidateArgsDeEncodingSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.MCSM8ValidateArgsDeEncodingSubtitleLabel.setSizePolicy(sizePolicy)
        self.MCSM8ValidateArgsDeEncodingSubtitleLabel.setObjectName(
            "MCSM8ValidateArgsDeEncodingSubtitleLabel"
        )
        self.gridLayout_82.addWidget(
            self.MCSM8ValidateArgsDeEncodingSubtitleLabel, 0, 0, 1, 1
        )
        self.MCSM8ValidateArgsInputDeEncodingLabel = StrongBodyLabel(
            self.MCSM8ValidateArgsDeEncodingWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM8ValidateArgsInputDeEncodingLabel.sizePolicy().hasHeightForWidth()
        )
        self.MCSM8ValidateArgsInputDeEncodingLabel.setSizePolicy(sizePolicy)
        self.MCSM8ValidateArgsInputDeEncodingLabel.setObjectName(
            "MCSM8ValidateArgsInputDeEncodingLabel"
        )
        self.gridLayout_82.addWidget(
            self.MCSM8ValidateArgsInputDeEncodingLabel, 3, 0, 1, 1
        )
        self.gridLayout_80.addWidget(self.MCSM8ValidateArgsDeEncodingWidget, 8, 2, 1, 3)
        spacerItem91 = QSpacerItem(20, 102, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout_80.addItem(spacerItem91, 0, 0, 21, 1)
        self.MCSM8ValidateArgsJVMArgWidget = QWidget(self.MCSM8ValidateArgs)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM8ValidateArgsJVMArgWidget.sizePolicy().hasHeightForWidth()
        )
        self.MCSM8ValidateArgsJVMArgWidget.setSizePolicy(sizePolicy)
        self.MCSM8ValidateArgsJVMArgWidget.setMinimumSize(QSize(0, 140))
        self.MCSM8ValidateArgsJVMArgWidget.setMaximumSize(QSize(16777215, 140))
        self.MCSM8ValidateArgsJVMArgWidget.setObjectName(
            "MCSM8ValidateArgsJVMArgWidget"
        )
        self.gridLayout_83 = QGridLayout(self.MCSM8ValidateArgsJVMArgWidget)
        self.gridLayout_83.setObjectName("gridLayout_83")
        self.MCSM8ValidateArgsJVMArgPlainTextEdit = PlainTextEdit(
            self.MCSM8ValidateArgsJVMArgWidget
        )
        self.MCSM8ValidateArgsJVMArgPlainTextEdit.setObjectName(
            "MCSM8ValidateArgsJVMArgPlainTextEdit"
        )
        self.gridLayout_83.addWidget(
            self.MCSM8ValidateArgsJVMArgPlainTextEdit, 1, 0, 1, 1
        )
        self.MCSM8ValidateArgsJVMArgSubtitleLabel = SubtitleLabel(
            self.MCSM8ValidateArgsJVMArgWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM8ValidateArgsJVMArgSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.MCSM8ValidateArgsJVMArgSubtitleLabel.setSizePolicy(sizePolicy)
        self.MCSM8ValidateArgsJVMArgSubtitleLabel.setObjectName(
            "MCSM8ValidateArgsJVMArgSubtitleLabel"
        )
        self.gridLayout_83.addWidget(
            self.MCSM8ValidateArgsJVMArgSubtitleLabel, 0, 0, 1, 1
        )
        self.gridLayout_80.addWidget(self.MCSM8ValidateArgsJVMArgWidget, 9, 2, 1, 3)
        self.MCSM8ValidateArgsCoreWidget = QWidget(self.MCSM8ValidateArgs)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM8ValidateArgsCoreWidget.sizePolicy().hasHeightForWidth()
        )
        self.MCSM8ValidateArgsCoreWidget.setSizePolicy(sizePolicy)
        self.MCSM8ValidateArgsCoreWidget.setObjectName("MCSM8ValidateArgsCoreWidget")
        self.gridLayout_84 = QGridLayout(self.MCSM8ValidateArgsCoreWidget)
        self.gridLayout_84.setObjectName("gridLayout_84")
        self.MCSM8ValidateArgsDownloadCorePrimaryPushBtn = PrimaryPushButton(
            self.MCSM8ValidateArgsCoreWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM8ValidateArgsDownloadCorePrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.MCSM8ValidateArgsDownloadCorePrimaryPushBtn.setSizePolicy(sizePolicy)
        self.MCSM8ValidateArgsDownloadCorePrimaryPushBtn.setMinimumSize(QSize(90, 0))
        self.MCSM8ValidateArgsDownloadCorePrimaryPushBtn.setObjectName(
            "MCSM8ValidateArgsDownloadCorePrimaryPushBtn"
        )
        self.gridLayout_84.addWidget(
            self.MCSM8ValidateArgsDownloadCorePrimaryPushBtn, 1, 3, 1, 1
        )
        self.MCSM8ValidateArgsCoreSubtitleLabel = SubtitleLabel(
            self.MCSM8ValidateArgsCoreWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM8ValidateArgsCoreSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.MCSM8ValidateArgsCoreSubtitleLabel.setSizePolicy(sizePolicy)
        self.MCSM8ValidateArgsCoreSubtitleLabel.setObjectName(
            "MCSM8ValidateArgsCoreSubtitleLabel"
        )
        self.gridLayout_84.addWidget(
            self.MCSM8ValidateArgsCoreSubtitleLabel, 0, 1, 1, 1
        )
        self.MCSM8ValidateArgsCoreLineEdit = LineEdit(self.MCSM8ValidateArgsCoreWidget)
        self.MCSM8ValidateArgsCoreLineEdit.setObjectName(
            "MCSM8ValidateArgsCoreLineEdit"
        )
        self.gridLayout_84.addWidget(self.MCSM8ValidateArgsCoreLineEdit, 1, 1, 1, 1)
        self.MCSM8ValidateArgsManuallyAddCorePrimaryPushBtn = PrimaryPushButton(
            self.MCSM8ValidateArgsCoreWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM8ValidateArgsManuallyAddCorePrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.MCSM8ValidateArgsManuallyAddCorePrimaryPushBtn.setSizePolicy(sizePolicy)
        self.MCSM8ValidateArgsManuallyAddCorePrimaryPushBtn.setMinimumSize(QSize(90, 0))
        self.MCSM8ValidateArgsManuallyAddCorePrimaryPushBtn.setObjectName(
            "MCSM8ValidateArgsManuallyAddCorePrimaryPushBtn"
        )
        self.gridLayout_84.addWidget(
            self.MCSM8ValidateArgsManuallyAddCorePrimaryPushBtn, 1, 2, 1, 1
        )
        self.gridLayout_80.addWidget(self.MCSM8ValidateArgsCoreWidget, 7, 2, 1, 3)
        self.MCSM8ValidateArgsMemWidget = QWidget(self.MCSM8ValidateArgs)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM8ValidateArgsMemWidget.sizePolicy().hasHeightForWidth()
        )
        self.MCSM8ValidateArgsMemWidget.setSizePolicy(sizePolicy)
        self.MCSM8ValidateArgsMemWidget.setMinimumSize(QSize(0, 85))
        self.MCSM8ValidateArgsMemWidget.setMaximumSize(QSize(16777215, 85))
        self.MCSM8ValidateArgsMemWidget.setObjectName("MCSM8ValidateArgsMemWidget")
        self.gridLayout_85 = QGridLayout(self.MCSM8ValidateArgsMemWidget)
        self.gridLayout_85.setObjectName("gridLayout_85")
        self.MCSM8ValidateArgsMinMemLineEdit = LineEdit(self.MCSM8ValidateArgsMemWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM8ValidateArgsMinMemLineEdit.sizePolicy().hasHeightForWidth()
        )
        self.MCSM8ValidateArgsMinMemLineEdit.setSizePolicy(sizePolicy)
        self.MCSM8ValidateArgsMinMemLineEdit.setMinimumSize(QSize(0, 30))
        self.MCSM8ValidateArgsMinMemLineEdit.setObjectName(
            "MCSM8ValidateArgsMinMemLineEdit"
        )
        self.gridLayout_85.addWidget(self.MCSM8ValidateArgsMinMemLineEdit, 1, 1, 1, 1)
        self.MCSM8ValidateArgsMemSubtitleLabel = SubtitleLabel(
            self.MCSM8ValidateArgsMemWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM8ValidateArgsMemSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.MCSM8ValidateArgsMemSubtitleLabel.setSizePolicy(sizePolicy)
        self.MCSM8ValidateArgsMemSubtitleLabel.setObjectName(
            "MCSM8ValidateArgsMemSubtitleLabel"
        )
        self.gridLayout_85.addWidget(self.MCSM8ValidateArgsMemSubtitleLabel, 0, 1, 1, 1)
        self.MCSM8ValidateArgsMaxMemLineEdit = LineEdit(self.MCSM8ValidateArgsMemWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM8ValidateArgsMaxMemLineEdit.sizePolicy().hasHeightForWidth()
        )
        self.MCSM8ValidateArgsMaxMemLineEdit.setSizePolicy(sizePolicy)
        self.MCSM8ValidateArgsMaxMemLineEdit.setMinimumSize(QSize(0, 30))
        self.MCSM8ValidateArgsMaxMemLineEdit.setObjectName(
            "MCSM8ValidateArgsMaxMemLineEdit"
        )
        self.gridLayout_85.addWidget(self.MCSM8ValidateArgsMaxMemLineEdit, 1, 3, 1, 1)
        self.MCSM8ValidateArgsToSymbol = SubtitleLabel(self.MCSM8ValidateArgsMemWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM8ValidateArgsToSymbol.sizePolicy().hasHeightForWidth()
        )
        self.MCSM8ValidateArgsToSymbol.setSizePolicy(sizePolicy)
        self.MCSM8ValidateArgsToSymbol.setObjectName("MCSM8ValidateArgsToSymbol")
        self.gridLayout_85.addWidget(self.MCSM8ValidateArgsToSymbol, 1, 2, 1, 1)
        spacerItem92 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_85.addItem(spacerItem92, 1, 5, 1, 1)
        self.MCSM8ValidateArgsMemUnitComboBox = ComboBox(
            self.MCSM8ValidateArgsMemWidget
        )
        self.MCSM8ValidateArgsMemUnitComboBox.setObjectName(
            "MCSM8ValidateArgsMemUnitComboBox"
        )
        self.gridLayout_85.addWidget(self.MCSM8ValidateArgsMemUnitComboBox, 1, 4, 1, 1)
        self.gridLayout_80.addWidget(self.MCSM8ValidateArgsMemWidget, 6, 2, 1, 3)
        self.MCSM8ValidateArgsTitle = SubtitleLabel(self.MCSM8ValidateArgs)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM8ValidateArgsTitle.sizePolicy().hasHeightForWidth()
        )
        self.MCSM8ValidateArgsTitle.setSizePolicy(sizePolicy)
        self.MCSM8ValidateArgsTitle.setObjectName("MCSM8ValidateArgsTitle")
        self.gridLayout_80.addWidget(self.MCSM8ValidateArgsTitle, 0, 3, 1, 1)
        self.MCSM8ValidateArgsStatus = PixmapLabel(self.MCSM8ValidateArgs)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM8ValidateArgsStatus.sizePolicy().hasHeightForWidth()
        )
        self.MCSM8ValidateArgsStatus.setSizePolicy(sizePolicy)
        self.MCSM8ValidateArgsStatus.setMinimumSize(QSize(30, 30))
        self.MCSM8ValidateArgsStatus.setMaximumSize(QSize(30, 30))
        self.MCSM8ValidateArgsStatus.setObjectName("MCSM8ValidateArgsStatus")
        self.gridLayout_80.addWidget(self.MCSM8ValidateArgsStatus, 0, 2, 1, 1)
        self.verticalLayout_11.addWidget(self.MCSM8ValidateArgs)
        self.MCSM8Save = CardWidget(self.MCSM8ScrollAreaWidgetContents)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.MCSM8Save.sizePolicy().hasHeightForWidth())
        self.MCSM8Save.setSizePolicy(sizePolicy)
        self.MCSM8Save.setMinimumSize(QSize(0, 125))
        self.MCSM8Save.setMaximumSize(QSize(16777215, 125))
        self.MCSM8Save.setObjectName("MCSM8Save")
        self.gridLayout_86 = QGridLayout(self.MCSM8Save)
        self.gridLayout_86.setObjectName("gridLayout_86")
        self.MCSM8SaveTitle = SubtitleLabel(self.MCSM8Save)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM8SaveTitle.sizePolicy().hasHeightForWidth()
        )
        self.MCSM8SaveTitle.setSizePolicy(sizePolicy)
        self.MCSM8SaveTitle.setObjectName("MCSM8SaveTitle")
        self.gridLayout_86.addWidget(self.MCSM8SaveTitle, 0, 1, 1, 1)
        self.MCSM8SaveServerNameLineEdit = LineEdit(self.MCSM8Save)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM8SaveServerNameLineEdit.sizePolicy().hasHeightForWidth()
        )
        self.MCSM8SaveServerNameLineEdit.setSizePolicy(sizePolicy)
        self.MCSM8SaveServerNameLineEdit.setMinimumSize(QSize(0, 30))
        self.MCSM8SaveServerNameLineEdit.setObjectName("MCSM8SaveServerNameLineEdit")
        self.gridLayout_86.addWidget(self.MCSM8SaveServerNameLineEdit, 1, 1, 1, 1)
        spacerItem93 = QSpacerItem(20, 79, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout_86.addItem(spacerItem93, 0, 0, 3, 1)
        self.MCSM8SaveServerPrimaryPushBtn = PrimaryPushButton(self.MCSM8Save)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM8SaveServerPrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.MCSM8SaveServerPrimaryPushBtn.setSizePolicy(sizePolicy)
        self.MCSM8SaveServerPrimaryPushBtn.setMinimumSize(QSize(130, 30))
        self.MCSM8SaveServerPrimaryPushBtn.setMaximumSize(QSize(16777215, 30))
        self.MCSM8SaveServerPrimaryPushBtn.setObjectName(
            "MCSM8SaveServerPrimaryPushBtn"
        )
        self.gridLayout_86.addWidget(self.MCSM8SaveServerPrimaryPushBtn, 2, 1, 1, 1)
        self.verticalLayout_11.addWidget(self.MCSM8Save)
        self.MCSM8ScrollArea.setWidget(self.MCSM8ScrollAreaWidgetContents)
        self.gridLayout_87.addWidget(self.MCSM8ScrollArea, 1, 3, 1, 2)
        spacerItem94 = QSpacerItem(20, 335, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout_87.addItem(spacerItem94, 0, 1, 2, 1)
        self.importNewServerStackWidget.addWidget(self.MCSM8)
        self.MCSM9 = QWidget()
        self.MCSM9.setObjectName("MCSM9")
        self.gridLayout_97 = QGridLayout(self.MCSM9)
        self.gridLayout_97.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_97.setObjectName("gridLayout_97")
        spacerItem95 = QSpacerItem(20, 340, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.gridLayout_97.addItem(spacerItem95, 1, 2, 1, 1)
        self.MCSM9ScrollArea = SmoothScrollArea(self.MCSM9)
        self.MCSM9ScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.MCSM9ScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.MCSM9ScrollArea.setWidgetResizable(True)
        self.MCSM9ScrollArea.setAlignment(Qt.AlignCenter)
        self.MCSM9ScrollArea.setObjectName("MCSM9ScrollArea")
        self.MCSM9ScrollAreaWidgetContents = QWidget()
        self.MCSM9ScrollAreaWidgetContents.setGeometry(QRect(0, 0, 506, 1191))
        self.MCSM9ScrollAreaWidgetContents.setObjectName(
            "MCSM9ScrollAreaWidgetContents"
        )
        self.verticalLayout_12 = QVBoxLayout(self.MCSM9ScrollAreaWidgetContents)
        self.verticalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.MCSM9Import = CardWidget(self.MCSM9ScrollAreaWidgetContents)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.MCSM9Import.sizePolicy().hasHeightForWidth())
        self.MCSM9Import.setSizePolicy(sizePolicy)
        self.MCSM9Import.setMinimumSize(QSize(0, 150))
        self.MCSM9Import.setMaximumSize(QSize(16777215, 150))
        self.MCSM9Import.setObjectName("MCSM9Import")
        self.gridLayout_88 = QGridLayout(self.MCSM9Import)
        self.gridLayout_88.setObjectName("gridLayout_88")
        spacerItem96 = QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout_88.addItem(spacerItem96, 0, 0, 3, 1)
        self.MCSM9ImportTitle = SubtitleLabel(self.MCSM9Import)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM9ImportTitle.sizePolicy().hasHeightForWidth()
        )
        self.MCSM9ImportTitle.setSizePolicy(sizePolicy)
        self.MCSM9ImportTitle.setObjectName("MCSM9ImportTitle")
        self.gridLayout_88.addWidget(self.MCSM9ImportTitle, 0, 2, 1, 1)
        self.MCSM9ImportStatusText = BodyLabel(self.MCSM9Import)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM9ImportStatusText.sizePolicy().hasHeightForWidth()
        )
        self.MCSM9ImportStatusText.setSizePolicy(sizePolicy)
        self.MCSM9ImportStatusText.setObjectName("MCSM9ImportStatusText")
        self.gridLayout_88.addWidget(self.MCSM9ImportStatusText, 1, 1, 1, 2)
        self.MCSM9ImportStatus = PixmapLabel(self.MCSM9Import)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM9ImportStatus.sizePolicy().hasHeightForWidth()
        )
        self.MCSM9ImportStatus.setSizePolicy(sizePolicy)
        self.MCSM9ImportStatus.setMinimumSize(QSize(30, 30))
        self.MCSM9ImportStatus.setMaximumSize(QSize(30, 30))
        self.MCSM9ImportStatus.setObjectName("MCSM9ImportStatus")
        self.gridLayout_88.addWidget(self.MCSM9ImportStatus, 0, 1, 1, 1)
        spacerItem97 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_88.addItem(spacerItem97, 2, 4, 1, 4)
        self.MCSM9ImportArchives = PrimaryPushButton(self.MCSM9Import)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM9ImportArchives.sizePolicy().hasHeightForWidth()
        )
        self.MCSM9ImportArchives.setSizePolicy(sizePolicy)
        self.MCSM9ImportArchives.setMinimumSize(QSize(110, 32))
        self.MCSM9ImportArchives.setMaximumSize(QSize(150, 32))
        self.MCSM9ImportArchives.setObjectName("MCSM9ImportArchives")
        self.gridLayout_88.addWidget(self.MCSM9ImportArchives, 2, 1, 1, 2)
        self.verticalLayout_12.addWidget(self.MCSM9Import)
        self.MCSM9SelectServer = CardWidget(self.MCSM9ScrollAreaWidgetContents)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM9SelectServer.sizePolicy().hasHeightForWidth()
        )
        self.MCSM9SelectServer.setSizePolicy(sizePolicy)
        self.MCSM9SelectServer.setMinimumSize(QSize(0, 250))
        self.MCSM9SelectServer.setObjectName("MCSM9SelectServer")
        self.gridLayout_89 = QGridLayout(self.MCSM9SelectServer)
        self.gridLayout_89.setObjectName("gridLayout_89")
        self.MCSM9SelectServerStatus = PixmapLabel(self.MCSM9SelectServer)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM9SelectServerStatus.sizePolicy().hasHeightForWidth()
        )
        self.MCSM9SelectServerStatus.setSizePolicy(sizePolicy)
        self.MCSM9SelectServerStatus.setMinimumSize(QSize(30, 30))
        self.MCSM9SelectServerStatus.setMaximumSize(QSize(30, 30))
        self.MCSM9SelectServerStatus.setObjectName("MCSM9SelectServerStatus")
        self.gridLayout_89.addWidget(self.MCSM9SelectServerStatus, 0, 1, 1, 1)
        spacerItem98 = QSpacerItem(20, 279, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout_89.addItem(spacerItem98, 0, 0, 3, 1)
        self.MCSM9SelectServerStatusText = BodyLabel(self.MCSM9SelectServer)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM9SelectServerStatusText.sizePolicy().hasHeightForWidth()
        )
        self.MCSM9SelectServerStatusText.setSizePolicy(sizePolicy)
        self.MCSM9SelectServerStatusText.setObjectName("MCSM9SelectServerStatusText")
        self.gridLayout_89.addWidget(self.MCSM9SelectServerStatusText, 1, 1, 1, 2)
        self.MCSM9SelectServerTitle = SubtitleLabel(self.MCSM9SelectServer)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM9SelectServerTitle.sizePolicy().hasHeightForWidth()
        )
        self.MCSM9SelectServerTitle.setSizePolicy(sizePolicy)
        self.MCSM9SelectServerTitle.setObjectName("MCSM9SelectServerTitle")
        self.gridLayout_89.addWidget(self.MCSM9SelectServerTitle, 0, 2, 1, 1)
        self.MCSM9SelectServerTreeWidget = TreeWidget(self.MCSM9SelectServer)
        self.MCSM9SelectServerTreeWidget.setObjectName("MCSM9SelectServerTreeWidget")
        self.MCSM9SelectServerTreeWidget.headerItem().setText(0, "1")
        self.gridLayout_89.addWidget(self.MCSM9SelectServerTreeWidget, 2, 1, 1, 2)
        self.verticalLayout_12.addWidget(self.MCSM9SelectServer)
        self.MCSM9ValidateArgs = CardWidget(self.MCSM9ScrollAreaWidgetContents)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM9ValidateArgs.sizePolicy().hasHeightForWidth()
        )
        self.MCSM9ValidateArgs.setSizePolicy(sizePolicy)
        self.MCSM9ValidateArgs.setMinimumSize(QSize(0, 630))
        self.MCSM9ValidateArgs.setMaximumSize(QSize(16777215, 630))
        self.MCSM9ValidateArgs.setObjectName("MCSM9ValidateArgs")
        self.gridLayout_90 = QGridLayout(self.MCSM9ValidateArgs)
        self.gridLayout_90.setObjectName("gridLayout_90")
        self.MCSM9ValidateArgsJavaWidget = QWidget(self.MCSM9ValidateArgs)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM9ValidateArgsJavaWidget.sizePolicy().hasHeightForWidth()
        )
        self.MCSM9ValidateArgsJavaWidget.setSizePolicy(sizePolicy)
        self.MCSM9ValidateArgsJavaWidget.setMinimumSize(QSize(0, 120))
        self.MCSM9ValidateArgsJavaWidget.setObjectName("MCSM9ValidateArgsJavaWidget")
        self.gridLayout_91 = QGridLayout(self.MCSM9ValidateArgsJavaWidget)
        self.gridLayout_91.setObjectName("gridLayout_91")
        self.MCSM9ValidateArgsJavaListPushBtn = PushButton(
            self.MCSM9ValidateArgsJavaWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM9ValidateArgsJavaListPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.MCSM9ValidateArgsJavaListPushBtn.setSizePolicy(sizePolicy)
        self.MCSM9ValidateArgsJavaListPushBtn.setMinimumSize(QSize(108, 31))
        self.MCSM9ValidateArgsJavaListPushBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.MCSM9ValidateArgsJavaListPushBtn.setObjectName(
            "MCSM9ValidateArgsJavaListPushBtn"
        )
        self.gridLayout_91.addWidget(self.MCSM9ValidateArgsJavaListPushBtn, 3, 2, 1, 1)
        self.MCSM9ValidateArgsJavaTextEdit = TextEdit(self.MCSM9ValidateArgsJavaWidget)
        self.MCSM9ValidateArgsJavaTextEdit.setObjectName(
            "MCSM9ValidateArgsJavaTextEdit"
        )
        self.gridLayout_91.addWidget(self.MCSM9ValidateArgsJavaTextEdit, 2, 0, 2, 1)
        self.MCSM9ValidateArgsAutoDetectJavaPrimaryPushBtn = PrimaryPushButton(
            self.MCSM9ValidateArgsJavaWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM9ValidateArgsAutoDetectJavaPrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.MCSM9ValidateArgsAutoDetectJavaPrimaryPushBtn.setSizePolicy(sizePolicy)
        self.MCSM9ValidateArgsAutoDetectJavaPrimaryPushBtn.setCursor(
            QCursor(Qt.PointingHandCursor)
        )
        self.MCSM9ValidateArgsAutoDetectJavaPrimaryPushBtn.setObjectName(
            "MCSM9ValidateArgsAutoDetectJavaPrimaryPushBtn"
        )
        self.gridLayout_91.addWidget(
            self.MCSM9ValidateArgsAutoDetectJavaPrimaryPushBtn, 2, 2, 1, 1
        )
        self.MCSM9ValidateArgsManuallyAddJavaPrimaryPushBtn = PrimaryPushButton(
            self.MCSM9ValidateArgsJavaWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM9ValidateArgsManuallyAddJavaPrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.MCSM9ValidateArgsManuallyAddJavaPrimaryPushBtn.setSizePolicy(sizePolicy)
        self.MCSM9ValidateArgsManuallyAddJavaPrimaryPushBtn.setMinimumSize(QSize(90, 0))
        self.MCSM9ValidateArgsManuallyAddJavaPrimaryPushBtn.setCursor(
            QCursor(Qt.PointingHandCursor)
        )
        self.MCSM9ValidateArgsManuallyAddJavaPrimaryPushBtn.setObjectName(
            "MCSM9ValidateArgsManuallyAddJavaPrimaryPushBtn"
        )
        self.gridLayout_91.addWidget(
            self.MCSM9ValidateArgsManuallyAddJavaPrimaryPushBtn, 2, 1, 1, 1
        )
        self.MCSM9ValidateArgsDownloadJavaPrimaryPushBtn = PrimaryPushButton(
            self.MCSM9ValidateArgsJavaWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM9ValidateArgsDownloadJavaPrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.MCSM9ValidateArgsDownloadJavaPrimaryPushBtn.setSizePolicy(sizePolicy)
        self.MCSM9ValidateArgsDownloadJavaPrimaryPushBtn.setMinimumSize(QSize(90, 0))
        self.MCSM9ValidateArgsDownloadJavaPrimaryPushBtn.setCursor(
            QCursor(Qt.PointingHandCursor)
        )
        self.MCSM9ValidateArgsDownloadJavaPrimaryPushBtn.setObjectName(
            "MCSM9ValidateArgsDownloadJavaPrimaryPushBtn"
        )
        self.gridLayout_91.addWidget(
            self.MCSM9ValidateArgsDownloadJavaPrimaryPushBtn, 3, 1, 1, 1
        )
        self.MCSM9ValidateArgsJavaSubtitleLabel = SubtitleLabel(
            self.MCSM9ValidateArgsJavaWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM9ValidateArgsJavaSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.MCSM9ValidateArgsJavaSubtitleLabel.setSizePolicy(sizePolicy)
        self.MCSM9ValidateArgsJavaSubtitleLabel.setObjectName(
            "MCSM9ValidateArgsJavaSubtitleLabel"
        )
        self.gridLayout_91.addWidget(
            self.MCSM9ValidateArgsJavaSubtitleLabel, 0, 0, 1, 1
        )
        self.gridLayout_90.addWidget(self.MCSM9ValidateArgsJavaWidget, 5, 2, 1, 3)
        self.MCSM9ValidateArgsDeEncodingWidget = QWidget(self.MCSM9ValidateArgs)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM9ValidateArgsDeEncodingWidget.sizePolicy().hasHeightForWidth()
        )
        self.MCSM9ValidateArgsDeEncodingWidget.setSizePolicy(sizePolicy)
        self.MCSM9ValidateArgsDeEncodingWidget.setMinimumSize(QSize(0, 122))
        self.MCSM9ValidateArgsDeEncodingWidget.setMaximumSize(QSize(16777215, 122))
        self.MCSM9ValidateArgsDeEncodingWidget.setObjectName(
            "MCSM9ValidateArgsDeEncodingWidget"
        )
        self.gridLayout_92 = QGridLayout(self.MCSM9ValidateArgsDeEncodingWidget)
        self.gridLayout_92.setObjectName("gridLayout_92")
        self.MCSM9ValidateArgsOutputDeEncodingComboBox = ComboBox(
            self.MCSM9ValidateArgsDeEncodingWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM9ValidateArgsOutputDeEncodingComboBox.sizePolicy().hasHeightForWidth()
        )
        self.MCSM9ValidateArgsOutputDeEncodingComboBox.setSizePolicy(sizePolicy)
        self.MCSM9ValidateArgsOutputDeEncodingComboBox.setObjectName(
            "MCSM9ValidateArgsOutputDeEncodingComboBox"
        )
        self.gridLayout_92.addWidget(
            self.MCSM9ValidateArgsOutputDeEncodingComboBox, 2, 1, 1, 1
        )
        self.MCSM9ValidateArgsInputDeEncodingComboBox = ComboBox(
            self.MCSM9ValidateArgsDeEncodingWidget
        )
        self.MCSM9ValidateArgsInputDeEncodingComboBox.setText("")
        self.MCSM9ValidateArgsInputDeEncodingComboBox.setObjectName(
            "MCSM9ValidateArgsInputDeEncodingComboBox"
        )
        self.gridLayout_92.addWidget(
            self.MCSM9ValidateArgsInputDeEncodingComboBox, 3, 1, 1, 1
        )
        self.MCSM9ValidateArgsOutputDeEncodingLabel = StrongBodyLabel(
            self.MCSM9ValidateArgsDeEncodingWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM9ValidateArgsOutputDeEncodingLabel.sizePolicy().hasHeightForWidth()
        )
        self.MCSM9ValidateArgsOutputDeEncodingLabel.setSizePolicy(sizePolicy)
        self.MCSM9ValidateArgsOutputDeEncodingLabel.setObjectName(
            "MCSM9ValidateArgsOutputDeEncodingLabel"
        )
        self.gridLayout_92.addWidget(
            self.MCSM9ValidateArgsOutputDeEncodingLabel, 2, 0, 1, 1
        )
        self.MCSM9ValidateArgsDeEncodingSubtitleLabel = SubtitleLabel(
            self.MCSM9ValidateArgsDeEncodingWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM9ValidateArgsDeEncodingSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.MCSM9ValidateArgsDeEncodingSubtitleLabel.setSizePolicy(sizePolicy)
        self.MCSM9ValidateArgsDeEncodingSubtitleLabel.setObjectName(
            "MCSM9ValidateArgsDeEncodingSubtitleLabel"
        )
        self.gridLayout_92.addWidget(
            self.MCSM9ValidateArgsDeEncodingSubtitleLabel, 0, 0, 1, 1
        )
        self.MCSM9ValidateArgsInputDeEncodingLabel = StrongBodyLabel(
            self.MCSM9ValidateArgsDeEncodingWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM9ValidateArgsInputDeEncodingLabel.sizePolicy().hasHeightForWidth()
        )
        self.MCSM9ValidateArgsInputDeEncodingLabel.setSizePolicy(sizePolicy)
        self.MCSM9ValidateArgsInputDeEncodingLabel.setObjectName(
            "MCSM9ValidateArgsInputDeEncodingLabel"
        )
        self.gridLayout_92.addWidget(
            self.MCSM9ValidateArgsInputDeEncodingLabel, 3, 0, 1, 1
        )
        self.gridLayout_90.addWidget(self.MCSM9ValidateArgsDeEncodingWidget, 8, 2, 1, 3)
        spacerItem99 = QSpacerItem(20, 102, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout_90.addItem(spacerItem99, 0, 0, 21, 1)
        self.MCSM9ValidateArgsJVMArgWidget = QWidget(self.MCSM9ValidateArgs)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM9ValidateArgsJVMArgWidget.sizePolicy().hasHeightForWidth()
        )
        self.MCSM9ValidateArgsJVMArgWidget.setSizePolicy(sizePolicy)
        self.MCSM9ValidateArgsJVMArgWidget.setMinimumSize(QSize(0, 140))
        self.MCSM9ValidateArgsJVMArgWidget.setMaximumSize(QSize(16777215, 140))
        self.MCSM9ValidateArgsJVMArgWidget.setObjectName(
            "MCSM9ValidateArgsJVMArgWidget"
        )
        self.gridLayout_93 = QGridLayout(self.MCSM9ValidateArgsJVMArgWidget)
        self.gridLayout_93.setObjectName("gridLayout_93")
        self.MCSM9ValidateArgsJVMArgPlainTextEdit = PlainTextEdit(
            self.MCSM9ValidateArgsJVMArgWidget
        )
        self.MCSM9ValidateArgsJVMArgPlainTextEdit.setObjectName(
            "MCSM9ValidateArgsJVMArgPlainTextEdit"
        )
        self.gridLayout_93.addWidget(
            self.MCSM9ValidateArgsJVMArgPlainTextEdit, 1, 0, 1, 1
        )
        self.MCSM9ValidateArgsJVMArgSubtitleLabel = SubtitleLabel(
            self.MCSM9ValidateArgsJVMArgWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM9ValidateArgsJVMArgSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.MCSM9ValidateArgsJVMArgSubtitleLabel.setSizePolicy(sizePolicy)
        self.MCSM9ValidateArgsJVMArgSubtitleLabel.setObjectName(
            "MCSM9ValidateArgsJVMArgSubtitleLabel"
        )
        self.gridLayout_93.addWidget(
            self.MCSM9ValidateArgsJVMArgSubtitleLabel, 0, 0, 1, 1
        )
        self.gridLayout_90.addWidget(self.MCSM9ValidateArgsJVMArgWidget, 9, 2, 1, 3)
        self.MCSM9ValidateArgsCoreWidget = QWidget(self.MCSM9ValidateArgs)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM9ValidateArgsCoreWidget.sizePolicy().hasHeightForWidth()
        )
        self.MCSM9ValidateArgsCoreWidget.setSizePolicy(sizePolicy)
        self.MCSM9ValidateArgsCoreWidget.setObjectName("MCSM9ValidateArgsCoreWidget")
        self.gridLayout_94 = QGridLayout(self.MCSM9ValidateArgsCoreWidget)
        self.gridLayout_94.setObjectName("gridLayout_94")
        self.MCSM9ValidateArgsDownloadCorePrimaryPushBtn = PrimaryPushButton(
            self.MCSM9ValidateArgsCoreWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM9ValidateArgsDownloadCorePrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.MCSM9ValidateArgsDownloadCorePrimaryPushBtn.setSizePolicy(sizePolicy)
        self.MCSM9ValidateArgsDownloadCorePrimaryPushBtn.setMinimumSize(QSize(90, 0))
        self.MCSM9ValidateArgsDownloadCorePrimaryPushBtn.setObjectName(
            "MCSM9ValidateArgsDownloadCorePrimaryPushBtn"
        )
        self.gridLayout_94.addWidget(
            self.MCSM9ValidateArgsDownloadCorePrimaryPushBtn, 1, 3, 1, 1
        )
        self.MCSM9ValidateArgsCoreSubtitleLabel = SubtitleLabel(
            self.MCSM9ValidateArgsCoreWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM9ValidateArgsCoreSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.MCSM9ValidateArgsCoreSubtitleLabel.setSizePolicy(sizePolicy)
        self.MCSM9ValidateArgsCoreSubtitleLabel.setObjectName(
            "MCSM9ValidateArgsCoreSubtitleLabel"
        )
        self.gridLayout_94.addWidget(
            self.MCSM9ValidateArgsCoreSubtitleLabel, 0, 1, 1, 1
        )
        self.MCSM9ValidateArgsCoreLineEdit = LineEdit(self.MCSM9ValidateArgsCoreWidget)
        self.MCSM9ValidateArgsCoreLineEdit.setObjectName(
            "MCSM9ValidateArgsCoreLineEdit"
        )
        self.gridLayout_94.addWidget(self.MCSM9ValidateArgsCoreLineEdit, 1, 1, 1, 1)
        self.MCSM9ValidateArgsManuallyAddCorePrimaryPushBtn = PrimaryPushButton(
            self.MCSM9ValidateArgsCoreWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM9ValidateArgsManuallyAddCorePrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.MCSM9ValidateArgsManuallyAddCorePrimaryPushBtn.setSizePolicy(sizePolicy)
        self.MCSM9ValidateArgsManuallyAddCorePrimaryPushBtn.setMinimumSize(QSize(90, 0))
        self.MCSM9ValidateArgsManuallyAddCorePrimaryPushBtn.setObjectName(
            "MCSM9ValidateArgsManuallyAddCorePrimaryPushBtn"
        )
        self.gridLayout_94.addWidget(
            self.MCSM9ValidateArgsManuallyAddCorePrimaryPushBtn, 1, 2, 1, 1
        )
        self.gridLayout_90.addWidget(self.MCSM9ValidateArgsCoreWidget, 7, 2, 1, 3)
        self.MCSM9ValidateArgsMemWidget = QWidget(self.MCSM9ValidateArgs)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM9ValidateArgsMemWidget.sizePolicy().hasHeightForWidth()
        )
        self.MCSM9ValidateArgsMemWidget.setSizePolicy(sizePolicy)
        self.MCSM9ValidateArgsMemWidget.setMinimumSize(QSize(0, 85))
        self.MCSM9ValidateArgsMemWidget.setMaximumSize(QSize(16777215, 85))
        self.MCSM9ValidateArgsMemWidget.setObjectName("MCSM9ValidateArgsMemWidget")
        self.gridLayout_95 = QGridLayout(self.MCSM9ValidateArgsMemWidget)
        self.gridLayout_95.setObjectName("gridLayout_95")
        self.MCSM9ValidateArgsMinMemLineEdit = LineEdit(self.MCSM9ValidateArgsMemWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM9ValidateArgsMinMemLineEdit.sizePolicy().hasHeightForWidth()
        )
        self.MCSM9ValidateArgsMinMemLineEdit.setSizePolicy(sizePolicy)
        self.MCSM9ValidateArgsMinMemLineEdit.setMinimumSize(QSize(0, 30))
        self.MCSM9ValidateArgsMinMemLineEdit.setObjectName(
            "MCSM9ValidateArgsMinMemLineEdit"
        )
        self.gridLayout_95.addWidget(self.MCSM9ValidateArgsMinMemLineEdit, 1, 1, 1, 1)
        self.MCSM9ValidateArgsMemSubtitleLabel = SubtitleLabel(
            self.MCSM9ValidateArgsMemWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM9ValidateArgsMemSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.MCSM9ValidateArgsMemSubtitleLabel.setSizePolicy(sizePolicy)
        self.MCSM9ValidateArgsMemSubtitleLabel.setObjectName(
            "MCSM9ValidateArgsMemSubtitleLabel"
        )
        self.gridLayout_95.addWidget(self.MCSM9ValidateArgsMemSubtitleLabel, 0, 1, 1, 1)
        self.MCSM9ValidateArgsMaxMemLineEdit = LineEdit(self.MCSM9ValidateArgsMemWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM9ValidateArgsMaxMemLineEdit.sizePolicy().hasHeightForWidth()
        )
        self.MCSM9ValidateArgsMaxMemLineEdit.setSizePolicy(sizePolicy)
        self.MCSM9ValidateArgsMaxMemLineEdit.setMinimumSize(QSize(0, 30))
        self.MCSM9ValidateArgsMaxMemLineEdit.setObjectName(
            "MCSM9ValidateArgsMaxMemLineEdit"
        )
        self.gridLayout_95.addWidget(self.MCSM9ValidateArgsMaxMemLineEdit, 1, 3, 1, 1)
        self.MCSM9ValidateArgsToSymbol = SubtitleLabel(self.MCSM9ValidateArgsMemWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM9ValidateArgsToSymbol.sizePolicy().hasHeightForWidth()
        )
        self.MCSM9ValidateArgsToSymbol.setSizePolicy(sizePolicy)
        self.MCSM9ValidateArgsToSymbol.setObjectName("MCSM9ValidateArgsToSymbol")
        self.gridLayout_95.addWidget(self.MCSM9ValidateArgsToSymbol, 1, 2, 1, 1)
        spacerItem100 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_95.addItem(spacerItem100, 1, 5, 1, 1)
        self.MCSM9ValidateArgsMemUnitComboBox = ComboBox(
            self.MCSM9ValidateArgsMemWidget
        )
        self.MCSM9ValidateArgsMemUnitComboBox.setObjectName(
            "MCSM9ValidateArgsMemUnitComboBox"
        )
        self.gridLayout_95.addWidget(self.MCSM9ValidateArgsMemUnitComboBox, 1, 4, 1, 1)
        self.gridLayout_90.addWidget(self.MCSM9ValidateArgsMemWidget, 6, 2, 1, 3)
        self.MCSM9ValidateArgsTitle = SubtitleLabel(self.MCSM9ValidateArgs)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM9ValidateArgsTitle.sizePolicy().hasHeightForWidth()
        )
        self.MCSM9ValidateArgsTitle.setSizePolicy(sizePolicy)
        self.MCSM9ValidateArgsTitle.setObjectName("MCSM9ValidateArgsTitle")
        self.gridLayout_90.addWidget(self.MCSM9ValidateArgsTitle, 0, 3, 1, 1)
        self.MCSM9ValidateArgsStatus = PixmapLabel(self.MCSM9ValidateArgs)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM9ValidateArgsStatus.sizePolicy().hasHeightForWidth()
        )
        self.MCSM9ValidateArgsStatus.setSizePolicy(sizePolicy)
        self.MCSM9ValidateArgsStatus.setMinimumSize(QSize(30, 30))
        self.MCSM9ValidateArgsStatus.setMaximumSize(QSize(30, 30))
        self.MCSM9ValidateArgsStatus.setObjectName("MCSM9ValidateArgsStatus")
        self.gridLayout_90.addWidget(self.MCSM9ValidateArgsStatus, 0, 2, 1, 1)
        self.verticalLayout_12.addWidget(self.MCSM9ValidateArgs)
        self.MCSM9Save = CardWidget(self.MCSM9ScrollAreaWidgetContents)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.MCSM9Save.sizePolicy().hasHeightForWidth())
        self.MCSM9Save.setSizePolicy(sizePolicy)
        self.MCSM9Save.setMinimumSize(QSize(0, 125))
        self.MCSM9Save.setMaximumSize(QSize(16777215, 125))
        self.MCSM9Save.setObjectName("MCSM9Save")
        self.gridLayout_96 = QGridLayout(self.MCSM9Save)
        self.gridLayout_96.setObjectName("gridLayout_96")
        self.MCSM9SaveTitle = SubtitleLabel(self.MCSM9Save)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM9SaveTitle.sizePolicy().hasHeightForWidth()
        )
        self.MCSM9SaveTitle.setSizePolicy(sizePolicy)
        self.MCSM9SaveTitle.setObjectName("MCSM9SaveTitle")
        self.gridLayout_96.addWidget(self.MCSM9SaveTitle, 0, 1, 1, 1)
        self.MCSM9SaveServerNameLineEdit = LineEdit(self.MCSM9Save)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM9SaveServerNameLineEdit.sizePolicy().hasHeightForWidth()
        )
        self.MCSM9SaveServerNameLineEdit.setSizePolicy(sizePolicy)
        self.MCSM9SaveServerNameLineEdit.setMinimumSize(QSize(0, 30))
        self.MCSM9SaveServerNameLineEdit.setObjectName("MCSM9SaveServerNameLineEdit")
        self.gridLayout_96.addWidget(self.MCSM9SaveServerNameLineEdit, 1, 1, 1, 1)
        spacerItem101 = QSpacerItem(20, 79, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout_96.addItem(spacerItem101, 0, 0, 3, 1)
        self.MCSM9SaveServerPrimaryPushBtn = PrimaryPushButton(self.MCSM9Save)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM9SaveServerPrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.MCSM9SaveServerPrimaryPushBtn.setSizePolicy(sizePolicy)
        self.MCSM9SaveServerPrimaryPushBtn.setMinimumSize(QSize(130, 30))
        self.MCSM9SaveServerPrimaryPushBtn.setMaximumSize(QSize(16777215, 30))
        self.MCSM9SaveServerPrimaryPushBtn.setObjectName(
            "MCSM9SaveServerPrimaryPushBtn"
        )
        self.gridLayout_96.addWidget(self.MCSM9SaveServerPrimaryPushBtn, 2, 1, 1, 1)
        self.verticalLayout_12.addWidget(self.MCSM9Save)
        self.MCSM9ScrollArea.setWidget(self.MCSM9ScrollAreaWidgetContents)
        self.gridLayout_97.addWidget(self.MCSM9ScrollArea, 1, 3, 1, 2)
        self.MCSM9BackToMain = TransparentToolButton(FIF.PAGE_LEFT, self.MCSM9)
        self.MCSM9BackToMain.setObjectName("MCSM9BackToMain")
        self.gridLayout_97.addWidget(self.MCSM9BackToMain, 0, 2, 1, 1)
        spacerItem102 = QSpacerItem(373, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_97.addItem(spacerItem102, 0, 4, 1, 1)
        self.MCSM9Title = SubtitleLabel(self.MCSM9)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.MCSM9Title.sizePolicy().hasHeightForWidth())
        self.MCSM9Title.setSizePolicy(sizePolicy)
        self.MCSM9Title.setObjectName("MCSM9Title")
        self.gridLayout_97.addWidget(self.MCSM9Title, 0, 3, 1, 1)
        spacerItem103 = QSpacerItem(20, 335, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout_97.addItem(spacerItem103, 0, 1, 2, 1)
        self.importNewServerStackWidget.addWidget(self.MCSM9)
        self.gridLayout_21.addWidget(self.importNewServerStackWidget, 1, 1, 1, 1)
        self.newServerStackedWidget.addWidget(self.importNewServerPage)
        self.gridLayout.addWidget(self.newServerStackedWidget, 2, 2, 1, 1)

        self.setObjectName("ConfigureInterface")

        self.importNewServerStackWidget.setCurrentIndex(0)

        self.noobNewServerScrollArea.setAttribute(Qt.WA_StyledBackground)
        self.extendedNewServerScrollArea.setAttribute(Qt.WA_StyledBackground)

        # 引导页
        self.titleLabel.setText("新建服务器")
        self.subTitleLabel.setText("有3种方式供你选择。")
        self.noobNewServerBtn.setText("简易模式")
        self.noobNewServerIntro.setText(
            "保留基础配置。\n" " - Java\n" " - 服务器核心\n" " - 最小最大内存\n" " - 服务器名称"
        )
        self.extendedNewServerBtn.setText("进阶模式")
        self.extendedNewServerIntro.setText(
            "在简易模式基础上\n" "，\n" "还能设置：\n" " - 内存单位\n" " - 控制台流编码\n" " - JVM参数"
        )
        self.importNewServerBtn.setText("导入")
        self.importNewServerIntro.setText("暂未完成。")

        # 简易模式
        self.noobJavaSubtitleLabel.setText("Java:")
        self.noobJavaInfoLabel.setText("[选择的Java的信息]")
        self.noobDownloadJavaPrimaryPushBtn.setText("下载Java")
        self.noobManuallyAddJavaPrimaryPushBtn.setText("手动导入")
        self.noobAutoDetectJavaPrimaryPushBtn.setText("自动查找Java")
        self.noobJavaListPushBtn.setText("Java列表")
        self.noobMemUnitLabel.setText("M")
        self.noobToSymbol.setText("~")
        self.noobMemSubtitleLabel.setText("内存:")
        self.noobDownloadCorePrimaryPushBtn.setText("下载核心")
        self.noobManuallyAddCorePrimaryPushBtn.setText("手动导入")
        self.noobCoreSubtitleLabel.setText("核心：")
        self.noobServerNameSubtitleLabel.setText("服务器名称：")
        self.noobSaveServerPrimaryPushBtn.setText("保存！")
        self.noobSubtitleLabel.setText("简易模式")
        self.noobMinMemLineEdit.setPlaceholderText("整数")
        self.noobMaxMemLineEdit.setPlaceholderText("整数")
        self.noobServerNameLineEdit.setPlaceholderText("不能包含非法字符")

        # 进阶模式
        self.extendedSubtitleLabel.setText("进阶模式")
        self.extendedJavaSubtitleLabel.setText("Java:")
        self.extendedJavaInfoLabel.setText("[选择的Java的信息]")
        self.extendedDownloadJavaPrimaryPushBtn.setText("下载Java")
        self.extendedManuallyAddJavaPrimaryPushBtn.setText("手动导入")
        self.extendedAutoDetectJavaPrimaryPushBtn.setText("自动查找Java")
        self.extendedJavaListPushBtn.setText("Java列表")
        self.extendedMemSubtitleLabel.setText("内存:")
        self.extendedToSymbol.setText("~")
        self.extendedDownloadCorePrimaryPushBtn.setText("下载核心")
        self.extendedManuallyAddCorePrimaryPushBtn.setText("手动导入")
        self.extendedCoreSubtitleLabel.setText("核心：")
        self.extendedDeEncodingSubtitleLabel.setText("编码设置：")
        self.extendedOutputDeEncodingLabel.setText("控制台输出编码（优先级高于全局设置）")
        self.extendedInputDeEncodingLabel.setText("指令输入编码（优先级高于全局设置）")
        self.extendedJVMArgSubtitleLabel.setText("JVM参数：")
        self.JVMArgPlainTextEdit.setPlaceholderText("可选，用一个空格分组")
        self.extendedServerNameSubtitleLabel.setText("服务器名称：")
        self.extendedSaveServerPrimaryPushBtn.setText("保存！")
        self.extendedMinMemLineEdit.setPlaceholderText("整数")
        self.extendedMaxMemLineEdit.setPlaceholderText("整数")
        self.extendedServerNameLineEdit.setPlaceholderText("不能包含非法字符")
        self.extendedOutputDeEncodingComboBox.addItems(
            ["跟随全局", "UTF-8", "GB18030", "ANSI(推荐)"]
        )
        self.extendedOutputDeEncodingComboBox.setCurrentIndex(0)
        self.extendedInputDeEncodingComboBox.addItems(
            ["跟随全局", "UTF-8", "GB18030", "ANSI(推荐)"]
        )
        self.extendedInputDeEncodingComboBox.setCurrentIndex(0)
        self.extendedMemUnitComboBox.addItems(["M", "G"])
        self.extendedMemUnitComboBox.setCurrentIndex(0)

        # 导入
        self.importSubtitleLabel.setText("导入")
        self.importNewServerFirstGuideTitle.setText("  请选择导入服务器的方式：")
        self.noShellArchivesTitle.setText("导入 不含开服脚本的 完整的 服务器 压缩包/文件夹")
        self.noShellArchivesImportStatusText.setText("[状态文本]")
        self.noShellArchivesImportArchives.setText("导入文件")
        self.noShellArchivesImportFolder.setText("导入文件夹")
        self.noShellArchivesImportTitle.setText("1. 导入文件/文件夹")
        self.noShellArchivesSelectCoreStatusText.setText("[状态文本]")
        self.noShellArchivesSelectCoreTitle.setText("2.选择核心")
        self.noShellArchivesJVMArgPlainTextEdit.setPlaceholderText("可选，用一个空格分组")
        self.noShellArchivesJVMArgSubtitleLabel.setText("JVM参数：")
        self.noShellArchivesSetArgsTitle.setText("3. 设置参数")
        self.noShellArchivesDownloadJavaPrimaryPushBtn.setText("下载Java")
        self.noShellArchivesManuallyAddJavaPrimaryPushBtn.setText("手动导入")
        self.noShellArchivesAutoDetectJavaPrimaryPushBtn.setText("自动查找Java")
        self.noShellArchivesJavaListPushBtn.setText("Java列表")
        self.noShellArchivesJavaInfoLabel.setText("[选择的Java的信息]")
        self.noShellArchivesJavaSubtitleLabel.setText("Java:")
        self.noShellArchivesOutputDeEncodingLabel.setText("控制台输出编码（优先级高于全局设置）")
        self.noShellArchivesDeEncodingSubtitleLabel.setText("编码设置：")
        self.noShellArchivesInputDeEncodingLabel.setText("指令输入编码（优先级高于全局设置）")
        self.noShellArchivesMemSubtitleLabel.setText("内存:")
        self.noShellArchivesToSymbol.setText("~")
        self.noShellArchivesSaveTitle.setText("4. 完成导入")
        self.noShellArchivesSaveServerNameLineEdit.setPlaceholderText(
            "设置服务器昵称，不能包含非法字符"
        )
        self.noShellArchivesSaveSaveServerPrimaryPushBtn.setText("导入！")
        self.shellArchivesTitle.setText("导入 含开服脚本的 完整的 服务器 压缩包/文件夹")
        self.shellArchivesImportStatusText.setText("[状态文本]")
        self.shellArchivesImportArchives.setText("导入文件")
        self.shellArchivesImportFolder.setText("导入文件夹")
        self.shellArchivesImportTitle.setText("1. 导入文件/文件夹")
        self.shellArchivesSelectShellStatusText.setText("[状态文本]")
        self.shellArchivesSelectShellTitle.setText("2.选择开服脚本")
        self.shellArchivesValidateArgsAutoDetectJavaPrimaryPushBtn.setText("自动查找Java")
        self.shellArchivesValidateArgsJavaSubtitleLabel.setText("Java:")
        self.shellArchivesValidateArgsJavaListPushBtn.setText("Java列表")
        self.shellArchivesValidateArgsManuallyAddJavaPrimaryPushBtn.setText("手动导入")
        self.shellArchivesValidateArgsDownloadJavaPrimaryPushBtn.setText("下载Java")
        self.shellArchivesValidateArgsOutputDeEncodingLabel.setText(
            "控制台输出编码（优先级高于全局设置）"
        )
        self.shellArchivesValidateArgsDeEncodingSubtitleLabel.setText("编码设置：")
        self.shellArchivesValidateArgsInputDeEncodingLabel.setText("指令输入编码（优先级高于全局设置）")
        self.shellArchivesValidateArgsJVMArgPlainTextEdit.setPlaceholderText(
            "可选，用一个空格分组"
        )
        self.shellArchivesValidateArgsJVMArgSubtitleLabel.setText("JVM参数：")
        self.shellArchivesValidateArgsMemSubtitleLabel.setText("内存:")
        self.shellArchivesValidateArgsToSymbol.setText("~")
        self.shellArchivesValidateArgsTitle.setText("3. 确认参数")
        self.shellArchivesValidateArgsDownloadCorePrimaryPushBtn.setText("下载核心")
        self.shellArchivesValidateArgsCoreSubtitleLabel.setText("核心：")
        self.shellArchivesValidateArgsManuallyAddCorePrimaryPushBtn.setText("重新导入")
        self.shellArchivesSaveTitle.setText("4. 完成导入")
        self.shellArchivesSaveServerNameLineEdit.setPlaceholderText("设置服务器昵称，不能包含非法字符")
        self.shellArchivesSaveSaveServerPrimaryPushBtn.setText("导入！")
        self.serverArchiveSiteImportStatusText.setText("[状态文本]")
        self.serverArchiveSiteImportArchives.setText("导入文件")
        self.serverArchiveSiteImportFolder.setText("导入文件夹")
        self.serverArchiveSiteImportTitle.setText("1. 导入文件/文件夹")
        self.serverArchiveSiteAutoDetectJavaPrimaryPushBtn.setText("自动查找Java")
        self.serverArchiveSiteJavaSubtitleLabel.setText("Java:")
        self.serverArchiveSiteJavaListPushBtn.setText("Java列表")
        self.serverArchiveSiteManuallyAddJavaPrimaryPushBtn.setText("手动导入")
        self.serverArchiveSiteDownloadJavaPrimaryPushBtn.setText("下载Java")
        self.serverArchiveSiteOutputDeEncodingLabel.setText("控制台输出编码（优先级高于全局设置）")
        self.serverArchiveSiteDeEncodingSubtitleLabel.setText("编码设置：")
        self.serverArchiveSiteInputDeEncodingLabel.setText("指令输入编码（优先级高于全局设置）")
        self.serverArchiveSiteJVMArgPlainTextEdit.setPlaceholderText("可选，用一个空格分组")
        self.serverArchiveSiteJVMArgSubtitleLabel.setText("JVM参数：")
        self.serverArchiveSiteMemSubtitleLabel.setText("内存:")
        self.serverArchiveSiteToSymbol.setText("~")
        self.serverArchiveSiteSetArgsTitle.setText("2. 设置参数")
        self.serverArchiveSiteDownloadCorePrimaryPushBtn.setText("下载核心")
        self.serverArchiveSiteCoreSubtitleLabel.setText("核心：")
        self.serverArchiveSiteManuallyAddCorePrimaryPushBtn.setText("重新导入")
        self.serverArchiveSiteSaveTitle.setText("4. 完成导入")
        self.serverArchiveSiteServerNameLineEdit.setPlaceholderText("设置服务器昵称，不能包含非法字符")
        self.serverArchiveSiteSaveServerPrimaryPushBtn.setText("导入！")
        self.serverArchiveSiteTitle.setText("导入 服务器 存档 压缩包/文件夹")
        self.MCSLv1Title.setText("导入 MCSL 1的服务器")
        self.MCSLv1ImportStatusText.setText("[状态文本]")
        self.MCSLv1ImportTitle.setText("1. 选择MCSL 1主程序")
        self.MCSLv1ImportArchives.setText("选择主程序")
        self.MCSLv1ValidateArgsAutoDetectJavaPrimaryPushBtn.setText("自动查找Java")
        self.MCSLv1ValidateArgsJavaSubtitleLabel.setText("Java:")
        self.MCSLv1ValidateArgsJavaListPushBtn.setText("Java列表")
        self.MCSLv1ValidateArgsManuallyAddJavaPrimaryPushBtn.setText("手动导入")
        self.MCSLv1ValidateArgsDownloadJavaPrimaryPushBtn.setText("下载Java")
        self.MCSLv1ValidateArgsOutputDeEncodingLabel.setText("控制台输出编码（优先级高于全局设置）")
        self.MCSLv1ValidateArgsDeEncodingSubtitleLabel.setText("编码设置：")
        self.MCSLv1ValidateArgsInputDeEncodingLabel.setText("指令输入编码（优先级高于全局设置）")
        self.MCSLv1ValidateArgsJVMArgPlainTextEdit.setPlaceholderText("可选，用一个空格分组")
        self.MCSLv1ValidateArgsJVMArgSubtitleLabel.setText("JVM参数：")
        self.MCSLv1ValidateArgsMemSubtitleLabel.setText("内存:")
        self.MCSLv1ValidateArgsToSymbol.setText("~")
        self.MCSLv1ValidateArgsTitle.setText("2. 确认参数")
        self.MCSLv1ValidateArgsDownloadCorePrimaryPushBtn.setText("下载核心")
        self.MCSLv1ValidateArgsCoreSubtitleLabel.setText("核心：")
        self.MCSLv1ValidateArgsManuallyAddCorePrimaryPushBtn.setText("重新导入")
        self.MCSLv1SaveTitle.setText("3. 完成导入")
        self.MCSLv1SaveServerNameLineEdit.setPlaceholderText("设置服务器昵称，不能包含非法字符")
        self.MCSLv1SaveServerPrimaryPushBtn.setText("导入！")
        self.MCSLv2Title.setText("导入 MCSL 2的服务器")
        self.MCSLv2ImportStatusText.setText("[状态文本]")
        self.MCSLv2ImportTitle.setText("1. 选择MCSL 2生成的MCSL2ServerConfig.json")
        self.MCSLv2ImportArchives.setText("选择配置文件")
        self.MCSLv2ValidateArgsAutoDetectJavaPrimaryPushBtn.setText("自动查找Java")
        self.MCSLv2ValidateArgsJavaSubtitleLabel.setText("Java:")
        self.MCSLv2ValidateArgsJavaListPushBtn.setText("Java列表")
        self.MCSLv2ValidateArgsManuallyAddJavaPrimaryPushBtn.setText("手动导入")
        self.MCSLv2ValidateArgsDownloadJavaPrimaryPushBtn.setText("下载Java")
        self.MCSLv2ValidateArgsOutputDeEncodingLabel.setText("控制台输出编码（优先级高于全局设置）")
        self.MCSLv2ValidateArgsDeEncodingSubtitleLabel.setText("编码设置：")
        self.MCSLv2ValidateArgsInputDeEncodingLabel.setText("指令输入编码（优先级高于全局设置）")
        self.MCSLv2ValidateArgsJVMArgPlainTextEdit.setPlaceholderText("可选，用一个空格分组")
        self.MCSLv2ValidateArgsJVMArgSubtitleLabel.setText("JVM参数：")
        self.MCSLv2ValidateArgsMemSubtitleLabel.setText("内存:")
        self.MCSLv2ValidateArgsToSymbol.setText("~")
        self.MCSLv2ValidateArgsTitle.setText("2. 确认参数")
        self.MCSLv2ValidateArgsDownloadCorePrimaryPushBtn.setText("下载核心")
        self.MCSLv2ValidateArgsCoreSubtitleLabel.setText("核心：")
        self.MCSLv2ValidateArgsManuallyAddCorePrimaryPushBtn.setText("重新导入")
        self.MCSLv2SaveTitle.setText("3. 完成导入")
        self.MCSLv2SaveServerNameLineEdit.setPlaceholderText("设置服务器昵称，不能包含非法字符")
        self.MCSLv2SaveServerPrimaryPushBtn.setText("导入！")
        self.MSL3Title.setText("导入 MSL 的服务器")
        self.MSL3ImportTitle.setText("1. 选择MSL文件夹中的ServerList.json")
        self.MSL3ImportStatusText.setText("[状态文本]")
        self.MSL3ImportArchives.setText("选择配置文件")
        self.MSL3SelectServerStatusText.setText("[状态文本]")
        self.MSL3SelectServerTitle.setText("2.选择需要导入的服务器")
        self.MSL3ValidateArgsJavaListPushBtn.setText("Java列表")
        self.MSL3ValidateArgsAutoDetectJavaPrimaryPushBtn.setText("自动查找Java")
        self.MSL3ValidateArgsManuallyAddJavaPrimaryPushBtn.setText("手动导入")
        self.MSL3ValidateArgsDownloadJavaPrimaryPushBtn.setText("下载Java")
        self.MSL3ValidateArgsJavaSubtitleLabel.setText("Java:")
        self.MSL3ValidateArgsOutputDeEncodingLabel.setText("控制台输出编码（优先级高于全局设置）")
        self.MSL3ValidateArgsDeEncodingSubtitleLabel.setText("编码设置：")
        self.MSL3ValidateArgsInputDeEncodingLabel.setText("指令输入编码（优先级高于全局设置）")
        self.MSL3ValidateArgsJVMArgPlainTextEdit.setPlaceholderText("可选，用一个空格分组")
        self.MSL3ValidateArgsJVMArgSubtitleLabel.setText("JVM参数：")
        self.MSL3ValidateArgsDownloadCorePrimaryPushBtn.setText("下载核心")
        self.MSL3ValidateArgsCoreSubtitleLabel.setText("核心：")
        self.MSL3ValidateArgsManuallyAddCorePrimaryPushBtn.setText("重新导入")
        self.MSL3ValidateArgsMemSubtitleLabel.setText("内存:")
        self.MSL3ValidateArgsToSymbol.setText("~")
        self.MSL3ValidateArgsTitle.setText("3. 确认参数")
        self.MSL3SaveTitle.setText("4. 完成导入")
        self.MSL3SaveServerNameLineEdit.setPlaceholderText("设置服务器昵称，不能包含非法字符")
        self.MSL3SaveServerPrimaryPushBtn.setText("导入！")
        self.NullCraftImportTitle.setText("1. 选择灵工艺开服器主程序")
        self.NullCraftImportStatusText.setText("[状态文本]")
        self.NullCraftImportArchives.setText("选择主程序")
        self.NullCraftValidateArgsJavaListPushBtn.setText("Java列表")
        self.NullCraftValidateArgsAutoDetectJavaPrimaryPushBtn.setText("自动查找Java")
        self.NullCraftValidateArgsManuallyAddJavaPrimaryPushBtn.setText("手动导入")
        self.NullCraftValidateArgsDownloadJavaPrimaryPushBtn.setText("下载Java")
        self.NullCraftValidateArgsJavaSubtitleLabel.setText("Java:")
        self.NullCraftValidateArgsOutputDeEncodingLabel.setText("控制台输出编码（优先级高于全局设置）")
        self.NullCraftValidateArgsDeEncodingSubtitleLabel.setText("编码设置：")
        self.NullCraftValidateArgsInputDeEncodingLabel.setText("指令输入编码（优先级高于全局设置）")
        self.NullCraftValidateArgsJVMArgPlainTextEdit.setPlaceholderText("可选，用一个空格分组")
        self.NullCraftValidateArgsJVMArgSubtitleLabel.setText("JVM参数：")
        self.NullCraftValidateArgsDownloadCorePrimaryPushBtn.setText("下载核心")
        self.NullCraftValidateArgsCoreSubtitleLabel.setText("核心：")
        self.NullCraftValidateArgsManuallyAddCorePrimaryPushBtn.setText("重新导入")
        self.NullCraftValidateArgsMemSubtitleLabel.setText("内存:")
        self.NullCraftValidateArgsToSymbol.setText("~")
        self.NullCraftValidateArgsTitle.setText("2. 确认参数")
        self.NullCraftSaveTitle.setText("3. 完成导入")
        self.NullCraftSaveServerNameLineEdit.setPlaceholderText("设置服务器昵称，不能包含非法字符")
        self.NullCraftSaveServerPrimaryPushBtn.setText("导入！")
        self.NullCraftTitle.setText("导入 灵工艺我的世界「轻」开服器 的服务器")
        self.MCSM8Title.setText("导入 MCSManager 8 的服务器")
        self.MCSM8ImportTitle.setText("1. 选择 MCSM8 运行目录")
        self.MCSM8ImportStatusText.setText("[状态文本]")
        self.MCSM8ImportArchives.setText("选择文件夹")
        self.MCSM8SelectServerStatusText.setText("[状态文本]")
        self.MCSM8SelectServerTitle.setText("2.选择需要导入的服务器")
        self.MCSM8ValidateArgsJavaListPushBtn.setText("Java列表")
        self.MCSM8ValidateArgsAutoDetectJavaPrimaryPushBtn.setText("自动查找Java")
        self.MCSM8ValidateArgsManuallyAddJavaPrimaryPushBtn.setText("手动导入")
        self.MCSM8ValidateArgsDownloadJavaPrimaryPushBtn.setText("下载Java")
        self.MCSM8ValidateArgsJavaSubtitleLabel.setText("Java:")
        self.MCSM8ValidateArgsOutputDeEncodingLabel.setText("控制台输出编码（优先级高于全局设置）")
        self.MCSM8ValidateArgsDeEncodingSubtitleLabel.setText("编码设置：")
        self.MCSM8ValidateArgsInputDeEncodingLabel.setText("指令输入编码（优先级高于全局设置）")
        self.MCSM8ValidateArgsJVMArgPlainTextEdit.setPlaceholderText("可选，用一个空格分组")
        self.MCSM8ValidateArgsJVMArgSubtitleLabel.setText("JVM参数：")
        self.MCSM8ValidateArgsDownloadCorePrimaryPushBtn.setText("下载核心")
        self.MCSM8ValidateArgsCoreSubtitleLabel.setText("核心：")
        self.MCSM8ValidateArgsManuallyAddCorePrimaryPushBtn.setText("重新导入")
        self.MCSM8ValidateArgsMemSubtitleLabel.setText("内存:")
        self.MCSM8ValidateArgsToSymbol.setText("~")
        self.MCSM8ValidateArgsTitle.setText("3. 确认参数")
        self.MCSM8SaveTitle.setText("4. 完成导入")
        self.MCSM8SaveServerNameLineEdit.setPlaceholderText("设置服务器昵称，不能包含非法字符")
        self.MCSM8SaveServerPrimaryPushBtn.setText("导入！")
        self.MCSM9ImportTitle.setText("1. 选择 MCSM9守护进程运行目录daemon")
        self.MCSM9ImportStatusText.setText("[状态文本]")
        self.MCSM9ImportArchives.setText("选择文件夹")
        self.MCSM9SelectServerStatusText.setText("[状态文本]")
        self.MCSM9SelectServerTitle.setText("2.选择需要导入的服务器")
        self.MCSM9ValidateArgsJavaListPushBtn.setText("Java列表")
        self.MCSM9ValidateArgsAutoDetectJavaPrimaryPushBtn.setText("自动查找Java")
        self.MCSM9ValidateArgsManuallyAddJavaPrimaryPushBtn.setText("手动导入")
        self.MCSM9ValidateArgsDownloadJavaPrimaryPushBtn.setText("下载Java")
        self.MCSM9ValidateArgsJavaSubtitleLabel.setText("Java:")
        self.MCSM9ValidateArgsOutputDeEncodingLabel.setText("控制台输出编码（优先级高于全局设置）")
        self.MCSM9ValidateArgsDeEncodingSubtitleLabel.setText("编码设置：")
        self.MCSM9ValidateArgsInputDeEncodingLabel.setText("指令输入编码（优先级高于全局设置）")
        self.MCSM9ValidateArgsJVMArgPlainTextEdit.setPlaceholderText("可选，用一个空格分组")
        self.MCSM9ValidateArgsJVMArgSubtitleLabel.setText("JVM参数：")
        self.MCSM9ValidateArgsDownloadCorePrimaryPushBtn.setText("下载核心")
        self.MCSM9ValidateArgsCoreSubtitleLabel.setText("核心：")
        self.MCSM9ValidateArgsManuallyAddCorePrimaryPushBtn.setText("重新导入")
        self.MCSM9ValidateArgsMemSubtitleLabel.setText("内存:")
        self.MCSM9ValidateArgsToSymbol.setText("~")
        self.MCSM9ValidateArgsTitle.setText("3. 确认参数")
        self.MCSM9SaveTitle.setText("4. 完成导入")
        self.MCSM9SaveServerNameLineEdit.setPlaceholderText("设置服务器昵称，不能包含非法字符")
        self.MCSM9SaveServerPrimaryPushBtn.setText("导入！")
        self.MCSM9Title.setText("导入 MCSManager 9 的服务器")
        self.importNewServerTypeComboBox.addItems(
            [
                "选择一项",
                "导入 不含开服脚本的 完整的 服务器",
                "导入 含开服脚本的 完整的 服务器",
                "导入 服务器 存档(没有开服脚本、没有服务器核心)",
                "导入 MCSL 1 的服务器",
                "导入 MCSL 2 的服务器",
                "导入 MSL 的服务器",
                "导入 灵工艺我的世界「轻」开服器 的服务器",
                "导入 MCSManager 8 的服务器",
                "导入 MCSManager 9 的服务器",
            ]
        )

        # 引导页绑定
        self.noobNewServerBtn.clicked.connect(self.newServerStackedWidgetNavigation)
        self.extendedNewServerBtn.clicked.connect(self.newServerStackedWidgetNavigation)
        self.importNewServerBtn.clicked.connect(self.newServerStackedWidgetNavigation)

        # 简易模式绑定
        self.noobBackToGuidePushButton.clicked.connect(
            lambda: self.newServerStackedWidget.setCurrentIndex(0)
        )
        self.noobDownloadJavaPrimaryPushBtn.clicked.connect(
            lambda: InfoBar.info(
                title="切换到MCSLAPI",
                content="因为FastMirror没有Java啊 (",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self.parent(),
            )
        )
        self.extendedDownloadJavaPrimaryPushBtn.clicked.connect(
            lambda: InfoBar.info(
                title="切换到MCSLAPI",
                content="因为FastMirror没有Java啊 (",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self,
            )
        )
        self.noobManuallyAddJavaPrimaryPushBtn.clicked.connect(self.addJavaManually)
        self.noobAutoDetectJavaPrimaryPushBtn.clicked.connect(self.autoDetectJava)
        self.noobManuallyAddCorePrimaryPushBtn.clicked.connect(self.addCoreManually)
        self.noobSaveServerPrimaryPushBtn.clicked.connect(self.finishNewServer)

        # 进阶模式绑定
        self.extendedBackToGuidePushButton.clicked.connect(
            lambda: self.newServerStackedWidget.setCurrentIndex(0)
        )
        self.extendedManuallyAddJavaPrimaryPushBtn.clicked.connect(self.addJavaManually)
        self.extendedAutoDetectJavaPrimaryPushBtn.clicked.connect(self.autoDetectJava)
        self.extendedManuallyAddCorePrimaryPushBtn.clicked.connect(self.addCoreManually)
        self.extendedSaveServerPrimaryPushBtn.clicked.connect(self.finishNewServer)

        # 导入法绑定
        self.importBackToGuidePushButton.clicked.connect(
            lambda: self.newServerStackedWidget.setCurrentIndex(0)
        )
        self.goBtn.clicked.connect(
            lambda: self.importNewServerStackWidget.setCurrentIndex(
                self.importNewServerTypeComboBox.currentIndex()
            )
        )

        self.noobNewServerScrollArea.viewport().setStyleSheet(
            GlobalMCSL2Variables.scrollAreaViewportQss
        )
        self.extendedNewServerScrollArea.viewport().setStyleSheet(
            GlobalMCSL2Variables.scrollAreaViewportQss
        )
        self.noShellArchivesScrollArea.viewport().setStyleSheet(
            GlobalMCSL2Variables.scrollAreaViewportQss
        )
        self.shellArchivesScrollArea.viewport().setStyleSheet(
            GlobalMCSL2Variables.scrollAreaViewportQss
        )
        self.serverArchiveSiteScrollArea.viewport().setStyleSheet(
            GlobalMCSL2Variables.scrollAreaViewportQss
        )
        self.MCSLv1ScrollArea.viewport().setStyleSheet(
            GlobalMCSL2Variables.scrollAreaViewportQss
        )
        self.MCSLv2ScrollArea.viewport().setStyleSheet(
            GlobalMCSL2Variables.scrollAreaViewportQss
        )
        self.MSL3ScrollArea.viewport().setStyleSheet(
            GlobalMCSL2Variables.scrollAreaViewportQss
        )
        self.NullCraftScrollArea.viewport().setStyleSheet(
            GlobalMCSL2Variables.scrollAreaViewportQss
        )
        self.MCSM8ScrollArea.viewport().setStyleSheet(
            GlobalMCSL2Variables.scrollAreaViewportQss
        )
        self.MCSM9ScrollArea.viewport().setStyleSheet(
            GlobalMCSL2Variables.scrollAreaViewportQss
        )

        self.settingsRunner_newServerType()
        self.importNewServerBtn.setEnabled(False)

    def settingsRunner_newServerType(self):
        self.newServerStackedWidget.setCurrentIndex(
            settingsVariables.newServerTypeList.index(
                settingsController.fileSettings["newServerType"]
            )
        )

    def newServerStackedWidgetNavigation(self):
        """决定新建服务器的方式"""
        naviList = [
            "PlaceHolder",
            self.noobNewServerBtn,
            self.extendedNewServerBtn,
            self.importNewServerBtn,
        ]
        self.newServerStackedWidget.setCurrentIndex(naviList.index(self.sender()))

    def addJavaManually(self):
        """手动添加Java"""
        selectedJavaPath = str(
            QFileDialog.getOpenFileName(self, "选择java.exe程序", getcwd(), "java.exe")[0]
        )
        if selectedJavaPath != "":
            selectedJavaPath = selectedJavaPath.replace("/", "\\")
            if v := javaDetector.getJavaVersion(selectedJavaPath):
                currentJavaPaths = configureServerVariables.javaPath
                if (
                    java := javaDetector.Java(selectedJavaPath, v)
                ) not in currentJavaPaths:
                    currentJavaPaths.append(javaDetector.Java(selectedJavaPath, v))
                    javaDetector.sortJavaList(currentJavaPaths)
                    InfoBar.success(
                        title="已添加",
                        content=f"Java路径：{selectedJavaPath}\n版本：{v}\n但你还需要继续到Java列表中选取。",
                        orient=Qt.Horizontal,
                        isClosable=True,
                        position=InfoBarPosition.TOP,
                        duration=3000,
                        parent=self,
                    )
                else:
                    InfoBar.warning(
                        title="未添加",
                        content="此Java已被添加过，也有可能是自动查找Java时已经搜索到了。请检查Java列表。",
                        orient=Qt.Horizontal,
                        isClosable=True,
                        position=InfoBarPosition.TOP,
                        duration=4848,
                        parent=self,
                    )
                javaDetector.saveJavaList(currentJavaPaths)
            else:
                InfoBar.error(
                    title="添加失败",
                    content="此Java无效！",
                    orient=Qt.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=3000,
                    parent=self,
                )
        else:
            InfoBar.warning(
                title="未添加",
                content="你并没有选择Java。",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self,
            )

    def autoDetectJava(self):
        """自动查找Java"""
        # 防止同时多次运行worker线程
        self.noobAutoDetectJavaPrimaryPushBtn.setEnabled(False)
        self.extendedAutoDetectJavaPrimaryPushBtn.setEnabled(False)
        self.javaFindWorkThreadFactory.create().start()

    @pyqtSlot(list)
    def autoDetectJavaFinished(self, _JavaPaths: list):
        """自动查找Java结果处理"""
        if ospath.exists("MCSL2/AutoDetectJavaHistory.txt"):
            remove("MCSL2/AutoDetectJavaHistory.txt")
        if ospath.exists("MCSL2/AutoDetectJavaHistory.json"):
            remove("MCSL2/AutoDetectJavaHistory.json")

        savedJavaList = javaDetector.loadJavaList()
        invaildJavaList = []
        javaList = javaDetector.combineJavaList(
            savedJavaList, _JavaPaths, invaild=invaildJavaList
        )
        javaDetector.sortJavaList(javaList, reverse=False)
        configureServerVariables.javaPath = javaList
        javaDetector.saveJavaList(javaList)
        for java in invaildJavaList:
            InfoBar.error(
                title=f"Java: {java.version} 已失效",
                content=f"位于{java.path}的{java.version}已失效",
            )

    @pyqtSlot(int)
    def onJavaFindWorkThreadFinished(self, sequenceNumber):
        """自动查找Java结束后的处理"""
        if sequenceNumber > 1:
            InfoBar.success(
                title="查找完毕",
                content=f"一共搜索到了{len(configureServerVariables.javaPath)}个Java。\n请单击“Java列表”按钮查看、选择。",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self,
            )

        self.noobAutoDetectJavaPrimaryPushBtn.setEnabled(True)
        self.extendedAutoDetectJavaPrimaryPushBtn.setEnabled(True)

    def addCoreManually(self):
        """手动添加服务器核心"""
        tmpCorePath = str(
            QFileDialog.getOpenFileName(self, "选择*.jar文件", getcwd(), "*.jar")[0]
        ).replace("/", "\\")
        if tmpCorePath != "":
            configureServerVariables.corePath = tmpCorePath
            configureServerVariables.coreFileName = tmpCorePath.split("\\")[-1]
            InfoBar.success(
                title="已添加",
                content=f"核心文件名：{configureServerVariables.coreFileName}",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self,
            )
        else:
            InfoBar.warning(
                title="未添加",
                content="你并没有选择服务器核心。",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self,
            )

    def checkJavaSet(self):
        """检查Java设置"""
        if configureServerVariables.selectedJavaPath != "":
            return "Java检查: 正常", 0
        else:
            return "Java检查: 出错，缺失", 1

    def checkMemSet(self, currentNewServerType):
        """检查内存设置"""
        minMemLineEditItems = [
            None,
            self.noobMinMemLineEdit,
            self.extendedMinMemLineEdit,
        ]
        maxMemLineEditItems = [
            None,
            self.noobMaxMemLineEdit,
            self.extendedMaxMemLineEdit,
        ]

        # 是否为空
        if (
            minMemLineEditItems[currentNewServerType].text() != ""
            and maxMemLineEditItems[currentNewServerType].text() != ""
        ):
            # 是否是数字
            if (
                minMemLineEditItems[currentNewServerType].text().isdigit()
                and maxMemLineEditItems[currentNewServerType].text().isdigit()
            ):
                # 是否为整数
                if (
                    int(minMemLineEditItems[currentNewServerType].text()) % 1 == 0
                    and int(maxMemLineEditItems[currentNewServerType].text()) % 1 == 0
                ):
                    # 是否为整数
                    if int(minMemLineEditItems[currentNewServerType].text()) <= int(
                        maxMemLineEditItems[currentNewServerType].text()
                    ):
                        # 设!
                        configureServerVariables.minMem = int(
                            minMemLineEditItems[currentNewServerType].text()
                        )
                        configureServerVariables.maxMem = int(
                            maxMemLineEditItems[currentNewServerType].text()
                        )
                        return "内存检查: 正常", 0

                    else:
                        return "内存检查: 出错, 最小内存必须小于等于最大内存", 1
                else:
                    return "内存检查: 出错, 不为整数", 1
            else:
                return "内存检查: 出错, 不为数字", 1
        else:
            return "内存检查: 出错, 内容为空", 1

    def checkCoreSet(self):
        """检查核心设置"""
        if (
            configureServerVariables.corePath != ""
            and configureServerVariables.coreFileName != ""
        ):
            return "核心检查: 正常", 0
        else:
            return "核心检查: 出错，缺失", 1

    def checkServerNameSet(self, currentNewServerType):
        """检查服务器名称设置"""
        errText = "服务器名称检查: 出错"
        isError: int
        illegalServerCharacterList = ["\\", "/", ":", "*", "?", '"', "<", ">", "|"]
        serverNameLineEditItems = [
            None,
            self.noobServerNameLineEdit,
            self.extendedServerNameLineEdit,
        ]
        illegalServerNameList = [
            "aux",
            "prn",
            "con",
            "lpt1",
            "lpt2",
            "nul",
            "com0",
            "com1",
            "com2",
            "com3",
            "com4",
            "com5",
            "com6",
            "com7",
            "com8",
            "com9",
        ]

        for i in range(len(illegalServerNameList)):
            if (
                illegalServerNameList[i]
                == serverNameLineEditItems[currentNewServerType].text()
            ):
                errText += "，名称与操作系统冲突"
                isError = 1
                break
            else:
                isError = 0
        for eachIllegalServerCharacter in illegalServerCharacterList:
            if (
                not eachIllegalServerCharacter
                in serverNameLineEditItems[currentNewServerType].text()
            ):
                pass
            else:
                errText += "，名称含有不合法字符"
                isError = 1
                break
        if serverNameLineEditItems[currentNewServerType].text() == "":
            errText += "，未填写"
            isError = 1
        if isError == 1:
            return errText, isError
        else:
            configureServerVariables.serverName = serverNameLineEditItems[
                currentNewServerType
            ].text()
            return "服务器名称检查: 正常", isError

    def checkDeEncodingSet(self, currentNewServerType):
        """检查编码设置"""
        # Noob
        if currentNewServerType == 1:
            configureServerVariables.consoleOutputDeEncoding = (
                configureServerVariables.consoleDeEncodingList[0]
            )
            configureServerVariables.consoleInputDeEncoding = (
                configureServerVariables.consoleDeEncodingList[0]
            )
            return "编码检查：正常（自动处理）", 0
        # Extended
        elif currentNewServerType == 2:
            configureServerVariables.consoleOutputDeEncoding = (
                configureServerVariables.consoleDeEncodingList[
                    self.extendedOutputDeEncodingComboBox.currentIndex()
                ]
            )
            configureServerVariables.consoleInputDeEncoding = (
                configureServerVariables.consoleDeEncodingList[
                    self.extendedInputDeEncodingComboBox.currentIndex()
                ]
            )
            return "编码检查：正常（手动设置）", 0

    def checkJVMArgSet(self, currentNewServerType):
        """检查JVM参数设置"""
        if currentNewServerType == 2:
            # 有写
            if self.JVMArgPlainTextEdit.toPlainText() != "":
                configureServerVariables.jvmArg = (
                    self.JVMArgPlainTextEdit.toPlainText().split(" ")
                )
                return "JVM参数检查：正常（手动设置）", 0
            # 没写
            else:
                configureServerVariables.jvmArg.append(
                    "-Dlog4j2.formatMsgNoLookups=true"
                )
                return "JVM参数检查：正常（无手动参数，自动启用log4j2防护）", 0
        elif currentNewServerType == 1:
            configureServerVariables.jvmArg.append("-Dlog4j2.formatMsgNoLookups=true")
            return "JVM参数检查：正常（无手动参数，自动启用log4j2防护）", 0

    def checkMemUnitSet(self, currentNewServerType):
        """检查JVM内存堆单位设置"""
        if currentNewServerType == 1:
            configureServerVariables.memUnit = configureServerVariables.memUnitList[0]
            return "JVM内存堆单位检查：正常（自动设置）", 0
        elif currentNewServerType == 2:
            configureServerVariables.memUnit = configureServerVariables.memUnitList[
                self.extendedMemUnitComboBox.currentIndex()
            ]
            return "JVM内存堆单位检查：正常（手动设置）", 0

    def setJavaPath(self, selectedJavaPath):
        """选择Java后处理Java路径"""
        configureServerVariables.selectedJavaPath = selectedJavaPath

    def setJavaVer(self, selectedJavaVer):
        """选择Java后处理Java版本"""
        configureServerVariables.selectedJavaVersion = selectedJavaVer
        javaVersionLabelItems = [
            None,
            self.noobJavaInfoLabel,
            self.extendedJavaInfoLabel,
        ]
        javaVersionLabelItems[self.newServerStackedWidget.currentIndex()].setText(
            f"已选择，版本{selectedJavaVer}"
        )

    def finishNewServer(self):
        """完成新建服务器的检查触发器"""
        # 定义
        currentNewServerType = self.newServerStackedWidget.currentIndex()
        # 检查
        javaResult = self.checkJavaSet()
        memResult = self.checkMemSet(currentNewServerType)
        coreResult = self.checkCoreSet()
        serverNameResult = self.checkServerNameSet(currentNewServerType)
        consoleDeEncodingResult = self.checkDeEncodingSet(currentNewServerType)
        jvmArgResult = self.checkJVMArgSet(currentNewServerType)
        memUnitResult = self.checkMemUnitSet(currentNewServerType)
        totalResultMsg = (
            f"{javaResult[0]}\n"
            f"{memResult[0]}\n"
            f"{memUnitResult[0]}\n"
            f"{coreResult[0]}\n"
            f"{serverNameResult[0]}\n"
            f"{consoleDeEncodingResult[0]}\n"
            f"{jvmArgResult[0]}"
        )
        totalResultIndicator = [
            javaResult[1],
            memResult[1],
            memUnitResult[1],
            coreResult[1],
            serverNameResult[1],
            consoleDeEncodingResult[1],
            jvmArgResult[1],
        ]
        # 错了多少
        errCount = 0
        for indicator in totalResultIndicator:
            if indicator == 1:
                errCount += 1
            else:
                pass
        # 如果出错
        if errCount != 0:
            title = f"创建服务器失败！有{errCount}个问题。"
            content = f"{totalResultMsg}\n----------------------------\n请根据上方提示，修改后再尝试保存。\n如果确认自己填写的没有问题，请联系开发者。"
            w = MessageBox(title, content, self)
            w.yesButton.setText("好的")
            w.cancelButton.setParent(None)
            w.exec()
        else:
            totalJVMArg: str = "\n".join(configureServerVariables.jvmArg)
            title = f"请再次检查你设置的参数是否有误："
            content = (
                f"{totalResultMsg}\n"
                f"----------------------------\n"
                f"Java：{configureServerVariables.selectedJavaPath}\n"
                f"Java版本：{configureServerVariables.selectedJavaVersion}\n"
                f"内存：{str(configureServerVariables.minMem)}{configureServerVariables.memUnit}~{str(configureServerVariables.maxMem)}{configureServerVariables.memUnit}\n"
                f"服务器核心：{configureServerVariables.corePath}\n"
                f"服务器核心文件名：{configureServerVariables.coreFileName}\n"
                f"输出编码设置：{self.extendedOutputDeEncodingComboBox.itemText(configureServerVariables.consoleDeEncodingList.index(configureServerVariables.consoleOutputDeEncoding))}\n"
                f"输入编码设置：{self.extendedInputDeEncodingComboBox.itemText(configureServerVariables.consoleDeEncodingList.index(configureServerVariables.consoleInputDeEncoding))}\n"
                f"JVM参数：\n"
                f"    {totalJVMArg}\n"
                f"服务器名称：{configureServerVariables.serverName}"
            )
            w = MessageBox(title, content, self)
            w.yesButton.setText("无误，添加")
            w.yesSignal.connect(self.confirmForgeServer)
            w.cancelButton.setText("我再看看")
            w.exec()

    def confirmForgeServer(self):
        w = MessageBox(
            "这是不是一个Forge服务器？", "由于Forge的安装比较离谱，所以我们需要询问您以对此类服务器进行特殊优化。", self
        )
        w.yesButton.setText("是")
        w.cancelButton.setText("不是")
        w.cancelSignal.connect(self.saveNewServer)
        w.yesSignal.connect(self.setForge)
        w.exec()

    def setForge(self):
        configureServerVariables.serverType = "forge"
        self.saveNewServer()

    def saveNewServer(self):
        """真正的保存服务器函数"""
        exit0Msg = f'添加服务器"{configureServerVariables.serverName}"成功！'
        exit1Msg = f'添加服务器"{configureServerVariables.serverName}"失败！'
        exitCode = 0

        # 检查JVM参数防止意外无法启动服务器
        for arg in configureServerVariables.jvmArg:
            if arg == "" or arg == " ":
                configureServerVariables.jvmArg.pop(
                    configureServerVariables.jvmArg.index(arg)
                )

        serverConfig = {
            "name": configureServerVariables.serverName,
            "core_file_name": configureServerVariables.coreFileName,
            "java_path": configureServerVariables.selectedJavaPath,
            "min_memory": configureServerVariables.minMem,
            "max_memory": configureServerVariables.maxMem,
            "memory_unit": configureServerVariables.memUnit,
            "jvm_arg": configureServerVariables.jvmArg,
            "output_decoding": configureServerVariables.consoleOutputDeEncoding,
            "input_encoding": configureServerVariables.consoleInputDeEncoding,
            "icon": "Grass.png",
        }

        # 新建文件夹
        mkdir(f"Servers//{configureServerVariables.serverName}")

        # 写入全局配置
        try:
            with open(
                r"MCSL2/MCSL2_ServerList.json", "r", encoding="utf-8"
            ) as globalServerListFile:
                # old
                globalServerList = loads(globalServerListFile.read())
                globalServerListFile.close()

            with open(
                r"MCSL2/MCSL2_ServerList.json", "w+", encoding="utf-8"
            ) as newGlobalServerListFile:
                # 添加新的
                globalServerList["MCSLServerList"].append(serverConfig)
                newGlobalServerListFile.write(dumps(globalServerList, indent=4))
            exitCode = 0
        except Exception as e:
            exitCode = 1
            exit1Msg += f"\n{e}"

        # 写入单独配置
        try:
            if not settingsController.fileSettings["onlySaveGlobalServerConfig"]:
                with open(
                    f"Servers//{configureServerVariables.serverName}//MCSL2ServerConfig.json",
                    "w+",
                    encoding="utf-8",
                ) as serverListFile:
                    serverListFile.write(dumps(serverConfig, indent=4))
            else:
                InfoBar.info(
                    title="功能提醒",
                    content=f"您在设置中开启了“只保存全局服务器设置”。\n将不会保存单独服务器设置。\n这有可能导致服务器迁移较为繁琐。",
                    orient=Qt.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=3000,
                    parent=self,
                )
            exitCode = 0
        except Exception as e:
            exitCode = 1
            exit1Msg += f"\n{e}"

        # 复制核心
        try:
            copy(
                configureServerVariables.corePath,
                f"./Servers/{configureServerVariables.serverName}/{configureServerVariables.coreFileName}",
            )
        except Exception as e:
            exitCode = 1
            exit1Msg += f"\n{e}"

        # 自动同意Mojang Eula
        if settingsController.fileSettings["acceptAllMojangEula"]:
            tmpServerName = serverVariables.serverName
            serverVariables.serverName = configureServerVariables.serverName
            MinecraftEulaInfoBar = InfoBar(
                icon=FIF.GITHUB,
                title="功能提醒",
                content="您开启了“创建时自动同意服务器的Eula”功能。\n如需要查看Minecraft Eula，请点击右边的按钮。",
                orient=Qt.Horizontal,
                isClosable=True,
                duration=10000,
                position=InfoBarPosition.TOP,
                parent=self,
            )
            MinecraftEulaInfoBar.addWidget(
                HyperlinkButton(
                    url="https://aka.ms/MinecraftEULA",
                    text="Eula",
                    parent=MinecraftEulaInfoBar,
                    icon=FIF.LINK,
                )
            )
            MinecraftEulaInfoBar.show()
            MojangEula().acceptEula()
            serverVariables.serverName = tmpServerName

        if exitCode == 0:
            InfoBar.success(
                title="成功",
                content=exit0Msg,
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self,
            )
            if configureServerVariables.serverType == "forge":
                self.installingForgeStateToolTip = StateToolTip(
                    "正在安装Forge", "请稍后...", self
                )
                self.installingForgeStateToolTip.move(
                    self.installingForgeStateToolTip.getSuitablePos()
                )
                self.installingForgeStateToolTip.show()
                ForgeInstaller(
                    cwd=f"Servers//{configureServerVariables.serverName}",
                    file=configureServerVariables.coreFileName,
                    java=configureServerVariables.selectedJavaPath,
                    logDecode=settingsController.fileSettings["outputDeEncoding"],
                )
            if settingsController.fileSettings["clearAllNewServerConfigInProgram"]:
                configureServerVariables.resetToDefault()
                if self.newServerStackedWidget.currentIndex() == 1:
                    self.noobJavaInfoLabel.setText("[选择的Java的信息]")
                    self.noobMinMemLineEdit.setText("")
                    self.noobMaxMemLineEdit.setText("")
                    self.noobServerNameLineEdit.setText("")
                elif self.newServerStackedWidget.currentIndex() == 2:
                    self.extendedJavaInfoLabel.setText("[选择的Java的信息]")
                    self.extendedMinMemLineEdit.setText("")
                    self.extendedMaxMemLineEdit.setText("")
                    self.extendedServerNameLineEdit.setText("")
                    self.extendedOutputDeEncodingComboBox.setCurrentIndex(0)
                    self.extendedInputDeEncodingComboBox.setCurrentIndex(0)
                    self.JVMArgPlainTextEdit.setPlainText("")
                InfoBar.info(
                    title="功能提醒",
                    content="”新建服务器后立刻清空相关设置项“已被开启。\n这是一个强迫症功能。如果需要关闭，请转到设置页。",
                    orient=Qt.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=3000,
                    parent=self,
                )

        else:
            InfoBar.error(
                title="失败",
                content=exit1Msg,
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self,
            )

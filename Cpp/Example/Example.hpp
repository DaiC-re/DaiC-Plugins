#pragma once

#include <QObject>
#include "Plugin.h"

class Example : public QObject, public Plugin {
    Q_OBJECT
    Q_PLUGIN_METADATA(IID "com.DaiC.Plugin")
    Q_INTERFACES(Plugin)
public:
    void init() override;
    void run() override;
    void terminate() override;

    std::string name() const override { return "Example"; }
    std::string author() const override { return "DaiC Team"; }
    std::string description() const override { return "Example Cpp Plugin"; }
    std::string version() const override { return "1.0"; }
};

// class CutterSamplePluginWidget : public CutterDockWidget
// {
//     Q_OBJECT
//
// public:
//     explicit CutterSamplePluginWidget(MainWindow *main);
//
// private:
//     QLabel *text;
//
// private slots:
//     void on_seekChanged(RVA addr);
//     void on_buttonClicked();
// };
//
// #endif // CUTTERSAMPLEPLUGIN_H

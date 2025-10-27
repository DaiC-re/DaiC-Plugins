// #include <QLabel>
// #include <QHBoxLayout>
// #include <QPushButton>
// #include <QAction>
// #include <MainWindow.h>

#include "Example.hpp"
#include <iostream>

void Example::terminate()
{
    std::cout << name() << " Terminated cleanly." << std::endl;
}

void Example::init()
{
    std::cout << name() << "Initialized successfully!" << std::endl;
}

void Example::run()
{
    std::cout << "--- Plugin Information ---" << std::endl;
    std::cout << "Name:        " << name() << std::endl;
    std::cout << "Version:     " << version() << std::endl;
    std::cout << "Description: " << description() << std::endl;
    // std::cout << "Author:      " << getattr(self, 'author', 'Unknown')}") << std::endl;
    // std::cout << "Path:        " << __file__}") << std::endl;
    std::cout << "---------------------------" << std::endl;
    // ExampleCppWidget *widget = new (main);
    // main->addPluginDockWidget(widget);
}

// ExampleCppWidget::ExampleCppWidget(MainWindow *main) : CutterDockWidget(main)
// {
//     this->setObjectName("CutterSamplePluginWidget");
//     this->setWindowTitle("Sample C++ Plugin");
//     QWidget *content = new QWidget();
//     this->setWidget(content);
//
//     QVBoxLayout *layout = new QVBoxLayout(content);
//     content->setLayout(layout);
//     text = new QLabel(content);
//     text->setFont(Config()->getFont());
//     text->setSizePolicy(QSizePolicy::Preferred, QSizePolicy::Preferred);
//     layout->addWidget(text);
//
//     QPushButton *button = new QPushButton(content);
//     button->setText("Want a fortune?");
//     button->setSizePolicy(QSizePolicy::Maximum, QSizePolicy::Maximum);
//     button->setMaximumHeight(50);
//     button->setMaximumWidth(200);
//     layout->addWidget(button);
//     layout->setAlignment(button, Qt::AlignHCenter);
//
//     // connect(Core(), &CutterCore::seekChanged, this, &CutterSamplePluginWidget::on_seekChanged);
//     // connect(button, &QPushButton::clicked, this, &CutterSamplePluginWidget::on_buttonClicked);
// }

// void CutterSamplePluginWidget::on_seekChanged(RVA addr)
// {
//     Q_UNUSED(addr);
//     RzCoreLocked core(Core());
//     TempConfig tempConfig;
//     tempConfig.set("scr.color", 0);
//     QString disasm = Core()->disassembleSingleInstruction(Core()->getOffset());
//     QString res = fromOwnedCharPtr(rz_core_clippy(core, disasm.toUtf8().constData()));
//     text->setText(res);
// }
//
// void CutterSamplePluginWidget::on_buttonClicked()
// {
//     RzCoreLocked core(Core());
//     auto fortune = fromOwned(rz_core_fortune_get_random(core));
//     if (!fortune) {
//         return;
//     }
//     QString res = fromOwnedCharPtr(rz_core_clippy(core, fortune.get()));
//     text->setText(res);
// }

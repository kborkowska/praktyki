#include <iostream>
//#include <string>
//#include <QApplication>
//#include <QLabel>
//#include <QWidget>
#include <QtGui>
#include <Qt>

//using namespace sd;

class GUI: QWidget{

public:
	GUI(): QWidget(){
		
		this->setSize();
		this->createSlider();
		this->show();

	}

private:
	static const int sliderWidth = 40;

	void createSlider(int tickInterval=1, int minimum=0, int maximum=10){

		QSlider *slider = new QSlider(Qt::Vertical, this);

		slider->setTickInterval(tickInterval);
		slider->setMinimum(minimum);
		slider->setMaximum(maximum);

		slider->setTickPosition(QSlider::TicksLeft);

		//slider->valueChanged.connect(self.updateGraph)

		slider->resize(this->sliderWidth,this->height()-this->height()*0.15);

	}
	
	void setSize(){

		QRect rec = QApplication::desktop()->screenGeometry();
		this->setGeometry(rec.x(),rec.y(),rec.width()*2/5,rec.height()*2/5);
	}

};

class View{

public:
	//GUI gui;

};


int main(int argc, char *argv[]){

	QApplication app(argc, argv);
	
	GUI gui;
 
	return app.exec();
}

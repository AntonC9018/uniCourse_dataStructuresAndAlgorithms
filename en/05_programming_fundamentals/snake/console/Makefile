CPPFLAGS=-Wall -Werror -Wconversion -Wextra -std=c++20

snake.out: main.o ../common/common.o graphic.o ../common/logic.o controller.o
	g++ -o snake.out main.o ../common/common.o graphic.o ../common/logic.o controller.o $(CPPFLAGS)

main.o: main.cpp ../common/common.h graphic.h ../common/logic.h
	g++ -c main.cpp $(CPPFLAGS)

graphic.o: graphic.cpp graphic.h ../common/logic.h ../common/common.h
	g++ -c graphic.cpp $(CPPFLAGS)

controller.o: controller.cpp controller.h ../common/common.h
	g++ -c controller.cpp $(CPPFLAGS)

../common.o: ../common/common.cpp ../common/common.h
	cd ../common; g++ -c common.cpp $(CPPFLAGS)

../logic.o: ../common/logic.cpp ../common/logic.h ../common/common.h
	cd ../common; g++ -c logic.cpp $(CPPFLAGS)


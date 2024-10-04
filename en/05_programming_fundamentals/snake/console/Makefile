CPPFLAGS=-Wall -Werror -Wconversion -Wextra -std=c++20
INCLUDES=-I../common

snake.out: main.o common.o graphic.o logic.o controller.o
	g++ -o snake.out main.o common.o graphic.o logic.o controller.o $(CPPFLAGS)

main.o: main.cpp common.h graphic.h ../common/logic.h
	g++ -c main.cpp $(CPPFLAGS) $(INCLUDES)

common.o: ../common/common.cpp ../common/common.h
	g++ -c ../common/common.cpp $(CPPFLAGS) $(INCLUDES)

graphic.o: graphic.cpp graphic.h ../common/logic.h ../common/common.h
	g++ -c graphic.cpp $(CPPFLAGS) $(INCLUDES)

controller.o: controller.cpp controller.h ../common/common.h
	g++ -c controller.cpp $(CPPFLAGS) $(INCLUDES)

logic.o: ../common/logic.cpp ../common/logic.h ../common/common.h
	g++ -c ../common/logic.cpp $(CPPFLAGS) $(INCLUDES)


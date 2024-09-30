CPPFLAGS=-Wall -Werror -Wconversion -Wextra -std=c++20

snake.out: main.o common.o graphic.o logic.o
	g++ -o snake.out main.o common.o graphic.o logic.o $(CPPFLAGS)

main.o: main.cpp common.h graphic.h logic.h
	g++ -c main.cpp $(CPPFLAGS)

common.o: common.cpp common.h
	g++ -c common.cpp $(CPPFLAGS)

graphic.o: graphic.cpp graphic.h logic.h common.h
	g++ -c graphic.cpp $(CPPFLAGS)

logic.o: logic.cpp logic.h common.h
	g++ -c logic.cpp $(CPPFLAGS)


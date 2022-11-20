CC=gcc
CFLAGS=-Wall -Werror -O3 -fPIC
SOURCE_DIR=src
BUILD_DIR=lib

build: $(SOURCE_DIR)/matmul.c $(SOURCE_DIR)/matmul.h
	mkdir $(BUILD_DIR)
	$(CC) -shared -o $(BUILD_DIR)/matmul.so $(SOURCE_DIR)/matmul.c $(CFLAGS)

clean:
	rm -rf $(BUILD_DIR)

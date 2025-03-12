test: test.o extras.o
	cc test.o extras.o -o test

extras.o: extras.c
	cc -c extras.c

test.o: test.c llvm-pass-skeleton/build/skeleton/SkeletonPass.so
	clang -fpass-plugin=llvm-pass-skeleton/build/skeleton/SkeletonPass.so -c test.c

llvm-pass-skeleton/build/skeleton/SkeletonPass.so: llvm-pass-skeleton/skeleton/Skeleton.cpp
	make -C llvm-pass-skeleton/build

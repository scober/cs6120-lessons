test: test.c llvm-pass-skeleton/build/skeleton/SkeletonPass.so
	clang -fpass-plugin=llvm-pass-skeleton/build/skeleton/SkeletonPass.so test.c -o test

llvm-pass-skeleton/build/skeleton/SkeletonPass.so: llvm-pass-skeleton/skeleton/Skeleton.cpp
	make -C llvm-pass-skeleton/build

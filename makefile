# Compiler
CXX = g++
# Flags
CXXFLAGS = -fPIC -shared
# Source files
SRCS = main.cpp bindings.cpp
# Output file
OUT = iTTE.so

all: $(OUT)

$(OUT): $(SRCS)
	$(CXX) $(CXXFLAGS) -o $@ $^

clean:
	rm -f $(OUT)

.PHONY: all clean
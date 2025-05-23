# Compiler
CXX = g++ # linux
CXXX = x86_64-w64-mingw32-g++
# Flags
CXXFLAGS = -fPIC -shared -static-libgcc -static-libstdc++
# Source files
SRCS = main.cpp bindings.cpp
# Output file
OUT = iTTE.so
OUT_WIN = iTTE.dll

# output directory
OUT_DIR = lib

all: $(OUT_DIR)/$(OUT) $(OUT_DIR)/$(OUT_WIN)

$(OUT_DIR):
	mkdir -p $(OUT_DIR)

$(OUT_DIR)/$(OUT): $(SRCS) | $(OUT_DIR)
	$(CXX) $(CXXFLAGS) -o $@ $^

$(OUT_DIR)/$(OUT_WIN): $(SRCS) | $(OUT_DIR)
	$(CXXX) $(CXXFLAGS) -o $@ $^

clean:
	rm -f $(OUT_DIR)/$(OUT) $(OUT_DIR)/$(OUT_WIN)

.PHONY: all clean
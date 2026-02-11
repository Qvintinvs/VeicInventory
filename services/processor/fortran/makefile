FC      := gfortran
SRC     := emiss.f90
BIN     := build/emiss.exe
FLAGS   := -w -g0 -O2 -mtune=native

.PHONY: all clean run

all: $(BIN)

$(BIN): $(SRC)
	@command -v $(FC) >/dev/null || (echo "❌ $(FC) not found"; exit 1)
	@mkdir -p $(dir $@)
	@$(FC) $(FLAGS) $< -o $@ || (echo "❌ Failed to compile $<"; exit 1)
	@echo "Build successful: $@"

run: $(BIN)
	@bash run.sh

clean:
	@rm -rf build
	@echo "Cleaned build directory"

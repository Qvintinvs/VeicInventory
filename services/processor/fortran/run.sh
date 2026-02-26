#!/bin/bash
set -e

# Paths to data directories
resources_dir="$GHG_EMIS_DIR"
wrf_emis="$WRF_EMIS_DIR"

# Absolute path to the project root
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

fortran_executable="$PROJECT_ROOT/fortran/build/emiss.exe"

cd "$PROJECT_ROOT/resources" || exit 1

if [ ! -f "$fortran_executable" ]; then
  echo "❌ Executable not found. Run 'make' first."
  exit 1
fi

# Run emiss.exe from the build folder, while being inside data/raw
"$fortran_executable" || {
  echo "❌ Falha ao executar emiss.exe"
  exit 1
}

# Check if wrfem_* files were generated
if ls "$resources_dir/wrfem_"* 1>/dev/null 2>&1; then
  echo "✅ Arquivos binários gerados com sucesso!"
else
  echo "❌ Falha ao gerar arquivos binários wrfem_*"
  exit 1
fi

cd "$wrf_emis" || {
  echo "❌ Falha ao acessar diretório $wrf_emis"
  exit 1
}

# Remove old output files if any
rm -f wrfchemi_* wrfem_* 2>/dev/null

# Copy generated wrfem files to current directory
cp "$resources_dir/wrfem_00to12z_d01" .
cp "$resources_dir/wrfem_12to24z_d01" .

# ======================== 00-12 ========================
echo "⏱️  Processando emissões WRF 00-12"

# Run real.exe for 00-12 window
cp namelist.00_12_real namelist.input
rm -f rsl.* || true
mpirun -np 10 ./real.exe
tail -n 1 rsl.error.0000 || true

# Run convert_emiss.exe for 00-12 window
cp namelist.00_12_convert_emis namelist.input
./convert_emiss.exe
tail -n 1 rsl.error.0000 || true

# Check if the output file was generated
if [ -f "wrfchemi_00z_d01" ]; then
  echo "✅ wrfchemi_00z_d01 criado com sucesso!"
else
  echo "❌ Falha ao criar wrfchemi_00z_d01"
  exit 1
fi

# ======================== 12-24 ========================
echo "⏱️  Processando emissões WRF 12-24"

# Run real.exe for 12-24 window
cp namelist.12_24_real namelist.input
rm -f rsl.* || true
mpirun -np 10 ./real.exe
tail -n 1 rsl.error.0000 || true

# Run convert_emiss.exe for 12-24 window
cp namelist.12_24_convert_emis namelist.input
./convert_emiss.exe
tail -n 1 rsl.error.0000 || true

# Check if the output file was generated
if [ -f "wrfchemi_12z_d01" ]; then
  echo "✅ wrfchemi_12z_d01 criado com sucesso!"
else
  echo "❌ Falha ao criar wrfchemi_12z_d01"
  exit 1
fi

# ======================== Final copy ========================
cd "$emis_emis" || {
  echo "❌ Falha ao acessar $emis_emis"
  exit 1
}

# Copy final output files
cp "$wrf_emis/wrfchemi_00z_d01" .
cp "$wrf_emis/wrfchemi_12z_d01" .

echo "🏁 Finalizado com sucesso."

cd - >/dev/null

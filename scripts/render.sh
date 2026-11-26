#!/usr/bin/env bash
# Renderiza todos os .puml do repo em diagramas-render/ (estrutura espelhada)
# e verifica erros de sintaxe. Uso: bash scripts/render.sh
set -euo pipefail
cd "$(dirname "$0")/.."

rm -rf diagramas-render
mkdir -p diagramas-render
find docs -name "*.puml" | while read -r f; do
  out="diagramas-render/${f#docs/}"
  mkdir -p "$(dirname "$out")"
  plantuml -tpng -o "$(realpath -m "$(dirname "$out")")" "$f" || {
    echo "ERRO de sintaxe: $f" >&2
    exit 1
  }
done
echo "Renderizados:"
find diagramas-render -name "*.png" | sort
